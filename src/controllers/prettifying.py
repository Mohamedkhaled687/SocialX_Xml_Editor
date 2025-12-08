class XMLcontroller:
    """
    Main controller class responsible for parsing, formatting (pretty-printing),
    and minifying XML strings manually without external XML parsers.
    """

    # --- 1. HELPER METHOD (Tokenizer) ---
    def _get_tokens(self, xml_string):
        """
        Parses a raw XML string into a structured list of tokens.
        A 'Token' is strictly defined here as either:
        1. A Tag (e.g., <name>, </id>)
        2. Text content between tags.
        """
        tokens = []
        i = 0
        length = len(xml_string)
        
        # Iterate through the string character by character
        while i < length:
            # Case 1: We found the start of a tag
            if xml_string[i] == '<':
                # Find the position of the closing bracket '>'
                j = xml_string.find('>', i)
                if j == -1: break  # Stop if XML is malformed (no closing bracket)
                
                # Extract the tag substring (e.g., "<id>")
                tag = xml_string[i:j+1]
                tokens.append(tag)
                
                # Move the main index 'i' past this tag
                i = j + 1
            
            # Case 2: We are inside text content (between tags)
            else:
                j = i
                # Read forward until we hit the start of the next tag
                while j < length and xml_string[j] != '<':
                    j += 1
                
                # Extract the text segment
                raw_text = xml_string[i:j]
                
                # Validation: If the text is just empty whitespace (newlines/tabs), ignore it.
                # We only want significant text data.
                if not raw_text.strip():
                    i = j
                    continue
                
                tokens.append(raw_text.strip())
                i = j
        return tokens

    # --- 2. FORMAT METHOD (Pretty-Printer) ---
    def format(self, xml_string): 
        """
        Reconstructs the XML string with proper indentation and newlines.
        It handles 'Leaf Nodes' (Tag -> Text -> EndTag) specifically to keep 
        them on a single line, regardless of text length.
        """
        tokens = self._get_tokens(xml_string)
        formatted = []
        level = 0  # depth level for indentation
        indentation = "    " # 4 spaces for indentation
        k = 0
        
        while k < len(tokens):
            token = tokens[k]
            
            # --- Scenario A: Closing Tag (e.g., </user>) ---
            if token.startswith('</'):
                # Decrease indentation level before printing
                # max(0, ...) prevents negative indentation errors
                level = max(0, level - 1)
                formatted.append((indentation * level) + token)
                
            # --- Scenario B: Opening Tag (e.g., <user>) ---
            elif token.startswith('<') and not token.startswith('</'):
                
                # CHECK: Is this a "Leaf Node"?
                # Logic: Is the Next token text? AND is the token after that a Closing tag?
                # Example: <body> ...text... </body>
                if (k + 2 < len(tokens) and 
                    not tokens[k+1].startswith('<') and 
                    tokens[k+2].startswith('</')):
                    
                    # 1. Get the text content from the next token
                    text_content = tokens[k+1]
                    
                    # 2. Flatten the text: 
                    # The .split() removes all existing newlines/tabs, 
                    # and .join(" ") puts it back together as one long line.
                    clean_text = " ".join(text_content.split())
                    
                    # 3. Build the single-line string: Indent + OpenTag + Text + CloseTag
                    line = (indentation * level) + tokens[k] + clean_text + tokens[k+2]
                    formatted.append(line)
                    
                    # Skip the next two tokens (the text and the closing tag) 
                    # because we just handled them manually.
                    k += 2 
                    
                else:
                    # It's a Parent Tag (contains other tags inside).
                    # Print it, then increase indentation for the children.
                    formatted.append((indentation * level) + token)
                    level += 1
            
            # --- Scenario C: Loose Text Content ---
            # Fallback for mixed content scenarios (rare in data-centric XML)
            else:
                lines = token.split('\n')
                aligned_lines = []
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line:
                        aligned_lines.append((indentation * level) + stripped_line)
                formatted.append("\n".join(aligned_lines))
            
            # Move to next token
            k += 1
            
        return "\n".join(formatted)

    # --- 3. MINIFY METHOD ---
    def minify(self, xml_string):
        """
        Removes all formatting (newlines, spaces between tags) to create 
        the smallest valid string representation.
        """
        # Since _get_tokens already strips whitespace around text and ignores
        # whitespace-only nodes, joining them results in a minified string.
        tokens = self._get_tokens(xml_string)
        return "".join(tokens)

# --- Test Section ---
# Defining a complex XML string to test indentation and long-text flattening
input_xml = """<?xml version="1.0" encoding="UTF-8"?>
<users>
<user>
<id>1</id>
<name>Ahmed Ali</name>
<posts>
<post>
<body>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
</body>
<topics>
<topic>
economy
</topic>
<topic>
finance
</topic>
</topics>
</post>
<post>
<body>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
</body>
<topics>
<topic>
solar_energy
</topic>
</topics>
</post>
</posts>
<followers>
<follower>
<id>2</id>
</follower>
<follower>
<id>3</id>
</follower>
</followers>
<followings>
<following>
<id>2</id>
</following>
<following>
<id>3</id>
</following>
</followings>
</user>
<user>
<id>2</id>
<name>Yasser Ahmed</name>
<posts>
<post>
<body>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
</body>
<topics>
<topic>
education
</topic>
</topics>
</post>
</posts>
<followers>
<follower>
<id>1</id>
</follower>
</followers>
<followings>
<following>
<id>1</id>
</following>
</followings>
</user>
<user>
<id>3</id>
<name>Mohamed Sherif</name>
<posts>
<post>
<body>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
</body>
<topics>
<topic>
sports
</topic>
</topics>
</post>
</posts>
<followers>
<follower>
<id>1</id>
</follower>
</followers>
<followings>
<following>
<id>1</id>
</following>
</followings>
</user>
</users>"""

# Instantiate the controller
controller = XMLcontroller()

print("/\/\/\/\ Formatted Output /\/\/\/\/")
print(controller.format(input_xml))

print("\n/\/\/\/\ Minified Output /\/\/\/\/")
print(controller.minify(input_xml))