import os
import sys
from typing import List

from reqif.cli.cli_arg_parser import ValidateCommandConfig
from reqif.models.error_handling import (
    ReqIFGeneralSemanticError,
    ReqIFSchemaError,
    ReqIFSemanticError,
    ReqIFSpecHierarchyMissingSpecObjectException,
    ReqIFSpecRelationMissingSpecObjectException,
    ReqIFXMLParsingError,
)
from reqif.models.reqif_spec_relation import ReqIFSpecRelation
from reqif.models.reqif_specification import ReqIFSpecification
from reqif.parser import ReqIFParser
from reqif.reqif_bundle import ReqIFBundle


class ReqIFErrorBundle:
    def __init__(
        self,
        xml_errors: List[ReqIFXMLParsingError],
        schema_errors: List[ReqIFSchemaError],
        semantic_warnings: List[ReqIFSemanticError],
    ):
        self.xml_errors: List[ReqIFXMLParsingError] = xml_errors
        self.schema_errors: List[ReqIFSchemaError] = schema_errors
        self.semantic_warnings: List[ReqIFSemanticError] = semantic_warnings


class ValidateCommand:
    @classmethod
    def execute(cls, config: ValidateCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")  # noqa: T201
            sys.exit(1)

        error_bundle = ValidateCommand._validate(config)
        for xml_error in error_bundle.xml_errors:
            print(f"error: {xml_error}")  # noqa: T201
        for schema_warning in error_bundle.schema_errors:
            print(f"warning: {schema_warning.get_description()}")  # noqa: T201
        for semantic_warning in error_bundle.semantic_warnings:
            print(  # noqa: T201
                f"warning: semantic error: {semantic_warning.get_description()}"
            )
        print(  # noqa: T201
            f"Validation complete with {len(error_bundle.xml_errors)} errors, "
            f"{len(error_bundle.schema_errors)} schema issues found, "
            f"{len(error_bundle.semantic_warnings)} semantic issues found."
        )

    @staticmethod
    def _validate(
        passthrough_config: ValidateCommandConfig,
    ) -> ReqIFErrorBundle:
        semantic_warnings: List[ReqIFSemanticError] = []
        try:
            reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)
        except ReqIFXMLParsingError as exception:
            return ReqIFErrorBundle(
                xml_errors=[exception],
                schema_errors=[],
                semantic_warnings=[],
            )

        if not reqif_bundle.namespace_info.doctype_is_present:
            warning = ReqIFGeneralSemanticError(
                "Document is missing a valid XML declaration. Every ReqIF"
                "document should have the following line: "
                '<?xml version="1.0" encoding="UTF-8"?>'
            )
            semantic_warnings.append(warning)
        if reqif_bundle.namespace_info.encoding != "UTF-8":
            warning = ReqIFGeneralSemanticError(
                "ReqIF Implementation Guide recommends using UTF-8 "
                "encoding for ReqIF files. Every ReqIF "
                "document should have the following line: "
                '<?xml version="1.0" encoding="UTF-8"?>'
            )
            semantic_warnings.append(warning)

        core_content = reqif_bundle.core_content
        if core_content is not None:
            req_if_content = core_content.req_if_content
            if req_if_content is not None:
                spec_relations = req_if_content.spec_relations
                if spec_relations is not None:
                    spec_relation_semantic_errors = (
                        ValidateCommand._validate_spec_relations(
                            spec_relations=spec_relations,
                            reqif_bundle=reqif_bundle,
                        )
                    )
                    semantic_warnings.extend(spec_relation_semantic_errors)
                specifications = req_if_content.specifications
                if specifications is not None:
                    spec_relation_semantic_errors = (
                        ValidateCommand._validate_specifications(
                            specifications=specifications,
                            reqif_bundle=reqif_bundle,
                        )
                    )
                    semantic_warnings.extend(spec_relation_semantic_errors)
        return ReqIFErrorBundle(
            xml_errors=[],
            schema_errors=reqif_bundle.exceptions,
            semantic_warnings=semantic_warnings,
        )

    @staticmethod
    def _validate_spec_relations(
        spec_relations: List[ReqIFSpecRelation],
        reqif_bundle: ReqIFBundle,
    ) -> List[ReqIFSemanticError]:
        semantic_errors: List[ReqIFSemanticError] = []
        for spec_relation in spec_relations:
            if not reqif_bundle.lookup.spec_object_exists(spec_relation.source):
                error = ReqIFSpecRelationMissingSpecObjectException(
                    xml_node=spec_relation.xml_node,
                    tag="SOURCE",
                    spec_object_identifier=spec_relation.source,
                )
                semantic_errors.append(error)
            if not reqif_bundle.lookup.spec_object_exists(spec_relation.target):
                error = ReqIFSpecRelationMissingSpecObjectException(
                    xml_node=spec_relation.xml_node,
                    tag="TARGET",
                    spec_object_identifier=spec_relation.target,
                )
                semantic_errors.append(error)
        return semantic_errors

    @staticmethod
    def _validate_specifications(
        specifications: List[ReqIFSpecification],
        reqif_bundle: ReqIFBundle,
    ) -> List[ReqIFSemanticError]:
        warnings: List[ReqIFSemanticError] = []

        for specification in specifications:
            for hierarchy in reqif_bundle.iterate_specification_hierarchy(
                specification
            ):
                if not reqif_bundle.lookup.spec_object_exists(
                    hierarchy.spec_object
                ):
                    warnings.append(
                        ReqIFSpecHierarchyMissingSpecObjectException(
                            xml_node=hierarchy.xml_node,
                            spec_object_identifier=hierarchy.spec_object,
                        )
                    )
        return warnings
