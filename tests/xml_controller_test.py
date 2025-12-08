"""
Tests package for SocialNet Parser.
"""
import sys
import os
# Add the parent directory to sys.path so we can find xml_controller.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.controllers.xml_controller import XMLcontroller  # Assumes your class is in xml_controller.py
import unittest

class TestXMLController(unittest.TestCase):

    def setUp(self):
        """Initialize the controller before each test."""
        self.controller = XMLcontroller()

    def test_basic_formatting_and_indentation(self):
        """Test if simple XML is indented correctly (4 spaces)."""
        raw_xml = "<user><name>Ali</name></user>"
        expected_output = (
            "<user>\n"
            "    <name>Ali</name>\n"
            "</user>"
        )
        self.assertEqual(self.controller.format(raw_xml), expected_output)

    def test_leaf_node_inline(self):
        """Test that short text (< 80 chars) stays on the same line as tags."""
        short_text = "This is short text"
        raw_xml = f"<desc>{short_text}</desc>"
        formatted = self.controller.format(raw_xml)
        
        # Verify it didn't break into multiple lines
        self.assertIn(f"<desc>{short_text}</desc>", formatted)
        self.assertEqual(formatted.count('\n'), 0)

    def test_long_text_wrapping(self):
        """Test that long text (> 80 chars) wraps to new lines."""
        # Create text > 80 chars
        long_text = "A" * 85 
        raw_xml = f"<body>{long_text}</body>"
        
        formatted = self.controller.format(raw_xml)
        
        # Logic Check:
        # 1. Opening tag should be on its own line
        # 2. Text should be on a new line (indented)
        # 3. Closing tag should be on a new line
        lines = formatted.split('\n')
        
        self.assertTrue(len(lines) >= 3, "Long text should result in at least 3 lines")
        self.assertEqual(lines[0], "<body>")
        self.assertTrue(lines[1].startswith("    "), "Wrapped text should be indented")
        self.assertEqual(lines[-1], "</body>")

    def test_minify(self):
        """Test if minification removes all whitespace between tags."""
        formatted_xml = """
        <user>
            <id>1</id>
        </user>
        """
        expected = "<user><id>1</id></user>"
        self.assertEqual(self.controller.minify(formatted_xml), expected)

    def test_attributes_preservation(self):
        """Test that attributes inside tags are preserved correctly."""
        raw_xml = '<user id="101" type="admin"></user>'
        # Format might indent it, but the tag string itself should remain intact
        formatted = self.controller.format(raw_xml)
        self.assertIn('<user id="101" type="admin">', formatted)

    def test_mixed_content_robustness(self):
        """Test how it handles nested structures."""
        raw_xml = "<root><child>Text</child><child>Text2</child></root>"
        formatted = self.controller.format(raw_xml)
        
        expected_fragment = "    <child>Text</child>"
        self.assertIn(expected_fragment, formatted)

if __name__ == '__main__':
    unittest.main()