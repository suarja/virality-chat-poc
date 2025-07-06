# 🔬 ITER_003: XGBoost Model Optimization

## 📋 **Informations de Base**

- **ID Itération**: ITER_003
- **Date de Création**: 2025-07-06
- **Durée Estimée**: 1-2 heures
- **Complexité**: Level 2 (Simple Enhancement)
- **Statut**: En Planification

---

## 🎯 **Hypothèse Principale**

### **Hypothèse Testée**

> "XGBoost améliore la généralisation par rapport à RandomForest sur le même dataset de 84 vidéos"

### **Justification Scientifique**

- **ITER_002** a montré un R² de 0.855 avec RandomForest mais un overfitting
- **XGBoost** est généralement plus robuste pour la généralisation
- Test d'une seule variable (algorithme) pour isoler l'effet du modèle

### **Prédiction**

- **R² attendu**: 0.875+ (amélioration de 2%+)
- **Généralisation**: Prédictions plus cohérentes sur nouvelles vidéos
- **Latence**: < 2 secondes (maintenue)

---

## 📊 **Variables Expérimentales**

### **Variables Constantes**

| Variable       | Valeur                  | Justification                     |
| -------------- | ----------------------- | --------------------------------- |
| **Dataset**    | 84 vidéos               | Même dataset qu'ITER_002 (agrégé) |
| **Features**   | 16 features             | Même feature set (comprehensive)  |
| **Validation** | Cross-validation 5-fold | Même protocole de validation      |
| **Target**     | log(view_count)         | Même transformation de la cible   |

### **Variables Manipulées**

| Variable            | Valeur Testée     | Valeur Contrôle       | Impact sur le Code               | Justification           |
| ------------------- | ----------------- | --------------------- | -------------------------------- | ----------------------- |
| **Algorithme**      | XGBoost           | RandomForest          | `scripts/train_xgboost_model.py` | Test de généralisation  |
| **Hyperparamètres** | XGBoost optimisés | RandomForest baseline | Nouveau script                   | Optimisation spécifique |
| **Modèle Version**  | iter_003          | iter_002              | `src/api/ml_model.py`            | Versioning des modèles  |

---

## 🔬 **Protocole Expérimental**

### **Phase 1: Préparation (15 min)**

```bash
# Vérifier que ITER_002 est complet
ls -la data/dataset_iter_002/features/aggregated_comprehensive.csv

# Vérifier les modèles existants
ls -la models/
```

**Objectifs**:

- [ ] Dataset ITER_002 disponible (84 vidéos)
- [ ] Modèles ITER_002 sauvegardés
- [ ] Environnement prêt pour XGBoost

### **Phase 2: Entraînement XGBoost (30 min)**

```bash
# Entraîner le modèle XGBoost
python3 scripts/train_xgboost_model.py
```

**Paramètres XGBoost**:

- **n_estimators**: 200
- **max_depth**: 6
- **learning_rate**: 0.1
- **subsample**: 0.8
- **colsample_bytree**: 0.8

### **Phase 3: Comparaison (15 min)**

```bash
# Comparer les performances
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_iter_002 --feature-set comprehensive --save-model --model-name iter_003_xgboost
```

**Métriques de Comparaison**:

- **R² Score** (objectif: > 0.875)
- **MAE** (objectif: < 0.3)
- **RMSE** (objectif: < 0.4)
- **Généralisation** (test sur nouvelles vidéos)

### **Phase 4: Test API (15 min)**

```bash
# Tester avec XGBoost
export ML_MODEL_TYPE=xgboost
export ML_MODEL_VERSION=iter_003
uvicorn src.api.main:app --reload --port 8000

# Test de prédiction
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@david_sepahan/video/7516571262638984470", "use_cache": false}'
```

### **Phase 5: Documentation (15 min)**

- [ ] Mettre à jour ITER_003 avec résultats
- [ ] Documenter les améliorations MLOps
- [ ] Planifier ITER_004

---

## 📈 **Métriques de Succès**

### **Objectifs Techniques**

