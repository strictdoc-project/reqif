# ReqIF

ReqIF is a Python library for working with ReqIF format.

Supported features:

- Parsing/unparsing ReqIF
- Formatting (pretty-printing) ReqIF

To be implemented:

- Validating ReqIF
- Converting from/to Excel and other formats

**The project is under construction.**

## Getting started

```bash
pip install reqif
```

## Using ReqIF as a library

### Parsing ReqIF

```py
reqif_bundle = ReqIFParser.parse(input_file_path)
for specification in reqif_bundle.core_content.req_if_content.specifications
    print(specification.long_name)

    for current_hierarchy in reqif_bundle.iterate_specification_hierarchy(specification):
        print(current_hierarchy)
```

### Unparsing ReqIF

```py
reqif_bundle = ReqIFParser.parse(input_file_path)
reqif_xml_output = ReqIFUnparser.unparse(reqif_bundle)
with open(output_file_path, "w", encoding="UTF-8") as output_file:
    output_file.write(reqif_xml_output)
```

The contents of `reqif_xml_output` should be the same as that the `input_file`.

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

This command is similar to `clang-format` for C/C++ files or `cmake-format` for
CMake files. The input file is parsed and then pretty-printed back to an output
file.

This command is useful when dealing with ReqIF files that are hand-written or
ReqIF files produced by the ReqIF tools that do not generate a well-formed XML
with consistent indentation.  

The `tests/integration/commands/format` contains typical examples of
incorrectly formatted ReqIF files. The integration tests ensure that the
`format` command fixes these issues.

## Implementation details

### Tolerance

The first-stage parser is made tolerant against possible issues in ReqIF.
It should be possible to parse a ReqIF file even if it is missing important
information. A separate validation command shall be used to confirm the validity
of the ReqIF contents.

## A bottom-up overview of the ReqIF format

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

## Reference documents

### [RD01] ReqIF standard

The latest version is 1.2:
[Requirements Interchange Format](https://www.omg.org/spec/ReqIF)

### [RD02] ReqIF Implementation Guide 

[ReqIF Implementation Guide](https://www.prostep.org/fileadmin/downloads/PSI_ImplementationGuide_ReqIF_V1-7.pdf)
