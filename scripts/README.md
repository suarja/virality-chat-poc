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

## 🧹 Nettoyage

- Les scripts intermédiaires/doublons ont été supprimés ou fusionnés.
- Pour des tests personnalisés, partez de `test_model_diagnostics.py` ou `test_pipeline_minimal.py`.

## 🚀 Conseils

- Toujours commencer par `test_model_final.py` pour valider l'installation.
- Utiliser `test_pipeline_minimal.py` pour valider le pipeline complet.
- Utiliser `test_model_diagnostics.py` pour un diagnostic avancé.
- Utiliser `test_gemini.py` pour tester Gemini seul.
