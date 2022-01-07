from itertools import chain

from lxml import etree
from lxml.etree import tostring


def dump_xml_node(node):
    return etree.tostring(node, method="xml").decode("utf8")


# https://stackoverflow.com/a/4624146/598057
def stringify_children(node):
    return "".join(
        chunk
        for chunk in chain(
            (node.text,),
            chain(
                *(
                    (tostring(child, encoding=str, with_tail=False), child.tail)
                    for child in node.getchildren()
                )
            ),
            (node.tail,),
        )
        if chunk
    )


def is_self_closed_tag(xml):
    data_type_string = etree.tostring(xml, pretty_print=True).decode("utf-8")
    return data_type_string.find(f"</{xml.tag}>") == -1
