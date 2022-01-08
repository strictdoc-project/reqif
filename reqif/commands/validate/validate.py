import os
import sys
from typing import List

from reqif.cli.cli_arg_parser import ValidateCommandConfig
from reqif.models.error_handling import ReqIFSchemaError
from reqif.parser import ReqIFParser


class ReqIFErrorBundle:
    def __init__(self, schema_errors: List[Exception], semantic_warnings):
        self.schema_errors: List[ReqIFSchemaError] = schema_errors
        self.semantic_warnings: List[str] = semantic_warnings


class ValidateCommand:
    @classmethod
    def execute(cls, config: ValidateCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        error_bundle = ValidateCommand._validate(config)
        for warning in error_bundle.schema_errors:
            print(f"warning: {warning.get_description()}")
        for warning in error_bundle.semantic_warnings:
            print(f"warning: semantic error: {warning}")
        print(
            f"Validation complete with 0 errors, "
            f"{len(error_bundle.schema_errors)} schema issues found, "
            f"{len(error_bundle.semantic_warnings)} semantic issues found."
        )

    @staticmethod
    def _validate(
        passthrough_config: ValidateCommandConfig,
    ) -> ReqIFErrorBundle:
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

        return ReqIFErrorBundle(
            schema_errors=reqif_bundle.exceptions, semantic_warnings=warnings
        )
