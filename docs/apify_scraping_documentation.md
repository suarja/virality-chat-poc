# 📊 Documentation Apify Scraping - TikTok Virality Prediction

## 🎯 Vue d'ensemble

Ce document documente l'utilisation de l'actor Apify `clockworks/tiktok-scraper` pour récupérer les données TikTok nécessaires à la prédiction de viralité.

---

## 🔗 Configuration Apify

### **Actor Utilisé**

- **ID Actor**: `clockworks/tiktok-scraper`
- **Version**: Latest
- **Capacités**: Scraping vidéo direct, scraping profil, téléchargement média

### **Configuration API**

```python
from apify_client import ApifyClient
client = ApifyClient("YOUR_API_TOKEN")
```

---

## 📋 Payloads de Configuration

### **1. Scraping Vidéo Direct (postURLs)**

```json
{
  "excludePinnedPosts": false,
  "postURLs": ["https://www.tiktok.com/@swarecito/video/7505706702050823446"],
  "proxyCountryCode": "None",
  "resultsPerPage": 100,
  "scrapeRelatedVideos": false,
  "shouldDownloadAvatars": false,
  "shouldDownloadCovers": false,
  "shouldDownloadMusicCovers": false,
  "shouldDownloadSlideshowImages": false,
  "shouldDownloadSubtitles": false,
  "shouldDownloadVideos": false
}
```

### **2. Scraping Vidéo avec Téléchargement**

```json
{
  "excludePinnedPosts": false,
  "postURLs": ["https://www.tiktok.com/@swarecito/video/7505706702050823446"],
  "resultsPerPage": 100,
  "shouldDownloadCovers": true,
  "shouldDownloadSlideshowImages": true,
  "shouldDownloadSubtitles": true,
  "shouldDownloadVideos": true,
  "videoKvStoreIdOrName": "tiktok-videos-test"
}
```

### **3. Scraping Profil**

```json
{
  "profiles": ["swarecito"],
  "profileSorting": "latest",
  "excludePinnedPosts": false,
  "resultsPerPage": 50,
  "maxProfilesPerQuery": 10,
  "shouldDownloadVideos": false,
  "shouldDownloadCovers": false,
  "shouldDownloadSubtitles": false,
  "shouldDownloadSlideshowImages": false,
  "shouldDownloadAvatars": false,
  "shouldDownloadMusicCovers": false,
  "proxyCountryCode": "None"
}
```

---

## 📊 Structure des Données Scrapées

### **Métadonnées Vidéo (Exemple Réel)**

```json
{
  "id": "7505706702050823446",
  "text": "Booste ton ChatGPT avec cet Agent personnalisé 🤖 commente \"INSTRUCTION\" pour l'obtenir #chatgpt #agent #prompt #instruction",
  "textLanguage": "fr",
  "createTime": 1747558528,
  "createTimeISO": "2025-05-18T08:55:28.000Z",
  "locationCreated": "FR",
  "isAd": false,
  "authorMeta": {
    "id": "7424447537598055456",
    "name": "swarecito",
    "profileUrl": "https://www.tiktok.com/@swarecito",
    "nickName": "Jason Suárez",
    "verified": false,
    "signature": "Développeur blockchain spécialisé IA & automatisation.",
    "bioLink": null,
    "originalAvatarUrl": "...",
    "avatar": "...",
    "privateAccount": false,
    "roomId": "",
    "ttSeller": false,
    "following": 54,
    "friends": 0,
    "fans": 2002,
    "heart": 4325,
    "video": 55,
    "digg": 222
  },
  "musicMeta": {
    "musicName": "son original",
    "musicAuthor": "Jason Suárez",
    "musicOriginal": true,
    "playUrl": "...",
    "coverMediumUrl": "...",
    "originalCoverMediumUrl": "...",
    "musicId": "7505706686134242070"
  },
  "webVideoUrl": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
  "mediaUrls": [],
  "videoMeta": {
    "height": 1024,
    "width": 576,
    "duration": 97,
    "coverUrl": "...",
    "originalCoverUrl": "...",
    "definition": "540p",
    "format": "mp4",
    "subtitleLinks": [
      {
        "language": "eng-US",
        "downloadLink": "...",
        "tiktokLink": "...",
        "source": "MT",
        "sourceUnabbreviated": "machine translation",
        "version": "4"
      },
      {
        "language": "fra-FR",
        "downloadLink": "...",
        "tiktokLink": "...",
        "source": "MT",
        "sourceUnabbreviated": "machine translation",
        "version": "8:whisper_lid"
      }
    ]
  },
  "diggCount": 1916,
  "shareCount": 302,
  "playCount": 53000,
  "collectCount": 1807,
  "commentCount": 631,
  "mentions": [],
  "detailedMentions": [],
  "hashtags": [
    {
      "id": "7172185891421552645",
      "name": "chatgpt",
      "title": "",
      "cover": ""
    },
    {
      "id": "754842",
      "name": "agent",
      "title": "",
      "cover": ""
    },
    {
      "id": "1928241",
      "name": "prompt",
      "title": "",
      "cover": ""
    },
    {
      "id": "474606",
      "name": "instruction",
      "title": "",
      "cover": ""
    }
  ],
  "effectStickers": [],
  "isSlideshow": false,
  "isPinned": false,
  "isSponsored": false,
  "submittedVideoUrl": "https://www.tiktok.com/@swarecito/video/7505706702050823446"
}
```

