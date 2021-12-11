import os
import sys

try:
    ROOT_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    if not os.path.isdir(ROOT_PATH):
        raise FileNotFoundError
    sys.path.append(ROOT_PATH)

    from reqif.cli.cli_arg_parser import create_reqif_args_parser
    from reqif.passthrough import ReqIFPassthrough

except FileNotFoundError:
    print("error: could not locate reqif's root folder.")
    sys.exit(1)


def main():
    # How to make python 3 print() utf8
    # https://stackoverflow.com/a/3597849/598057
    # sys.stdout.reconfigure(encoding='utf-8') for Python 3.7
    sys.stdout = open(  # pylint: disable=bad-option-value,consider-using-with
        1, "w", encoding="utf-8", closefd=False
    )

    parser = create_reqif_args_parser()

    if parser.is_passthrough_command:
        config = parser.get_passthrough_config()
        input_file = config.input_file
        if not os.path.isfile(input_file):
            sys.stdout.flush()
            message = "error: passthrough command's input file does not exist"
            print(f"{message}: {input_file}")
            sys.exit(1)

        output = ReqIFPassthrough.pass_through(config)
        output_file = config.output_file
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            print(f"not a directory: {output_file}")
            sys.exit(1)
        with open(output_file, "w", encoding="UTF-8") as file:
            file.write(output)

    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
