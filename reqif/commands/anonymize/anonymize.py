import hashlib
import io
import os
import sys
from typing import List

from lxml import etree
from lxml.etree import tostring

from reqif.cli.cli_arg_parser import AnonimizeCommandConfig
from reqif.helpers.lxml import lxml_stringify_namespaced_children
from reqif.models.error_handling import ReqIFXMLParsingError
from reqif.models.reqif_spec_object import ReqIFSpecObject, SpecObjectAttribute
from reqif.models.reqif_specification import ReqIFSpecification
from reqif.models.reqif_types import SpecObjectAttributeType

ANONYMIZED = "Anonymized"


def anonymize_string(string: str) -> str:
    # https://stackoverflow.com/a/42089311/598057
    hash_number = (
        int(hashlib.sha256(string.encode("utf8")).hexdigest(), 16) % 10**10
    )
    return "..." + ANONYMIZED + "-" + str(hash_number) + "..."


class AnonymizeCommand:
    @classmethod
    def execute(cls, config: AnonimizeCommandConfig) -> None:
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")  # noqa: T201
            sys.exit(1)

        output = AnonymizeCommand._anonymize(config)
        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if len(output_dir) > 0 and not os.path.isdir(output_dir):
            print(  # noqa: T201
                f"error: output directory does not exist: {output_file}"
            )
            sys.exit(1)
        with open(output_file, "w", encoding="UTF-8") as file:
            file.write(output)

    @staticmethod
    def _anonymize(config: AnonimizeCommandConfig):
        with open(config.input_file, "r", encoding="UTF-8") as file:
            content = file.read()
        try:
            # Parse XML.
            # https://github.com/eerohele/sublime-lxml/issues/5#issuecomment-209781719
            xml_reqif = etree.parse(io.BytesIO(bytes(content, "UTF-8")))
        except Exception as exception:  # pylint: disable=broad-except
            raise ReqIFXMLParsingError(str(exception)) from None

        # https://stackoverflow.com/a/8056239/598057
        xml_reqif_root = xml_reqif.getroot()
        fixns = {"reqif": xml_reqif_root.nsmap[None]}

        # Clear out HEADER comment.
        xml_header_comment = xml_reqif.xpath(
            "//reqif:REQ-IF-HEADER/reqif:COMMENT", namespaces=fixns
        )
        for xml_header_comment_singleton in xml_header_comment:
            xml_header_comment_singleton.text = anonymize_string(
                xml_header_comment_singleton.text
            )

        # Clear out TITLE comment.
        xml_header_title = xml_reqif.xpath(
            "//reqif:REQ-IF-HEADER/reqif:TITLE", namespaces=fixns
        )
        for xml_header_title_singleton in xml_header_title:
            xml_header_title_singleton.text = anonymize_string(
                xml_header_title_singleton.text
            )

        # Clear out all SPECIFICATION names.
        xml_specifications = xml_reqif.xpath(
            "//reqif:SPECIFICATION", namespaces=fixns
        )
        for xml_specification in xml_specifications:
            if "LONG-NAME" in xml_specification.attrib:
                xml_specification.attrib["LONG-NAME"] = anonymize_string(
                    xml_specification.attrib["LONG-NAME"]
                )

        # Clear out all ATTRIBUTE-VALUE-STRINGs.
        xml_attribute_value_strings = xml_reqif.xpath(
            "//reqif:ATTRIBUTE-VALUE-STRING", namespaces=fixns
        )
        for xml_attribute_value_string in xml_attribute_value_strings:
            if "THE-VALUE" in xml_attribute_value_string.attrib:
                xml_attribute_value_string.attrib[
                    "THE-VALUE"
                ] = anonymize_string(
                    xml_attribute_value_string.attrib["THE-VALUE"]
                )

        # Clear out all ATTRIBUTE-VALUE-XHTMLs.
        xml_attribute_value_xhtmls = xml_reqif.xpath(
            "//reqif:ATTRIBUTE-VALUE-XHTML/reqif:THE-VALUE", namespaces=fixns
        )
        for xml_attribute_value_xhtml in xml_attribute_value_xhtmls:
            xml_attribute_value_xhtml_text: str = (
                lxml_stringify_namespaced_children(xml_attribute_value_xhtml)
            )
            for child in list(xml_attribute_value_xhtml):
                xml_attribute_value_xhtml.remove(child)
            xml_attribute_value_xhtml.text = anonymize_string(
                xml_attribute_value_xhtml_text
            )

        return str(
            tostring(
                xml_reqif,
                encoding="UTF-8",
                pretty_print=True,
                doctype='<?xml version="1.0" encoding="UTF-8"?>',
            ),
            encoding="utf8",
        )

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
            attribute.value = f"<xhtml:div>{ANONYMIZED}</xhtml:div>"
