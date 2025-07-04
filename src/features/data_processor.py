"""
Data processor for combining TikTok data and Gemini analysis
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime

import pandas as pd
from .feature_extractor import FeatureExtractor
from pydantic import BaseModel, Field, validator, model_validator

logger = logging.getLogger(__name__)


class RawDataSchema(BaseModel):
    """Schema for raw TikTok data validation."""
    videos: List[Dict] = Field(..., description="List of video data")
    scraped_at: Union[str, float] = Field(...,
                                          description="Timestamp of data collection")
    username: str = Field(...,
                          description="TikTok account name")

    class Config:
        validate_by_name = True
        extra = "allow"

    @validator('scraped_at')
    def validate_timestamp(cls, v):
        if isinstance(v, float):
            return datetime.fromtimestamp(v).isoformat()
        return v

    @model_validator(mode='before')
    def map_username_to_account(cls, values):
        if isinstance(values, dict):
            if 'account' not in values and 'username' in values:
                values['account'] = values['username']
            elif 'username' not in values and 'account' in values:
                values['username'] = values['account']
        return values


class DataProcessor:
    """
    Process and combine TikTok data with Gemini analysis
    """

    def __init__(self, feature_extractor: Optional[FeatureExtractor] = None):
        """
        Initialize data processor.

        Args:
            feature_extractor: Optional FeatureExtractor instance
        """
        self.feature_extractor = feature_extractor or FeatureExtractor()
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

            # Validate data structure
            validated_data = RawDataSchema(**data).dict()

            video_count = len(validated_data['videos'])
            logger.info(
                f"Loaded {video_count} videos from {validated_data['username']}")

            return validated_data

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
            analysis_files = list(analysis_dir.glob('video_*_analysis_*.json'))

            if not analysis_files:
                raise ValueError(f"No analysis files found in {analysis_dir}")

            for file_path in analysis_files:
                try:
                    with file_path.open('r') as f:
                        analysis_data = json.load(f)

                    # Extract video ID from filename
                    video_id = file_path.stem.split('_')[1]

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

    def extract_gemini_features(self, analysis: Dict) -> Dict:
        """
        Extract features from Gemini analysis.

        Args:
            analysis: Gemini analysis dictionary

        Returns:
            Dictionary of extracted features
        """
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
            raise

    def process_video(
        self,
        video_data: Dict,
        gemini_analysis: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        Process a single video, combining TikTok data with Gemini analysis.

        Args:
            video_data: Raw video data dictionary
            gemini_analysis: Optional Gemini analysis dictionary

        Returns:
            Tuple of (combined features dict, metadata dict)
        """
        try:
            # Start metadata tracking
            metadata = {
                'video_id': video_data.get('id'),
                'features_extracted': [],
                'extraction_start': pd.Timestamp.now().isoformat(),
                'warnings': []
            }

            # Extract basic features
            features = {}
            features.update(
                self.feature_extractor.extract_basic_features(video_data))
            metadata['features_extracted'].append('basic')

            # Extract engagement features
            features.update(
                self.feature_extractor.extract_engagement_features(video_data))
            metadata['features_extracted'].append('engagement')

            # Calculate engagement ratios
            features.update(
                self.feature_extractor.calculate_engagement_ratios(features))
            metadata['features_extracted'].append('ratios')

            # Extract content features
            features.update(
                self.feature_extractor.extract_content_features(video_data))
            metadata['features_extracted'].append('content')

            # Extract temporal features
            features.update(self.feature_extractor.extract_temporal_features(
                pd.Timestamp(video_data.get('createTime', 0), unit='s')
            ))
            metadata['features_extracted'].append('temporal')

            # Add Gemini features if available
            if gemini_analysis:
                try:
                    gemini_features = self.extract_gemini_features(
                        gemini_analysis)
                    features.update(gemini_features)
                    metadata['features_extracted'].append('gemini_analysis')
                except Exception as e:
                    metadata['warnings'].append(
                        f"Gemini feature extraction failed: {str(e)}")

            # Update metadata
            metadata['extraction_time_ms'] = (
                pd.Timestamp.now() - pd.Timestamp(metadata['extraction_start'])
            ).total_seconds() * 1000
            metadata['is_valid'] = len(metadata['warnings']) == 0

            return features, metadata

        except Exception as e:
            logger.error(
                f"Error processing video {video_data.get('id')}: {str(e)}")
            raise

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
