"""
Data validation utilities for TikTok pipeline
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class DataValidator:
    """Comprehensive data validation for TikTok pipeline"""

    def __init__(self):
        """Initialize validator with validation rules."""
        self.min_views = 1000
        self.max_video_age_days = 180  # 6 months
        self.min_video_duration = 1  # seconds
        self.max_video_duration = 600  # 10 minutes
        self.required_fields = ['id', 'text', 'playCount',
                                'diggCount', 'commentCount', 'shareCount']

    def validate_account(self, account_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate account data from scraping.

        Args:
            account_data: Raw account data from scraper

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        if not account_data.get('username'):
            errors.append("Missing username")

        if 'videos' not in account_data:
            errors.append("No videos field found")
            return False, errors

        videos = account_data['videos']
        if not isinstance(videos, list):
            errors.append("Videos field is not a list")
            return False, errors

        # Check if account has videos
        if len(videos) == 0:
            errors.append("Account has no videos")
            return False, errors

        # Check for minimum video count
        if len(videos) < 1:
            errors.append("Account has insufficient videos")
            return False, errors

        # Validate each video
        valid_videos = 0
        for video in videos:
            is_valid, video_errors = self.validate_video(video)
            if is_valid:
                valid_videos += 1
            else:
                errors.extend(
                    [f"Video {video.get('id', 'unknown')}: {e}" for e in video_errors])

        # Check if we have enough valid videos
        if valid_videos == 0:
            errors.append("No valid videos found in account")
            return False, errors

        logger.info(
            f"Account {account_data.get('username')}: {valid_videos}/{len(videos)} valid videos")

        return True, errors

    def validate_video(self, video_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate individual video data.

        Args:
            video_data: Raw video data from scraper

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        for field in self.required_fields:
            if field not in video_data:
                errors.append(f"Missing required field: {field}")

        # Check video ID
        video_id = video_data.get('id')
        if not video_id:
            errors.append("Missing video ID")
        elif not str(video_id).isdigit():
            errors.append("Invalid video ID format")

        # Check view count
        view_count = video_data.get('playCount', 0)
        if not isinstance(view_count, (int, float)) or view_count < 0:
            errors.append("Invalid view count")
        elif view_count < self.min_views:
            errors.append(
                f"View count too low: {view_count} < {self.min_views}")

        # Check engagement metrics
        for metric in ['diggCount', 'commentCount', 'shareCount']:
            count = video_data.get(metric, 0)
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(f"Invalid {metric}: {count}")

        # Check video duration
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if not isinstance(duration, (int, float)) or duration < 0:
            errors.append("Invalid video duration")
        elif duration < self.min_video_duration:
            errors.append(
                f"Video too short: {duration}s < {self.min_video_duration}s")
        elif duration > self.max_video_duration:
            errors.append(
                f"Video too long: {duration}s > {self.max_video_duration}s")

        # Check posting date
        create_time = video_data.get('createTimeISO')
        if create_time:
            try:
                post_date = datetime.fromisoformat(
                    create_time.replace('Z', '+00:00'))
                age_days = (datetime.now(post_date.tzinfo) - post_date).days
                if age_days > self.max_video_age_days:
                    errors.append(
                        f"Video too old: {age_days} days > {self.max_video_age_days} days")
            except Exception as e:
                errors.append(f"Invalid posting date: {e}")

        # Check for sponsored content indicators
        text = video_data.get('text', '').lower()
        sponsored_indicators = ['sponsored', 'ad',
                                'promotion', 'partnership', 'collab']
        if any(indicator in text for indicator in sponsored_indicators):
            errors.append("Detected sponsored content")

        # Check for valid video URL
        web_video_url = video_data.get('webVideoUrl')
        if not web_video_url:
            errors.append("Missing video URL")
        elif not web_video_url.startswith('https://'):
            errors.append("Invalid video URL format")

        return len(errors) == 0, errors

    def validate_gemini_analysis(self, analysis_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate Gemini analysis data.

        Args:
            analysis_data: Analysis data from Gemini

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check if analysis was successful
        if not analysis_data.get('success', False):
            errors.append("Analysis was not successful")
            return False, errors

        # Check for analysis content
        analysis = analysis_data.get('analysis')
        if not analysis:
            errors.append("No analysis content found")
            return False, errors

        # Check for required analysis fields
        required_analysis_fields = ['visual_elements',
                                    'content_structure', 'engagement_factors']
        for field in required_analysis_fields:
            if field not in analysis:
                errors.append(f"Missing analysis field: {field}")

        # Check for minimum analysis length
        analysis_text = str(analysis)
        if len(analysis_text) < 100:
            errors.append("Analysis too short (possible error)")

        return len(errors) == 0, errors

    def filter_valid_videos(self, videos: List[Dict]) -> List[Dict]:
        """
        Filter videos to only include valid ones.

        Args:
            videos: List of video data

        Returns:
            List of valid videos
        """
        valid_videos = []

        for video in videos:
            is_valid, errors = self.validate_video(video)
            if is_valid:
                valid_videos.append(video)
            else:
                logger.warning(
                    f"Filtering out invalid video {video.get('id', 'unknown')}: {', '.join(errors)}")

        logger.info(f"Filtered {len(valid_videos)}/{len(videos)} valid videos")
        return valid_videos

    def validate_dataset_quality(self, dataset_path: Path) -> Dict:
        """
        Validate overall dataset quality.

        Args:
            dataset_path: Path to dataset directory

        Returns:
            Quality metrics dictionary
        """
        quality_metrics = {
            'total_videos': 0,
            'valid_videos': 0,
            'invalid_videos': 0,
            'avg_views': 0,
            'avg_engagement_rate': 0,
            'date_range': None,
            'quality_score': 0.0
        }

        # Load and validate dataset
        try:
            # This would need to be implemented based on your dataset structure
            # For now, return basic metrics
            pass
        except Exception as e:
            logger.error(f"Error validating dataset: {e}")

        return quality_metrics
