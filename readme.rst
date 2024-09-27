
PDF Table of Contents Generator
===============================

This Python module allows you to generate a table of contents (TOC) for a PDF file based on a formatted text file. The TOC can have hierarchical levels such as top-level, sublevel, and sub-sublevel items.

Keywords: "Generate outline pdf"

Overview
--------

The module reads a PDF file and a text file with titles and page numbers, then writes a new PDF file with an outline (TOC) that matches the structure of the text file.

Functions
---------

### isName(line: str) -> bool
Checks if a line is a valid name (non-empty, non-whitespace, non-numeric).

**Arguments:**
- `line`: A string representing a line of text.

**Returns:** `True` if the line is a valid name, otherwise `False`.

### matchPattern(line: str, pattern: str) -> bool
Matches a line of text against a given regex pattern.

**Arguments:**
- `line`: The line of text to be matched.
- `pattern`: The regex pattern to check against.

**Returns:** `True` if the line matches the pattern, otherwise `False`.

### writeTableOfContents(d: dict) -> None
Writes a table of contents (TOC) to a new PDF file based on a provided dictionary of parameters.

**Arguments:**
- `d`: A dictionary containing the following keys:
  - `src`: Path to the source PDF file.
  - `dst`: Path to the destination PDF file (this file will be created or overwritten).
  - `contents`: Path to a text file containing the TOC structure.
  - `toplevel`: A regex pattern for top-level items (optional).
  - `sublevel`: A regex pattern for sublevel items (optional).
  - `subsublevel`: A regex pattern for sub-sublevel items (optional).

This function reads the content file line by line, matches patterns, and adds outline items to the PDF file.

### generateOutline(src: str, dst: str, contents: str, toplevel_pattern: str | None, sublevel_pattern: str | None, subsublevel_pattern: str | None) -> bool
A wrapper function for `writeTableOfContents`. It prepares the data and generates a new PDF with a table of contents.

**Arguments:**
- `src`: Path to the source PDF file.
- `dst`: Path to the destination PDF file.
- `contents`: Path to a formatted text file containing the TOC structure.
- `toplevel_pattern`: A regex pattern for top-level items (optional).
- `sublevel_pattern`: A regex pattern for sublevel items (optional).
- `subsublevel_pattern`: A regex pattern for sub-sublevel items (optional).

**Returns:** `True` if the outline is successfully generated, otherwise `False`.

Usage
-----

1. **Prepare your content file**: 
   Create a plain text file with titles and page numbers. For example:

   .. code-block::

      Chapter I: Introduction
      1
      Section 1.1: Basics
      2
      Subsection 1.1.1: Definitions
      3

2. **Call the generateOutline function**: 
   Use the `generateOutline` function to create the TOC in your PDF file.

   .. code-block:: python

      import pdf_outline as po

      src_pdf = "/path/to/source.pdf"
      dst_pdf = "/path/to/destination.pdf"
      contents_txt = "/path/to/contents.txt"

      toplevel_pattern = r"Chapter\s\d+"
      sublevel_pattern = r"Section\s\d+"
      subsublevel_pattern = r"Subsection\s\d+"

      success = po.generateOutline(src_pdf, dst_pdf, contents_txt, toplevel_pattern, sublevel_pattern, subsublevel_pattern)

      if success:
          print("Outline generated successfully!")
      else:
          print("Failed to generate outline.")

Requirements
------------

- `pypdf` `GitHub <https://github.com/py-pdf/pypdf>`
- `os` (standard library)
- `re` (standard library)

License
-------

This project is licensed under the GNU GPL v3.0.
