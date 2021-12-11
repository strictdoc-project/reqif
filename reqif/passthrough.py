from reqif.cli.cli_arg_parser import PassthroughCommandConfig
from reqif.parser import ReqIFStage1Parser
from reqif.writer import ReqIFWriter


class ReqIFPassthrough:
    @staticmethod
    def pass_through(passthrough_config: PassthroughCommandConfig):
        reqif_bundle = ReqIFStage1Parser.parse(passthrough_config.input_file)

        reqif_xml_output = ReqIFWriter.write(reqif_bundle)
        return reqif_xml_output
