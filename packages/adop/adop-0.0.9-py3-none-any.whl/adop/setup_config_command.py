import argparse

from . import parse_config


class register:
    """
    A simple decorator to register sub parsers, but also
    acts as a singelton. Get a list of sub parsers by
    calling `register.subparsers` from the `main` function
    """

    subparsers = []
    "List of registered subparsers"

    @classmethod
    def subparser(cls, w):
        "Register sub parser"
        cls.subparsers.append(w)
        return w


def setup(subparsers: argparse.Action):
    """
    Sub parser for the ``config`` argument.
    """
    setup_v1(subparsers, "config", "Config commands")


def setup_v1(subparsers: argparse.Action, name: str, help: str):
    """
    Sub parser for the ``config-v1`` argument.
    """
    parser = subparsers.add_parser(name, help=help)

    subparsers = parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    # get all registered sub parsers and call its function
    for setup in register.subparsers:
        setup(subparsers)


@register.subparser
def setup_init_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config init`` argument.
    """
    parser = subparsers.add_parser("init", help="init options")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-m",
        "--merge",
        dest="merge",
        action="store_true",
        help="Write default values to file",
    )
    parser.set_defaults(func=parse_config.config_init)


@register.subparser
def setup_set_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config set`` argument.
    """
    parser = subparsers.add_parser("set", help="set option")
    # path_or_file
    parser.add_argument(
        "section",
        type=str,
        default="",
        help="section-name in adop.ini",
    )
    parser.add_argument(
        "option",
        type=str,
        default="",
        help="option-name in adop.ini",
    )
    parser.add_argument(
        "value",
        type=str,
        default="",
        help="new value for given option in given section",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_set)


@register.subparser
def setup_get_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config get`` argument.
    """
    parser = subparsers.add_parser("get", help="get option")
    # path_or_file
    parser.add_argument(
        "section",
        type=str,
        default="",
        help="section-name in adop.ini",
    )
    parser.add_argument(
        "option",
        type=str,
        default="",
        help="option-name in adop.ini",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Include default values in result",
    )
    parser.set_defaults(func=parse_config.config_get)


@register.subparser
def setup_list_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config list`` argument.
    """
    parser = subparsers.add_parser("list", help="list options")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Include default values in result",
    )
    parser.set_defaults(func=parse_config.config_list)


@register.subparser
def setup_generate_token_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``generate-token`` argument.
    """
    parser = subparsers.add_parser("generate-token", help="Generate a token")
    parser.set_defaults(func=parse_config.generate_token)


@register.subparser
def setup_import_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config import`` argument.
    """
    parser = subparsers.add_parser("import", help="import options")

    parser.add_argument(
        "file",
        type=str,
        default="./import-config.ini",
        help="import given ini file",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_import)


@register.subparser
def setup_open_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config open`` argument.
    """
    parser = subparsers.add_parser("open", help="open options")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_open)


@register.subparser
def setup_add_remote_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config add-remote`` argument.
    Add a remote named <name> for the server at <URL>.
    """
    parser = subparsers.add_parser(
        "add-remote", help="Add a remote named <name> for the server at <URL>"
    )

    parser.add_argument(
        "name",
        type=str,
        default="",
        help="remote name",
    )
    parser.add_argument(
        "url",
        type=str,
        default="",
        help="remote url",
    )
    parser.add_argument(
        "-p",
        "--token-prompt",
        action="store_true",
        help="prompt for a remote token",
    )
    parser.add_argument(
        "-e",
        "--token-env",
        type=str,
        default="",
        help="get the remote token from environment variable",
    )
    parser.add_argument(
        "-k",
        "--token-keyring",
        type=str,
        default="",
        help="get the remote token from keyring",
    )
    parser.add_argument(
        "-i",
        "--insecure",
        action="store_true",
        help="Allow untrusted certificates",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_add_remote)


@register.subparser
def setup_add_install_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config add-install`` argument.
    Add a install location named <name> at <install_root> with a cache at <cache_root>.
    """
    parser = subparsers.add_parser(
        "add-install",
        help="Add a install location named <name> at <install_root> with a cache at <cache_root>",
    )

    parser.add_argument(
        "name",
        type=str,
        default="",
        help="install name",
    )
    parser.add_argument(
        "install_root",
        type=str,
        default="",
        help="install root path",
    )
    parser.add_argument(
        "cache_root",
        type=str,
        default="",
        help="cache root path",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_add_install)


@register.subparser
def setup_add_autofetch_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``config autofetch`` argument.
    Add a autofetch named <name>.
    """
    parser = subparsers.add_parser(
        "add-autofetch", help="Add a autofetch source named <name>"
    )

    parser.add_argument(
        "name",
        type=str,
        default="",
        help="autofetch name",
    )
    parser.add_argument(
        "root",
        type=str,
        default="",
        help="root name",
    )
    parser.add_argument(
        "check_url",
        type=str,
        default="",
        help="check_url",
    )
    parser.add_argument(
        "payload_url",
        type=str,
        default="",
        help="payload_url",
    )
    parser.add_argument(
        "-H",
        "--headers",
        type=str,
        default="",
        help="headers",
    )
    parser.add_argument(
        "-z",
        "--zip-root",
        type=str,
        default="",
        help="zip_root",
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.set_defaults(func=parse_config.config_add_autofetch_source)
