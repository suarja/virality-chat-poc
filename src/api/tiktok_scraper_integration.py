"""
🔗 Module d'intégration du scraper TikTok pour l'API

🎯 DDD Phase 4: Intégration du vrai scraper Apify
📊 Utilise l'actor clockworks/tiktok-scraper pour récupérer les vraies données TikTok
"""
import logging
import re
import os
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

# Import Apify client
try:
    from apify_client import ApifyClient
    APIFY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Apify client non disponible: {e}")
    APIFY_AVAILABLE = False

logger = logging.getLogger(__name__)


class TikTokScraperIntegration:
    """Intégration du scraper TikTok pour l'API"""

    def __init__(self):
        self.client = None
        self.available = APIFY_AVAILABLE

        if self.available:
            try:
                api_token = os.getenv("APIFY_API_TOKEN")
                if not api_token:
                    logger.warning("⚠️ APIFY_API_TOKEN non défini")
                    self.available = False
                else:
                    self.client = ApifyClient(api_token)
                    logger.info("✅ Client Apify initialisé")
            except Exception as e:
                logger.error(f"❌ Erreur initialisation Apify: {e}")
                self.available = False

    def extract_username_from_url(self, url: str) -> Optional[str]:
        """Extrait le nom d'utilisateur depuis une URL TikTok"""
        # Patterns pour extraire le username
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
        """Extrait l'ID de la vidéo depuis une URL TikTok"""
        # Patterns pour extraire l'ID vidéo
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
        """Valide si l'URL est une URL TikTok valide"""
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

    async def get_video_data_from_url(self, url: str) -> Dict[str, Any]:
        """Récupère les données d'une vidéo TikTok via son URL"""
        if not self.available or not self.client:
            raise ValueError("Client Apify non disponible")

        if not self.validate_tiktok_url(url):
            raise ValueError("URL TikTok invalide")

        try:
            # Configuration pour scraping vidéo direct
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
                raise ValueError(f"Aucune vidéo trouvée pour l'URL: {url}")

            # Retourner la première (et seule) vidéo formatée
            return self._format_video_data(items[0])

        except Exception as e:
            logger.error(f"❌ Erreur scraping vidéo: {e}")
            raise

    async def get_profile_data(self, username: str, max_videos: int = 50) -> Dict[str, Any]:
        """Récupère les données d'un profil TikTok"""
        if not self.available or not self.client:
            raise ValueError("Client Apify non disponible")

        try:
            # Nettoyer le username
            username = username.lstrip('@')

            # Configuration pour scraping profil
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
                    f"Aucune vidéo trouvée pour le profil: {username}")

            # Formater les données du profil
            return self._format_profile_data(items, username)

        except Exception as e:
            logger.error(f"❌ Erreur scraping profil: {e}")
            raise

    def _format_video_data(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """Formate les données d'une vidéo pour l'API"""
        # Extraire les métadonnées de base
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

        # Construire l'URL complète
        username = video.get('authorMeta', {}).get('name', '')
        if username and video_data['id']:
            video_data['url'] = f"https://www.tiktok.com/@{username}/video/{video_data['id']}"

        return video_data

    def _format_profile_data(self, videos: List[Dict[str, Any]], username: str) -> Dict[str, Any]:
        """Formate les données d'un profil pour l'API"""
        formatted_videos = [self._format_video_data(video) for video in videos]

        return {
            "username": username,
            "scraped_at": "2025-01-06T00:00:00Z",  # Timestamp de scraping
            "videos_count": len(formatted_videos),
            "videos": formatted_videos
        }

    def is_available(self) -> bool:
        """Vérifie si le scraper est disponible"""
        return self.available and self.client is not None


# Instance globale
tiktok_scraper_integration = TikTokScraperIntegration()
