# 🚀 POC Quick Start - Virality Prediction

## 🎯 Objectif

Valider rapidement l'idée de prédiction de viralité TikTok en testant le pipeline end-to-end et en créant un modèle baseline.

## ⚡ Démarrage Immédiat (5 minutes)

### 1. Test Rapide du Pipeline (avec agrégation automatique)

```bash
# Test avec 6 vidéos seulement (agrégation automatique incluse)
python3 scripts/test_pipeline_with_aggregation.py
```

**Ce test va :**

- ✅ Scraper 3 vidéos de 1 compte
- ✅ Analyser avec Gemini AI
- ✅ Extraire les features
- ✅ **Agréger automatiquement** les données
- ✅ Vérifier que tout fonctionne

### 2. Analyse des Données Existantes

```bash
# Si tu as déjà des données, analyser sans relancer le pipeline
python3 scripts/check_poc_data.py --dataset-dir data/dataset_poc_test --aggregate

# Ou analyser avec dépendances (si installées)
pip install pandas numpy matplotlib scikit-learn
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --save-model
```

**Cette analyse va :**

- 📊 Analyser la distribution des données
- 🔗 Calculer les corrélations
- 🤖 Créer un modèle baseline
- 💡 Générer des insights

## 📋 Plan Complet (3 semaines)

### **Semaine 1 : Validation Rapide**

```bash
# Jour 1-2 : Test pipeline avec agrégation automatique
python3 scripts/test_pipeline_with_aggregation.py

# Jour 3-4 : Analyse et modèle baseline
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test_aggregation --save-model

# Jour 5 : Évaluation et planification
```

### **Semaine 2 : Développement du Modèle**

```bash
# Jour 1-2 : Dataset d'entraînement (150 vidéos)
python3 scripts/run_pipeline.py --dataset poc_training --batch-size 3 --videos-per-account 15 --max-total-videos 150 --feature-system modular --feature-set comprehensive

# Jour 3-4 : Modèle avancé
python3 scripts/train_advanced_model.py --dataset-dir data/dataset_poc_training

# Jour 5 : API de prédiction
python3 scripts/create_prediction_api.py
```

### **Semaine 3 : Démo et Validation**

```bash
# Jour 1-2 : Démo Upwork
python3 scripts/generate_virality_report.py --video-urls urls.txt

# Jour 3-4 : Intégration app mobile
# (Code JavaScript/React Native)

# Jour 5 : Tests et optimisations
```

## 🎯 Métriques de Succès

### **Techniques (Phase 1)**

- ✅ **Pipeline fonctionnel** end-to-end
- ✅ **Agrégation automatique** des features
- ✅ **R² Score > 0.4** sur validation croisée
- ✅ **Features extraites** correctement
- ✅ **Données valides** et cohérentes

### **Business (Phase 3)**

- ✅ **Démo Upwork** prête
- ✅ **Rapport PDF** professionnel
- ✅ **API fonctionnelle** pour l'app
- ✅ **Insights actionnables** générés

## 🚨 Dépannage Rapide

### **Erreur de dépendances**

```bash
pip install pandas numpy matplotlib scikit-learn seaborn
```

### **Erreur de pipeline**

```bash
# Vérifier les logs
tail -f logs/pipeline_poc_test_aggregation.log

# Vérifier les erreurs
tail -f logs/errors.log
```

### **Erreur d'API Gemini**

```bash
# Vérifier la clé API
echo $GEMINI_API_KEY

# Tester l'API
python3 scripts/test_gemini.py
```

### **Fichier agrégé manquant**

```bash
# Agrégation manuelle si nécessaire
python3 scripts/aggregate_features.py --dataset-dir data/dataset_poc_test --feature-set comprehensive --show-stats
```

## 📊 Structure des Données

```
data/dataset_poc_test_aggregation/
├── batch_20241201_143022.json    # Données scrapées
├── gemini_analysis/              # Analyses Gemini
│   └── @account_name/
│       └── 20241201/
│           └── video_*.json
└── features/                     # Features extraites
    ├── @account_name_features_comprehensive.csv  # Par compte
    └── aggregated_comprehensive.csv              # Agrégé automatiquement
```

## 🎯 Prochaines Étapes

### **Si le test rapide réussit :**

1. **Augmenter le dataset** à 150 vidéos
2. **Optimiser le modèle** (Gradient Boosting, XGBoost)
3. **Créer l'API** de prédiction
4. **Préparer la démo** Upwork

### **Si le test échoue :**

1. **Analyser les erreurs** dans les logs
2. **Corriger les problèmes** identifiés
3. **Retester** avec moins de vidéos
4. **Considérer un pivot** vers Account Analyzer

## 💡 Tips pour le POC

### **Optimisation des Coûts**

- Commencer avec **6 vidéos** seulement
- Utiliser **batch-size=1** pour éviter les erreurs
- **Tester localement** avant de scaler

### **Optimisation du Temps**

- **Agrégation automatique** incluse dans le pipeline
- **Paralléliser** les phases quand possible
- **Cacher les résultats** pour éviter les re-calculs
- **Logs détaillés** pour le debugging

### **Qualité des Données**

- **Valider** chaque phase avant de continuer
- **Vérifier** la cohérence des features
- **Nettoyer** les données aberrantes

## 🎯 Commandes de Test Rapide

```bash
# Test minimal avec agrégation automatique (5 minutes)
python3 scripts/test_pipeline_with_aggregation.py

# Test avec analyse des données existantes (2 minutes)
python3 scripts/check_poc_data.py --dataset-dir data/dataset_poc_test --aggregate

# Test complet (30 minutes)
python3 scripts/run_pipeline.py --dataset poc_validation --batch-size 2 --videos-per-account 10 --max-total-videos 40 --feature-system modular --feature-set comprehensive
```

## 🔧 Scripts Disponibles

### **Pipeline et Tests**

- `scripts/test_pipeline_with_aggregation.py` - Test complet avec agrégation automatique
- `scripts/test_poc_pipeline.py` - Test basique du pipeline
- `scripts/run_pipeline.py` - Pipeline principal

### **Analyse des Données**

- `scripts/check_poc_data.py` - Vérification simple sans dépendances
- `scripts/analyze_existing_data.py` - Analyse complète avec ML
- `scripts/aggregate_features.py` - Agrégation manuelle si nécessaire

### **Utilitaires**

- `scripts/analyze_poc_data.py` - Analyse avec visualisations (dépendances requises)

**Prêt à commencer ?** 🚀

```bash
# Commencer maintenant
python3 scripts/test_pipeline_with_aggregation.py
```
