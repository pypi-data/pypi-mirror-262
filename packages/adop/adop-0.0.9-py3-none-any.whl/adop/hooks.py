import os
import pathlib
import shlex
import subprocess

from . import exceptions


class register:
    """
    A class that acts as a global singelton. Get a dict of hooks by
    calling `register.hooks`
    """

    hooks = {}
    names = {}
    callables = {}
    "List of registered hooks"

    @classmethod
    def hook_entrypoint(cls, section: str, option: str, entrypoint: str):
        if entrypoint:
            if ":" not in entrypoint:
                raise exceptions.CommandFail(
                    f"Hook configuration error: {entrypoint}: "
                    "hook option formatting error."
                )
            entrypoint_type = entrypoint.rsplit(":", 1)[0]
            if entrypoint_type not in (
                "builtins:basedir",  # TODO: change this
                "builtins",
                "run",
            ):
                raise exceptions.CommandFail(
                    f"Hook configuration error: {entrypoint}: "
                    "Only 'builtins:' and 'run:' hooks is supported for now."
                )
            if section not in cls.hooks:
                cls.hooks[section] = {}
                cls.names[section] = {}
            if entrypoint in cls.callables:
                cls.hooks[section][option] = cls.callables[entrypoint]
                cls.names[section][option] = entrypoint
            elif entrypoint_type in cls.callables:
                cls.hooks[section][option] = cls.callables[entrypoint_type]
                cls.names[section][option] = entrypoint
            else:
                raise exceptions.CommandFail(
                    f"Hook configuration error: {entrypoint} not found"
                )

    @classmethod
    def hook_callable(cls, name: str):
        """
        A simple decorator to register hook `callable`.
        Get a dict of hook callables by calling `register.callables`.

        .. code-block:: py

            @register.hook_function("function:print_debugger")
            def print_debugger_func(*args, **kwargs):
                print(args, kwargs)
                return args, kwargs
        """

        def wrap(c):
            cls.callables[name] = c
            return c

        return wrap


@register.hook_callable("run")
def run_subprocess(name: str, root: str, *args, **kwargs) -> int:
    """
    Run a subprocess.

    :returns: return_code.

    Example:

    .. code-block:: ini

        [hooks:mylib]
        hook:pre-deploy = run:pre-deploy.sh
        hook:post-deploy = run:post-deploy.sh

    """
    key, cmd = name.rsplit(":", 1)
    envs = {"ADOP_ROOT": root}
    try:
        returncode = subprocess.run(shlex.split(cmd), env=envs).returncode
    except Exception as err:
        raise exceptions.Fail(f"Error in hook: {err}")
    return returncode


def run_hook(section: str, opt: str, root: str, locals: dict):
    "Search for hook and call it if found. Returns the result"
    fn_result = None
    if section in register.hooks:
        if opt in register.hooks[section]:
            fn = register.hooks[section][opt]
            name = register.names[section][opt]
            fn_result = fn(name, root, locals)
    return fn_result


@register.hook_callable("builtins:basedir:add-as-prefix")
def builtins_basedir(root, *args, **kwargs):
    """
    Add cwd base name as a prefix to root name.
    Should only be used with the ``hook:transform-root`` option
    for now:

    .. code-block:: ini

        [install:subprojdir]
        hook:transform-root = builtins:basedir:add-as-prefix

    """
    cwd = pathlib.Path.cwd()
    new_root = f"{cwd.stem}_{root}"
    return new_root


def transform_root(install_to: str, root: str, locals: dict) -> str:
    "Search for a ``hook:transform-root`` and return the result"
    opt = "hook:transform-root"
    transform_root = ""

    if install_to in register.hooks:
        if opt in register.hooks[install_to]:
            fn = register.hooks[install_to][opt]
            transform_root = fn(root, locals)
    return transform_root


def getenv(key: str) -> str:
    """
    Return the value of the environment variable ``key``
    if it exists, or ``""`` if not.

    .. code-block:: ini

        [remote:myremote]
        url = myurl
        token = ${hook:env:REMOTE_TOKEN}

    """
    return os.getenv(key=key, default="")


def getkeyring(key: str) -> str:
    """
    Return the password of the given keyring service
    if it exists, or ``""`` if not.

    :param key: a string formatted as ``service:user``

    .. code-block:: ini

        [remote:myremote]
        url = myurl
        token = ${hook:keyring:SERVICE:USER}
    """
    try:
        import keyring
    except ModuleNotFoundError:
        return ""
    service, username = key.split(":", 1)
    pwd = keyring.get_password(service, username)
    return pwd if pwd else ""
