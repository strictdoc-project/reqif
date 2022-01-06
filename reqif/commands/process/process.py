import os
import sys

import pandas as pd

from reqif.cli.cli_arg_parser import ProcessCommandConfig
from reqif.parser import ReqIFParser


class ProcessCommand:
    @classmethod
    def execute(cls, config: ProcessCommandConfig):
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: process command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        reqif_bundle = ReqIFParser.parse(config.input_file)
        print(reqif_bundle)

        spec_object_entry_list = []
        for spec_object in reqif_bundle.core_content.req_if_content.spec_objects:
            spec_object_entry = {}
            for attribute in spec_object.attributes:
                spec_object_entry[attribute.name] = attribute.value
            spec_object_entry_list.append(spec_object_entry)

        print(pd.DataFrame(spec_object_entry_list))

        print("TBD: What next?")
        exit(1)
