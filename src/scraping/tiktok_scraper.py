"""
TikTok Scraper using Apify API
"""
import logging
import time
import os
import sys
from typing import List, Dict, Optional
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from apify_client import ApifyClient
except ImportError:
    ApifyClient = None
    print("⚠️  apify-client not installed. Install with: pip install apify-client")

# Import settings with fallback
try:
    from config.settings import APIFY_API_TOKEN, RAW_DATA_DIR
except ImportError:
    # Fallback configuration
    from dotenv import load_dotenv
    load_dotenv()
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
    RAW_DATA_DIR = project_root / "data" / "raw"
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)


class TikTokScraper:
    """
    TikTok scraper using Apify API
    """

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize TikTok scraper

        Args:
            api_token: Apify API token
        """
        self.api_token = api_token or APIFY_API_TOKEN
        if not self.api_token:
            raise ValueError(
                "Apify API token is required. Please set APIFY_API_TOKEN in .env file")

        if ApifyClient is None:
            raise ImportError(
                "apify-client is required. Install with: pip install apify-client")

        self.client = ApifyClient(self.api_token)

    def scrape_profile(self, username: str, max_videos: int = 50) -> Dict:
        """
        Scrape TikTok profile and videos

        Args:
            username: TikTok username (with or without @)
            max_videos: Maximum number of videos to scrape

        Returns:
            Dictionary containing profile data and videos
        """
        # Remove @ if present
        username = username.lstrip('@')

        logger.info(f"Scraping TikTok profile: {username}")

        # Apify TikTok scraper actor
        actor_id = "clockworks/free-tiktok-scraper"

        run_input = {
            "profiles": [f"@{username}"],
            "resultsPerPage": max_videos,
            "shouldDownloadVideos": False,
            "shouldDownloadCovers": False,
            "shouldDownloadSlideshowImages": False
        }

        try:
            # Start the actor
            run = self.client.actor(actor_id).call(run_input=run_input)

            # Get results
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)

            logger.info(f"Scraped {len(results)} videos for {username}")
            return {
                "username": username,
                "scraped_at": time.time(),
                "videos": results
            }

        except Exception as e:
            logger.error(f"Error scraping {username}: {str(e)}")
            raise

    def scrape_multiple_profiles(self, usernames: List[str], max_videos: int = 50) -> List[Dict]:
        """
        Scrape multiple TikTok profiles

        Args:
            usernames: List of TikTok usernames
            max_videos: Maximum number of videos per profile

        Returns:
            List of profile data dictionaries
        """
        results = []

        for username in usernames:
            try:
                profile_data = self.scrape_profile(username, max_videos)
                results.append(profile_data)

                # Rate limiting
                time.sleep(2)

            except Exception as e:
                logger.error(f"Failed to scrape {username}: {str(e)}")
                continue

        return results

    def save_raw_data(self, data: Dict, filename: str) -> None:
        """
        Save raw scraped data to JSON file

        Args:
            data: Scraped data dictionary
            filename: Output filename
        """
        import json

        output_path = RAW_DATA_DIR / f"{filename}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved raw data to {output_path}")
