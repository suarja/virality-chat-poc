#!/usr/bin/env python3
"""
Script de test scraping - Validation rapide sur un compte
"""

from config.settings import TEST_ACCOUNTS, RAW_DATA_DIR
from src.scraping.tiktok_scraper import TikTokScraper
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_single_account(account: str, max_videos: int = 5):
    """
    Tester le scraping sur un seul compte

    Args:
        account: Nom du compte (ex: @leaelui)
        max_videos: Nombre max de vidéos à scraper
    """
    print(f"🧪 Test scraping sur {account}")
    print("=" * 50)

    try:
        # Initialize scraper
        scraper = TikTokScraper()
        print("✅ Scraper initialisé")

        # Start scraping
        print(f"🎯 Scraping {max_videos} vidéos de {account}...")
        start_time = time.time()

        result = scraper.scrape_profile(
            username=account,
            max_videos=max_videos
        )

        duration = time.time() - start_time

        # Analyze results
        videos = result.get('videos', [])
        video_count = len(videos)

        print(f"⏱️  Durée: {duration:.2f}s")
        print(f"📹 Vidéos collectées: {video_count}")

        if video_count > 0:
            # Sample analysis
            sample_video = videos[0]
            print(f"\n📊 Échantillon vidéo 1:")
            print(f"   • Vues: {sample_video.get('playCount', 'N/A')}")
            print(f"   • Likes: {sample_video.get('diggCount', 'N/A')}")
            print(
                f"   • Commentaires: {sample_video.get('commentCount', 'N/A')}")
            print(f"   • Partages: {sample_video.get('shareCount', 'N/A')}")
            print(f"   • Durée: {sample_video.get('duration', 'N/A')}s")
            print(
                f"   • Description: {sample_video.get('desc', 'N/A')[:50]}...")

        # Save test data
        test_filename = f"test_{account.replace('@', '').replace('.', '_')}_{datetime.now().strftime('%H%M%S')}"
        scraper.save_raw_data(result, test_filename)

        print(f"\n💾 Données sauvées: {RAW_DATA_DIR / f'{test_filename}.json'}")

        # Validate data structure
        required_fields = ['username', 'scraped_at', 'videos']
        missing_fields = [
            field for field in required_fields if field not in result]

        if missing_fields:
            print(f"⚠️  Champs manquants: {missing_fields}")
            return False

        print("✅ Structure des données validée")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False


def main():
    """
    Lancer les tests de scraping
    """
    print("🚀 Tests de Scraping - Virality Chat POC")
    print("=" * 60)

    # Test avec le compte principal
    test_account = TEST_ACCOUNTS[0]  # @leaelui par défaut

    print(f"🎯 Compte de test: {test_account}")
    print(f"📹 Vidéos max: 5")
    print(f"💾 Stockage: {RAW_DATA_DIR}")
    print()

    # Run test
    success = test_single_account(test_account, max_videos=5)

    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST RÉUSSI!")
        print("✅ Le scraping fonctionne correctement")
        print("\n🎯 Prochaines étapes:")
        print("   1. Examiner les données: ls -la data/raw/")
        print("   2. Lancer scraping complet: python scripts/run_scraping.py")
        print("   3. Commencer l'exploration: jupyter notebook")
    else:
        print("❌ TEST ÉCHOUÉ!")
        print("🔧 Vérifiez:")
        print("   • Clés API dans .env")
        print("   • Connexion internet")
        print("   • Limites API Apify")


def interactive_test():
    """
    Test interactif - permet de choisir le compte
    """
    print("🧪 Test Scraping Interactif")
    print("=" * 40)

    print("Comptes disponibles:")
    for i, account in enumerate(TEST_ACCOUNTS, 1):
        print(f"   {i}. {account}")

    try:
        choice = input(
            "\nChoisissez un compte (1-3) ou tapez un @compte: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(TEST_ACCOUNTS):
                account = TEST_ACCOUNTS[idx]
            else:
                print("❌ Choix invalide")
                return
        elif choice.startswith('@'):
            account = choice
        else:
            account = f"@{choice}"

        max_videos = input("Nombre de vidéos (défaut: 5): ").strip()
        max_videos = int(max_videos) if max_videos.isdigit() else 5

        test_single_account(account, max_videos)

    except KeyboardInterrupt:
        print("\n👋 Test annulé")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_test()
        else:
            # Test avec compte spécifique
            account = sys.argv[1]
            max_videos = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            test_single_account(account, max_videos)
    else:
        main()
