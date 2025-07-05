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

#### A. Collecte de données historiques (Entraînement)

- Scrapping de comptes TikTok (Apify, etc.)
- Extraction de la liste des vidéos, stats, métadonnées
- **Objectif** : Créer un dataset d'entraînement avec features complètes

#### B. Extraction de features vidéo

- Analyse vidéo (Gemini ou autre API LMM)
- Structuration automatisée des features clés (visuels, textes, sons, rythme…)
- **Distinction** : Features pré-publication vs post-publication

#### C. Prédiction de viralité AVANT publication

- Modèle ML entraîné sur données historiques complètes
- **Prédiction** : Avec seulement features pré-publication disponibles
- Seuil viralité paramétrable (par niche, par audience)

#### D. Interface utilisateur

- Upload de vidéo par l'utilisateur
- Analyse automatique des features pré-publication
- Prédiction de viralité en temps réel
- **Valeur business** : Aide à la décision avant publication

#### E. Interprétation et recommandations

- Importance des features (feature importance)
- "Pourquoi ma vidéo a du potentiel/ne marchera pas"
- Conseils actionnables pour améliorer la viralité
- Suggestions d'optimisation avant publication

### 5.2 Fonctionnalités secondaires (stretch goals / V2)

- Historisation (time series) des performances
- Segmentation par niche, hashtag, etc.
- Intégration interface chat
- API pour usage externe ou automatisation plus poussée
- Mode "batch" sur plusieurs vidéos/comptes

---

## 6. User Stories

- En tant que créateur TikTok, je veux télécharger ma vidéo AVANT publication pour savoir si elle a du potentiel viral
- En tant qu'utilisateur, je veux recevoir des recommandations spécifiques pour améliorer ma vidéo avant de la publier
- En tant que créateur, je veux comprendre quels éléments visuels boostent mes chances de viralité
- En tant que freelance/data engineer, je veux produire un cas d'étude sur la prédiction pré-publication pour démontrer mes skills

---

## 7. Architecture & Tech Stack

- **Data** : Apify (scraping), fichiers JSON/CSV, Supabase ou Google Sheets pour stockage rapide
- **Feature extraction** : API Gemini (ou équivalent), scripts Python pour structuration
- **ML** : Jupyter/Quarto Notebooks, pandas, scikit-learn, XGBoost
- **Demo/App** : Streamlit (optionnel pour démo interactive)
- **Docs/Case study** : Markdown, Notion, Google Docs, vidéos tutos

---

## 8. Métriques de succès (KPIs)

- Prédiction "précise" (>70% accuracy) de viralité AVANT publication
- Corrélation >0.7 entre prédictions pré-publication et viralité réelle
- Interprétabilité des résultats (feature importance, explications générées)
- Interface utilisateur fonctionnelle pour upload et analyse de vidéos
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
