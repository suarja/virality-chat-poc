# 🔍 Méthodologie d'Extraction des Features Gemini

## 🎯 Vue d'Ensemble

Les features Gemini sont extraites via l'API Google Gemini Vision, qui analyse le contenu visuel des vidéos TikTok pour générer des scores prédictifs de viralité. Cette méthodologie combine l'analyse multimodale avec des règles de scoring basées sur la recherche scientifique.

## 📋 Processus d'Extraction

### **1. Analyse Gemini Vision**

#### **Prompt Utilisé**

```python
GEMINI_PROMPT = """
Analyse cette vidéo TikTok pour évaluer son potentiel viral.
Fournis une analyse structurée avec les éléments suivants :

1. ENGAGEMENT FACTORS:
   - viral_potential: [low/medium/high]
   - audience_connection: [weak/moderate/strong]
   - emotional_triggers: [liste des déclencheurs émotionnels]

2. TECHNICAL ELEMENTS:
   - visual_quality: [low/medium/high]
   - production_quality: [low/medium/high]
   - sound_design: [low quality/high quality]
   - length_optimization: [too short/appropriate/too long]

3. TREND ALIGNMENT:
   - current_trends: [aligné/partiellement aligné/non aligné]
   - hashtag_potential: [liste des hashtags suggérés]

4. VISUAL ANALYSIS:
   - human_presence: [description de la présence humaine]
   - shot_type: [close-up/medium/wide/extreme close-up]
   - color_analysis: [vibrant/bright/muted/dull]
"""
```

#### **Réponse Gemini Exemple**

```json
{
  "engagement_factors": {
    "viral_potential": "high",
    "audience_connection": "strong",
    "emotional_triggers": "humor, relatability, surprise"
  },
  "technical_elements": {
    "visual_quality": "high",
    "production_quality": "high",
    "sound_design": "high quality",
    "length_optimization": "appropriate"
  },
  "trend_alignment": {
    "current_trends": "perfectly aligned",
    "hashtag_potential": "#trending #viral #funny #relatable"
  },
  "visual_analysis": {
    "human_presence": "single person, close-up shot",
    "shot_type": "close-up",
    "color_analysis": "vibrant colors, high saturation"
  }
}
```

### **2. Extraction des Features**

#### **audience_connection_score**

```python
def extract_audience_connection_score(gemini_analysis: Dict) -> float:
    """
    Extrait le score de connexion avec l'audience.

    Méthode : Analyse du texte de réponse Gemini pour détecter
    les mots-clés indiquant une forte connexion avec l'audience.

    Logique de scoring :
    - 'strong' ou 'excellent' → 1.0
    - 'moderate' ou 'good' → 0.7
    - Autres → 0.5 (valeur par défaut)
    """
    engagement = gemini_analysis.get('engagement_factors', {})
    audience_text = engagement.get('audience_connection', '').lower()

    if 'strong' in audience_text or 'excellent' in audience_text:
        return 1.0
    elif 'moderate' in audience_text or 'good' in audience_text:
        return 0.7
    else:
        return 0.5
```

**Exemples concrets :**

- "strong audience connection" → 1.0
- "moderate connection with viewers" → 0.7
- "weak audience engagement" → 0.5

#### **viral_potential_score**

```python
def extract_viral_potential_score(gemini_analysis: Dict) -> float:
    """
    Extrait le score de potentiel viral.

    Logique de scoring :
    - 'high' → 1.0
    - 'medium' → 0.7
    - 'low' → 0.3
    """
    engagement = gemini_analysis.get('engagement_factors', {})
    viral_text = engagement.get('viral_potential', '').lower()

    if 'high' in viral_text:
        return 1.0
    elif 'medium' in viral_text:
        return 0.7
    else:
        return 0.3
```

#### **emotional_trigger_count**

```python
def extract_emotional_trigger_count(gemini_analysis: Dict) -> int:
    """
    Compte le nombre de déclencheurs émotionnels identifiés.

    Méthode : Parse la liste des emotional_triggers et compte
    les éléments séparés par des virgules.
    """
    engagement = gemini_analysis.get('engagement_factors', {})
    triggers_text = engagement.get('emotional_triggers', '')

    if not triggers_text:
        return 0

    # Split par virgule et compte les éléments non vides
    triggers = [t.strip() for t in triggers_text.split(',') if t.strip()]
    return len(triggers)
```

**Exemples :**

- "humor, relatability, surprise" → 3
- "excitement" → 1
- "" → 0

#### **visual_quality_score**

```python
def extract_visual_quality_score(gemini_analysis: Dict) -> float:
    """
    Extrait le score de qualité visuelle.

    Logique de scoring :
    - 'high' → 1.0
    - 'medium' → 0.7
    - 'low' → 0.3
    """
    technical = gemini_analysis.get('technical_elements', {})
    quality_text = technical.get('visual_quality', '').lower()

    if 'high' in quality_text:
        return 1.0
    elif 'medium' in quality_text:
        return 0.7
    else:
        return 0.3
```

### **3. Features Visuelles Granulaires**

#### **human_count**

```python
def extract_human_count(gemini_analysis: Dict) -> int:
    """
    Extrait le nombre de personnes dans la vidéo.

    Méthode : Analyse du texte de human_presence pour détecter
    les mots-clés indiquant le nombre de personnes.
    """
    visual = gemini_analysis.get('visual_analysis', {})
    human_text = visual.get('human_presence', '').lower()

    if 'multiple people' in human_text or 'group' in human_text:
        return 3
    elif 'two people' in human_text or 'couple' in human_text:
        return 2
    elif 'person' in human_text or 'human' in human_text or 'individual' in human_text:
        return 1
    else:
        return 0
```

