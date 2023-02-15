from reqif.helpers.string.xhtml_indent import (
    reqif_indent_xhtml_string,
    reqif_unindent_xhtml_string,
)


def test__reqif_unindent_xhtml_string__01() -> None:
    expected_string = """\
<xhtml:div>
  <xhtml:p style=" font-style: italic">Delay <xhtml:span style="text-decoration: underline;">&lt;= 5s</xhtml:span></xhtml:p>
</xhtml:div>\
"""  # noqa: E501

    indented_string = """
                <xhtml:div>
                  <xhtml:p style=" font-style: italic">Delay <xhtml:span style="text-decoration: underline;">&lt;= 5s</xhtml:span></xhtml:p>
                </xhtml:div>
              \
"""  # noqa: E501
    string = reqif_unindent_xhtml_string(indented_string)
    assert string == expected_string


def test__reqif_indent_xhtml_string__01() -> None:
    unindented_string = """\
<xhtml:div>
  <xhtml:p style=" font-style: italic">Delay <xhtml:span style="text-decoration: underline;">&lt;= 5s</xhtml:span></xhtml:p>
</xhtml:div>\
"""  # noqa: E501

    expected_string = """
                <xhtml:div>
                  <xhtml:p style=" font-style: italic">Delay <xhtml:span style="text-decoration: underline;">&lt;= 5s</xhtml:span></xhtml:p>
                </xhtml:div>
              \
"""  # noqa: E501
    string = reqif_indent_xhtml_string(unindented_string)
    assert string == expected_string


def test__reqif_indent_and_unindent_roundtrip() -> None:
    string = ""
    indented_string = reqif_indent_xhtml_string(string)
    unindented_string = reqif_unindent_xhtml_string(indented_string)
    assert string == unindented_string

    string = "<xhtml></xhtml>"
    indented_string = reqif_indent_xhtml_string(string)
    unindented_string = reqif_unindent_xhtml_string(indented_string)
    assert string == unindented_string

    string = "<xhtml></xhtml>\n<xhtml></xhtml>"
    indented_string = reqif_indent_xhtml_string(string)
    unindented_string = reqif_unindent_xhtml_string(indented_string)
    assert string == unindented_string

    string = "<xhtml></xhtml>\n<xhtml></xhtml>\n<xhtml></xhtml>"
    indented_string = reqif_indent_xhtml_string(string)
    unindented_string = reqif_unindent_xhtml_string(indented_string)
    assert string == unindented_string
