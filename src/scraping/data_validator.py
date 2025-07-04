"""
Data validation utilities for scraped TikTok data
"""
import logging
from typing import Dict, List, Optional, Any
import pandas as pd

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates and cleans scraped TikTok data
    """

    REQUIRED_FIELDS = [
        'id', 'text', 'createTime', 'stats'
    ]

    STATS_FIELDS = [
        'playCount', 'likeCount', 'commentCount', 'shareCount'
    ]

    def __init__(self, min_views: int = 1000):
        """
        Initialize data validator

        Args:
            min_views: Minimum view count to consider valid
        """
        self.min_views = min_views

    def validate_video(self, video: Dict) -> bool:
        """
        Validate a single video record

        Args:
            video: Video data dictionary

        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in video:
                logger.warning(f"Missing required field: {field}")
                return False

        # Check stats fields
        stats = video.get('stats', {})
        for field in self.STATS_FIELDS:
            if field not in stats:
                logger.warning(f"Missing stats field: {field}")
                return False

        # Check minimum views
        play_count = stats.get('playCount', 0)
        if play_count < self.min_views:
            logger.debug(f"Video below minimum views: {play_count}")
            return False

        return True

    def clean_video_data(self, video: Dict) -> Optional[Dict]:
        """
        Clean and normalize video data

        Args:
            video: Raw video data

        Returns:
            Cleaned video data or None if invalid
        """
        if not self.validate_video(video):
            return None

        stats = video.get('stats', {})

        cleaned = {
            'video_id': video.get('id'),
            'text': video.get('text', ''),
            'create_time': video.get('createTime'),
            'views': stats.get('playCount', 0),
            'likes': stats.get('likeCount', 0),
            'comments': stats.get('commentCount', 0),
            'shares': stats.get('shareCount', 0),
            'duration': video.get('duration', 0),
            'hashtags': self._extract_hashtags(video.get('text', '')),
            'author': video.get('author', {}).get('uniqueId', ''),
            'music': video.get('music', {}).get('title', ''),
            'raw_data': video  # Keep original for reference
        }

        # Calculate engagement metrics
        cleaned['engagement_rate'] = self._calculate_engagement_rate(cleaned)
        cleaned['virality_score'] = self._calculate_virality_score(cleaned)

        return cleaned

    def clean_dataset(self, videos: List[Dict]) -> pd.DataFrame:
        """
        Clean entire dataset of videos

        Args:
            videos: List of raw video data

        Returns:
            Cleaned DataFrame
        """
        cleaned_videos = []

        for video in videos:
            cleaned = self.clean_video_data(video)
            if cleaned:
                cleaned_videos.append(cleaned)

        logger.info(
            f"Cleaned {len(cleaned_videos)} videos from {len(videos)} raw videos")

        return pd.DataFrame(cleaned_videos)

    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from video text"""
        import re
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]

    def _calculate_engagement_rate(self, video: Dict) -> float:
        """Calculate engagement rate"""
        views = video.get('views', 0)
        if views == 0:
            return 0.0

        engagement = video.get('likes', 0) + \
            video.get('comments', 0) + video.get('shares', 0)
        return engagement / views

    def _calculate_virality_score(self, video: Dict) -> float:
        """Calculate basic virality score"""
        views = video.get('views', 0)
        engagement_rate = video.get('engagement_rate', 0)

        # Simple scoring formula (can be refined)
        return (views / 1000) * (1 + engagement_rate * 10)
