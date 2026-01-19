
import os
import markdown
from xhtml2pdf import pisa
import re
import glob

# Directory configuration
SOURCE_DIR = r'c:\Users\afd\Desktop\exam-ASD-S1-25-26\extracted_code\corrections'
OUTPUT_DIR = r'c:\Users\afd\Desktop\exam-ASD-S1-25-26\extracted_code\corrections\split'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def convert_md_to_split_pdf(source_md):
    try:
        base_name = os.path.splitext(os.path.basename(source_md))[0]
        print(f"Splitting corrections for {base_name}...")
        
        with open(source_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split content by header "## COPY NUMBER: X"
        # Regex to find headers and capture copy number
        copy_pattern = re.compile(r'^(#+\s*COPY NUMBER:\s*(\d+).*$)', re.MULTILINE | re.IGNORECASE)
        splits = list(copy_pattern.finditer(content))
        
        sections = []
        if not splits:
            # Maybe just one copy? Or header format different?
            pass
        else:
            for i in range(len(splits)):
                start = splits[i].start()
                end = splits[i+1].start() if i+1 < len(splits) else len(content)
                header_match = splits[i]
                copy_num = header_match.group(2)
                section_text = content[start:end]
                sections.append({'copy_num': copy_num, 'text': section_text})

        for sec in sections:
            html = markdown.markdown(sec['text'], extensions=['tables'])
            
            # Add basic styling
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Helvetica, sans-serif; font-size: 10pt; }}
                    h1 {{ color: #2c3e50; }}
                    h2 {{ color: #e74c3c; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 20px; }}
                    h3 {{ color: #3498db; margin-top: 15px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
                </style>
            </head>
            <body>
                {html}
            </body>
            </html>
            """
            
            output_name = f"{base_name}_Copy_{sec['copy_num']}.pdf"
            output_path = os.path.join(OUTPUT_DIR, output_name)
            
            with open(output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                
            if pisa_status.err:
                print(f"Error converting {output_name}")
            
    except Exception as e:
        print(f"Failed to convert {source_md}: {str(e)}")

# Files to process
files = glob.glob(os.path.join(SOURCE_DIR, "Corr_*.md"))

for f in files:
    convert_md_to_split_pdf(f)
