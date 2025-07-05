"""
Data validation utilities for TikTok pipeline
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class ValidationError:
    """Represents a validation error with type classification."""

    def __init__(self, message: str, error_type: str = "validation"):
        self.message = message
        self.error_type = error_type  # "validation", "critical", "warning"

    def __str__(self):
        return self.message


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

    def classify_error(self, error_message: str) -> str:
        """
        Classify error type based on error message.

        Args:
            error_message: The error message to classify

        Returns:
            Error type: "critical", "validation", or "warning"
        """
        # Critical errors - missing essential data
        critical_indicators = [
            "Missing video ID",
            "Missing required field: id",
            "Missing video URL",
            "Invalid video ID format",
            "Missing username"
        ]

        # Validation errors - data doesn't meet quality criteria
        validation_indicators = [
            "View count too low",
            "Video too old",
            "Video too short",
            "Video too long",
            "Detected sponsored content",
            "No valid videos found in account"
        ]

        # Warning errors - minor issues
        warning_indicators = [
            "Invalid view count",
            "Invalid video duration",
            "Invalid posting date"
        ]

        for indicator in critical_indicators:
            if indicator in error_message:
                return "critical"

        for indicator in validation_indicators:
            if indicator in error_message:
                return "validation"

        for indicator in warning_indicators:
            if indicator in error_message:
                return "warning"

        # Default to validation for unknown errors
        return "validation"

    def validate_account(self, account_data: Dict) -> Tuple[bool, List[ValidationError]]:
        """
        Validate account data from scraping.

        Args:
            account_data: Raw account data from scraper

        Returns:
            (is_valid, list_of_validation_errors)
        """
        errors = []

        # Check required fields
        if not account_data.get('username'):
            errors.append(ValidationError("Missing username", "critical"))

        if 'videos' not in account_data:
            errors.append(ValidationError("No videos field found", "critical"))
            return False, errors

        videos = account_data['videos']
        if not isinstance(videos, list):
            errors.append(ValidationError(
                "Videos field is not a list", "critical"))
            return False, errors

        # Check if account has videos
        if len(videos) == 0:
            errors.append(ValidationError(
                "Account has no videos", "validation"))
            return False, errors

        # Check for minimum video count
        if len(videos) < 1:
            errors.append(ValidationError(
                "Account has insufficient videos", "validation"))
            return False, errors

        # Validate each video
        valid_videos = 0
        for video in videos:
            is_valid, video_errors = self.validate_video(video)
            if is_valid:
                valid_videos += 1
            else:
                video_id = video.get('id', 'unknown')
                for error in video_errors:
                    errors.append(ValidationError(
                        f"Video {video_id}: {error.message}", error.error_type))

        # Check if we have enough valid videos
        if valid_videos == 0:
            errors.append(ValidationError(
                "No valid videos found in account", "validation"))
            return False, errors

        logger.info(
            f"Account {account_data.get('username')}: {valid_videos}/{len(videos)} valid videos")

        return True, errors

    def validate_video(self, video_data: Dict) -> Tuple[bool, List[ValidationError]]:
        """
        Validate individual video data.

        Args:
            video_data: Raw video data from scraper

        Returns:
            (is_valid, list_of_validation_errors)
        """
        errors = []

        # Check required fields
        for field in self.required_fields:
            if field not in video_data:
                error_type = "critical" if field == "id" else "validation"
                errors.append(ValidationError(
                    f"Missing required field: {field}", error_type))

        # Check video ID
        video_id = video_data.get('id')
        if not video_id:
            errors.append(ValidationError("Missing video ID", "critical"))
        elif not str(video_id).isdigit():
            errors.append(ValidationError(
                "Invalid video ID format", "critical"))

        # Check view count
        view_count = video_data.get('playCount', 0)
        if not isinstance(view_count, (int, float)) or view_count < 0:
            errors.append(ValidationError("Invalid view count", "warning"))
        elif view_count < self.min_views:
            errors.append(ValidationError(
                f"View count too low: {view_count} < {self.min_views}", "validation"))

        # Check engagement metrics
        for metric in ['diggCount', 'commentCount', 'shareCount']:
            count = video_data.get(metric, 0)
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(ValidationError(
                    f"Invalid {metric}: {count}", "warning"))

        # Check video duration
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if not isinstance(duration, (int, float)) or duration < 0:
            errors.append(ValidationError("Invalid video duration", "warning"))
        elif duration < self.min_video_duration:
            errors.append(ValidationError(
                f"Video too short: {duration}s < {self.min_video_duration}s", "validation"))
        elif duration > self.max_video_duration:
            errors.append(ValidationError(
                f"Video too long: {duration}s > {self.max_video_duration}s", "validation"))

        # Check posting date
        create_time = video_data.get('createTimeISO')
        if create_time:
            try:
                post_date = datetime.fromisoformat(
                    create_time.replace('Z', '+00:00'))
                age_days = (datetime.now(post_date.tzinfo) - post_date).days
                if age_days > self.max_video_age_days:
                    errors.append(ValidationError(
                        f"Video too old: {age_days} days > {self.max_video_age_days} days", "validation"))
            except Exception as e:
                errors.append(ValidationError(
                    f"Invalid posting date: {e}", "warning"))

        # Check for sponsored content indicators
        text = video_data.get('text', '').lower()
        sponsored_indicators = ['sponsored', 'ad',
                                'promotion', 'partnership', 'collab']
        if any(indicator in text for indicator in sponsored_indicators):
            errors.append(ValidationError(
                "Detected sponsored content", "validation"))

        # Check for valid video URL
        web_video_url = video_data.get('webVideoUrl')
        if not web_video_url:
            errors.append(ValidationError("Missing video URL", "critical"))
        elif not web_video_url.startswith('https://'):
            errors.append(ValidationError(
                "Invalid video URL format", "critical"))

        return len(errors) == 0, errors

    def has_critical_errors(self, errors: List[ValidationError]) -> bool:
        """Check if there are any critical errors in the list."""
        return any(error.error_type == "critical" for error in errors)

    def get_error_summary(self, errors: List[ValidationError]) -> Dict[str, List[str]]:
        """Get summary of errors by type."""
        summary = {
            "critical": [],
            "validation": [],
            "warning": []
        }

        for error in errors:
            summary[error.error_type].append(error.message)

        return summary

    def validate_gemini_analysis(self, analysis_data: Dict) -> Tuple[bool, List[ValidationError]]:
        """
        Validate Gemini analysis data.

        Args:
            analysis_data: Analysis data from Gemini

        Returns:
            (is_valid, list_of_validation_errors)
        """
        errors = []

        # Check if analysis was successful
        if not analysis_data.get('success', False):
            errors.append(ValidationError(
                "Analysis was not successful", "critical"))
            return False, errors

        # Check for analysis content
        analysis = analysis_data.get('analysis')
        if not analysis:
            errors.append(ValidationError(
                "No analysis content found", "critical"))
            return False, errors

        # Check for required analysis fields
        required_analysis_fields = ['visual_analysis',
                                    'content_structure', 'engagement_factors']
        for field in required_analysis_fields:
            if field not in analysis:
                errors.append(ValidationError(
                    f"Missing analysis field: {field}", "validation"))

        # Check for minimum analysis length
        analysis_text = str(analysis)
        if len(analysis_text) < 100:
            errors.append(ValidationError(
                "Analysis too short (possible error)", "validation"))

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
                # Log different error types appropriately
                error_summary = self.get_error_summary(errors)

                if error_summary["critical"]:
                    logger.error(
                        f"Critical errors for video {video.get('id', 'unknown')}: {', '.join(error_summary['critical'])}")
                if error_summary["validation"]:
                    logger.warning(
                        f"Validation errors for video {video.get('id', 'unknown')}: {', '.join(error_summary['validation'])}")
                if error_summary["warning"]:
                    logger.debug(
                        f"Warnings for video {video.get('id', 'unknown')}: {', '.join(error_summary['warning'])}")

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
