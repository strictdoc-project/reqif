import io
import sys
from collections import defaultdict
from typing import List, Optional, Dict

from lxml import etree
from lxml.etree import DocInfo

from reqif.models.reqif_core_content import ReqIFCoreContent
from reqif.models.reqif_namespace_info import ReqIFNamespaceInfo
from reqif.models.reqif_req_if_content import ReqIFReqIFContent
from reqif.models.reqif_reqif_header import ReqIFReqIFHeader
from reqif.models.reqif_spec_object import ReqIFSpecObject
from reqif.models.reqif_spec_relation import ReqIFSpecRelation
from reqif.models.reqif_specification import (
    ReqIFSpecification,
)
from reqif.object_lookup import ReqIFObjectLookup
from reqif.parsers.data_type_parser import (
    DataTypeParser,
)
from reqif.parsers.header_parser import ReqIFHeaderParser
from reqif.parsers.spec_object_parser import (
    SpecObjectParser,
)
from reqif.parsers.spec_relation_parser import (
    SpecRelationParser,
)
from reqif.parsers.spec_types.spec_object_type_parser import (
    SpecObjectTypeParser,
)
from reqif.parsers.spec_types.spec_relation_type_parser import (
    SpecRelationTypeParser,
)
from reqif.parsers.spec_types.specification_type_parser import (
    SpecificationTypeParser,
)
from reqif.parsers.specification_parser import (
    ReqIFSpecificationParser,
)
from reqif.reqif_bundle import ReqIFBundle


