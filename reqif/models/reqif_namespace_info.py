from typing import Optional


class ReqIFNamespaceInfo:
    def __init__(
        self,
        namespace: str,
        configuration: str,
        schema_namespace: Optional[str],
        schema_location: Optional[str],
    ):
        self.namespace: str = namespace
        self.configuration: str = configuration
        self.schema_namespace: Optional[str] = schema_namespace
        self.schema_location: Optional[str] = schema_location

    def __str__(self) -> str:
        return (
            f"ReqIFNamespaceInfo("
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
            namespace=namespace_or_default,
            configuration=configuration_or_default,
            schema_namespace=None,
            schema_location=None,
        )
