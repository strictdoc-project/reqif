from typing import Dict


class ReqIFSpecObject:
    def __init__(self, identifier: str, spec_object_type, attribute_map):
        self.identifier: str = identifier
        self.spec_object_type = spec_object_type
        self.attribute_map: Dict[str, str] = attribute_map

    def __str__(self) -> str:
        return (
            f"ReqIFSpecObject("
            f"identifier: {self.identifier}"
            ", "
            f"spec_object_type: {self.spec_object_type}"
            ", "
            f"attribute_map: {self.attribute_map}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
