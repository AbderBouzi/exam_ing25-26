import os
import glob
import markdown
from xhtml2pdf import pisa
import re

# Directory containing the markdown files
SOURCE_DIR = r'c:\Users\afd\Desktop\exam-ASD-S1-25-26\extracted_code'

def format_c_code(code):
    """
    Extremely robust C formatter for OCR-extracted code.
    Forces newlines and proper IDE-like indentation.
    """
    # 1. Basic cleaning of OCR mess in includes
    code = re.sub(r'#\s*include\s*[<"]\s*([\w\s\.]+)\s*[>"]', r'#include <\1>', code)
    code = code.replace('. h>', '.h>')
    code = code.replace(' .h>', '.h>')
    code = code.replace('< ', '<')
    code = code.replace(' >', '>')
    
    # 2. Add spaces around operators and remove excessive whitespace
    code = re.sub(r'\s+', ' ', code)
    
    # 3. Handle structural line breaks
    # Move includes to their own lines
    code = re.sub(r'(#include\s*<[^>]+>)', r'\1\n', code)
    
    # Braces on new lines (Allman Style)
    code = code.replace('{', '\n{\n')
    code = code.replace('}', '\n}\n')
    
    # Semicolons followed by newline (protect for-loops)
    # Temporary placeholder for semicolons inside parentheses
    def hide_semicolons_in_parens(match):
        return match.group(0).replace(';', '###MARK###')
    
    # Protect content inside (...)
    code = re.sub(r'\([^)]*\)', hide_semicolons_in_parens, code)
    
    # Now split by semicolons
    code = code.replace(';', ';\n')
    
    # Add newlines after if/for/while closing parens if not followed by brace
    # code = re.sub(r'(\)\s*)([^{;\s])', r'\1\n\2', code)
    
    # Restore semicolons
    code = code.replace('###MARK###', ';')
    
    # 4. Final cleaning and Indentation
    raw_lines = code.split('\n')
    indented_lines = []
    level = 0
    
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
            
        # Adjust level for closing brace
        if line.startswith('}'):
            level = max(0, level - 1)
            
        # Add line with indentation
        indented_lines.append('    ' * level + line)
        
        # Adjust level for opening brace
        if line.endswith('{') or line == '{':
            level += 1
            
        # Blank line after a block ends for "aeration"
        if line == '}':
            indented_lines.append('')

    return '\n'.join(indented_lines)

def process_markdown_code_blocks(text):
    """
    Finds ``` ... ``` blocks and formats the code inside.
    Returns (processed_text, dict_of_placeholders)
    """
    placeholders = {}
    pattern = re.compile(r'```(?:c|)\n?(.*?)```', re.DOTALL | re.IGNORECASE)
    
    def replacer(match):
        code_content = match.group(1)
        formatted_code = format_c_code(code_content)
        placeholder = f"ZZZ_CODE_BLOCK_{len(placeholders)}_ZZZ"
        # We manually escape basic HTML in code but keep our formatting
        safe_code = formatted_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        placeholders[placeholder] = f'<pre class="code-block"><code>{safe_code}</code></pre>'
        return f"\n\n{placeholder}\n\n"
    
    processed_text = pattern.sub(replacer, text)
    return processed_text, placeholders

def convert_md_to_pdf(md_file):
    try:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        pdf_file = os.path.join(SOURCE_DIR, f"{base_name}.pdf")
        
        print(f"Converting {base_name}...")

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Protect code blocks and format them
        content, placeholders = process_markdown_code_blocks(content)

        # 2. Split into copies based on headers
        copy_pattern = re.compile(r'^#+\s*Copy.*$', re.MULTILINE | re.IGNORECASE)
        splits = list(copy_pattern.finditer(content))
        
        sections = []
        if not splits:
            sections = [content]
        else:
            for i in range(len(splits)):
                start = splits[i].start()
                end = splits[i+1].start() if i+1 < len(splits) else len(content)
                sections.append(content[start:end])

        # 3. Build HTML Body
        html_body = ""
        for i, sec in enumerate(sections):
            # Convert section to markdown
            sec_html = markdown.markdown(sec, extensions=['fenced_code'])
            
            # Replace placeholders back
            for placeholder, code_html in placeholders.items():
                # We use a pattern to avoid partial matches and handle potential <p> wrapper from markdown
                sec_html = sec_html.replace(f"<p>{placeholder}</p>", code_html)
                sec_html = sec_html.replace(placeholder, code_html)

            style = "page-break-after: always;" if i < len(sections) - 1 else ""
            html_body += f'<div class="section-container" style="{style}">{sec_html}</div>'

        # 4. Final PDF Template with strict CSS
        full_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: a4;
                    margin: 1.5cm;
                }}
                body {{
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 11pt;
                    color: #222;
                    line-height: 1.4;
                }}
                h1, h2, h3 {{
                    color: #000;
                    border-bottom: 2px solid #555;
                    padding-bottom: 5px;
                    margin-top: 0;
                }}
                .section-container {{
                    display: block;
                    width: 100%;
                }}
                pre.code-block {{
                    background-color: #f8f8f8;
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin: 20px 0;
                    font-family: 'Courier New', monospace;
                    font-size: 10pt;
                    white-space: pre; /* CRITICAL: Must be pre to respect \n */
                    color: #000;
                    display: block;
                    width: 95%;
                }}
                code {{
                    font-family: 'Courier New', monospace;
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """

        with open(pdf_file, "wb") as f_out:
            pisa_status = pisa.CreatePDF(full_html, dest=f_out, encoding='utf-8')

        if pisa_status.err:
            print(f"Error converting {base_name}: {pisa_status.err}")
        else:
            print(f"Success: {pdf_file}")

    except Exception as e:
        print(f"Exception for {md_file}: {e}")

def main():
    files = glob.glob(os.path.join(SOURCE_DIR, "*.md"))
    for f in files:
        convert_md_to_pdf(f)

if __name__ == "__main__":
    main()
