from typing import List, Optional

from reqif.models.reqif_spec_object import (
    ReqIFSpecObject,
    SpecObjectAttribute,
)
from reqif.parsers.attribute_value_parser import AttributeValueParser


class SpecObjectParser:
    @staticmethod
    def parse(spec_object_xml) -> ReqIFSpecObject:
        assert "SPEC-OBJECT" in spec_object_xml.tag
        xml_attributes = spec_object_xml.attrib

        spec_object_description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        try:
            identifier = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None
        spec_object_last_change: Optional[str] = (
            xml_attributes["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attributes
            else None
        )
        spec_object_long_name: Optional[str] = (
            xml_attributes["LONG-NAME"]
            if "LONG-NAME" in xml_attributes
            else None
        )

        spec_object_type = (
            spec_object_xml.find("TYPE").find("SPEC-OBJECT-TYPE-REF").text
        )

        xml_spec_values = spec_object_xml.find("VALUES")
        attributes: Optional[
            List[SpecObjectAttribute]
        ] = AttributeValueParser.parse_attribute_values(xml_spec_values)

        # FIXME: Technically, we can get a ReqIF file where VALUES is empty.
        # But don't want to break the interfaces for now.
        assert attributes is not None

        return ReqIFSpecObject(
            xml_node=spec_object_xml,
            description=spec_object_description,
            identifier=identifier,
            last_change=spec_object_last_change,
            long_name=spec_object_long_name,
            spec_object_type=spec_object_type,
            attributes=attributes,
        )

    @staticmethod
    def unparse(spec_object: ReqIFSpecObject) -> str:
        output = ""

        output += "        <SPEC-OBJECT"
        if spec_object.description is not None:
            output += f' DESC="{spec_object.description}"'

        output += f' IDENTIFIER="{spec_object.identifier}"'

        if spec_object.last_change:
            output += f' LAST-CHANGE="{spec_object.last_change}"'
        if spec_object.long_name is not None:
            output += f' LONG-NAME="{spec_object.long_name}"'
        output += ">\n"

        if spec_object.xml_node is not None:
            children_tags = list(
                map(lambda el: el.tag, list(spec_object.xml_node))
            )
            assert "VALUES" in children_tags
            assert "TYPE" in children_tags
        else:
            children_tags = ["VALUES", "TYPE"]

        for child_tag in children_tags:
            if child_tag == "VALUES":
                output += AttributeValueParser.unparse_attribute_values(
                    spec_object.attributes
                )
            elif child_tag == "TYPE":
                output += SpecObjectParser._unparse_spec_object_type(
                    spec_object
                )
            else:
                print(f"warning: Unknown child tag: {child_tag}.")  # noqa: T201

        output += "        </SPEC-OBJECT>\n"

        return output

    @staticmethod
    def _unparse_spec_object_type(spec_object: ReqIFSpecObject):
        output = ""
        output += (
            "          <TYPE>\n"
            f"            "
            f"<SPEC-OBJECT-TYPE-REF>"
            f"{spec_object.spec_object_type}"
            f"</SPEC-OBJECT-TYPE-REF>\n"
            "          </TYPE>\n"
        )
        return output
