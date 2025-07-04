#!/usr/bin/env python3
"""
Script de scraping optimisé pour Virality Chat POC
Basé sur research synthesis et bonnes pratiques
"""
from src.scraping.tiktok_scraper import TikTokScraper
from config.settings import TIKTOK_ACCOUNTS, MAX_VIDEOS_PER_ACCOUNT, RAW_DATA_DIR
from datetime import datetime
import time
import json
import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="TikTok scraping script")
    parser.add_argument(
        "--accounts",
        nargs="+",
        type=str,
        help="List of TikTok accounts to scrape"
    )
    parser.add_argument(
        "--max-videos",
        type=int,
        default=MAX_VIDEOS_PER_ACCOUNT,
        help="Maximum number of videos per account"
    )
    return parser.parse_args()


def main():
    """
    Lancer le scraping de tous les comptes TikTok configurés
    """
    args = parse_args()

    # Use CLI arguments if provided, otherwise use config
    accounts = args.accounts if args.accounts else TIKTOK_ACCOUNTS
    max_videos = args.max_videos

    print("🚀 Démarrage du scraping TikTok - Virality Chat POC")
    print("=" * 60)
    print(f"📊 Configuration:")
    print(f"   • Comptes à scraper : {len(accounts)}")
    print(f"   • Vidéos par compte : {max_videos}")
    print(f"   • Total estimé : {len(accounts) * max_videos} vidéos")
    print("=" * 60)

    # Initialize scraper
    try:
        scraper = TikTokScraper()
        print("✅ Scraper TikTok initialisé")
    except Exception as e:
        print(f"❌ Erreur initialisation scraper: {e}")
        return 1

    # Scraping results
    all_results = []
    failed_accounts = []

    for i, account in enumerate(accounts, 1):
        print(f"\n�� [{i}/{len(accounts)}] Scraping {account}...")

        try:
            # Scrape account
            start_time = time.time()
            result = scraper.scrape_profile(
                username=account,
                max_videos=max_videos
            )

            # Add metadata
            result['scraping_metadata'] = {
                'scraping_duration': time.time() - start_time,
                'scraping_timestamp': datetime.now().isoformat(),
                'account_index': i,
                'target_video_count': max_videos,
                'actual_video_count': len(result.get('videos', []))
            }

            all_results.append(result)

            # Save individual account data
            filename = f"tiktok_{account.replace('@', '').replace('.', '_')}"
            scraper.save_raw_data(result, filename)

            video_count = len(result.get('videos', []))
            print(f"   ✅ {video_count} vidéos récupérées")

            # Rate limiting (respecter les limites API)
            if i < len(accounts):
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
            'total_accounts_targeted': len(accounts),
            'successful_accounts': len(all_results),
            'failed_accounts': len(failed_accounts),
            'total_videos_collected': sum(len(r.get('videos', [])) for r in all_results),
            'scraping_completed_at': datetime.now().isoformat()
        },
        'accounts_data': all_results,
        'failed_accounts': failed_accounts,
        'configuration': {
            'max_videos_per_account': max_videos,
            'target_accounts': accounts
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
    print(f"✅ Comptes réussis : {len(all_results)}/{len(accounts)}")
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