class ReqIFParser:
    @staticmethod
    def parse(input_path: str) -> ReqIFBundle:
        # Import file.
        with open(input_path, "r", encoding="UTF-8") as file:
            content = file.read()
        try:
            # Parse XML.
            # https://github.com/eerohele/sublime-lxml/issues/5#issuecomment-209781719
            xml_reqif_root = etree.parse(io.BytesIO(bytes(content, "UTF-8")))
        except Exception as exception:  # pylint: disable=broad-except
            # TODO: handle
            print(f"error: problem parsing file: {exception}")
            sys.exit(1)

        # Build ReqIF bundle.
        reqif_bundle = ReqIFParser.parse_reqif(xml_reqif_root)
        return reqif_bundle

    @staticmethod
    def parse_reqif(xml_reqif_root) -> ReqIFBundle:
        docinfo: DocInfo = xml_reqif_root.docinfo

        # There should be a better way of detecting if the whole
        # <?xml version="1.0" encoding="UTF-8"?> line is missing.
        doctype_is_present = docinfo.standalone is not None

        namespace_info = xml_reqif_root.getroot().nsmap
        namespace: Optional[str] = namespace_info[None]
        configuration: Optional[str] = (
            namespace_info["configuration"]
            if "configuration" in namespace_info
            else None
        )
        schema_namespace = namespace_info.get("xsi")
        xml_reqif_root_nons = ReqIFParser.strip_namespace_from_xml(
            xml_reqif_root
        )
        xml_reqif = xml_reqif_root_nons.getroot()
        if xml_reqif is None:
            raise NotImplementedError(xml_reqif) from None

        schema_location: Optional[str] = None
        if schema_namespace:
            schema_location_attribute = f"{{{schema_namespace}}}schemaLocation"
            if schema_location_attribute in xml_reqif.attrib:
                schema_location = xml_reqif.attrib[schema_location_attribute]
        language: Optional[str] = None
        xml_namespace = "http://www.w3.org/XML/1998/namespace"
        language_attribute = f"{{{xml_namespace}}}lang"
        if language_attribute in xml_reqif.attrib:
            language = xml_reqif.attrib[language_attribute]
        namespace_info = ReqIFNamespaceInfo(
            doctype_is_present=doctype_is_present,
            encoding=docinfo.encoding,
            namespace=namespace,
            configuration=configuration,
            schema_namespace=schema_namespace,
            schema_location=schema_location,
            language=language,
        )

        # ReqIF element naming convention: element_xyz where xyz is the name of
        # the reqif(xml) tag. Dashes are turned into underscores.
        if xml_reqif is None:
            raise NotImplementedError
        if xml_reqif.tag != "REQ-IF":
            raise NotImplementedError

        if len(xml_reqif) == 0:
            return ReqIFBundle.create_empty(
                namespace=namespace, configuration=configuration
            )

        # <THE-HEADER>
        req_if_header: Optional[ReqIFReqIFHeader] = None
        xml_the_header = xml_reqif.find("THE-HEADER")
        if xml_the_header is not None:
            req_if_header = ReqIFHeaderParser.parse(xml_the_header)

        # <CORE-CONTENT>
        # <REQ-IF-CONTENT>
        core_content: Optional[ReqIFCoreContent] = None
        lookup: Optional[ReqIFObjectLookup] = None
        xml_core_content = xml_reqif.find("CORE-CONTENT")
        if xml_core_content is not None:
            xml_req_if_content = xml_core_content.find("REQ-IF-CONTENT")
            if xml_req_if_content is not None:
                reqif_content, lookup = ReqIFParser.parse_reqif_content(
                    xml_req_if_content
                )
                core_content = ReqIFCoreContent(req_if_content=reqif_content)
            else:
                core_content = ReqIFCoreContent(req_if_content=None)

        # TODO: Tool extensions contains information specific to the tool used
        # to create the ReqIF file.
        # element_tool_extensions = xml_reqif.find(
        #     "TOOL-EXTENSIONS", namespace_dict
        # )
        tool_extensions_tag_exists = (
            xml_reqif.find("TOOL-EXTENSIONS") is not None
        )

        return ReqIFBundle(
            namespace_info=namespace_info,
            req_if_header=req_if_header,
            core_content=core_content,
            tool_extensions_tag_exists=tool_extensions_tag_exists,
            lookup=lookup,
        )

    @staticmethod
    def parse_reqif_content(
        xml_req_if_content,
    ) -> (ReqIFReqIFContent, ReqIFObjectLookup):
        assert xml_req_if_content is not None
        assert xml_req_if_content.tag == "REQ-IF-CONTENT"

        data_types: Optional[List] = None
        data_types_lookup: Optional[Dict] = None
        xml_data_types = xml_req_if_content.find("DATATYPES")
        if xml_data_types is not None:
            data_types = []
            data_types_lookup = {}
            for xml_data_type in list(xml_data_types):
                data_type = DataTypeParser.parse(xml_data_type)
                data_types.append(data_type)
                data_types_lookup[data_type.identifier] = data_type

        spec_types = None
        xml_spec_types = xml_req_if_content.find("SPEC-TYPES")
        if xml_spec_types is not None:
            spec_types = []
            for xml_spec_object_type_xml in list(xml_spec_types):
                if xml_spec_object_type_xml.tag == "SPEC-OBJECT-TYPE":
                    spec_type = SpecObjectTypeParser.parse(
                        xml_spec_object_type_xml
                    )
                elif xml_spec_object_type_xml.tag == "SPEC-RELATION-TYPE":
                    spec_type = SpecRelationTypeParser.parse(
                        xml_spec_object_type_xml
                    )
                elif xml_spec_object_type_xml.tag == "SPECIFICATION-TYPE":
                    spec_type = SpecificationTypeParser.parse(
                        xml_spec_object_type_xml
                    )
                else:
                    raise NotImplementedError(
                        xml_spec_object_type_xml
                    ) from None
                spec_types.append(spec_type)

        # <SPECIFICATIONS>
        specifications: Optional[List[ReqIFSpecification]] = None
        xml_specifications = xml_req_if_content.find("SPECIFICATIONS")
        if xml_specifications is not None:
            specifications = []
            for xml_specification in xml_specifications:
                specification = ReqIFSpecificationParser.parse(
                    xml_specification
                )
                specifications.append(specification)

        # <SPEC-RELATIONS>
        spec_relations: Optional[List[ReqIFSpecRelation]] = None
        spec_relations_parent_lookup: Optional[Dict[str, List[str]]] = None
        xml_spec_relations = xml_req_if_content.find("SPEC-RELATIONS")
        if xml_spec_relations is not None:
            spec_relations = []
            spec_relations_parent_lookup = defaultdict(list)

            for xml_spec_relation in xml_spec_relations:
                spec_relation = SpecRelationParser.parse(xml_spec_relation)
                spec_relations.append(spec_relation)
                spec_relations_parent_lookup[spec_relation.source].append(
                    spec_relation.target
                )

        # <SPEC-OBJECTS>
        spec_objects: Optional[List[ReqIFSpecObject]] = None
        spec_objects_lookup: Optional[Dict[str, ReqIFSpecObject]] = None
        xml_spec_objects = xml_req_if_content.find("SPEC-OBJECTS")
        if xml_spec_objects is not None:
            spec_objects = []
            spec_objects_lookup = {}
            for xml_spec_object in xml_spec_objects:
                spec_object = SpecObjectParser.parse(xml_spec_object)
                spec_objects.append(spec_object)
                spec_objects_lookup[spec_object.identifier] = spec_object

        # <SPEC-RELATION-GROUPS>
        spec_relation_groups: Optional[List] = None
        xml_spec_relation_groups = xml_req_if_content.find(
            "SPEC-RELATION-GROUPS"
        )
        if xml_spec_relation_groups is not None:
            spec_relation_groups = []
            if len(xml_spec_relation_groups) != 0:
                raise NotImplementedError(xml_spec_relation_groups) from None

        lookup = ReqIFObjectLookup(
            data_types_lookup=data_types_lookup,
            spec_objects_lookup=spec_objects_lookup,
            spec_relations_parent_lookup=spec_relations_parent_lookup,
        )
        reqif_content = ReqIFReqIFContent(
            data_types=data_types,
            spec_types=spec_types,
            spec_objects=spec_objects,
            spec_relations=spec_relations,
            specifications=specifications,
            spec_relation_groups=spec_relation_groups,
        )
        return reqif_content, lookup

    @staticmethod
    def strip_namespace_from_xml(root_xml):
        for elem in root_xml.getiterator():
            # Remove a namespace URI in the element's name
            elem.tag = etree.QName(elem).localname

        # Remove unused namespace declarations
        etree.cleanup_namespaces(root_xml)
        return root_xml
        # objectify.deannotate(root_xml, xsi_nil=True, cleanup_namespaces=True)
        # return root_xml
