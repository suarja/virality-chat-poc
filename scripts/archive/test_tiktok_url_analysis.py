#!/usr/bin/env python3
# ARCHIVE: Ce script est obsolète ou redondant avec la nouvelle architecture.
# Voir test_model_diagnostics.py pour l'analyse d'URL TikTok.

"""
🧪 Script de test pour l'analyse d'URL TikTok

🎯 Test de la DDD Phase 4: Analyse de vidéos TikTok via URL
📊 Validation du pipeline complet URL → features → prédiction
"""
import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000"  # Local pour test
# API_BASE_URL = "https://virality-chat-poc-production.up.railway.app"  # Production


def test_tiktok_url_analysis():
    """Test de l'analyse d'URL TikTok"""

    # URLs de test
    test_urls = [
        "https://www.tiktok.com/@user123/video/1234567890123456789",
        "https://www.tiktok.com/@creator/video/9876543210987654321",
        "https://vm.tiktok.com/ABC123/",  # URL raccourcie (doit échouer)
        # URL invalide (doit échouer)
        "https://www.youtube.com/watch?v=invalid"
    ]

    print("🎬 Test de l'analyse d'URL TikTok")
    print("=" * 50)

    for i, url in enumerate(test_urls, 1):
        print(f"\n📹 Test {i}: {url}")
        print("-" * 30)

        try:
            # Test de l'endpoint
            response = requests.post(
                f"{API_BASE_URL}/analyze-tiktok-url",
                json={"url": url},
                headers={"Content-Type": "application/json"},
                timeout=30
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

            else:
                print(f"❌ Erreur {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")

        time.sleep(1)  # Pause entre les tests


def test_api_health():
    """Test de santé de l'API"""
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
        else:
            print(f"❌ API hors ligne: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")


if __name__ == "__main__":
    print("🚀 Démarrage des tests DDD Phase 4")
    print("=" * 50)

    # Test de santé
    test_api_health()

    # Test d'analyse d'URL
    test_tiktok_url_analysis()

    print("\n🎉 Tests terminés!")
