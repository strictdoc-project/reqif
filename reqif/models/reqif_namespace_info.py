from typing import Optional

from reqif.helpers.debug import auto_str


class ReqIFNamespaceInfo:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        original_reqif_tag_dump: Optional[str],
        doctype_is_present: bool,
        encoding: str,
        namespace: Optional[str],
        configuration: Optional[str],
        namespace_id: Optional[str],
        namespace_xhtml: Optional[str],
        schema_namespace: Optional[str],
        schema_location: Optional[str],
        language: Optional[str],
    ):
        self.original_reqif_tag_dump: Optional[str] = original_reqif_tag_dump
        self.doctype_is_present: bool = doctype_is_present
        self.encoding: str = encoding
        self.namespace: Optional[str] = namespace
        self.configuration: Optional[str] = configuration
        self.namespace_id: Optional[str] = namespace_id
        self.namespace_xhtml: Optional[str] = namespace_xhtml
        self.schema_namespace: Optional[str] = schema_namespace
        self.schema_location: Optional[str] = schema_location
        self.language: Optional[str] = language

    @staticmethod
    def empty(
        namespace: Optional[str],
        configuration: Optional[str],
    ):
        return ReqIFNamespaceInfo(
            original_reqif_tag_dump=None,
            doctype_is_present=True,
            encoding="UTF-8",
            namespace=namespace,
            configuration=configuration,
            namespace_id=None,
            namespace_xhtml=None,
            schema_namespace=None,
            schema_location=None,
            language=None,
        )

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
