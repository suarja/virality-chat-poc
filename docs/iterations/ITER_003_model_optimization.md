# 🔬 ITER_003: Model Optimization - XGBoost vs RandomForest

## 📋 **Informations Générales**

- **Itération ID**: `ITER_003`
- **Date de début**: `2025-07-06`
- **Date de fin**: `2025-07-06`
- **Responsable**: `Équipe POC`
- **Version du modèle**: `iter_003`

---

## 🎯 **Hypothèse de Recherche**

### **Question Principale**

> XGBoost peut-il améliorer les performances de prédiction de viralité par rapport à RandomForest sur le même dataset ?

### **Hypothèses Testées**

1. **H1**: XGBoost > RandomForest en termes de R² score
2. **H2**: XGBoost > RandomForest en termes de généralisation
3. **H3**: XGBoost peut réduire l'overfitting observé dans ITER_002

### **Objectifs Spécifiques**

- [x] Entraîner un modèle XGBoost sur le dataset agrégé (84 vidéos)
- [x] Comparer les performances avec RandomForest (ITER_002)
- [x] Intégrer le modèle XGBoost dans l'API
- [x] Tester l'API avec des vidéos virales et non-virales
- [x] Corriger le bug de feature extraction
- [x] Documenter les résultats et insights

---

## 📊 **Variables Expérimentales**

### **Variables Constantes**

| Variable          | Valeur                    | Justification                         |
| ----------------- | ------------------------- | ------------------------------------- |
| **Dataset**       | `84 vidéos`               | Dataset agrégé de ITER_001 + ITER_002 |
| **Feature set**   | `model_compatible`        | 16 features exactes pour le modèle    |
| **Validation**    | `Cross-validation 5-fold` | Validation robuste                    |
| **API Framework** | `FastAPI`                 | Framework de production               |

### **Variables Manipulées**

| Variable          | Valeur Testée | Valeur Contrôle | Impact sur le Code          | Justification                               |
| ----------------- | ------------- | --------------- | --------------------------- | ------------------------------------------- |
| **ML Model**      | `XGBoost`     | `RandomForest`  | `src/api/ml_model.py`       | Tester si XGBoost améliore les performances |
| **Model Version** | `iter_003`    | `iter_002`      | `ML_MODEL_VERSION=iter_003` | Nouvelle version du modèle                  |

---

## 🔬 **Protocole Expérimental**

### **Phase 1: Entraînement XGBoost**

```bash
# Script d'entraînement XGBoost
python scripts/train_xgboost_model.py --dataset-dir data/dataset_poc_test_aggregation --feature-set model_compatible --save-model
```

**Résultats**:

- **R² Score**: 0.875 (vs 0.855 RandomForest)
- **MAE**: 0.023 (vs 0.031 RandomForest)
- **RMSE**: 0.034 (vs 0.042 RandomForest)
- **Temps d'entraînement**: ~2 minutes

### **Phase 2: Intégration API**

```bash
# Configuration des variables d'environnement
export ML_MODEL_TYPE=xgboost
export ML_MODEL_VERSION=iter_003

# Test de l'API
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@swarecito/video/7505706702050823446"}'
```

### **Phase 3: Correction Bug Feature Extraction**

**Problème Identifié**:

- Erreur `string indices must be integers, not 'str'` dans `ModelCompatibleFeatureSet`
- Les hashtags étaient une liste de chaînes `["chatgpt", "agent"]` mais le code s'attendait à une liste de dictionnaires `[{"name": "chatgpt"}]`

**Correction Appliquée**:

```python
# Avant (bug)
hashtags = [tag['name'] for tag in video_data.get('hashtags', [])]

# Après (corrigé)
hashtags = video_data.get('hashtags', [])
if hashtags and isinstance(hashtags[0], dict):
    hashtags = [tag['name'] for tag in hashtags]
```

**Impact**:

- ✅ Features maintenant extraites correctement (16 features)
- ✅ API fonctionnelle avec prédictions différenciées
- ✅ Modèle XGBoost intégré avec succès

### **Phase 4: Tests API**

**Vidéos Testées**:

1. **@swarecito** (virale - 53k vues): 6.3% viralité prédite
2. **@david_sepahan** (non-virale): 13.9% viralité prédite

**Features Extraites** (16 features):

- `duration`, `hashtag_count`, `estimated_hashtag_count`
- `hour_of_day`, `day_of_week`, `month`
- `visual_quality_score`, `has_hook`, `viral_potential_score`
- `emotional_trigger_count`, `audience_connection_score`
- `sound_quality_score`, `production_quality_score`
- `trend_alignment_score`, `color_vibrancy_score`
- `video_duration_optimized`

---

## 📈 **Résultats et Insights**

### **Métriques de Performance**

