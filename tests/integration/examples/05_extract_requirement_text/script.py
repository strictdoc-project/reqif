# ruff: noqa: T201
import lxml.html

from reqif.models.reqif_types import SpecObjectAttributeType
from reqif.parser import ReqIFParser


def xhtml_to_plain_text(xhtml: str) -> str:
    # Keep only the text of the XHTML fragment and collapse the whitespace
    # that comes from the indentation of the XHTML tags.
    text = lxml.html.fromstring(xhtml).text_content()
    return " ".join(text.split())


input_file_path = "input.reqif"

reqif_bundle = ReqIFParser.parse(input_file_path)
for specification in reqif_bundle.core_content.req_if_content.specifications:
    print(f"Specification: {specification.long_name}")

    for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(
        specification
    ):
        # A SPEC-HIERARCHY node only holds the identifier of a SPEC-OBJECT
        # (the SPEC-OBJECT-REF). Look up the SPEC-OBJECT by this identifier.
        spec_object_ref = current_hierarchy.spec_object
        spec_object = reqif_bundle.get_spec_object_by_ref(spec_object_ref)

        # The attribute names, such as "ReqIF.Text", are defined by the
        # SPEC-OBJECT-TYPE of the SPEC-OBJECT.
        spec_object_type = reqif_bundle.get_spec_object_type_by_ref(
            spec_object.spec_object_type
        )

        indent = "  " * current_hierarchy.level
        print(f"{indent}SPEC-OBJECT: {spec_object.identifier}")
        print(f"{indent}  LONG-NAME: {spec_object.long_name}")

        for attribute in spec_object.attributes:
            attribute_definition = spec_object_type.attribute_map[
                attribute.definition_ref
            ]
            if attribute.attribute_type == SpecObjectAttributeType.XHTML:
                # attribute.value is the raw XHTML with its namespace prefix,
                # e.g., <xhtml:div>. attribute.value_stripped_xhtml is the same
                # XHTML without the prefix, e.g., <div>.
                value = xhtml_to_plain_text(attribute.value_stripped_xhtml)
            else:
                value = attribute.value
            print(f"{indent}  {attribute_definition.long_name}: {value}")
