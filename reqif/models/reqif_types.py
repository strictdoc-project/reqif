from enum import Enum


class SpecObjectAttributeType(Enum):
    STRING = 1
    ENUMERATION = 2
    INTEGER = 3
    BOOLEAN = 4
    XHTML = 5

    def get_spec_type_tag(self):
        if self == SpecObjectAttributeType.STRING:
            return "ATTRIBUTE-DEFINITION-STRING"
        if self == SpecObjectAttributeType.INTEGER:
            return "ATTRIBUTE-DEFINITION-INTEGER"
        if self == SpecObjectAttributeType.BOOLEAN:
            return "ATTRIBUTE-DEFINITION-BOOLEAN"
        if self == SpecObjectAttributeType.XHTML:
            return "ATTRIBUTE-DEFINITION-XHTML"
        if self == SpecObjectAttributeType.ENUMERATION:
            return "ATTRIBUTE-DEFINITION-ENUMERATION"
        raise NotImplementedError(self) from None

    def get_definition_tag(self):
        return f"DATATYPE-DEFINITION-{self.name}-REF"

    def get_attribute_value_tag(self):
        return f"ATTRIBUTE-VALUE-{self.name}"
