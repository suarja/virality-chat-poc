"""
🔗 TikTok Scraper Integration Module for API

🎯 Production-ready TikTok data scraping with caching
📊 Uses Apify's clockworks/tiktok-scraper actor for real TikTok data
"""
import logging
import re
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

# Import Apify client
try:
    from apify_client import ApifyClient
    APIFY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Apify client not available: {e}")
    APIFY_AVAILABLE = False

logger = logging.getLogger(__name__)


class TikTokScraperIntegration:
    """TikTok scraper integration for API with caching support"""

    def __init__(self):
        self.client = None
        self.available = APIFY_AVAILABLE
        self.cache_dir = Path("data/api_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        if self.available:
            try:
                api_token = os.getenv("APIFY_API_TOKEN")
                if not api_token:
                    logger.warning("⚠️ APIFY_API_TOKEN not defined")
                    self.available = False
                else:
                    self.client = ApifyClient(api_token)
                    logger.info("✅ Apify client initialized")
            except Exception as e:
                logger.error(f"❌ Apify initialization error: {e}")
                self.available = False

    def extract_username_from_url(self, url: str) -> Optional[str]:
        """Extract username from TikTok URL"""
        # Patterns to extract username
        patterns = [
            r'tiktok\.com/@([\w.-]+)',
            r'tiktok\.com/user/([\w.-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def extract_video_id_from_url(self, url: str) -> Optional[str]:
        """Extract video ID from TikTok URL"""
        # Patterns to extract video ID
        patterns = [
            r'/video/(\d+)',
            r'/v/(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def validate_tiktok_url(self, url: str) -> bool:
        """Validate if URL is a valid TikTok URL"""
        tiktok_patterns = [
            r'tiktok\.com/@[\w.-]+/video/\d+',
            r'tiktok\.com/v/\d+',
            r'vm\.tiktok\.com/[\w]+',
            r'vt\.tiktok\.com/[\w]+'
        ]

        for pattern in tiktok_patterns:
            if re.search(pattern, url):
                return True
        return False

    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL"""
        video_id = self.extract_video_id_from_url(url)
        if video_id:
            return f"video_{video_id}"
        return f"url_{hash(url)}"

    def _get_profile_cache_key(self, username: str) -> str:
        """Generate cache key for profile"""
        return f"profile_{username.lstrip('@')}"

    async def get_cached_video_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Get cached video data if available"""
        try:
            cache_key = self._get_cache_key(url)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                logger.info(f"✅ Using cached video data for {url}")
                # Return the video_data part
                return cached_data.get("video_data")
            return None
        except Exception as e:
            logger.warning(f"⚠️ Error reading cache: {e}")
            return None

    async def cache_video_data(self, url: str, video_data: Dict[str, Any]) -> None:
        """Cache video data"""
        try:
            cache_key = self._get_cache_key(url)
            cache_file = self.cache_dir / f"{cache_key}.json"

            cache_data = {
                "url": url,
                "video_data": video_data,
                "cached_at": "2025-01-06T00:00:00Z"
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Cached video data for {url}")
        except Exception as e:
            logger.warning(f"⚠️ Error caching video data: {e}")

    async def get_cached_profile_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Get cached profile data if available"""
        try:
            cache_key = self._get_profile_cache_key(username)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                logger.info(f"✅ Using cached profile data for {username}")
                return cached_data
            return None
        except Exception as e:
            logger.warning(f"⚠️ Error reading profile cache: {e}")
            return None

    async def cache_profile_data(self, username: str, profile_data: Dict[str, Any]) -> None:
        """Cache profile data"""
        try:
            cache_key = self._get_profile_cache_key(username)
            cache_file = self.cache_dir / f"{cache_key}.json"

            cache_data = {
                "username": username,
                "profile_data": profile_data,
                "cached_at": "2025-01-06T00:00:00Z"
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Cached profile data for {username}")
        except Exception as e:
            logger.warning(f"⚠️ Error caching profile data: {e}")

    async def get_video_data_from_url(self, url: str) -> Dict[str, Any]:
        """Get video data from TikTok URL"""
        if not self.available or not self.client:
            raise ValueError("Apify client not available")

        if not self.validate_tiktok_url(url):
            raise ValueError("Invalid TikTok URL")

        try:
            # Configuration for direct video scraping
            run_input = {
                "excludePinnedPosts": False,
                "postURLs": [url],
                "proxyCountryCode": "None",
                "resultsPerPage": 100,
                "scrapeRelatedVideos": False,
                "shouldDownloadAvatars": False,
                "shouldDownloadCovers": False,
                "shouldDownloadMusicCovers": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadSubtitles": False,
                "shouldDownloadVideos": False
            }

            # Run the Actor
            run = self.client.actor(
                "clockworks/tiktok-scraper").call(run_input=run_input)

            # Fetch results
            items = []
            dataset = self.client.dataset(run["defaultDatasetId"])
            if dataset:
                for item in dataset.iterate_items():
                    items.append(item)

            if not items:
                raise ValueError(f"No video found for URL: {url}")

            # Return the first (and only) formatted video
            return self._format_video_data(items[0])

        except Exception as e:
            logger.error(f"❌ Video scraping error: {e}")
            raise

    async def get_profile_data(self, username: str, max_videos: int = 50) -> Dict[str, Any]:
        """Get profile data from TikTok"""
        if not self.available or not self.client:
            raise ValueError("Apify client not available")

        try:
            # Clean username
            username = username.lstrip('@')

            # Configuration for profile scraping
            run_input = {
                "profiles": [username],
                "profileSorting": "latest",
                "excludePinnedPosts": False,
                "resultsPerPage": max_videos,
                "maxProfilesPerQuery": 1,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
                "shouldDownloadSubtitles": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadAvatars": False,
                "shouldDownloadMusicCovers": False,
                "proxyCountryCode": "None"
            }

            # Run the Actor
            run = self.client.actor(
                "clockworks/tiktok-scraper").call(run_input=run_input)

            # Fetch results
            items = []
            dataset = self.client.dataset(run["defaultDatasetId"])
            if dataset:
                for item in dataset.iterate_items():
                    items.append(item)

            if not items:
                raise ValueError(
                    f"No videos found for profile: {username}")

            # Format profile data
            return self._format_profile_data(items, username)

        except Exception as e:
            logger.error(f"❌ Profile scraping error: {e}")
            raise

    def _format_video_data(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """Format video data for API"""
        # Extract basic metadata
        video_data = {
            "id": str(video.get('id', '')),
            "text": video.get('text', ''),
            "duration": video.get('videoMeta', {}).get('duration', 0),
            "playCount": video.get('playCount', 0),
            "diggCount": video.get('diggCount', 0),
            "commentCount": video.get('commentCount', 0),
            "shareCount": video.get('shareCount', 0),
            "collectCount": video.get('collectCount', 0),
            "hashtags": [tag.get('name', '') for tag in video.get('hashtags', [])],
            "musicMeta": video.get('musicMeta', {}),
            "createTimeISO": video.get('createTimeISO', ''),
            "videoMeta": video.get('videoMeta', {}),
            "authorMeta": video.get('authorMeta', {}),
            "webVideoUrl": video.get('webVideoUrl', ''),
            "isSlideshow": video.get('isSlideshow', False),
            "isPinned": video.get('isPinned', False),
            "isSponsored": video.get('isSponsored', False)
        }

        # Build complete URL
        username = video.get('authorMeta', {}).get('name', '')
        if username and video_data['id']:
            video_data['url'] = f"https://www.tiktok.com/@{username}/video/{video_data['id']}"

        return video_data

    def _format_profile_data(self, videos: List[Dict[str, Any]], username: str) -> Dict[str, Any]:
        """Format profile data for API"""
        formatted_videos = [self._format_video_data(video) for video in videos]

        return {
            "username": username,
            "scraped_at": "2025-01-06T00:00:00Z",  # Scraping timestamp
            "videos_count": len(formatted_videos),
            "videos": formatted_videos
        }

    def is_available(self) -> bool:
        """Check if scraper is available"""
        return self.available and self.client is not None


# Global instance
tiktok_scraper_integration = TikTokScraperIntegration()
