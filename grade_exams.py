#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction encourageante pour étudiants débutants
Extrait les anciennes notes et génère de nouvelles corrections plus bienveillantes
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple

class EncouragingGrader:
    """Correcteur encourageant pour étudiants débutants en C"""
    
    def __init__(self):
        self.base_dir = Path(r"c:\exam_ing25-26")
        self.extracted_code_dir = self.base_dir / "extracted_code"
        self.old_corrections_dir = self.extracted_code_dir / "corrections"
        self.new_corrections_dir = self.base_dir / "corrections_par_groupe"
        
    def extract_old_grades(self, correction_file: Path) -> Dict[int, Dict]:
        """Extrait les anciennes notes d'un fichier de correction"""
        if not correction_file.exists():
            return {}
        
        content = correction_file.read_text(encoding='utf-8')
        old_grades = {}
        
        # Pattern pour extraire les copies
        copy_pattern = r'## COPY NUMBER: (\d+)(.*?)(?=## COPY NUMBER:|\Z)'
        copies = re.findall(copy_pattern, content, re.DOTALL)
        
        for copy_num_str, copy_content in copies:
            copy_num = int(copy_num_str)
            
            # Extraire la note finale
            note_match = re.search(r'\*\*NOTE FINALE\s*:\s*(\d+)\s*/\s*20\*\*', copy_content)
            if note_match:
                old_note = int(note_match.group(1))
                
                # Extraire les détails de notation
                details = {}
                detail_pattern = r'\|\s*([^|]+?)\s*\|\s*(\d+)\s*/\s*(\d+)\s*\|'
                for match in re.finditer(detail_pattern, copy_content):
                    criterion = match.group(1).strip()
                    points = int(match.group(2))
                    max_points = int(match.group(3))
                    details[criterion] = (points, max_points)
                
                # Extraire le feedback
                feedback_match = re.search(r'### Feedback :(.*?)(?=---|## COPY|\Z)', copy_content, re.DOTALL)
                feedback = feedback_match.group(1).strip() if feedback_match else ""
                
                old_grades[copy_num] = {
                    'note': old_note,
                    'details': details,
                    'feedback': feedback
                }
        
        return old_grades
    
    def grade_with_encouragement(self, code: str, old_grade: Dict = None) -> Dict:
        """
        Applique une correction encourageante
        Critères adaptés pour débutants:
        - Lecture des données (0-4 pts): +1 pt par rapport à l'ancien barème
        - Initialisation (0-3 pts): même barème mais plus tolérant
        - Structure de boucle (0-5 pts): +1 pt
        - Logique présence/absence (0-5 pts): +1 pt
        - Compteurs (0-2 pts): -1 pt (moins strict)
        - Affichages (0-1 pt): -1 pt (simplifié)
        """
        
        new_grade = {
            'lecture_donnees': 0,  # max 4
            'initialisation': 0,    # max 3
            'structure_boucle': 0,  # max 5
            'logique_presence': 0,  # max 5
            'compteurs': 0,         # max 2
            'affichages': 0,        # max 1
            'points_forts': [],
            'points_ameliorer': [],
            'encouragement': ""
        }
        
        code_lower = code.lower()
        
        # 1. Lecture des données (0-4 pts) - Encourageant
        if 'scanf' in code_lower and '&n' in code_lower:
            new_grade['lecture_donnees'] += 2
            new_grade['points_forts'].append("Lecture de N avec scanf")
        if 'scanf' in code_lower and '&a' in code_lower:
            new_grade['lecture_donnees'] += 1
            new_grade['points_forts'].append("Lecture de A avec scanf")
        if 'scanf' in code_lower and '&s' in code_lower:
            new_grade['lecture_donnees'] += 1
            new_grade['points_forts'].append("Lecture de S avec scanf")
        
        # Bonus si printf avant scanf (bonne pratique)
        if 'printf' in code_lower and 'scanf' in code_lower:
            try:
                if code_lower.index('printf') < code_lower.index('scanf'):
                    if new_grade['lecture_donnees'] < 4:
                        new_grade['lecture_donnees'] = min(4, new_grade['lecture_donnees'] + 1)
                        new_grade['points_forts'].append("Messages utilisateur avant saisie")
            except ValueError:
                pass  # Si scanf ou printf non trouvé, on ignore
        
        # 2. Initialisation (0-3 pts) - Tolérant
        has_declarations = bool(re.search(r'int\s+\w+', code))
        if has_declarations:
            new_grade['initialisation'] += 2
            new_grade['points_forts'].append("Déclaration des variables")
        
        # Chercher initialisation explicite
        if re.search(r'=\s*0', code):
            new_grade['initialisation'] += 1
            new_grade['points_forts'].append("Initialisation de variables à 0")
        elif has_declarations:
            # Bonus partiel même sans initialisation explicite
            new_grade['initialisation'] = min(3, new_grade['initialisation'] + 1)
        
        # 3. Structure de boucle (0-5 pts) - Encourageant
        has_for = 'for' in code_lower
        has_while = 'while' in code_lower
        
        if has_for or has_while:
            new_grade['structure_boucle'] += 2
            loop_type = "for" if has_for else "while"
            new_grade['points_forts'].append(f"Utilisation d'une boucle {loop_type}")
            
            # Vérifier condition de boucle
            if has_for and re.search(r'i\s*<=?\s*n', code_lower):
                new_grade['structure_boucle'] += 2
                new_grade['points_forts'].append("Condition de boucle sur N")
            elif has_while and re.search(r'i\s*<=?\s*n', code_lower):
                new_grade['structure_boucle'] += 2
                new_grade['points_forts'].append("Condition de boucle sur N")
            else:
                new_grade['structure_boucle'] += 1
                new_grade['points_ameliorer'].append("Revoir la condition d'arrêt de la boucle")
            
            # Bonus pour tentative d'arrêt sur seuil
            if 's' in code_lower and ('&&' in code or '||' in code):
                new_grade['structure_boucle'] = min(5, new_grade['structure_boucle'] + 1)
                new_grade['points_forts'].append("Tentative de gestion du seuil d'absence")
        else:
            new_grade['points_ameliorer'].append("Ajouter une boucle pour traiter N étudiants")
        
        # 4. Logique présence/absence (0-5 pts) - Encourageant
        has_comparison = bool(re.search(r'x\s*<?=?\s*a|a\s*>?=?\s*x', code_lower))
        if has_comparison:
            new_grade['logique_presence'] += 3
            new_grade['points_forts'].append("Comparaison X < A pour déterminer l'absence")
            
            # Vérifier if/else
            if 'if' in code_lower:
                new_grade['logique_presence'] += 1
                if 'else' in code_lower:
                    new_grade['logique_presence'] += 1
                    new_grade['points_forts'].append("Structure if/else pour présence/absence")
        else:
            if 'if' in code_lower:
                new_grade['logique_presence'] += 2
                new_grade['points_forts'].append("Utilisation de structure conditionnelle")
                new_grade['points_ameliorer'].append("Comparer X avec A pour déterminer l'absence")
        
        # 5. Compteurs (0-2 pts) - Simplifié
        has_increment = bool(re.search(r'\+\+|--|\+=|-=', code))
        if has_increment:
            new_grade['compteurs'] += 1
            new_grade['points_forts'].append("Utilisation d'incrémentation")
            
            # Vérifier plusieurs compteurs
            if code.count('++') >= 2 or code.count('+=') >= 2:
                new_grade['compteurs'] += 1
                new_grade['points_forts'].append("Gestion de plusieurs compteurs")
        else:
            new_grade['points_ameliorer'].append("Utiliser des compteurs pour présents/absents")
        
        # 6. Affichages (0-1 pt) - Simplifié
        printf_count = code_lower.count('printf')
        if printf_count >= 3:
            new_grade['affichages'] += 1
            new_grade['points_forts'].append("Affichages multiples")
        elif printf_count >= 1:
            new_grade['affichages'] += 0.5  # Demi-point
            new_grade['points_ameliorer'].append("Ajouter plus d'affichages pour suivre l'évolution")
        
        # Arrondir affichages
        new_grade['affichages'] = int(round(new_grade['affichages']))
        
        # Calculer note totale
        total = sum([
            new_grade['lecture_donnees'],
            new_grade['initialisation'],
            new_grade['structure_boucle'],
            new_grade['logique_presence'],
            new_grade['compteurs'],
            new_grade['affichages']
        ])
        
        new_grade['total'] = total
        
        # Générer encouragement personnalisé
        new_grade['encouragement'] = self.generate_encouragement(total, new_grade['points_forts'])
        
        return new_grade
    
    def generate_encouragement(self, note: int, points_forts: List[str]) -> str:
        """Génère un message d'encouragement personnalisé"""
        if note >= 18:
            return "🌟 Excellent travail ! Vous maîtrisez très bien les concepts de base de la programmation en C. Continuez comme ça !"
        elif note >= 15:
            return "👏 Très bon travail ! Vous avez bien compris les concepts principaux. Quelques petits ajustements et ce sera parfait !"
        elif note >= 12:
            return "✅ Bon travail ! Vous êtes sur la bonne voie. Continuez à pratiquer les boucles et les conditions."
        elif note >= 9:
            return "💪 Vous avez compris plusieurs concepts importants. Avec un peu plus de pratique sur les boucles et les compteurs, vous allez progresser rapidement !"
        elif note >= 6:
            return "🌱 Vous avez fait des efforts et montré que vous comprenez certains concepts de base. Concentrez-vous sur la structure des boucles et la lecture des données. Vous pouvez y arriver !"
        else:
            return "📚 C'est un début ! La programmation demande de la pratique. Revoyez les exemples de cours sur les boucles et les conditions. N'hésitez pas à demander de l'aide à votre enseignant."
    
    def format_correction(self, copy_num: int, code: str, old_data: Dict, new_grade: Dict) -> str:
        """Formate une correction complète avec comparaison"""
        
        old_note = old_data.get('note', 0) if old_data else 0
        new_note = new_grade['total']
        difference = new_note - old_note
        diff_sign = "+" if difference >= 0 else ""
        
        correction = f"""# Correction Encourageante - Copie N°{copy_num}

## 📊 Comparaison des Notes

| Ancienne Note | Nouvelle Note | Différence |
|:-------------:|:-------------:|:----------:|
| **{old_note}/20** | **{new_note}/20** | **{diff_sign}{difference}** |

> **Note**: La nouvelle correction adopte une approche plus encourageante pour les étudiants débutants, en valorisant l'effort et la compréhension des concepts même si l'implémentation n'est pas parfaite.

---

## ✅ Points Forts

"""
        
        if new_grade['points_forts']:
            for point in new_grade['points_forts']:
                correction += f"- ✓ {point}\n"
        else:
            correction += "- Vous avez rendu une copie, c'est déjà un premier pas !\n"
        
        correction += f"""
---

## 📝 Code Soumis

```c
{code}
```

---

## 🔍 Analyse Détaillée

### 📥 Lecture des données ({new_grade['lecture_donnees']}/4 pts)
"""
        
        if old_data and 'details' in old_data:
            old_lecture = old_data['details'].get('Lecture N, A, S', (0, 3))[0]
            correction += f"*Ancienne note: {old_lecture}/3*\n\n"
        
        if new_grade['lecture_donnees'] >= 3:
            correction += "Très bien ! Vous avez correctement lu les données d'entrée avec `scanf`. "
        elif new_grade['lecture_donnees'] >= 2:
            correction += "Bon début ! Vous avez lu certaines données. Pensez à lire N, A et S au début du programme. "
        else:
            correction += "Il faut lire les trois valeurs N, A et S au début avec `scanf(\"%d\", &variable)`. "
        
        correction += f"""

### 🔧 Initialisation des variables ({new_grade['initialisation']}/3 pts)
"""
        
        if old_data and 'details' in old_data:
            old_init = old_data['details'].get('Initalisation', (0, 3))[0]
            correction += f"*Ancienne note: {old_init}/3*\n\n"
        
        if new_grade['initialisation'] >= 2:
            correction += "Bien ! Vous avez déclaré vos variables. "
            if new_grade['initialisation'] == 3:
                correction += "Et vous les avez même initialisées à 0, c'est une excellente pratique ! "
        else:
            correction += "N'oubliez pas de déclarer vos variables avec `int` et de les initialiser à 0. "
        
        correction += f"""

### 🔄 Structure de boucle ({new_grade['structure_boucle']}/5 pts)
"""
        
        if old_data and 'details' in old_data:
            old_boucle = old_data['details'].get('Condition boucle', (0, 4))[0]
            correction += f"*Ancienne note: {old_boucle}/4*\n\n"
        
        if new_grade['structure_boucle'] >= 4:
            correction += "Excellent ! Vous avez bien utilisé une boucle pour traiter les N étudiants. "
        elif new_grade['structure_boucle'] >= 2:
            correction += "Vous avez utilisé une boucle, c'est bien ! Vérifiez que la condition d'arrêt est correcte (i <= N). "
        else:
            correction += "Il faut utiliser une boucle `for` ou `while` pour traiter chaque étudiant. Exemple: `for(i=1; i<=N; i++)` "
        
        correction += f"""

### 🎯 Logique présence/absence ({new_grade['logique_presence']}/5 pts)
"""
        
        if old_data and 'details' in old_data:
            old_logique = old_data['details'].get('Logique prés./abs.', (0, 4))[0]
            correction += f"*Ancienne note: {old_logique}/4*\n\n"
        
        if new_grade['logique_presence'] >= 4:
            correction += "Parfait ! Vous avez bien compris la logique : si X < A, l'étudiant est absent, sinon il est présent. "
        elif new_grade['logique_presence'] >= 2:
            correction += "Vous avez utilisé des conditions, c'est bien ! Pensez à comparer X (séances suivies) avec A (minimum requis). "
        else:
            correction += "Il faut comparer le nombre de séances X avec le minimum A : `if (X < A)` alors absent, `else` présent. "
        
        correction += f"""

### 🔢 Gestion des compteurs ({new_grade['compteurs']}/2 pts)
"""
        
        if old_data and 'details' in old_data:
            old_compteurs = old_data['details'].get('Compteurs', (0, 3))[0]
            correction += f"*Ancienne note: {old_compteurs}/3*\n\n"
        
        if new_grade['compteurs'] >= 2:
            correction += "Très bien ! Vous avez utilisé des compteurs pour suivre les présents et absents. "
        elif new_grade['compteurs'] >= 1:
            correction += "Vous avez commencé à utiliser des compteurs. Pensez à en avoir un pour les présents et un pour les absents. "
        else:
            correction += "Utilisez des compteurs (ex: `presents++` et `absents++`) pour compter les étudiants. "
        
        correction += f"""

### 📺 Affichages ({new_grade['affichages']}/1 pt)
"""
        
        if old_data and 'details' in old_data:
            old_affichages = old_data['details'].get('Affichages inter.', (0, 2))[0]
            old_final = old_data['details'].get('Affichage final', (0, 1))[0]
            correction += f"*Ancienne note: {old_affichages + old_final}/3*\n\n"
        
        if new_grade['affichages'] >= 1:
            correction += "Bien ! Vous avez pensé à afficher des résultats. "
        else:
            correction += "N'oubliez pas d'afficher les résultats avec `printf`. "
        
        correction += """

---

## 💡 Suggestions d'Amélioration

"""
        
        if new_grade['points_ameliorer']:
            for i, point in enumerate(new_grade['points_ameliorer'], 1):
                correction += f"{i}. {point}\n"
        else:
            correction += "Continuez à pratiquer et à consolider vos acquis !\n"
        
        correction += f"""

---

## 🌟 Message d'Encouragement

{new_grade['encouragement']}

---

## 📋 Détails de l'Ancienne Correction

<details>
<summary>Cliquez pour voir l'analyse précédente (correction stricte)</summary>

"""
        
        if old_data and 'feedback' in old_data:
            correction += old_data['feedback']
        else:
            correction += "*Pas de correction précédente disponible*"
        
        correction += """

</details>

---

*Correction réalisée avec une approche encourageante pour étudiants débutants*
"""
        
        return correction
    
    def process_pdf_group(self, pdf_name: str):
        """Traite un groupe PDF complet"""
        
        print(f"\n{'='*60}")
        print(f"Traitement du groupe: {pdf_name}")
        print(f"{'='*60}")
        
        # Chemins des fichiers
        code_file = self.extracted_code_dir / f"code_{pdf_name}.md"
        old_correction_file = self.old_corrections_dir / f"Corr_{pdf_name}.md"
        
        if not code_file.exists():
            print(f"[ERREUR] Fichier de code non trouvé: {code_file}")
            return
        
        # Créer le répertoire de sortie
        output_dir = self.new_corrections_dir / f"groupe_{pdf_name}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extraire les anciennes notes
        print(f"[INFO] Extraction des anciennes notes...")
        old_grades = self.extract_old_grades(old_correction_file)
        print(f"   Trouvé {len(old_grades)} anciennes corrections")
        
        # Lire le fichier de code
        content = code_file.read_text(encoding='utf-8')
        
        # Extraire les copies
        # Essayer d'abord avec ## Copy (format standard)
        copy_pattern = r'## Copy (\d+)\s*```c\s*(.*?)\s*```'
        copies = re.findall(copy_pattern, content, re.DOTALL | re.IGNORECASE)
        
        # Si aucune copie trouvée, essayer avec # Copy (format alternatif)
        if not copies:
            copy_pattern = r'# Copy (\d+)\s*```c\s*(.*?)\s*```'
            copies = re.findall(copy_pattern, content, re.DOTALL | re.IGNORECASE)
        
        print(f"[INFO] Trouvé {len(copies)} copies à corriger")
        
        # Générer les corrections
        all_corrections = []
        stats = {
            'total': len(copies),
            'old_avg': 0,
            'new_avg': 0,
            'improvements': 0
        }
        
        for copy_num_str, code in copies:
            copy_num = int(copy_num_str)
            print(f"   Correction copie #{copy_num}...", end=" ")
            
            old_data = old_grades.get(copy_num, {})
            new_grade = self.grade_with_encouragement(code, old_data)
            
            correction = self.format_correction(copy_num, code, old_data, new_grade)
            all_corrections.append(correction)
            
            # Stats
            old_note = old_data.get('note', 0)
            new_note = new_grade['total']
            stats['old_avg'] += old_note
            stats['new_avg'] += new_note
            if new_note > old_note:
                stats['improvements'] += 1
            
            print(f"Ancienne: {old_note}/20 -> Nouvelle: {new_note}/20")
        
        # Calculer moyennes
        if stats['total'] > 0:
            stats['old_avg'] = stats['old_avg'] / stats['total']
            stats['new_avg'] = stats['new_avg'] / stats['total']
        
        # Sauvegarder les corrections
        corrections_file = output_dir / "corrections.md"
        full_content = "\n\n---\n\n".join(all_corrections)
        
        # Ajouter un en-tête
        header = f"""# Corrections Encourageantes - {pdf_name}

**Nombre de copies**: {stats['total']}
**Moyenne ancienne correction**: {stats['old_avg']:.2f}/20
**Moyenne nouvelle correction**: {stats['new_avg']:.2f}/20
**Différence moyenne**: {stats['new_avg'] - stats['old_avg']:+.2f}
**Copies améliorées**: {stats['improvements']}/{stats['total']}

---

"""
        
        corrections_file.write_text(header + full_content, encoding='utf-8')
        print(f"\n[OK] Corrections sauvegardées: {corrections_file}")
        
        # Sauvegarder les statistiques
        stats_file = output_dir / "statistiques.md"
        
        # Éviter division par zéro
        improvement_pct = (stats['improvements']/stats['total']*100) if stats['total'] > 0 else 0
        
        stats_content = f"""# Statistiques - {pdf_name}

## 📊 Vue d'ensemble

- **Nombre total de copies**: {stats['total']}
- **Moyenne ancienne correction**: {stats['old_avg']:.2f}/20
- **Moyenne nouvelle correction**: {stats['new_avg']:.2f}/20
- **Différence moyenne**: {stats['new_avg'] - stats['old_avg']:+.2f} points
- **Copies avec amélioration**: {stats['improvements']} ({improvement_pct:.1f}%)

## 📈 Analyse

La nouvelle approche encourageante a permis d'augmenter la moyenne de **{stats['new_avg'] - stats['old_avg']:.2f} points** en moyenne.

Cela reflète une évaluation plus adaptée au niveau débutant des étudiants, valorisant:
- L'effort et la compréhension des concepts
- Les tentatives même incomplètes
- La logique algorithmique même avec des erreurs de syntaxe

## 🎯 Recommandations

Les étudiants doivent continuer à travailler sur:
1. La structure des boucles (for/while)
2. L'initialisation des variables
3. La gestion des compteurs
4. La lecture des données avec scanf

"""
        
        stats_file.write_text(stats_content, encoding='utf-8')
        print(f"[OK] Statistiques sauvegardées: {stats_file}")
        
        return stats
    
    def process_all_groups(self):
        """Traite tous les groupes PDF"""
        
        pdf_groups = [
            "doc20260115201344",
            "doc20260115220910",
            "doc20260115221134",
            "doc20260115221404",
            "doc20260115221630",
            "doc20260115222057",
            "doc20260115222309",
            "doc20260115222526",
            "doc20260115223319",
            "doc20260115223525",
            "doc20260115223647"
        ]
        
        print("\n" + "="*60)
        print("CORRECTION ENCOURAGEANTE DES EXAMENS")
        print("="*60)
        
        all_stats = []
        
        for pdf_name in pdf_groups:
            stats = self.process_pdf_group(pdf_name)
            if stats:
                all_stats.append((pdf_name, stats))
        
        # Rapport global
        self.generate_global_report(all_stats)
    
    def generate_global_report(self, all_stats: List[Tuple[str, Dict]]):
        """Génère un rapport global de toutes les corrections"""
        
        total_copies = sum(s['total'] for _, s in all_stats)
        total_old = sum(s['old_avg'] * s['total'] for _, s in all_stats)
        total_new = sum(s['new_avg'] * s['total'] for _, s in all_stats)
        total_improvements = sum(s['improvements'] for _, s in all_stats)
        
        global_old_avg = total_old / total_copies if total_copies > 0 else 0
        global_new_avg = total_new / total_copies if total_copies > 0 else 0
        
        report = f"""# 📊 Rapport Global des Corrections

## Vue d'ensemble

- **Nombre total de copies corrigées**: {total_copies}
- **Nombre de groupes PDF**: {len(all_stats)}
- **Moyenne générale (ancienne correction)**: {global_old_avg:.2f}/20
- **Moyenne générale (nouvelle correction)**: {global_new_avg:.2f}/20
- **Amélioration moyenne**: {global_new_avg - global_old_avg:+.2f} points
- **Copies avec amélioration de note**: {total_improvements}/{total_copies} ({total_improvements/total_copies*100:.1f}%)

---

## 📈 Détails par groupe

| Groupe | Copies | Anc. Moy. | Nouv. Moy. | Diff. | Améliorées |
|:-------|:------:|:---------:|:----------:|:-----:|:----------:|
"""
        
        for pdf_name, stats in all_stats:
            report += f"| {pdf_name} | {stats['total']} | {stats['old_avg']:.2f} | {stats['new_avg']:.2f} | {stats['new_avg']-stats['old_avg']:+.2f} | {stats['improvements']}/{stats['total']} |\n"
        
        report += f"""

---

## 🎯 Philosophie de la Correction Encourageante

Cette nouvelle approche de correction vise à:

### ✅ Valoriser l'effort
- Reconnaître les tentatives même incomplètes
- Encourager la compréhension conceptuelle
- Récompenser la logique algorithmique

### 📚 Adapter au niveau débutant
- Être plus tolérant sur les erreurs de syntaxe
- Valoriser les bonnes pratiques (messages printf, initialisation)
- Donner du crédit partiel généreusement

### 💪 Motiver les étudiants
- Messages personnalisés et encourageants
- Focus sur les points forts avant les améliorations
- Suggestions constructives et spécifiques

---

## 📋 Comparaison des Barèmes

### Ancien barème (strict)
- Lecture N, A, S: 3 pts
- Initialisation: 3 pts
- Condition boucle: 4 pts
- Logique présence/absence: 4 pts
- Compteurs: 3 pts
- Affichages intermédiaires: 2 pts
- Affichage final: 1 pt
**Total: 20 pts**

### Nouveau barème (encourageant)
- Lecture des données: 4 pts (+1)
- Initialisation: 3 pts (=)
- Structure de boucle: 5 pts (+1)
- Logique présence/absence: 5 pts (+1)
- Compteurs: 2 pts (-1, simplifié)
- Affichages: 1 pt (-1, simplifié)
**Total: 20 pts**

---

## 🌟 Impact

L'approche encourageante a permis:
- Une augmentation moyenne de **{global_new_avg - global_old_avg:.2f} points**
- **{total_improvements/total_copies*100:.1f}%** des étudiants ont vu leur note s'améliorer
- Une meilleure reconnaissance de l'effort et de la compréhension

Cette approche maintient des standards académiques tout en étant plus adaptée au niveau débutant des étudiants de 1ère année.

---

*Rapport généré automatiquement*
*Date: {Path(__file__).stat().st_mtime}*
"""
        
        report_file = self.new_corrections_dir / "rapport_global.md"
        report_file.write_text(report, encoding='utf-8')
        
        print(f"\n{'='*60}")
        print(f"TRAITEMENT TERMINE")
        print(f"{'='*60}")
        print(f"Total: {total_copies} copies corrigées")
        print(f"Moyenne ancienne: {global_old_avg:.2f}/20")
        print(f"Moyenne nouvelle: {global_new_avg:.2f}/20")
        print(f"Amélioration: {global_new_avg - global_old_avg:+.2f} points")
        print(f"Rapport global: {report_file}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    grader = EncouragingGrader()
    grader.process_all_groups()
