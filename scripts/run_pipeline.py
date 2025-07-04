#!/usr/bin/env python3
"""
Complete pipeline script for TikTok virality analysis with batch processing:
1. Scrape TikTok videos in batches
2. Run Gemini analysis
3. Extract and process features
"""
from src.features.data_processor import DataProcessor
from src.scraping.tiktok_scraper import TikTokScraper
from src.utils.batch_tracker import BatchTracker
from src.utils.data_validator import DataValidator
from config.settings import TIKTOK_ACCOUNTS
import argparse
import json
import logging
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run complete TikTok virality analysis pipeline with batch processing"
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Dataset name (e.g. v1, test)"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of accounts to process in each batch (default: 5)"
    )

    parser.add_argument(
        "--videos-per-account",
        type=int,
        default=15,
        help="Number of videos to analyze per account (default: 15)"
    )

    parser.add_argument(
        "--max-total-videos",
        type=int,
        default=500,
        help="Maximum total number of videos to analyze (default: 500)"
    )

    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry accounts that failed in previous runs"
    )

    parser.add_argument(
        "--retry-phase",
        choices=['scraping', 'analysis', 'features'],
        help="Only retry specific phase for failed accounts"
    )

    return parser.parse_args()


def setup_logging(dataset_name: str):
    """Setup logging configuration."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Setup handlers
    handlers = [
        logging.FileHandler(f'logs/pipeline_{dataset_name}.log'),
        logging.StreamHandler()
    ]

    # Add error log if not exists
    error_handler = logging.FileHandler('logs/errors.log')
    error_handler.setLevel(logging.ERROR)
    handlers.append(error_handler)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    return logging.getLogger(__name__)


def run_scraping_phase(accounts: List[str], max_videos: int, tracker: BatchTracker) -> List[Dict]:
    """Run TikTok scraping phase for a batch of accounts."""
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 Starting TikTok scraping for {len(accounts)} accounts...")

    validator = DataValidator()
    results = []

    for account in accounts:
        try:
            scraper = TikTokScraper()
            account_results = scraper.scrape_multiple_profiles(
                [account], max_videos)

            # Validate account data
            for result in account_results:
                is_valid, errors = validator.validate_account(result)
                if not is_valid:
                    logger.error(
                        f"❌ Account {account} failed validation: {', '.join(errors)}")
                    tracker.mark_account_failed(
                        account, "scraping", f"Validation failed: {', '.join(errors)}")
                    continue

                # Filter valid videos
                valid_videos = validator.filter_valid_videos(
                    result.get('videos', []))
                if len(valid_videos) == 0:
                    logger.error(
                        f"❌ Account {account} has no valid videos after filtering")
                    tracker.mark_account_failed(
                        account, "scraping", "No valid videos after filtering")
                    continue

                # Update result with filtered videos
                result['videos'] = valid_videos
                results.append(result)
                logger.info(
                    f"✅ Successfully scraped and validated account: {account} ({len(valid_videos)} valid videos)")

        except Exception as e:
            error_msg = f"Scraping failed: {str(e)}"
            logger.error(error_msg)
            tracker.mark_account_failed(account, "scraping", error_msg)
            continue

    return results


def run_gemini_phase(videos: List[Dict], account: str, tracker: BatchTracker):
    """Run Gemini analysis phase for a batch of videos."""
    logger = logging.getLogger(__name__)
    logger.info(
        f"🧠 Starting Gemini analysis for {len(videos)} videos from {account}")

    validator = DataValidator()

    try:
        from scripts.test_gemini import analyze_tiktok_video

        date_str = datetime.now().strftime("%Y%m%d")
        analysis_dir = Path("data/gemini_analysis") / account / date_str
        analysis_dir.mkdir(parents=True, exist_ok=True)

        successful_analyses = 0
        for video in videos:
            video_url = video.get("webVideoUrl")
            if not video_url:
                continue

            video_id = video_url.split("/")[-1]
            output_file = analysis_dir / f"video_{video_id}_analysis.json"

            if output_file.exists():
                logger.info(f"Analysis exists for video {video_id}, skipping")
                successful_analyses += 1
                continue

            try:
                result = analyze_tiktok_video(video_url)

                # Validate analysis result
                is_valid, errors = validator.validate_gemini_analysis(result)
                if not is_valid:
                    logger.warning(
                        f"❌ Analysis validation failed for video {video_id}: {', '.join(errors)}")
                    tracker.log_error(
                        account, "analysis", f"Validation failed for video {video_id}: {', '.join(errors)}")
                    continue

                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                successful_analyses += 1
                time.sleep(2)  # Rate limiting
            except Exception as e:
                error_msg = f"Analysis failed for video {video_id}: {str(e)}"
                logger.error(error_msg)
                tracker.log_error(account, "analysis", error_msg)
                # Continue with next video instead of failing completely

        if successful_analyses == 0:
            raise Exception(
                f"No videos were successfully analyzed for {account}")

        logger.info(
            f"✅ Completed Gemini analysis for {account}: {successful_analyses}/{len(videos)} videos")

    except Exception as e:
        error_msg = f"Gemini analysis failed: {str(e)}"
        logger.error(error_msg)
        tracker.log_error(account, "analysis", error_msg)
        raise


def run_feature_extraction_phase(
    raw_data_path: Path,
    analysis_dir: Path,
    output_dir: Path,
    account: str,
    tracker: BatchTracker
):
    """Run feature extraction phase for a batch."""
    logger = logging.getLogger(__name__)
    logger.info(f"📊 Starting feature extraction for {account}")

    try:
        processor = DataProcessor()
        features_df, metadata = processor.process_dataset(
            raw_data_path=raw_data_path,
            gemini_analysis_dir=analysis_dir,
            output_dir=output_dir
        )

        # Log summary
        valid_count = sum(1 for m in metadata if m["is_valid"])
        logger.info(f"✅ Feature extraction completed for {account}:")
        logger.info(f"   • Processed {len(features_df)} videos")
        logger.info(f"   • Valid entries: {valid_count}/{len(metadata)}")

        return features_df, metadata

    except Exception as e:
        error_msg = f"Feature extraction failed: {str(e)}"
        logger.error(error_msg)
        tracker.log_error(account, "features", error_msg)
        raise


def process_batch(
    accounts: List[str],
    args: argparse.Namespace,
    tracker: BatchTracker
) -> bool:
    """Process a batch of accounts through all pipeline phases."""
    logger = logging.getLogger(__name__)
    logger.info(f"\n🚀 Processing batch of {len(accounts)} accounts...")

    try:
        # 1. Scraping Phase
        results = run_scraping_phase(
            accounts, args.videos_per_account, tracker)
        if not results:
            logger.error("❌ Scraping phase failed completely")
            return False

        # Save consolidated results
        raw_dir = Path("data") / "raw" / f"dataset_{args.dataset}"
        raw_dir.mkdir(parents=True, exist_ok=True)

        consolidated_data = {
            "dataset": args.dataset,
            "batch_timestamp": datetime.now().isoformat(),
            "accounts": accounts,
            "videos": []
        }

        for result in results:
            consolidated_data["videos"].extend(result.get("videos", []))

        consolidated_path = raw_dir / \
            f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(consolidated_path, 'w') as f:
            json.dump(consolidated_data, f, indent=2)

        # 2. Gemini Analysis Phase
        analysis_success = True
        for account in accounts:
            account_videos = [v for v in consolidated_data["videos"]
                              if v.get("authorMeta", {}).get("name") == account]
            if account_videos:
                try:
                    run_gemini_phase(account_videos, account, tracker)
                except Exception as e:
                    logger.error(
                        f"❌ Gemini analysis failed for {account}: {str(e)}")
                    analysis_success = False
                    # Mark account as failed to prevent infinite loop
                    tracker.mark_account_failed(
                        account, "analysis", f"Analysis failed: {str(e)}")
                    continue

        # 3. Feature Extraction Phase
        features_dir = Path("data") / "features" / f"dataset_{args.dataset}"
        features_dir.mkdir(parents=True, exist_ok=True)

        for account in accounts:
            try:
                features_df, _ = run_feature_extraction_phase(
                    raw_data_path=consolidated_path,
                    analysis_dir=Path("data/gemini_analysis") / account,
                    output_dir=features_dir,
                    account=account,
                    tracker=tracker
                )

                # Mark account as processed only if all phases succeeded
                tracker.mark_account_processed(account)
                logger.info(
                    f"✅ Successfully completed all phases for {account}")

            except Exception as e:
                logger.error(
                    f"❌ Feature extraction failed for {account}: {str(e)}")
                # Mark account as failed to prevent infinite loop
                tracker.mark_account_failed(
                    account, "features", f"Feature extraction failed: {str(e)}")
                continue

        return True

    except Exception as e:
        logger.error(f"❌ Batch processing failed: {str(e)}")
        return False


def main():
    """Run the complete pipeline with batch processing."""
    # Parse arguments
    args = parse_args()

    # Setup logging
    logger = setup_logging(args.dataset)
    logger.info(
        f"\n{'='*80}\n🚀 Starting TikTok Analysis Pipeline - Dataset: {args.dataset}\n{'='*80}")

    try:
        # Initialize batch tracker
        tracker = BatchTracker(args.dataset)

        if args.retry_failed:
            # Process failed accounts
            failed_accounts = tracker.get_failed_accounts(args.retry_phase)
            if not failed_accounts:
                logger.info("No failed accounts to retry")
                return

            logger.info(f"Retrying {len(failed_accounts)} failed accounts")
            accounts_to_process = failed_accounts
        else:
            # Get accounts from settings
            accounts_to_process = TIKTOK_ACCOUNTS

        # Process in batches
        total_processed = 0
        max_attempts = 3  # Prevent infinite loops
        attempt_count = 0

        while total_processed < len(accounts_to_process) and attempt_count < max_attempts:
            batch = tracker.get_next_batch(
                accounts_to_process[total_processed:],
                args.batch_size
            )

            if not batch:
                logger.info("No more accounts to process")
                break

            logger.info(f"Processing batch {attempt_count + 1}: {batch}")

            if process_batch(batch, args, tracker):
                total_processed += len(batch)
                attempt_count = 0  # Reset attempt count on success
            else:
                attempt_count += 1
                logger.warning(
                    f"Batch failed, attempt {attempt_count}/{max_attempts}")

            # Check if we've hit the video limit
            if total_processed * args.videos_per_account >= args.max_total_videos:
                logger.info(
                    f"Reached maximum video limit ({args.max_total_videos})")
                break

        # Log final summary
        summary = tracker.summarize_progress()
        logger.info("\n📊 Pipeline Summary:")
        logger.info(f"Total accounts processed: {summary['total_processed']}")
        logger.info(
            f"Accounts with errors: {len(summary['accounts_with_errors'])}")
        logger.info("Error counts by phase:")
        for phase, count in summary['error_phases'].items():
            logger.info(f"  • {phase}: {count}")

        if attempt_count >= max_attempts:
            logger.warning(
                f"⚠️  Stopped after {max_attempts} failed attempts to prevent infinite loop")

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
