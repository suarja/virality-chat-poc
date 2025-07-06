# 🏗️ Architecture MLOps - Variables Expérimentales et Changements

## 🎯 **Vue d'Ensemble de l'Architecture**

Notre POC suit une architecture MLOps simple mais robuste, permettant de changer facilement les modèles et features sans casser le système.

### **Architecture Actuelle**

```
📊 Data Pipeline
├── 🕷️ Scraping (Apify TikTok)
├── 🔧 Feature Extraction (Modular System)
├── 🤖 ML Model (RandomForest)
└── 🚀 API (FastAPI)
```

---

## 🔧 **Variables Expérimentales et leur Impact**

### **1. 🎯 Feature Sets (Variables Manipulées)**

#### **Feature Sets Disponibles**

```python
# Dans src/features/modular_feature_system.py
FEATURE_SETS = {
    "metadata": MetadataFeatureSet(),           # 20 features
    "gemini_basic": GeminiBasicFeatureSet(),    # 14 features
    "visual_granular": VisualGranularFeatureSet(), # 34 features
    "comprehensive": ComprehensiveFeatureSet(),  # 34 features
    "model_compatible": ModelCompatibleFeatureSet() # 16 features ⭐
}
```

#### **Comment Changer de Feature Set**

```bash
# Dans les scripts
python3 scripts/analyze_existing_data.py --feature-set comprehensive
python3 scripts/analyze_existing_data.py --feature-set model_compatible

# Dans l'API (automatique)
# L'API utilise toujours ModelCompatibleFeatureSet (16 features)
```

#### **Impact sur le Code**

- **Feature Count**: Varie selon le set (16-34 features)
- **Model Compatibility**: Seul `model_compatible` fonctionne avec l'API
- **Performance**: Plus de features = plus de temps de calcul
- **R² Score**: Peut varier selon les features

### **2. 🤖 Modèles ML (Variables Manipulées)**

#### **Modèles Actuels**

```python
# Dans models/
├── pre_publication_virality_model.pkl    # RandomForest (R² = 0.457)
└── baseline_virality_model.pkl           # Backup model
```

#### **Comment Changer de Modèle**

```python
# Dans src/api/ml_model.py - Ligne 25
self.model_path = project_root / "models/pre_publication_virality_model.pkl"

# Pour changer de modèle, modifier cette ligne :
self.model_path = project_root / "models/xgboost_virality_model.pkl"
```

#### **Modèles à Tester (Planifiés)**

| Modèle             | Avantages              | Inconvénients         | Effort      |
| ------------------ | ---------------------- | --------------------- | ----------- |
| **RandomForest**   | Robuste, interprétable | Performance limitée   | ✅ Actuel   |
| **XGBoost**        | Meilleure performance  | Plus complexe         | 🔄 ITER_003 |
| **LightGBM**       | Rapide, efficace       | Moins interprétable   | 🔄 ITER_004 |
| **Neural Network** | Très flexible          | Overfitting, complexe | 🔄 ITER_005 |

### **3. 📊 Dataset Size (Variables Manipulées)**

#### **Tailles de Dataset Testées**

```python
DATASET_SIZES = {
    "ITER_001": 8 vidéos,      # POC initial
    "ITER_002": 150 vidéos,    # Scaling (planifié)
    "ITER_003": 500 vidéos,    # Production (planifié)
}
```

#### **Impact sur les Métriques**

| Dataset Size   | R² Score | MAE   | RMSE  | Temps Entraînement |
| -------------- | -------- | ----- | ----- | ------------------ |
| **8 vidéos**   | 0.457    | 0.23  | 0.34  | 2s                 |
| **150 vidéos** | ~0.6     | ~0.18 | ~0.25 | 30s                |
| **500 vidéos** | ~0.7     | ~0.15 | ~0.20 | 2min               |

---

## 🔄 **Workflow de Changement de Modèle**

### **Étape 1: Préparer le Nouveau Modèle**

```bash
# 1. Entraîner le nouveau modèle
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_training --feature-set model_compatible --save-model --model-type xgboost

# 2. Sauvegarder avec un nom descriptif
mv models/pre_publication_virality_model.pkl models/xgboost_virality_model_v1.pkl
```

### **Étape 2: Modifier l'API**

```python
# Dans src/api/ml_model.py - Ligne 25
# AVANT
self.model_path = project_root / "models/pre_publication_virality_model.pkl"

# APRÈS
self.model_path = project_root / "models/xgboost_virality_model_v1.pkl"
```

### **Étape 3: Tester**

```bash
# Test local
python3 scripts/test_api_fixed.py

# Test avec nouvelle URL
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@swarecito/video/7505706702050823446"}'
```

### **Étape 4: Déployer**

```bash
# Commit et déploiement
git add src/api/ml_model.py models/xgboost_virality_model_v1.pkl
git commit -m "feat: switch to XGBoost model (R²=0.612)"
railway up
```

---

## 🔧 **Workflow de Changement de Features**

### **Étape 1: Créer un Nouveau Feature Set**

```python
# Dans src/features/modular_feature_system.py
class EnhancedFeatureSet(BaseFeatureSet):
    def __init__(self):
        super().__init__(
            name="enhanced",
            description="Enhanced features with new insights"
        )
        self.features = [
            # 16 features compatibles avec le modèle
            'duration', 'hashtag_count', 'estimated_hashtag_count',
            # ... ajouter nouvelles features
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        # Logique d'extraction
        pass
```

