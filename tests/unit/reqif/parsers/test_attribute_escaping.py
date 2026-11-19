from lxml import etree

from reqif.parsers.relation_group_parser import ReqIFRelationGroupParser
from reqif.parsers.spec_hierarchy_parser import ReqIFSpecHierarchyParser
from reqif.parsers.spec_object_parser import SpecObjectParser
from reqif.parsers.spec_relation_parser import SpecRelationParser

# DESC and LONG-NAME are unescaped by lxml when parsing, so unparse has to
# escape them again, or the output is not well-formed XML.
SPECIAL = "A &amp; B &lt;C&gt; &quot;D&quot;"
SPECIAL_VALUE = 'A & B <C> "D"'


def _round_trip(parser, xml: str, **unparse_kwargs):
    node = parser.parse(etree.fromstring(xml))
    output = parser.unparse(node, **unparse_kwargs)
    return node, parser.parse(etree.fromstring(output))


def test_spec_object_desc_and_long_name_are_escaped():
    original, reparsed = _round_trip(
        SpecObjectParser,
        f"""
<SPEC-OBJECT DESC="{SPECIAL}" IDENTIFIER="SO-1" LONG-NAME="{SPECIAL}">
  <TYPE><SPEC-OBJECT-TYPE-REF>SOT-1</SPEC-OBJECT-TYPE-REF></TYPE>
</SPEC-OBJECT>
""",
    )
    assert original.description == SPECIAL_VALUE
    assert reparsed.description == SPECIAL_VALUE
    assert reparsed.long_name == SPECIAL_VALUE


def test_spec_relation_desc_is_escaped():
    _, reparsed = _round_trip(
        SpecRelationParser,
        f"""
<SPEC-RELATION DESC="{SPECIAL}" IDENTIFIER="SR-1" LONG-NAME="{SPECIAL}">
  <TYPE><SPEC-RELATION-TYPE-REF>SRT-1</SPEC-RELATION-TYPE-REF></TYPE>
  <SOURCE><SPEC-OBJECT-REF>SO-1</SPEC-OBJECT-REF></SOURCE>
  <TARGET><SPEC-OBJECT-REF>SO-2</SPEC-OBJECT-REF></TARGET>
</SPEC-RELATION>
""",
    )
    assert reparsed.description == SPECIAL_VALUE
    assert reparsed.long_name == SPECIAL_VALUE


def test_relation_group_desc_and_long_name_are_escaped():
    _, reparsed = _round_trip(
        ReqIFRelationGroupParser,
        f"""
<RELATION-GROUP DESC="{SPECIAL}" IDENTIFIER="RG-1" LONG-NAME="{SPECIAL}">
  <SOURCE-SPECIFICATION><SPECIFICATION-REF>S-1</SPECIFICATION-REF></SOURCE-SPECIFICATION>
  <SPEC-RELATIONS><SPEC-RELATION-REF>SR-1</SPEC-RELATION-REF></SPEC-RELATIONS>
  <TARGET-SPECIFICATION><SPECIFICATION-REF>S-2</SPECIFICATION-REF></TARGET-SPECIFICATION>
  <TYPE><RELATION-GROUP-TYPE-REF>RGT-1</RELATION-GROUP-TYPE-REF></TYPE>
</RELATION-GROUP>
""",
    )
    assert reparsed.description == SPECIAL_VALUE
    assert reparsed.long_name == SPECIAL_VALUE


def test_spec_hierarchy_long_name_is_escaped():
    hierarchy = ReqIFSpecHierarchyParser.parse(
        etree.fromstring(
            f"""
<SPEC-HIERARCHY IDENTIFIER="SH-1" LONG-NAME="{SPECIAL}">
  <OBJECT><SPEC-OBJECT-REF>SO-1</SPEC-OBJECT-REF></OBJECT>
</SPEC-HIERARCHY>
"""
        )
    )
    output = ReqIFSpecHierarchyParser.unparse(hierarchy)
    assert f'LONG-NAME="{SPECIAL}"' in output
