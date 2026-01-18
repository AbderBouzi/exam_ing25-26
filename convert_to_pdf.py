import os
import glob
import markdown
from xhtml2pdf import pisa

# Directory containing the markdown files
SOURCE_DIR = r'c:\Users\afd\Desktop\exam-ASD-S1-25-26\extracted_code'

def convert_md_to_pdf(md_file):
    try:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        pdf_file = os.path.join(SOURCE_DIR, f"{base_name}.pdf")
        
        print(f"Converting {base_name}...")

        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])

        # Add some basic styling
        full_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, sans-serif; font-size: 10pt; }}
                pre {{ background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc; }}
                code {{ font-family: Courier New, monospace; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; border-bottom: 1px solid #eee; }}
            </style>
        </head>
        <body>
            {html_content}
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
