#!/usr/bin/env python3
"""
🎥 Gestionnaire de Cache Apify - TikTok Virality Prediction
📊 Télécharge et stocke les vidéos TikTok pour éviter le re-scraping
"""

import os
import json
import shutil
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()


class ApifyCacheManager:
    """Gestionnaire de cache pour les données Apify"""

    def __init__(self, cache_dir="data/apify_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Créer les sous-dossiers
        (self.cache_dir / "videos").mkdir(exist_ok=True)
        (self.cache_dir / "profiles").mkdir(exist_ok=True)

        self.index_file = self.cache_dir / "cache_index.json"
        self.load_index()

        # Initialiser le client Apify
        api_token = os.getenv("APIFY_API_TOKEN")
        if not api_token:
            raise ValueError("APIFY_API_TOKEN non défini")
        self.client = ApifyClient(api_token)

    def load_index(self):
        """Charge l'index du cache"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                "last_updated": datetime.now().isoformat(),
                "videos": {},
                "profiles": {}
            }

    def save_index(self):
        """Sauvegarde l'index du cache"""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def extract_video_id(self, url: str) -> str:
        """Extrait l'ID vidéo depuis une URL TikTok"""
        import re
        patterns = [
            r'/video/(\d+)',
            r'/v/(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError(f"Impossible d'extraire l'ID vidéo de: {url}")

    def extract_username(self, url: str) -> str:
        """Extrait le username depuis une URL TikTok"""
        import re
        patterns = [
            r'tiktok\.com/@([\w.-]+)',
            r'tiktok\.com/user/([\w.-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError(f"Impossible d'extraire le username de: {url}")

    def download_video_with_cache(self, url: str, force_download: bool = False) -> Dict[str, Any]:
        """Télécharge une vidéo avec cache"""
        video_id = self.extract_video_id(url)
        username = self.extract_username(url)

        # Vérifier si déjà en cache
        if not force_download and video_id in self.index["videos"]:
            print(f"✅ Vidéo {video_id} déjà en cache")
            return self.index["videos"][video_id]

        # Télécharger via Apify
        print(f"📥 Téléchargement vidéo {video_id}...")

        try:
            # Configuration pour téléchargement complet
            run_input = {
                "excludePinnedPosts": False,
                "postURLs": [url],
                "resultsPerPage": 100,
                "shouldDownloadCovers": True,
                "shouldDownloadSlideshowImages": True,
                "shouldDownloadSubtitles": True,
                "shouldDownloadVideos": True,
                "videoKvStoreIdOrName": f"video-{video_id}"
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

            video_data = items[0]

            # Créer le dossier pour cette vidéo
            video_dir = self.cache_dir / "videos" / video_id
            video_dir.mkdir(parents=True, exist_ok=True)

            # Sauvegarder les métadonnées
            metadata_file = video_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(video_data, f, indent=2, default=str)

            # Télécharger les fichiers média si disponibles
            files_info = self._download_media_files(video_data, video_dir)

            # Mettre à jour l'index
            self.index["videos"][video_id] = {
                "url": url,
                "username": username,
                "scraped_at": datetime.now().isoformat(),
                "files": files_info,
                "features": self._extract_features(video_data)
            }
            self.save_index()

            print(f"✅ Vidéo {video_id} téléchargée et mise en cache")
            return self.index["videos"][video_id]

        except Exception as e:
            print(f"❌ Erreur téléchargement vidéo {video_id}: {e}")
            raise

    def _download_media_files(self, video_data: Dict[str, Any], video_dir: Path) -> Dict[str, str]:
        """Télécharge les fichiers média"""
        files_info = {
            "metadata": str(video_dir / "metadata.json")
        }

        # Télécharger la cover
        if "videoMeta" in video_data and "coverUrl" in video_data["videoMeta"]:
            cover_url = video_data["videoMeta"]["coverUrl"]
            cover_file = video_dir / "cover.jpg"
            try:
                response = requests.get(cover_url, timeout=30)
                if response.status_code == 200:
                    with open(cover_file, 'wb') as f:
                        f.write(response.content)
                    files_info["cover"] = str(cover_file)
                    print(f"✅ Cover téléchargée: {cover_file}")
            except Exception as e:
                print(f"⚠️ Erreur téléchargement cover: {e}")

        # Télécharger les sous-titres
        if "videoMeta" in video_data and "subtitleLinks" in video_data["videoMeta"]:
            subtitles_dir = video_dir / "subtitles"
            subtitles_dir.mkdir(exist_ok=True)

            subtitle_files = []
            for subtitle in video_data["videoMeta"]["subtitleLinks"]:
                language = subtitle.get("language", "unknown")
                download_link = subtitle.get("downloadLink")

                if download_link:
                    subtitle_file = subtitles_dir / f"{language}.srt"
                    try:
                        response = requests.get(download_link, timeout=30)
                        if response.status_code == 200:
                            with open(subtitle_file, 'wb') as f:
                                f.write(response.content)
                            subtitle_files.append(str(subtitle_file))
                            print(
                                f"✅ Sous-titre {language} téléchargé: {subtitle_file}")
                    except Exception as e:
                        print(
                            f"⚠️ Erreur téléchargement sous-titre {language}: {e}")

            if subtitle_files:
                files_info["subtitles"] = subtitle_files

        # Note: Les vidéos sont stockées dans le KV store d'Apify
        # Pour les récupérer, il faudrait utiliser l'API Apify
        files_info["video_kv_store"] = f"video-{video_data.get('id', 'unknown')}"

        return files_info

    def _extract_features(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les features importantes de la vidéo"""
        return {
            "duration": video_data.get("videoMeta", {}).get("duration", 0),
            "hashtags": [tag.get("name", "") for tag in video_data.get("hashtags", [])],
            "language": video_data.get("textLanguage", "unknown"),
            "engagement": {
                "playCount": video_data.get("playCount", 0),
                "diggCount": video_data.get("diggCount", 0),
                "commentCount": video_data.get("commentCount", 0),
                "shareCount": video_data.get("shareCount", 0),
                "collectCount": video_data.get("collectCount", 0)
            },
            "text": video_data.get("text", ""),
            "isOriginalAudio": video_data.get("musicMeta", {}).get("musicOriginal", False)
        }

    def get_cached_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une vidéo du cache"""
        if video_id in self.index["videos"]:
            return self.index["videos"][video_id]
        return None

    def list_cached_videos(self) -> List[Dict[str, Any]]:
        """Liste toutes les vidéos en cache"""
        return list(self.index["videos"].values())

    def cleanup_cache(self, max_age_days: int = 30):
        """Nettoie le cache des anciens fichiers"""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        removed_count = 0

        for video_id, video_data in list(self.index["videos"].items()):
            scraped_at = datetime.fromisoformat(video_data["scraped_at"])
            if scraped_at < cutoff_date:
                # Supprimer les fichiers
                video_dir = self.cache_dir / "videos" / video_id
                if video_dir.exists():
                    shutil.rmtree(video_dir)
                    print(f"🗑️ Supprimé: {video_dir}")

                # Retirer de l'index
                del self.index["videos"][video_id]
                removed_count += 1

        self.save_index()
        print(f"✅ Nettoyage terminé: {removed_count} vidéos supprimées")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        total_size = 0
        for video_dir in (self.cache_dir / "videos").iterdir():
            if video_dir.is_dir():
                for file_path in video_dir.rglob("*"):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size

        return {
            "total_videos": len(self.index["videos"]),
            "total_profiles": len(self.index["profiles"]),
            "cache_size_mb": round(total_size / (1024 * 1024), 2),
            "last_updated": self.index["last_updated"]
        }


def main():
    """Script principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Gestionnaire de cache Apify")
    parser.add_argument("--url", help="URL de la vidéo TikTok à télécharger")
    parser.add_argument("--force", action="store_true",
                        help="Forcer le re-téléchargement")
    parser.add_argument("--cleanup", type=int,
                        help="Nettoyer le cache (jours)")
    parser.add_argument("--stats", action="store_true",
                        help="Afficher les stats du cache")
    parser.add_argument("--list", action="store_true",
                        help="Lister les vidéos en cache")

    args = parser.parse_args()

    try:
        cache_manager = ApifyCacheManager()

        if args.stats:
            stats = cache_manager.get_cache_stats()
            print("📊 Statistiques du cache:")
            print(f"   - Vidéos: {stats['total_videos']}")
            print(f"   - Profils: {stats['total_profiles']}")
            print(f"   - Taille: {stats['cache_size_mb']} MB")
            print(f"   - Dernière mise à jour: {stats['last_updated']}")

        elif args.list:
            videos = cache_manager.list_cached_videos()
            print(f"📋 Vidéos en cache ({len(videos)}):")
            for video in videos:
                print(f"   - {video['username']}: {video['url']}")

        elif args.cleanup:
            cache_manager.cleanup_cache(args.cleanup)

        elif args.url:
            result = cache_manager.download_video_with_cache(
                args.url, args.force)
            print(f"✅ Vidéo téléchargée: {result['url']}")

        else:
            print("❌ Veuillez spécifier une action (--url, --stats, --list, --cleanup)")

    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    main()
