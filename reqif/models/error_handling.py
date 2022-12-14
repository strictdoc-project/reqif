from reqif.helpers.lxml import dump_xml_node


class ReqIFXMLParsingError(Exception):
    pass


class ReqIFSchemaError(Exception):
    def get_description(self) -> str:
        raise NotImplementedError


class ReqIFSemanticError(Exception):
    def get_description(self) -> str:
        raise NotImplementedError


class ReqIFGeneralSemanticError(ReqIFSemanticError):
    def __init__(self, description: str):
        super().__init__(description)
        self.description: str = description

    def get_description(self) -> str:
        return self.description


class ReqIFMissingTagException(ReqIFSchemaError):
    def __init__(self, xml_node, tag):
        super().__init__(xml_node, tag)
        self.xml_node = xml_node
        self.tag = tag

    def get_description(self) -> str:
        return (
            f"schema error: Tag <{self.xml_node.tag}> is missing a "
            f"<{self.tag}> child tag. "
            f"Affected fragment:\n{dump_xml_node(self.xml_node)}"
        )


class ReqIFSpecRelationMissingSpecObjectException(ReqIFSemanticError):
    def __init__(self, xml_node, tag: str, spec_object_identifier: str):
        super().__init__(xml_node, tag)
        self.xml_node = xml_node
        self.tag: str = tag
        self.spec_object_identifier: str = spec_object_identifier

    def get_description(self) -> str:
        return (
            f"schema error: A <{self.xml_node.tag}>'s <{self.tag}> "
            "contains a link to a non-existing <SPEC-OBJECT>: "
            f"{self.spec_object_identifier}\n"
            f"Affected fragment:\n{dump_xml_node(self.xml_node)}"
        )


class ReqIFSpecHierarchyMissingSpecObjectException(ReqIFSemanticError):
    def __init__(self, xml_node, spec_object_identifier: str):
        super().__init__(xml_node)
        self.xml_node = xml_node
        self.spec_object_identifier: str = spec_object_identifier

    def get_description(self) -> str:
        return (
            f"schema error: A <SPEC-HIERARCHY>'s <SPEC-OBJECT-REF> "
            "contains a link to a non-existing <SPEC-OBJECT>: "
            f"{self.spec_object_identifier}\n"
            f"Affected fragment:\n{dump_xml_node(self.xml_node)}"
        )
