# ruff: noqa: T201
from reqif.parser import ReqIFParser

input_file_path = "input.reqif"

reqif_bundle = ReqIFParser.parse(input_file_path)
for specification in reqif_bundle.core_content.req_if_content.specifications:
    print(specification.long_name)

    for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(
        specification
    ):
        print(current_hierarchy)
