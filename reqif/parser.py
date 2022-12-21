import copy
import io
from collections import defaultdict, OrderedDict
from typing import List, Optional, Dict, Any, Tuple

from lxml import etree
from lxml.etree import DocInfo

from reqif.models.error_handling import (
    ReqIFMissingTagException,
    ReqIFSchemaError,
    ReqIFXMLParsingError,
)
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
        with open(input_path, "r", encoding="UTF-8") as file:
            content = file.read()
        return ReqIFParser.parse_from_string(content)

    @staticmethod
    def parse_from_string(reqif_content: str) -> ReqIFBundle:
        try:
            # Parse XML.
            # https://github.com/eerohele/sublime-lxml/issues/5#issuecomment-209781719
            xml_reqif_root = etree.parse(
                io.BytesIO(bytes(reqif_content, "UTF-8"))
            )
        except Exception as exception:  # pylint: disable=broad-except
            raise ReqIFXMLParsingError(str(exception)) from None

        # Build ReqIF bundle.
        reqif_bundle = ReqIFParser._parse_reqif(xml_reqif_root)
        return reqif_bundle

    @staticmethod
    def _parse_reqif(xml_reqif) -> ReqIFBundle:
        docinfo: DocInfo = xml_reqif.docinfo

        # There should be a better way of detecting if the whole
        # <?xml version="1.0" encoding="UTF-8"?> line is missing.
        doctype_is_present = docinfo.standalone is not None

        namespace_info = OrderedDict(xml_reqif.getroot().nsmap)

        namespace: Optional[str] = (
            namespace_info[None] if None in namespace_info else None
        )

        configuration: Optional[str] = (
            namespace_info["configuration"]
            if "configuration" in namespace_info
            else None
        )
        namespace_id: Optional[str] = (
            namespace_info["id"] if "id" in namespace_info else None
        )
        namespace_xhtml: Optional[str] = (
            namespace_info["xhtml"] if "xhtml" in namespace_info else None
        )

        schema_namespace = namespace_info.get("xsi")

        xml_reqif_nons = (
            ReqIFParser._strip_namespace_from_xml(copy.deepcopy(xml_reqif))
            if namespace is not None
            else xml_reqif
        )

        xml_reqif_nons_root = xml_reqif_nons.getroot()
        if xml_reqif_nons_root is None:
            raise NotImplementedError(xml_reqif_nons_root) from None
        if xml_reqif_nons_root.tag != "REQ-IF":
            raise ReqIFXMLParsingError(
                "Expected root tag to be REQ-IF, got: "
                f"{xml_reqif_nons_root.tag}."
            ) from None

        # The best workaround I could find for getting the exact content of
        # the namespaces and attributes of the <REQ-IF ...> tag.
        # https://stackoverflow.com/questions/74879238
        xml_reqif_root_2 = xml_reqif.getroot()
        for child in list(xml_reqif_root_2):
            xml_reqif_root_2.remove(child)
        original_reqif_tag_dump = etree.tostring(
            xml_reqif_root_2, pretty_print=True
        ).decode("utf8")
        original_reqif_tag_dump = original_reqif_tag_dump.replace(
            "</REQ-IF>", ""
        ).strip()

        schema_location: Optional[str] = None
        if schema_namespace:
            schema_location_attribute = f"{{{schema_namespace}}}schemaLocation"
            if schema_location_attribute in xml_reqif_nons_root.attrib:
                schema_location = xml_reqif_nons_root.attrib[
                    schema_location_attribute
                ]
        language: Optional[str] = None
        xml_namespace = "http://www.w3.org/XML/1998/namespace"
        language_attribute = f"{{{xml_namespace}}}lang"
        if language_attribute in xml_reqif_nons_root.attrib:
            language = xml_reqif_nons_root.attrib[language_attribute]
        namespace_info_container = ReqIFNamespaceInfo(
            original_reqif_tag_dump=original_reqif_tag_dump,
            doctype_is_present=doctype_is_present,
            encoding=docinfo.encoding,
            namespace=namespace,
            configuration=configuration,
            namespace_id=namespace_id,
            namespace_xhtml=namespace_xhtml,
            schema_namespace=schema_namespace,
            schema_location=schema_location,
            language=language,
        )

        # ReqIF element naming convention: element_xyz where xyz is the name of
        # the reqif(xml) tag. Dashes are turned into underscores.
        if xml_reqif_nons_root is None:
            raise NotImplementedError
        if xml_reqif_nons_root.tag != "REQ-IF":
            raise NotImplementedError

        if len(xml_reqif_nons_root) == 0:
            return ReqIFBundle.create_empty(
                namespace=namespace, configuration=configuration
            )

        exceptions: List[ReqIFSchemaError] = []

        # <THE-HEADER>
        req_if_header: Optional[ReqIFReqIFHeader] = None
        xml_the_header = xml_reqif_nons_root.find("THE-HEADER")
        if xml_the_header is not None:
            req_if_header = ReqIFHeaderParser.parse(xml_the_header)

        # <CORE-CONTENT>
        # <REQ-IF-CONTENT>
        core_content: Optional[ReqIFCoreContent] = None
        lookup: ReqIFObjectLookup = ReqIFObjectLookup.empty()
        xml_core_content = xml_reqif_nons_root.find("CORE-CONTENT")
        if xml_core_content is not None:
            xml_req_if_content = xml_core_content.find("REQ-IF-CONTENT")
            if xml_req_if_content is not None:
                (
                    reqif_content,
                    lookup,
                    content_exceptions,
                ) = ReqIFParser._parse_reqif_content(xml_req_if_content)
                core_content = ReqIFCoreContent(req_if_content=reqif_content)
                exceptions.extend(content_exceptions)
            else:
                core_content = ReqIFCoreContent(req_if_content=None)

        # TODO: Tool extensions contains information specific to the tool used
        # to create the ReqIF file.
        # element_tool_extensions = xml_reqif_nons_root.find(
        #     "TOOL-EXTENSIONS", namespace_dict
        # )
        tool_extensions_tag_exists = (
            xml_reqif_nons_root.find("TOOL-EXTENSIONS") is not None
        )

        return ReqIFBundle(
            namespace_info=namespace_info_container,
            req_if_header=req_if_header,
            core_content=core_content,
            tool_extensions_tag_exists=tool_extensions_tag_exists,
            lookup=lookup,
            exceptions=exceptions,
        )

    @staticmethod
    def _parse_reqif_content(
        xml_req_if_content,
    ) -> Tuple[ReqIFReqIFContent, ReqIFObjectLookup, List[ReqIFSchemaError]]:
        assert xml_req_if_content is not None
        assert xml_req_if_content.tag == "REQ-IF-CONTENT"

        exceptions: List[ReqIFSchemaError] = []
        data_types: Optional[List] = None
        data_types_lookup: Dict[str, Any] = {}
        xml_data_types = xml_req_if_content.find("DATATYPES")
        if xml_data_types is not None:
            data_types = []
            for xml_data_type in list(xml_data_types):
                data_type = DataTypeParser.parse(xml_data_type)
                data_types.append(data_type)
                data_types_lookup[data_type.identifier] = data_type

        spec_types = None
        spec_types_lookup: Dict = {}
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
                spec_types_lookup[spec_type.identifier] = spec_type
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
        spec_relations_parent_lookup: Dict[str, List[str]] = defaultdict(list)
        xml_spec_relations = xml_req_if_content.find("SPEC-RELATIONS")
        if xml_spec_relations is not None:
            spec_relations = []

            for xml_spec_relation in xml_spec_relations:
                try:
                    spec_relation = SpecRelationParser.parse(xml_spec_relation)
                    spec_relations.append(spec_relation)
                    spec_relations_parent_lookup[spec_relation.source].append(
                        spec_relation.target
                    )
                except ReqIFMissingTagException as exception:
                    exceptions.append(exception)

        # <SPEC-OBJECTS>
        spec_objects: Optional[List[ReqIFSpecObject]] = None
        spec_objects_lookup: Dict[str, ReqIFSpecObject] = {}
        xml_spec_objects = xml_req_if_content.find("SPEC-OBJECTS")
        if xml_spec_objects is not None:
            spec_objects = []
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
            spec_types_lookup=spec_types_lookup,
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
        return reqif_content, lookup, exceptions

    @staticmethod
    def _strip_namespace_from_xml(root_xml):
        for elem in root_xml.getiterator():
            # Remove an XML namespace URI in the element's name but keep the
            # namespaces in the HTML content as found in the
            # <ATTRIBUTE-VALUE-XHTML> of ReqIF XML.
            if "http://www.w3.org/1999/xhtml" in elem.tag:
                continue
            elem.tag = etree.QName(elem).localname
        # Remove unused namespace declarations
        etree.cleanup_namespaces(root_xml)
        return root_xml
        # objectify.deannotate(root_xml, xsi_nil=True, cleanup_namespaces=True)
        # return root_xml
