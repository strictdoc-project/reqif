from lxml import etree

from reqif.helpers.lxml import (
    lxml_is_self_closed_tag,
    lxml_stringify_namespaced_children,
)


def test__02_stringify_namespaced_children__01_basic() -> None:
    expected_string = "\n<reqif-xhtml:div>--</reqif-xhtml:div>\n"

    spec_type_string = f"""\
<THE-VALUE xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml">\
{expected_string}\
</THE-VALUE>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    string = lxml_stringify_namespaced_children(spec_type_xml)

    assert string == expected_string


def test__02_stringify_namespaced_children__02_nested_tags_and_attrs() -> None:
    expected_string = """
AA<reqif-xhtml:div>\
11<reqif-xhtml:span attr="FOO">--</reqif-xhtml:span>22\
</reqif-xhtml:div>BB
"""

    spec_type_string = f"""\
<THE-VALUE xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml">\
{expected_string}\
</THE-VALUE>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    string = lxml_stringify_namespaced_children(spec_type_xml)

    assert string == expected_string


def test__is_self_closed_tag() -> None:
    spec_type_string = """\
<THE-VALUE>\
Text
</THE-VALUE>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    assert lxml_is_self_closed_tag(spec_type_xml) is False

    spec_type_string = """\
<THE-VALUE></THE-VALUE>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    assert lxml_is_self_closed_tag(spec_type_xml) is True

    spec_type_string = """\
<THE-VALUE/>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    assert lxml_is_self_closed_tag(spec_type_xml) is True
