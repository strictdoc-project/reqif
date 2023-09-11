# ruff: noqa: T201
from reqif.parser import ReqIFZParser

input_file_path = "input.reqifz"

reqifz_bundle = ReqIFZParser.parse(input_file_path)
for reqif_bundle_file, reqif_bundle in reqifz_bundle.reqif_bundles.items():
    print(f"Bundle: {reqif_bundle_file} {reqif_bundle}")
    for (
        specification
    ) in reqif_bundle.core_content.req_if_content.specifications:
        print(specification)

for attachment in reqifz_bundle.attachments:
    print(f"Attachment: {attachment}")
