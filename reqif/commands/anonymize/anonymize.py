import os
import sys
from typing import List

from reqif.cli.cli_arg_parser import AnonimizeCommandConfig
from reqif.models.reqif_spec_object import ReqIFSpecObject, SpecObjectAttribute
from reqif.models.reqif_specification import ReqIFSpecification
from reqif.models.reqif_types import SpecObjectAttributeType

from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser


ANONYMIZED = "...Anonymized..."


class AnonymizeCommand:
    @classmethod
    def execute(cls, config: AnonimizeCommandConfig) -> None:
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        output = AnonymizeCommand._anonymize(config)
        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            print(f"error: output directory does not exist: {output_file}")
            sys.exit(1)
        with open(output_file, "w", encoding="UTF-8") as file:
            file.write(output)

    @staticmethod
    def _anonymize(passthrough_config: AnonimizeCommandConfig):
        reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)

        req_if_header = reqif_bundle.req_if_header
        if req_if_header:
            if req_if_header.title:
                req_if_header.title = ANONYMIZED
            if req_if_header.comment:
                req_if_header.comment = ANONYMIZED

        core_content = reqif_bundle.core_content
        if core_content:
            reqif_content = core_content.req_if_content
            if reqif_content:
                spec_objects = reqif_content.spec_objects
                if spec_objects:
                    AnonymizeCommand._anonymize_spec_objects(spec_objects)
                specifications = reqif_content.specifications
                if specifications:
                    AnonymizeCommand._anonymize_specifications(specifications)
        reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
        return reqif_xml_output

    @staticmethod
    def _anonymize_spec_objects(spec_objects: List[ReqIFSpecObject]):
        for spec_object in spec_objects:
            for attribute in spec_object.attributes:
                AnonymizeCommand._anonymize_attribute(attribute)

    @staticmethod
    def _anonymize_specifications(specifications: List[ReqIFSpecification]):
        for specification in specifications:
            if specification.long_name:
                specification.long_name = ANONYMIZED
            if specification.values:
                for value in specification.values:
                    AnonymizeCommand._anonymize_attribute(value)

    @staticmethod
    def _anonymize_attribute(attribute):
        assert isinstance(attribute, SpecObjectAttribute), f"{attribute}"
        if attribute.attribute_type == SpecObjectAttributeType.STRING:
            attribute.value = ANONYMIZED
        elif attribute.attribute_type == SpecObjectAttributeType.XHTML:
            attribute.value = (
                "                " f"<xhtml:div>{ANONYMIZED}</xhtml:div>"
            )
