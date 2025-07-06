# 🔬 ITER_004: Dataset Cleaning & Feature Engineering

## 📋 **Informations Générales**

- **Itération ID**: `ITER_004`
- **Date de début**: `2025-07-06`
- **Date de fin**: `[En cours]`
- **Responsable**: `Équipe POC`
- **Version du modèle**: `iter_004`

---

## 🎯 **Hypothèse de Recherche**

### **Question Principale**

> Le nettoyage du dataset et l'amélioration des features peuvent-ils résoudre l'overfitting et améliorer la généralisation du modèle ?

### **Hypothèses Testées**

1. **H1**: Supprimer les duplications (62%) améliore la généralisation
2. **H2**: Équilibrer la distribution par compte réduit le biais
3. **H3**: Nouvelles features basées sur la qualité > quantité améliorent les prédictions
4. **H4**: Validation croisée stratifiée par compte mesure mieux la généralisation

### **Objectifs Spécifiques**

- [ ] Nettoyer le dataset en supprimant les duplications
- [ ] Équilibrer la distribution par compte (max 10 vidéos/compte)
- [ ] Implémenter de nouvelles features de qualité
- [ ] Entraîner un nouveau modèle sur le dataset propre
- [ ] Valider avec cross-validation stratifiée
- [ ] Comparer les performances avec ITER_003

---

## 📊 **Variables Expérimentales**

### **Variables Constantes**

| Variable          | Valeur                    | Justification               |
| ----------------- | ------------------------- | --------------------------- |
| **Modèle ML**     | `XGBoost`                 | Meilleur performer ITER_003 |
| **Feature set**   | `model_compatible`        | 16 features de base         |
| **Validation**    | `Cross-validation 5-fold` | Validation robuste          |
| **API Framework** | `FastAPI`                 | Framework de production     |

### **Variables Manipulées**

| Variable         | Valeur Testée                   | Valeur Contrôle       | Impact sur le Code                       | Justification              |
| ---------------- | ------------------------------- | --------------------- | ---------------------------------------- | -------------------------- |
| **Dataset**      | `Nettoyé (sans duplications)`   | `ITER_002 (dupliqué)` | `scripts/clean_dataset.py`               | Résoudre l'overfitting     |
| **Distribution** | `Équilibrée (max 10/compte)`    | `Déséquilibrée`       | `scripts/balance_dataset.py`             | Réduire le biais de compte |
| **Features**     | `Nouvelles features de qualité` | `16 features de base` | `src/features/modular_feature_system.py` | Améliorer les prédictions  |
| **Validation**   | `Stratifiée par compte`         | `Random CV`           | `scripts/train_model.py`                 | Mesurer la généralisation  |

---

## 🔬 **Protocole Expérimental**

### **Phase 1: Nettoyage du Dataset** 🧹

```bash
# Supprimer les duplications
python scripts/clean_dataset.py --input data/dataset_iter_002/features/aggregated_comprehensive.csv --output data/dataset_iter_004_clean/clean_dataset.csv --max-videos-per-account 10

# Équilibrer la distribution par compte
python scripts/balance_dataset.py --input data/dataset_iter_004_clean/clean_dataset.csv --max-videos-per-account 10 --output data/dataset_iter_004_clean/balanced_dataset.csv
```

**Résultats**:

- **Dataset original**: 84 vidéos (62% duplications)
- **Dataset nettoyé**: 20 vidéos (0% duplications)
- **Distribution**: 2 comptes équilibrés (10 vidéos chacun)

### 🔧 **Corrections Apportées - Phase 1**

### **Problèmes Identifiés et Résolus**

#### **1. Critères de Validation Trop Stricts** ✅ Corrigé

**Problème**: Les critères de validation rejetaient trop de vidéos valides

- `min_views = 1000` → Rejetait les vidéos avec < 1000 vues
- `max_video_age_days = 180` → Rejetait les vidéos > 6 mois
- `min_video_duration = 1` → Rejetait les vidéos < 1 seconde

