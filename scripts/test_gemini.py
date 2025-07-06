from pathlib import Path
import json
import logging
from datetime import datetime

# Import the new Gemini service
try:
    from src.services.gemini_service import analyze_tiktok_video
    GEMINI_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Gemini service not available: {e}")
    GEMINI_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gemini_analysis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    if not GEMINI_AVAILABLE:
        logger.error(
            "❌ Gemini service not available. Please check your setup.")
        return

    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    output_dir = Path("docs/gemini_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test videos
    test_videos = [
        "https://www.tiktok.com/@leaelui/video/7522161584643263766",
        "https://www.tiktok.com/@leaelui/video/7521405759767219478"
    ]

    logger.info("🎥 Starting Gemini Video Analysis Test\n")

    for i, video_url in enumerate(test_videos, 1):
        logger.info(f"\n📊 Analyzing Video {i}: {video_url}")
        result = analyze_tiktok_video(video_url)

        # Save complete result including raw response
        output_file = output_dir / \
            f"video_{i}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"\n💾 Results saved to {output_file}")

        if result['success']:
            logger.info("\n✅ Analysis Complete!")
        else:
            logger.error(
                f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
