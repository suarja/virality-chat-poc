"""
🔗 Module d'intégration du scraper TikTok pour l'API

🎯 DDD Phase 4: Intégration du vrai scraper Apify
📊 Utilise le scraper existant pour récupérer les vraies données TikTok
"""
import logging
import re
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

# Import du scraper existant
try:
    from src.scraping.tiktok_scraper import TikTokScraper
    SCRAPER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Scraper TikTok non disponible: {e}")
    SCRAPER_AVAILABLE = False

logger = logging.getLogger(__name__)


class TikTokScraperIntegration:
    """Intégration du scraper TikTok pour l'API"""

    def __init__(self):
        self.scraper = None
        self.available = SCRAPER_AVAILABLE

        if self.available:
            try:
                self.scraper = TikTokScraper()
                logger.info("✅ Scraper TikTok initialisé")
            except Exception as e:
                logger.error(f"❌ Erreur initialisation scraper: {e}")
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

    def get_video_data_from_url(self, url: str) -> Dict[str, Any]:
        """Récupère les données d'une vidéo TikTok via URL"""
        if not self.available or not self.scraper:
            raise ValueError("Scraper TikTok non disponible")

        if not self.validate_tiktok_url(url):
            raise ValueError("URL TikTok invalide")

        # Extraire le username et l'ID vidéo
        username = self.extract_username_from_url(url)
        video_id = self.extract_video_id_from_url(url)

        if not username:
            raise ValueError("Impossible d'extraire le nom d'utilisateur")

        if not video_id:
            raise ValueError("Impossible d'extraire l'ID de la vidéo")

        try:
            # Scraper le profil pour obtenir toutes les vidéos
            profile_data = self.scraper.scrape_profile(
                username, max_videos=100)

            # Chercher la vidéo spécifique
            target_video = None
            for video in profile_data.get('videos', []):
                if str(video.get('id')) == video_id:
                    target_video = video
                    break

            if not target_video:
                raise ValueError(
                    f"Vidéo {video_id} non trouvée dans le profil {username}")

            # Retourner les données formatées
            return self._format_video_data(target_video, username)

        except Exception as e:
            logger.error(f"❌ Erreur scraping vidéo: {e}")
            raise

    def get_profile_data(self, username: str, max_videos: int = 50) -> Dict[str, Any]:
        """Récupère les données d'un profil TikTok"""
        if not self.available or not self.scraper:
            raise ValueError("Scraper TikTok non disponible")

        try:
            # Nettoyer le username
            username = username.lstrip('@')

            # Scraper le profil
            profile_data = self.scraper.scrape_profile(username, max_videos)

            # Formater les données
            return self._format_profile_data(profile_data)

        except Exception as e:
            logger.error(f"❌ Erreur scraping profil: {e}")
            raise

    def _format_video_data(self, video: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Formate les données d'une vidéo pour l'API"""
        return {
            "id": str(video.get('id', '')),
            "url": f"https://www.tiktok.com/@{username}/video/{video.get('id', '')}",
            "text": video.get('text', ''),
            "duration": video.get('videoMeta', {}).get('duration', 0),
            "playCount": video.get('playCount', 0),
            "diggCount": video.get('diggCount', 0),
            "commentCount": video.get('commentCount', 0),
            "shareCount": video.get('shareCount', 0),
            "hashtags": video.get('hashtags', []),
            "musicMeta": video.get('musicMeta', {}),
            "createTimeISO": video.get('createTimeISO', ''),
            "videoMeta": video.get('videoMeta', {}),
            "authorMeta": video.get('authorMeta', {}),
            "stats": video.get('stats', {}),
            "duetInfo": video.get('duetInfo', {}),
            "challengeInfo": video.get('challengeInfo', {}),
            "textExtra": video.get('textExtra', [])
        }

    def _format_profile_data(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formate les données d'un profil pour l'API"""
        return {
            "username": profile_data.get('username', ''),
            "scraped_at": profile_data.get('scraped_at', ''),
            "videos_count": len(profile_data.get('videos', [])),
            "videos": [self._format_video_data(video, profile_data.get('username', ''))
                       for video in profile_data.get('videos', [])]
        }

    def is_available(self) -> bool:
        """Vérifie si le scraper est disponible"""
        return self.available and self.scraper is not None


# Instance globale
tiktok_scraper_integration = TikTokScraperIntegration()