**Solution**: Critères assouplis dans `src/utils/data_validator.py`

```python
# AVANT (trop strict)
self.min_views = 1000
self.max_video_age_days = 180  # 6 mois
self.min_video_duration = 1  # seconde

# APRÈS (plus permissif)
self.min_views = 100  # 10x plus permissif
self.max_video_age_days = 365  # 1 an au lieu de 6 mois
self.min_video_duration = 0.5  # 0.5 seconde au lieu de 1
```

#### **2. Limitation Artificielle du Nettoyage** ✅ Corrigé

**Problème**: Le script de nettoyage limitait artificiellement à 10 vidéos par compte

- Dataset original: 84 vidéos → 20 vidéos (perte de 64 vidéos)

**Solution**: Limitation augmentée dans `scripts/clean_dataset.py`

```python
# AVANT
def clean_dataset(input_file, output_file, max_videos_per_account=10):

# APRÈS
def clean_dataset(input_file, output_file, max_videos_per_account=20):
```

#### **3. Analyse des Duplications** ✅ Ajoutée

**Problème**: 61.9% de duplications dans ITER_002 (52/84 vidéos)

- Mêmes vidéos attribuées à 3 comptes différents
- Seulement 32 vidéos uniques sur 84 total

**Solution**: Script d'analyse des duplications ajouté

```bash
python scripts/analyze_dataset.py --input data/dataset_iter_002/features/aggregated_comprehensive.csv --analyze-duplications
```

### **Résultats des Corrections**

**Dataset ITER_002**:

- **Avant**: 20 vidéos (critères stricts)
- **Après**: 32 vidéos (critères assouplis)
- **Amélioration**: +60% de vidéos conservées

**Validation des Critères**:

- ✅ Plus de vidéos conservées lors du scraping
- ✅ Critères plus réalistes pour TikTok
- ✅ Meilleure représentation de la diversité

### **Phase 2: Collecte de Données Diversifiées** 📊

```bash
# Collecte avec randomisation et diversité
python scripts/run_pipeline.py --dataset iter_004_diverse --batch-size 3 --videos-per-account 10 --max-total-videos 150 --enable-diversity --random-seed 42 --max-accounts 15 --feature-set comprehensive

# Collecte simple avec randomisation
python scripts/run_pipeline.py --dataset iter_004_random --batch-size 5 --videos-per-account 10 --max-total-videos 200 --random-seed 123
```

**Nouvelles Fonctionnalités**:

- **Randomisation des comptes**: Sélection aléatoire pour éviter les biais
- **Diversité par catégories**: Assure la représentation de différents types de contenu
- **Contrôle de la randomisation**: Seed reproductible et limite de comptes
- **Batches diversifiés**: Mélange de catégories dans chaque batch

**Catégories de Comptes**:

- **Lifestyle**: @leaelui, @unefille.ia, @lea*mary, @marie29france*
- **Tech**: @swarecito, @julien.snsn, @david_sepahan
- **Food**: @swiss_fit.cook, @healthyfood_creation, @pastelcuisine
- **Gaming**: @gotaga, @domingo, @squeezie, @sosah1.6
- **Humor**: @athenasol, @isabrunellii, @contiped
- **Travel**: @loupernaut, @astucequotidienne87
- **Fitness**: @oceane_dmg

### **Phase 3: Nouvelles Features** 🆕

```bash
# Implémenter les nouvelles features
# - hashtag_quality_score
# - creator_popularity_bias
# - content_uniqueness_score
# - completion_rate_estimate

# Tester les nouvelles features
python scripts/test_new_features.py --dataset data/dataset_iter_004_clean/balanced_dataset.csv
```

**Nouvelles Features**:

