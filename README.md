# Virality Chat POC

> Prédire la viralité d'une vidéo TikTok à partir de l'analyse vidéo IA et des métadonnées — POC Data Engineering, ML & Création de Contenu

---

## 🚀 Démarrage Rapide

### 1. Configuration initiale

```bash
# Exécuter le script de setup automatique
python scripts/setup_project.py

# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Configurer les clés API
cp env.template .env
# Éditer .env avec vos clés API
```

### 2. Validation de l'installation

```bash
# Vérifier que tout est correctement configuré
python scripts/validate_setup.py
```

### 3. Lancement

```bash
# Interface Streamlit
streamlit run streamlit_app/app.py

# Ou exploration avec Jupyter
jupyter notebook notebooks/01_data_exploration.ipynb
```

📖 **Guide complet** : Voir [GETTING_STARTED.md](GETTING_STARTED.md) pour les instructions détaillées

---

## 🧠 Contexte

Virality Chat POC est un projet expérimental, conçu pour démontrer qu'il est possible de prédire (et d'expliquer) la viralité d'une vidéo TikTok en combinant :

- Le scrapping automatisé de données publiques (via Apify ou équivalent)
- L'analyse structurelle avancée des vidéos par une IA multimodale (Gemini API, Google)
- Des méthodes de data engineering et machine learning accessibles (Python, pandas, scikit-learn, XGBoost…)
- Un focus fort sur la création d'insights actionnables, la transparence des features utilisées, et la possibilité de générer du contenu éducatif/documentaire autour du process

Le projet s'inscrit à la fois comme preuve de compétence en data/IA (case study pour Upwork et réseaux), et comme prototype pour un futur produit SaaS intégré à l'application EditIA.

---

## 🎯 Objectifs

- Montrer par l'exemple qu'on peut prédire la viralité de vidéos TikTok à partir de features extraites par IA
- Documenter le process de bout en bout : scrapping, feature engineering, modélisation, interprétation, automatisation minimale
- Créer du contenu de démonstration (étude de cas, tutoriels, vidéos, script TikTok/LinkedIn)
- Préparer une base technique pour industrialiser/produire un outil plus avancé (score viralité, assistant IA, intégration EditIA…)

---

## 🔗 Structure du projet

- `data/` : jeux de données scrappés, features extraites, etc.
- `notebooks/` : notebooks Jupyter/Quarto de data exploration et ML
- `src/` : scripts Python pour ETL, scrapping, ingestion, analyse
- `streamlit_app/` : démo Streamlit (ou autre interface légère)
- `reports/` : documentation, case study, résultats intermédiaires
- `README.md` : documentation générale (ce fichier)
- `docs/prd.md` : Product Requirements Document détaillant la vision, le scope, les user stories, les specs, la roadmap

---

## 🚀 Processus et Backlog

Le projet se déroule en sprints de 10 jours :

1. Collecte des données (scrapping de comptes TikTok)
2. Extraction des features (API Gemini, parsing des métadonnées)
3. Exploration & modélisation rapide (notebook ML)
4. Interprétation & génération d'insights
5. Documentation, création de contenu, partage

La méthodologie adoptée est 80-20 (priorité à l'impact, au livrable, à l'apprentissage).

---

## 📦 Livrables attendus

- 1 notebook/documentation (case study complet)
- 1 démo publique ou privée (Streamlit/vidéo/screencast)
- 1 script ou template réutilisable pour automatiser le process
- 1 (ou plusieurs) contenus vidéo/texte pour portfolio, réseaux, ou onboarding client

---

## 📝 Product Requirements Document (PRD)

Le PRD de ce projet, qui détaille la vision, la roadmap et toutes les spécifications, est disponible dans le fichier `docs/prd.md`.

Il inclut :

- L'état de l'art ("state of the art") de la viralité TikTok
- Les user stories
- L'architecture cible (MVP puis scalable)
- Les specs techniques, éthiques et data

---

## 🛠️ Stack Technique

- **Python 3.9+** : Langage principal
- **pandas, numpy** : Manipulation des données
- **scikit-learn, XGBoost** : Machine learning
- **Streamlit** : Interface utilisateur
- **Jupyter** : Notebooks d'exploration
- **Plotly** : Visualisations interactives
- **Apify** : Scraping TikTok
- **Gemini API** : Analyse vidéo IA

---

## 📚 Documentation

- [GETTING_STARTED.md](GETTING_STARTED.md) - Guide de démarrage complet
- [docs/prd.md](docs/prd.md) - Product Requirements Document
- [docs/development_guide.md](docs/development_guide.md) - Guide de développement
- `notebooks/` - Notebooks d'exploration et de modélisation

---

## 🤝 Contribution

Ce projet suit une approche de développement par phases :

1. **Phase 1** : Foundation Sprint (Jours 1-2)
2. **Phase 2** : Core MVP Sprint (Jours 3-5)
3. **Phase 3** : Enhancement Sprint (Jours 6-8)
4. **Phase 4** : Packaging Sprint (Jours 9-10)

Voir [docs/development_guide.md](docs/development_guide.md) pour plus de détails.

---

## 📬 Contact & License

Projet initié par Jason Suarez (contact : [ajouter lien/contact])  
Ce projet est open (showcase, inspiration, etc).  
Voir LICENSE pour les conditions de réutilisation.

---

Pour toute contribution, bug, question ou suggestion, ouvrez une issue ou contactez-moi directement.
