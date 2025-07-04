# Synthèse des Articles de Recherche - Viralité TikTok

## 📚 Articles Analysés

1. **"Understanding Indicators of Virality in TikTok Short Videos"** (2021)
2. **"Analyzing User Engagement with TikTok's Short [Videos]"**
3. **"Trick and Please: A Mixed-Method Study On User Assumptions About the TikTok Algorithm"**
4. **"An Empirical Investigation of Personalization Factors on TikTok"**
5. **"Analysis on the Douyin (TikTok) Mania"**
6. **"Monolith Real Time Recommendation System"**

---

## 🎯 Findings Clés pour notre POC

### 1. Indicateurs de Viralité Principaux

**Métriques Quantitatives :**

- **Vues** : Métrique primaire de viralité
- **Ratio Engagement** : (Likes + Comments + Shares) / Views
- **Vitesse de propagation** : Croissance des vues dans les premières heures
- **Durée de rétention** : Temps de visionnage moyen

**Seuils de Viralité Suggérés :**

- **Micro-viral** : 10K+ vues (applicable à nos comptes moyens)
- **Viral** : 100K+ vues
- **Méga-viral** : 1M+ vues

### 2. Features Vidéo Déterminantes

**Features Visuelles :**

- **Mouvement** : Vidéos avec action/danse surperforment
- **Visages humains** : Présence d'humains augmente l'engagement
- **Couleurs vives** : Palettes saturées attirent l'attention
- **Transitions rapides** : Rythme élevé maintient l'attention

**Features Audio :**

- **Trending sounds** : Utilisation de sons populaires
- **Musique originale vs tendance** : Balance critique
- **Synchronisation** : Alignement mouvement/son

**Features Textuelles :**

- **Hashtags trending** : 3-5 hashtags optimaux
- **Descriptions courtes** : <100 caractères préférés
- **Call-to-action** : "Commentez si...", "Partagez si..."

### 3. Facteurs Temporels

**Timing de Publication :**

- **Heures de pointe** : 18h-22h (audience française)
- **Jours optimaux** : Mardi-Jeudi pour contenu informatif, Vendredi-Dimanche pour entertainment
- **Consistance** : Publication régulière > timing parfait

**Algorithme Temporel :**

- **Golden Hour** : Premières 30 minutes critiques
- **Fenêtre 24h** : Performance quasi-finale après 24h
- **Long terme** : Possible résurgence après plusieurs semaines

---

## 🏗️ Architecture Recommandée pour notre Modèle

### Features à Extraire (Priorité)

**Niveau 1 - Métadonnées TikTok :**

```python
PRIMARY_FEATURES = [
    'view_count', 'like_count', 'comment_count', 'share_count',
    'video_duration', 'hashtags_count', 'description_length',
    'account_followers', 'account_verification', 'publish_hour',
    'publish_day_of_week', 'trending_sound_usage'
]
```

**Niveau 2 - Analyse Vidéo (Gemini) :**

```python
VISUAL_FEATURES = [
    'human_presence', 'face_count', 'movement_intensity',
    'color_vibrancy', 'scene_changes', 'text_overlay_presence',
    'lighting_quality', 'video_style' # (selfie, landscape, close-up)
]
```

**Niveau 3 - Analyse Avancée :**

```python
ADVANCED_FEATURES = [
    'audio_energy', 'speech_presence', 'music_sync_quality',
    'emotional_tone', 'content_category', 'trend_alignment_score'
]
```

### Modèle ML Recommandé

**Architecture 80/20 :**

1. **Baseline Model** : RandomForest sur features niveau 1 (80% performance)
2. **Enhanced Model** : XGBoost avec features niveau 1+2 (95% performance)
3. **Premium Model** : Ensemble avec features niveau 3 (100% performance)

---

## 📊 Dataset & Sampling Strategy

### Stratégie de Collecte

**Volume Optimal :**

- **30-50 vidéos par compte** (basé sur les études)
- **Total : 300-450 vidéos** pour robustesse statistique
- **Balance niches** : Éviter le biais vers une catégorie

**Filtres de Qualité :**

- Minimum 1K vues (éviter le bruit)
- Vidéos publiées dans les 6 derniers mois (algorithme stable)
- Exclure les vidéos sponsorisées/ads

**Labels de Viralité :**

```python
VIRALITY_LABELS = {
    'low': views < 10_000,
    'medium': 10_000 <= views < 100_000,
    'high': 100_000 <= views < 1_000_000,
    'viral': views >= 1_000_000
}
```

---

## 🎯 Insights Actionnables

### Pour Créateurs

**Recommandations Génériques :**

1. **Optimiser les 3 premières secondes** : Hook visuel/audio fort
2. **Utiliser trending sounds** mais avec twist personnel
3. **Posting régulier** > timing parfait
4. **Engager rapidement** : Répondre aux premiers commentaires

**Recommandations par Niche :**

- **Tech/IA** : Démonstrations courtes, résultats rapides
- **Food** : Transformation visuelle, ASMR elements
- **Lifestyle** : Authenticité, behind-the-scenes

### Pour notre Modèle

**Priorités Développement :**

1. **Phase 1** : Scraping + features métadonnées (2 jours)
2. **Phase 2** : Analyse vidéo Gemini + baseline model (3 jours)
3. **Phase 3** : Optimisation + interprétabilité (3 jours)
4. **Phase 4** : Interface + documentation (2 jours)

**Métriques de Succès :**

- **Accuracy** : >75% sur classification viralité
- **Interpretability** : Feature importance claire
- **Latency** : <5s prédiction par vidéo
- **Coverage** : Recommendations pour 90% des vidéos

---

## 🔬 Validation Scientifique

### Méthodologie

**Cross-validation :**

- Split temporel : 70% train (vidéos anciennes), 30% test (récentes)
- K-fold par niche pour éviter le biais
- Validation sur comptes non vus

**Métriques :**

- **Classification** : Precision, Recall, F1 par classe de viralité
- **Regression** : MAE, RMSE sur log(views)
- **Business** : Top-10 accuracy pour recommandations

---

_Synthèse basée sur 6 articles de recherche académique_  
_Dernière mise à jour : Janvier 2025_
