from reqif.cli.cli_arg_parser import PassthroughCommandConfig
from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser


class ReqIFPassthrough:
    @staticmethod
    def pass_through(passthrough_config: PassthroughCommandConfig):
        reqif_bundle = ReqIFParser.parse(passthrough_config.input_file)
        reqif_xml_output = ReqIFUnparser.write(reqif_bundle)
        return reqif_xml_output
