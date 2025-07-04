# Guide de Développement - Virality Chat POC

## 🚀 Démarrage Rapide

### 1. Configuration initiale

```bash
# Cloner le projet
git clone <repository-url>
cd virality-chat-poc

# Exécuter le script de setup
python scripts/setup_project.py

# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Configurer les clés API
cp env.template .env
# Éditer .env avec vos clés API
```

### 2. Structure du projet

```
virality-chat-poc/
├── config/                 # Configuration
│   └── settings.py
├── data/                   # Données
│   ├── raw/               # Données brutes
│   ├── processed/         # Données traitées
│   └── external/          # Données externes
├── docs/                   # Documentation
│   ├── prd.md
│   └── development_guide.md
├── notebooks/              # Notebooks Jupyter
│   ├── exploration/
│   ├── modeling/
│   └── demo/
├── src/                    # Code source
│   ├── scraping/          # Scraping TikTok
│   ├── features/          # Feature engineering
│   ├── models/            # Modèles ML
│   └── api/               # API et services
├── streamlit_app/          # Interface Streamlit
├── reports/                # Rapports et résultats
├── scripts/                # Scripts utilitaires
└── requirements.txt
```

## 📋 Workflow de Développement

### Phase 1: Foundation Sprint (Jours 1-2)

**Objectif**: Collecte et exploration des données

1. **Scraping des données**

   ```bash
   # Configurer les comptes TikTok dans config/settings.py
   # Exécuter le scraping
   python -m src.scraping.tiktok_scraper
   ```

2. **Exploration des données**

   ```bash
   # Ouvrir le notebook d'exploration
   jupyter notebook notebooks/01_data_exploration.ipynb
   ```

3. **Validation des données**
   ```python
   from src.scraping.data_validator import DataValidator
   validator = DataValidator()
   clean_data = validator.clean_dataset(raw_videos)
   ```

### Phase 2: Core MVP Sprint (Jours 3-5)

**Objectif**: Feature engineering et modèle baseline

1. **Feature engineering**

   - Extraction des features de base (vues, likes, etc.)
   - Analyse des hashtags et du texte
   - Features temporelles

2. **Modèle baseline**

   ```python
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.model_selection import train_test_split

   # Entraîner le modèle
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
   model = RandomForestClassifier(random_state=42)
   model.fit(X_train, y_train)
   ```

3. **Interface Streamlit**
   ```bash
   # Lancer l'app Streamlit
   streamlit run streamlit_app/app.py
   ```

### Phase 3: Enhancement Sprint (Jours 6-8)

**Objectif**: Amélioration du modèle et insights

1. **Feature engineering avancé**

   - Intégration Gemini API pour analyse vidéo
   - Features sémantiques et visuelles
   - Optimisation des hyperparamètres

2. **Interprétabilité**

   ```python
   import shap

   # Analyse SHAP
   explainer = shap.TreeExplainer(model)
   shap_values = explainer.shap_values(X_test)
   shap.summary_plot(shap_values, X_test)
   ```

### Phase 4: Packaging Sprint (Jours 9-10)

**Objectif**: Documentation et livraison

1. **Documentation complète**
2. **Rapport final** (Quarto/Jupyter)
3. **Vidéo de démonstration**
4. **Contenu marketing**

## 🔧 Outils et Technologies

### Stack Principal

- **Python 3.9+**: Langage principal
- **pandas**: Manipulation des données
- **scikit-learn**: Machine learning
- **Streamlit**: Interface utilisateur
- **Jupyter**: Notebooks d'exploration
- **Plotly**: Visualisations interactives

### APIs Externes

- **Apify**: Scraping TikTok
- **Gemini API**: Analyse vidéo IA
- **OpenAI** (optionnel): Backup pour l'analyse

### Outils de Développement

- **Git**: Contrôle de version
- **Black**: Formatage du code
- **pytest**: Tests unitaires
- **Quarto**: Documentation

## 📊 Métriques et Validation

### Métriques ML

- **Accuracy**: Précision globale
- **Precision/Recall**: Par classe de viralité
- **F1-Score**: Métrique équilibrée
- **ROC-AUC**: Discrimination des classes

### Métriques Business

- **Taux de prédiction correct**: >70%
- **Temps de traitement**: <5 secondes par vidéo
- **Couverture des features**: >20 features significatives

## 🚨 Bonnes Pratiques

### Code

- Suivre PEP 8 pour le style Python
- Documenter les fonctions avec docstrings
- Utiliser des noms de variables explicites
- Gérer les erreurs avec try/except

### Données

- Valider les données avant traitement
- Sauvegarder les données brutes
- Versionner les datasets traités
- Documenter les transformations

### Sécurité

- Ne jamais committer les clés API
- Utiliser .env pour les secrets
- Limiter les permissions des APIs
- Respecter les rate limits

## 🐛 Debugging

### Problèmes Courants

1. **Erreur d'import**

   ```bash
   # Vérifier le PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. **API Rate Limit**

   ```python
   import time
   time.sleep(2)  # Pause entre les requêtes
   ```

3. **Données manquantes**
   ```python
   df.fillna(method='ffill')  # Forward fill
   ```

### Logs

- Utiliser le module `logging` Python
- Niveaux: DEBUG, INFO, WARNING, ERROR
- Logs sauvegardés dans `logs/`

## 📈 Monitoring

### Métriques à suivre

- Nombre de vidéos scrappées
- Taux de succès du scraping
- Performance du modèle
- Utilisation des APIs

### Alertes

- Échec du scraping
- Dépassement des quotas API
- Chute de performance du modèle

## 🎯 Prochaines Étapes

1. **V2 Features**

   - Analyse temporelle des tendances
   - Segmentation par niche
   - API REST pour intégration

2. **Déploiement**

   - Conteneurisation Docker
   - Déploiement cloud (Heroku/Railway)
   - CI/CD avec GitHub Actions

3. **Scaling**
   - Base de données (PostgreSQL)
   - Cache Redis
   - Queue de traitement (Celery)
