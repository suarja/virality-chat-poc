#!/usr/bin/env python3
"""
Script de scraping optimisé pour Virality Chat POC
Basé sur research synthesis et bonnes pratiques
"""

from config.settings import TIKTOK_ACCOUNTS, MAX_VIDEOS_PER_ACCOUNT, RAW_DATA_DIR
from src.scraping.tiktok_scraper import TikTokScraper
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """
    Lancer le scraping de tous les comptes TikTok configurés
    """
    print("🚀 Démarrage du scraping TikTok - Virality Chat POC")
    print("=" * 60)
    print(f"📊 Configuration:")
    print(f"   • Comptes à scraper : {len(TIKTOK_ACCOUNTS)}")
    print(f"   • Vidéos par compte : {MAX_VIDEOS_PER_ACCOUNT}")
    print(
        f"   • Total estimé : {len(TIKTOK_ACCOUNTS) * MAX_VIDEOS_PER_ACCOUNT} vidéos")
    print("=" * 60)

    # Initialize scraper
    try:
        scraper = TikTokScraper()
        print("✅ Scraper TikTok initialisé")
    except Exception as e:
        print(f"❌ Erreur initialisation scraper: {e}")
        return

    # Scraping results
    all_results = []
    failed_accounts = []

    for i, account in enumerate(TIKTOK_ACCOUNTS, 1):
        print(f"\n🎯 [{i}/{len(TIKTOK_ACCOUNTS)}] Scraping {account}...")

        try:
            # Scrape account
            start_time = time.time()
            result = scraper.scrape_profile(
                username=account,
                max_videos=MAX_VIDEOS_PER_ACCOUNT
            )

            # Add metadata
            result['scraping_metadata'] = {
                'scraping_duration': time.time() - start_time,
                'scraping_timestamp': datetime.now().isoformat(),
                'account_index': i,
                'target_video_count': MAX_VIDEOS_PER_ACCOUNT,
                'actual_video_count': len(result.get('videos', []))
            }

            all_results.append(result)

            # Save individual account data
            filename = f"tiktok_{account.replace('@', '').replace('.', '_')}"
            scraper.save_raw_data(result, filename)

            video_count = len(result.get('videos', []))
            print(f"   ✅ {video_count} vidéos récupérées")

            # Rate limiting (respecter les limites API)
            if i < len(TIKTOK_ACCOUNTS):
                print("   ⏳ Pause anti-rate-limit (30s)...")
                time.sleep(30)

        except Exception as e:
            print(f"   ❌ Erreur pour {account}: {e}")
            failed_accounts.append({
                'account': account,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            continue

    # Save consolidated results
    print(f"\n📊 Sauvegarde des résultats consolidés...")

    consolidated_data = {
        'scraping_summary': {
            'total_accounts_targeted': len(TIKTOK_ACCOUNTS),
            'successful_accounts': len(all_results),
            'failed_accounts': len(failed_accounts),
            'total_videos_collected': sum(len(r.get('videos', [])) for r in all_results),
            'scraping_completed_at': datetime.now().isoformat()
        },
        'accounts_data': all_results,
        'failed_accounts': failed_accounts,
        'configuration': {
            'max_videos_per_account': MAX_VIDEOS_PER_ACCOUNT,
            'target_accounts': TIKTOK_ACCOUNTS
        }
    }

    # Save to consolidated file
    consolidated_file = RAW_DATA_DIR / \
        f"tiktok_consolidated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(consolidated_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, ensure_ascii=False, indent=2)

    # Print final summary
    print("=" * 60)
    print("🎉 SCRAPING TERMINÉ!")
    print("=" * 60)
    print(f"✅ Comptes réussis : {len(all_results)}/{len(TIKTOK_ACCOUNTS)}")
    print(
        f"📹 Total vidéos : {consolidated_data['scraping_summary']['total_videos_collected']}")
    print(f"💾 Données sauvées : {consolidated_file}")

    if failed_accounts:
        print(f"⚠️  Comptes échoués : {len(failed_accounts)}")
        for failed in failed_accounts:
            print(f"   • {failed['account']}: {failed['error']}")

    print(f"\n🎯 Prochaines étapes:")
    print(f"   1. Vérifier les données : ls -la {RAW_DATA_DIR}")
    print(f"   2. Lancer l'exploration : jupyter notebook notebooks/01_data_exploration.ipynb")
    print(f"   3. Démarrer l'analyse vidéo (Phase 2)")


if __name__ == "__main__":
    main()
