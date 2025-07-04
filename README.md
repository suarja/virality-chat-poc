# Virality Chat POC

> Prédire la viralité d'une vidéo TikTok à partir de l'analyse vidéo IA et des métadonnées — POC Data Engineering, ML & Création de Contenu

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

## 📬 Contact & License

Projet initié par Jason Suarez (contact : [ajouter lien/contact])  
Ce projet est open (showcase, inspiration, etc).  
Voir LICENSE pour les conditions de réutilisation.

---

Pour toute contribution, bug, question ou suggestion, ouvrez une issue ou contactez-moi directement.
