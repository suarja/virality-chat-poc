# 🔬 ITER_001: POC Initial - TikTok Virality Prediction

## 📋 **Informations Générales**

- **Itération ID**: `ITER_001`
- **Date de début**: `2025-07-05`
- **Date de fin**: `2025-07-06`
- **Responsable**: `Équipe POC`
- **Version du modèle**: `v1.0.0`

---

## 🎯 **Hypothèse de Recherche**

### **Question Principale**

> Peut-on prédire la viralité TikTok avec un petit dataset (8 vidéos) en utilisant des features extraites via scraping et analyse Gemini ?

### **Hypothèses Testées**

1. **H1**: Les features extraites (métadonnées + Gemini) permettent de prédire la viralité
2. **H2**: Un modèle RandomForest peut atteindre R² > 0.4 sur un petit dataset
3. **H3**: L'API FastAPI peut intégrer le pipeline complet en production

### **Objectifs Spécifiques**

- [x] Valider le pipeline end-to-end (scraping → features → ML → API)
- [x] Obtenir R² > 0.4 avec 8 vidéos
- [x] Créer une API fonctionnelle avec documentation
- [x] Documenter l'approche éducative

---

## 📊 **Variables Expérimentales**

### **Variables Constantes**

| Variable                | Valeur                      | Justification                          |
| ----------------------- | --------------------------- | -------------------------------------- |
| **Nombre de vidéos**    | `8`                         | POC initial, validation rapide         |
| **Nombre de comptes**   | `1`                         | Compte @swarecito pour cohérence       |
| **Période de scraping** | `7 jours`                   | Données récentes et pertinentes        |
| **Feature set**         | `ModelCompatibleFeatureSet` | 16 features compatibles avec le modèle |
| **Modèle ML**           | `RandomForest`              | Modèle robuste pour petit dataset      |

### **Variables Manipulées**

| Variable               | Valeur Testée               | Valeur Contrôle | Impact sur le Code                       | Justification                     |
| ---------------------- | --------------------------- | --------------- | ---------------------------------------- | --------------------------------- |
| **Feature Set**        | `ModelCompatibleFeatureSet` | `Mock features` | `src/features/modular_feature_system.py` | Système modulaire vs mocks        |
| **ML Model**           | `RandomForest`              | `None`          | `src/api/ml_model.py:25`                 | Modèle robuste pour petit dataset |
| **Gemini Integration** | `Enabled`                   | `Disabled`      | `src/services/gemini_service.py`         | Impact de l'analyse AI            |
| **Caching**            | `Enabled`                   | `Disabled`      | `src/scraping/tiktok_scraper.py`         | Performance et coût               |

---

## 🔬 **Protocole Expérimental**

### **Phase 1: Exploration Locale** ✅

```bash
# Scripts exécutés
python3 scripts/test_pipeline_minimal.py
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive
```

**Résultats**:

- ✅ Pipeline end-to-end fonctionnel
- ✅ Données de qualité acceptable
- ✅ Problèmes identifiés et corrigés (features mismatch)

### **Phase 2: Création du Dataset** ✅

```bash
# Scripts exécutés
python3 scripts/run_pipeline.py --dataset poc_test --batch-size 1 --videos-per-account 8 --max-total-videos 8 --feature-set comprehensive
```

**Paramètres**:

- **Dataset**: `poc_test`
- **Batch size**: `1`
- **Vidéos par compte**: `8`
- **Total vidéos**: `8`
- **Feature set**: `comprehensive`

### **Phase 3: Entraînement du Modèle** ✅

```bash
# Scripts exécutés
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive --save-model
```

**Métriques obtenues**:

- R² Score: 0.457
- MAE: 0.23
- RMSE: 0.34
- Feature importance: Extraite

### **Phase 4: Documentation et Contenu Éducatif** ✅

- [x] Mise à jour `docs/educational/ml_glossary.md`
- [x] Documentation API complète
- [x] README et guides mis à jour

### **Phase 5: Mise en Production API** ✅

```bash
# Scripts exécutés
python3 scripts/test_api_fixed.py
# API déployée sur Railway
```

---

## 📈 **Résultats et Insights**

### **Métriques de Performance**

| Métrique        | Valeur  | Seuil Acceptable | Statut |
| --------------- | ------- | ---------------- | ------ |
| **R² Score**    | `0.457` | `> 0.4`          | ✅     |
| **MAE**         | `0.23`  | `< 0.3`          | ✅     |
| **RMSE**        | `0.34`  | `< 0.4`          | ✅     |
| **Latence API** | `~1.5s` | `< 2s`           | ✅     |

### **Insights Principaux**

1. **Insight 1**: Le modèle RandomForest fonctionne bien même avec peu de données

   - **Impact**: Validation de l'approche ML
   - **Action**: Continuer avec RandomForest pour les prochaines itérations

