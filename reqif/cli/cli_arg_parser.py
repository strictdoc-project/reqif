import argparse


def cli_args_parser() -> argparse.ArgumentParser:
    def formatter(prog):
        return argparse.RawTextHelpFormatter(
            prog, indent_increment=2, max_help_position=4, width=80
        )

    # https://stackoverflow.com/a/19476216/598057
    main_parser = argparse.ArgumentParser()
    main_parser.formatter_class = formatter

    command_subparsers = main_parser.add_subparsers(
        title="command", dest="command"
    )
    command_subparsers.required = True

    # Command – Passthrough
    command_parser_passthrough = command_subparsers.add_parser(
        "passthrough",
        help="Read an SDoc file, then output it again. (used for testing)",
        formatter_class=formatter,
    )
    command_parser_passthrough.add_argument(
        "input_file", type=str, help="Path to the input ReqIF file"
    )

    command_parser_passthrough.add_argument(
        "output_file", type=str, help="Path to the output ReqIF file"
    )

    # Command – Anonimize
    command_parser_anonymize = command_subparsers.add_parser(
        "anonymize",
        help="Read an SDoc file, anonymize it, then output it again.",
        formatter_class=formatter,
    )
    command_parser_anonymize.add_argument(
        "input_file", type=str, help="Path to the input ReqIF file"
    )
    command_parser_anonymize.add_argument(
        "output_file", type=str, help="Path to the anonymized output ReqIF file"
    )

    # Command – Dump
    command_parser_dump = command_subparsers.add_parser(
        "dump",
        help="Read an SDoc file, dump its concents to a raw HTML page.",
        formatter_class=formatter,
    )
    command_parser_dump.add_argument(
        "input_file", type=str, help="Path to the input ReqIF file"
    )

    command_parser_dump.add_argument(
        "output_file", type=str, help="Path to the output HTML file"
    )

    # Command – Format
    command_parser_format = command_subparsers.add_parser(
        "format",
        help=(
            "Read a ReqIF file and pretty-print its contents to "
            "an output file."
        ),
        formatter_class=formatter,
    )
    command_parser_format.add_argument(
        "input_file", type=str, help="Path to an input ReqIF file"
    )
    command_parser_format.add_argument(
        "output_file", type=str, help="Path to an output ReqIF file"
    )

    # Command – Validate
    command_parser_validate = command_subparsers.add_parser(
        "validate",
        help=("Read a ReqIF file and validate its content."),
        formatter_class=formatter,
    )
    command_parser_validate.add_argument(
        "input_file", type=str, help="Path to an input ReqIF file"
    )

    # Command – Version
    command_subparsers.add_parser(
        "version",
        help="Print the version of StrictDoc.",
        formatter_class=formatter,
    )
    return main_parser


class PassthroughCommandConfig:
    def __init__(self, input_file: str, output_file: str):
        self.input_file: str = input_file
        self.output_file: str = output_file


class AnonimizeCommandConfig:
    def __init__(self, input_file: str, output_file: str):
        self.input_file: str = input_file
        self.output_file: str = output_file


class DumpCommandConfig:
    def __init__(self, input_file: str, output_file: str):
        self.input_file: str = input_file
        self.output_file: str = output_file


class FormatCommandConfig:
    def __init__(self, input_file: str, output_file: str):
        self.input_file: str = input_file
        self.output_file: str = output_file


class ValidateCommandConfig:
    def __init__(self, input_file: str):
        self.input_file: str = input_file


class ReqIFArgsParser:
    def __init__(self, args):
        self.args = args

    @property
    def is_passthrough_command(self):
        return self.args.command == "passthrough"

    @property
    def is_anonymize_command(self):
        return self.args.command == "anonymize"

    @property
    def is_dump_command(self):
        return self.args.command == "dump"

    @property
    def is_format_command(self):
        return self.args.command == "format"

    @property
    def is_validate_command(self):
        return self.args.command == "validate"

    @property
    def is_version_command(self):
        return self.args.command == "version"

    def get_passthrough_config(self) -> PassthroughCommandConfig:
        return PassthroughCommandConfig(
            self.args.input_file, self.args.output_file
        )

    def get_anonymize_config(self) -> AnonimizeCommandConfig:
        return AnonimizeCommandConfig(
            self.args.input_file, self.args.output_file
        )

    def get_dump_config(self) -> DumpCommandConfig:
        return DumpCommandConfig(self.args.input_file, self.args.output_file)

    def get_format_config(self) -> FormatCommandConfig:
        return FormatCommandConfig(self.args.input_file, self.args.output_file)

    def get_validate_config(self) -> ValidateCommandConfig:
        return ValidateCommandConfig(self.args.input_file)


def create_reqif_args_parser(testing_args=None) -> ReqIFArgsParser:
    args = testing_args
    if not args:
        parser = cli_args_parser()
        args = parser.parse_args()
    return ReqIFArgsParser(args)
