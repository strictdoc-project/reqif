import html
from itertools import chain

from lxml import etree
from lxml.etree import tostring


def dump_xml_node(node):
    return etree.tostring(node, method="xml").decode("utf8")


# Using this rather hacky version because I could not make lxml to print
# the namespaced tags such as:
# <reqif-xhtml:div>--/reqif-xhtml:div>
# but at the same time NOT print the namespace declaration which is produced
# when the etree.tostring(...) method is used:
# <reqif-xhtml:div xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml">--</reqif-xhtml:div>  # noqa: E501
# FIXME: Would be great to find a better solution for this.
def stringify_namespaced_children(node):
    def _stringify_reqif_ns_node(node):
        assert node is not None
        nskey = next(iter(node.nsmap.keys()))
        output = ""
        node_no_ns_tag = etree.QName(node).localname
        output += f"<{nskey}:{node_no_ns_tag}"
        for attribute, attribute_value in node.attrib.items():
            output += f' {attribute}="{attribute_value}"'
        output += ">"
        if node.text is not None:
            output += html.escape(node.text)
        for child in node.getchildren():
            output += _stringify_reqif_ns_node(child)
        output += f"</{nskey}:{node_no_ns_tag}>"
        if node.tail is not None:
            output += node.tail
        return output

    string = ""
    if node.text is not None:
        string += html.escape(node.text)
    for child in node.getchildren():
        string += _stringify_reqif_ns_node(child)
    return string


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
