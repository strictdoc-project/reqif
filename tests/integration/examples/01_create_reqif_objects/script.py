import uuid

from reqif.models.reqif_core_content import ReqIFCoreContent
from reqif.models.reqif_data_type import ReqIFDataTypeDefinitionString
from reqif.models.reqif_namespace_info import ReqIFNamespaceInfo
from reqif.models.reqif_req_if_content import ReqIFReqIFContent
from reqif.models.reqif_reqif_header import ReqIFReqIFHeader
from reqif.models.reqif_spec_hierarchy import ReqIFSpecHierarchy
from reqif.models.reqif_spec_object import ReqIFSpecObject, SpecObjectAttribute
from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
    SpecAttributeDefinition,
)
from reqif.models.reqif_specification import ReqIFSpecification
from reqif.models.reqif_specification_type import ReqIFSpecificationType
from reqif.models.reqif_types import SpecObjectAttributeType
from reqif.object_lookup import ReqIFObjectLookup
from reqif.reqif_bundle import ReqIFBundle
from reqif.unparser import ReqIFUnparser


# "_" is needed to make the ReqIF XML schema validator happy.
def create_uuid():
    return "_" + uuid.uuid4().hex


date_now = "2023-01-01T00:00:00.000+02:00"


class ExampleIdentifiers:
    # These are usually unique identifiers (UUID)
    # For example, 550e8400-e29b-41d4-a716-446655440000 or similar.
    # For this example, we keep it as strings.
    STRING_DATATYPE_ID = create_uuid()
    SPEC_ATTRIBUTE_IDs = list(map(create_uuid, range(9)))
    SPEC_OBJECT_TYPE_ID = create_uuid()
    SPEC_OBJECT_ID = create_uuid()
    SPEC_HIERARCHY_ID = create_uuid()
    SPECIFICATION_TYPE_ID = create_uuid()
    SPECIFICATION_ID = create_uuid()
    HEADER_ID = create_uuid()


string_data_type = ReqIFDataTypeDefinitionString(
    identifier=ExampleIdentifiers.STRING_DATATYPE_ID,
    last_change=date_now,
    long_name="String type",
    max_length="50",
)

requirement_text_attribute = SpecAttributeDefinition(
    attribute_type=SpecObjectAttributeType.STRING,
    identifier=ExampleIdentifiers.SPEC_ATTRIBUTE_ID,
    datatype_definition=ExampleIdentifiers.STRING_DATATYPE_ID,
    last_change=date_now,
    long_name="Requirement text",
)

spec_object_type = ReqIFSpecObjectType.create(
    identifier=ExampleIdentifiers.SPEC_OBJECT_TYPE_ID,
    long_name="Requirement",
    last_change=date_now,
    attribute_definitions=[requirement_text_attribute],
)

spec_object_attributes = [
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.STRING,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[0],
        value="System ABC shall do XYQ.",
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.INTEGER,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[1],
        value="1",
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.INTEGER,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[2],
        value=1,
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.REAL,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[3],
        value="1.0",
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.REAL,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[4],
        value=1.0,
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.BOOLEAN,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[5],
        value=False,
    ),
    SpecObjectAttribute(
        attribute_type=SpecObjectAttributeType.BOOLEAN,
        definition_ref=ExampleIdentifiers.SPEC_ATTRIBUTE_IDs[6],
        value=True,
    ),
]

spec_object = ReqIFSpecObject(
    identifier=ExampleIdentifiers.SPEC_OBJECT_ID,
    attributes=spec_object_attributes,
    spec_object_type=spec_object_type.identifier,
    last_change=date_now,
)

spec_hierarchy = ReqIFSpecHierarchy(
    xml_node=None,
    is_self_closed=False,
    identifier=ExampleIdentifiers.SPEC_HIERARCHY_ID,
    last_change=date_now,
    long_name=None,
    spec_object=spec_object.identifier,
    children=[],
    ref_then_children_order=True,
    level=1,
)

specification_type = ReqIFSpecificationType(
    identifier=ExampleIdentifiers.SPECIFICATION_TYPE_ID,
    description=None,
    last_change=date_now,
    long_name="Software Requirements Specification Document",
    spec_attributes=None,
    spec_attribute_map={},
    is_self_closed=True,
)

specification = ReqIFSpecification(
    identifier=ExampleIdentifiers.SPECIFICATION_ID,
    last_change=date_now,
    long_name="ReqIF library requirements specification",
    # Empty <VALUES/> tag is needed to make the XML schema validator happy.
    values=[],
    specification_type=specification_type.identifier,
    children=[spec_hierarchy],
)

reqif_content = ReqIFReqIFContent(
    data_types=[string_data_type],
    spec_types=[
        specification_type,
        spec_object_type,
    ],
    spec_objects=[spec_object],
    spec_relations=[],
    specifications=[specification],
    spec_relation_groups=[],
)

core_content = ReqIFCoreContent(req_if_content=reqif_content)

namespace_info = ReqIFNamespaceInfo.empty(
    namespace="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd",
    configuration=None,
)

reqif_header = ReqIFReqIFHeader(
    identifier=ExampleIdentifiers.HEADER_ID,
    creation_time=date_now,
    repository_id="FOO BAR ID",
    req_if_tool_id="ReqIF library",
    req_if_version="1.0",
    source_tool_id="FOO BAZ ID",
    title="An example ReqIF file created from Python objects using reqif library",
)

reqif_lookup = ReqIFObjectLookup.empty()

bundle = ReqIFBundle(
    namespace_info=namespace_info,
    req_if_header=reqif_header,
    core_content=core_content,
    tool_extensions_tag_exists=False,
    lookup=reqif_lookup,
    exceptions=[],
)

reqif_string_content = ReqIFUnparser.unparse(bundle)
with open("Output/output.reqif", "w") as output_reqif_file:
    output_reqif_file.write(reqif_string_content)
