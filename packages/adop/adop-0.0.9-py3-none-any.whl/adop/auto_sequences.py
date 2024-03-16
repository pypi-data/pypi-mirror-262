import logging
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from flask import Flask, Request

from . import (
    deploy_state,
    downloaders,
    exceptions,
    hooks,
    store_payload,
    tags,
    unpack_payload,
    verify_payload,
)

logger = logging.getLogger(__name__)
workers = ThreadPoolExecutor(10)


def handle_zip_in_threadpool(
    app: Flask, request: Request, root: str, store_data: bool, unpack_data: bool
):
    """
    Passes `handle_zip` into a `~concurrent.futures.ThreadPoolExecutor` and
    yields the result using a `~queue.Queue`. This is done to ensure that
    `handle_zip` will complete, even if the client stops to iterate.

    :return: A generator
    """

    def fn(out: Queue):
        try:
            _handle_zip = handle_zip(app, request, root, store_data, unpack_data)
            for res in _handle_zip:
                out.put(res)
                logger.info(res)
        except Exception as err:
            out.put(err)
            logger.exception(err)
        out.put(StopIteration)

    out = Queue()
    workers.submit(fn, out)
    return iter(out.get, StopIteration)


def handle_zip(
    app: Flask, request: Request, root: str, store_data: bool, unpack_data: bool
):
    """
    Yields result from `deploy_zip_sequence` and
    updates ``app.config["shared_progress_dict"]`` with progression
    and logs.

    :returns: A generator
    """
    progress = None
    _handle_zip = deploy_zip_sequence(app, request, root, store_data, unpack_data)

    res = next(_handle_zip)

    if isinstance(res, dict) and "root" in res and res["root"]:
        with app.config["shared_lock"]:
            progress = app.config["shared_progress_dict"][res["root"]] = {}
            log = progress["log"] = []
    yield res

    for res in _handle_zip:
        if isinstance(res, dict):
            with app.config["shared_lock"]:
                if progress:
                    progress.update(res)
        else:
            with app.config["shared_lock"]:
                if progress:
                    log.append(res)
        yield res


def deploy_zip_sequence(
    app: Flask, request: Request, root: str, store_data: bool, unpack_data: bool
):
    """
    Handle storing and unpacking of zip files.

    Returns a generator.

        Yield protocol:

        - if type is `str`: log message.
        - if type is `dict`: result or progress.
        - first result is a "in progress" dict with keys: progress, root
        - final result is a dict with following keys: result, result_code, root

    :return: A generator
    """

    try:
        result = {"root": root, "result": "In progress", "result_code": 2}

        yield {"root": root}  # first result: returns only root
        yield f"root: {root}"

        if not root:
            raise exceptions.Fail("HTTP url <root> not found")

        headers = dict(request.headers)

        remote_info = {
            "remote_address": request.remote_addr,
            "remote_user": request.remote_user,
        }

        if store_data:
            payload = request.get_data()
            headers["Content-Length"] = request.headers.get("Content-Length", "0")
            tag = request.headers.get("Zip-Tag", "")

            yield "store data"
            cache_file, cache_id = store_payload.store(
                payload, app.config["cache_root"], root, tag, remote_info
            )

            yield from verify_payload.verify_content(
                int(headers.get("Content-Length", "0")),
                len(payload),
                cache_file.stat().st_size,
            )
            if app.config["keep_on_disk"] > 0:
                yield from store_payload.auto_delete(
                    app.config["cache_root"], app.config["keep_on_disk"], root
                )
        else:
            cache_file, cache_id, tag = store_payload.find_file_from_headers(
                app.config["cache_root"], root, headers
            )

        root_dir_name = unpack_payload.extract_root_dir_name(cache_file)
        yield from verify_payload.verify_root(
            root_dir_name, root, headers.get("Zip-Root", "")
        )

        if store_data and tag:
            yield f"update tag: {tag}"
            with app.config["shared_lock"]:
                tags.store(root, cache_id, tag, app.config["cache_root"])

        if unpack_data:
            pre_deploy = hooks.run_hook(
                f"hooks:{root}", "hook:pre-deploy", root, locals()
            )
            if pre_deploy is not None:
                yield f"pre-deploy result code {pre_deploy}"
                if not pre_deploy == 0:
                    raise exceptions.Fail(
                        f"abort: pre-hook exited with return-code {pre_deploy}"
                    )
            yield from unpack_payload.unpack(
                cache_file, app.config["deploy_root"], root
            )

            with app.config["shared_lock"]:
                deploy_state.store(
                    root,
                    cache_file,
                    cache_id,
                    app.config["deploy_root"],
                )
            post_deploy = hooks.run_hook(
                f"hooks:{root}", "hook:post-deploy", root, locals()
            )
            if post_deploy is not None:
                yield f"post-deploy result code: {post_deploy}"

        result = {"root": root, "result": "Success", "result_code": 0}
    except exceptions.Fail as err:
        result = {"root": root, "result": str(err), "result_code": 1}
    except Exception as err:
        logger.exception(err)
        result = {"root": root, "result": "Fail", "result_code": 1}
    finally:
        yield result


