"""
Handles all file reading/writing in a consistent and safe way.
Controllers should NOT touch disk operations directly.
"""
import pathlib
from pathlib import Path
import xml.etree.ElementTree as ET
import re 

## I/O operations

def read_file(path: str) -> [bool, str]:
    """
    Reads a file and returns (success, content or error message).
    This avoids exceptions leaking into controllers.
    """
    try:
        content = Path(path).read_text(encoding="utf-8")
        return True, content
    except Exception as e:
        return False, str(e)


def write_file(path: str, data: str, is_xml: bool = True) -> [bool, str]:
    """
    Writes data to a file in UTF-8. Optionally formats XML data before writing.
    Returns (success, message).
    """
    try:
        if "\\n" in data:
            data = data.replace("\\n", "\n")
        if is_xml:
            final_data = pretty_format(data) #adds indentation and new lines
        else:
            final_data = data                #return raw data
        
        with open(path, "w", encoding="utf-8") as file:
            file.write(final_data)           #write to disk (formatted or raw)
        
        message = "File written successfully."
        if is_xml:
            message = "XML file written successfully with formatting."
            
        return True, message
    except OSError as e:
        return False, f"File error: {e}"

