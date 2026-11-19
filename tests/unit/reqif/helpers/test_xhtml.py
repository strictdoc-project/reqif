import pytest

from reqif.helpers.xhtml import xhtml_to_plain_text

INDENTED = """
<div>
  <p>The system <b>shall</b> lock after:</p>
  <ul>
    <li>5 attempts, or</li>
    <li>admin request.</li>
  </ul>
</div>
"""

COMPACT = (
    "<div><p>The system <b>shall</b> lock after:</p>"
    "<ul><li>5 attempts, or</li><li>admin request.</li></ul></div>"
)


@pytest.mark.parametrize(
    "xhtml, expected",
    [
        (INDENTED, "The system shall lock after: 5 attempts, or admin request."),
        (COMPACT, "The system shall lock after: 5 attempts, or admin request."),
        ("<p>First.</p><p>Second.</p>", "First. Second."),
        ("<div>Line one<br/>Line two</div>", "Line one Line two"),
        ("<div>Some <i>inline</i> <b>markup</b>.</div>", "Some inline markup."),
        ("Plain text only", "Plain text only"),
        ("Before<p>inside</p>after", "Before inside after"),
        ("", ""),
        ("<div></div>", ""),
    ],
)
def test_xhtml_to_plain_text(xhtml, expected):
    assert xhtml_to_plain_text(xhtml) == expected


@pytest.mark.parametrize(
    "xhtml, expected",
    [
        (
            INDENTED,
            "The system shall lock after:\n\n5 attempts, or\n\nadmin request.",
        ),
        (
            COMPACT,
            "The system shall lock after:\n\n5 attempts, or\n\nadmin request.",
        ),
        ("<p>First.</p><p>Second.</p>", "First.\n\nSecond."),
        ("<div>Line one<br/>Line two</div>", "Line one\nLine two"),
        ("<div><p>Nested</p></div><div>blocks</div>", "Nested\n\nblocks"),
        ("", ""),
    ],
)
def test_xhtml_to_plain_text_keeps_paragraphs(xhtml, expected):
    assert xhtml_to_plain_text(xhtml, keep_paragraphs=True) == expected


def test_xhtml_to_plain_text_ignores_comments():
    assert xhtml_to_plain_text("<p>Text<!-- note --></p><p>more</p>") == ("Text more")
