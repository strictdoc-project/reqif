import os
import sys

from reqif.cli.cli_arg_parser import PassthroughCommandConfig

from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser


class PassthroughCommand:
    @classmethod
    def execute(cls, config: PassthroughCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        output = PassthroughCommand._passthrough(config)
        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            print(f"error: output directory does not exist: {output_file}")
            sys.exit(1)
        with open(output_file, "w", encoding="UTF-8") as file:
            file.write(output)

    @staticmethod
    def _passthrough(passthrough_config: PassthroughCommandConfig):
        reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)
        reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
        return reqif_xml_output
