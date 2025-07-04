# Analyse des Coûts Gemini - Analyse Vidéo TikTok

## 📊 Vue d'Ensemble

**Pas besoin de télécharger les vidéos !** Gemini peut analyser directement les URLs TikTok, ce qui simplifie énormément le workflow.

---

## 🎯 Méthodes d'Analyse Vidéo

### 1. URL TikTok Directe (Recommandé)

```python
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        {"file_data": {"file_uri": "https://www.tiktok.com/@leaelui/video/7522161584643263766"}},
        {"text": "Analyse cette vidéo: présence humaine, mouvement, couleurs, texte, audio"}
    ]
)
```

### 2. Upload Fichier (Si nécessaire)

```python
# Pour fichiers > 20MB ou réutilisation multiple
myfile = client.files.upload(file="path/to/video.mp4")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[myfile, "Analyse features viralité"]
)
```

### 3. Inline Data (Petites vidéos)

```python
# Pour vidéos < 20MB
video_bytes = open('video.mp4', 'rb').read()
response = client.models.generate_content(
    contents=[
        {"inline_data": {"mime_type": "video/mp4", "data": video_bytes}},
        {"text": "Analyse rapide features"}
    ]
)
```

---

## 💰 Calcul des Coûts Détaillé

### Tokenisation Vidéo

**Règles de base :**

- **Images** : 1 FPS (1 image par seconde)
  - Résolution normale : **258 tokens/image**
  - Résolution basse : **66 tokens/image**
- **Audio** : **32 tokens/seconde**
- **Total par seconde** :
  - Résolution normale : ~**300 tokens/seconde**
  - Résolution basse : ~**100 tokens/seconde**

### Notre Dataset Cible

**Configuration actuelle :**

- **33 comptes × 15 vidéos = 495 vidéos**
- **Durée moyenne TikTok : ~30 secondes**
- **Total : 495 × 30 = 14,850 secondes**

### Estimation des Coûts

#### Gemini 2.0 Flash (Recommandé)

**Résolution Normale :**

```
Input tokens: 14,850s × 300 = 4.455M tokens
Coût input: 4.455M × $0.10 = $0.45

Output estimé: ~1M tokens (features structurées)
Coût output: 1M × $0.40 = $0.40

TOTAL: ~$0.85
```

**Résolution Basse (Optimisé) :**

```
Input tokens: 14,850s × 100 = 1.485M tokens
Coût input: 1.485M × $0.10 = $0.15

Output estimé: ~1M tokens
Coût output: 1M × $0.40 = $0.40

TOTAL: ~$0.55
```

#### Gemini 2.5 Flash (Premium)

**Résolution Normale :**

```
Input: 4.455M × $0.30 = $1.34
Output: 1M × $2.50 = $2.50
TOTAL: ~$3.84
```

---

## 🎯 Stratégie d'Optimisation des Coûts

### 1. Résolution Basse par Défaut

```python
# Utiliser mediaResolution="low" pour économiser
video_metadata = types.VideoMetadata(
    fps=1,  # 1 image par seconde (défaut)
    media_resolution="low"  # 66 tokens/image vs 258
)
```

### 2. Analyse Sélective

```python
# Ne analyser que les vidéos > seuil de viralité
if video_views > 50000:  # Seulement vidéos intéressantes
    analyze_with_gemini(video_url)
```

### 3. Batch Processing

```python
# Grouper les analyses pour optimiser
batch_videos = []
for video in high_potential_videos:
    if len(batch_videos) < 10:
        batch_videos.append(video)
    else:
        process_batch(batch_videos)
        batch_videos = []
```

### 4. Features Progressives

```python
# Niveau 1: Features de base (métadonnées TikTok) - GRATUIT
# Niveau 2: Analyse Gemini pour top 20% des vidéos - ~$0.11
# Niveau 3: Analyse approfondie pour top 5% - ~$0.03
```

---

## 📊 Comparaison des Approches

| Approche                             | Vidéos Analysées | Coût Estimé | Couverture |
| ------------------------------------ | ---------------- | ----------- | ---------- |
| **Toutes vidéos (résolution basse)** | 495              | $0.55       | 100%       |
| **Top 50% par vues**                 | 248              | $0.28       | 50%        |
| **Top 20% par vues**                 | 99               | $0.11       | 20%        |
| **Top 10% viral**                    | 50               | $0.06       | 10%        |

---

## 🎯 Recommandation Finale

### Phase 1 : Test (Budget $0.10)

- **50 vidéos** les plus virales
- **Résolution basse**
- **Validation du pipeline**

### Phase 2 : Production (Budget $0.30)

- **Top 200 vidéos** par engagement
- **Résolution basse**
- **Features complètes**

### Phase 3 : Optimisation (Budget $0.55)

- **Toutes les vidéos**
- **Résolution adaptative**
- **ML model complet**

---

## 🔧 Configuration Optimisée

```python
# Configuration recommandée
GEMINI_CONFIG = {
    "model": "gemini-2.0-flash",  # Meilleur rapport qualité/prix
    "media_resolution": "low",    # Économie 70% sur les tokens
    "fps": 1,                     # 1 image/seconde (standard)
    "max_videos_per_batch": 10,   # Optimisation requêtes
    "analysis_threshold": 10000   # Seuil minimum de vues
}

# Prompt optimisé pour économiser les tokens output
ANALYSIS_PROMPT = """
Analyse cette vidéo TikTok et retourne UNIQUEMENT un JSON structuré:
{
  "human_presence": boolean,
  "face_count": number,
  "movement_intensity": "low|medium|high",
  "color_vibrancy": "low|medium|high",
  "text_overlay": boolean,
  "lighting_quality": "poor|good|excellent"
}
"""
```

---

## 📈 ROI Analysis

**Coût total projet : ~$0.55**
**Bénéfices :**

- Modèle ML avec features visuelles avancées
- Insights exploitables pour créateurs
- Case study valorisable (>$1000 en consulting)
- Portfolio technique démontrable

**ROI estimé : >1000x** 🚀

---

_Analyse basée sur la documentation officielle Gemini API_  
_Dernière mise à jour : Janvier 2025_
