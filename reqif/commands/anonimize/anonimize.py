import os
import sys
from typing import List

from reqif.cli.cli_arg_parser import AnonimizeCommandConfig
from reqif.models.reqif_spec_object import ReqIFSpecObject

from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser


class AnonimizeCommand:
    @classmethod
    def execute(cls, config: AnonimizeCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        output = AnonimizeCommand._anonimize(config)
        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            print(f"error: output directory does not exist: {output_file}")
            sys.exit(1)
        with open(output_file, "w", encoding="UTF-8") as file:
            file.write(output)

    @staticmethod
    def _anonimize(passthrough_config: AnonimizeCommandConfig):
        reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)

        core_content = reqif_bundle.core_content
        if core_content:
            reqif_content = core_content.req_if_content
            if reqif_content:
                AnonimizeCommand._anonimize_spec_objects(
                    reqif_content.spec_objects
                )
        reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
        return reqif_xml_output

    @staticmethod
    def _anonimize_spec_objects(spec_objects: List[ReqIFSpecObject]):
        for spec_object in spec_objects:
            for attribute in spec_object.attributes:
                attribute.value = "<Anonymized>"
