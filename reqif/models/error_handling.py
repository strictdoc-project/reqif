from reqif.helpers.lxml import dump_xml_node


class ReqIFSchemaError(Exception):
    def get_description(self) -> str:
        raise NotImplementedError


class ReqIFMissingTagException(Exception):
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