- `hashtag_quality_score`: Qualité vs quantité des hashtags
- `creator_popularity_bias`: Correction du biais de popularité
- `content_uniqueness_score`: Mesure d'unicité du contenu
- `completion_rate_estimate`: Estimation du taux de completion

### **Phase 4: Entraînement du Modèle** 🤖

```bash
# Entraîner avec validation stratifiée
python scripts/train_model_iter_004.py --dataset data/dataset_iter_004_clean/balanced_dataset.csv --feature-set enhanced --validation-strategy stratified --save-model
```

**Métriques à surveiller**:

- **R² Score** (objectif: > 0.6 avec généralisation)
- **MAE** (objectif: < 0.3)
- **RMSE** (objectif: < 0.4)
- **Généralisation** (objectif: R² > 0.5 sur comptes non vus)

### **Phase 5: Validation et Tests** ✅

```bash
# Tests sur nouveaux comptes
python scripts/test_generalization.py --model models/iter_004_xgboost_model.pkl --test-accounts new_accounts.txt

# Tests API
python scripts/test_api_iter_004.py
```

### **Phase 6: Documentation et Contenu Éducatif** 📚

- [ ] Mettre à jour `docs/iterations/ITER_004_dataset_cleaning.md`
- [ ] Créer contenu TikTok sur le nettoyage de données
- [ ] Documenter les nouvelles features

---

## 📊 **Résultats et Insights**

### **Phase 1: Nettoyage du Dataset** ✅

**Résultats**:

- **Dataset original**: 84 vidéos (62% duplications)
- **Dataset nettoyé**: 20 vidéos (0% duplications)
- **Distribution**: 2 comptes équilibrés (10 vidéos chacun)

### **Phase 2: Collecte de Données Diversifiées** ✅

**Test de Randomisation Réussi**:

```bash
# Test avec 5 comptes, randomisation activée
python scripts/run_pipeline.py --dataset test_randomization --batch-size 2 --videos-per-account 3 --max-total-videos 20 --enable-diversity --random-seed 123 --max-accounts 5 --feature-set comprehensive
```

**Résultats du Test**:

- ✅ **Randomisation fonctionnelle**: 5 comptes sélectionnés aléatoirement
- ✅ **Diversité par catégories**: Batches mélangent food, gaming, humor
- ✅ **Gestion d'erreurs**: 1 compte invalide détecté et ignoré
- ✅ **Agrégation automatique**: 12 features agrégées de 4 comptes
- ✅ **Performance**: 8 vidéos collectées en ~3 minutes

**Comptes Traités**:

- **Batch 1**: @healthyfood_creation (food), @gotaga (gaming) - 4 vidéos
- **Batch 2**: @squeezie (gaming), @isabrunellii@domingo (échec) - 3 vidéos
- **Batch 3**: @sosah1.6 (gaming) - 1 vidéo

**Nouvelles Fonctionnalités Validées**:

- **`--random-seed`**: Contrôle la reproductibilité (seed=123)
- **`--enable-diversity`**: Active la sélection par catégories
- **`--max-accounts`**: Limite le nombre de comptes traités
- **Logs améliorés**: Affichage des catégories dans chaque batch

### **Phase 3: Nouvelles Features** 🆕

```bash
# Test des nouvelles features de qualité
python scripts/test_new_features.py --input data/dataset_iter_004_clean/cleaned_dataset.csv
```

**Features Ajoutées**:

- `hashtag_quality_score`: Qualité des hashtags utilisés
- `creator_bias_factor`: Biais du créateur
- `content_uniqueness`: Unicité du contenu
- `completion_rate_estimate`: Estimation du taux de completion

### **Phase 4: Entraînement du Modèle** 🤖

```bash
# Entraînement avec validation croisée stratifiée
python scripts/train_xgboost_model.py --input data/dataset_iter_004_clean/balanced_dataset.csv --cv-folds 5 --stratified
```

**Métriques Objectifs**:

