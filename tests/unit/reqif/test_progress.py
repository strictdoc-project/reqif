import zipfile
from typing import List, Tuple

from reqif.parser import ReqIFParser, ReqIFZParser
from reqif.unparser import ReqIFUnparser, ReqIFZUnparser

REQIF_WITH_CONTENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd">
  <CORE-CONTENT>
    <REQ-IF-CONTENT>
      <SPEC-OBJECTS>
        <SPEC-OBJECT IDENTIFIER="obj-1" LAST-CHANGE="2021-10-15T11:34:36.007+02:00">
          <TYPE><SPEC-OBJECT-TYPE-REF>t</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES/>
        </SPEC-OBJECT>
        <SPEC-OBJECT IDENTIFIER="obj-2" LAST-CHANGE="2021-10-15T11:34:36.007+02:00">
          <TYPE><SPEC-OBJECT-TYPE-REF>t</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES/>
        </SPEC-OBJECT>
        <SPEC-OBJECT IDENTIFIER="obj-3" LAST-CHANGE="2021-10-15T11:34:36.007+02:00">
          <TYPE><SPEC-OBJECT-TYPE-REF>t</SPEC-OBJECT-TYPE-REF></TYPE>
          <VALUES/>
        </SPEC-OBJECT>
      </SPEC-OBJECTS>
    </REQ-IF-CONTENT>
  </CORE-CONTENT>
</REQ-IF>
"""


class ProgressRecorder:
    def __init__(self):
        self.calls: List[Tuple[str, int, int]] = []

    def __call__(self, section: str, items_done: int, items_total: int):
        self.calls.append((section, items_done, items_total))


def test_01_parse_reports_progress():
    recorder = ProgressRecorder()

    ReqIFParser.parse_from_string(REQIF_WITH_CONTENT, progress=recorder)

    assert recorder.calls == [
        ("SPEC-OBJECTS", 1, 3),
        ("SPEC-OBJECTS", 2, 3),
        ("SPEC-OBJECTS", 3, 3),
    ]


def test_02_parse_without_progress_reports_nothing():
    bundle = ReqIFParser.parse_from_string(REQIF_WITH_CONTENT)
    assert len(bundle.core_content.req_if_content.spec_objects) == 3


def test_03_unparse_reports_progress():
    bundle = ReqIFParser.parse_from_string(REQIF_WITH_CONTENT)

    recorder = ProgressRecorder()
    output = ReqIFUnparser.unparse(bundle, progress=recorder)

    assert recorder.calls == [
        ("SPEC-OBJECTS", 1, 3),
        ("SPEC-OBJECTS", 2, 3),
        ("SPEC-OBJECTS", 3, 3),
    ]
    assert output.count("<SPEC-OBJECT ") == 3
    # The callback must not affect the unparse output.
    assert output == ReqIFUnparser.unparse(bundle)


def test_04_progress_with_unparseable_children_still_reaches_total():
    # A comment node inside <SPEC-OBJECTS> is skipped by the parser but must
    # still be counted, so that items_done reaches items_total.
    reqif_with_comment = REQIF_WITH_CONTENT.replace(
        "      </SPEC-OBJECTS>",
        "        <!-- A comment. -->\n      </SPEC-OBJECTS>",
    )

    recorder = ProgressRecorder()
    ReqIFParser.parse_from_string(reqif_with_comment, progress=recorder)

    assert recorder.calls == [
        ("SPEC-OBJECTS", 1, 4),
        ("SPEC-OBJECTS", 2, 4),
        ("SPEC-OBJECTS", 3, 4),
        ("SPEC-OBJECTS", 4, 4),
    ]


def test_05_reqifz_parse_reports_file_level_progress(tmp_path):
    reqifz_path = tmp_path / "sample.reqifz"
    with zipfile.ZipFile(reqifz_path, "w") as zip_file:
        zip_file.writestr("first.reqif", REQIF_WITH_CONTENT)
        zip_file.writestr("attachment.txt", "Some attachment.")

    recorder = ProgressRecorder()
    reqifz_bundle = ReqIFZParser.parse(str(reqifz_path), progress=recorder)

    assert recorder.calls == [
        ("first.reqif", 1, 2),
        ("attachment.txt", 2, 2),
    ]
    assert len(reqifz_bundle.reqif_bundles) == 1
    assert len(reqifz_bundle.attachments) == 1


def test_06_reqifz_unparse_reports_file_level_progress(tmp_path):
    reqifz_path = tmp_path / "sample.reqifz"
    with zipfile.ZipFile(reqifz_path, "w") as zip_file:
        zip_file.writestr("first.reqif", REQIF_WITH_CONTENT)
        zip_file.writestr("attachment.txt", "Some attachment.")
    reqifz_bundle = ReqIFZParser.parse(str(reqifz_path))

    recorder = ProgressRecorder()
    output_bytes = ReqIFZUnparser.unparse(reqifz_bundle, progress=recorder)

    assert recorder.calls == [
        ("first.reqif", 1, 2),
        ("attachment.txt", 2, 2),
    ]
    # The callback must not affect the unparse output.
    assert output_bytes == ReqIFZUnparser.unparse(reqifz_bundle)
