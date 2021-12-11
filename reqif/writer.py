from reqif.reqif_bundle import ReqIFBundle


class ReqIFWriter:
    @staticmethod
    def write(bundle: ReqIFBundle) -> str:
        reqif_xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        if bundle.namespace is not None and bundle.configuration is not None:
            reqif_xml_output += (
                f"<REQ-IF "
                f'xmlns="{bundle.namespace}" '
                f'xmlns:configuration="{bundle.configuration}">'
                "\n"
            )
        else:
            raise NotImplementedError

        if bundle.core_content is not None:
            reqif_xml_output += "  <CORE-CONTENT>\n"
            reqif_xml_output += "    <REQ-IF-CONTENT>\n"
            reqif_xml_output += "    </REQ-IF-CONTENT>\n"
            reqif_xml_output += "  </CORE-CONTENT>\n"

        reqif_xml_output += "</REQ-IF>" "\n"
        return reqif_xml_output