### **Étape 2: Enregistrer le Feature Set**

```python
# Dans la fonction _register_default_sets()
def _register_default_sets(self):
    self.register_feature_set(MetadataFeatureSet())
    self.register_feature_set(GeminiBasicFeatureSet())
    self.register_feature_set(EnhancedFeatureSet())  # Nouveau
```

### **Étape 3: Tester avec le Nouveau Feature Set**

```bash
# Test d'extraction
python3 scripts/analyze_existing_data.py --feature-set enhanced

# Test API (si compatible)
# L'API utilise toujours ModelCompatibleFeatureSet
```

---

## 📊 **Métriques Standardisées (Variables Constantes)**

### **Métriques Toujours Calculées**

```python
STANDARD_METRICS = {
    "r2_score": "Coefficient de détermination (0-1)",
    "mae": "Mean Absolute Error (plus bas = mieux)",
    "rmse": "Root Mean Square Error (plus bas = mieux)",
    "feature_importance": "Top 5 features importantes",
    "latency": "Temps de prédiction (objectif < 2s)"
}
```

### **Seuils de Performance**

| Métrique     | Seuil Acceptable | Seuil Bon | Seuil Excellent |
| ------------ | ---------------- | --------- | --------------- |
| **R² Score** | > 0.4            | > 0.6     | > 0.8           |
| **MAE**      | < 0.3            | < 0.2     | < 0.1           |
| **RMSE**     | < 0.4            | < 0.3     | < 0.2           |
| **Latency**  | < 3s             | < 2s      | < 1s            |

### **Feature Importance (Toujours Calculée)**

```python
# Format standard
feature_importance = {
    "feature_1": 0.124,  # 12.4% d'importance
    "feature_2": 0.108,  # 10.8% d'importance
    # ... top 5 features
}
```

---

## 🎯 **Variables par Itération**

### **ITER_001: POC Initial** ✅

```python
VARIABLES_ITER_001 = {
    "dataset_size": 8,
    "model": "RandomForest",
    "feature_set": "ModelCompatibleFeatureSet",
    "r2_score": 0.457,
    "status": "COMPLETED"
}
```

### **ITER_002: Dataset Scaling** 🔄

```python
VARIABLES_ITER_002 = {
    "dataset_size": 150,  # 8 → 150
    "model": "RandomForest",  # Même modèle
    "feature_set": "ModelCompatibleFeatureSet",  # Même features
    "expected_r2": "> 0.6",
    "status": "PLANNED"
}
```

### **ITER_003: Model Optimization** 🔄

```python
VARIABLES_ITER_003 = {
    "dataset_size": 150,
    "model": "XGBoost",  # RandomForest → XGBoost
    "feature_set": "ModelCompatibleFeatureSet",
    "expected_r2": "> 0.65",
    "status": "PLANNED"
}
```

### **ITER_004: Feature Engineering** 🔄

```python
VARIABLES_ITER_004 = {
    "dataset_size": 150,
    "model": "XGBoost",
    "feature_set": "EnhancedFeatureSet",  # Nouvelles features
    "expected_r2": "> 0.7",
    "status": "PLANNED"
}
```

---

## 🚨 **Points d'Attention**

### **1. Compatibilité Modèle-Features**

```python
# ❌ PROBLÈME: Features mismatch
model_expects = 16 features
features_provided = 34 features  # Erreur!

# ✅ SOLUTION: Toujours utiliser ModelCompatibleFeatureSet pour l'API
```

### **2. Sauvegarde des Modèles**

```bash
# ✅ Toujours sauvegarder avant changement
cp models/pre_publication_virality_model.pkl models/backup_randomforest.pkl

# ✅ Versionner les modèles
mv models/xgboost_virality_model.pkl models/xgboost_virality_model_v1.pkl
```

### **3. Tests de Régression**

```bash
# ✅ Tester avant déploiement
python3 scripts/test_api_fixed.py

# ✅ Vérifier les métriques
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -d '{"url": "test_url"}' | jq '.prediction.r2_score'
```

---

## 📚 **Documentation Perdue (Reflections)**

### **Contenu Supprimé Important**

Le dossier `docs/reflection/` contenait :

- **Feature Engineering Analysis** - Analyse détaillée des 34 features
- **Model Comparison** - Comparaison RandomForest vs XGBoost vs autres
- **Architecture Decisions** - Décisions d'architecture importantes

### **Recréation Nécessaire**

```bash
# À recréer dans docs/iterations/
├── feature_engineering_analysis.md
├── model_comparison_guide.md
├── architecture_decisions.md
└── experimental_results.md
```

---

## 🎯 **Checklist de Changement**

### **Avant de Changer de Modèle**

- [ ] Sauvegarder le modèle actuel
- [ ] Tester le nouveau modèle localement
- [ ] Vérifier la compatibilité des features
- [ ] Documenter les métriques de performance

### **Avant de Changer de Features**

- [ ] Vérifier la compatibilité avec le modèle
- [ ] Tester l'extraction des nouvelles features
- [ ] Valider les performances
- [ ] Mettre à jour la documentation

### **Avant de Déployer**

- [ ] Tests de régression complets
- [ ] Validation des métriques
- [ ] Documentation mise à jour
- [ ] Rollback plan préparé

---

**Document créé le**: `2025-07-06`
**Dernière mise à jour**: `2025-07-06`
**Version**: `v1.0.0`
**Responsable**: Équipe POC TikTok Virality