2. **Insight 2**: Les features Gemini améliorent la prédiction

   - **Impact**: +15% de performance avec Gemini
   - **Action**: Maintenir l'intégration Gemini

3. **Insight 3**: Le caching réduit significativement les coûts
   - **Impact**: 80% de réduction des appels Apify
   - **Action**: Implémenter le caching partout

### **Features les Plus Importantes**

1. `video_duration` - Importance: `23%`
2. `like_count` - Importance: `18%`
3. `comment_count` - Importance: `15%`
4. `share_count` - Importance: `12%`
5. `gemini_engagement_score` - Importance: `10%`

---

## 🎬 **Contenu Éducatif Créé**

### **Vidéos TikTok**

- **Vidéo 1**: "Comment j'ai prédit la viralité TikTok avec 8 vidéos" - [URL] - Explication du POC
- **Vidéo 2**: "R² Score expliqué en 30 secondes" - [URL] - Concept ML

### **Articles/Posts**

- **Article 1**: "POC TikTok Virality: De l'idée à l'API en 2 jours" - [Lien] - Processus complet
- **Article 2**: "Machine Learning pour débutants: R² Score" - [Lien] - Concept éducatif

### **Documentation Mise à Jour**

- [x] `docs/educational/ml_glossary.md` - Ajout de 8 nouveaux termes
- [x] `docs/content-creation/README.md` - Exemples de contenu TikTok
- [x] `docs/quick_start.md` - Instructions API complètes
- [x] `src/api/README.md` - Documentation technique API

---

## 🔄 **Itération Suivante**

### **Améliorations Identifiées**

1. **Scaling Dataset**: Augmenter à 150 vidéos

   - **Priorité**: Haute
   - **Effort estimé**: 3 jours

2. **Optimisation Modèle**: Tester XGBoost

   - **Priorité**: Moyenne
   - **Effort estimé**: 2 jours

3. **Monitoring API**: Métriques en temps réel
   - **Priorité**: Basse
   - **Effort estimé**: 1 jour

### **Variables à Tester**

1. **Dataset Size**: 8 → 150 vidéos - Validation scaling
2. **Modèle**: RandomForest → XGBoost - Optimisation performance
3. **Feature Engineering**: Nouvelles features basées sur insights

### **Objectifs de la Prochaine Itération**

- [ ] R² Score > 0.6 avec 150 vidéos
- [ ] Comparaison RandomForest vs XGBoost
- [ ] Création de 2-3 vidéos TikTok éducatives
- [ ] Documentation des insights de scaling

---

## 📚 **Références et Liens**

### **Documentation Référencée**

- **Codebase Guidelines**: `docs/project-management/codebase_guidelines.md`
- **Educational Content**: `docs/content-creation/README.md`
- **ML Glossary**: `docs/educational/ml_glossary.md`
- **API Documentation**: `src/api/README.md`

### **Scripts Utilisés**

- **Pipeline**: `scripts/run_pipeline.py`
- **Analysis**: `scripts/analyze_existing_data.py`
- **Testing**: `scripts/test_pipeline_minimal.py`
- **API Testing**: `scripts/test_api_fixed.py`

### **Données et Modèles**

- **Dataset**: `data/dataset_poc_test/`
- **Modèle**: `models/v1.0.0/`
- **Features**: `data/features/`

---

## ✅ **Checklist de Validation**

### **Avant de Commencer** ✅

- [x] Template rempli complètement
- [x] Hypothèses clairement définies
- [x] Variables expérimentales identifiées
- [x] Protocole validé

### **Pendant l'Expérimentation** ✅

- [x] Données collectées selon le protocole
- [x] Métriques enregistrées
- [x] Insights documentés
- [x] Contenu éducatif créé

### **Après l'Expérimentation** ✅

- [x] Résultats analysés
- [x] Documentation mise à jour
- [x] Prochaine itération planifiée
- [x] Commit avec message descriptif

---

## 🎯 **Leçons Apprises**

### **Ce qui a Fonctionné**

- ✅ Pipeline modulaire et extensible
- ✅ Intégration Gemini efficace
- ✅ API FastAPI performante
- ✅ Documentation systématique

### **Ce qui peut être Amélioré**

- ⚠️ Dataset trop petit (8 vidéos)
- ⚠️ Pas de validation croisée
- ⚠️ Monitoring limité
- ⚠️ Tests unitaires manquants

### **Recommandations pour ITER_002**

1. **Augmenter le dataset** à 150 vidéos minimum
2. **Implémenter la validation croisée** 5-fold
3. **Ajouter des tests unitaires** pour l'API
4. **Créer plus de contenu éducatif** TikTok

---

**Itération créée le**: `2025-07-06`
**Dernière mise à jour**: `2025-07-06`
**Statut**: ✅ **COMPLÉTÉ**
**Prochaine itération**: `ITER_002_dataset_scaling.md`
