# 🧪 Scripts de Test - TikTok Virality Prediction

Ce dossier contient les scripts de test pour valider le pipeline, l'API et les modules du projet.

## 📋 Liste des scripts principaux

- **test_model_final.py** :

  - Test minimal global (smoke test)
  - Vérifie que le modèle ML et l'API fonctionnent correctement (scores normalisés, pas d'erreur de features)
  - Usage : `python3 scripts/test_model_final.py`

- **test_model_diagnostics.py** :

  - Test avancé (analyse + simulation)
  - Vérifie la correction des erreurs de features, la cohérence des scores, la stabilité de l'API
  - Usage : `python3 scripts/test_model_diagnostics.py`

- **test_pipeline_minimal.py** :

  - Teste le pipeline complet (scraping, Gemini, features, ML) sur 1 compte, 2 vidéos max
  - Usage : `python3 scripts/test_pipeline_minimal.py`

- **test_gemini.py** :

  - Teste le service Gemini en isolation (hors pipeline)
  - Usage : `python3 scripts/test_gemini.py`

- **test_video_scraping.py** :
  - Teste le scraping brut d'une vidéo TikTok via Apify
  - Usage : `python3 scripts/test_video_scraping.py`

## 🗃️ Scripts archivés

Les scripts suivants sont conservés dans `scripts/archive/` pour référence historique ou debug avancé, mais **ne sont plus maintenus** :

- `test_simulation_endpoint.py`, `test_real_pipeline.py`, `test_real_tiktok_scraper.py`, `test_tiktok_url_analysis.py` : anciens tests API/pipeline, remplacés par les nouveaux tests ci-dessus
- `scraper_demo.py`, `scraper.js` : démos de scraping, non maintenues
- `deploy_railway.py`, `ddd_deploy.py` : scripts de déploiement/DDD historiques

**Politique d'archivage** :

- Tout script obsolète, redondant ou non compatible avec la nouvelle architecture est déplacé dans `archive/` avec un commentaire explicite en tête de fichier.
- Pour tout nouveau test, partir des scripts principaux ci-dessus.

## 🚀 Conseils

- Toujours commencer par `test_model_final.py` pour valider l'installation.
- Utiliser `test_pipeline_minimal.py` pour valider le pipeline complet.
- Utiliser `test_model_diagnostics.py` pour un diagnostic avancé.
- Utiliser `test_gemini.py` pour tester Gemini seul.
- Utiliser `test_video_scraping.py` pour valider le scraping brut ou debug Apify.
