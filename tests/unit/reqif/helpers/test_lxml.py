from lxml import etree

from reqif.helpers.lxml import dump_xml_node


def test_01_dump_xml() -> None:
    spec_type_string = """\
<PARENT>
  <CHILD>text</CHILD>
</PARENT>\
"""
    spec_type_xml = etree.fromstring(spec_type_string)
    dump = dump_xml_node(spec_type_xml)

    assert dump == spec_type_string
