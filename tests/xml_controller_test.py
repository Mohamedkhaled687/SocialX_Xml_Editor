"""
Unit tests for the XMLController class.
This test suite covers formatting, indentation, text wrapping, minification, 
and XML consistency/validation.
"""

import unittest
import sys
import os

# Add parent directory to system path to allow imports from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the XMLController class
from src.controllers.xml_controller import XMLController  # type: ignore


class TestXMLController(unittest.TestCase):
    """
    Test suite for XMLController class.
    Tests XML formatting, minification, and consistency/validation.
    """

    def setUp(self):
        """Initialize the controller before each test."""
        self.controller = XMLController()

    # -------------------------
    # Formatting and Indentation
    # -------------------------
    def test_basic_formatting_and_indentation(self):
        """Test simple XML is indented correctly (4 spaces per level)."""
        raw_xml = "<user><name>Ali</name></user>"
        self.controller.xml_string = raw_xml
        formatted = self.controller.format()
        expected_output = (
            "<user>\n"
            "    <name>Ali</name>\n"
            "</user>"
        )
        self.assertEqual(formatted, expected_output)

    def test_leaf_node_inline(self):
        """Test that short text (<80 chars) stays inline with tags."""
        short_text = "This is short text"
        raw_xml = f"<desc>{short_text}</desc>"
        self.controller.xml_string = raw_xml
        formatted = self.controller.format()
        self.assertIn(f"<desc>{short_text}</desc>", formatted)
        self.assertEqual(formatted.count('\n'), 0)

    def test_long_text_wrapping(self):
        """Test that long text (>80 chars) wraps to new lines."""
        long_text = "A" * 85
        raw_xml = f"<body>{long_text}</body>"
        self.controller.xml_string = raw_xml
        formatted = self.controller.format()
        lines = formatted.split('\n')
        self.assertTrue(len(lines) >= 3, "Long text should wrap to multiple lines")
        self.assertEqual(lines[0], "<body>")
        self.assertTrue(lines[1].startswith("    "), "Wrapped text should be indented")
        self.assertEqual(lines[-1], "</body>")

    # -------------------------
    # Minification
    # -------------------------
    def test_minify(self):
        """Test minification removes all whitespace and newlines."""
        formatted_xml = """
        <user>
            <id>1</id>
        </user>
        """
        self.controller.xml_string = formatted_xml
        minified = self.controller.minify()
        expected = "<user><id>1</id></user>"
        self.assertEqual(minified, expected)

    # -------------------------
    # Attributes
    # -------------------------
    def test_attributes_preservation(self):
        """Test that attributes inside tags are preserved correctly."""
        raw_xml = '<user id="101" type="admin"></user>'
        self.controller.xml_string = raw_xml
        formatted = self.controller.format()
        self.assertIn('<user id="101" type="admin">', formatted)

    # -------------------------
    # Mixed Content
    # -------------------------
    def test_mixed_content_robustness(self):
        """Test proper indentation for nested structures with multiple children."""
        raw_xml = "<root><child>Text</child><child>Text2</child></root>"
        self.controller.xml_string = raw_xml
        formatted = self.controller.format()
        expected_fragment = "    <child>Text</child>"
        self.assertIn(expected_fragment, formatted)

    # -------------------------
    # XML Validation / Consistency
    # -------------------------
    def test_validate_empty_xml(self):
        """Test validation on empty XML string."""
        self.controller.xml_string = ""
        result = self.controller.validate()
        self.assertFalse(result['is_valid'])
        self.assertEqual(result['error_count'], 1)
        self.assertEqual(result['errors'][0]['description'], "No XML content to validate")

    def test_validate_correct_xml(self):
        """Test validation on a well-formed XML."""
        xml = "<user><id>1</id><name>Ali</name></user>"
        self.controller.xml_string = xml
        result = self.controller.validate()
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['error_count'], 0)

    def test_validate_unclosed_tag(self):
        """Test validation with an unclosed tag."""
        xml = "<user><id>1</id><name>Ali</name>"
        self.controller.xml_string = xml
        result = self.controller.validate()
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("Unclosed tag" in e['description'] for e in result['errors']))

    def test_validate_mismatched_tags(self):
        """Test validation with mismatched opening and closing tags."""
        xml = "<user><name>Ali</id></user>"
        self.controller.xml_string = xml
        result = self.controller.validate()
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("Mismatched tags" in e['description'] for e in result['errors']))

    def test_validate_duplicate_user_ids(self):
        """Test validation for duplicate user IDs."""
        xml = "<user><id>1</id><name>Ali</name></user><user><id>1</id><name>Omar</name></user>"
        self.controller.xml_string = xml
        result = self.controller.validate()
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("Duplicate user ID" in e['description'] for e in result['errors']))

    def test_validate_invalid_follower_reference(self):
        """Test validation where a follower references a non-existent user ID."""
        xml = (
            "<user><id>1</id><name>Ali</name></user>"
            "<user><id>2</id><name>Omar</name><follower><id>3</id></follower></user>"
        )
        self.controller.xml_string = xml
        result = self.controller.validate()
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("Invalid follower reference" in e['description'] for e in result['errors']))


# Run tests if script is executed directly
if __name__ == '__main__':
    unittest.main()
