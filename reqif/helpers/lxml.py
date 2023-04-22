import re
from copy import deepcopy
from itertools import chain

from lxml import etree
from lxml.etree import tostring
from lxml.html import fragment_fromstring


def lxml_dump_node(node):
    return lxml_stringify_node(node)


# This code is taken from Python 3.7. The addition is escaping of the tab
# character.
def lxml_escape_for_html(string: str) -> str:
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


def lxml_escape_title(string: str) -> str:
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
def lxml_stringify_namespaced_children(node, namespace_tag=None) -> str:
    if namespace_tag is None:
        assert len(node.nsmap) > 0, (
            f"This method must be called on a namespaced tag. "
            f"Tag: {node}, line: {node.sourceline}."
        )
        nskey = next(iter(node.nsmap.keys()))
    else:
        nskey = namespace_tag

    def _lxml_stringify_reqif_ns_node(node):
        output = ""
        node_no_ns_tag = etree.QName(node).localname

        # There are ReqIF files where the XHTML-based tags can have their own
        # namespace that overrides the document-level namespace. Making the best
        # effort to detect this case. Example:
        # <THE-VALUE>
        #   <div xmlns="http://www.w3.org/1999/xhtml">
        #     &quot;New Header&quot; Template reqFile
        #   </div>
        # </THE-VALUE>
        # FIXME: Such tricks can introduce further edge cases. Not clear how to
        # implement this properly.
        node_has_its_own_ns = False
        node_ns_match = re.search("{(.+?)}", node.tag)
        if node_ns_match:
            node_ns = node_ns_match.group(1)

            for nskey_, ns_ in node.nsmap.items():
                if ns_ == node_ns and nskey_ is None:
                    node_has_its_own_ns = True

        tag = (
            node_no_ns_tag
            if node_has_its_own_ns
            else (
                f"{nskey}:{node_no_ns_tag}"
                if node.tag[0] == "{" or namespace_tag is not None
                else node.tag
            )
        )
        output += f"<{tag}"
        if node_has_its_own_ns:
            output += f' xmlns="{node.nsmap[None]}"'

        for attribute, attribute_value in node.attrib.items():
            output += f' {attribute}="{lxml_escape_for_html(attribute_value)}"'
        # <object> is surprisingly a tag that must have a closing tag even
        # if it is empty. If self-closed, it breaks all the following markup.
        if (
            node.text is not None
            or len(node.getchildren()) > 0
            or node.tag.casefold() == "object"
        ):
            output += ">"
            if node.text is not None:
                output += lxml_escape_for_html(node.text)
            for child in node.getchildren():
                output += _lxml_stringify_reqif_ns_node(child)
            output += f"</{tag}>"
        else:
            output += "/>"

        if node.tail is not None:
            output += lxml_escape_for_html(node.tail)
        return output

    string = ""
    if node.text is not None:
        string += lxml_escape_for_html(node.text)
    for child in node.getchildren():
        string += _lxml_stringify_reqif_ns_node(child)
    return string


def lxml_stringify_node(node):
    nskey = None
    if len(node.nsmap) > 0:
        nskey = next(iter(node.nsmap.keys()))
    output = ""
    node_no_ns_tag = etree.QName(node).localname
    tag = f"{nskey}:{node_no_ns_tag}" if node.tag[0] == "{" else node.tag
    output += f"<{tag}"
    for attribute, attribute_value in node.attrib.items():
        output += f' {attribute}="{lxml_escape_for_html(attribute_value)}"'
    # <object> is surprisingly a tag that must have a closing tag even if it
    # is empty. If self-closed, it breaks all the following markup.
    if (
        node.text is not None
        or len(node.getchildren()) > 0
        or node.tag.casefold() == "object"
    ):
        output += ">"
        if node.text is not None:
            output += lxml_escape_for_html(node.text)
        for child in node.getchildren():
            output += lxml_stringify_node(child)
        output += f"</{tag}>"
    else:
        output += "/>"
    if node.tail is not None:
        output += lxml_escape_for_html(node.tail)
    return output


# https://stackoverflow.com/a/28173933/598057
def lxml_stringify_children(node):
    return "".join(
        chunk
        for chunk in chain(
            (node.text,),
            chain(
                *(
                    (
                        lxml_stringify_node(child),
                        child.tail,
                    )
                    for child in node.getchildren()
                )
            ),
            # The original snippet prints the node tail for some reason which is
            # surprisingly unnecessary.
            # (node.tail,),  # noqa: ERA001
            (None,),
        )
        if chunk
    )


def lxml_convert_to_reqif_ns_xhtml_string(string, reqif_xhtml=True) -> str:
    namespace_tag = "reqif-xhtml" if reqif_xhtml else "xhtml"
    node = fragment_fromstring(string, create_parent="NOT-USED")
    return lxml_stringify_namespaced_children(node, namespace_tag=namespace_tag)


def lxml_convert_from_reqif_ns_xhtml_string(lxml_node) -> str:
    lxml_node_deep_copy = deepcopy(lxml_node)
    lxml_strip_namespace_from_xml(lxml_node_deep_copy, full=True)
    return tostring(
        lxml_node_deep_copy, encoding=str, pretty_print=True
    ).rstrip()


def lxml_convert_children_from_reqif_ns_xhtml_string(lxml_node) -> str:
    lxml_node_deep_copy = deepcopy(lxml_node)
    lxml_strip_namespace_from_xml(lxml_node_deep_copy, full=True)
    return lxml_stringify_children(lxml_node_deep_copy)


def lxml_is_self_closed_tag(xml):
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
