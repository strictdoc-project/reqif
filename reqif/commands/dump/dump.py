from jinja2 import Environment, PackageLoader, StrictUndefined

from reqif.cli.cli_arg_parser import DumpCommandConfig
from reqif.parser import ReqIFParser


class DumpCommand:
    env = Environment(
        loader=PackageLoader("reqif", "commands/dump/templates"),
        undefined=StrictUndefined,
    )
    env.globals.update(isinstance=isinstance)

    @classmethod
    def execute(cls, config: DumpCommandConfig):
        template = cls.env.get_template("index.jinja.html")

        reqif_bundle = ReqIFParser.parse(config.input_file)

        output = template.render(reqif_bundle=reqif_bundle)
        output += "\n"

        with open(config.output_file, "w", encoding="utf8") as output_file:
            output_file.write(output)
