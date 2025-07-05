# 🧠 Espace de Réflexion - Viralité TikTok

## 📋 Objectif de ce Document

Ce document sert d'espace de réflexion pour :

- **Formuler des hypothèses** basées sur la recherche
- **Détailler chaque phase** de développement
- **Expliquer le "pourquoi"** de chaque feature
- **Définir des systèmes de scoring** quantifiables
- **Structurer notre approche** méthodologique

---

## 📚 Documentation Disponible

### 1. **Articles de Recherche** ✅

- **"Understanding Indicators of Virality in TikTok Short Videos"** (2021) - **CLÉ**
- **"Analyzing User Engagement with TikTok's Short Videos"**
- **"Trick and Please: Mixed-Method Study on TikTok Algorithm"**
- **"An Empirical Investigation of Personalization Factors on TikTok"**
- **"Analysis on the Douyin (TikTok) Mania"**
- **"Monolith Real Time Recommendation System"**

### 2. **Synthèse de Recherche** ✅

- `docs/articles/research_synthesis.md` - Synthèse des 6 articles
- Insights clés sur les indicateurs de viralité
- Seuils et métriques recommandés

### 3. **Documentation Technique** ✅

- `docs/features_tracking.md` - État d'avancement des features
- `docs/feature_engineering.md` - Architecture des features
- `docs/prd.md` - Product Requirements Document

### 4. **Recherche Internet** 🔍

- Articles récents sur la viralité TikTok
- Études de cas de créateurs viraux
- Analyses d'algorithmes TikTok

---

## 🎯 Hypothèses de Travail

### **Hypothèse Principale**

> "La viralité d'une vidéo TikTok peut être prédite avec précision en combinant des métadonnées quantitatives (vues, engagement) avec des analyses qualitatives visuelles et temporelles."

### **Hypothèses Secondaires**

#### **H1 : Features Visuelles Critiques**

- **Hypothèse** : Les features visuelles (close-ups, zooms, transitions) sont des prédicteurs forts de viralité
- **Source** : "Understanding Indicators of Virality in TikTok Short Videos"
- **Validation** : Analyse comparative vidéos virales vs non-virales

#### **H2 : Timing Optimal**

- **Hypothèse** : Le timing de publication (heure/jour) influence significativement la viralité
- **Source** : Synthèse de recherche + études de cas
- **Validation** : Analyse temporelle des performances

#### **H3 : Engagement Précoce**

- **Hypothèse** : La vitesse d'engagement dans les premières heures prédit la viralité
- **Source** : Articles sur l'algorithme TikTok
- **Validation** : Métriques de velocity et rétention

#### **H4 : Cohérence de Contenu**

- **Hypothèse** : La cohérence visuelle et thématique avec le compte augmente la viralité
- **Source** : Études sur la personnalisation
- **Validation** : Analyse de similarité avec historique

---

## 🏗️ Phases Détaillées

### **Phase 1 : Features Statistiques Avancées** (Actuelle)

#### **1.1 Métadonnées TikTok Brutes**

```python
BASIC_METADATA = {
    'view_count': int,           # Métrique primaire
    'like_count': int,           # Engagement direct
    'comment_count': int,        # Engagement social
    'share_count': int,          # Viralité pure
    'video_duration': float,     # Optimisation longueur
    'hashtags_count': int,       # Optimisation SEO
    'description_length': int,   # Optimisation description
}
```

**Pourquoi ?**

- **Base quantitative** : Métriques objectives et mesurables
- **Validation historique** : Données prouvées par la recherche
- **Facilité d'extraction** : Disponibles via API TikTok

#### **1.2 Métriques d'Engagement Calculées**

```python
ENGAGEMENT_METRICS = {
    'engagement_rate': float,    # (likes+comments+shares)/views
    'like_rate': float,         # likes/views
    'comment_rate': float,      # comments/views
    'share_rate': float,        # shares/views
    'virality_ratio': float,    # shares/(likes+comments)
}
```

**Pourquoi ?**

- **Normalisation** : Comparaison équitable entre vidéos
- **Indicateurs de qualité** : Engagement > vues brutes
- **Prédicteurs validés** : Corrélés avec la viralité

#### **1.3 Features Temporelles**

