# 🚀 Guide de Démarrage - Virality Chat POC

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python 3.9+** installé
- **Git** installé
- Un compte **Apify** (pour le scraping TikTok)
- Une clé API **Google Gemini** (pour l'analyse vidéo)

## 📋 Étapes de Configuration

### Étape 1 : Cloner et Configurer le Projet

```bash
# Si pas encore fait, cloner le projet
git clone <your-repo-url>
cd virality-chat-poc

# Exécuter le script de setup automatique
python scripts/setup_project.py
```

**✅ Validation** : Vous devriez voir :

```
✓ Created directory: data/raw
✓ Created directory: data/processed
✓ Virtual environment created
✓ Requirements installed
✓ Created .env file from template
```

### Étape 2 : Activer l'Environnement Virtuel

```bash
# Sur macOS/Linux
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

**✅ Validation** : Votre terminal devrait afficher `(venv)` au début de la ligne.

### Étape 3 : Configurer les Clés API

```bash
# Éditer le fichier .env
nano .env  # ou votre éditeur préféré
```

Remplir avec vos vraies clés API :

```env
APIFY_API_TOKEN=votre_token_apify_ici
GEMINI_API_KEY=votre_cle_gemini_ici
DEBUG=True
LOG_LEVEL=INFO
```

**✅ Validation** : Vérifier que le fichier `.env` existe et contient vos clés.

### Étape 4 : Tester l'Installation

```bash
# Tester l'import des modules
python -c "from src.scraping.tiktok_scraper import TikTokScraper; print('✅ Import OK')"

# Tester Jupyter
jupyter --version

# Tester Streamlit
streamlit --version
```

**✅ Validation** : Toutes les commandes doivent s'exécuter sans erreur.

## 🎯 Démarrage par Phase

### Phase 1 : Exploration des Données (Jours 1-2)

#### 1.1 Configurer les Comptes TikTok à Analyser

```bash
# Éditer le fichier de configuration
nano config/settings.py
```

Ajouter les comptes TikTok dans la liste `TIKTOK_ACCOUNTS` :

```python
TIKTOK_ACCOUNTS = [
    "@username1",
    "@username2",
    "@username3"
]
```

#### 1.2 Lancer le Scraping (Test)

```bash
# Créer un script de test
python -c "
from src.scraping.tiktok_scraper import TikTokScraper
scraper = TikTokScraper()
print('✅ Scraper initialisé avec succès')
"
```

**✅ Validation** : Le scraper doit s'initialiser sans erreur.

#### 1.3 Ouvrir le Notebook d'Exploration

```bash
# Lancer Jupyter
jupyter notebook notebooks/01_data_exploration.ipynb
```

**✅ Validation** : Le notebook doit s'ouvrir dans votre navigateur.

### Phase 2 : Interface de Démonstration

#### 2.1 Lancer l'Application Streamlit

```bash
# Depuis la racine du projet
streamlit run streamlit_app/app.py
```

**✅ Validation** : L'application doit s'ouvrir sur `http://localhost:8501`

#### 2.2 Vérifier les Pages

- 🏠 **Accueil** : Présentation du projet
- 📊 **Exploration** : Métriques des données
- 🤖 **Prédiction** : Interface de prédiction
- 📈 **Insights** : Recommandations

**✅ Validation** : Toutes les pages doivent se charger correctement.

## 🔧 Commandes Utiles

### Gestion de l'Environnement

```bash
# Activer l'environnement
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Désactiver l'environnement
deactivate

# Installer de nouvelles dépendances
pip install package_name
pip freeze > requirements.txt  # Mettre à jour requirements.txt
```

### Développement

```bash
# Formater le code
black src/
black streamlit_app/

# Lancer les tests (quand ils existent)
pytest tests/

# Lancer Jupyter Lab (alternative à Jupyter Notebook)
jupyter lab
```

### Git et Versioning

```bash
# Voir le statut
git status

# Ajouter les modifications
git add .

# Commit avec message descriptif
git commit -m "✨ Add feature: description"

# Pousser vers le repo
git push origin main
```

## 🚨 Résolution des Problèmes Courants

### Problème 1 : Erreur d'Import

**Symptôme** : `ModuleNotFoundError: No module named 'src'`

**Solution** :

```bash
# Ajouter le dossier src au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Ou dans le code Python
import sys
sys.path.append('src')
```

### Problème 2 : Clés API Manquantes

**Symptôme** : `ValueError: Apify API token is required`

**Solution** :

1. Vérifier que le fichier `.env` existe
2. Vérifier que les clés API sont correctement remplies
3. Redémarrer l'environnement Python

### Problème 3 : Dépendances Manquantes

**Symptôme** : `ModuleNotFoundError: No module named 'package'`

**Solution** :

```bash
# Réinstaller les dépendances
pip install -r requirements.txt

# Ou installer le package manquant
pip install package_name
```

### Problème 4 : Port Streamlit Occupé

**Symptôme** : `Port 8501 is already in use`

**Solution** :

```bash
# Utiliser un autre port
streamlit run streamlit_app/app.py --server.port 8502

# Ou tuer le processus existant
lsof -ti:8501 | xargs kill -9
```

## 📊 Vérification de l'État du Projet

### Checklist de Démarrage

- [ ] Environnement virtuel activé
- [ ] Dépendances installées
- [ ] Clés API configurées
- [ ] Modules Python importables
- [ ] Jupyter fonctionne
- [ ] Streamlit fonctionne
- [ ] Git configuré

### Commande de Diagnostic

```bash
# Script de diagnostic complet
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import pandas as pd
    print('✅ pandas OK')
except ImportError:
    print('❌ pandas manquant')

try:
    from src.scraping.tiktok_scraper import TikTokScraper
    print('✅ TikTokScraper OK')
except ImportError as e:
    print(f'❌ TikTokScraper: {e}')

try:
    import streamlit as st
    print('✅ streamlit OK')
except ImportError:
    print('❌ streamlit manquant')

import os
if os.path.exists('.env'):
    print('✅ .env file exists')
else:
    print('❌ .env file missing')
"
```

## 🎯 Prochaines Étapes

Une fois le setup terminé :

1. **Commencer par l'exploration** : `jupyter notebook notebooks/01_data_exploration.ipynb`
2. **Tester le scraping** : Scraper quelques vidéos test
3. **Valider les données** : Vérifier la qualité des données collectées
4. **Itérer** : Améliorer progressivement chaque composant

## 📞 Support

En cas de problème :

1. Vérifier cette documentation
2. Consulter les logs dans `logs/`
3. Vérifier les issues GitHub
4. Créer une nouvelle issue avec les détails de l'erreur

---

**Prêt à commencer ? Suivez les étapes ci-dessus et validez chaque étape avant de passer à la suivante !** 🚀
