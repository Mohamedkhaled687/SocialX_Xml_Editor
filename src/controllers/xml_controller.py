"""
XML Controller - Handles XML parsing, validation, and formatting operations.
It manages the XML state and relies on the utilities package for low-level tasks.
"""

import xml.etree.ElementTree as ET
import re
from ..utilities import file_io
from ..utilities import token_utils


class XMLController:
    """Controller for XML-related operations."""
    
    def __init__(self):
        self.xml_tree = None
        self.xml_data = None
        self.current_file_path = ""
        self.user_record_count = 0
    
    def parse_xml_file(self, file_path):       #assuming the file is already structurally valid
        """
        Parse an XML file and load the data into the controller state.
        
        Returns:
            tuple: (success: bool, message: str, user_count: int)
        """
        try:
            self.xml_tree = ET.parse(file_path)
            self.xml_data = self.xml_tree.getroot()
            self.current_file_path = file_path
            self.user_record_count = len(self.xml_data.findall('.//user'))
            return True, f"File loaded successfully. Found {self.user_record_count} user records.", self.user_record_count
        except ET.ParseError as e:
            return False, f"XML parsing failed: {str(e)}", 0
        except FileNotFoundError:
            return False, f"File not found: {file_path}", 0
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", 0

    def format_xml_file(self, file_path):
        """
        Prettifies (formats) the XML file content and saves it back.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            success, raw_content = file_io.read_file(file_path)         #read content
            if not success:                                             #check if failed
                 return False, f"Failed to read file for formatting: {raw_content}"
                 
            success, message = file_io.write_file(file_path, raw_content, is_xml=True)
            
            if success:                                         
                self.xml_tree = ET.parse(file_path)             #reload the formatted XML
                self.xml_data = self.xml_tree.getroot()         #update internal state to reflect changes
                self.user_record_count = len(self.xml_data.findall('.//user'))
                return True, f"XML file formatted successfully. {message}"
            else:
                return False, f"Failed to save formatted XML: {message}"
                
        except ET.ParseError as e:                      #catch XML parsing errors 
            return False, f"XML parsing failed during formatting check: {str(e)}"
        except Exception as e:                          #catch other errors    
            return False, f"Failed to format XML: {str(e)}"
        
    def minify_xml_file(self, file_path, output_path):
        """
        Minifies the XML file and saves it to a specified output path.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            success, raw_content = file_io.read_file(file_path)         #Read the content
            if not success:
                 return False, f"Failed to read file for minification: {raw_content}"
                 
            minified_xml = file_io.minify_xml(raw_content)              #Minify the content
            
            success, message = file_io.write_file(output_path, minified_xml, is_xml=False)
            
            if success:
                return True, f"XML file minified successfully and saved to {output_path}."
            else:
                return False, f"Failed to save minified XML: {message}"
                
        except Exception as e:
            return False, f"Failed to minify XML: {str(e)}"
        
    def check_well_formedness(self, xml_content: str):
        """
        Check if the XML content is well-formed using a Stack-based approach.
        Only checks for matching opening/closing tags, relying on token_utils.
        Returns:
            tuple: (success: bool, message: str)
        """
        tag_stack = []                                  #initialize empty list (stack)
        tokens = token_utils.tokenize(xml_content)      #tokenize the XML content into tags and text
        
        for token in tokens:
            # Skip non-tag content
            if not token_utils.is_opening_tag(token) and not token_utils.is_closing_tag(token):
                continue                                #skip content

            tag_name = token_utils.extract_tag_name(token)  #extract tag name

            if token_utils.is_opening_tag(token):
                # Ignore self-closing tags (e.g., <br/>) for the stack check if found
                if token.endswith('/>'):
                    continue
                tag_stack.append(tag_name)
            
            elif token_utils.is_closing_tag(token):             #check closing tag
                if not tag_stack:                           #stack empty but found closing tag
                    return False, f"Syntax Error: Closing tag '</{tag_name}>' found with no matching opening tag."
                
                last_open_tag = tag_stack.pop()             #pop the last opening tag from stack
                if last_open_tag != tag_name:               #compare tag names
                    return False, f"Mismatched Tags: Expected closing tag for '<{last_open_tag}>' but found '</{tag_name}>'."
        
        if tag_stack:                                       #check for any unclosed tags
            return False, f"Syntax Error: Found {len(tag_stack)} unclosed tags, including '<{tag_stack[-1]}>'."
        
        return True, "XML is well-formed."

    
    def validate_xml_structure(self, file_path):
        """
        Performs full validation: (1) Well-formedness check (stack) and 
        (2) Basic structural and attribute checks (ET).
        
        Returns:
            tuple: (success: bool, message: str)
        """
        success, content = file_io.read_file(file_path)         #get content
        if not success:
            return False, f"Failed to read file for validation: {content}"
            
        is_well_formed, wf_message = self.check_well_formedness(content)
        if not is_well_formed:
            return False, f"Well-formedness Check Failed: {wf_message}"
        
        try:
            tree = ET.parse(file_path)               #parse XML using ElementTree
            root = tree.getroot()               
            
            # Check for the required root element name
            if root.tag != 'social_network':
                return False, f"Structural Check Failed: Expected root tag 'social_network', but found '{root.tag}'."
            
            # Application-specific checks
            users = root.findall('.//user')         #find all user records
            metadata = root.find('metadata')        #check for metadata section
            user_count = len(users)                 #count user records
            valid_id_count = sum(1 for user in users if user.get('id'))
            
            if user_count == 0:                      #check for at least one user record            
                return False, "Structural Check Failed: No '<user>' records found in the network."
            if valid_id_count != user_count:         #check for valid 'id' attribute
                return False, f"Structural Check Failed: Found {user_count} users, but only {valid_id_count} have a valid 'id' attribute."
            if metadata is None:                     #check for metadata section
                return False, "Structural Check Failed: Missing required 'metadata' section."
            
            # Update controller state upon successful validation
            self.xml_tree = tree
            self.xml_data = root
            self.user_record_count = user_count
            
            return True, f"XML Structure and Well-formedness are Valid. Found {user_count} users."
            
        except ET.ParseError as e:
            return False, f"XML Parsing Error during structural check: {str(e)}"
        except Exception as e:
            return False, f"An unexpected error occurred during structural validation: {str(e)}"