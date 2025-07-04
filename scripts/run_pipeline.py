#!/usr/bin/env python3
"""
Complete pipeline script for TikTok virality analysis:
1. Scrape TikTok videos
2. Run Gemini analysis
3. Extract and process features
"""
from src.features.data_processor import DataProcessor
from src.scraping.tiktok_scraper import TikTokScraper
import argparse
import json
import logging
import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run complete TikTok virality analysis pipeline"
    )

    parser.add_argument(
        "--accounts",
        type=str,
        nargs="+",
        help="TikTok accounts to analyze (e.g. @username1 @username2)"
    )

    parser.add_argument(
        "--max-videos",
        type=int,
        default=50,
        help="Maximum number of videos per account"
    )

    parser.add_argument(
        "--skip-scraping",
        action="store_true",
        help="Skip TikTok scraping phase"
    )

    parser.add_argument(
        "--skip-gemini",
        action="store_true",
        help="Skip Gemini analysis phase"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/processed",
        help="Directory to save processed features"
    )

    return parser.parse_args()


def run_scraping_phase(accounts: list, max_videos: int) -> list:
    """Run TikTok scraping phase."""
    logger.info("🔍 Starting TikTok scraping phase...")

    try:
        scraper = TikTokScraper()
        results = scraper.scrape_multiple_profiles(accounts, max_videos)

        logger.info(f"✅ Scraping completed: {len(results)} accounts processed")
        return results

    except Exception as e:
        logger.error(f"❌ Scraping failed: {str(e)}")
        raise


def run_gemini_phase(video_urls: list):
    """Run Gemini analysis phase."""
    logger.info("🧠 Starting Gemini analysis phase...")

    try:
        from scripts.test_gemini import analyze_tiktok_video

        analysis_dir = Path("docs/gemini_analysis")
        analysis_dir.mkdir(parents=True, exist_ok=True)

        for i, url in enumerate(video_urls, 1):
            logger.info(f"Analyzing video {i}/{len(video_urls)}: {url}")

            result = analyze_tiktok_video(url)

            # Save analysis
            output_file = analysis_dir / \
                f"video_{i}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)

            # Rate limiting
            if i < len(video_urls):
                time.sleep(2)

        logger.info(
            f"✅ Gemini analysis completed: {len(video_urls)} videos analyzed")

    except Exception as e:
        logger.error(f"❌ Gemini analysis failed: {str(e)}")
        raise


def run_feature_extraction_phase(raw_data_path: Path, gemini_dir: Path, output_dir: Path):
    """Run feature extraction and processing phase."""
    logger.info("📊 Starting feature extraction phase...")

    try:
        processor = DataProcessor()
        features_df, metadata_list = processor.process_dataset(
            raw_data_path=raw_data_path,
            gemini_analysis_dir=gemini_dir,
            output_dir=output_dir
        )

        # Log summary
        valid_count = sum(1 for m in metadata_list if m["is_valid"])
        logger.info(f"✅ Feature extraction completed:")
        logger.info(f"   • Processed {len(features_df)} videos")
        logger.info(f"   • Valid entries: {valid_count}/{len(metadata_list)}")
        logger.info(f"   • Features extracted: {features_df.columns.tolist()}")

        return features_df, metadata_list

    except Exception as e:
        logger.error(f"❌ Feature extraction failed: {str(e)}")
        raise


def main():
    """Run the complete pipeline."""
    # Parse arguments
    args = parse_args()

    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Initialize video_urls and raw_data_path
        video_urls = []
        raw_data_path = None

        # 1. Scraping Phase
        if not args.skip_scraping:
            results = run_scraping_phase(args.accounts, args.max_videos)

            # Extract video URLs for Gemini analysis
            for result in results:
                for video in result.get("videos", []):
                    if video.get("note") == "Profile has no videos":
                        logger.error(
                            f"Account {result.get('username', 'Unknown')} has no videos")
                        sys.exit(1)
                    if video.get("webVideoUrl"):  # Use webVideoUrl instead of url
                        video_urls.append(video.get("webVideoUrl"))

            # Use the newly scraped data
            raw_data_path = next(Path("data/raw").glob("tiktok_*.json"))
        else:
            # If skipping scraping, find the latest data file for the specified account
            raw_data_dir = Path("data/raw")
            if args.accounts:
                account = args.accounts[0].replace("@", "")
                data_files = list(raw_data_dir.glob(f"tiktok_{account}*.json"))
                if not data_files:
                    logger.error(
                        f"No data files found for account {args.accounts[0]}")
                    sys.exit(1)

                # Use the most recent file
                raw_data_path = max(
                    data_files, key=lambda p: p.stat().st_mtime)

                # Load video URLs from the file
                with open(raw_data_path) as f:
                    data = json.load(f)
                    for video in data.get("videos", []):
                        if video.get("note") == "Profile has no videos":
                            logger.error(
                                f"Account {data.get('username', 'Unknown')} has no videos")
                            sys.exit(1)
                        if video.get("webVideoUrl"):  # Use webVideoUrl instead of url
                            video_urls.append(video.get("webVideoUrl"))

                if not video_urls:
                    logger.error(
                        f"No valid video URLs found in {raw_data_path}")
                    sys.exit(1)

                logger.info(
                    f"Loaded {len(video_urls)} valid video URLs from {raw_data_path}")
            else:
                logger.error("No account specified with --accounts")
                sys.exit(1)

        if raw_data_path is None:
            logger.error("No data file found to process")
            sys.exit(1)

        # 2. Gemini Analysis Phase
        if not args.skip_gemini and video_urls:
            run_gemini_phase(video_urls)
        elif not video_urls:
            logger.error("No videos to analyze")
            sys.exit(1)

        # 3. Feature Extraction Phase
        gemini_dir = Path("docs/gemini_analysis")

        features_df, metadata_list = run_feature_extraction_phase(
            raw_data_path=raw_data_path,
            gemini_dir=gemini_dir,
            output_dir=output_dir
        )

        logger.info("\n🎉 Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"\n❌ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
