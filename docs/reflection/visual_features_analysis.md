# 🎬 Analyse des Features Visuelles - Viralité TikTok

## 📚 Article de Référence Principal

**"Understanding Indicators of Virality in TikTok Short Videos"** (2021)

> Cet article a identifié des patterns visuels spécifiques qui corrèlent fortement avec la viralité des vidéos TikTok courtes.

---

## 🎯 Features Visuelles Critiques Identifiées

### **1. Close-ups et Plans Rapprochés** 🔍

**Finding de l'article :** Les vidéos avec des plans rapprochés (close-ups) surperforment significativement.

**Hypothèse :** Les close-ups créent une intimité émotionnelle et augmentent l'engagement.

**Features à extraire :**

```python
CLOSE_UP_FEATURES = {
    'close_up_presence': bool,          # Présence de plans rapprochés
    'close_up_duration_ratio': float,   # % temps en close-up
    'face_shot_ratio': float,           # % temps avec visage visible
    'close_up_intensity': float,        # 0-10, proximité du visage
    'eye_contact_presence': bool,       # Regard direct caméra
}
```

**Scoring :**

- **Faible** : 0-20% temps en close-up
- **Moyen** : 20-60% temps en close-up
- **Élevé** : 60-100% temps en close-up

### **2. Effets de Zoom et Mouvements** 🔄

**Finding de l'article :** Les vidéos avec des effets de zoom et mouvements de caméra dynamiques ont un engagement plus élevé.

**Hypothèse :** Les zooms attirent l'attention et créent du dynamisme visuel.

**Features à extraire :**

```python
ZOOM_MOVEMENT_FEATURES = {
    'zoom_effects_count': int,          # Nombre d'effets de zoom
    'zoom_intensity': float,            # 0-10, amplitude des zooms
    'camera_movement_score': float,     # 0-10, mouvements caméra
    'pan_effects_presence': bool,       # Effets de panoramique
    'tilt_effects_presence': bool,      # Effets d'inclinaison
    'movement_consistency': float,      # Cohérence des mouvements
}
```

**Scoring :**

- **Statique** : 0-2 mouvements/zooms
- **Modéré** : 3-7 mouvements/zooms
- **Dynamique** : 8+ mouvements/zooms

### **3. Transitions et Rythme** ⚡

**Finding de l'article :** Les vidéos avec des transitions rapides et un rythme élevé maintiennent mieux l'attention.

**Hypothèse :** Le rythme rapide correspond aux attentes de l'audience TikTok.

**Features à extraire :**

```python
RHYTHM_FEATURES = {
    'transition_count': int,            # Nombre de transitions
    'transition_speed': float,          # Vitesse moyenne (sec/transition)
    'scene_changes_count': int,         # Changements de scène
    'rhythm_consistency': float,        # 0-10, cohérence rythmique
    'cut_frequency': float,             # Fréquence des cuts (cuts/sec)
    'pace_score': float,                # 0-10, rythme global
}
```

**Scoring :**

- **Lent** : <2 transitions, >3s/transition
- **Modéré** : 2-5 transitions, 1-3s/transition
- **Rapide** : >5 transitions, <1s/transition

### **4. Couleurs et Esthétique** 🎨

**Finding de l'article :** Les vidéos avec des couleurs vives et des palettes saturées attirent plus l'attention.

**Hypothèse :** Les couleurs vives se démarquent dans le feed et captent l'attention.

**Features à extraire :**

```python
COLOR_FEATURES = {
    'color_vibrancy_score': float,      # 0-10, saturation des couleurs
    'color_palette_consistency': float, # 0-10, cohérence palette
    'brightness_score': float,          # 0-10, luminosité
    'contrast_score': float,            # 0-10, contraste
    'color_harmony': float,             # 0-10, harmonie des couleurs
    'dominant_colors': list,            # Couleurs dominantes
    'color_trend_alignment': float,     # 0-10, alignement tendances
}
```

**Scoring :**

- **Terne** : 0-3, couleurs neutres
- **Normal** : 4-7, couleurs équilibrées
- **Vif** : 8-10, couleurs saturées

### **5. Présence Humaine** 👥

**Finding de l'article :** La présence d'humains augmente significativement l'engagement.

**Hypothèse :** Les humains créent une connexion émotionnelle et sociale.

**Features à extraire :**

```python
HUMAN_FEATURES = {
    'human_presence': bool,             # Présence humaine
    'face_count': int,                  # Nombre de visages
    'face_visibility_ratio': float,     # % temps visages visibles
    'body_presence': bool,              # Présence de corps
    'gesture_intensity': float,         # 0-10, intensité gestes
    'expression_variety': float,        # 0-10, variété expressions
    'social_interaction': bool,         # Interactions sociales
}
```

**Scoring :**

- **Aucune** : 0 visages
- **Faible** : 1 visage, <50% temps visible
- **Élevée** : 1+ visages, >50% temps visible

### **6. Éléments Textuels et Graphiques** 📝

**Finding de l'article :** Les vidéos avec du texte à l'écran et des éléments graphiques ont une meilleure rétention.

**Hypothèse :** Le texte améliore la compréhension et la mémorisation.

**Features à extraire :**

```python
TEXT_GRAPHIC_FEATURES = {
    'text_overlay_presence': bool,      # Texte à l'écran
    'text_readability_score': float,    # 0-10, lisibilité
    'text_duration_ratio': float,       # % temps avec texte
    'graphic_elements_count': int,      # Éléments graphiques
    'emoji_presence': bool,             # Présence d'emojis
    'call_to_action_presence': bool,    # Présence CTA
    'branding_elements': int,           # Éléments de marque
}
```

