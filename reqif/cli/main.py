import logging
import os
import sys

try:
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if not os.path.isdir(ROOT_PATH):
        raise FileNotFoundError(ROOT_PATH)
    sys.path.append(ROOT_PATH)

    from reqif.cli.cli_arg_parser import create_reqif_args_parser
    from reqif.commands.anonymize.anonymize import AnonymizeCommand
    from reqif.commands.dump.dump import DumpCommand
    from reqif.commands.format.format import FormatCommand
    from reqif.commands.passthrough.passthrough import PassthroughCommand
    from reqif.commands.validate.validate import ValidateCommand
    from reqif.commands.version.version_command import VersionCommand

except FileNotFoundError:
    print("error: could not locate reqif's root folder.")  # noqa: T201
    sys.exit(1)


class _LowercaseLevelFormatter(logging.Formatter):
    """
    Renders log records the way the CLI used to print() them, e.g.
    "warning: Unknown child tag: FOO." with a lowercase level prefix.
    """

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = record.levelname.lower()
        return super().format(record)


def main() -> None:
    # How to make python 3 print() utf8
    # https://stackoverflow.com/a/3597849/598057
    # sys.stdout.reconfigure(encoding='utf-8') for Python 3.7
    sys.stdout = open(  # pylint: disable=bad-option-value,consider-using-with
        1, "w", encoding="utf-8", closefd=False
    )

    # The reqif library logs through the "reqif" logger hierarchy and emits
    # nothing by default. The CLI shows the library's warnings on stdout in
    # the same format the CLI printed them before the library switched to
    # logging. The handler is constructed after the sys.stdout reassignment
    # above so that it writes to the UTF-8-configured stream.
    reqif_log_handler = logging.StreamHandler(stream=sys.stdout)
    reqif_log_handler.setFormatter(
        _LowercaseLevelFormatter("%(levelname)s: %(message)s")
    )
    logging.getLogger("reqif").addHandler(reqif_log_handler)
    logging.getLogger("reqif").setLevel(logging.WARNING)

    parser = create_reqif_args_parser()

    if parser.is_passthrough_command:
        PassthroughCommand.execute(parser.get_passthrough_config())
    elif parser.is_anonymize_command:
        AnonymizeCommand.execute(parser.get_anonymize_config())
    elif parser.is_dump_command:
        DumpCommand.execute(parser.get_dump_config())
    elif parser.is_format_command:
        FormatCommand.execute(parser.get_format_config())
    elif parser.is_validate_command:
        ValidateCommand.execute(parser.get_validate_config())
    elif parser.is_version_command:
        VersionCommand.execute()
    else:
        raise NotImplementedError(parser) from None


if __name__ == "__main__":
    main()
