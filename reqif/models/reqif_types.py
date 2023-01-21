from enum import Enum


class SpecObjectAttributeType(Enum):
    STRING = 1
    ENUMERATION = 2
    INTEGER = 3
    REAL = 4
    BOOLEAN = 5
    DATE = 6
    XHTML = 7

    def get_spec_type_tag(self):  # pylint: disable=too-many-return-statements
        if self == SpecObjectAttributeType.STRING:
            return "ATTRIBUTE-DEFINITION-STRING"
        if self == SpecObjectAttributeType.ENUMERATION:
            return "ATTRIBUTE-DEFINITION-ENUMERATION"
        if self == SpecObjectAttributeType.INTEGER:
            return "ATTRIBUTE-DEFINITION-INTEGER"
        if self == SpecObjectAttributeType.REAL:
            return "ATTRIBUTE-DEFINITION-REAL"
        if self == SpecObjectAttributeType.BOOLEAN:
            return "ATTRIBUTE-DEFINITION-BOOLEAN"
        if self == SpecObjectAttributeType.DATE:
            return "ATTRIBUTE-DEFINITION-DATE"
        if self == SpecObjectAttributeType.XHTML:
            return "ATTRIBUTE-DEFINITION-XHTML"
        raise NotImplementedError(self) from None

    def get_definition_tag(self):
        return f"DATATYPE-DEFINITION-{self.name}-REF"

    def get_attribute_value_tag(self):
        return f"ATTRIBUTE-VALUE-{self.name}"
