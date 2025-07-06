# 🔬 Itérations Scientifiques - TikTok Virality Prediction

## 🎯 **Approche Méthodologique**

Ce dossier contient toutes les itérations scientifiques de notre POC TikTok Virality Prediction. Chaque itération suit une approche structurée et reproductible, documentant systématiquement les hypothèses, protocoles, résultats et insights.

### **Philosophie**
> _"Chaque itération est une expérience scientifique complète, de l'hypothèse à la production"_

---

## 📋 **Structure des Itérations**

### **Template Principal**
- **`template_iteration.md`** - Template scientifique pour chaque itération

### **Itérations Réalisées**
- **`ITER_001_initial_poc.md`** - POC initial avec 8 vidéos (R² = 0.457)
- **`ITER_002_dataset_scaling.md`** - Scaling à 150 vidéos (en cours)
- **`ITER_003_model_optimization.md`** - Optimisation du modèle (planifié)

---

## 🔬 **Protocole Standard**

### **Phase 1: Exploration Locale** 🧪
```bash
# Validation du pipeline
python3 scripts/test_pipeline_minimal.py

# Analyse des données existantes
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive
```

**Objectifs**:
- ✅ Valider le pipeline end-to-end
- ✅ Vérifier la qualité des données
- ✅ Identifier les problèmes potentiels

### **Phase 2: Création du Dataset** 📊
```bash
# Pipeline principal
python3 scripts/run_pipeline.py --dataset poc_training --batch-size 3 --videos-per-account 15 --max-total-videos 150 --feature-set comprehensive
```

**Variables Constantes**:
- **Feature set**: `comprehensive` (16 features)
- **Modèle**: `RandomForest` (baseline)
- **Validation**: Cross-validation 5-fold

### **Phase 3: Entraînement du Modèle** 🤖
```bash
# Analyse et entraînement
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_training --feature-set comprehensive --save-model
```

**Métriques Clés**:
- **R² Score** (objectif: > 0.6)
- **MAE** (objectif: < 0.3)
- **RMSE** (objectif: < 0.4)
- **Feature Importance** (top 5)

### **Phase 4: Documentation Éducative** 📚
- [ ] Mettre à jour `docs/educational/ml_glossary.md`
- [ ] Créer contenu TikTok éducatif
- [ ] Documenter les insights dans `docs/content-creation/`

### **Phase 5: Mise en Production** 🚀
```bash
# Tests API
python3 scripts/test_api_fixed.py

# Déploiement Railway
railway up
```

---

## 📊 **Variables Expérimentales**

### **Variables Constantes (Toutes Itérations)**
| Variable | Valeur | Justification |
|----------|--------|---------------|
| **Feature Extraction** | `ModularFeatureSystem` | Système modulaire et extensible |
| **Scraping** | `Apify TikTok Scraper` | Données réelles et fiables |
| **API Framework** | `FastAPI` | Performance et documentation auto |
| **Déploiement** | `Railway` | Simplicité et scalabilité |

### **Variables Manipulées (Par Itération)**
| Itération | Dataset Size | Modèle | Feature Set | Objectif |
|-----------|--------------|--------|-------------|----------|
| **ITER_001** | 8 vidéos | RandomForest | Comprehensive | Validation POC |
| **ITER_002** | 150 vidéos | RandomForest | Comprehensive | Scaling dataset |
| **ITER_003** | 150 vidéos | XGBoost | Enhanced | Optimisation modèle |

---

## 🎬 **Contenu Éducatif par Itération**

### **Format TikTok**
- **Durée**: 30-60 secondes
- **Format**: Vertical (9:16)
- **Style**: Éducatif + Entertainment
- **Hashtags**: #MachineLearning #TikTok #DataScience #Virality

### **Thèmes par Itération**
- **ITER_001**: "Comment prédire la viralité TikTok avec 8 vidéos"
- **ITER_002**: "Scaling à 150 vidéos: les défis du dataset"
- **ITER_003**: "XGBoost vs RandomForest: quel modèle gagne?"

