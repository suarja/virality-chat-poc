#!/usr/bin/env python3
"""
Complete pipeline script for TikTok virality analysis with batch processing:
1. Scrape TikTok videos in batches
2. Run Gemini analysis
3. Extract and process features

🎯 ITER_004 Improvements:
- Randomized account selection for better diversity
- Improved batch processing with account rotation
- Better error handling and retry logic
"""
from src.scraping.tiktok_scraper import TikTokScraper
from src.utils.batch_tracker import BatchTracker
from src.utils.data_validator import DataValidator
from config.settings import TIKTOK_ACCOUNTS
import argparse
import json
import logging
import sys
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def get_randomized_accounts(accounts: List[str], max_accounts: Optional[int] = None, seed: Optional[int] = None) -> List[str]:
    """
    Get a randomized list of accounts for better diversity.

    Args:
        accounts: List of all available accounts
        max_accounts: Maximum number of accounts to return (None for all)
        seed: Random seed for reproducibility

    Returns:
        Randomized list of accounts
    """
    if seed is not None:
        random.seed(seed)

    # Create a copy to avoid modifying the original list
    randomized_accounts = accounts.copy()
    random.shuffle(randomized_accounts)

    if max_accounts is not None:
        randomized_accounts = randomized_accounts[:max_accounts]

    return randomized_accounts