```python
TEMPORAL_FEATURES = {
    'publish_hour': int,        # 0-23
    'publish_day_of_week': int, # 0-6
    'is_weekend': bool,         # Weekend vs semaine
    'is_business_hours': bool,  # 9h-17h
    'is_peak_hours': bool,      # 18h-22h (audience française)
    'days_since_posted': int,   # Âge de la vidéo
}
```

**Pourquoi ?**

- **Algorithme temporel** : TikTok favorise certains créneaux
- **Audience cible** : Heures de pointe par région
- **Fenêtre d'opportunité** : Premières heures critiques

#### **1.4 Features de Compte**

```python
ACCOUNT_FEATURES = {
    'account_followers': int,    # Taille audience
    'account_verification': bool, # Crédibilité
    'account_age_days': int,     # Expérience
    'avg_views_per_video': float, # Performance historique
    'consistency_score': float,  # Régularité de posting
}
```

**Pourquoi ?**

- **Contexte créateur** : Influence sur la viralité
- **Historique de performance** : Prédicteur de succès futur
- **Crédibilité** : Facteur de confiance algorithme

---

### **Phase 2 : Historical Analysis & Visual Features** (Suivante)

#### **2.1 Historical Analysis** 🔍

**Qu'est-ce que c'est ?**
L'analyse historique examine les patterns de performance d'un compte sur le temps pour identifier :

- **Tendances de croissance** de l'audience
- **Cohérence de performance** entre vidéos
- **Évolution des métriques** d'engagement
- **Patterns de viralité** récurrents

**Pourquoi c'est important ?**

```python
HISTORICAL_FEATURES = {
    # Performance historique
    'avg_views_last_10_videos': float,
    'std_views_last_10_videos': float,  # Consistance
    'growth_rate_30_days': float,       # Tendance

    # Patterns de viralité
    'viral_videos_ratio': float,        # % vidéos virales
    'avg_time_to_viral': float,         # Temps moyen vers viralité

    # Cohérence de contenu
    'content_category_consistency': float, # Cohérence thématique
    'style_consistency_score': float,      # Cohérence visuelle
}
```

**Intérêt :**

- **Prédicteur de stabilité** : Comptes cohérents > comptes volatils
- **Pattern recognition** : Identifier les "formules" qui marchent
- **Évolution algorithmique** : S'adapter aux changements TikTok

#### **2.2 Visual Features (Gemini Analysis)**

**Basé sur l'article clé :** "Understanding Indicators of Virality in TikTok Short Videos"

##### **2.2.1 Features de Composition Visuelle**

```python
COMPOSITION_FEATURES = {
    # Close-ups et zooms (CRITIQUE selon l'article)
    'close_up_presence': bool,          # Présence de plans rapprochés
    'zoom_effects_count': int,          # Nombre d'effets de zoom
    'face_shot_ratio': float,           # % temps avec visage visible

    # Mouvement et dynamisme
    'movement_intensity': float,        # 0-10, intensité du mouvement
    'camera_movement_score': float,     # Mouvements de caméra
    'action_scenes_ratio': float,       # % scènes d'action

    # Transitions et rythme
    'transition_count': int,            # Nombre de transitions
    'transition_speed': float,          # Vitesse moyenne transitions
    'rhythm_consistency': float,        # Cohérence rythmique
}
```

**Pourquoi ces features ?**

- **Close-ups** : Créent intimité et engagement émotionnel
- **Zooms** : Attirent l'attention et créent du dynamisme
- **Mouvement** : Maintient l'attention (algorithme favorise)
- **Transitions** : Rythme élevé = rétention accrue

##### **2.2.2 Features de Qualité Visuelle**

```python
QUALITY_FEATURES = {
    # Couleurs et esthétique
    'color_vibrancy_score': float,      # 0-10, saturation des couleurs
    'color_palette_consistency': float, # Cohérence palette
    'lighting_quality': float,          # 0-10, qualité éclairage

    # Technique
    'video_resolution_score': float,    # Qualité technique
    'stability_score': float,           # Stabilité caméra
    'professional_quality': float,      # Score production pro
}
```

**Pourquoi ?**

- **Couleurs vives** : Attirent l'attention (algorithme favorise)
- **Qualité technique** : Signe de professionnalisme
- **Cohérence esthétique** : Marque de fabrique du créateur

