# 🔄 Guide d'Agrégation des Features

## 🎯 Comprendre l'Agrégation des Features

### **Comment ça marche ?**

Quand tu utilises le **système modulaire**, chaque compte génère son propre fichier de features :

```
data/dataset_mon_dataset/features/
├── unefille.ia_features_visual_granular.csv    # 1 fichier pour unefille.ia
├── loupernaut_features_visual_granular.csv     # 1 fichier pour loupernaut
└── athenasol_features_visual_granular.csv      # 1 fichier pour athenasol
```

**Question :** Est-ce que les features sont agrégées automatiquement ?

**Réponse :** **NON** - Le système modulaire ne fait **PAS** d'agrégation automatique. Chaque compte garde son fichier séparé pour plus de flexibilité.

## 🚀 Options d'Agrégation

### **Option 1 : Script d'Agrégation Automatique** (Recommandé)

```bash
# Agréger toutes les features metadata
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set metadata --output features_agregees.csv

# Agréger avec statistiques détaillées
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set visual_granular --show-stats
```

**Résultat :**

```csv
video_id,human_count,eye_contact_with_camera,...,account_name
7488008313704172822,0,False,...,unefille.ia
7505807127567453462,1,True,...,loupernaut
7165165723566755077,2,True,...,athenasol
```

### **Option 2 : Agrégation Manuelle en Python**

```python
import pandas as pd
from pathlib import Path

def agreger_features_manuelle(dataset_dir, feature_set):
    features_dir = Path(dataset_dir) / "features"
    fichiers = list(features_dir.glob(f"*_features_{feature_set}.csv"))

    all_features = []
    for fichier in fichiers:
        df = pd.read_csv(fichier)
        # Extraire le nom du compte
        account_name = fichier.stem.split('_features_')[0]
        df['account_name'] = account_name
        all_features.append(df)

    return pd.concat(all_features, ignore_index=True)

# Utilisation
features_combinees = agreger_features_manuelle("data/dataset_mon_dataset", "visual_granular")
features_combinees.to_csv("features_agregees.csv", index=False)
```

### **Option 3 : Utiliser le Système Legacy**

Si tu veux un fichier consolidé automatiquement :

```bash
# Le système legacy crée automatiquement un seul fichier
python scripts/run_pipeline.py --dataset mon_dataset --feature-system legacy
```

**Résultat :**

```
data/dataset_mon_dataset/features/
└── processed_features.csv    # UN SEUL fichier pour tous les comptes
```

## 📊 Exemple Pratique

### **Avant Agrégation** (Système Modulaire)

```
data/dataset_test_modular/features/
├── unefille.ia_features_metadata.csv    # 2 features
└── loupernaut_features_metadata.csv     # 1 feature
```

### **Après Agrégation**

```bash
python scripts/aggregate_features.py --dataset-dir data/dataset_test_modular --feature-set metadata --show-stats
```

**Résultat :**

```
📊 Statistiques des Features Agrégées:
   • Total de features: 3
   • Comptes uniques: ['unefille.ia' 'loupernaut']
   • Features par compte:
     - unefille.ia: 2 features
     - loupernaut: 1 features
```

## 🎯 Quand Utiliser l'Agrégation ?

### **✅ Utiliser l'Agrégation pour :**

- **Analyse globale** : Voir les patterns across tous les comptes
- **Machine Learning** : Entraîner des modèles sur l'ensemble des données
- **Comparaisons** : Comparer les performances entre comptes
- **Visualisations** : Créer des graphiques avec toutes les données

### **✅ Garder les Fichiers Séparés pour :**

- **Analyse par compte** : Étudier chaque compte individuellement
- **Debugging** : Identifier les problèmes spécifiques à un compte
- **Flexibilité** : Traiter certains comptes différemment
- **Performance** : Éviter de charger toutes les données en mémoire

## 🔧 Commandes Utiles

### **Voir les Fichiers Disponibles**

```bash
# Lister tous les fichiers de features d'un dataset
ls data/dataset_mon_dataset/features/

# Lister les fichiers d'un feature set spécifique
ls data/dataset_mon_dataset/features/*_features_visual_granular.csv
```

### **Agréger avec Options**

```bash
# Agrégation basique
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set metadata

# Agrégation avec fichier de sortie
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set visual_granular --output visual_features_agregees.csv

# Agrégation sans colonne compte (pour ML)
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set comprehensive --no-account-column --output ml_features.csv
```

### **Vérifier les Données**

```bash
# Voir les statistiques détaillées
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set metadata --show-stats

# Voir un aperçu des données
python scripts/aggregate_features.py --dataset-dir data/dataset_mon_dataset --feature-set visual_granular
```

## ⚠️ Points Importants

### **1. Cohérence des Feature Sets**

- Assure-toi que tous les comptes utilisent le **même feature set**
- Les colonnes doivent être identiques pour l'agrégation

### **2. Gestion des Données Manquantes**

- Le script gère automatiquement les fichiers manquants
- Les erreurs de chargement sont loggées mais n'arrêtent pas l'agrégation

### **3. Performance**

- Pour de gros datasets, l'agrégation peut prendre du temps
- Utilise `--show-stats` pour voir le progrès

### **4. Compatibilité**

- Le script fonctionne avec tous les feature sets : `metadata`, `gemini_basic`, `visual_granular`, `comprehensive`
- Compatible avec la structure de dossiers du pipeline

## 🎉 Résumé

**L'agrégation des features :**

- ✅ **N'est PAS automatique** dans le système modulaire
- ✅ **Peut être faite facilement** avec le script `aggregate_features.py`
- ✅ **Offre de la flexibilité** : tu choisis quand et comment agréger
- ✅ **Maintient la traçabilité** : tu sais d'où viennent les données

**Pour commencer :**

1. Lance le pipeline avec le système modulaire
2. Utilise le script d'agrégation quand tu as besoin de données consolidées
3. Choisis l'option qui correspond à ton cas d'usage