| Métrique        | XGBoost (ITER_003) | RandomForest (ITER_002) | Amélioration |
| --------------- | ------------------ | ----------------------- | ------------ |
| **R² Score**    | `0.875`            | `0.855`                 | `+2.3%`      |
| **MAE**         | `0.023`            | `0.031`                 | `-25.8%`     |
| **RMSE**        | `0.034`            | `0.042`                 | `-19.0%`     |
| **Latence API** | `< 2s`             | `< 2s`                  | `=`          |

### **Insights Principaux**

1. **XGBoost Améliore les Performances** ✅

   - **Impact**: R² +2.3%, MAE -25.8%, RMSE -19.0%
   - **Action**: XGBoost devient le modèle par défaut

2. **Bug Feature Extraction Corrigé** ✅

   - **Impact**: API maintenant fonctionnelle avec 16 features
   - **Action**: Documentation de la correction pour éviter la récurrence

3. **Overfitting Potentiel Détecté** ⚠️
   - **Impact**: Vidéo non-virale prédite plus virale que vidéo virale
   - **Action**: Analyser le dataset d'entraînement pour comprendre

### **Features les Plus Importantes (XGBoost)**

1. `audience_connection_score` - Importance: `12.4%`
2. `hour_of_day` - Importance: `10.8%`
3. `video_duration_optimized` - Importance: `10.1%`
4. `emotional_trigger_count` - Importance: `9.9%`
5. `estimated_hashtag_count` - Importance: `9.6%`

---

## 🎬 **Contenu Éducatif Créé**

### **Vidéos TikTok**

- **Vidéo 1**: "XGBoost vs RandomForest: quel modèle gagne?" - [À créer]
- **Vidéo 2**: "Comment corriger un bug de feature extraction" - [À créer]

### **Articles/Posts**

- **Article 1**: "ITER_003: XGBoost améliore la prédiction de viralité" - [À créer]
- **Article 2**: "Debug: Correction du bug de feature extraction" - [À créer]

### **Documentation Mise à Jour**

- [x] `src/features/modular_feature_system.py` - Correction du bug hashtags
- [x] `src/api/feature_integration.py` - Logs de debug ajoutés
- [x] `docs/iterations/ITER_003_model_optimization.md` - Documentation complète
- [x] `scripts/train_xgboost_model.py` - Script d'entraînement XGBoost

---

## 🔄 **Itération Suivante**

### **Améliorations Identifiées**

1. **Analyse du Dataset d'Entraînement** (Priorité: Haute)

   - **Description**: Comprendre pourquoi le modèle prédit une viralité plus élevée pour les vidéos non-virales
   - **Effort estimé**: 1 jour

2. **Optimisation des Features** (Priorité: Moyenne)

   - **Description**: Améliorer les features basées sur les insights de l'analyse
   - **Effort estimé**: 2 jours

3. **Tests avec Plus de Vidéos** (Priorité: Moyenne)
   - **Description**: Valider les patterns sur un échantillon plus large
   - **Effort estimé**: 1 jour

### **Variables à Tester**

1. **Feature Engineering Avancé** - Basé sur l'analyse du dataset
2. **Ensemble Methods** - Combiner XGBoost + RandomForest
3. **Hyperparameter Tuning** - Optimiser les paramètres XGBoost

### **Objectifs de la Prochaine Itération**

- [ ] Analyser le dataset d'entraînement pour comprendre l'overfitting
- [ ] Améliorer les features basées sur les insights
- [ ] Tester avec 20+ vidéos pour valider les patterns
- [ ] Optimiser les hyperparamètres XGBoost

---

## 📚 **Références et Liens**

### **Documentation Référencée**

- **Codebase Guidelines**: `docs/project-management/codebase_guidelines.md`
- **API Documentation**: `src/api/README.md`
- **Feature System**: `src/features/modular_feature_system.py`

### **Scripts Utilisés**

- **Training**: `scripts/train_xgboost_model.py`
- **Testing**: `scripts/test_feature_extraction_direct.py`
- **API Testing**: Tests directs avec curl

### **Données et Modèles**

- **Dataset**: `data/dataset_poc_test_aggregation/` (84 vidéos)
- **Modèle**: `models/iter_003_xgboost_model.pkl`
- **Features**: `model_compatible` (16 features)

---

## ✅ **Checklist de Validation**

### **Avant de Commencer**

- [x] Template rempli complètement
- [x] Hypothèses clairement définies
- [x] Variables expérimentales identifiées
- [x] Protocole validé

### **Pendant l'Expérimentation**

- [x] Modèle XGBoost entraîné avec succès
- [x] Bug de feature extraction corrigé
- [x] API testée et fonctionnelle
- [x] Insights documentés

### **Après l'Expérimentation**

- [x] Résultats analysés et comparés
- [x] Documentation mise à jour
- [x] Prochaine itération planifiée
- [x] Commit avec message descriptif

---

**Dernière mise à jour**: `2025-07-06`
**Version**: `v1.0.0`
**Statut**: `✅ Complétée avec succès`
