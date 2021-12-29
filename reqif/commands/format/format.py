from lxml import etree

from reqif.cli.cli_arg_parser import FormatCommandConfig


class FormatCommand:
    @classmethod
    def execute(cls, config: FormatCommandConfig):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(config.input_file, parser)
        tree.write(
            config.output_file,
            doctype='<?xml version="1.0" encoding="UTF-8"?>',
            pretty_print=True,
        )
