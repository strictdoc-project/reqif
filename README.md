# ReqIF

ReqIF is a Python library for working with ReqIF format.

## Supported features

- Parsing/unparsing ReqIF
- Formatting (pretty-printing) ReqIF
- Basic validation of ReqIF
- Anonymizing ReqIF files to safely exchange the problematic ReqIF files.

To be implemented:

- Converting from/to Excel and other formats

## Getting started

```bash
pip install reqif
```

## Using ReqIF as a library

### Parsing ReqIF

```py
from reqif.parser import ReqIFParser

input_file_path = "input.reqif"

reqif_bundle = ReqIFParser.parse(input_file_path)
for specification in reqif_bundle.core_content.req_if_content.specifications:
    print(specification.long_name)

    for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(specification):
        print(current_hierarchy)
```

or for ReqIFz files:

```py
from reqif.parser import ReqIFZParser

input_file_path = "input.reqifz"

reqifz_bundle = ReqIFZParser.parse(input_file_path)
for reqif_bundle in reqifz_bundle.reqif_bundles:
    for specification in reqif_bundle.core_content.req_if_content.specifications:
        print(specification.long_name)

for attachment in reqifz_bundle.attachments:
    print(attachment)
```

### Unparsing ReqIF

```py
from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser

input_file_path = "input.sdoc"
output_file_path = "output.sdoc"

reqif_bundle = ReqIFParser.parse(input_file_path)
reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
with open(output_file_path, "w", encoding="UTF-8") as output_file:
    output_file.write(reqif_xml_output)
```

The contents of `reqif_xml_output` should be the same as the contents of the 
`input_file`.

## Using ReqIF as a command-line tool

### Passthrough command

Before using the ReqIF library, it is useful to check if it fully understands a
particular ReqIF file format that a user has in hand. The `passthrough` command
first parses the ReqIF XML into in-memory Python objects and then unparses
these Python objects back to an output ReqIF file.

If everything goes fine, the output of the passthrough command should be
identical to the contents of the input file.

`tests/integration/examples` contains samples of ReqIF files found on the 
internet. The integration tests ensure that for these samples, the passthrough
command always produces outputs that are identical to inputs. 

### Formatting ReqIF

The `format` command is similar to `clang-format` for C/C++ files or 
`cmake-format` for CMake files. The input file is parsed and then pretty-printed
back to an output file.

This command is useful when dealing with ReqIF files that are hand-written or
ReqIF files produced by the ReqIF tools that do not generate a well-formed XML
with consistent indentation.  

The `tests/integration/commands/format` contains typical examples of
incorrectly formatted ReqIF files. The integration tests ensure that the
`format` command fixes these issues.

### Anonymizing ReqIF

The anonymization helps when exchanging ReqIF documents between different ReqIF
tools including this `reqif` library. If a particular file is not recognized
correctly by a tool, a user can send their anonymized file to a developer for
further inspection.

The anonymize command accepts an input `.reqif` file and produces an anonymized
version of that file to the output `.reqif` file.

```
usage: reqif anonymize [-h] input_file output_file
main.py anonymize: error: the following arguments are required: input_file, output_file
```

Examples of anonymization:

```xml
...
<ATTRIBUTE-VALUE-STRING THE-VALUE="...Anonymized-2644691225...">
...
<ATTRIBUTE-VALUE-XHTML>
  <DEFINITION>
    <ATTRIBUTE-DEFINITION-XHTML-REF>rmf-7d0ed062-e964-424c-8305-45067118d959</ATTRIBUTE-DEFINITION-XHTML-REF>
  </DEFINITION>
  <THE-VALUE>...Anonymized-141441514...</THE-VALUE>
...
```

The anonymization algorithm preserves the uniqueness of the anonymized strings
in the document. This way, if the requirement UID identifiers are anonymized,
they will still be unique strings in an anonymized document.

## Implementation details

