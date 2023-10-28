from enum import Enum
from typing import Any, Dict, Optional

from reqif.models.reqif_spec_object import ReqIFSpecObject
from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
    SpecAttributeDefinition,
)
from reqif.reqif_bundle import ReqIFBundle


class ReqIFSchema:
    class ReqIFSchemaType(Enum):
        POLARION = 1
        DEFAULT = 2

    def __init__(self, reqif_bundle: ReqIFBundle):
        data_type_definitions: Dict[str, Any] = {}
        spec_object_type_attributes: Dict[str, SpecAttributeDefinition] = {}
        spec_object_type_names: Dict[str, str] = {}
        detected_section_spec_type: Optional[ReqIFSpecObjectType] = None
        detected_chapter_name_attribute: Optional[
            SpecAttributeDefinition
        ] = None
        detected_schema_type: ReqIFSchema.ReqIFSchemaType = (
            ReqIFSchema.ReqIFSchemaType.DEFAULT
        )

        # First, collect iterate over all spec object types and collect all
        # attributes which are essentially the requirements fields.
        assert reqif_bundle.core_content is not None
        assert reqif_bundle.core_content.req_if_content is not None
        assert reqif_bundle.core_content.req_if_content.spec_types is not None
        for spec_type in reqif_bundle.core_content.req_if_content.spec_types:
            if not isinstance(spec_type, ReqIFSpecObjectType):
                continue

            assert spec_type.long_name is not None
            if spec_type.long_name == "Heading":
                detected_section_spec_type = spec_type
                detected_schema_type = ReqIFSchema.ReqIFSchemaType.POLARION

            spec_object_type_names[spec_type.identifier] = spec_type.long_name

            assert spec_type.attribute_definitions is not None
            for attribute_definition in spec_type.attribute_definitions:
                if attribute_definition.long_name == "ReqIF.ChapterName":
                    detected_chapter_name_attribute = attribute_definition
                spec_object_type_attributes[
                    attribute_definition.identifier
                ] = attribute_definition

        assert reqif_bundle.core_content.req_if_content.data_types is not None
        for data_type in reqif_bundle.core_content.req_if_content.data_types:
            data_type_definitions[data_type.identifier] = data_type

        self.data_type_definitions: Dict[str, Any] = data_type_definitions
        self.spec_object_type_attributes: Dict[
            str, SpecAttributeDefinition
        ] = spec_object_type_attributes
        self.spec_object_type_names: Dict[str, str] = spec_object_type_names
        self.reqif_bundle: ReqIFBundle = reqif_bundle
        self.detected_heading_spec_type = detected_section_spec_type
        self.detected_chapter_name_attribute: Optional[
            SpecAttributeDefinition
        ] = detected_chapter_name_attribute
        self.detected_schema_type: ReqIFSchema.ReqIFSchemaType = (
            detected_schema_type
        )

    def is_spec_object_a_heading(self, spec_object: ReqIFSpecObject):
        if self.detected_heading_spec_type is not None:
            return (
                spec_object.spec_object_type
                == self.detected_heading_spec_type.identifier
            )
        if self.detected_chapter_name_attribute is not None:
            return (
                self.detected_chapter_name_attribute.identifier
                in spec_object.attribute_map
            )

        # If neither a Heading/Section spec type nor ReqIF.ChapterName attribute
        # could be detected, assume that all spec objects in the ReqIF file are
        # simply requirements.
        return False