| Métrique        | ITER_002 (RF) | ITER_003 (XGB) | Objectif | Statut |
| --------------- | ------------- | -------------- | -------- | ------ |
| **R² Score**    | 0.855         | ?              | > 0.875  | ⏳     |
| **MAE**         | ?             | ?              | < 0.3    | ⏳     |
| **RMSE**        | ?             | ?              | < 0.4    | ⏳     |
| **Latence API** | < 2s          | ?              | < 2s     | ⏳     |

### **Objectifs de Généralisation**

- [ ] Prédiction cohérente sur vidéo non-virale
- [ ] Score < 0.5 pour vidéo avec 1,442 vues
- [ ] Amélioration de la robustesse

---

## 🔧 **Gestion MLOps**

### **Variables d'Environnement**

```bash
# Utiliser RandomForest (par défaut)
export ML_MODEL_TYPE=randomforest
export ML_MODEL_VERSION=iter_002

# Utiliser XGBoost
export ML_MODEL_TYPE=xgboost
export ML_MODEL_VERSION=iter_003
```

### **Fichiers de Modèles**

- `models/iter_002_model.pkl` - RandomForest ITER_002
- `models/iter_003_xgboost_model.pkl` - XGBoost ITER_003
- `models/iter_003_xgboost_metrics.json` - Métriques XGBoost

### **Changement de Modèle**

```python
# Dans src/api/ml_model.py
self.model_type = os.getenv("ML_MODEL_TYPE", "randomforest")
self.model_version = os.getenv("ML_MODEL_VERSION", "iter_002")
```

---

## 🎬 **Contenu Éducatif Planifié**

### **Vidéo TikTok**

- **Titre**: "XGBoost vs RandomForest: quel modèle prédit mieux la viralité?"
- **Durée**: 45 secondes
- **Thème**: Comparaison d'algorithmes ML
- **Hashtags**: #MachineLearning #XGBoost #RandomForest #DataScience

### **Documentation**

- [ ] Mise à jour du glossaire ML
- [ ] Explication des différences XGBoost vs RandomForest
- [ ] Guide de choix d'algorithme

---

## 🔄 **Itération Suivante (ITER_004)**

### **Hypothèses Possibles**

1. **Feature Engineering**: Nouvelles features basées sur insights ITER_003
2. **Hyperparameter Tuning**: Optimisation avancée des paramètres
3. **Ensemble Methods**: Combinaison RandomForest + XGBoost

### **Variables à Tester**

- **Feature Engineering**: Nouvelles features contextuelles
- **Hyperparameters**: Grid search pour XGBoost
- **Ensemble**: Voting regressor

---

## 📚 **Références et Liens**

### **Documentation Référencée**

- **Architecture MLOps**: `docs/iterations/architecture_mlops.md`
- **ITER_002**: `docs/iterations/ITER_002_feature_optimization.md`
- **Template**: `docs/iterations/template_iteration.md`

### **Scripts Utilisés**

- **XGBoost Training**: `scripts/train_xgboost_model.py`
- **Analyse Données**: `scripts/analyze_existing_data.py`
- **API Testing**: Tests manuels avec curl

### **Données et Modèles**

- **Dataset**: `data/dataset_iter_002/features/aggregated_comprehensive.csv`
- **Modèle RF**: `models/iter_002_model.pkl`
- **Modèle XGB**: `models/iter_003_xgboost_model.pkl`

---

## ✅ **Checklist de Validation**

### **Avant de Commencer**

- [ ] Dataset ITER_002 disponible (84 vidéos)
- [ ] Script XGBoost créé et testé
- [ ] Variables d'environnement documentées
- [ ] Protocole validé

### **Pendant l'Expérimentation**

- [ ] XGBoost entraîné avec succès
- [ ] Comparaison RandomForest vs XGBoost
- [ ] Tests API avec nouveau modèle
- [ ] Métriques enregistrées

### **Après l'Expérimentation**

- [ ] Résultats analysés et documentés
- [ ] Modèle XGBoost sauvegardé
- [ ] API configurée pour changement de modèle
- [ ] Prochaine itération planifiée

---

**Créé le**: `2025-07-06`
**Dernière mise à jour**: `2025-07-06`
**Version**: `v1.0.0`