The core of the library is a **ReqIF first-stage parser** that only transforms
the contents of a ReqIF XML file into a ReqIF in-memory representation. The
in-memory representation is a tree of Python objects that map directly to the 
objects of the ReqIF XML file structure (e.g, Spec Objects, Spec Types, Data
Types, Specifications, etc.).

### Parsing: Converting from ReqIF to other formats

The first-stage parser (implemented by the class `ReqIFParser`) can be used by
user's second-stage parser/converter scripts that convert the ReqIF in-memory
structure into a desired format such as Excel, HTML or other formats. The
two-stage process allows the first stage parsing to focus solely on creating an
in-memory ReqIF object tree, while the second stage parsing can further parse
the ReqIF object tree according to the logical structure of user's documents as
encoded in the ReqIF XML file that was produced by user's requirements
management tool.

### Unparsing: Converting from other formats to ReqIF

The reverse process is also possible. A user's script converts another format's
contents into a ReqIF in-memory representation. The ReqIF un-parser
(implemented by the class `ReqIFUnparser`) can be used to render the in-memory
objects to the ReqIF XML file.

### Tolerance

The first-stage parser is made tolerant against possible issues in ReqIF.
It should be possible to parse a ReqIF file even if it is missing important
information.

A minimum ReqIF parsed by the `reqif`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0">
</REQ-IF>
```

A separate validation command shall be used to confirm the validity
of the ReqIF contents.

### Printing of the attributes

The `reqif` library uses a simple convention for printing the XML attributes: the
attributes are always printed in the alphabetic order of their attribute names.

```xml
<DATATYPE-DEFINITION-REAL ACCURACY="10" IDENTIFIER="ID_TC1000_DatatypeDefinitionReal" LAST-CHANGE="2012-04-07T01:51:37.112+02:00" LONG-NAME="TC1000 DatatypeDefinitionReal" MAX="1234.5678" MIN="-1234.5678"/>
```

Some tools do not respect this rule: for example some tools will print
the attribute `ACCURACY="10"` after the `LONG-NAME` attribute but the `reqif`
library does not provide support for preserving a non-alphabetic order of the
attributes.

### A bottom-up overview of the ReqIF format

- ReqIF is a standard. See reference document [RD01](#rd01-reqif-standard).
- ReqIF has a fixed structure (see "What is common for all ReqIF documents" 
below)
- ReqIF standard does not define a document structure for every documents so
a ReqIF tool implementor is free to choose between several implementation 
approaches. There is a
[ReqIF Implementation Guide](#rd02-reqif-implementation-guide)
that attempts to harmonize ReqIF tool developments. See also
"What is left open by the ReqIF standard" below.
- ReqIF files produced by various tool often have incomplete schemas. 

### What is common for all ReqIF documents

- All documents have ReqIF tags:
  - Document metadata is stored inside tags of `REQ-IF-HEADER` tag.
  - Requirements are stored as `<SPEC-OBJECT>`s
  - Requirements types are stored as `<SPEC-TYPE>`s
  - Supported data types are stored as `<DATATYPE>`
  - Relationships such as 'Parent-Child' as stored as `<SPEC-RELATIONS>`

### What is left open by the ReqIF standard
 
- How to distinguish requirements from headers/sections?
  - One way: create separate `SPEC-TYPES`: one or more for requirements and
    one for sections.
  - Another way: have one spec type but have it provide a `TYPE` field that can
    be used to distinguish between `REQUIREMENT` or `SECTION`.
  - Yet another way: Check if the "ReqIF.ChapterName" is present on the spec object.
    When present, it is a section. When not, it is a requirement.

## Reference documents

### [RD01] ReqIF standard

The latest version is 1.2:
[Requirements Interchange Format](https://www.omg.org/spec/ReqIF)

### [RD02] ReqIF Implementation Guide 

[ReqIF Implementation Guide v1.8](https://www.prostep.org/fileadmin/downloads/prostep-ivip_ImplementationGuide_ReqIF_V1-8.pdf)
