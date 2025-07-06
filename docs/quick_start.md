# 🚀 POC Quick Start - Virality Prediction

## 🎯 Objectif

Valider rapidement l'idée de prédiction de viralité TikTok en testant le pipeline end-to-end et en créant un modèle baseline.

## ⚡ Démarrage Immédiat (5 minutes)

### 1. Test Rapide du Pipeline (avec agrégation automatique)

```bash
# Test avec 2 vidéos seulement (agrégation automatique incluse)
python3 scripts/test_pipeline_minimal.py
```

**Ce test va :**

- ✅ Scraper 2 vidéos de 1 compte
- ✅ Analyser avec Gemini AI
- ✅ Extraire les features
- ✅ **Agréger automatiquement** les données
- ✅ Vérifier que tout fonctionne
- ✅ Tester les endpoints API

### 2. Analyse des Données Existantes

```bash
# Analyser les données existantes sans relancer le pipeline
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive

# Sauvegarder le modèle entraîné
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive --save-model

# Analyser avec différents feature sets
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set metadata
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set visual_granular
```

**Cette analyse va :**

- 📊 Analyser la distribution des données
- 🔗 Calculer les corrélations
- 🤖 Créer un modèle baseline
- 💡 Générer des insights

## 🚀 API Usage - Production Ready

### **📊 Analysis Endpoints (Post-Publication Data)**

#### Analyze Existing Video

```bash
# Analyser une vidéo existante avec données réelles
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true
  }'
```

**Use Case**: "Pourquoi cette vidéo a-t-elle été virale?"

- ✅ Score de viralité actuel (0.75 = 75% de potentiel viral)
- ✅ Données d'engagement réelles (vues, likes, commentaires)
- ✅ Analyse d'importance des features
- ✅ Recommandations spécifiques d'amélioration

#### Analyze Profile

```bash
# Analyser plusieurs vidéos d'un profil
curl -X POST "http://localhost:8000/analyze-tiktok-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "swarecito",
    "max_videos": 10,
    "use_cache": true
  }'
```

**Use Case**: "Qu'est-ce qui rend les vidéos de ce créateur virales?"

### **🎯 Simulation Endpoints (Pre-Publication Scenarios)**

#### Simulate Publication Scenarios

```bash
# Simuler différents scénarios de publication
curl -X POST "http://localhost:8000/simulate-virality" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true,
    "scenarios": [
      {
        "name": "Publication Matin",
        "description": "Publier à 9h le lundi",
        "publication_hour": 9,
        "publication_day": "monday",
        "hashtags": ["fyp", "viral", "trending"],
        "engagement_multiplier": 1.2
      },
      {
        "name": "Publication Soir",
        "description": "Publier à 20h le vendredi",
        "publication_hour": 20,
        "publication_day": "friday",
        "hashtags": ["fyp", "comedy", "funny"],
        "engagement_multiplier": 1.5
      }
    ],
    "simulation_count": 5
  }'
```

**Use Case**: "Quand devrais-je publier cette vidéo pour maximiser la viralité?"

**⚠️ Important**: Cette simulation est PRE-PUBLICATION et n'utilise PAS les données d'engagement réelles. L'URL de la vidéo sert uniquement à l'analyse du contenu (durée, format, etc.), pas aux vues/likes/commentaires.

- ✅ Meilleur moment de publication recommandé
- ✅ Combinaisons de hashtags optimales
- ✅ Amélioration de viralité attendue
- ✅ Suggestions d'optimisation de contenu
- ✅ Support du cache pour l'efficacité
- ✅ Simulation de scénarios sans biais des données réelles

## 🔄 Analysis vs Simulation: Quand Utiliser Quoi?

### **📊 Utilisez Analysis Endpoints Quand:**

- ✅ Vous avez une vidéo TikTok existante
- ✅ Vous voulez comprendre pourquoi elle a été virale (ou pas)
- ✅ Vous voulez analyser des données d'engagement réelles
- ✅ Vous faites de la recherche concurrentielle

**Exemple**: "Pourquoi la vidéo ChatGPT de @swarecito a-t-elle eu 53k vues?"

### **🎯 Utilisez Simulation Endpoints Quand:**

- ✅ Vous planifiez de publier une vidéo
- ✅ Vous voulez optimiser le timing de publication
- ✅ Vous voulez tester différentes stratégies de hashtags
- ✅ Vous voulez prédire la viralité avant publication

**Exemple**: "Quand devrais-je publier ma nouvelle vidéo pour maximiser la viralité?"

## 📈 Interprétation des Scores

### **Score de Viralité (0-1)**

- **0.0-0.3**: Potentiel viral faible
- **0.3-0.6**: Potentiel viral modéré
- **0.6-0.8**: Potentiel viral élevé
- **0.8-1.0**: Potentiel viral très élevé

### **Score de Confiance (0-1)**

- **0.0-0.5**: Confiance faible dans la prédiction
- **0.5-0.8**: Confiance modérée
- **0.8-1.0**: Confiance élevée

### **Score R² (0-1)**

- **0.457**: Notre modèle explique 45.7% de la variance virale
- **Standard industriel**: 0.4+ est considéré comme bon pour la prédiction sur réseaux sociaux

## 📋 Plan Complet (3 semaines)

### **Semaine 1 : Validation Rapide**

```bash
# Jour 1-2 : Test pipeline avec agrégation automatique
python3 scripts/test_pipeline_with_aggregation.py

# Jour 3-4 : Analyse et modèle baseline
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive --save-model

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
pip install pandas numpy matplotlib scikit-learn seaborn google-generativeai
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
echo $GOOGLE_API_KEY

# Tester le service Gemini
python3 scripts/test_gemini.py

# Vérifier l'architecture des services
ls -la src/services/
```

### **Erreur de Features ML**

```bash
# Tester l'API après correction des features
python3 scripts/test_api_fixed.py

# Vérifier que l'API utilise les bonnes features (16 au lieu de 34)
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@swarecito/video/7505706702050823446", "use_cache": false}' | jq '.prediction.virality_score'
```

### **Fichier agrégé manquant**

```bash
# Agrégation manuelle si nécessaire
python3 scripts/aggregate_features.py --dataset-dir data/dataset_poc_test --feature-set comprehensive --show-stats

# Ou analyser directement les features existantes
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive
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
# Test minimal avec agrégation automatique (2 minutes)
python3 scripts/test_pipeline_minimal.py

# Test avec analyse des données existantes (2 minutes)
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive

# Test complet (30 minutes)
python3 scripts/run_pipeline.py --dataset poc_validation --batch-size 2 --videos-per-account 10 --max-total-videos 40 --feature-set comprehensive
```

## 🔧 Scripts Disponibles

### **Pipeline et Tests**

- `scripts/test_pipeline_minimal.py` - Test complet avec agrégation automatique (recommandé)
- `scripts/run_pipeline.py` - Pipeline principal

### **Analyse des Données**

- `scripts/analyze_existing_data.py` - Analyse complète avec ML (recommandé)
- `scripts/aggregate_features.py` - Agrégation manuelle si nécessaire

### **Services Réutilisables**

- `src/services/gemini_service.py` - Service d'analyse Gemini centralisé
- `src/services/README.md` - Documentation de l'architecture des services

**Note**: Le script d'analyse transforme automatiquement les dates en features numériques (heure, jour de semaine, etc.) pour optimiser les performances du modèle.

## 📚 Documentation API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **README API**: `src/api/README.md`
- **Health Check**: `http://localhost:8000/health`

**Prêt à commencer ?** 🚀

```bash
# Commencer maintenant
python3 scripts/test_pipeline_minimal.py
```
