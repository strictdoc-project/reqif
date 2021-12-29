import os
import sys
from typing import List

from reqif.cli.cli_arg_parser import ValidateCommandConfig
from reqif.parser import ReqIFParser


class ValidateCommand:
    @classmethod
    def execute(cls, config: ValidateCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        warnings = ValidateCommand._validate(config)
        for warning in warnings:
            print(f"warning: {warning}")
        print(
            f"Validation complete with 0 errors, "
            f"{len(warnings)} warnings found."
        )

    @staticmethod
    def _validate(passthrough_config: ValidateCommandConfig) -> List[str]:
        warnings: List[str] = []
        reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)
        if not reqif_bundle.namespace_info.doctype_is_present:
            warning = (
                "Document is missing a valid XML declaration. Every ReqIF"
                "document should have the following line: "
                '<?xml version="1.0" encoding="UTF-8"?>'
            )
            warnings.append(warning)
        if reqif_bundle.namespace_info.encoding != "UTF-8":
            warning = (
                "ReqIF Implementation Guide recommends using UTF-8 "
                "encoding for ReqIF files. Every ReqIF "
                "document should have the following line: "
                '<?xml version="1.0" encoding="UTF-8"?>'
            )
            warnings.append(warning)

        return warnings