**Scoring :**

- **Aucun** : Pas de texte/éléments
- **Faible** : 1-2 éléments
- **Élevé** : 3+ éléments

---

## 🏗️ Architecture d'Extraction

### **Prompt Gemini Optimisé**

```python
VISUAL_ANALYSIS_PROMPT = """
Analysez cette vidéo TikTok pour extraire des features visuelles spécifiques à la viralité.

Vidéo: {video_url}

Extrayez les features suivantes avec des scores numériques (0-10) :

1. COMPOSITION VISUELLE:
   - close_up_presence: bool (présence de plans rapprochés)
   - close_up_duration_ratio: float (0-1, % temps en close-up)
   - face_shot_ratio: float (0-1, % temps visage visible)
   - zoom_effects_count: int (nombre d'effets de zoom)
   - camera_movement_score: float (0-10, mouvements caméra)

2. RYTHME ET TRANSITIONS:
   - transition_count: int (nombre de transitions)
   - transition_speed: float (secondes par transition)
   - cut_frequency: float (cuts par seconde)
   - pace_score: float (0-10, rythme global)

3. COULEURS ET ESTHÉTIQUE:
   - color_vibrancy_score: float (0-10, saturation)
   - brightness_score: float (0-10, luminosité)
   - contrast_score: float (0-10, contraste)
   - dominant_colors: list (couleurs principales)

4. PRÉSENCE HUMAINE:
   - human_presence: bool
   - face_count: int
   - face_visibility_ratio: float (0-1)
   - gesture_intensity: float (0-10)

5. ÉLÉMENTS TEXTUELS:
   - text_overlay_presence: bool
   - text_readability_score: float (0-10)
   - graphic_elements_count: int

Retournez un JSON structuré avec ces features.
"""
```

### **Système de Validation**

```python
VISUAL_FEATURE_VALIDATION = {
    'required_fields': [
        'close_up_presence', 'face_shot_ratio', 'transition_count',
        'color_vibrancy_score', 'human_presence', 'text_overlay_presence'
    ],
    'range_checks': {
        'close_up_duration_ratio': (0, 1),
        'face_shot_ratio': (0, 1),
        'color_vibrancy_score': (0, 10),
        'transition_speed': (0, 60),  # max 60s par transition
    },
    'type_checks': {
        'close_up_presence': bool,
        'human_presence': bool,
        'text_overlay_presence': bool,
        'zoom_effects_count': int,
        'transition_count': int,
    }
}
```

---

## 📊 Métriques de Performance Visuelles

### **Scores Composés**

```python
VISUAL_PERFORMANCE_SCORES = {
    'engagement_potential': float,      # Score global engagement
    'attention_retention': float,       # Capacité à retenir l'attention
    'viral_potential': float,           # Potentiel viralité
    'professional_quality': float,      # Qualité production
    'trend_alignment': float,           # Alignement tendances
}
```

### **Calcul des Scores**

```python
def calculate_visual_scores(features):
    """Calcule les scores de performance visuelle."""

    # Score d'engagement (basé sur présence humaine + dynamisme)
    engagement_score = (
        features['human_presence'] * 0.4 +
        features['face_shot_ratio'] * 0.3 +
        features['camera_movement_score'] / 10 * 0.3
    )

    # Score de rétention (basé sur rythme + transitions)
    retention_score = (
        min(features['transition_count'] / 5, 1) * 0.4 +
        (10 - features['transition_speed']) / 10 * 0.3 +
        features['pace_score'] / 10 * 0.3
    )

    # Score viral (basé sur dynamisme + couleurs)
    viral_score = (
        features['color_vibrancy_score'] / 10 * 0.3 +
        features['zoom_effects_count'] / 5 * 0.3 +
        features['close_up_duration_ratio'] * 0.4
    )

    return {
        'engagement_potential': engagement_score,
        'attention_retention': retention_score,
        'viral_potential': viral_score,
        'overall_visual_score': (engagement_score + retention_score + viral_score) / 3
    }
```

---

## 🎯 Validation et Tests

### **Tests A/B Visuels**

1. **Test Close-ups** : Vidéos avec/sans close-ups
2. **Test Couleurs** : Vidéos vives vs neutres
3. **Test Rythme** : Vidéos rapides vs lentes
4. **Test Transitions** : Vidéos avec/sans transitions

### **Métriques de Validation**

```python
VISUAL_VALIDATION_METRICS = {
    'feature_correlation': float,       # Corrélation avec viralité
    'prediction_accuracy': float,       # Précision prédictions
    'feature_importance': dict,         # Importance relative
    'cross_validation_score': float,    # Score validation croisée
}
```

---

## 📈 Roadmap d'Implémentation

### **Phase 1 : Features de Base** (Semaine 1)

- [ ] Implémenter extraction close-ups et visages
- [ ] Implémenter comptage transitions
- [ ] Implémenter analyse couleurs basique
- [ ] Tester sur 50 vidéos

### **Phase 2 : Features Avancées** (Semaine 2)

- [ ] Implémenter analyse mouvements caméra
- [ ] Implémenter scoring rythme
- [ ] Implémenter analyse textes/graphiques
- [ ] Optimiser prompts Gemini

### **Phase 3 : Optimisation** (Semaine 3)

- [ ] Ajuster les seuils de scoring
- [ ] Valider sur dataset complet
- [ ] Intégrer dans modèle ML
- [ ] Mesurer impact sur performance

---

_Document basé sur l'analyse de "Understanding Indicators of Virality in TikTok Short Videos" (2021)_
