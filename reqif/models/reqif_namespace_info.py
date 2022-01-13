from typing import Optional


class ReqIFNamespaceInfo:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        doctype_is_present: bool,
        encoding: str,
        namespace: str,
        configuration: Optional[str],
        namespace_id: Optional[str],
        namespace_xhtml: Optional[str],
        schema_namespace: Optional[str],
        schema_location: Optional[str],
        language: Optional[str],
    ):
        self.doctype_is_present: bool = doctype_is_present
        self.encoding: str = encoding
        self.namespace: str = namespace
        self.configuration: Optional[str] = configuration
        self.namespace_id: Optional[str] = namespace_id
        self.namespace_xhtml: Optional[str] = namespace_xhtml
        self.schema_namespace: Optional[str] = schema_namespace
        self.schema_location: Optional[str] = schema_location
        self.language: Optional[str] = language

    def __str__(self) -> str:
        return (
            f"ReqIFNamespaceInfo("
            f"encoding={self.encoding}"
            ", "
            f"namespace={self.namespace}"
            ", "
            f"configuration={self.configuration}"
            ", "
            f"schema_namespace={self.schema_namespace}"
            ", "
            f"schema_location={self.schema_location}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def empty(
        namespace: Optional[str],
        configuration: Optional[str],
    ):
        namespace_or_default = (
            namespace
            if namespace
            else "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
        )
        configuration_or_default = configuration if configuration else "TBD"
        return ReqIFNamespaceInfo(
            doctype_is_present=True,
            encoding="UTF-8",
            namespace=namespace_or_default,
            configuration=configuration_or_default,
            namespace_id=None,
            namespace_xhtml=None,
            schema_namespace=None,
            schema_location=None,
            language=None,
        )
