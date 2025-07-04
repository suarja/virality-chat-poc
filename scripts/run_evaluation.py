#!/usr/bin/env python3
"""
Script for automated evaluation runs.
Starts with raw data evaluation, will expand to feature and model evaluation
as the pipeline develops.
"""
from config.evaluation_config import get_config
from src.features.evaluation import evaluate_raw_data
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Run evaluation pipeline."""
    try:
        # Get configuration
        config = get_config()

        # Phase 1: Evaluate raw data
        logger.info("Starting raw data evaluation...")

        # Find latest raw data file
        raw_data_dir = Path("data/raw")
        raw_data_files = list(raw_data_dir.glob("tiktok_consolidated_*.json"))

        if not raw_data_files:
            logger.error("No raw data files found in data/raw/")
            return 1

        latest_data = max(raw_data_files, key=lambda p: p.stat().st_mtime)
        logger.info(f"Evaluating raw data file: {latest_data}")

        # Run evaluation
        metrics = evaluate_raw_data(latest_data)

        # Print results
        print("\n📊 Raw Data Evaluation Results:")
        print("=" * 50)
        print(f"Total Videos: {metrics.total_videos}")
        print(f"Total Accounts: {metrics.total_accounts}")
        print(
            f"Average Videos per Account: {sum(metrics.videos_per_account.values()) / len(metrics.videos_per_account):.1f}")

        print("\nField Completeness:")
        for field, completeness in metrics.field_completeness.items():
            print(f"- {field}: {completeness:.1%}")

        print("\nMissing Fields:")
        for field, count in metrics.missing_fields.items():
            print(f"- {field}: {count} videos")

        # Check quality thresholds
        has_warnings = False
        if metrics.total_videos < 10:
            print("\n⚠️ WARNING: Very few videos collected")
            has_warnings = True

        for field, completeness in metrics.field_completeness.items():
            if completeness < 0.9:
                print(
                    f"\n⚠️ WARNING: Low completeness for {field}: {completeness:.1%}")
                has_warnings = True

        if has_warnings:
            print("\n⚠️ Some quality checks failed. Please review the warnings above.")
            return 1

        print("\n✅ All quality checks passed!")
        return 0

    except Exception as e:
        logger.error(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