def client_install_zip_sequence(
    install_data: dict,
    keep_on_disk: int,
    remote_data: list[dict],
    requires_data: dict,
    extra_data: dict,
):
    """
    Handle unpacking/installation of zip files in client computers.

    Returns a generator.

        Yield protocol:

        - if type is `str`: log message.
        - if type is `dict`: result or progress.

    :param dict[str, str] install_data: install path and cache path
    :param list[dict] remote_data: list of remote url and token
    :param dict[str, str] requires_data: root and sha246
    :return: A generator
    """
    # requires_data: dict[str, str],

    install_section = install_data["install_section"]
    install_root = install_data["install_root"]
    cache_root = install_data["cache_root"]

    for root, shasum in requires_data.items():
        yield {"root": root}  # first result: returns only root
        yield f"checking {root}={shasum[:15]}..."

        if shasum.startswith("tag:"):
            headers = {"Zip-Tag": shasum.split(":", 1)[1].strip()}
        elif shasum.startswith("sha256:"):
            headers = {"Zip-Sha256": shasum.split(":", 1)[1].strip()}
        else:
            raise exceptions.CommandFail(
                "Only tag or sha256 is supported in the [requires] section. "
                f"ie. {root} = sha256:AABBCC"
            )

        yield f"using cache_root: {cache_root}"
        already_downloaded = False
        try:
            cache_file, cache_id, tag = store_payload.find_file_from_headers(
                cache_root, root, headers
            )
            already_downloaded = True
            yield f"{root} already downloaded."
        except exceptions.CacheNotFound:
            cache_file, cache_id, tag = yield from downloaders.api_download(
                cache_root, remote_data, root, headers
            )
        except exceptions.Fail as err:
            raise exceptions.CommandFail(err)

        if not already_downloaded:
            if keep_on_disk > 0:
                yield from store_payload.auto_delete(cache_root, keep_on_disk, root)

            root_dir_name = unpack_payload.extract_root_dir_name(cache_file)
            if root in extra_data:
                zip_root = extra_data[root].get("Zip-Root", root_dir_name)
            else:
                zip_root = root_dir_name
            yield from verify_payload.verify_root(root_dir_name, root, zip_root)

            if tag:
                yield f"update tag: {tag}"
                tags.store(root, cache_id, tag, cache_root)

        yield f"using install_root: {install_root}"

        transform_root = hooks.transform_root(install_section, root, locals())
        transformed_root = transform_root if transform_root else root

        state_config, *_ = deploy_state.get_config(install_root)
        if state_config.has_option(transformed_root, "source_hash"):
            if state_config.get(transformed_root, "source_hash") == cache_id:
                if transform_root:
                    yield f"{root} already installed as {transformed_root}."
                else:
                    yield f"{root} already installed."
                continue

        yield from unpack_payload.unpack(cache_file, install_root, transformed_root)

        deploy_state.store(
            transformed_root,
            cache_file,
            cache_id,
            install_root,
        )
        yield f"{transformed_root} installation complete."
