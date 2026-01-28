#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir automatiquement les HTML en PDF via Chrome/Edge headless
"""

import subprocess
from pathlib import Path
import shutil

def find_chrome_edge():
    """Trouve Chrome ou Edge sur le système"""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    
    return None

def convert_html_to_pdf(html_file: Path, pdf_file: Path, browser_path: str):
    """Convertit HTML en PDF avec Chrome/Edge headless"""
    try:
        cmd = [
            browser_path,
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + str(pdf_file),
            '--no-margins',
            str(html_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if pdf_file.exists():
            return True
        else:
            print(f"  Erreur: PDF non créé - {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  Timeout")
        return False
    except Exception as e:
        print(f"  Erreur: {e}")
        return False

def main():
    base_dir = Path(r"c:\exam_ing25-26\corrections_par_groupe")
    
    print("\n" + "="*60)
    print("CONVERSION AUTOMATIQUE HTML -> PDF")
    print("="*60)
    
    # Trouver le navigateur
    browser_path = find_chrome_edge()
    
    if not browser_path:
        print("\n[ERREUR] Chrome ou Edge non trouvé!")
        print("Veuillez installer Google Chrome ou Microsoft Edge")
        print("\nAlternative: Ouvrez les fichiers .html et imprimez-les manuellement")
        return
    
    print(f"\n[INFO] Utilisation de: {Path(browser_path).name}")
    
    # Trouver tous les fichiers HTML
    html_files = list(base_dir.glob("**/*.html"))
    
    print(f"[INFO] Trouvé {len(html_files)} fichiers HTML à convertir\n")
    
    success_count = 0
    fail_count = 0
    
    for html_file in html_files:
        pdf_file = html_file.with_suffix('.pdf')
        
        relative_path = html_file.relative_to(base_dir)
        print(f"[PDF] {relative_path}...", end=" ")
        
        success = convert_html_to_pdf(html_file, pdf_file, browser_path)
        
        if success:
            print(f"OK ({pdf_file.stat().st_size // 1024} KB)")
            success_count += 1
        else:
            print(f"ECHEC")
            fail_count += 1
    
    print("\n" + "="*60)
    print("CONVERSION TERMINEE")
    print("="*60)
    print(f"Succès: {success_count}/{len(html_files)}")
    print(f"Échecs: {fail_count}/{len(html_files)}")
    print("="*60 + "\n")
    
    if success_count > 0:
        print(f"[INFO] Les PDFs sont dans: {base_dir}")

if __name__ == "__main__":
    main()