---

## 🎥 Stockage des Vidéos Téléchargées

### **Structure de Stockage**

```
data/
├── apify_cache/
│   ├── videos/
│   │   ├── 7505706702050823446/
│   │   │   ├── video.mp4
│   │   │   ├── cover.jpg
│   │   │   ├── subtitles/
│   │   │   │   ├── eng-US.srt
│   │   │   │   └── fra-FR.srt
│   │   │   └── metadata.json
│   │   └── README.md
│   ├── profiles/
│   │   ├── swarecito/
│   │   │   ├── profile_data.json
│   │   │   ├── videos/
│   │   │   └── metadata.json
│   │   └── README.md
│   └── cache_index.json
```

### **Cache Index**

```json
{
  "last_updated": "2025-01-06T07:00:00Z",
  "videos": {
    "7505706702050823446": {
      "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
      "username": "swarecito",
      "scraped_at": "2025-01-06T07:00:00Z",
      "files": {
        "video": "videos/7505706702050823446/video.mp4",
        "cover": "videos/7505706702050823446/cover.jpg",
        "metadata": "videos/7505706702050823446/metadata.json",
        "subtitles": [
          "videos/7505706702050823446/subtitles/eng-US.srt",
          "videos/7505706702050823446/subtitles/fra-FR.srt"
        ]
      },
      "features": {
        "duration": 97,
        "hashtags": ["chatgpt", "agent", "prompt", "instruction"],
        "language": "fr",
        "engagement": {
          "playCount": 53000,
          "diggCount": 1916,
          "commentCount": 631,
          "shareCount": 302,
          "collectCount": 1807
        }
      }
    }
  },
  "profiles": {
    "swarecito": {
      "scraped_at": "2025-01-06T07:00:00Z",
      "videos_count": 55,
      "profile_data": "profiles/swarecito/profile_data.json"
    }
  }
}
```

---

## 🔧 Scripts de Gestion du Cache

### **1. Script de Téléchargement et Cache**

```python
#!/usr/bin/env python3
"""
🎥 Script de téléchargement et cache Apify
📊 Télécharge et stocke les vidéos TikTok pour éviter le re-scraping
"""

import os
import json
import shutil
from datetime import datetime
from apify_client import ApifyClient
from pathlib import Path

class ApifyCacheManager:
    def __init__(self, cache_dir="data/apify_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.cache_dir / "cache_index.json"
        self.load_index()

    def load_index(self):
        """Charge l'index du cache"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                "last_updated": datetime.now().isoformat(),
                "videos": {},
                "profiles": {}
            }

    def save_index(self):
        """Sauvegarde l'index du cache"""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def download_video_with_cache(self, url, force_download=False):
        """Télécharge une vidéo avec cache"""
        video_id = self.extract_video_id(url)

        # Vérifier si déjà en cache
        if not force_download and video_id in self.index["videos"]:
            print(f"✅ Vidéo {video_id} déjà en cache")
            return self.index["videos"][video_id]

        # Télécharger via Apify
        print(f"📥 Téléchargement vidéo {video_id}...")
        # ... logique de téléchargement

        # Mettre à jour l'index
        self.index["videos"][video_id] = {
            "url": url,
            "scraped_at": datetime.now().isoformat(),
            "files": {
                "video": f"videos/{video_id}/video.mp4",
                "metadata": f"videos/{video_id}/metadata.json"
            }
        }
        self.save_index()

        return self.index["videos"][video_id]
```

