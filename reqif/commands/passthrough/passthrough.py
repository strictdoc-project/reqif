import os
import sys

from reqif.cli.cli_arg_parser import PassthroughCommandConfig
from reqif.parser import ReqIFParser, ReqIFZParser
from reqif.reqif_bundle import ReqIFZBundle
from reqif.unparser import ReqIFUnparser, ReqIFZUnparser


class PassthroughCommand:
    @classmethod
    def execute(cls, config: PassthroughCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")  # noqa: T201
            sys.exit(1)

        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if len(output_dir) > 0 and not os.path.isdir(output_dir):
            print(  # noqa: T201
                f"error: output directory does not exist: {output_file}"
            )
            sys.exit(1)

        # If a file is a ReqIFz archive, we treat it differently.
        if input_file.endswith(".reqifz"):
            output = PassthroughCommand._passthrough_reqifz(config)
        else:
            output = PassthroughCommand._passthrough(config)
        with open(output_file, "wb") as file:
            file.write(output)

    @staticmethod
    def _passthrough(passthrough_config: PassthroughCommandConfig) -> bytes:
        with open(passthrough_config.input_file, "r", encoding="UTF-8") as file:
            content = file.read()
        reqif_bundle = ReqIFParser.parse_from_string(content)
        reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
        return reqif_xml_output.encode("UTF-8")

    @staticmethod
    def _passthrough_reqifz(
        passthrough_config: PassthroughCommandConfig,
    ) -> bytes:
        reqifz_bundle: ReqIFZBundle = ReqIFZParser.parse(
            passthrough_config.input_file
        )
        reqifz_output = ReqIFZUnparser.unparse(reqifz_bundle)
        return reqifz_output
