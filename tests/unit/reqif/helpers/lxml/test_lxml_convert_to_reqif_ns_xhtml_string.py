from reqif.helpers.lxml import (
    lxml_convert_to_reqif_ns_xhtml_string,
)


def test__reqif_convert_to_ns_xhtml_string__1__xhtml_ns() -> None:
    spec_type_string = """\
<div>Some<span>combination</span>of<b>tags</b></div>\
"""
    expected_spec_type_string = """\
<xhtml:div>Some<xhtml:span>combination</xhtml:span>of<xhtml:b>tags</xhtml:b></xhtml:div>\
"""

    ns_xhtml_string = lxml_convert_to_reqif_ns_xhtml_string(
        spec_type_string, reqif_xhtml=False
    )

    assert ns_xhtml_string == expected_spec_type_string


def test__reqif_convert_to_ns_xhtml_string__2__reqif_xhtml_ns() -> None:
    spec_type_string = """\
<div>Some<span>combination</span>of<b>tags</b></div>\
"""
    expected_spec_type_string = """\
<reqif-xhtml:div>Some<reqif-xhtml:span>combination</reqif-xhtml:span>of<reqif-xhtml:b>tags</reqif-xhtml:b></reqif-xhtml:div>\
"""

    ns_xhtml_string = lxml_convert_to_reqif_ns_xhtml_string(
        spec_type_string, reqif_xhtml=True
    )

    assert ns_xhtml_string == expected_spec_type_string


def test__reqif_convert_to_ns_xhtml_string__3__string_without_tags() -> None:
    spec_type_string = """\
Some combination of words. Multi string.\
"""
    expected_spec_type_string = """\
Some combination of words. Multi string.\
"""

    ns_xhtml_string = lxml_convert_to_reqif_ns_xhtml_string(
        spec_type_string, reqif_xhtml=False
    )

    assert ns_xhtml_string == expected_spec_type_string
