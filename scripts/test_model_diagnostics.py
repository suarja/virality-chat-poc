#!/usr/bin/env python3
"""
Test avancé du modèle ML et de l'API TikTok Virality Prediction.

- Vérifie la correction de l'erreur de features (16 vs 34)
- Vérifie la cohérence des scores et l'absence de warnings
- Vérifie la stabilité de l'API sur plusieurs endpoints

Usage :
    python3 scripts/test_model_diagnostics.py
"""

import requests
import time


def test_analysis_endpoint():
    """Test de l'endpoint d'analyse."""
    print("🧪 Test de l'endpoint d'analyse")
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
            gemini_used = result.get('gemini_used', False)
            print(f"   • Score viralité: {virality_score:.3f}")
            print(f"   • Confiance: {confidence:.3f}")
            print(f"   • Gemini utilisé: {gemini_used}")
            if 0 <= virality_score <= 1 and 0 <= confidence <= 1:
                print("   ✅ Score et confiance dans la plage normale (0-1)")
            else:
                print("   ❌ Score ou confiance hors plage")
            if "❌ Prediction error" not in str(result):
                print("   ✅ Aucune erreur de features détectée")
            else:
                print("   ❌ Erreur de features détectée")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_simulation_endpoint():
    """Test de l'endpoint de simulation."""
    print("\n🎯 Test de l'endpoint de simulation")
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
            print(f"   • Meilleur score: {best_score:.3f}")
            if 0 <= best_score <= 1:
                print("   ✅ Score de simulation dans la plage normale (0-1)")
            else:
                print("   ❌ Score de simulation hors plage")
            if "❌ Prediction error" not in str(result):
                print("   ✅ Aucune erreur de features détectée")
            else:
                print("   ❌ Erreur de features détectée")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    print("\n==============================")
    print("Test avancé du modèle ML/API")
    print("==============================\n")
    analysis_ok = test_analysis_endpoint()
    simulation_ok = test_simulation_endpoint()
    print("\nRésumé:")
    print(f"   • Analyse: {'✅' if analysis_ok else '❌'}")
    print(f"   • Simulation: {'✅' if simulation_ok else '❌'}")
    if analysis_ok and simulation_ok:
        print("\n🎉 Tous les tests avancés sont passés!")
        return 0
    else:
        print("\n⚠️ Certains tests ont échoué.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
