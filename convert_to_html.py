#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir les corrections Markdown en HTML (imprimable en PDF)
"""

import markdown
from pathlib import Path

def convert_md_to_html(md_file: Path, html_file: Path):
    """Convertit un fichier Markdown en HTML avec style d'impression"""
    try:
        # Lire le contenu Markdown
        md_content = md_file.read_text(encoding='utf-8')
        
        # Convertir Markdown en HTML
        html_body = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        # Template HTML complet avec CSS d'impression
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_file.stem}</title>
    <style>
        @media print {{
            @page {{
                margin: 2cm;
                size: A4;
            }}
            body {{
                margin: 0;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background: white;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            page-break-after: avoid;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
            background-color: #f0f8ff;
            padding: 10px 20px;
            border-radius: 3px;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        em {{
            color: #7f8c8d;
        }}
        
        details {{
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }}
        
        summary {{
            cursor: pointer;
            font-weight: bold;
            color: #495057;
            padding: 5px;
        }}
        
        summary:hover {{
            color: #3498db;
        }}
        
        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        
        .print-button:hover {{
            background-color: #2980b9;
        }}
        
        @media print {{
            .print-button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">🖨️ Imprimer en PDF</button>
    {html_body}
</body>
</html>"""
        
        # Écrire le fichier HTML
        html_file.write_text(full_html, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"Erreur pour {md_file.name}: {e}")
        return False

def main():
    base_dir = Path(r"c:\exam_ing25-26\corrections_par_groupe")
    
    print("\n" + "="*60)
    print("CONVERSION DES CORRECTIONS EN HTML (IMPRIMABLE EN PDF)")
    print("="*60)
    print("\nLes fichiers HTML peuvent être ouverts dans un navigateur")
    print("et imprimés en PDF avec Ctrl+P > Enregistrer en PDF")
    
    # Trouver tous les fichiers .md
    md_files = list(base_dir.glob("**/*.md"))
    
    print(f"\n[INFO] Trouvé {len(md_files)} fichiers Markdown à convertir\n")
    
    success_count = 0
    fail_count = 0
    
    for md_file in md_files:
        html_file = md_file.with_suffix('.html')
        
        relative_path = md_file.relative_to(base_dir)
        print(f"[CONVERSION] {relative_path}...", end=" ")
        
        success = convert_md_to_html(md_file, html_file)
        
        if success:
            print(f"OK")
            success_count += 1
        else:
            print(f"ECHEC")
            fail_count += 1
    
    print("\n" + "="*60)
    print("CONVERSION TERMINEE")
    print("="*60)
    print(f"Succès: {success_count}/{len(md_files)}")
    print(f"Échecs: {fail_count}/{len(md_files)}")
    
    if success_count > 0:
        print("\n[INFO] Pour créer les PDFs:")
        print("1. Ouvrez les fichiers .html dans votre navigateur")
        print("2. Appuyez sur Ctrl+P (ou cliquez sur le bouton 'Imprimer en PDF')")
        print("3. Sélectionnez 'Enregistrer en PDF' comme imprimante")
        print("4. Enregistrez le fichier")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
