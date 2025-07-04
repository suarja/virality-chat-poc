# PRD – Virality Chat POC

## 1. Résumé Exécutif

Virality Chat POC vise à prouver la faisabilité de la prédiction et de l'explication de la viralité de vidéos TikTok en combinant :

- Le scrapping automatisé des comptes TikTok
- L'analyse vidéo avancée via une IA multimodale (Gemini)
- Des algos de machine learning 80/20, interprétables
- Une documentation exemplaire (case study, contenu pédagogique)

Le tout, dans une logique "MVP utile + démonstrateur pour portfolio Upwork/LinkedIn".

---

## 2. Objectifs

### Objectif principal

Prédire la viralité (et expliquer les facteurs clés) d'une vidéo TikTok à partir de features extraites automatiquement (data TikTok + analyse vidéo IA).

### Objectifs secondaires

- Industrialiser la collecte et le processing des données pour accélérer la R&D et le prototypage
- Documenter chaque étape pour créer un case study réutilisable (content & personal branding)
- Préparer les briques techniques pour une future industrialisation ou intégration EditIA

---

## 3. Problème Utilisateur

> "Aujourd'hui, il n'existe pas d'outil simple pour comprendre ou prédire ce qui va rendre une vidéo TikTok virale, ni pour expliquer 'pourquoi ça marche ou pas' de manière personnalisée pour chaque compte ou niche."

---

## 4. Cibles et Personas

- Créateurs TikTok solo ou PME voulant faire grandir leur audience
- Consultants/agents/marketeurs qui veulent identifier les leviers de viralité pour leurs clients
- Développeurs/data engineers curieux d'appliquer la data science à la viralité des contenus sociaux
- Toi-même, pour démontrer ta compétence en data, IA et automatisation sur Upwork/LinkedIn

---

## 5. Scope Fonctionnel (MVP/POC)

### 5.1 Fonctionnalités principales

#### A. Collecte de données

- Scrapping de comptes TikTok (Apify, etc.)
- Extraction de la liste des vidéos, stats, métadonnées

#### B. Extraction de features vidéo

- Analyse vidéo (Gemini ou autre API LMM)
- Structuration automatisée des features clés (visuels, textes, sons, rythme…)

#### C. Prédiction de viralité

- Modèle ML rapide (RandomForest, XGBoost…)
- Seuil viralité paramétrable (par niche, par audience)

#### D. Interprétation/explanation

- Importance des features (feature importance)
- "Pourquoi ma vidéo marche/ne marche pas" (explanation automatique)

#### E. Génération d'insights

- Conseils actionnables, suggestions d'amélioration
- Export des résultats, cas d'étude (template)

### 5.2 Fonctionnalités secondaires (stretch goals / V2)

- Historisation (time series) des performances
- Segmentation par niche, hashtag, etc.
- Intégration interface chat
- API pour usage externe ou automatisation plus poussée
- Mode "batch" sur plusieurs vidéos/comptes

---

## 6. User Stories

- En tant qu'utilisateur je veux soumettre le lien d'une vidéo pour savoir si elle peut devenir virale (et pourquoi)
- En tant que créateur je veux comprendre ce qui booste/limite mes performances pour améliorer mes prochaines vidéos
- En tant que freelance/data engineer je veux produire un cas d'étude sur ce sujet pour démontrer mes skills

---

## 7. Architecture & Tech Stack

- **Data** : Apify (scraping), fichiers JSON/CSV, Supabase ou Google Sheets pour stockage rapide
- **Feature extraction** : API Gemini (ou équivalent), scripts Python pour structuration
- **ML** : Jupyter/Quarto Notebooks, pandas, scikit-learn, XGBoost
- **Demo/App** : Streamlit (optionnel pour démo interactive)
- **Docs/Case study** : Markdown, Notion, Google Docs, vidéos tutos

---

## 8. Métriques de succès (KPIs)

- Prédiction "précise" (>70% accuracy) sur la viralité sur un batch test
- Interprétabilité des résultats (feature importance, explications générées)
- Livrable "case study" documenté (notebook, vidéo, doc)
- Capacité à enrichir le portfolio Upwork, LinkedIn, TikTok avec un vrai use-case

---

## 9. Roadmap & Sprints

### Sprint 1 (Jours 1–5)

- Scrapper plusieurs comptes TikTok (data brute)
- Organiser/structurer les features (Gemini + parsing)
- Premiers notebooks d'exploration

### Sprint 2 (Jours 6–10)

- Training du modèle prédictif
- Interprétation et explication des résultats
- Génération de rapports (notebook, template)
- Création de contenu (case study, vidéo TikTok/LinkedIn)

---

## 10. Spécifications Data & Features

### Features de base

- Vues, likes, partages, commentaires
- Durée, hashtags, date de publication
- Topic (niche), score d'engagement

### Features avancées (via IA)

- Type de plan, nombre de cuts, rapidité du rythme
- Présence humaine/animaux, thématiques visuelles
- Mots-clés détectés (OCR/ASR)

---

## 11. Risques & Limitations

- Accès API Gemini limité/coûteux (pas de mise en public "live" possible)
- Prédiction brute : à valider sur des batchs externes (généralisation limitée)
- Scope MVP volontairement restreint : no-code/no-productisation tant que la démo n'est pas validée

---

## 12. Annexes

- Bibliographie, articles de référence (ex : Slapping Cats, Bopping Heads and Oreo Shakes: Understanding Indicators of Virality in TikTok Short Videos, 2023)
- Inspirations/outils existants (vidIQ, TikBuddy, Spark Ads TikTok…)
- README principal

---

_Document évolutif._  
Ce PRD sera mis à jour à chaque étape majeure (livraison, exploration, changement de scope).
