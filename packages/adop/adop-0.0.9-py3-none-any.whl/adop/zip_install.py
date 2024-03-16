import configparser
import json
import os
import pathlib

from . import __version__, exceptions, parse_config, zip_install_sequences


# TODO: Improve this
def compare_version(version: str, requires: str) -> bool:
    """
    Compares `version` and `requires`.

    :returns: `True` if `version` is greater than or equal to `requires`.
    """

    v1 = tuple(int(i) for i in version.split(".") if i.isdigit())
    v2 = tuple(int(i) for i in requires.split(".") if i.isdigit())
    return v1 >= v2


def install(file: str, config: str, cwd: str, remote: list[str], install: str):
    """
    Parses :term:`root` data from `file`, downloads the required zip-files
    from `remote` into the local cache, and unpack the files
    into the `install` location.
    """

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, "", "")

    installer = Installer(local_config)

    requires_file_data = installer.parse_requires_file(file)
    install_data = installer.parse_install_to(install, requires_file_data)
    remote_data = installer.parse_remotes(remote, requires_file_data)

    requires_data = requires_file_data["requires"]
    extra_data = {}

    installer.install(install_data, remote_data, requires_data, extra_data)


class RequireFile:
    """
    This class parses the contents of ``requires.ini``.
    """

    def __init__(self, local_config: configparser.ConfigParser) -> None:
        self.config = local_config

    def parse_requires_file(self, requires_file: str) -> dict:
        """
        Parses the `requires.ini` file into a dict.

        .. code-block:: py

            {
                "requires": {},
                "options": {
                    "install": "",
                    "remote": "",
                }
            }

        :returns: data from the requires-file.

        :rtype: dict[str, dict]
        """
        if "=" in requires_file and " " not in requires_file:
            requires_string = f"[requires]\n{requires_file}"
        else:
            requires_file_path = pathlib.Path.cwd().joinpath(requires_file)
            if not requires_file_path.exists():
                raise exceptions.CommandFail(
                    f"Requires-file not found: {requires_file_path}"
                )
            requires_string = requires_file_path.read_text()

        requires = configparser.ConfigParser()
        requires.read_string(requires_string)

        if not requires.has_section("requires"):
            raise exceptions.CommandFail(
                f"Section [requires] is missing in file: {requires_file}"
            )

        if requires.has_option("tool_requires", "adop"):
            required_version = requires.get("tool_requires", "adop")
            if not compare_version(__version__, required_version):
                raise exceptions.CommandFail(
                    f"Required adop version {required_version} is not installed."
                )

        requires_file_data = {
            "options": {
                "install": self.config.get("client", "install", fallback="basedir"),
                "remote": self.config.get("client", "remote", fallback="local"),
            }
        }
        if requires.has_section("options"):
            requires_file_data["options"].update(
                {k: v for k, v in requires.items("options")}
            )

        requires_file_data["requires"] = {k: v for k, v in requires.items("requires")}
        return requires_file_data

    def parse_remotes(self, remote: list[str], requires_data: dict) -> list[dict]:
        """
        Parse the options from the given ``remote:``-section into a dict.
        """
        remote_data = []
        remote_sections = remote if remote else [requires_data["options"]["remote"]]
        for remote_from in remote_sections:
            remote_section = f"remote:{remote_from}"

            if not self.config.has_section(remote_section):
                raise exceptions.CommandFail(
                    f"Configuration error: section [{remote_section}] not defined."
                )

            try:
                remote_data.append(
                    {
                        "url": self.config.get(remote_section, "url"),
                        "token": self.config.get(remote_section, "token"),
                        "insecure": self.config.getboolean(
                            remote_section, "insecure", fallback=False
                        ),
                        "direct": self.config.getboolean(
                            remote_section, "direct", fallback=False
                        ),
                    }
                )
            except configparser.NoOptionError as err:
                raise exceptions.CommandFail(f"Configuration error: {err}")

        return remote_data

    def parse_install_to(self, install: str, requires_data: dict) -> dict:
        """
        Parse the options from the given ``install:``-section into a dict.
        """
        install_to = install if install else requires_data["options"]["install"]
        install_section = f"install:{install_to}"

        if not self.config.has_section(install_section):
            raise exceptions.CommandFail(
                f"Configuration error: section [{install_section}] not defined."
            )
        try:
            install_root = self.config.get(install_section, "install_root")
            cache_root = self.config.get(install_section, "cache_root")
        except configparser.NoOptionError as err:
            raise exceptions.CommandFail(f"Configuration error: {err}")

        install_root = os.path.expanduser(install_root)
        cache_root = os.path.expanduser(cache_root)
        return {
            "install_section": install_section,
            "install_root": install_root,
            "cache_root": cache_root,
        }


class Installer(RequireFile):
    def install(
        self,
        install_data: dict,
        remote_data: list[dict],
        requires_data: dict,
        extra_data: dict,
    ):
        """
        Iterates over `~.zip_install_sequences.client_install_zip_sequence` and print
        the result.
        """

        keep_on_disk = 0
        if self.config.getboolean("auto_delete", "on"):
            keep_on_disk = self.config.getint("auto_delete", "keep_on_disk")

        _handle_zip = zip_install_sequences.client_install_zip_sequence(
            install_data, keep_on_disk, remote_data, requires_data, extra_data
        )

        try:
            for res in _handle_zip:
                if isinstance(res, dict):
                    if "root" in res:
                        print(f"Requires: {res['root']}")
                    elif "result" in res:
                        print(f"{json.dumps(res)}")
                else:
                    print(f"          {res}")
        except exceptions.CommandFail as err:
            print("          ERROR:")
            raise exceptions.CommandFail(f"             {err}")
