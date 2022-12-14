import pytest

from reqif.models.error_handling import ReqIFXMLParsingError
from reqif.parser import ReqIFParser


def test_01_minimal_reqif():
    reqif = """
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF
  xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
  xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0"
></REQ-IF>
""".strip()

    parser = ReqIFParser()
    bundle = parser.parse_from_string(reqif)

    assert (
        bundle.namespace_info.namespace
        == "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
    )
    assert (
        bundle.namespace_info.configuration
        == "http://eclipse.org/rmf/pror/toolextensions/1.0"
    )


def test_02_minimal_reqif_without_xml_decl():
    reqif = """
<REQ-IF
    xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
    xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0"
></REQ-IF>
""".strip()

    parser = ReqIFParser()
    bundle = parser.parse_from_string(reqif)

    assert (
        bundle.namespace_info.namespace
        == "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
    )
    assert (
        bundle.namespace_info.configuration
        == "http://eclipse.org/rmf/pror/toolextensions/1.0"
    )


def test_03_minimal_reqif_without_namespace_and_configuration():
    reqif = """
<REQ-IF></REQ-IF>
""".strip()

    parser = ReqIFParser()
    bundle = parser.parse_from_string(reqif)

    assert bundle.namespace_info.namespace is None
    assert bundle.namespace_info.configuration is None


def test_error_01_empty_string():
    parser = ReqIFParser()

    with pytest.raises(ReqIFXMLParsingError) as exception_info:
        parser.parse_from_string("")

    assert (
        str(exception_info.value)
        == "Document is empty, line 1, column 1 (<string>, line 1)"
    )


def test_error_02_unexpected_symbol():
    parser = ReqIFParser()

    with pytest.raises(ReqIFXMLParsingError) as exception_info:
        parser.parse_from_string("!")

    assert (
        str(exception_info.value) == "Start tag expected, "
        "'<' not found, line 1, column 1 (<string>, line 1)"
    )


def test_error_03_minimal_non_reqif_xml():
    parser = ReqIFParser()

    with pytest.raises(ReqIFXMLParsingError) as exception_info:
        parser.parse_from_string("<xml_garbage></xml_garbage>")

    assert (
        str(exception_info.value)
        == "Expected root tag to be REQ-IF, got: xml_garbage."
    )
