from lxml.html import fragment_fromstring

# Elements after which the text continues on a new line. Without a break, the
# words of adjacent blocks run together when the XHTML has no whitespace
# between the tags, e.g., "<p>First.</p><p>Second.</p>".
BLOCK_TAGS = {
    "address",
    "blockquote",
    "dd",
    "div",
    "dl",
    "dt",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}

# Markers for the breaks, from the Unicode Private Use Area. lxml does not
# accept control characters in text, and these code points have no meaning in
# requirement text.
_PARAGRAPH_BREAK = "\ue000"
_LINE_BREAK = "\ue001"


def xhtml_to_plain_text(xhtml: str, keep_paragraphs: bool = False) -> str:
    """
    Convert an XHTML attribute value to plain text.

    The input is an XHTML fragment without namespace prefixes, such as
    SpecObjectAttribute.value_stripped_xhtml. The fragment may have several
    top-level elements, plain text only, or be empty.

    The whitespace of the XHTML is collapsed, and block elements such as
    <p>, <li> or <div>, as well as <br/>, separate the words of adjacent
    blocks.

    By default, the result is one line. With keep_paragraphs=True, the
    blocks are separated by a blank line and <br/> starts a new line.
    """
    root = fragment_fromstring(xhtml, create_parent="div")
    for element in root.iterdescendants():
        if not isinstance(element.tag, str):
            # Comments and processing instructions.
            continue
        tag = element.tag.lower()
        if tag == "br":
            element.tail = _LINE_BREAK + (element.tail or "")
        elif tag in BLOCK_TAGS:
            element.text = _PARAGRAPH_BREAK + (element.text or "")
            element.tail = _PARAGRAPH_BREAK + (element.tail or "")
    text = root.text_content()

    if not keep_paragraphs:
        text = text.replace(_PARAGRAPH_BREAK, " ").replace(_LINE_BREAK, " ")
        return " ".join(text.split())

    paragraphs = []
    for paragraph in text.split(_PARAGRAPH_BREAK):
        lines = [" ".join(line.split()) for line in paragraph.split(_LINE_BREAK)]
        lines = [line for line in lines if line]
        if lines:
            paragraphs.append("\n".join(lines))
    return "\n\n".join(paragraphs)
