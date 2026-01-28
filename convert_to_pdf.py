#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir les corrections Markdown en PDF
"""

import os
import subprocess
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

def convert_md_to_pdf_weasyprint(md_file: Path, pdf_file: Path):
    """Convertit un fichier Markdown en PDF avec WeasyPrint"""
    try:
        # Lire le contenu Markdown
        md_content = md_file.read_text(encoding='utf-8')
        
        # Convertir Markdown en HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )
        
        # Ajouter un style CSS basique
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
        
        # Convertir HTML en PDF
        HTML(string=full_html).write_pdf(pdf_file)
        return True
        
    except Exception as e:
        print(f"Erreur avec WeasyPrint pour {md_file.name}: {e}")
        return False

def convert_md_to_pdf_pandoc(md_file: Path, pdf_file: Path):
    """Convertit un fichier Markdown en PDF avec Pandoc"""
    try:
        cmd = [
            'pandoc',
            str(md_file),
            '-o', str(pdf_file),
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=2cm',
            '-V', 'fontsize=11pt'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Erreur Pandoc: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Pandoc n'est pas installé")
        return False
    except Exception as e:
        print(f"Erreur avec Pandoc pour {md_file.name}: {e}")
        return False

def main():
    base_dir = Path(r"c:\exam_ing25-26\corrections_par_groupe")
    
    print("\n" + "="*60)
    print("CONVERSION DES CORRECTIONS EN PDF")
    print("="*60)
    
    # Vérifier si WeasyPrint est disponible
    try:
        import weasyprint
        use_weasyprint = True
        print("\n[INFO] Utilisation de WeasyPrint pour la conversion")
    except ImportError:
        use_weasyprint = False
        print("\n[INFO] WeasyPrint non disponible, tentative avec Pandoc")
    
    # Trouver tous les fichiers .md
    md_files = list(base_dir.glob("**/*.md"))
    
    print(f"\n[INFO] Trouvé {len(md_files)} fichiers Markdown à convertir")
    
    success_count = 0
    fail_count = 0
    
    for md_file in md_files:
        pdf_file = md_file.with_suffix('.pdf')
        
        print(f"\n[CONVERSION] {md_file.relative_to(base_dir)}...", end=" ")
        
        # Essayer WeasyPrint d'abord, puis Pandoc
        if use_weasyprint:
            success = convert_md_to_pdf_weasyprint(md_file, pdf_file)
        else:
            success = convert_md_to_pdf_pandoc(md_file, pdf_file)
        
        if success:
            print(f"OK -> {pdf_file.name}")
            success_count += 1
        else:
            print(f"ECHEC")
            fail_count += 1
    
    print("\n" + "="*60)
    print("CONVERSION TERMINEE")
    print("="*60)
    print(f"Succès: {success_count}/{len(md_files)}")
    print(f"Échecs: {fail_count}/{len(md_files)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