- **R² Score** (objectif: > 0.6)
- **Généralisation** (objectif: R² > 0.5 sur comptes non vus)

### **Phase 5: Validation et Tests** ✅

```bash
# Tests complets
python scripts/test_model_final.py --model models/iter_004_xgboost.pkl --test-data data/dataset_iter_004_clean/test_set.csv
```

### **Phase 6: Documentation et Contenu Éducatif** 📚

- [ ] Mettre à jour `docs/iterations/ITER_004_dataset_cleaning.md`
- [ ] Créer contenu TikTok sur la diversité des données
- [ ] Documenter les nouvelles features

---

## 🎯 **Situation Actuelle et Recommandations**

### **📊 Analyse de la Situation**

**Dataset Actuel (ITER_002)**:

- **20 vidéos** de **2 comptes** seulement
- **Problèmes identifiés**:
  - Dataset trop petit (besoin de 100+ vidéos)
  - Manque de diversité des comptes (besoin de 10+ comptes)
  - Corrélations faibles avec les vues (seulement 2 corrélations > 0.3)

**Corrélations Actuelles**:

- `like_count`: 0.979 (très forte)
- `comment_count`: 0.966 (très forte)
- `share_count`: 0.608 (modérée)
- `hour_of_day`: 0.353 (faible)
- Autres features: corrélations très faibles (< 0.3)

### **🚀 Plan de Collecte ITER_004**

**Objectifs**:

- **150 vidéos** de **15 comptes** diversifiés
- **10 vidéos par compte** (équilibré)
- **6 catégories** représentées

**Commande de Collecte**:

```bash
python scripts/run_pipeline.py --dataset iter_004_diverse --batch-size 3 --videos-per-account 10 --max-total-videos 150 --enable-diversity --random-seed 42 --max-accounts 15 --feature-set comprehensive
```

**Catégories Cibles**:

- **Lifestyle**: @leaelui, @unefille.ia, @lea*mary, @marie29france*
- **Tech**: @swarecito, @julien.snsn, @david_sepahan
- **Food**: @swiss_fit.cook, @healthyfood_creation, @pastelcuisine
- **Gaming**: @gotaga, @domingo, @squeezie, @sosah1.6
- **Humor**: @athenasol, @isabrunellii, @contiped
- **Travel**: @loupernaut, @astucequotidienne87

### **✅ Scripts Documentés et Prêts**

**Scripts de Data Processing**:

- ✅ `scripts/clean_dataset.py` - Nettoyage et déduplication
- ✅ `scripts/balance_dataset.py` - Équilibrage par compte
- ✅ `scripts/analyze_dataset.py` - Analyse et recommandations

**Scripts de Collecte**:

- ✅ `scripts/run_pipeline.py` - Pipeline principal avec randomisation
- ✅ `scripts/aggregate_features.py` - Agrégation automatique

**Fichiers Supprimés**:

- ❌ 10+ datasets de test obsolètes
- ❌ Scripts de test redondants
- ✅ Structure simplifiée et organisée

### **🎯 Prochaines Étapes**

1. **Collecte de Données** (1-2 jours):

   ```bash
   python scripts/run_pipeline.py --dataset iter_004_diverse --enable-diversity --max-accounts 15
   ```

2. **Nettoyage et Équilibrage** (1 jour):

   ```bash
   python scripts/clean_dataset.py --input data/dataset_iter_004_diverse/features/aggregated_comprehensive.csv --output data/dataset_iter_004_final/cleaned_dataset.csv --max-videos-per-account 10
   python scripts/balance_dataset.py --input data/dataset_iter_004_final/cleaned_dataset.csv --output data/dataset_iter_004_final/balanced_dataset.csv --max-videos-per-account 10
   ```

3. **Entraînement du Modèle** (1 jour):

   ```bash
   python scripts/train_xgboost_model.py --input data/dataset_iter_004_final/balanced_dataset.csv --cv-folds 5 --stratified
   ```

