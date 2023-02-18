from lxml import etree

from reqif.helpers.lxml import (
    lxml_dump_node,
)


def test__01__basic() -> None:
    spec_type_string = """\
<PARENT>
  <CHILD>text</CHILD>
</PARENT>\
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    dump = lxml_dump_node(spec_type_xml)

    assert dump == spec_type_string


def test__02__xhtml() -> None:
    expected_string = """\
<THE-VALUE>
    AA<reqif-xhtml:div>
      11<reqif-xhtml:span attr="FOO">--<div>123</div>--</reqif-xhtml:span>22
    </reqif-xhtml:div>BB
  </THE-VALUE>
"""

    spec_type_string = """\
<THE-ROOT xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml">\
  <THE-VALUE>
    AA<reqif-xhtml:div>
      11<reqif-xhtml:span attr="FOO">--<div>123</div>--</reqif-xhtml:span>22
    </reqif-xhtml:div>BB
  </THE-VALUE>
</THE-ROOT>
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    string = lxml_dump_node(spec_type_xml.find("THE-VALUE"))

    assert string == expected_string
