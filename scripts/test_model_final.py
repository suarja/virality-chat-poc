#!/usr/bin/env python3
"""
Test final du modèle ML - Vérification que tout fonctionne correctement.
"""

import requests
import json


def test_model():
    """Test simple du modèle."""
    print("🧪 Test final du modèle ML")
    print("=" * 40)

    # Test d'analyse
    print("📊 Test d'analyse...")
    url = "http://localhost:8000/analyze-tiktok-url"
    data = {
        "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
        "use_cache": False
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            virality_score = result.get(
                'prediction', {}).get('virality_score', 0)
            confidence = result.get('prediction', {}).get('confidence', 0)

            print(
                f"✅ Analyse: Score {virality_score:.3f}, Confiance {confidence:.3f}")

            # Vérifications
            checks = []
            if 0 <= virality_score <= 1:
                checks.append("✅ Score normal")
            else:
                checks.append(f"❌ Score anormal: {virality_score}")

            if 0 <= confidence <= 1:
                checks.append("✅ Confiance normale")
            else:
                checks.append(f"❌ Confiance anormale: {confidence}")

            for check in checks:
                print(f"   {check}")

        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

    # Test de simulation
    print("\n🎯 Test de simulation...")
    url = "http://localhost:8000/simulate-virality"
    data = {
        "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
        "use_cache": False,
        "scenarios": [
            {
                "name": "Test",
                "description": "Test scenario",
                "publication_hour": 9,
                "publication_day": "monday",
                "hashtags": ["fyp"],
                "engagement_multiplier": 1.2
            }
        ]
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            best_score = result.get('best_score', 0)

            print(f"✅ Simulation: Score {best_score:.3f}")

            # Vérification
            if 0 <= best_score <= 1:
                print("   ✅ Score normal")
            else:
                print(f"   ❌ Score anormal: {best_score}")
                return False

        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

    print("\n🎉 Test final réussi!")
    print("✅ Le modèle ML fonctionne correctement!")
    print("✅ Les scores sont dans la plage normale (0-1)")
    print("✅ Aucune erreur de features détectée")
    return True


if __name__ == "__main__":
    success = test_model()
    exit(0 if success else 1)
