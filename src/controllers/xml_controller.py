"""
XMLController Module
====================
This module provides functionality for XML parsing, formatting, minification,
and validation.

Key Features:
- Parse XML strings into tokens
- Format XML with proper indentation (4 spaces per level)
- Wrap long text content across multiple lines (80 char limit)
- Minify XML by removing all whitespace
- Validate XML structure and semantics

Author: [Your Name]
Date: [Date]
"""

import textwrap
import re
from typing import List, Dict, Set, Tuple


class XMLController:
    """
    Main controller class for parsing, formatting, minifying, and validating
    XML strings.
    
    This class provides methods to:
    1. Parse raw XML into structured tokens
    2. Format XML with intelligent indentation and text wrapping
    3. Minify XML by removing all unnecessary whitespace
    4. Validate XML for structural and semantic errors
    
    Attributes:
        xml_string (str): The XML content to be processed
    """
    
    def __init__(self, xml: str = None):
        """
        Initialize the XMLController with optional XML content.
        
        Args:
            xml (str, optional): Initial XML string to process. Defaults to None.
        
        Example:
            controller = XMLController("<root><child>text</child></root>")
        """
        self.xml_string: str = xml

    # ===================================================================
    # SECTION 1: HELPER METHODS (Setter, Getter, Tokenizer)
    # ===================================================================
    
    def set_xml_string(self, xml_string: str):
        """
        Set or update the XML string to be processed.
        
        Args:
            xml_string (str): The new XML content
            
        Example:
            controller.set_xml_string("<person><name>John</name></person>")
        """
        self.xml_string = xml_string

    def get_xml_string(self) -> str:
        """
        Retrieve the current XML string.
        
        Returns:
            str: The current XML content stored in the controller
            
        Example:
            xml = controller.get_xml_string()
        """
        return self.xml_string
    
    def _get_tokens(self) -> List:
        """
        Parse a raw XML string into a structured list of tokens.
        
        This method breaks down XML into its component parts:
        - Opening tags: <tag>, <tag attr="value">
        - Closing tags: </tag>
        - Text content: the text between tags
        
        Returns:
            List: A list of tokens extracted from the XML
            
        Example:
            Input:  "<user><name>Ali</name></user>"
            Output: ['<user>', '<name>', 'Ali', '</name>', '</user>']
        """
        tokens = []
        i = 0
        length = len(self.xml_string)

        while i < length:
            if self.xml_string[i] == '<':
                j = self.xml_string.find('>', i)
                
                if j == -1: 
                    break
                
                tag = self.xml_string[i:j + 1]
                tokens.append(tag)
                i = j + 1
                
            else:
                j = i
                
                while j < length and self.xml_string[j] != '<':
                    j += 1
                
                raw_text = self.xml_string[i:j]
                
                if not raw_text.strip():
                    i = j
                    continue
                
                tokens.append(raw_text.strip())
                i = j
                
        return tokens

    # ===================================================================
    # SECTION 2: FORMAT METHOD (Main Formatting Logic)
    # ===================================================================
    
    def format(self) -> str:
        """
        Reconstruct and format the XML with proper indentation and text wrapping.
        
        Formatting Rules:
        1. Each nesting level is indented by 4 spaces
        2. Short text (≤80 chars) stays inline: <name>Value</name>
        3. Long text (>80 chars) is wrapped across multiple lines
        4. Wrapped text is indented one level deeper than its tag
        
        Returns:
            str: Beautifully formatted XML string with newlines
        """
        tokens = self._get_tokens()
        formatted = []
        level = 0
        indentation = "    "
        k = 0
        MAX_WIDTH = 80

        while k < len(tokens):
            token = tokens[k]

            if token.startswith('</'):
                level = max(0, level - 1)
                formatted.append((indentation * level) + token)

            elif token.startswith('<') and not token.startswith('</'):
                if (k + 2 < len(tokens) and
                        not tokens[k + 1].startswith('<') and
                        tokens[k + 2].startswith('</')):

                    text_content = tokens[k + 1]
                    clean_text = " ".join(text_content.split())

                    if len(clean_text) > MAX_WIDTH:
                        formatted.append((indentation * level) + tokens[k])
                        wrapper = textwrap.TextWrapper(
                            width=MAX_WIDTH,
                            break_long_words=False
                        )
                        wrapped_lines = wrapper.wrap(clean_text)
                        for line in wrapped_lines:
                            formatted.append((indentation * (level + 1)) + line)
                        formatted.append((indentation * level) + tokens[k + 2])
                    else:
                        line = (indentation * level) + tokens[k] + clean_text + tokens[k + 2]
                        formatted.append(line)

                    k += 2
                else:
                    formatted.append((indentation * level) + token)
                    level += 1
            else:
                formatted.append((indentation * level) + token.strip())

            k += 1

        return "\n".join(formatted)

    # ===================================================================
    # SECTION 3: MINIFY METHOD
    # ===================================================================
    
    def minify(self) -> str:
        """
        Minify the XML by removing all whitespace and newlines.
        
        Returns:
            str: Minified XML string (single line, no spaces)
        """
        tokens = self._get_tokens()
        return "".join(tokens)

    # ===================================================================
    # SECTION 4: VALIDATION METHOD (XML Consistency Checker)
    # ===================================================================
    
    def validate(self) -> Dict:
        """
        Validate the XML for structural and semantic errors.
        
        This method performs comprehensive validation including:
        - Syntax errors (malformed tags)
        - Structure errors (mismatched/unclosed tags)
        - Semantic errors (duplicate IDs, invalid references, empty fields)
        
        Returns:
            Dict: Validation results with structure:
            {
                'is_valid': bool,
                'error_count': int,
                'errors': [
                    {
                        'line': int,
                        'description': str,
                        'type': str  # 'syntax', 'semantic', 'structure'
                    },
                    ...
                ]
            }
            
        Example:
            controller = XMLController("<user><name>Ali</name></user>")
            result = controller.validate()
            if result['is_valid']:
                print("XML is valid!")
            else:
                for error in result['errors']:
                    print(f"Line {error['line']}: {error['description']}")
        """
        if not self.xml_string:
            return {
                'is_valid': False,
                'error_count': 1,
                'errors': [{
                    'line': 0,
                    'description': 'No XML content to validate',
                    'type': 'structure'
                }]
            }
        
        errors = []
        tag_stack: List[Tuple[str, int]] = []
        user_ids: Set[str] = set()
        all_user_ids: Set[str] = set()
        
        # First pass - collect all user IDs
        all_user_ids = self._collect_user_ids()
        
        # Second pass - validate structure and semantics
        lines = self.xml_string.split('\n')
        follower_ids = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            line = line.strip()
            
            if not line:
                continue
            
            # Check for basic XML syntax errors
            if '<' in line and '>' not in line:
                error = {
                    'line': line_num,
                    'description': "Malformed tag: missing closing '>'",
                    'type': 'syntax'
                }
                if show_line_preview: # type: ignore
                    error['line_content'] = original_line.rstrip()
                    pointer_pos = original_line.find('<')
                    error['pointer'] = ' ' * pointer_pos + '^' * (len(line) - pointer_pos)
                errors.append(error)
                continue
            
            if '>' in line and '<' not in line:
                error = {
                    'line': line_num,
                    'description': "Malformed tag: missing opening '<'",
                    'type': 'syntax'
                }
                if show_line_preview: # type: ignore
                    error['line_content'] = original_line.rstrip()
                    pointer_pos = original_line.find('>')
                    error['pointer'] = ' ' * pointer_pos + '^'
                errors.append(error)
                continue
            
            # Process opening tags
            opening_tags = re.findall(r'<([a-zA-Z_][a-zA-Z0-9_]*)[^/>]*>', line)
            for tag in opening_tags:
                # Skip if it's a self-closing or has closing tag on same line
                if not re.search(rf'<{tag}[^/>]*/>|<{tag}[^>]*>.*?</{tag}>', line):
                    tag_stack.append((tag, line_num))
            
            # Process closing tags
            closing_tags = re.findall(r'</([a-zA-Z_][a-zA-Z0-9_]*)>', line)
            for tag in closing_tags:
                if not tag_stack:
                    error = {
                        'line': line_num,
                        'description': f"Closing tag '</{tag}>' without matching opening tag",
                        'type': 'structure'
                    }
                    if show_line_preview: # type: ignore
                        error['line_content'] = original_line.rstrip()
                        pointer_pos = original_line.find(f'</{tag}>')
                        error['pointer'] = ' ' * pointer_pos + '^' * (len(f'</{tag}>'))
                    errors.append(error)
                elif tag_stack[-1][0] != tag:
                    expected = tag_stack[-1][0]
                    error = {
                        'line': line_num,
                        'description': f"Mismatched tags: expected '</{expected}>' but found '</{tag}>'",
                        'type': 'structure'
                    }
                    if show_line_preview: # type: ignore
                        error['line_content'] = original_line.rstrip()
                        pointer_pos = original_line.find(f'</{tag}>')
                        error['pointer'] = ' ' * pointer_pos + '^' * (len(f'</{tag}>'))
                    errors.append(error)
                    tag_stack.pop()
                else:
                    tag_stack.pop()
            
            # Semantic validation - check user IDs
            if '<id>' in line and len(tag_stack) >= 2:
                parent = tag_stack[-1][0] if tag_stack else None
                
                match = re.search(r'<id>(.+?)</id>', line)
                if match:
                    user_id = match.group(1).strip()
                    
                    if not user_id:
                        error = {
                            'line': line_num,
                            'description': "Empty user ID",
                            'type': 'semantic'
                        }
                        if show_line_preview: # type: ignore
                            error['line_content'] = original_line.rstrip()
                            pointer_pos = original_line.find('<id>')
                            error['pointer'] = ' ' * pointer_pos + '^' * len('<id></id>')
                        errors.append(error)
                    elif parent == 'user':
                        # This is a user's main ID
                        if user_id in user_ids:
                            error = {
                                'line': line_num,
                                'description': f"Duplicate user ID '{user_id}'",
                                'type': 'semantic'
                            }
                            if show_line_preview: # type: ignore
                                error['line_content'] = original_line.rstrip()
                                pointer_pos = original_line.find('<id>')
                                error['pointer'] = ' ' * pointer_pos + '^' * len(f'<id>{user_id}</id>')
                            errors.append(error)
                        else:
                            user_ids.add(user_id)
                    elif parent == 'follower':
                        # This is a follower reference
                        follower_ids.append((user_id, line_num, original_line))
            
            # Check for empty required fields
            if '<name></name>' in line or '<name> </name>' in line:
                errors.append({
                    'line': line_num,
                    'description': "Empty user name",
                    'type': 'semantic'
                })
            
            if '<body></body>' in line or '<body> </body>' in line:
                errors.append({
                    'line': line_num,
                    'description': "Empty post body",
                    'type': 'semantic'
                })
        
        # Check for unclosed tags
        if tag_stack:
            for tag, line in tag_stack:
                error = {
                    'line': line,
                    'description': f"Unclosed tag '<{tag}>'",
                    'type': 'structure'
                }
                if show_line_preview: # type: ignore
                    line_content = lines[line - 1] if line <= len(lines) else ""
                    error['line_content'] = line_content.rstrip()
                    pointer_pos = line_content.find(f'<{tag}')
                    if pointer_pos >= 0:
                        end_pos = line_content.find('>', pointer_pos)
                        if end_pos >= 0:
                            error['pointer'] = ' ' * pointer_pos + '^' * (end_pos - pointer_pos + 1)
                        else:
                            error['pointer'] = ' ' * pointer_pos + '^'
                errors.append(error)
        
        # Check follower references
        for item in follower_ids:
            if len(item) == 3:
                follower_id, line_num, original_line = item
            else:
                follower_id, line_num = item
                original_line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            if follower_id not in all_user_ids:
                error = {
                    'line': line_num,
                    'description': f"Invalid follower reference: user ID '{follower_id}' does not exist",
                    'type': 'semantic'
                }
                if show_line_preview: # type: ignore
                    error['line_content'] = original_line.rstrip()
                    pointer_pos = original_line.find('<id>')
                    if pointer_pos >= 0:
                        error['pointer'] = ' ' * pointer_pos + '^' * len(f'<id>{follower_id}</id>')
                    else:
                        error['pointer'] = '^'
                errors.append(error)
        
        # Sort errors by line number
        errors.sort(key=lambda x: x['line'])
        
        return {
            'is_valid': len(errors) == 0,
            'error_count': len(errors),
            'errors': errors
        }
    
    def _collect_user_ids(self) -> Set[str]:
        """
        Helper method: Collect all user IDs from the XML for reference checking.
        
        Returns:
            Set[str]: Set of all user IDs found in the XML
        """
        all_user_ids = set()
        lines = self.xml_string.split('\n')
        in_user = False
        
        for line in lines:
            line = line.strip()
            
            if '<user>' in line:
                in_user = True
            elif '</user>' in line:
                in_user = False
            elif in_user and '<id>' in line:
                match = re.search(r'<id>(.+?)</id>', line)
                if match:
                    all_user_ids.add(match.group(1).strip())
        
        return all_user_ids