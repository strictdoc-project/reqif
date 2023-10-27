import argparse
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from dataclasses_json import dataclass_json

from reqif.models.reqif_data_type import (
    ReqIFDataTypeDefinitionDateIdentifier,
    ReqIFDataTypeDefinitionEnumeration,
    ReqIFDataTypeDefinitionString,
    ReqIFDataTypeDefinitionXHTML,
)
from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
    SpecAttributeDefinition,
)
from reqif.parser import ReqIFParser, ReqIFZParser
from reqif.reqif_bundle import ReqIFBundle, ReqIFZBundle


@dataclass_json
@dataclass
class Specification:
    name: str
    content: List

    def get_as_dict(self):
        return self.to_dict()  # noqa: E1101


@dataclass_json
@dataclass
class ReqDict:
    documents: List[Specification] = field(default_factory=list)
    fields: List = field(default_factory=list)

    def get_as_dict(self):
        return self.to_dict()  # noqa: E1101


class ReqIFToDictConverter:
    def __init__(self):
        pass

    @staticmethod
    def convert(reqif_bundle: ReqIFBundle) -> ReqDict:
        # This dictionary will be written to CSV.
        reqif_dict = ReqDict()

        data_type_definitions: Dict[str, Any] = {}
        spec_object_type_attributes: Dict[str, SpecAttributeDefinition] = {}
        spec_object_type_names: Dict[str, str] = {}

        # First, collect iterate over all spec object types and collect all attributes
        # which are essentially the requirements fields.
        assert reqif_bundle.core_content is not None
        assert reqif_bundle.core_content.req_if_content is not None
        assert reqif_bundle.core_content.req_if_content.spec_types is not None
        for spec_type in reqif_bundle.core_content.req_if_content.spec_types:
            if not isinstance(spec_type, ReqIFSpecObjectType):
                continue

            assert spec_type.long_name is not None
            spec_object_type_names[spec_type.identifier] = spec_type.long_name

            assert spec_type.attribute_definitions is not None
            for attribute_definition in spec_type.attribute_definitions:
                spec_object_type_attributes[
                    attribute_definition.identifier
                ] = attribute_definition

        assert reqif_bundle.core_content.req_if_content.data_types is not None
        for data_type in reqif_bundle.core_content.req_if_content.data_types:
            data_type_definitions[data_type.identifier] = data_type

        # The easiest way to define the CSV columns is to collect all field names
        # available in the ReqIF file.
        # NOTE: This can create many unused columns if the requirements and chapters
        # attributes are two distinct sets of fields.
        reqif_dict.fields = []
        reqif_dict.fields.extend(
            list(
                {
                    attribute_definition_.long_name: 1
                    for attribute_definition_ in spec_object_type_attributes.values()
                }.keys()
            )
        )

        assert (
            reqif_bundle.core_content.req_if_content.specifications is not None
        )
        for (
            specification
        ) in reqif_bundle.core_content.req_if_content.specifications:
            assert specification.long_name is not None
            specification_dict: Specification = Specification(
                name=specification.long_name, content=[]
            )

            for (
                current_hierarchy
            ) in reqif_bundle.iterate_specification_hierarchy(specification):
                spec_object = reqif_bundle.get_spec_object_by_ref(
                    current_hierarchy.spec_object
                )

                spec_object_type_ref = spec_object.spec_object_type

                spec_object_type = reqif_bundle.get_spec_object_type_by_ref(
                    spec_object_type_ref
                )
                assert spec_object_type is not None
                row_dict = {
                    "Type": spec_object_type_names[spec_object_type.identifier]
                }
                for spec_object_attribute_ in spec_object.attributes:
                    attribute_definition = spec_object_type_attributes[
                        spec_object_attribute_.definition_ref
                    ]
                    assert attribute_definition.long_name is not None

                    data_type = data_type_definitions[
                        attribute_definition.datatype_definition
                    ]
                    assert data_type is not None
                    if isinstance(
                        data_type, ReqIFDataTypeDefinitionDateIdentifier
                    ):
                        assert isinstance(spec_object_attribute_.value, str)
                        row_dict[
                            attribute_definition.long_name
                        ] = spec_object_attribute_.value
                    elif isinstance(
                        data_type, ReqIFDataTypeDefinitionEnumeration
                    ):
                        assert isinstance(spec_object_attribute_.value, list)

                        enum_values: List[str] = []
                        for (
                            enum_value_identifier_
                        ) in spec_object_attribute_.value:
                            assert data_type.values is not None
                            for data_type_enum_value_ in data_type.values:
                                if (
                                    data_type_enum_value_.identifier
                                    == enum_value_identifier_
                                ):
                                    assert (
                                        data_type_enum_value_.long_name
                                        is not None
                                    )
                                    enum_values.append(
                                        data_type_enum_value_.long_name
                                    )
                                    break
                            else:
                                raise AssertionError("Enum value not found.")
                        row_dict[attribute_definition.long_name] = ", ".join(
                            enum_values
                        )
                    elif isinstance(data_type, ReqIFDataTypeDefinitionString):
                        assert isinstance(spec_object_attribute_.value, str)
                        row_dict[
                            attribute_definition.long_name
                        ] = spec_object_attribute_.value
                    elif isinstance(data_type, ReqIFDataTypeDefinitionXHTML):
                        assert isinstance(spec_object_attribute_.value, str)
                        row_dict[
                            attribute_definition.long_name
                        ] = spec_object_attribute_.value
                    else:
                        raise NotImplementedError(data_type)
                specification_dict.content.append(row_dict)
            reqif_dict.documents.append(specification_dict)

        return reqif_dict


def main():
    main_parser = argparse.ArgumentParser()

    main_parser.add_argument(
        "input_file", type=str, help="Path to the input ReqIF file."
    )
    main_parser.add_argument(
        "--output-dir",
        type=str,
        help="Path to the output dir.",
        default="output/",
    )
    main_parser.add_argument(
        "--stdout",
        help="Makes the script write the output ReqIF to standard output.",
        action="store_true",
    )
    main_parser.add_argument(
        "--no-filesystem",
        help=(
            "Disables writing to the file system. "
            "Should be used in combination with --stdout."
        ),
        action="store_true",
    )

    args = main_parser.parse_args()
    input_file: str = args.input_file
    should_use_file_system: bool = not args.no_filesystem
    should_use_stdout: bool = args.stdout

    if input_file.endswith(".reqifz"):
        reqifz_bundle: ReqIFZBundle = ReqIFZParser.parse(input_file)
        assert len(reqifz_bundle.reqif_bundles) == 1
        reqif_bundle = (list(reqifz_bundle.reqif_bundles.values()))[0]
    else:
        reqif_bundle = ReqIFParser.parse(input_file)

    req_dict = ReqIFToDictConverter.convert(reqif_bundle)
    reqif_json = json.dumps(req_dict.get_as_dict(), indent=4)

    if should_use_file_system:
        path_to_output_dir = args.output_dir
        Path(path_to_output_dir).mkdir(exist_ok=True)

        path_to_output_file = os.path.join(path_to_output_dir, "output.json")
        with open(path_to_output_file, "w", encoding="utf8") as json_file:
            json_file.write(reqif_json)
            json_file.write("\n")

    if should_use_stdout:
        print(reqif_json)  # noqa: T201


main()