##### **2.2.3 Features de Contenu Visuel**

```python
CONTENT_VISUAL_FEATURES = {
    # Éléments visuels
    'human_presence': bool,             # Présence humaine
    'face_count': int,                  # Nombre de visages
    'text_overlay_presence': bool,      # Texte à l'écran
    'graphic_elements_count': int,      # Éléments graphiques

    # Style de contenu
    'video_style_category': str,        # selfie, landscape, close-up, etc.
    'aesthetic_category': str,          # minimaliste, coloré, sombre, etc.
    'content_mood': str,                # joyeux, sérieux, mystérieux, etc.
}
```

**Pourquoi ?**

- **Présence humaine** : Augmente l'engagement (validé par recherche)
- **Texte à l'écran** : Améliore la rétention et compréhension
- **Style cohérent** : Marque de fabrique du créateur

---

## 🎯 Systèmes de Scoring

### **Scoring de Viralité**

```python
VIRALITY_SCORING = {
    'micro_viral': 10000,      # 10K vues
    'viral': 100000,           # 100K vues
    'mega_viral': 1000000,     # 1M vues
    'ultra_viral': 10000000,   # 10M vues
}
```

### **Scoring d'Engagement**

```python
ENGAGEMENT_SCORING = {
    'low': 0.02,               # <2% engagement rate
    'medium': 0.05,            # 2-5% engagement rate
    'high': 0.10,              # 5-10% engagement rate
    'excellent': 0.15,         # >10% engagement rate
}
```

### **Scoring Visuel**

```python
VISUAL_SCORING = {
    'movement_intensity': {
        'low': (0, 3),         # Statique
        'medium': (3, 7),      # Modéré
        'high': (7, 10),       # Dynamique
    },
    'color_vibrancy': {
        'low': (0, 3),         # Terne
        'medium': (3, 7),      # Normal
        'high': (7, 10),       # Vif
    },
    'quality_score': {
        'amateur': (0, 4),     # Amateur
        'semi_pro': (4, 7),    # Semi-professionnel
        'professional': (7, 10), # Professionnel
    }
}
```

---

## 🔬 Méthodologie de Validation

### **1. Validation Croisée**

- **Split temporel** : 70% train (ancien), 30% test (récent)
- **K-fold par niche** : Éviter le biais catégoriel
- **Validation externe** : Test sur comptes non vus

### **2. Métriques de Performance**

```python
PERFORMANCE_METRICS = {
    'classification': ['precision', 'recall', 'f1', 'accuracy'],
    'regression': ['mae', 'rmse', 'r2_score'],
    'business': ['top_10_accuracy', 'viral_prediction_rate'],
}
```

### **3. Tests d'Hypothèses**

- **Test A/B** : Features avec/sans analyse visuelle
- **Corrélation** : Features vs métriques de viralité
- **Feature importance** : Quelles features sont les plus prédictives

---

## 📊 Roadmap Détaillée

### **Semaine 1 : Phase 1 Complète**

- [ ] Implémenter toutes les features statistiques avancées
- [ ] Créer le baseline model (RandomForest)
- [ ] Valider les performances (target: >70% accuracy)
- [ ] Documenter les résultats

### **Semaine 2 : Phase 2 - Historical Analysis**

- [ ] Implémenter l'analyse historique des comptes
- [ ] Extraire les patterns de performance
- [ ] Créer les features de cohérence
- [ ] Tester l'impact sur les prédictions

### **Semaine 3 : Phase 2 - Visual Features**

- [ ] Améliorer les prompts Gemini pour features spécifiques
- [ ] Implémenter l'extraction de features visuelles
- [ ] Créer les systèmes de scoring visuel
- [ ] Intégrer dans le modèle

### **Semaine 4 : Optimisation & Documentation**

- [ ] Optimiser le modèle final
- [ ] Créer le case study complet
- [ ] Documenter les insights et recommandations
- [ ] Préparer la démo

---

## 🎯 Prochaines Étapes

1. **Valider les hypothèses** avec un petit dataset
2. **Implémenter Phase 1** complète
3. **Tester l'impact** de chaque feature
4. **Itérer** sur les résultats

---

_Document évolutif - Mise à jour continue basée sur les résultats et insights_
