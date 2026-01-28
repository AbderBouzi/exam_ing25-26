# Système de Correction Encourageante pour Étudiants Débutants

## 📖 Description

Ce système permet de corriger les examens de programmation C des étudiants de 1ère année avec une approche **encourageante et bienveillante**, tout en comparant avec les notes d'une correction stricte.

## 🎯 Philosophie

**"Arkhaf fi tashah"** - Soyez indulgent dans la correction

L'approche valorise:
- ✅ L'effort et la compréhension des concepts
- ✅ Les tentatives même incomplètes
- ✅ La logique algorithmique même avec des erreurs de syntaxe
- ✅ Les bonnes pratiques (initialisation, messages utilisateur)

## 📊 Résultats

- **104 copies corrigées** across 11 PDF groups
- **Amélioration moyenne**: +8.11 points (9.47/20 → 17.58/20)
- **93.3%** des étudiants ont vu leur note s'améliorer

## 📁 Structure des Fichiers

```
exam_ing25-26/
├── grade_exams.py                      # Script de correction principal
├── extracted_code/                     # Code extrait des PDFs
│   ├── code_*.md                       # Fichiers de code par groupe
│   └── corrections/                    # Anciennes corrections (strictes)
│       └── Corr_*.md
└── corrections_par_groupe/             # Nouvelles corrections (encourageantes)
    ├── rapport_global.md               # Rapport global avec statistiques
    └── groupe_*/
        ├── corrections.md              # Corrections détaillées
        └── statistiques.md             # Statistiques du groupe
```

## 🚀 Utilisation

### Prérequis

- Python 3.8+
- Fichiers de code extraits dans `extracted_code/code_*.md`
- Anciennes corrections dans `extracted_code/corrections/Corr_*.md`

### Exécution

```bash
cd c:\exam_ing25-26
python grade_exams.py
```

Le script va:
1. Extraire les anciennes notes de chaque groupe
2. Analyser chaque copie avec le barème encourageant
3. Générer les corrections avec comparaison
4. Créer les statistiques par groupe
5. Produire un rapport global

### Résultats

Les corrections sont organisées par groupe dans `corrections_par_groupe/`:
- `groupe_*/corrections.md` - Corrections détaillées de toutes les copies
- `groupe_*/statistiques.md` - Statistiques du groupe
- `rapport_global.md` - Vue d'ensemble de tous les groupes

## 📋 Format des Corrections

Chaque correction inclut:

### 📊 Comparaison des Notes
```markdown
| Ancienne Note | Nouvelle Note | Différence |
|:-------------:|:-------------:|:----------:|
| 6/20          | 17/20         | +11        |
```

### ✅ Points Forts
Liste des éléments bien réalisés par l'étudiant

### 📝 Code Soumis
Le code de l'étudiant formaté

### 🔍 Analyse Détaillée
Analyse critère par critère avec comparaison ancienne/nouvelle note:
- Lecture des données (4 pts)
- Initialisation (3 pts)
- Structure de boucle (5 pts)
- Logique présence/absence (5 pts)
- Compteurs (2 pts)
- Affichages (1 pt)

### 💡 Suggestions d'Amélioration
Conseils constructifs et spécifiques

### 🌟 Message d'Encouragement
Message personnalisé selon la note:
- 18-20: Excellent travail!
- 15-17: Très bon travail!
- 12-14: Bon travail!
- 9-11: Vous avez compris plusieurs concepts
- 6-8: Vous avez fait des efforts
- 0-5: C'est un début, continuez!

### 📋 Ancienne Correction
L'analyse stricte précédente (section repliable)

## 🎓 Barème de Notation

### Nouveau Barème (Encourageant)

| Critère | Points | Description |
|:--------|:------:|:------------|
| Lecture des données | 4 | Lecture de N, A, S avec scanf (+1 bonus si printf avant) |
| Initialisation | 3 | Déclaration et initialisation des variables |
| Structure de boucle | 5 | Boucle for/while avec condition correcte |
| Logique présence/absence | 5 | Comparaison X < A avec if/else |
| Compteurs | 2 | Incrémentation pour présents/absents |
| Affichages | 1 | Affichages des résultats |
| **TOTAL** | **20** | |

### Comparaison avec l'Ancien Barème

| Critère | Ancien | Nouveau | Changement |
|:--------|:------:|:-------:|:----------:|
| Lecture N, A, S | 3 | 4 | +1 |
| Initialisation | 3 | 3 | = |
| Condition boucle | 4 | 5 | +1 |
| Logique prés./abs. | 4 | 5 | +1 |
| Compteurs | 3 | 2 | -1 |
| Affichages | 3 | 1 | -2 |

## 🔧 Personnalisation

### Modifier les Messages d'Encouragement

Dans `grade_exams.py`, fonction `generate_encouragement()`:

```python
def generate_encouragement(self, note: int, points_forts: List[str]) -> str:
    if note >= 18:
        return "Votre message pour 18-20"
    elif note >= 15:
        return "Votre message pour 15-17"
    # etc.
```

### Ajuster le Barème

Dans `grade_with_encouragement()`, modifiez les points attribués:

```python
# Exemple: augmenter les points pour la lecture
if 'scanf' in code_lower and '&n' in code_lower:
    new_grade['lecture_donnees'] += 3  # au lieu de 2
```

## 📈 Statistiques Générées

### Par Groupe
- Nombre de copies
- Moyenne ancienne/nouvelle
- Différence moyenne
- Nombre de copies améliorées
- Pourcentage d'amélioration

### Global
- Total de copies corrigées
- Moyenne générale ancienne/nouvelle
- Amélioration moyenne globale
- Tableau comparatif par groupe

## 🐛 Résolution de Problèmes

### Erreur: "Fichier de code non trouvé"
Vérifiez que les fichiers `code_*.md` sont dans `extracted_code/`

### Erreur: "Division by zero"
Certains groupes n'ont pas de copies extraites (normal)

### Erreur Unicode
Le script utilise du texte ASCII pour compatibilité Windows

## 📝 Notes Importantes

1. **Encodage**: Tous les fichiers sont en UTF-8
2. **Compatibilité**: Testé sur Windows avec Python 3.12
3. **Anciennes corrections**: Conservées dans section repliable
4. **Pas de modification**: Les fichiers originaux ne sont jamais modifiés

## 👥 Auteur

Système créé pour encourager les étudiants débutants en programmation C, 1ère année Informatique.

## 📄 Licence

Usage éducatif - Université

---

**Date de création**: Janvier 2026
**Version**: 1.0
**Copies traitées**: 104
**Amélioration moyenne**: +8.11 points
