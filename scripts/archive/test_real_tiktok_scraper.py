# ARCHIVE: Ce script est obsolète ou redondant avec la nouvelle architecture.
# Voir test_video_scraping.py pour le scraping brut et test_pipeline_minimal.py pour le pipeline complet.
#!/usr/bin/env python3
"""
🧪 Script de test pour le vrai scraper TikTok

🎯 Test de la DDD Phase 4: Intégration du vrai scraper Apify
📊 Validation du pipeline complet avec vraies données TikTok
"""
import requests
import json
import time
import os
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"  # Local pour test
# API_BASE_URL = "https://virality-chat-poc-production.up.railway.app"  # Production


def test_api_health():
    """Test de santé de l'API avec statut du scraper"""
    print("\n🏥 Test de santé de l'API")
    print("-" * 30)

    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API en ligne")
            print(
                f"   📊 Features disponibles: {health.get('features_count', 'N/A')}")
            print(
                f"   🤖 Système de features: {health.get('feature_system_available', 'N/A')}")
            print(
                f"   🔗 Scraper TikTok: {health.get('tiktok_scraper_available', 'N/A')}")

            if not health.get('tiktok_scraper_available', False):
                print("   ⚠️  Scraper TikTok non disponible - Vérifiez APIFY_API_TOKEN")
                return False
        else:
            print(f"❌ API hors ligne: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

    return True


def test_tiktok_url_analysis():
    """Test de l'analyse d'URL TikTok avec vrai scraper"""
    print("\n🎬 Test de l'analyse d'URL TikTok (Vrai scraper)")
    print("=" * 60)

    # URLs de test (vraies URLs TikTok)
    test_urls = [
        "https://www.tiktok.com/@tiktok/video/7234567890123456789",  # Exemple
        "https://www.tiktok.com/@creator/video/9876543210987654321",  # Exemple
    ]

    for i, url in enumerate(test_urls, 1):
        print(f"\n📹 Test {i}: {url}")
        print("-" * 40)

        try:
            # Test de l'endpoint
            response = requests.post(
                f"{API_BASE_URL}/analyze-tiktok-url",
                json={"url": url},
                headers={"Content-Type": "application/json"},
                timeout=60  # Plus long pour le scraping
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Succès!")
                print(
                    f"   📊 Score de viralité: {result['prediction']['virality_score']:.3f}")
                print(
                    f"   🎯 Confiance: {result['prediction']['confidence']:.3f}")
                print(
                    f"   ⏱️  Temps d'analyse: {result['analysis_time']:.3f}s")
                print(f"   🔢 Nombre de features: {len(result['features'])}")
                print(
                    f"   💡 Recommandations: {len(result['prediction']['recommendations'])}")

                # Afficher quelques données récupérées
                video_data = result['video_data']
                print(f"   📹 Données vidéo:")
                print(
                    f"      - Titre: {video_data.get('text', 'N/A')[:50]}...")
                print(f"      - Durée: {video_data.get('duration', 'N/A')}s")
                print(f"      - Vues: {video_data.get('playCount', 'N/A')}")
                print(f"      - Likes: {video_data.get('diggCount', 'N/A')}")

            else:
                print(f"❌ Erreur {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")

        time.sleep(2)  # Pause entre les tests


def test_tiktok_profile_analysis():
    """Test de l'analyse de profil TikTok"""
    print("\n👤 Test de l'analyse de profil TikTok")
    print("=" * 50)

    # Profils de test (vrais usernames TikTok)
    test_profiles = [
        {"username": "tiktok", "max_videos": 5},  # Compte officiel TikTok
        {"username": "creator", "max_videos": 3},  # Exemple
    ]

    for i, profile in enumerate(test_profiles, 1):
        print(f"\n👤 Test {i}: @{profile['username']}")
        print("-" * 40)

        try:
            # Test de l'endpoint
            response = requests.post(
                f"{API_BASE_URL}/analyze-tiktok-profile",
                json=profile,
                headers={"Content-Type": "application/json"},
                timeout=120  # Très long pour le scraping de profil
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Succès!")
                print(
                    f"   📊 Vidéos analysées: {result['profile_stats']['total_videos_analyzed']}")
                print(
                    f"   🎯 Score viralité moyen: {result['profile_stats']['average_virality_score']:.3f}")
                print(
                    f"   ⏱️  Temps d'analyse: {result['analysis_time']:.3f}s")

                # Afficher les top vidéos
                top_videos = result['profile_stats']['top_viral_videos']
                if top_videos:
                    print(
                        f"   🔥 Top vidéo: {top_videos[0]['prediction']['virality_score']:.3f}")

            else:
                print(f"❌ Erreur {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")

        time.sleep(5)  # Pause plus longue entre les profils


def check_apify_token():
    """Vérifie si le token Apify est configuré"""
    print("\n🔑 Vérification du token Apify")
    print("-" * 30)

    # Vérifier les variables d'environnement
    apify_token = os.getenv("APIFY_API_TOKEN")
    if apify_token:
        print(f"✅ Token Apify trouvé: {apify_token[:10]}...")
        return True
    else:
        print("❌ Token Apify non trouvé")
        print("   💡 Ajoutez APIFY_API_TOKEN dans votre fichier .env")
        return False


if __name__ == "__main__":
    print("🚀 Démarrage des tests DDD Phase 4 - Vrai scraper")
    print("=" * 60)

    # Vérifier le token Apify
    if not check_apify_token():
        print("\n⚠️  Tests limités sans token Apify")

    # Test de santé
    if not test_api_health():
        print("\n❌ API non disponible, arrêt des tests")
        exit(1)

    # Tests avec vrai scraper
    test_tiktok_url_analysis()
    test_tiktok_profile_analysis()

    print("\n🎉 Tests terminés!")
    print("\n💡 Note: Les tests utilisent de vraies URLs TikTok.")
    print("   Assurez-vous d'avoir un token Apify valide pour les tests complets.")
