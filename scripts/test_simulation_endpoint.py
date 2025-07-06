#!/usr/bin/env python3
"""
🧪 Test de l'endpoint de simulation pre-publication
🎯 Teste différents scénarios de publication pour optimiser la viralité
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_VIDEO_URL = "https://www.tiktok.com/@swarecito/video/7505706702050823446"


def test_simulation_endpoint():
    """Test de l'endpoint de simulation"""

    # Scénarios de test
    scenarios = [
        {
            "name": "Publication matin optimale",
            "description": "Test publication 9h du matin avec hashtags trending",
            "publication_hour": 9,
            "publication_day": "monday",
            "hashtags": ["fyp", "viral", "trending"],
            "trending_hashtags": ["fyp", "viral"],
            "video_length": 30,
            "has_text_overlays": True,
            "has_transitions": False,
            "has_call_to_action": True,
            "engagement_multiplier": 1.2,
            "reach_multiplier": 1.1
        },
        {
            "name": "Publication soir optimale",
            "description": "Test publication 21h avec engagement boost",
            "publication_hour": 21,
            "publication_day": "friday",
            "hashtags": ["fyp", "comedy", "funny"],
            "trending_hashtags": ["fyp", "comedy"],
            "video_length": 45,
            "has_text_overlays": False,
            "has_transitions": True,
            "has_call_to_action": True,
            "engagement_multiplier": 1.5,
            "reach_multiplier": 1.3
        },
        {
            "name": "Publication weekend",
            "description": "Test publication weekend avec hashtags personnalisés",
            "publication_hour": 14,
            "publication_day": "saturday",
            "hashtags": ["fyp", "weekend", "vibes"],
            "custom_hashtags": ["weekend", "vibes"],
            "video_length": 60,
            "has_text_overlays": True,
            "has_transitions": True,
            "has_call_to_action": False,
            "engagement_multiplier": 1.0,
            "reach_multiplier": 1.0
        }
    ]

    # Requête de simulation
    request_data = {
        "video_url": TEST_VIDEO_URL,
        "scenarios": scenarios,
        "include_post_publication": False,
        "simulation_count": 3
    }

    print(f"🎯 Test simulation pre-publication")
    print(f"📹 URL vidéo: {TEST_VIDEO_URL}")
    print(f"📊 Scénarios: {len(scenarios)}")
    print(f"🔄 Simulations par scénario: {request_data['simulation_count']}")
    print("=" * 60)

    try:
        # Appel à l'endpoint
        response = requests.post(
            f"{API_BASE_URL}/simulate-virality",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()

            print(f"✅ Simulation réussie!")
            print(f"📊 Score original: {result['original_virality_score']:.3f}")
            print(f"🏆 Meilleur scénario: {result['best_scenario']}")
            print(f"🎯 Meilleur score: {result['best_score']:.3f}")
            print(
                f"📈 Potentiel d'amélioration: {result['summary']['improvement_potential']:.3f}")
            print(
                f"⏱️ Temps d'analyse: {result['summary']['analysis_time']:.2f}s")

            print(f"\n📋 Résultats par scénario:")
            for scenario in result['scenarios']:
                print(f"\n🎭 {scenario['scenario_name']}")
                print(f"   📝 {scenario['scenario_description']}")
                print(
                    f"   📊 Score moyen: {scenario['average_virality_score']:.3f}")
                print(f"   🏆 Meilleur: {scenario['best_virality_score']:.3f}")
                print(f"   📉 Pire: {scenario['worst_virality_score']:.3f}")

                if scenario['recommendations']:
                    print(f"   💡 Recommandations:")
                    for rec in scenario['recommendations']:
                        print(f"      • {rec}")

            # Sauvegarder les résultats
            with open("simulation_results.json", "w") as f:
                json.dump(result, f, indent=2, default=str)

            print(f"\n💾 Résultats sauvegardés dans simulation_results.json")

        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")


def test_health_check():
    """Test du health check"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API en ligne")
            print(f"   - Modèle ML: {data.get('model_loaded', False)}")
            print(
                f"   - Features: {data.get('feature_system_available', False)}")
            print(
                f"   - Scraper: {data.get('tiktok_scraper_available', False)}")
            print(
                f"   - Simulation: {data.get('simulation_service_available', False)}")
            return True
        else:
            print(f"❌ API hors ligne: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion API: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Test de l'endpoint de simulation TikTok")
    print("=" * 60)

    # Test 1: Health check
    print("\n1️⃣ Test health check")
    if not test_health_check():
        print("❌ API non disponible, arrêt du test")
        exit(1)

    # Test 2: Simulation
    print("\n2️⃣ Test simulation pre-publication")
    test_simulation_endpoint()

    print("\n✅ Tests terminés")
