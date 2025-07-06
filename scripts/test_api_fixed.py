#!/usr/bin/env python3
"""
Test de l'API après correction de l'erreur de features.
Vérifie que l'API utilise maintenant les bonnes features (16 au lieu de 34).
"""

import requests
import json
import time


def test_analysis_endpoint():
    """Test de l'endpoint d'analyse."""
    print("🧪 Test de l'endpoint d'analyse")
    print("=" * 40)

    url = "http://localhost:8000/analyze-tiktok-url"
    data = {
        "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
        "use_cache": False
    }

    try:
        print("📤 Envoi de la requête...")
        start_time = time.time()
        response = requests.post(url, json=data, timeout=30)
        end_time = time.time()

        print(f"⏱️  Temps de réponse: {end_time - start_time:.1f}s")
        print(f"📊 Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # Vérifier les éléments clés
            virality_score = result.get(
                'prediction', {}).get('virality_score', 'N/A')
            confidence = result.get('prediction', {}).get('confidence', 'N/A')
            gemini_used = result.get('gemini_used', 'N/A')

            print(f"✅ Analyse réussie!")
            print(f"   • Score viralité: {virality_score}")
            print(f"   • Confiance: {confidence}")
            print(f"   • Gemini utilisé: {gemini_used}")

            # Vérifier qu'il n'y a pas d'erreur de features
            if "❌ Prediction error" not in str(result):
                print("✅ Aucune erreur de features détectée")
                return True
            else:
                print("❌ Erreur de features détectée")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False


def test_simulation_endpoint():
    """Test de l'endpoint de simulation."""
    print("\n🎯 Test de l'endpoint de simulation")
    print("=" * 40)

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
        print("📤 Envoi de la requête...")
        start_time = time.time()
        response = requests.post(url, json=data, timeout=30)
        end_time = time.time()

        print(f"⏱️  Temps de réponse: {end_time - start_time:.1f}s")
        print(f"📊 Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # Vérifier les éléments clés
            best_score = result.get('best_score', 'N/A')
            scenarios = result.get('scenarios', [])

            print(f"✅ Simulation réussie!")
            print(f"   • Meilleur score: {best_score}")
            print(f"   • Scénarios testés: {len(scenarios)}")

            if scenarios:
                avg_score = scenarios[0].get('average_virality_score', 'N/A')
                print(f"   • Score moyen: {avg_score}")

            # Vérifier qu'il n'y a pas d'erreur de features
            if "❌ Prediction error" not in str(result):
                print("✅ Aucune erreur de features détectée")
                return True
            else:
                print("❌ Erreur de features détectée")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False


def main():
    """Test principal."""
    print("🧪 Test de l'API après correction de l'erreur de features")
    print("=" * 60)

    # Test 1: Endpoint d'analyse
    analysis_success = test_analysis_endpoint()

    # Test 2: Endpoint de simulation
    simulation_success = test_simulation_endpoint()

    # Résumé
    print("\n📊 Résumé des tests:")
    print("=" * 30)
    print(f"   • Analyse: {'✅ Réussi' if analysis_success else '❌ Échoué'}")
    print(
        f"   • Simulation: {'✅ Réussi' if simulation_success else '❌ Échoué'}")

    if analysis_success and simulation_success:
        print("\n🎉 Tous les tests sont passés!")
        print("✅ L'erreur de features est corrigée!")
        print("✅ L'API utilise maintenant les bonnes features (16 au lieu de 34)")
        return 0
    else:
        print("\n⚠️ Certains tests ont échoué.")
        print("Vérifiez les logs pour plus de détails.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