### **2. Script de Nettoyage du Cache**

```python
def cleanup_cache(self, max_age_days=30):
    """Nettoie le cache des anciens fichiers"""
    cutoff_date = datetime.now() - timedelta(days=max_age_days)

    for video_id, video_data in self.index["videos"].items():
        scraped_at = datetime.fromisoformat(video_data["scraped_at"])
        if scraped_at < cutoff_date:
            # Supprimer les fichiers
            video_dir = self.cache_dir / "videos" / video_id
            if video_dir.exists():
                shutil.rmtree(video_dir)

            # Retirer de l'index
            del self.index["videos"][video_id]

    self.save_index()
```

---

## 🧪 Vidéo de Test - Swagger Interface

### **URL de Test**

```
https://www.tiktok.com/@swarecito/video/7505706702050823446
```

### **Métadonnées de Test**

```json
{
  "test_video": {
    "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "username": "swarecito",
    "video_id": "7505706702050823446",
    "duration": 97,
    "hashtags": ["chatgpt", "agent", "prompt", "instruction"],
    "language": "fr",
    "engagement_stats": {
      "playCount": 53000,
      "diggCount": 1916,
      "commentCount": 631,
      "shareCount": 302,
      "collectCount": 1807
    },
    "features_pre_publication": {
      "text": "Booste ton ChatGPT avec cet Agent personnalisé 🤖 commente \"INSTRUCTION\" pour l'obtenir",
      "hashtag_count": 4,
      "duration_seconds": 97,
      "language": "fr",
      "has_mentions": false,
      "is_original_audio": true
    }
  }
}
```

### **Exemple de Requête Swagger**

```json
{
  "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
  "scenarios": [
    {
      "name": "Test Publication Matin",
      "description": "Publication 9h avec hashtags trending",
      "publication_hour": 9,
      "publication_day": "monday",
      "hashtags": ["fyp", "viral", "trending"],
      "video_length": 97,
      "has_call_to_action": true
    }
  ],
  "simulation_count": 3
}
```

---

## 📈 Métriques de Performance

### **Temps de Scraping (Moyennes)**

- **Vidéo simple (métadonnées)**: ~10-15 secondes
- **Vidéo avec téléchargement**: ~20-30 secondes
- **Profil (50 vidéos)**: ~2-3 minutes

### **Taille des Fichiers**

- **Vidéo MP4 (540p)**: ~5-15 MB
- **Cover image**: ~50-100 KB
- **Subtitles**: ~1-5 KB
- **Métadonnées JSON**: ~2-5 KB

### **Limitations**

- **Rate limiting**: ~100 requêtes/heure
- **Taille max vidéo**: ~50 MB
- **Durée max scraping**: 30 minutes

---

## 🔄 Workflow Recommandé

### **1. Développement/Test**

```bash
# Utiliser le cache local
python scripts/test_video_scraping.py
python scripts/test_simulation_endpoint.py
```

### **2. Production**

```bash
# Scraping direct + cache
curl -X POST "http://localhost:8000/simulate-virality" \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

### **3. Maintenance**

```bash
# Nettoyer le cache
python scripts/cleanup_cache.py --max-age 30
```

---

## 📚 Références

- **Actor Apify**: https://apify.com/clockworks/tiktok-scraper
- **Documentation API**: https://docs.apify.com/
- **Exemples de payload**: Voir sections ci-dessus
- **Cache local**: `data/apify_cache/`
- **Vidéo de test**: `7505706702050823446`
