"""Command-line script to run the feature extraction pipeline."""
import argparse
import logging
from pathlib import Path

from features.data_processor import DataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract features from TikTok videos and Gemini analysis."
    )

    parser.add_argument(
        "--raw-data",
        type=str,
        required=True,
        help="Path to raw TikTok data JSON file"
    )

    parser.add_argument(
        "--gemini-analysis",
        type=str,
        required=True,
        help="Path to directory containing Gemini analysis files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save processed features"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )

    return parser.parse_args()


def main():
    """Run the feature extraction pipeline."""
    # Parse arguments
    args = parse_args()

    # Set log level
    logging.getLogger().setLevel(args.log_level)

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        logger.info("Starting feature extraction pipeline...")

        # Initialize data processor
        processor = DataProcessor()

        # Process dataset
        features_df, metadata_list = processor.process_dataset(
            raw_data_path=args.raw_data,
            gemini_analysis_dir=args.gemini_analysis,
            output_dir=args.output_dir
        )

        # Log summary statistics
        logger.info(f"Processed {len(features_df)} videos")
        logger.info(f"Features extracted: {features_df.columns.tolist()}")

        # Log validation results
        valid_count = sum(1 for m in metadata_list if m["is_valid"])
        logger.info(f"Valid entries: {valid_count}/{len(metadata_list)}")

        # Log any processing warnings
        for metadata in metadata_list:
            if metadata.get("warnings"):
                logger.warning(
                    f"Warnings for video {metadata['video_id']}: "
                    f"{metadata['warnings']}"
                )

        logger.info("Feature extraction completed successfully!")

    except Exception as e:
        logger.error(
            f"Error during feature extraction: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
