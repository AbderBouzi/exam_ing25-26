import os
import glob
import markdown
from xhtml2pdf import pisa
import re

# Directory containing the markdown files
SOURCE_DIR = r'c:\Users\afd\Desktop\exam-ASD-S1-25-26\extracted_code'

def format_c_code(code):
    """
    Standard C formatter. 
    Enforces:
    - Newlines after semicolons (except in for loops).
    - Newlines after '{' and '}'.
    - Correct indentation.
    """
    # 1. Normalize all whitespace to single spaces to clear messy formatting
    code = re.sub(r'\s+', ' ', code)
    
    # 2. Temporary protection for 'for' loops to avoid splitting their semicolons
    # We use a placeholder for semicolons inside parentheses
    def protect_loops(match):
        return match.group(0).replace(';', '<SEMICOLON>')
    
    # Regex for for loops: for (...)
    # Minimal balancing for parentheses (up to 2 levels deep for simplicity or just greedy non-newline)
    # Since we normalized to single line, ".*?" works well.
    code = re.sub(r'for\s*\(.*?\)', protect_loops, code)

    # 3. Add newlines around structural elements
    code = code.replace(';', ';\n')
    code = code.replace('{', '\n{\n')
    code = code.replace('}', '\n}\n')
    
    # 4. Restore protected semicolons in for loops
    code = code.replace('<SEMICOLON>', ';')
    
    # 5. Add newlines for #include
    code = re.sub(r'#\s*include', '\n#include', code)

    # 6. Re-indent line by line
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    indent_size = 4
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Dedent for closing brace
        if line.startswith('}'):
            indent_level = max(0, indent_level - 1)
            
        # Add current indent
        formatted_lines.append(' ' * (indent_level * indent_size) + line)
        
        # Indent for opening brace
        if line.endswith('{') or line == '{':
            indent_level += 1
            
        # Extra spacing: Add a blank line after closing a block (function/if/loop)
        # to separate logical sections "aerated"
        if line.startswith('}'):
            formatted_lines.append('')

    return '\n'.join(formatted_lines)

def process_markdown_code_blocks(text):
    """
    Finds ```c ... ``` blocks and formats the code inside.
    """
    pattern = re.compile(r'```c(.*?)```', re.DOTALL)
    
    def replacer(match):
        code_content = match.group(1)
        formatted_code = format_c_code(code_content)
        return f'```c\n{formatted_code}\n```'
    
    return pattern.sub(replacer, text)

def convert_md_to_pdf(md_file):
    try:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        pdf_file = os.path.join(SOURCE_DIR, f"{base_name}.pdf")
        
        print(f"Converting {base_name}...")

        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Pre-process: Format C code blocks
        text = process_markdown_code_blocks(text)

        # Custom processing to wrap each copy in a page-breaking div
        # Split by lines, identify headers
        lines = text.split('\n')
        sections = []
        current_section = []
        
        # Regex to match "# Copy", "## Copy", etc.
        copy_header_pattern = re.compile(r'^#+\s*Copy', re.IGNORECASE)

        for line in lines:
            # Check for Copy header
            if copy_header_pattern.match(line):
                if current_section:
                    # If we have a previous section, add it ONLY if it's a Copy section
                    # (Discard preamble text that doesn't start with a header if it's before the first copy)
                    # Actually, better logic: split sections, ignore preamble.
                    sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                if current_section: # Only add lines if we are inside a section (skips preamble)
                    current_section.append(line)
        
        if current_section:
            sections.append('\n'.join(current_section))

        # Convert each section to HTML and wrap it
        full_body_content = ""
        for i, sec in enumerate(sections):
            if not sec.strip(): continue
            
            # Extract Copy Number for cleaner display if needed, but MD header is fine.
            sec_html = markdown.markdown(sec, extensions=['fenced_code', 'codehilite'])
            
            # Wrapper div for page break control.
            # We use page-break-after: always for ALL sections to ensure isolation.
            # The last page blank check is handled by xhtml2pdf usually stripping empty last pages, 
            # or we can try to avoid it for the last one.
            # But "1 page = 1 copie" is strict.
            
            style = 'page-break-after: always;'
            if i == len(sections) - 1:
                style = '' # No break after the last one
                
            full_body_content += f'<div class="copy-section" style="{style}">{sec_html}</div>'

        # Add CSS
        full_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: a4;
                    margin: 1cm;
                }}
                body {{ 
                    font-family: Helvetica, sans-serif; 
                    font-size: 8pt; /* Small font to fit content on one page */
                }}
                .copy-section {{
                    display: block;
                    width: 100%;
                }}
                h1 {{ 
                    color: #000;
                    font-size: 12pt;
                    border-bottom: 1px solid #000;
                    margin-top: 0;
                    margin-bottom: 10px;
                    padding-bottom: 5px;
                }}
                pre {{ 
                    background-color: #f8f8f8; 
                    padding: 8px; 
                    border: 1px solid #eee; 
                    white-space: pre-wrap; 
                    word-wrap: break-word; /* Ensure wrapping */
                    font-size: 9pt; /* Slightly clearer code */
                    line-height: 1.4; /* More spaced out */
                    font-family: "Courier New", monospace;
                }}
                p {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            {full_body_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        with open(pdf_file, "wb") as pdf_out:
            pisa_status = pisa.CreatePDF(full_html, dest=pdf_out, encoding='utf-8')

        if pisa_status.err:
            print(f"Error converting {base_name}: {pisa_status.err}")
        else:
            print(f"Successfully created {pdf_file}")

    except Exception as e:
        print(f"Failed to convert {md_file}: {e}")

def main():
    md_files = glob.glob(os.path.join(SOURCE_DIR, "*.md"))
    if not md_files:
        print("No markdown files found in the source directory.")
        return

    print(f"Found {len(md_files)} markdown files.")
    for md_file in md_files:
        convert_md_to_pdf(md_file)
    print("Conversion complete.")

if __name__ == "__main__":
    main()
