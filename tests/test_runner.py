#to run type this command python3 tests/test_runner.py

import sys
from pathlib import Path
import os
import re


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT)) 


from src.controllers.xml_controller import XMLController
from src.utilities.file_io import read_file, write_file, pretty_format, minify_xml 

TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_GOOD_FILE = TEST_DATA_DIR / "test_good.xml"
TEST_BAD_FILE = TEST_DATA_DIR / "test_bad.xml"
OUTPUT_MIN_FILE = TEST_DATA_DIR / "output_minified.xml"
OUTPUT_PRETTY_FILE = TEST_DATA_DIR / "output_prettified.xml"

# --- Test Functions --

def test_minify_and_prettify():
    print("--- 1. Testing Minify and Prettify ---")
    
    success, xml_content = read_file(str(TEST_GOOD_FILE))
    if not success:
        print(f"FATAL: Could not read {TEST_GOOD_FILE}. Check path and file existence.")
        return

    # 1. Test Minify (using the utility function)
    minified_xml = minify_xml(xml_content)
    print(f"Original size: {len(xml_content)} | Minified size: {len(minified_xml)}")
    print("Minified (Sample):", minified_xml[:100])
    
    # Save minified output (is_xml=False to prevent re-formatting)
    write_file(str(OUTPUT_MIN_FILE), minified_xml, is_xml=False) 
    print(f"[Result] Minified output saved to {OUTPUT_MIN_FILE}")

    # 2. Test Prettify (using the utility function)
    prettified_xml = pretty_format(minified_xml)
    
    # Save prettified output (is_xml=True to ensure prettify is called)
    write_file(str(OUTPUT_PRETTY_FILE), minified_xml, is_xml=True)
    
    print(f"\n[Result] Prettified size: {len(prettified_xml)}")
    print(f"         Output saved to {OUTPUT_PRETTY_FILE}")
    print("\nPrettified Content (First 5 lines):")
    for line in prettified_xml.split('\n')[:5]:
        print("    ", line)
    print("-" * 50)


def test_validate():
    print("--- 2. Testing Validation Method (XMLController) ---")
    
    controller = XMLController()

    # --- Test 2a: Good XML (Should Pass Structural and Well-formedness) ---
    print("2a. Valid XML (test_good.xml):")
    success, message = controller.validate_xml_structure(str(TEST_GOOD_FILE))
    if success:
        print(f"    SUCCESS: {message}")
    else:
        print(f"    FAILURE: Unexpected validation error: {message}")

    # --- Test 2b: Bad XML (Should Fail due to Structural/Well-formedness Errors) ---
    print("\n2b. Invalid XML (test_bad.xml):")
    success, message = controller.validate_xml_structure(str(TEST_BAD_FILE))
    if success:
        print(f"    FAILURE: Expected errors, but passed.")
    else:
        print(f"    SUCCESS: Error caught: {message}")
    
    print("-" * 50)

def cleanup():
    """Removes generated output files."""
    for f in [OUTPUT_MIN_FILE, OUTPUT_PRETTY_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    test_minify_and_prettify()
    test_validate()
    cleanup()