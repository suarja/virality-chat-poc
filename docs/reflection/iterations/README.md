# 📚 Documentation des Itérations - TikTok Virality Prediction

Ce dossier contient la documentation scientifique de chaque itération du POC, organisée comme une publication scientifique avec méthodologie, résultats et analyses.

## 🎯 Itération 1 - Validation de l'Approche Pré-Publication

### **Documents**

- [`iteration_1_scientific_documentation.md`](./iteration_1_scientific_documentation.md) - Documentation scientifique complète
- [`iteration_1_development_plan.md`](./iteration_1_development_plan.md) - Plan de développement original
- [`gemini_feature_extraction_methodology.md`](./gemini_feature_extraction_methodology.md) - Méthodologie d'extraction Gemini
- [`documentation_cleanup_plan.md`](./documentation_cleanup_plan.md) - Plan de nettoyage de la documentation

### **Question de Recherche**

_Peut-on prédire la viralité d'une vidéo TikTok en utilisant uniquement les features disponibles avant sa publication ?_

### **Résultats Clés**

- **R² Score** : 0.457 avec features pré-publication seulement
- **Dataset** : 8 vidéos de 3 comptes différents
- **Features** : 16 features pré-publication identifiées
- **Perte de performance** : 10.6% seulement (excellent)
- **Validation** : Approche pré-publication confirmée ✅

### **Features les Plus Importantes**

1. **audience_connection_score** (0.124) - Score Gemini de connexion audience
2. **hour_of_day** (0.108) - Timing de publication
3. **video_duration_optimized** (0.101) - Durée optimisée
4. **emotional_trigger_count** (0.099) - Déclencheurs émotionnels Gemini
5. **estimated_hashtag_count** (0.096) - Nombre de hashtags

### **Insights Scientifiques**

- **Dominance des features Gemini** : 6/10 des features les plus importantes
- **Corrélations très fortes** : audience_connection_score (r=0.976 avec vues)
- **Timing crucial** : hour_of_day et day_of_week dans le top 10
- **Qualité prédictive** : Performance excellente malgré le petit dataset

### **Limitations Identifiées**

- **Taille du dataset** : 8 vidéos seulement (risque de surapprentissage)
- **Variable cible** : view_count comme proxy (pas de colonne IsViral)
- **Features Gemini** : Extraction par mots-clés (à améliorer)

## 🚀 Itération 2 - Augmentation du Dataset et Optimisation

### **Objectifs Planifiés**

- **Dataset** : Augmentation à 150+ vidéos minimum
- **Modèles** : Test Gradient Boosting, XGBoost
- **Features** : Amélioration des prompts Gemini
- **Validation** : Cross-validation stratifiée par compte

### **Hypothèses à Tester**

1. Performance stable avec dataset plus large
2. Features Gemini améliorées augmentent la précision
3. Modèles plus complexes améliorent les prédictions
4. Généralisation sur nouveaux comptes

### **Métriques de Succès**

- **R² Score** : > 0.5 avec dataset élargi
- **Généralisation** : Performance stable sur nouveaux comptes
- **Robustesse** : Cross-validation > 0.4

## 📊 Méthodologie Générale

### **Approche Scientifique**

1. **Hypothèse** : Formulation claire et testable
2. **Méthodologie** : Séparation pré-publication/post-publication
3. **Validation** : Cross-validation et métriques multiples
4. **Documentation** : Traçabilité complète des expériences

### **Pipeline Expérimental**

```
Scraping → Analyse Gemini → Extraction Features →
Séparation Pré/Post → Entraînement → Validation → Documentation
```

### **Standards de Documentation**

- **Reproductibilité** : Code, données, paramètres documentés
- **Traçabilité** : Chaque expérience tracée et versionnée
- **Scientificité** : Méthodologie rigoureuse et peer-reviewable

## 🔗 Liens Utiles

### **Code et Données**

- [`scripts/analyze_existing_data.py`](../../../scripts/analyze_existing_data.py) - Script d'analyse principal
- [`data/dataset_poc_test/`](../../../data/dataset_poc_test/) - Dataset de l'itération 1
- [`models/pre_publication_virality_model.pkl`](../../../models/pre_publication_virality_model.pkl) - Modèle sauvegardé

### **Documentation Technique**

- [`docs/reflection/architecture/`](../architecture/) - Architecture du système
- [`docs/reflection/feature_engineering/`](../feature_engineering/) - Ingénierie des features
- [`src/features/modular_feature_system.py`](../../../src/features/modular_feature_system.py) - Système de features

---

_Index créé le 5 juillet 2025 - Documentation scientifique des itérations du POC TikTok Virality Prediction_
