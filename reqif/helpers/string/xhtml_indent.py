import re

PATTERN_XHTML_INDENTED_16 = re.compile(r" {16}")
PATTERN_XHTML_UNINDENTED_16 = re.compile(r"\n")

PADDING_14 = "              "
PADDING_16 = "                "


def reqif_indent_xhtml_string(string: str) -> str:
    return (
        PATTERN_XHTML_UNINDENTED_16.sub(
            "\n" + PADDING_16, "\n" + string.strip()
        )
        + "\n"
        + PADDING_14
    )


def reqif_unindent_xhtml_string(string: str) -> str:
    return PATTERN_XHTML_INDENTED_16.sub("", string).strip()