---

## 📈 **Métriques de Succès**

### **Techniques**
- **R² Score**: > 0.6 (vs 0.457 actuel)
- **Latence API**: < 2 secondes
- **Uptime**: > 99.5%
- **Feature Importance**: Top 5 identifiés

### **Éducatives**
- **Vidéos créées**: 1-2 par itération
- **Glossary updates**: 5-10 nouveaux termes
- **Documentation**: 100% à jour
- **Insights partagés**: 3-5 par itération

### **Business**
- **API utilisable**: Production ready
- **Contenu viral**: Engagement > 1000 vues
- **Communauté**: Croissance audience éducative

---

## 🔄 **Workflow d'Itération**

### **Avant de Commencer**
1. **Copier le template**: `cp template_iteration.md ITER_XXX_description.md`
2. **Définir les hypothèses**: Basées sur les insights précédents
3. **Planifier les variables**: Constantes vs manipulées
4. **Valider le protocole**: Avec l'équipe

### **Pendant l'Itération**
1. **Suivre le protocole**: Phase par phase
2. **Documenter les résultats**: Métriques et insights
3. **Créer le contenu**: TikTok et documentation
4. **Tester l'API**: Validation end-to-end

### **Après l'Itération**
1. **Analyser les résultats**: Comparaison avec objectifs
2. **Mettre à jour la documentation**: Tous les fichiers concernés
3. **Planifier la suivante**: Basée sur les insights
4. **Commiter avec message clair**: "feat: ITER_XXX - [description]"

---

## 📚 **Documentation Référencée**

### **Guidelines**
- **Codebase Guidelines**: `docs/project-management/codebase_guidelines.md`
- **API Documentation**: `src/api/README.md`
- **Quick Start**: `docs/quick_start.md`

### **Contenu Éducatif**
- **ML Glossary**: `docs/educational/ml_glossary.md`
- **Content Creation**: `docs/content-creation/README.md`
- **Learning Roadmap**: `docs/educational/learning_roadmap.md`

### **Scripts et Pipeline**
- **Pipeline Principal**: `scripts/run_pipeline.py`
- **Analyse Données**: `scripts/analyze_existing_data.py`
- **Tests API**: `scripts/test_api_fixed.py`

---

## ✅ **Checklist de Qualité**

### **Avant de Commencer une Itération**
- [ ] Template rempli complètement
- [ ] Hypothèses clairement définies
- [ ] Variables expérimentales identifiées
- [ ] Protocole validé avec l'équipe
- [ ] Ressources nécessaires disponibles

### **Pendant l'Itération**
- [ ] Données collectées selon le protocole
- [ ] Métriques enregistrées systématiquement
- [ ] Insights documentés en temps réel
- [ ] Contenu éducatif créé
- [ ] Tests API validés

### **Après l'Itération**
- [ ] Résultats analysés et comparés
- [ ] Documentation mise à jour (tous les fichiers)
- [ ] Prochaine itération planifiée
- [ ] Commit avec message descriptif
- [ ] Contenu partagé sur TikTok

---

## 🎯 **Prochaines Itérations Planifiées**

### **ITER_002: Dataset Scaling** (En cours)
- **Objectif**: Scaling à 150 vidéos
- **Hypothèse**: Plus de données = meilleur modèle
- **Durée estimée**: 1 semaine

### **ITER_003: Model Optimization** (Planifié)
- **Objectif**: Tester XGBoost vs RandomForest
- **Hypothèse**: XGBoost > RandomForest
- **Durée estimée**: 1 semaine

### **ITER_004: Feature Engineering** (Planifié)
- **Objectif**: Nouvelles features basées sur insights
- **Hypothèse**: Features contextuelles importantes
- **Durée estimée**: 1 semaine

---

**Dernière mise à jour**: `2025-07-06`
**Version**: `v1.0.0`
**Responsable**: Équipe POC TikTok Virality 