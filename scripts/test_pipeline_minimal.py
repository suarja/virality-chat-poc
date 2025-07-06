#!/usr/bin/env python3
"""
Test minimal du pipeline avec 1 compte et 2 vidéos maximum.
Vérifie que le pipeline complet fonctionne après la refactorisation.
"""

import subprocess
import sys
import time
from pathlib import Path


def test_pipeline_minimal():
    """Test du pipeline avec paramètres minimaux."""
    print("🧪 Test minimal du pipeline TikTok Virality Prediction")
    print("=" * 60)

    # Paramètres de test
    dataset = "test_minimal"
    batch_size = 1
    videos_per_account = 2
    max_total_videos = 2
    feature_set = "metadata"

    print(f"📊 Paramètres de test:")
    print(f"   • Dataset: {dataset}")
    print(f"   • Batch size: {batch_size}")
    print(f"   • Vidéos par compte: {videos_per_account}")
    print(f"   • Total max: {max_total_videos}")
    print(f"   • Feature set: {feature_set}")
    print()

    # Commande de test
    cmd = [
        "python3", "scripts/run_pipeline.py",
        "--dataset", dataset,
        "--batch-size", str(batch_size),
        "--videos-per-account", str(videos_per_account),
        "--max-total-videos", str(max_total_videos),
        "--feature-set", feature_set
    ]

    print("🚀 Lancement du pipeline...")
    print(f"Commande: {' '.join(cmd)}")
    print()

    try:
        # Exécuter le pipeline
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True,
                                text=True, timeout=300)  # 5 minutes max
        end_time = time.time()

        print("📋 Résultats:")
        print(f"   • Durée: {end_time - start_time:.1f} secondes")
        print(f"   • Code de sortie: {result.returncode}")
        print()

        if result.returncode == 0:
            print("✅ Pipeline exécuté avec succès!")

            # Vérifier les fichiers générés
            dataset_dir = Path(f"data/dataset_{dataset}")
            if dataset_dir.exists():
                print("📁 Fichiers générés:")

                # Vérifier les données scrapées
                batch_files = list(dataset_dir.glob("batch_*.json"))
                if batch_files:
                    print(
                        f"   • Données scrapées: {len(batch_files)} fichiers")

                # Vérifier les analyses Gemini
                gemini_dir = dataset_dir / "gemini_analysis"
                if gemini_dir.exists():
                    analysis_files = list(gemini_dir.rglob("*.json"))
                    print(
                        f"   • Analyses Gemini: {len(analysis_files)} fichiers")

                # Vérifier les features
                features_dir = dataset_dir / "features"
                if features_dir.exists():
                    feature_files = list(features_dir.glob("*.csv"))
                    print(
                        f"   • Features extraites: {len(feature_files)} fichiers")

                    # Vérifier l'agrégation
                    aggregated_files = list(
                        features_dir.glob("aggregated_*.csv"))
                    if aggregated_files:
                        print(
                            f"   • Features agrégées: {len(aggregated_files)} fichiers")

            print()
            print("🎯 Test réussi! Le pipeline fonctionne correctement.")
            return True

        else:
            print("❌ Pipeline échoué!")
            print("Erreur de sortie:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Timeout: Le pipeline a pris trop de temps (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False


def test_api_endpoints():
    """Test des endpoints de l'API."""
    print("\n🌐 Test des endpoints API")
    print("=" * 40)

    # Test de l'endpoint d'analyse
    print("📊 Test endpoint d'analyse...")
    try:
        import requests
        import json

        url = "http://localhost:8000/analyze-tiktok-url"
        data = {
            "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
            "use_cache": True
        }

        response = requests.post(url, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Analyse réussie")
            print(
                f"   • Score viralité: {result.get('prediction', {}).get('virality_score', 'N/A')}")
            print(
                f"   • Confiance: {result.get('prediction', {}).get('confidence', 'N/A')}")
            print(f"   • Gemini utilisé: {result.get('gemini_used', 'N/A')}")
            return True
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Erreur de test API: {e}")
        return False


def main():
    """Fonction principale de test."""
    print("🧪 Test complet du système TikTok Virality Prediction")
    print("=" * 70)

    # Test 1: Pipeline minimal
    pipeline_success = test_pipeline_minimal()

    # Test 2: API endpoints (si le pipeline a réussi)
    api_success = False
    if pipeline_success:
        api_success = test_api_endpoints()

    # Résumé final
    print("\n📊 Résumé des tests:")
    print("=" * 30)
    print(f"   • Pipeline: {'✅ Réussi' if pipeline_success else '❌ Échoué'}")
    print(f"   • API: {'✅ Réussi' if api_success else '❌ Échoué'}")

    if pipeline_success and api_success:
        print("\n🎉 Tous les tests sont passés!")
        print("✅ Le système fonctionne correctement après la refactorisation.")
        return 0
    else:
        print("\n⚠️ Certains tests ont échoué.")
        print("Vérifiez les logs pour plus de détails.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
