# 🧠 Feature Engineering - Guide Complet

Ce dossier contient toute la documentation sur l'ingénierie des features, l'optimisation et l'utilisation du système modulaire.

## 🎯 Vue d'Ensemble

Le projet utilise un **système modulaire** pour l'extraction de features avec 4 feature sets différents, chacun optimisé pour des cas d'usage spécifiques.

## 🚀 Comment Utiliser le Système Modulaire

### 1. **Commandes de Base**

```bash
# Utiliser le système modulaire avec un feature set spécifique
python scripts/run_pipeline.py --dataset mon_dataset --feature-system modular --feature-set visual_granular

# Utiliser le système legacy (par défaut)
python scripts/run_pipeline.py --dataset mon_dataset --feature-system legacy

# Voir l'aide pour tous les paramètres
python scripts/run_pipeline.py --help
```

### 2. **Feature Sets Disponibles**

| Feature Set       | Features | Description                                           | Cas d'Usage                          |
| ----------------- | -------- | ----------------------------------------------------- | ------------------------------------ |
| `metadata`        | 20       | Features de base (durée, engagement, hashtags)        | Analyse rapide, données limitées     |
| `gemini_basic`    | 14       | Features d'analyse Gemini (qualité, viralité)         | Analyse de contenu avec IA           |
| `visual_granular` | 10       | Features visuelles détaillées (composition, couleurs) | Analyse visuelle approfondie         |
| `comprehensive`   | 32       | Toutes les features combinées                         | Analyse complète, maximum d'insights |

### 3. **Exemples d'Utilisation**

```bash
# Analyse rapide avec features de base
python scripts/run_pipeline.py --dataset quick_test --feature-system modular --feature-set metadata

# Analyse visuelle détaillée
python scripts/run_pipeline.py --dataset visual_analysis --feature-system modular --feature-set visual_granular

# Analyse complète avec toutes les features
python scripts/run_pipeline.py --dataset full_analysis --feature-system modular --feature-set comprehensive
```

## 📊 Structure des Fichiers Générés

### Système Modulaire

```
data/dataset_mon_dataset/
├── features/
│   ├── compte1_features_metadata.csv          # Features de base pour compte1
│   ├── compte2_features_visual_granular.csv   # Features visuelles pour compte2
│   └── compte3_features_comprehensive.csv     # Toutes les features pour compte3
├── gemini_analysis/
│   ├── compte1/20250705/
│   │   └── video_123_analysis.json
│   └── compte2/20250705/
│       └── video_456_analysis.json
└── batch_20250705_123456.json
```

### Système Legacy

```
data/dataset_mon_dataset/
├── features/
│   └── processed_features.csv                 # UN SEUL fichier pour tous les comptes
├── gemini_analysis/
│   └── [même structure]
└── batch_20250705_123456.json
```

## 🔄 Agrégation des Features

### **Comment ça marche ?**

1. **Extraction par Compte** : Chaque compte génère son propre fichier de features
2. **Pas d'Agrégation Automatique** : Les features ne sont pas automatiquement agrégées
3. **Flexibilité** : Tu peux choisir comment combiner les données

### **Options d'Agrégation**

#### Option 1 : Utiliser les Fichiers Séparés

```python
import pandas as pd

# Charger les features de chaque compte
features_compte1 = pd.read_csv('data/dataset/features/compte1_features_visual_granular.csv')
features_compte2 = pd.read_csv('data/dataset/features/compte2_features_visual_granular.csv')

# Combiner manuellement
features_combinees = pd.concat([features_compte1, features_compte2], ignore_index=True)
```

#### Option 2 : Script d'Agrégation Automatique

```python
# Script pour agréger tous les fichiers d'un feature set
import pandas as pd
from pathlib import Path

def agreger_features(dataset_dir, feature_set):
    features_dir = Path(dataset_dir) / "features"
    fichiers = list(features_dir.glob(f"*_features_{feature_set}.csv"))

    all_features = []
    for fichier in fichiers:
        df = pd.read_csv(fichier)
        all_features.append(df)

    return pd.concat(all_features, ignore_index=True)

# Utilisation
features_agregees = agreger_features("data/dataset_mon_dataset", "visual_granular")
```

#### Option 3 : Utiliser le Système Legacy

```bash
# Le système legacy crée automatiquement un fichier consolidé
python scripts/run_pipeline.py --dataset mon_dataset --feature-system legacy
```

## 📋 Documentation Détaillée

### **Features Disponibles**

#### Metadata Features (20 features)

- `video_id`, `duration`, `view_count`, `like_count`, `comment_count`, `share_count`
- `hashtag_count`, `description_length`, `publish_hour`, `publish_day_of_week`
- `engagement_rate`, `like_rate`, `comment_rate`, `share_rate`
- Et plus...

#### Visual Granular Features (10 features)

- `human_count`, `eye_contact_with_camera`, `shot_type`
- `color_vibrancy_score`, `rule_of_thirds_score`, `depth_of_field_type`
- `color_palette_type`, `movement_intensity_score`, `composition_balance`
- `lighting_quality`

#### Comprehensive Features (32 features)

- Combinaison de toutes les catégories
- Features les plus complètes pour l'analyse

### **Optimisation et Sélection**

- [`optimization_summary.md`](./optimization_summary.md) - Stratégie d'optimisation
- [`phase1_feature_selection.md`](./phase1_feature_selection.md) - Sélection pour Phase 1
- [`enhanced_visual_features.md`](./enhanced_visual_features.md) - Features visuelles granulaires

## ⚠️ Points Importants

### **Fallback Automatique**

Si le système modulaire échoue, le pipeline bascule automatiquement vers le système legacy :

```
⚠️ Modular system failed: [erreur]
🔄 Falling back to legacy DataProcessor
```

### **Compatibilité**

- Les deux systèmes peuvent coexister
- Même structure de dossiers pour les analyses Gemini
- Différences uniquement dans la structure des features

### **Performance**

- **Metadata** : Plus rapide, moins de ressources
- **Visual Granular** : Nécessite des analyses Gemini
- **Comprehensive** : Plus lent, plus de features

## 🔗 Liens Utiles

- [Comprehensive Feature Engineering](./comprehensive_feature_engineering.md) - 107 features détaillées
- [Feature Engineering Optimization](./feature_engineering_optimization.md) - Stratégie d'optimisation
- [Visual Features Analysis](./visual_features_analysis.md) - Analyse des features visuelles
- [Migration Summary](../../migration_summary.md) - Guide de migration