4. **Validation et Tests** (1 jour):
   ```bash
   python scripts/test_model_final.py --model models/iter_004_xgboost.pkl
   ```

**Estimation Totale**: 4-5 jours pour ITER_004 complet

---

## 🎬 **Contenu Éducatif Créé**

### **Vidéos TikTok**

- **Vidéo 1**: "Comment nettoyer un dataset ML pour éviter l'overfitting" - [À créer]
- **Vidéo 2**: "Feature Engineering: Qualité vs Quantité" - [À créer]

### **Articles/Posts**

- **Article 1**: "ITER_004: Nettoyage de dataset et nouvelles features" - [À créer]
- **Article 2**: "Validation croisée stratifiée: Mesurer la vraie généralisation" - [À créer]

### **Documentation Mise à Jour**

- [ ] `docs/iterations/ITER_004_dataset_cleaning.md` - Documentation complète
- [ ] `src/features/modular_feature_system.py` - Nouvelles features
- [ ] `scripts/clean_dataset.py` - Script de nettoyage
- [ ] `scripts/balance_dataset.py` - Script d'équilibrage

---

## 🔄 **Itération Suivante**

### **Améliorations Identifiées**

1. **Collecte de Données Diversifiées** (Priorité: Haute)

   - **Description**: Collecter des données de créateurs émergents
   - **Effort estimé**: 2 jours

2. **Features Avancées** (Priorité: Moyenne)

   - **Description**: Features basées sur l'analyse de contenu vidéo
   - **Effort estimé**: 3 jours

3. **Ensemble Methods** (Priorité: Basse)
   - **Description**: Combiner plusieurs modèles
   - **Effort estimé**: 2 jours

### **Variables à Tester**

1. **Diversité des Créateurs** - Inclure des créateurs émergents
2. **Features Vidéo** - Analyse du contenu visuel
3. **Temporal Features** - Patterns temporels de viralité

### **Objectifs de la Prochaine Itération**

- [ ] Collecter des données de créateurs émergents
- [ ] Implémenter des features d'analyse vidéo
- [ ] Tester avec un dataset plus diversifié
- [ ] Valider la généralisation sur nouveaux créateurs

---

## 📚 **Références et Liens**

### **Documentation Référencée**

- **Analyse ITER_003**: `docs/iterations/ITER_003_dataset_analysis.md`
- **Template Itération**: `docs/iterations/template_iteration.md`
- **Feature System**: `src/features/modular_feature_system.py`

### **Scripts Utilisés**

- **Nettoyage**: `scripts/clean_dataset.py`
- **Équilibrage**: `scripts/balance_dataset.py`
- **Training**: `scripts/train_model_iter_004.py`
- **Testing**: `scripts/test_generalization.py`

### **Données et Modèles**

- **Dataset Original**: `data/dataset_iter_002/features/aggregated_comprehensive.csv`
- **Dataset Nettoyé**: `data/dataset_iter_004_clean/`
- **Modèle**: `models/iter_004_xgboost_model.pkl`

---

## ✅ **Checklist de Validation**

### **Avant de Commencer**

- [x] Template rempli complètement
- [x] Hypothèses clairement définies
- [x] Variables expérimentales identifiées
- [x] Protocole validé

### **Pendant l'Expérimentation**

- [ ] Dataset nettoyé et équilibré
- [ ] Nouvelles features implémentées
- [ ] Modèle entraîné avec validation stratifiée
- [ ] Tests de généralisation effectués

### **Après l'Expérimentation**

- [ ] Résultats analysés et comparés
- [ ] Documentation mise à jour
- [ ] Prochaine itération planifiée
- [ ] Commit avec message descriptif

---

**Dernière mise à jour**: `2025-07-06`
**Version**: `v1.0.0`
**Statut**: `🚀 En cours - Phase 1: Nettoyage du Dataset`
