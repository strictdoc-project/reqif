from copy import deepcopy
from itertools import chain

from lxml import etree
from lxml.etree import tostring
from lxml.html import fragment_fromstring


def dump_xml_node(node):
    return etree.tostring(node, method="xml").decode("utf8")


# This code is taken from Python 3.7. The addition is escaping of the tab
# character.
def my_escape(string: str) -> str:
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    string = string.replace("&", "&amp;")  # Must be done first!
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    string = string.replace('"', "&quot;")
    string = string.replace("'", "&#x27;")
    # Invisible tab character
    string = string.replace("\t", "&#9;")
    return string


def my_escape_title(string: str) -> str:
    # The only known reason for this method is the presence of &amp; in the
    # HEADER title of ReqIF files found at the ci.eclipse.org.
    string = string.replace("&", "&amp;")
    return string


# Using this rather hacky version because I could not make lxml to print
# the namespaced tags such as:
# <reqif-xhtml:div>--/reqif-xhtml:div>
# but at the same time NOT print the namespace declaration which is produced
# when the etree.tostring(...) method is used:
# <reqif-xhtml:div xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml">--</reqif-xhtml:div>  # noqa: E501
# FIXME: Would be great to find a better solution for this.
def stringify_namespaced_children(node, namespace_tag=None) -> str:
    if namespace_tag is None:
        nskey = next(iter(node.nsmap.keys()))
    else:
        nskey = namespace_tag

    def _stringify_reqif_ns_node(node):
        assert node is not None

        output = ""
        node_no_ns_tag = etree.QName(node).localname
        output += f"<{nskey}:{node_no_ns_tag}"
        for attribute, attribute_value in node.attrib.items():
            output += f' {attribute}="{my_escape(attribute_value)}"'
        if node.text is not None or len(node.getchildren()) > 0:
            output += ">"
            if node.text is not None:
                output += my_escape(node.text)
            for child in node.getchildren():
                output += _stringify_reqif_ns_node(child)
            output += f"</{nskey}:{node_no_ns_tag}>"
        else:
            output += "/>"

        if node.tail is not None:
            output += my_escape(node.tail)
        return output

    string = ""
    if node.text is not None:
        string += my_escape(node.text)
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


def lxml_convert_to_reqif_ns_xhtml_string(string, reqif_xhtml=True) -> str:
    namespace_tag = "reqif-xhtml" if reqif_xhtml else "xhtml"
    node = fragment_fromstring(string, create_parent="NOT-USED")
    return stringify_namespaced_children(node, namespace_tag=namespace_tag)


def lxml_convert_from_reqif_ns_xhtml_string(lxml_node) -> str:
    lxml_node_deep_copy = deepcopy(lxml_node)
    lxml_strip_namespace_from_xml(lxml_node_deep_copy, full=True)
    return tostring(
        lxml_node_deep_copy, encoding=str, pretty_print=True
    ).rstrip()


def is_self_closed_tag(xml):
    # The tag cannot be closed if it has children or has a non-None text.
    if len(xml.getchildren()) > 0:
        return False
    if xml.text is not None:
        return False
    return True


def lxml_strip_namespace_from_xml(root_xml, full=False):
    for elem in root_xml.getiterator():
        # Remove an XML namespace URI in the element's name but keep the
        # namespaces in the HTML content as found in the
        # <ATTRIBUTE-VALUE-XHTML> of ReqIF XML.
        if not full and "http://www.w3.org/1999/xhtml" in elem.tag:
            continue
        elem.tag = etree.QName(elem).localname
    # Remove unused namespace declarations
    etree.cleanup_namespaces(root_xml)
    return root_xml