def get_diverse_account_batch(accounts: List[str], batch_size: int, processed_accounts: set,
                              account_categories: Optional[Dict[str, List[str]]] = None) -> List[str]:
    """
    Get a diverse batch of accounts ensuring different categories are represented.

    Args:
        accounts: List of all available accounts
        batch_size: Size of the batch to return
        processed_accounts: Set of already processed accounts
        account_categories: Dictionary mapping categories to account lists

    Returns:
        Diverse batch of accounts
    """
    # Remove already processed accounts
    available_accounts = [
        acc for acc in accounts if acc not in processed_accounts]

    if len(available_accounts) <= batch_size:
        return available_accounts

    # If we have category information, try to diversify
    if account_categories is not None:
        batch = []
        categories_used = set()

        # First, try to get one account from each category
        for category, category_accounts in account_categories.items():
            if len(batch) >= batch_size:
                break

            # Find accounts in this category that are available
            category_available = [
                acc for acc in category_accounts if acc in available_accounts]
            if category_available and category not in categories_used:
                selected = random.choice(category_available)
                batch.append(selected)
                categories_used.add(category)
                available_accounts.remove(selected)

        # Fill remaining slots randomly
        remaining_slots = batch_size - len(batch)
        if remaining_slots > 0 and available_accounts:
            additional = random.sample(available_accounts, min(
                remaining_slots, len(available_accounts)))
            batch.extend(additional)

        return batch

    # Fallback to simple random selection
    return random.sample(available_accounts, batch_size)


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

    # New feature system parameters
    parser.add_argument(
        "--feature-system",
        choices=['legacy', 'modular'],
        default='modular',
        help="Feature extraction system to use (default: modular)"
    )

    parser.add_argument(
        "--feature-set",
        choices=['metadata', 'gemini_basic',
                 'visual_granular', 'comprehensive'],
        default='metadata',
        help="Feature set to use with modular system (default: metadata)"
    )

    # ITER_004: Randomization and diversity arguments
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed for reproducible account selection (default: 42)"
    )

    parser.add_argument(
        "--enable-diversity",
        action="store_true",
        help="Enable diverse batch selection by account categories"
    )

    parser.add_argument(
        "--max-accounts",
        type=int,
        help="Maximum number of accounts to process (default: all available)"
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
                    # Check if there are critical errors
                    if validator.has_critical_errors(errors):
                        error_summary = validator.get_error_summary(errors)
                        critical_errors = ', '.join(error_summary["critical"])
                        logger.error(
                            f"❌ Account {account} has critical errors: {critical_errors}")
                        tracker.mark_account_failed(
                            account, "scraping", f"Critical errors: {critical_errors}")
                        continue

                    # For validation errors, log as warning and continue
                    error_summary = validator.get_error_summary(errors)
                    validation_errors = ', '.join(error_summary["validation"])
                    logger.warning(
                        f"⚠️ Account {account} failed validation: {validation_errors}")
                    tracker.mark_account_failed(
                        account, "scraping", f"Validation failed: {validation_errors}")
                    continue

                # Filter valid videos
                valid_videos = validator.filter_valid_videos(
                    result.get('videos', []))
                if len(valid_videos) == 0:
                    logger.warning(
                        f"⚠️ Account {account} has no valid videos after filtering")
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
            logger.error(f"❌ {error_msg}")
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
        from src.services.gemini_service import analyze_tiktok_video

        date_str = datetime.now().strftime("%Y%m%d")
        # Unified structure: data/dataset_name/gemini_analysis/account/date
        analysis_dir = Path(
            "data") / f"dataset_{tracker.dataset_name}" / "gemini_analysis" / account / date_str
        analysis_dir.mkdir(parents=True, exist_ok=True)

        successful_analyses = 0
        for video in videos:
            video_url = video.get("webVideoUrl")
            if not video_url:
                logger.warning(f"⚠️ Skipping video without URL from {account}")
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
                    if validator.has_critical_errors(errors):
                        error_summary = validator.get_error_summary(errors)
                        critical_errors = ', '.join(error_summary["critical"])
                        logger.error(
                            f"❌ Critical analysis errors for video {video_id}: {critical_errors}")
                        tracker.log_error(
                            account, "analysis", f"Critical errors for video {video_id}: {critical_errors}")
                    else:
                        error_summary = validator.get_error_summary(errors)
                        validation_errors = ', '.join(
                            error_summary["validation"])
                        logger.warning(
                            f"⚠️ Analysis validation failed for video {video_id}: {validation_errors}")
                        tracker.log_error(
                            account, "analysis", f"Validation failed for video {video_id}: {validation_errors}")
                    continue

                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                successful_analyses += 1
                time.sleep(2)  # Rate limiting
            except Exception as e:
                error_msg = f"Analysis failed for video {video_id}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                tracker.log_error(account, "analysis", error_msg)
                # Continue with next video instead of failing completely

        if successful_analyses == 0:
            raise Exception(
                f"No videos were successfully analyzed for {account}")

        logger.info(
            f"✅ Completed Gemini analysis for {account}: {successful_analyses}/{len(videos)} videos")

    except Exception as e:
        error_msg = f"Gemini analysis failed: {str(e)}"
        logger.error(f"❌ {error_msg}")
        tracker.log_error(account, "analysis", error_msg)
        raise


def run_feature_extraction_phase(
    raw_data_path: Path,
    analysis_dir: Path,
    output_dir: Path,
    account: str,
    tracker: BatchTracker,
    feature_system: str = 'legacy',
    feature_set: str = 'metadata'
):
    """Run feature extraction phase for a batch."""
    logger = logging.getLogger(__name__)
    logger.info(
        f"📊 Starting feature extraction for {account} using {feature_system} system")

    features_df = None
    metadata = []

    try:
        if feature_system == 'modular':
            try:
                # Try modular system first
                from src.features.modular_feature_system import FeatureExtractorManager

                logger.info(
                    f"🔧 Using modular feature system with {feature_set} feature set")
                manager = FeatureExtractorManager([feature_set])

                # Load raw data and analysis data
                with open(raw_data_path, 'r') as f:
                    raw_data = json.load(f)

                # Process each video with modular system
                all_features = []
                all_metadata = []

                for video in raw_data.get('videos', []):
                    # Find corresponding analysis file (search recursively like legacy system)
                    video_id = video.get('id', '')
                    analysis_files = list(analysis_dir.rglob(
                        f'video_{video_id}_analysis.json'))

                    gemini_analysis = None
                    if analysis_files:
                        # Take the first found
                        analysis_file = analysis_files[0]
                        with open(analysis_file, 'r') as f:
                            analysis_data = json.load(f)
                            # Extract the analysis field from the response structure
                            if analysis_data.get('success') and 'analysis' in analysis_data:
                                gemini_analysis = analysis_data['analysis']
                            else:
                                gemini_analysis = analysis_data  # Fallback for old format

                    # Extract features using modular system
                    features = manager.extract_features(video, gemini_analysis)
                    all_features.append(features)

                    # Create metadata entry
                    metadata_entry = {
                        "video_id": video_id,
                        "is_valid": True,
                        "feature_count": len(features),
                        "system_used": "modular",
                        "feature_set": feature_set
                    }
                    all_metadata.append(metadata_entry)

                # Convert to DataFrame
                import pandas as pd
                features_df = pd.DataFrame(all_features)
                metadata = all_metadata

                # Save results
                output_file = output_dir / \
                    f"{account}_features_{feature_set}.csv"
                features_df.to_csv(output_file, index=False)

                logger.info(f"✅ Modular features saved to {output_file}")

            except ImportError as e:
                logger.warning(f"⚠️ Modular system not available: {e}")
                logger.info("🔄 Falling back to legacy DataProcessor")
                feature_system = 'legacy'

            except Exception as e:
                logger.error(f"❌ Modular system failed: {e}")
                logger.info("🔄 Falling back to legacy DataProcessor")
                feature_system = 'legacy'

        if feature_system == 'legacy':
            logger.error(
                "❌ Legacy DataProcessor not available - using modular system only")
            raise Exception("Legacy system not available - use modular system")

        # Log summary
        if features_df is not None and metadata:
            valid_count = sum(1 for m in metadata if m.get("is_valid", False))
            logger.info(f"✅ Feature extraction completed for {account}:")
            logger.info(f"   • System used: {feature_system}")
            if feature_system == 'modular':
                logger.info(f"   • Feature set: {feature_set}")
            logger.info(f"   • Processed {len(features_df)} videos")
            logger.info(f"   • Valid entries: {valid_count}/{len(metadata)}")
        else:
            logger.error("❌ Feature extraction failed - no data produced")
            raise Exception("No features extracted")

        return features_df, metadata

    except Exception as e:
        error_msg = f"Feature extraction failed: {str(e)}"
        logger.error(error_msg)
        tracker.log_error(account, "features", error_msg)
        raise


def aggregate_features_after_extraction(output_dir: Path, feature_set: str):
    """Aggregate features after extraction phase."""
    logger = logging.getLogger(__name__)

    try:
        # Import the aggregation function
        from scripts.aggregate_features import aggregate_features

        # Get dataset directory from output_dir
        dataset_dir = output_dir.parent

        logger.info(f"🔄 Aggregating features for {feature_set}...")

        # Aggregate features
        aggregated_df = aggregate_features(
            dataset_dir=str(dataset_dir),
            feature_set=feature_set,
            output_file=str(output_dir / f"aggregated_{feature_set}.csv"),
            add_account_column=True
        )

        logger.info(
            f"✅ Features aggregated: {len(aggregated_df)} total features")
        logger.info(
            f"   • Accounts: {aggregated_df['account_name'].nunique()}")
        logger.info(f"   • Features per account:")
        for account in aggregated_df['account_name'].unique():
            count = len(
                aggregated_df[aggregated_df['account_name'] == account])
            logger.info(f"     - {account}: {count} features")

        return aggregated_df

    except Exception as e:
        logger.warning(f"⚠️ Feature aggregation failed: {e}")
        logger.info("   Continuing without aggregation...")
        return None


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

        # If no results from scraping, log and continue (don't fail the batch)
        if not results:
            logger.warning(
                "⚠️ No valid accounts found in scraping phase, continuing with next batch")
            return True  # Don't fail the batch, just continue

        # Unified structure: data/dataset_name/
        dataset_dir = Path("data") / f"dataset_{args.dataset}"
        dataset_dir.mkdir(parents=True, exist_ok=True)

        # Save consolidated results in unified structure
        consolidated_data = {
            "dataset": args.dataset,
            "batch_timestamp": datetime.now().isoformat(),
            "accounts": accounts,
            "videos": []
        }

        for result in results:
            consolidated_data["videos"].extend(result.get("videos", []))

        consolidated_path = dataset_dir / \
            f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(consolidated_path, 'w') as f:
            json.dump(consolidated_data, f, indent=2)

            # 2. Gemini Analysis Phase - FIXED LOGIC
        for result in results:
            account = result.get('username')
            videos = result.get('videos', [])

            if account and videos:  # Only run if we have account and videos
                try:
                    run_gemini_phase(videos, account, tracker)
                except Exception as e:
                    logger.error(
                        f"❌ Gemini analysis failed for {account}: {str(e)}")
                    # Mark account as failed to prevent infinite loop
                    tracker.mark_account_failed(
                        account, "analysis", f"Analysis failed: {str(e)}")
                    continue

        # 3. Feature Extraction Phase
        features_dir = dataset_dir / "features"
        features_dir.mkdir(parents=True, exist_ok=True)

        for result in results:
            account = result.get('username')
            if not account:
                logger.warning("⚠️ Skipping result without username")
                continue

            try:
                # Unified analysis directory path
                analysis_dir = dataset_dir / "gemini_analysis" / account

                features_df, _ = run_feature_extraction_phase(
                    raw_data_path=consolidated_path,
                    analysis_dir=analysis_dir,
                    output_dir=features_dir,
                    account=account,
                    tracker=tracker,
                    feature_system=args.feature_system,
                    feature_set=args.feature_set
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

        # 4. Automatic Feature Aggregation
        if args.feature_system == 'modular':
            logger.info("🔄 Starting automatic feature aggregation...")
            aggregated_df = aggregate_features_after_extraction(
                features_dir, args.feature_set
            )
            if aggregated_df is not None:
                logger.info("✅ Feature aggregation completed successfully")
            else:
                logger.warning(
                    "⚠️ Feature aggregation failed, but pipeline continues")

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

    # Define account categories for better diversity
    account_categories = {
        "lifestyle": ["@leaelui", "@unefille.ia", "@lea_mary", "@marie29france_", "@lindalys1_"],
        "tech": ["@swarecito", "@julien.snsn", "@david_sepahan"],
        "food": ["@swiss_fit.cook", "@healthyfood_creation", "@pastelcuisine"],
        "gaming": ["@gotaga", "@domingo", "@squeezie", "@sosah1.6"],
        "humor": ["@athenasol", "@isabrunellii", "@contiped"],
        "travel": ["@loupernaut", "@astucequotidienne87"],
        "fitness": ["@oceane_dmg"]
    }

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
            # Get randomized accounts from settings
            logger.info(
                "🎲 Randomizing account selection for better diversity...")
            accounts_to_process = get_randomized_accounts(
                TIKTOK_ACCOUNTS,
                max_accounts=args.max_accounts,  # Use max_accounts argument
                seed=args.random_seed  # Use random_seed argument
            )
            logger.info(
                f"Selected {len(accounts_to_process)} accounts in randomized order")

        # Process in batches with diversity
        total_processed = 0
        batch_count = 0
        total_videos_processed = 0
        processed_accounts = set()

        while total_processed < len(accounts_to_process):
            # Get diverse batch instead of linear selection
            remaining_accounts = [
                acc for acc in accounts_to_process if acc not in processed_accounts]

            if not remaining_accounts:
                logger.info("No more accounts to process")
                break

            # Use diversity if enabled, otherwise simple random selection
            if args.enable_diversity:
                batch = get_diverse_account_batch(
                    remaining_accounts,
                    args.batch_size,
                    processed_accounts,
                    account_categories
                )
            else:
                batch = random.sample(remaining_accounts, min(
                    args.batch_size, len(remaining_accounts)))

            batch_count += 1
            logger.info(f"🎯 Processing diverse batch {batch_count}: {batch}")
            logger.info(
                f"   Categories in batch: {[cat for cat, accs in account_categories.items() if any(acc in batch for acc in accs)]}")

            # Process batch
            success = process_batch(batch, args, tracker)
            if success:
                processed_accounts.update(batch)
                total_processed += len(batch)

            # Check actual videos processed from batch results
            try:
                dataset_dir = Path("data") / f"dataset_{args.dataset}"
                batch_files = list(dataset_dir.glob("batch_*.json"))
                if batch_files:
                    latest_batch = max(
                        batch_files, key=lambda x: x.stat().st_mtime)
                    with open(latest_batch, 'r') as f:
                        batch_data = json.load(f)
                        actual_videos = len(batch_data.get('videos', []))
                        total_videos_processed += actual_videos

                        logger.info(
                            f"📊 Batch {batch_count}: {actual_videos} videos processed (Total: {total_videos_processed})")

                        if total_videos_processed >= args.max_total_videos:
                            logger.info(
                                f"🎯 Reached actual video limit ({total_videos_processed} >= {args.max_total_videos})")
                            break
            except Exception as e:
                logger.warning(f"Could not count actual videos: {e}")
                # Fallback to estimation
                estimated_videos = total_processed * args.videos_per_account
                if estimated_videos >= args.max_total_videos:
                    logger.info(
                        f"Reached estimated video limit ({estimated_videos} >= {args.max_total_videos})")
                    break

        # Log final summary
        summary = tracker.summarize_progress()
        logger.info("\n📊 Pipeline Summary:")
        logger.info(f"Total accounts attempted: {summary['total_processed']}")
        logger.info(f"✅ Successful accounts: {summary['successful_accounts']}")
        logger.info(f"❌ Failed accounts: {summary['failed_accounts']}")
        logger.info(
            f"🎲 Accounts processed with randomization: {len(processed_accounts)}")
        logger.info("Error counts by phase:")
        for phase, count in summary['error_phases'].items():
            if count > 0:
                logger.info(f"  • {phase}: {count}")

        logger.info("✅ Pipeline completed successfully")

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
