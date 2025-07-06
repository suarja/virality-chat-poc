#!/usr/bin/env python3
"""
🧪 Test du scraping vidéo TikTok direct
🎯 Teste l'actor clockworks/tiktok-scraper avec postURLs
📊 Documente les métadonnées disponibles
"""

import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not API_TOKEN:
    raise ValueError("APIFY_API_TOKEN non défini")

client = ApifyClient(API_TOKEN)


def test_video_scraping():
    """Test du scraping d'une vidéo spécifique"""

    # URL de test
    test_url = "https://www.tiktok.com/@swarecito/video/7505706702050823446"

    # Configuration pour scraping vidéo direct
    run_input = {
        "excludePinnedPosts": False,
        "postURLs": [test_url],
        "proxyCountryCode": "None",
        "resultsPerPage": 100,
        "scrapeRelatedVideos": False,
        "shouldDownloadAvatars": False,
        "shouldDownloadCovers": False,
        "shouldDownloadMusicCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False  # On teste d'abord sans télécharger
    }

    print(f"🔍 Test scraping vidéo: {test_url}")
    print(f"📋 Configuration: {json.dumps(run_input, indent=2)}")

    try:
        # Run the Actor
        run = client.actor(
            "clockworks/tiktok-scraper").call(run_input=run_input)

        print(f"✅ Scraping terminé - Run ID: {run['id']}")

        # Fetch results
        items = []
        dataset = client.dataset(run["defaultDatasetId"])
        if dataset:
            for item in dataset.iterate_items():
                items.append(item)

        print(f"📊 {len(items)} vidéos trouvées")

        if items:
            # Documenter la structure des données
            video_data = items[0]
            print(f"\n📋 Structure des données vidéo:")
            print(f"   - Clés disponibles: {list(video_data.keys())}")

            # Sauvegarder pour analyse
            with open("test_video_scraping_result.json", "w") as f:
                json.dump(items, f, indent=2, default=str)

            print(f"💾 Données sauvegardées dans test_video_scraping_result.json")

            # Analyser les métadonnées importantes
            analyze_video_metadata(video_data)

        return items

    except Exception as e:
        print(f"❌ Erreur scraping: {e}")
        return None


def analyze_video_metadata(video_data):
    """Analyse les métadonnées disponibles"""

    print(f"\n🔍 Analyse des métadonnées:")

    # Métadonnées de base
    basic_fields = [
        'id', 'desc', 'createTime', 'author', 'video', 'stats',
        'music', 'challenges', 'duetInfo', 'originalItem', 'textExtra'
    ]

    for field in basic_fields:
        if field in video_data:
            value = video_data[field]
            if isinstance(value, dict):
                print(f"   ✅ {field}: {list(value.keys())}")
            else:
                print(f"   ✅ {field}: {type(value).__name__}")
        else:
            print(f"   ❌ {field}: Non disponible")

    # Métadonnées spécifiques pour virality prediction
    virality_fields = [
        'stats.playCount', 'stats.diggCount', 'stats.commentCount',
        'stats.shareCount', 'stats.collectCount', 'stats.heartCount'
    ]

    print(f"\n📊 Métadonnées pour prédiction virality:")
    for field in virality_fields:
        keys = field.split('.')
        value = video_data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break

        if value is not None:
            print(f"   ✅ {field}: {value}")
        else:
            print(f"   ❌ {field}: Non disponible")


def test_video_download():
    """Test avec téléchargement de la vidéo pour Gemini"""

    test_url = "https://www.tiktok.com/@swarecito/video/7505706702050823446"

    run_input = {
        "excludePinnedPosts": False,
        "postURLs": [test_url],
        "resultsPerPage": 100,
        "shouldDownloadCovers": True,
        "shouldDownloadSlideshowImages": True,
        "shouldDownloadSubtitles": True,
        "shouldDownloadVideos": True,
        "videoKvStoreIdOrName": "tiktok-videos-test"
    }

    print(f"\n🎥 Test téléchargement vidéo pour Gemini")

    try:
        run = client.actor(
            "clockworks/tiktok-scraper").call(run_input=run_input)
        print(f"✅ Téléchargement terminé - Run ID: {run['id']}")

        # Vérifier les fichiers téléchargés
        dataset = client.dataset(run["defaultDatasetId"])
        items = []
        if dataset:
            items = list(dataset.iterate_items())

        if items:
            video_item = items[0]
            print(f"📁 Fichiers disponibles:")

            # Vérifier les clés de téléchargement
            download_keys = [
                'videoUrl', 'coverUrl', 'slideshowImageUrls',
                'subtitleUrls', 'videoKvStoreId'
            ]

            for key in download_keys:
                if key in video_item:
                    print(f"   ✅ {key}: {video_item[key]}")
                else:
                    print(f"   ❌ {key}: Non disponible")

        return items

    except Exception as e:
        print(f"❌ Erreur téléchargement: {e}")
        return None


if __name__ == "__main__":
    print("🚀 Test du scraping vidéo TikTok direct")
    print("=" * 50)

    # Test 1: Scraping sans téléchargement
    print("\n1️⃣ Test scraping métadonnées")
    test_video_scraping()

    # Test 2: Scraping avec téléchargement
    print("\n2️⃣ Test téléchargement vidéo")
    test_video_download()

    print("\n✅ Tests terminés")
