import pypdf as pp
import os
import re

def isName(line: str) -> bool:
    """
    Returns false if line is empty, only whitespace, or numeric
    """
    ret = True
    if line.isnumeric() or line.isspace() or line == "":
        ret = False
    return ret

def matchPattern(line: str, regex_string: str):
    """
    Returns true if line matches pattern (regex)
    line: string to check
    regex_string: string, formatted r"pattern"
    """
    if not isName(line):
        return False

    regex = re.compile(regex_string)
    if regex.fullmatch(line):
        return True
    else:
        return False

def writeTableOfContents(d: dict) -> None:
    """
    Arguments:
    source: string, abs path to source pdf file 
    destination: string, abs path to destination file (overwrites or creates new file) 
    contents: string, abs path to .txt file with formatted table of contents

    Copies pdf file at source, reads annotations from contents txt file, then writes 
    new annotated file to destination
    """
    reader = None
    parent = None
    child = None
    grandchild = None

    if d["src"] != None:
        try:
            reader = pp.PdfReader(d["src"])
            if "pdf" not in reader.pdf_header.lower():
                raise Exception("Not a PDF file")
        except BaseException as e:
            print(f"Exception {e} was raised.")

    if d["dst"] != None and d["contents"] != None and reader != None:
        with open(d["dst"], "wb") as file:
            try:
                writer = pp.PdfWriter(clone_from=reader)

                # Get lines from contents text file
                with open(d["contents"], "r") as c:
                    lines = [line.strip() for line in c]

                # Iterate over lines, match for patterns and add outline items
                for i in range(0, len(lines)):
                    if isName(lines[i]):
                        if not d["toplevel"] and d["sublevel"]:
                            writer.add_outline_item(title=lines[i],
                                                    page_number=int(lines[i+1]))
                        else:
                            if matchPattern(lines[i], d["toplevel"]):
                                parent = writer.add_outline_item(title=lines[i],
                                                             page_number=int(lines[i+1]))
                            elif matchPattern(lines[i], d["sublevel"]):
                                child = writer.add_outline_item(title=lines[i],
                                                            page_number=int(lines[i+1]),
                                                            parent=parent)
                            elif d["subsublevel"]:
                                if matchPattern(lines[i], d["subsublevel"]):
                                    grandchild = writer.add_outline_item(title=lines[i],
                                                    page_number=int(lines[i+1]),
                                                    parent=child)
                            else:
                                # If it does not match any pattern, add as top level
                                writer.add_outline_item(title=lines[i],
                                                        page_number=int(lines[i+1]))
                else:
                    # When all lines are read, write file
                    writer.write(file)
            except BaseException as e:
                print(f"Exception {e} was raised.")

def generateOutline(src: str, dst: str, contents: str, toplevel_pattern: str | None,
                    sublevel_pattern: str | None, subsublevel_pattern: str | None) -> bool:
    """
    Shitty wrapper for writeTableOfContents

    Copies PDF document at src, creates outline (table of contents) from contents.txt file, then
    writes copied pdf with outline to dst.
    To define a hierarchy, set toplevel_pattern and sublevel_pattern. Sublevel items will then be
    assigned toplevel items as parents. The same mechanism works for subsublevel_pattern.

    contents must be a formatted text file, where page titles are followed by page number on the next line
    Example:
    Chapter V: Compact Families of Meromorphic Functions
    219

    Note that any item that does not match any pattern is automatically a top level item.

    src: path to source pdf file
    dst: path to destination pdf file (remember .pdf extension!)
    contents: formatted text file with contents page of pdf file
    toplevel_pattern: regex pattern for toplevel
    sublevel_pattern: regex pattern for sublevel
    subsublevel_pattern: regex pattern for subsublevel
    """     
    data_dict = {"src": "",
                 "dst": "",
                 "contents": "",
                 "toplevel": None,
                 "sublevel": None,
                 "subsublevel": None}
    if src == "" or dst == "" or contents == "":
        return False
    else:
        data_dict["src"] = os.path.abspath(src)
        data_dict["dst"] = os.path.abspath(dst)
        data_dict["contents"] = os.path.abspath(contents)

    if toplevel_pattern:
        data_dict["toplevel"] = toplevel_pattern
    if sublevel_pattern:
        data_dict["sublevel"] = sublevel_pattern
    if subsublevel_pattern:
        data_dict["subsublevel"] = subsublevel_pattern

    writeTableOfContents(data_dict)
    return True


