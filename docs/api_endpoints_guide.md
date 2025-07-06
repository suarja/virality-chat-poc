# 📊 Guide des Endpoints API - Analyse TikTok

## 🎯 Vue d'ensemble

L'API TikTok Virality Prediction propose deux types d'analyse distincts, chacun optimisé pour des cas d'usage spécifiques.

---

## 🔗 Analyse par URL Vidéo (`/analyze-tiktok-url`)

### 📋 Description

Analyse une vidéo TikTok spécifique via son URL pour prédire sa viralité.

### 🎯 Cas d'usage

- **Analyse ciblée** : Vous avez une URL spécifique et voulez connaître le potentiel viral
- **Validation rapide** : Test rapide d'une vidéo avant publication
- **Analyse post-publication** : Évaluer pourquoi une vidéo a performé ou non

### 🔄 Pipeline

```
URL TikTok → Scraping vidéo → Extraction features → Prédiction viralité
```

### 📊 Données retournées

```json
{
  "url": "https://www.tiktok.com/@user/video/1234567890",
  "video_data": {
    "id": "1234567890",
    "text": "Description de la vidéo",
    "duration": 30.5,
    "playCount": 15000,
    "diggCount": 2500,
    "commentCount": 150,
    "shareCount": 75,
    "hashtags": ["#viral", "#trending"]
  },
  "features": {
    "video_duration_optimized": 1.0,
    "hashtag_effectiveness_score": 0.8,
    "audience_connection_score": 0.75
    // ... 34 features au total
  },
  "prediction": {
    "virality_score": 0.78,
    "confidence": 0.85,
    "recommendations": [
      "Optimiser les hashtags pour plus de visibilité",
      "Améliorer l'engagement dans les premières secondes"
    ]
  },
  "analysis_time": 2.3,
  "status": "completed"
}
```

### ⚡ Performance

- **Temps d'analyse** : 2-5 secondes
- **Précision** : R² = 0.457 (prédiction pré-publication)
- **Features** : 34 features avancées extraites automatiquement

---

## 👤 Analyse de Profil (`/analyze-tiktok-profile`)

### 📋 Description

Analyse complète d'un profil TikTok, incluant toutes ses vidéos récentes.

### 🎯 Cas d'usage

- **Audit de compte** : Analyse complète des performances d'un profil
- **Stratégie de contenu** : Identifier les patterns qui fonctionnent
- **Analyse concurrentielle** : Étudier les stratégies des concurrents
- **Optimisation globale** : Améliorer la stratégie de contenu

### 🔄 Pipeline

```
Username → Scraping profil → Analyse vidéos multiples → Statistiques globales
```

### 📊 Données retournées

```json
{
  "username": "@username",
  "profile_data": {
    "username": "username",
    "scraped_at": "2024-01-15T10:30:00Z",
    "videos_count": 25
  },
  "videos_analysis": [
    {
      "video_id": "1234567890",
      "url": "https://www.tiktok.com/@user/video/1234567890",
      "features": {
        /* 34 features */
      },
      "prediction": {
        "virality_score": 0.78,
        "confidence": 0.85
      }
    }
    // ... pour chaque vidéo
  ],
  "profile_stats": {
    "total_videos_analyzed": 25,
    "average_virality_score": 0.72,
    "top_viral_videos": [
      // Top 5 vidéos les plus virales
    ]
  },
  "analysis_time": 45.2,
  "status": "completed"
}
```

### ⚡ Performance

- **Temps d'analyse** : 30-60 secondes (selon le nombre de vidéos)
- **Vidéos analysées** : Jusqu'à 50 vidéos par défaut (configurable)
- **Précision** : Même R² = 0.457 pour chaque vidéo

---

## 🔍 Comparaison Détaillée

| Aspect          | Analyse URL       | Analyse Profil                 |
| --------------- | ----------------- | ------------------------------ |
| **Objectif**    | Vidéo spécifique  | Profil complet                 |
| **Temps**       | 2-5 secondes      | 30-60 secondes                 |
| **Données**     | 1 vidéo           | Jusqu'à 50 vidéos              |
| **Cas d'usage** | Validation rapide | Audit stratégique              |
| **Complexité**  | Simple            | Avancée                        |
| **Coût API**    | 1 appel           | 1 appel (mais plus de données) |

---

## 🛠️ Utilisation Pratique

### Exemple d'analyse URL

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@username/video/1234567890"
  }'
```

### Exemple d'analyse profil

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "username",
    "max_videos": 25
  }'
```

---

## 📈 Recommandations d'Usage

### 🎯 Quand utiliser l'analyse URL

- ✅ Test rapide d'une vidéo
- ✅ Validation avant publication
- ✅ Analyse post-mortem d'une vidéo spécifique
- ✅ Intégration dans un workflow automatisé

### 🎯 Quand utiliser l'analyse profil

- ✅ Audit complet d'un compte
- ✅ Analyse de la stratégie de contenu
- ✅ Étude concurrentielle
- ✅ Optimisation globale du profil
- ✅ Génération de rapports détaillés

---

## 🔧 Configuration et Limites

### ⚙️ Paramètres configurables

- **max_videos** : Nombre maximum de vidéos à analyser (profil)
- **Timeout** : Délai d'attente pour le scraping
- **Cache** : Mise en cache des résultats (optionnel)

### 🚫 Limites actuelles

- **Vidéos privées** : Non accessibles
- **Vidéos supprimées** : Non analysables
- **Rate limiting** : Respect des limites TikTok/Apify
- **Données historiques** : Limitées aux vidéos récentes

---

## 🧪 Tests et Validation

### Script de test complet

```bash
python scripts/test_real_pipeline.py
```

### Validation des résultats

- ✅ Health check de l'API
- ✅ Test des endpoints individuels
- ✅ Validation du pipeline complet
- ✅ Test avec de vraies URLs TikTok

---

## 📚 Ressources Additionnelles

- **Documentation API** : `/docs` (Swagger UI)
- **Health Check** : `/health`
- **Informations API** : `/info`
- **Tests automatisés** : `scripts/test_real_pipeline.py`

---

## 🎯 Prochaines Étapes

1. **Testez avec de vraies URLs TikTok** pour valider le pipeline
2. **Analysez vos propres profils** pour optimiser votre stratégie
3. **Intégrez l'API** dans vos workflows de création de contenu
4. **Surveillez les performances** et ajustez selon vos besoins
