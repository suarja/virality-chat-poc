# 📚 Documentation - TikTok Virality Prediction POC

Bienvenue dans la documentation complète du POC de prédiction de viralité TikTok. Cette documentation est organisée pour faciliter la navigation et la compréhension du projet.

## 🚀 Démarrage Rapide

### **Nouveaux Utilisateurs**

- [`quick_start.md`](./quick_start.md) - Guide de démarrage rapide (5 minutes)
- [`setup_guide.md`](./setup_guide.md) - Installation et configuration complète

### **Développeurs**

- [`development_guide.md`](./development_guide.md) - Guide de développement
- [`project_structure.md`](./project_structure.md) - Structure du projet

## 📊 Documentation Scientifique

### **Itérations et Expériences**

- [`reflection/iterations/`](./reflection/iterations/) - Documentation scientifique des itérations
  - **Itération 1** : Validation de l'approche pré-publication (R² = 0.457)
  - **Gemini Features** : Méthodologie d'extraction des features IA
  - **Résultats** : 16 features pré-publication identifiées

### **Architecture et Ingénierie**

- [`reflection/architecture/`](./reflection/architecture/) - Architecture du système
- [`reflection/feature_engineering/`](./reflection/feature_engineering/) - Ingénierie des features

## 🎯 Contexte Business

### **Stratégie Produit**

- [`broader-context.md`](./broader-context.md) - Contexte global et stratégie
- [`prd.md`](./prd.md) - Product Requirements Document

### **Évaluation et Métriques**

- [`evaluation/`](./evaluation/) - Framework d'évaluation
  - [`evaluation_framework.md`](./evaluation/evaluation_framework.md) - Méthodologie d'évaluation
  - [`metrics.md`](./evaluation/metrics.md) - Métriques et KPIs

## 🔬 Analyse et Recherche

### **Recherche Académique**

- [`articles/`](./articles/) - Papers académiques sur la viralité TikTok
- [`articles/research_synthesis.md`](./articles/research_synthesis.md) - Synthèse de la recherche

### **Analyse Gemini**

- [`gemini_analysis/`](./gemini_analysis/) - Documentation de l'analyse IA
  - [`gemini_analysis.md`](./gemini_analysis/gemini_analysis.md) - Méthodologie Gemini
  - [`video-understanding.md`](./gemini_analysis/video-understanding.md) - Compréhension vidéo

## 🛠️ Guides Techniques

### **Évaluateurs et Tests**

- [`evaluators/`](./evaluators/) - Systèmes d'évaluation
  - [`ai-agents-eval.md`](./evaluators/ai-agents-eval.md) - Évaluation des agents IA
  - [`pydanticai-intro.md`](./evaluators/pydanticai-intro.md) - Introduction PydanticAI

### **Pipeline et Traitement**

- [`pipeline.md`](./pipeline.md) - Pipeline de traitement des données
- [`NEXT_STEPS.md`](./NEXT_STEPS.md) - Prochaines étapes

## 📈 Résultats et Insights

### **Résultats Itération 1**

- **Question de recherche** : Prédiction pré-publication possible ?
- **Réponse** : ✅ Oui, avec seulement 10.6% de perte de performance
- **R² Score** : 0.457 (features pré-publication) vs 0.511 (toutes features)
- **Dataset** : 8 vidéos de 3 comptes (leaelui, athenasol, loupernaut)

### **Features les Plus Importantes**

1. **audience_connection_score** (0.124) - Score Gemini
2. **hour_of_day** (0.108) - Timing de publication
3. **video_duration_optimized** (0.101) - Durée optimisée
4. **emotional_trigger_count** (0.099) - Déclencheurs émotionnels
5. **estimated_hashtag_count** (0.096) - Nombre de hashtags

### **Insights Clés**

- **Dominance Gemini** : 6/10 des features les plus importantes sont issues de l'IA
- **Corrélations fortes** : audience_connection_score (r=0.976 avec vues)
- **Timing crucial** : Les facteurs temporels sont très prédictifs
- **Validation concept** : L'approche pré-publication est scientifiquement validée

## 🎯 Cas d'Usage

### **Mobile App**

- Analyse de vidéos pour créateurs de contenu
- Prédiction de viralité avant publication
- Recommandations d'optimisation

### **Services Upwork**

- Audit de comptes TikTok
- Analyse de performance vidéo
- Rapports de viralité personnalisés

### **Building Blocks**

- Module réutilisable dans l'écosystème
- API de prédiction
- Intégration avec autres outils

## 🔍 Navigation Rapide

### **Par Rôle**

- **Développeur** : [`development_guide.md`](./development_guide.md) → [`reflection/iterations/`](./reflection/iterations/)
- **Data Scientist** : [`reflection/feature_engineering/`](./reflection/feature_engineering/) → [`evaluation/`](./evaluation/)
- **Product Manager** : [`broader-context.md`](./broader-context.md) → [`prd.md`](./prd.md)
- **Chercheur** : [`articles/research_synthesis.md`](./articles/research_synthesis.md) → [`reflection/iterations/`](./reflection/iterations/)

### **Par Objectif**

- **Comprendre le projet** : [`quick_start.md`](./quick_start.md) → [`broader-context.md`](./broader-context.md)
- **Reproduire les résultats** : [`reflection/iterations/`](./reflection/iterations/) → [`setup_guide.md`](./setup_guide.md)
- **Améliorer le modèle** : [`reflection/feature_engineering/`](./reflection/feature_engineering/) → [`evaluation/`](./evaluation/)
- **Déployer en production** : [`development_guide.md`](./development_guide.md) → [`pipeline.md`](./pipeline.md)

## 📋 Checklist Rapide

### **Pour Commencer**

- [ ] Lire [`quick_start.md`](./quick_start.md)
- [ ] Installer l'environnement avec [`setup_guide.md`](./setup_guide.md)
- [ ] Tester le pipeline avec les données existantes
- [ ] Analyser les résultats de l'itération 1

### **Pour Contribuer**

- [ ] Comprendre l'architecture dans [`reflection/architecture/`](./reflection/architecture/)
- [ ] Suivre les guidelines de [`development_guide.md`](./development_guide.md)
- [ ] Documenter les expériences dans [`reflection/iterations/`](./reflection/iterations/)
- [ ] Respecter les standards d'évaluation dans [`evaluation/`](./evaluation/)

---

_Documentation mise à jour le 5 juillet 2025 - TikTok Virality Prediction POC_
_Structure optimisée pour la navigation et la compréhension scientifique_
