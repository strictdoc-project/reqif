from typing import Union

from reqif.helpers.lxml import lxml_escape_title
from reqif.models.reqif_reqif_header import EmptyTag, ReqIFReqIFHeader


class ReqIFHeaderParser:
    @staticmethod
    def parse(xml_header) -> ReqIFReqIFHeader:
        assert xml_header.tag == "THE-HEADER"

        xml_reqif_header = xml_header.find("REQ-IF-HEADER")
        if xml_reqif_header is None:
            raise NotImplementedError(xml_header)

        xml_reqif_header_attributes = xml_reqif_header.attrib
        try:
            identifier = xml_reqif_header_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None

        comment = None
        creation_time = None
        repository_id: Union[None, str, EmptyTag] = None
        req_if_tool_id = None
        req_if_version = None
        source_tool_id = None
        title = None

        xml_comment = xml_reqif_header.find("COMMENT")
        if xml_comment is not None:
            comment = xml_comment.text

        xml_creation_time = xml_reqif_header.find("CREATION-TIME")
        if xml_creation_time is not None:
            creation_time = xml_creation_time.text

        xml_repository_id = xml_reqif_header.find("REPOSITORY-ID")
        if xml_repository_id is not None:
            if xml_repository_id.text is not None:
                repository_id = xml_repository_id.text
            else:
                repository_id = EmptyTag()

        xml_req_if_tool_id = xml_reqif_header.find("REQ-IF-TOOL-ID")
        if xml_req_if_tool_id is not None:
            req_if_tool_id = xml_req_if_tool_id.text

        xml_req_if_version = xml_reqif_header.find("REQ-IF-VERSION")
        if xml_req_if_version is not None:
            req_if_version = xml_req_if_version.text

        xml_source_tool_id = xml_reqif_header.find("SOURCE-TOOL-ID")
        if xml_source_tool_id is not None:
            source_tool_id = xml_source_tool_id.text

        xml_title = xml_reqif_header.find("TITLE")
        if xml_title is not None:
            title = xml_title.text

        return ReqIFReqIFHeader(
            identifier=identifier,
            comment=comment,
            creation_time=creation_time,
            repository_id=repository_id,
            req_if_tool_id=req_if_tool_id,
            req_if_version=req_if_version,
            source_tool_id=source_tool_id,
            title=title,
        )

    @staticmethod
    def unparse(header: ReqIFReqIFHeader) -> str:
        output = ""

        output += "  <THE-HEADER>\n"

        if header.identifier:
            output += f'    <REQ-IF-HEADER IDENTIFIER="{header.identifier}">\n'

            if header.comment:
                output += f"      <COMMENT>{header.comment}</COMMENT>\n"
            if header.creation_time:
                output += (
                    "      "
                    "<CREATION-TIME>"
                    f"{header.creation_time}"
                    "</CREATION-TIME>\n"
                )
            if header.repository_id is not None:
                if isinstance(header.repository_id, str):
                    output += (
                        "      "
                        "<REPOSITORY-ID>"
                        f"{header.repository_id}"
                        "</REPOSITORY-ID>\n"
                    )
                else:
                    output += "      <REPOSITORY-ID/>\n"
            if header.req_if_tool_id:
                output += (
                    "      "
                    "<REQ-IF-TOOL-ID>"
                    f"{header.req_if_tool_id}"
                    "</REQ-IF-TOOL-ID>\n"
                )
            if header.req_if_version:
                output += (
                    "      "
                    "<REQ-IF-VERSION>"
                    f"{header.req_if_version}"
                    "</REQ-IF-VERSION>\n"
                )
            if header.source_tool_id:
                output += (
                    "      "
                    "<SOURCE-TOOL-ID>"
                    f"{header.source_tool_id}"
                    "</SOURCE-TOOL-ID>\n"
                )
            if header.title:
                output += (
                    f"      <TITLE>{lxml_escape_title(header.title)}</TITLE>\n"
                )

            output += "    </REQ-IF-HEADER>\n"
        else:
            raise NotImplementedError

        output += "  </THE-HEADER>\n"

        return output
