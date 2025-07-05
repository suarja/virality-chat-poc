"""
Data processor for combining TikTok data and Gemini analysis
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Process and combine TikTok data with Gemini analysis
    """

    def __init__(self):
        """Initialize data processor."""
        logger.info("Initializing DataProcessor")

    def load_raw_data(self, raw_data_path: Union[str, Path]) -> Dict:
        """
        Load and validate raw TikTok data from JSON file.

        Args:
            raw_data_path: Path to raw data JSON file

        Returns:
            Dictionary containing validated TikTok data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If data validation fails
            JSONDecodeError: If JSON parsing fails
        """
        raw_data_path = Path(raw_data_path)
        logger.info(f"Loading raw data from {raw_data_path}")

        if not raw_data_path.exists():
            raise FileNotFoundError(
                f"Raw data file not found: {raw_data_path}")

        try:
            with raw_data_path.open('r') as f:
                data = json.load(f)

            # Basic validation
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary")
            if 'videos' not in data:
                raise ValueError("Data must contain 'videos' key")
            if not isinstance(data['videos'], list):
                raise ValueError("'videos' must be a list")

            video_count = len(data['videos'])
            logger.info(
                f"Loaded {video_count} videos from {data.get('username', 'unknown')}")

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from {raw_data_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading raw data: {e}")
            raise

    def load_gemini_analysis(self, analysis_dir: Union[str, Path]) -> Dict[str, Dict]:
        """
        Load and validate Gemini analysis files from directory.

        Args:
            analysis_dir: Directory containing analysis JSON files

        Returns:
            Dictionary mapping video IDs to analysis results

        Raises:
            NotADirectoryError: If directory doesn't exist
            ValueError: If no analysis files found
        """
        analysis_dir = Path(analysis_dir)
        logger.info(f"Loading Gemini analysis from {analysis_dir}")

        if not analysis_dir.is_dir():
            raise NotADirectoryError(
                f"Analysis directory not found: {analysis_dir}")

        try:
            analyses = {}
            # Search recursively for analysis files (including date subdirectories)
            analysis_files = list(analysis_dir.rglob('video_*_analysis.json'))

            if not analysis_files:
                raise ValueError(f"No analysis files found in {analysis_dir}")

            for file_path in analysis_files:
                try:
                    with file_path.open('r') as f:
                        analysis_data = json.load(f)

                    # Extract video ID from filename (new format)
                    # Now directly the TikTok video ID
                    video_id = file_path.stem.split('_')[1]

                    if not analysis_data.get('success'):
                        logger.warning(
                            f"Analysis unsuccessful for video {video_id}")
                        continue

                    if 'analysis' not in analysis_data:
                        logger.warning(
                            f"No analysis data found in {file_path}")
                        continue

                    analyses[video_id] = analysis_data['analysis']

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    continue

            if not analyses:
                raise ValueError("No valid analysis data found")

            logger.info(f"Loaded {len(analyses)} analysis files successfully")
            return analyses

        except Exception as e:
            logger.error(f"Error loading Gemini analysis: {e}")
            raise

    def extract_features(self, video_data: Dict) -> Dict:
        """Extract basic features from video data."""
        features = {
            'title': video_data.get('text', ''),
            'description': video_data.get('text', ''),
            'duration': video_data.get('videoMeta', {}).get('duration', 0),
            'post_time': video_data.get('createTimeISO', ''),
            'extraction_time': datetime.now().isoformat(),
            'view_count': video_data.get('playCount', 0),
            'like_count': video_data.get('diggCount', 0),
            'comment_count': video_data.get('commentCount', 0),
            'share_count': video_data.get('shareCount', 0),
        }

        # Calculate engagement rates
        if features['view_count'] > 0:
            features['like_rate'] = features['like_count'] / \
                features['view_count']
            features['comment_rate'] = features['comment_count'] / \
                features['view_count']
            features['share_rate'] = features['share_count'] / \
                features['view_count']
            features['engagement_rate'] = (features['like_count'] + features['comment_count'] +
                                           features['share_count']) / features['view_count']
        else:
            features['like_rate'] = 0
            features['comment_rate'] = 0
            features['share_rate'] = 0
            features['engagement_rate'] = 0

        # Extract hashtags
        hashtags = [tag['name'] for tag in video_data.get('hashtags', [])]
        features['hashtags'] = ','.join(hashtags)
        features['hashtag_count'] = len(hashtags)

        # Extract music info
        music_meta = video_data.get('musicMeta', {})
        features['music_info'] = f"{music_meta.get('musicAuthor', '')} - {music_meta.get('musicName', '')}"

        # Extract temporal features
        if features['post_time']:
            post_time = pd.to_datetime(features['post_time'])
            features['hour_of_day'] = post_time.hour
            features['day_of_week'] = post_time.dayofweek
            features['month'] = post_time.month
            features['is_weekend'] = post_time.dayofweek >= 5
            features['is_business_hours'] = 9 <= post_time.hour <= 17

        return features

    def process_video(
        self,
        video_data: Dict,
        gemini_analysis: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """Process a single video's data and analysis."""
        try:
            # Extract video ID
            video_id = str(video_data.get('id'))
            if not video_id:
                logger.warning("Video missing ID, skipping")
                return {}, {"is_valid": False, "error": "Missing video ID"}

            # Extract basic features
            features = self.extract_features(video_data)
            features['video_id'] = video_id

            # Add Gemini analysis features if available
            if gemini_analysis:
                gemini_features = self.extract_gemini_features(gemini_analysis)
                features.update(gemini_features)
            else:
                logger.warning(
                    f"No Gemini analysis found for video {video_id}")

            metadata = {
                "is_valid": True,
                "video_id": video_id,
                "processed_at": datetime.now().isoformat()
            }

            return features, metadata

        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return {}, {"is_valid": False, "error": str(e)}

    def process_dataset(
        self,
        raw_data_path: Union[str, Path],
        gemini_analysis_dir: Union[str, Path],
        output_dir: Union[str, Path]
    ) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Process complete dataset with TikTok data and Gemini analysis.

        Args:
            raw_data_path: Path to raw TikTok data JSON
            gemini_analysis_dir: Directory containing Gemini analysis files
            output_dir: Directory to save processed features

        Returns:
            Tuple of (features DataFrame, list of metadata dictionaries)
        """
        # Convert all paths to Path objects
        raw_data_path = Path(raw_data_path)
        gemini_analysis_dir = Path(gemini_analysis_dir)
        output_dir = Path(output_dir)

        try:
            # Load and validate data
            raw_data = self.load_raw_data(raw_data_path)
            gemini_analyses = self.load_gemini_analysis(gemini_analysis_dir)

            # Process each video
            all_features = []
            all_metadata = []

            for video in raw_data['videos']:
                try:
                    video_id = video.get('id')
                    if not video_id:
                        logger.warning("Video missing ID, skipping")
                        continue

                    gemini_analysis = gemini_analyses.get(video_id)
                    if not gemini_analysis:
                        logger.warning(
                            f"No Gemini analysis found for video {video_id}")

                    features, metadata = self.process_video(
                        video, gemini_analysis)
                    all_features.append(features)
                    all_metadata.append(metadata)

                except Exception as e:
                    logger.error(
                        f"Error processing video {video.get('id', 'unknown')}: {e}")
                    continue

            if not all_features:
                raise ValueError("No features extracted from any videos")

            # Convert to DataFrame
            features_df = pd.DataFrame(all_features)

            # Save processed features
            output_path = output_dir / 'processed_features.csv'
            features_df.to_csv(output_path, index=False)
            logger.info(f"Saved processed features to {output_path}")

            return features_df, all_metadata

        except Exception as e:
            logger.error(f"Error processing dataset: {e}")
            raise

    def extract_gemini_features(self, analysis: Dict) -> Dict:
        """Extract features from Gemini analysis."""
        features = {}

        try:
            # Visual Analysis Features
            visual = analysis.get('visual_analysis', {})
            features['has_text_overlays'] = 'text overlays' in visual.get(
                'text_overlays', '').lower()
            features['has_transitions'] = 'transitions' in visual.get(
                'transitions', '').lower()
            features['visual_quality_score'] = 1.0 if 'high quality' in visual.get(
                'style_quality', '').lower() else 0.5

            # Content Structure Features
            content = analysis.get('content_structure', {})
            features['has_hook'] = 1.0 if 'effective' in content.get(
                'hook_effectiveness', '').lower() else 0.5
            features['has_story'] = 'story' in content.get(
                'story_flow', '').lower()
            features['has_call_to_action'] = 'call to action' in content.get(
                'call_to_action', '').lower()

            # Engagement Features
            engagement = analysis.get('engagement_factors', {})
            features['viral_potential_score'] = 1.0 if 'high' in engagement.get(
                'viral_potential', '').lower() else 0.5
            features['emotional_trigger_count'] = len(
                engagement.get('emotional_triggers', '').split(','))
            features['audience_connection_score'] = 1.0 if 'strong' in engagement.get(
                'audience_connection', '').lower() else 0.5

            # Technical Features
            technical = analysis.get('technical_elements', {})
            features['length_optimized'] = 'appropriate' in technical.get(
                'length_optimization', '').lower()
            features['sound_quality_score'] = 1.0 if 'high quality' in technical.get(
                'sound_design', '').lower() else 0.5
            features['production_quality_score'] = 1.0 if 'high' in technical.get(
                'production_quality', '').lower() else 0.5

            # Trend Features
            trends = analysis.get('trend_alignment', {})
            features['trend_alignment_score'] = 1.0 if 'perfectly' in trends.get(
                'current_trends', '').lower() else 0.5
            features['estimated_hashtag_count'] = len(
                trends.get('hashtag_potential', '').split('#')) - 1

            return features

        except Exception as e:
            logger.error(f"Error extracting Gemini features: {str(e)}")
            return {}
