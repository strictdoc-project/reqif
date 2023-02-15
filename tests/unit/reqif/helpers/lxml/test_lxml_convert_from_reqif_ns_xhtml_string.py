from lxml.etree import fromstring

from reqif.helpers.lxml import (
    lxml_convert_from_reqif_ns_xhtml_string,
)


def test__01__() -> None:
    spec_type_string = """\
<xhtml:div xmlns:xhtml="http://www.w3.org/1999/xhtml">Some<xhtml:span>combination</xhtml:span>of<xhtml:b>tags</xhtml:b></xhtml:div>\
"""  # noqa: E501
    expected_spec_type_string = """\
<div>Some<span>combination</span>of<b>tags</b></div>\
"""
    lxml_node = fromstring(spec_type_string)
    xhtml_string = lxml_convert_from_reqif_ns_xhtml_string(lxml_node=lxml_node)
    assert xhtml_string == expected_spec_type_string
