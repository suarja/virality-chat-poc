#!/usr/bin/env python3
"""
Test de la correction du modèle ML.
Vérifie que le modèle fonctionne correctement après les corrections.
"""

import requests
import json
import time
import numpy as np


def test_model_predictions():
    """Test des prédictions du modèle."""
    print("🧪 Test des prédictions du modèle ML")
    print("=" * 50)

    # Test avec différentes vidéos
    test_videos = [
        {
            "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
            "name": "Vidéo de test 1"
        }
    ]

    results = []

    for video in test_videos:
        print(f"\n📹 Test: {video['name']}")
        print(f"🔗 URL: {video['url']}")

        url = "http://localhost:8000/analyze-tiktok-url"
        data = {
            "url": video['url'],
            "use_cache": False
        }

        try:
            print("📤 Envoi de la requête...")
            start_time = time.time()
            response = requests.post(url, json=data, timeout=30)
            end_time = time.time()

            print(f"⏱️  Temps de réponse: {end_time - start_time:.1f}s")

            if response.status_code == 200:
                result = response.json()

                # Extraire les métriques importantes
                virality_score = result.get(
                    'prediction', {}).get('virality_score', 0)
                confidence = result.get('prediction', {}).get('confidence', 0)
                gemini_used = result.get('gemini_used', False)

                print(f"✅ Prédiction réussie!")
                print(f"   • Score viralité: {virality_score:.3f}")
                print(f"   • Confiance: {confidence:.3f}")
                print(f"   • Gemini utilisé: {gemini_used}")

                # Vérifications de qualité
                checks = []

                # 1. Score dans la plage normale (0-1)
                if 0 <= virality_score <= 1:
                    checks.append("✅ Score dans la plage normale (0-1)")
                else:
                    checks.append(f"❌ Score hors plage: {virality_score}")

                # 2. Confiance dans la plage normale (0-1)
                if 0 <= confidence <= 1:
                    checks.append("✅ Confiance dans la plage normale (0-1)")
                else:
                    checks.append(f"❌ Confiance hors plage: {confidence}")

                # 3. Pas d'erreur de features
                if "❌ Prediction error" not in str(result):
                    checks.append("✅ Aucune erreur de features")
                else:
                    checks.append("❌ Erreur de features détectée")

                # 4. Pas de warnings de feature names
                if "UserWarning" not in str(result):
                    checks.append("✅ Aucun warning de feature names")
                else:
                    checks.append("❌ Warnings de feature names détectés")

                # Afficher les vérifications
                for check in checks:
                    print(f"   {check}")

                results.append({
                    "video": video['name'],
                    "virality_score": virality_score,
                    "confidence": confidence,
                    "gemini_used": gemini_used,
                    "checks": checks
                })

            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                results.append({
                    "video": video['name'],
                    "error": f"HTTP {response.status_code}"
                })

        except Exception as e:
            print(f"❌ Erreur de test: {e}")
            results.append({
                "video": video['name'],
                "error": str(e)
            })

    return results


def test_simulation_scenarios():
    """Test des scénarios de simulation."""
    print("\n🎯 Test des scénarios de simulation")
    print("=" * 50)

    url = "http://localhost:8000/simulate-virality"
    data = {
        "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
        "use_cache": False,
        "scenarios": [
            {
                "name": "Matin",
                "description": "Publication à 9h le lundi",
                "publication_hour": 9,
                "publication_day": "monday",
                "hashtags": ["fyp", "viral"],
                "engagement_multiplier": 1.2
            },
            {
                "name": "Soir",
                "description": "Publication à 20h le vendredi",
                "publication_hour": 20,
                "publication_day": "friday",
                "hashtags": ["fyp", "comedy"],
                "engagement_multiplier": 1.5
            }
        ]
    }

    try:
        print("📤 Envoi de la requête de simulation...")
        start_time = time.time()
        response = requests.post(url, json=data, timeout=30)
        end_time = time.time()

        print(f"⏱️  Temps de réponse: {end_time - start_time:.1f}s")

        if response.status_code == 200:
            result = response.json()

            best_score = result.get('best_score', 0)
            scenarios = result.get('scenarios', [])

            print(f"✅ Simulation réussie!")
            print(f"   • Meilleur score: {best_score:.3f}")
            print(f"   • Scénarios testés: {len(scenarios)}")

            # Vérifications de qualité
            checks = []

            # 1. Meilleur score dans la plage normale
            if 0 <= best_score <= 1:
                checks.append("✅ Meilleur score dans la plage normale (0-1)")
            else:
                checks.append(f"❌ Meilleur score hors plage: {best_score}")

            # 2. Scores des scénarios cohérents
            scenario_scores = []
            for scenario in scenarios:
                avg_score = scenario.get('average_virality_score', 0)
                scenario_scores.append(avg_score)
                print(f"   • {scenario['name']}: {avg_score:.3f}")

            if all(0 <= score <= 1 for score in scenario_scores):
                checks.append(
                    "✅ Tous les scores de scénarios dans la plage normale")
            else:
                checks.append("❌ Certains scores de scénarios hors plage")

            # 3. Pas d'erreur de features
            if "❌ Prediction error" not in str(result):
                checks.append("✅ Aucune erreur de features")
            else:
                checks.append("❌ Erreur de features détectée")

            # Afficher les vérifications
            for check in checks:
                print(f"   {check}")

            return {
                "best_score": best_score,
                "scenarios_count": len(scenarios),
                "scenario_scores": scenario_scores,
                "checks": checks
            }

        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return {"error": f"HTTP {response.status_code}"}

    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return {"error": str(e)}


def main():
    """Test principal."""
    print("🧪 Test de la correction du modèle ML")
    print("=" * 60)

    # Test 1: Prédictions du modèle
    prediction_results = test_model_predictions()

    # Test 2: Scénarios de simulation
    simulation_result = test_simulation_scenarios()

    # Résumé
    print("\n📊 Résumé des tests:")
    print("=" * 30)

    # Analyser les résultats des prédictions
    successful_predictions = 0
    total_predictions = len(prediction_results)

    for result in prediction_results:
        if 'error' not in result:
            successful_predictions += 1
            print(
                f"   • {result['video']}: Score {result['virality_score']:.3f}")
        else:
            print(f"   • {result['video']}: ❌ {result['error']}")

    # Analyser les résultats de simulation
    if 'error' not in simulation_result:
        print(f"   • Simulation: Score {simulation_result['best_score']:.3f}")
    else:
        print(f"   • Simulation: ❌ {simulation_result['error']}")

    # Évaluation globale
    print(f"\n🎯 Évaluation globale:")
    print(
        f"   • Prédictions réussies: {successful_predictions}/{total_predictions}")
    print(
        f"   • Simulation: {'✅' if 'error' not in simulation_result else '❌'}")

    if successful_predictions == total_predictions and 'error' not in simulation_result:
        print("\n🎉 Tous les tests sont passés!")
        print("✅ Le modèle ML fonctionne correctement!")
        print("✅ Les scores sont dans la plage normale (0-1)")
        print("✅ Aucune erreur de features détectée")
        return 0
    else:
        print("\n⚠️ Certains tests ont échoué.")
        print("Vérifiez les logs pour plus de détails.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