#### **shot_type**

```python
def extract_shot_type(gemini_analysis: Dict) -> str:
    """
    Extrait le type de plan utilisé.

    Valeurs possibles : 'close_up', 'medium', 'wide', 'unknown'
    """
    visual = gemini_analysis.get('visual_analysis', {})
    shot_text = visual.get('shot_type', '').lower()

    if 'close-up' in shot_text:
        return 'close_up'
    elif 'medium' in shot_text:
        return 'medium'
    elif 'wide' in shot_text:
        return 'wide'
    else:
        return 'unknown'
```

#### **color_vibrancy_score**

```python
def extract_color_vibrancy_score(gemini_analysis: Dict) -> float:
    """
    Extrait le score de saturation des couleurs.

    Logique de scoring basée sur l'analyse des couleurs :
    - 'vibrant' ou 'saturated' → 0.8
    - 'bright' → 0.6
    - 'muted' ou 'dull' → 0.3
    - Autres → 0.5
    """
    visual = gemini_analysis.get('visual_analysis', {})
    color_text = visual.get('color_analysis', '').lower()

    if 'vibrant' in color_text or 'saturated' in color_text:
        return 0.8
    elif 'bright' in color_text:
        return 0.6
    elif 'muted' in color_text or 'dull' in color_text:
        return 0.3
    else:
        return 0.5
```

## 🔬 Validation et Qualité

### **1. Cohérence des Scores**

#### **Vérification de Cohérence**

```python
def validate_gemini_scores(features: Dict) -> bool:
    """
    Valide la cohérence des scores Gemini.
    """
    # Vérifier que les scores sont dans les bonnes plages
    score_features = [
        'audience_connection_score',
        'viral_potential_score',
        'visual_quality_score',
        'production_quality_score'
    ]

    for feature in score_features:
        if feature in features:
            score = features[feature]
            if not (0.0 <= score <= 1.0):
                logger.warning(f"Score {feature} hors plage: {score}")
                return False

    return True
```

### **2. Gestion des Erreurs**

#### **Fallback Values**

```python
def safe_extract_gemini_feature(gemini_analysis: Dict, feature_name: str, default_value: Any) -> Any:
    """
    Extraction sécurisée avec valeurs par défaut.
    """
    try:
        if feature_name == 'audience_connection_score':
            return extract_audience_connection_score(gemini_analysis)
        elif feature_name == 'viral_potential_score':
            return extract_viral_potential_score(gemini_analysis)
        # ... autres features
        else:
            return default_value
    except Exception as e:
        logger.error(f"Erreur extraction {feature_name}: {e}")
        return default_value
```

## 📊 Analyse de Performance

### **1. Corrélations Observées**

| Feature                   | Corrélation avec View Count | Interprétation         |
| ------------------------- | --------------------------- | ---------------------- |
| audience_connection_score | 0.976                       | Très forte corrélation |
| viral_potential_score     | 0.976                       | Très forte corrélation |
| visual_quality_score      | 0.976                       | Très forte corrélation |
| emotional_trigger_count   | 0.099                       | Corrélation modérée    |

### **2. Importance dans le Modèle**

| Feature                   | Importance | Rang |
| ------------------------- | ---------- | ---- |
| audience_connection_score | 0.124      | 1er  |
| emotional_trigger_count   | 0.099      | 4ème |
| viral_potential_score     | 0.094      | 6ème |
| production_quality_score  | 0.089      | 8ème |

## 🚀 Améliorations Futures

### **1. Prompts Plus Sophistiqués**

#### **Prompt Amélioré**

```python
IMPROVED_GEMINI_PROMPT = """
Analyse cette vidéo TikTok avec une approche scientifique pour la prédiction de viralité.

Évalue chaque aspect sur une échelle de 1-10 et fournis une justification :

1. ENGAGEMENT ANALYSIS:
   - viral_potential: [1-10] - Justification: [texte]
   - audience_connection: [1-10] - Justification: [texte]
   - emotional_triggers: [liste détaillée avec scores]

2. TECHNICAL QUALITY:
   - visual_quality: [1-10] - Justification: [texte]
   - production_quality: [1-10] - Justification: [texte]
   - audio_quality: [1-10] - Justification: [texte]

3. CONTENT ANALYSIS:
   - hook_strength: [1-10] - Justification: [texte]
   - story_structure: [1-10] - Justification: [texte]
   - relatability: [1-10] - Justification: [texte]
"""
```

### **2. Extraction Plus Granulaire**

#### **Scores Numériques Directs**

```python
def extract_numeric_score(gemini_text: str) -> float:
    """
    Extrait un score numérique directement du texte Gemini.
    """
    import re

    # Chercher un nombre entre 1-10 dans le texte
    match = re.search(r'(\d+)/10|score:\s*(\d+)', gemini_text.lower())
    if match:
        score = int(match.group(1) or match.group(2))
        return score / 10.0  # Normaliser à 0-1

    return 0.5  # Valeur par défaut
```

### **3. Validation Croisée**

#### **Validation Humaine**

- Comparer les scores Gemini avec des évaluations humaines
- Identifier les biais dans l'analyse automatique
- Ajuster les prompts en conséquence

## 📚 Références

### **Fichiers de Code**

- `src/features/modular_feature_system.py` - Implémentation actuelle
- `src/features/comprehensive_feature_extractor.py` - Version avancée
- `tests/features/test_data_processor.py` - Tests unitaires

### **Documentation Associée**

- `docs/reflection/iterations/iteration_1_scientific_documentation.md`
- `docs/gemini_analysis/README.md`

---

_Document créé le 5 juillet 2025 - Méthodologie d'extraction des features Gemini_
