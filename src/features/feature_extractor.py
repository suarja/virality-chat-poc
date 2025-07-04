"""
Feature extraction for TikTok video virality prediction.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from sklearn.preprocessing import StandardScaler


class FeatureSchema(BaseModel):
    """Schema for extracted features."""

    # Basic metrics
    video_id: str = Field(..., description="Unique video identifier")
    title: str = Field(..., description="Video title")
    description: Optional[str] = Field(None, description="Video description")
    duration: float = Field(..., description="Video duration in seconds")

    # Engagement metrics
    view_count: int = Field(..., description="Number of views")
    like_count: int = Field(..., description="Number of likes")
    comment_count: int = Field(..., description="Number of comments")
    share_count: int = Field(..., description="Number of shares")

    # Content features
    hashtags: List[str] = Field(
        default_factory=list, description="List of hashtags")
    music_info: Optional[Dict] = Field(None, description="Music information")

    # Temporal features
    post_time: pd.Timestamp = Field(..., description="Time of posting")
    extraction_time: pd.Timestamp = Field(...,
                                          description="Time of data extraction")

    class Config:
        arbitrary_types_allowed = True


@dataclass
class FeatureExtractor:
    """Extract and transform features from TikTok video data."""

    def __init__(self):
        """Initialize feature extractor."""
        self.scaler = StandardScaler()
        self._is_fitted = False

    def extract_basic_features(self, video_data: Dict) -> Dict:
        """
        Extract basic video features.

        Args:
            video_data: Raw video data dictionary

        Returns:
            Dictionary of basic features
        """
        return {
            "video_id": video_data["id"],
            "title": video_data.get("title", ""),
            "description": video_data.get("description", ""),
            "duration": float(video_data.get("duration", 0)),
            "post_time": pd.to_datetime(video_data["createTime"], unit="s"),
            "extraction_time": pd.Timestamp.now()
        }

    def extract_engagement_features(self, video_data: Dict) -> Dict:
        """
        Extract engagement metrics.

        Args:
            video_data: Raw video data dictionary

        Returns:
            Dictionary of engagement features
        """
        stats = video_data.get("stats", {})
        return {
            "view_count": int(stats.get("playCount", 0)),
            "like_count": int(stats.get("diggCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "share_count": int(stats.get("shareCount", 0))
        }

    def calculate_engagement_ratios(self, engagement_features: Dict) -> Dict:
        """
        Calculate engagement ratios.

        Args:
            engagement_features: Dictionary of engagement metrics

        Returns:
            Dictionary of engagement ratios
        """
        views = engagement_features["view_count"]
        if views == 0:
            return {
                "like_rate": 0.0,
                "comment_rate": 0.0,
                "share_rate": 0.0,
                "engagement_rate": 0.0
            }

        return {
            "like_rate": engagement_features["like_count"] / views,
            "comment_rate": engagement_features["comment_count"] / views,
            "share_rate": engagement_features["share_count"] / views,
            "engagement_rate": (
                engagement_features["like_count"] +
                engagement_features["comment_count"] +
                engagement_features["share_count"]
            ) / views
        }

    def extract_content_features(self, video_data: Dict) -> Dict:
        """
        Extract content-related features.

        Args:
            video_data: Raw video data dictionary

        Returns:
            Dictionary of content features
        """
        # Extract hashtags
        hashtags = []
        if "challenges" in video_data:
            hashtags.extend(
                challenge["title"]
                for challenge in video_data["challenges"]
            )

        # Extract music info
        music_info = None
        if "music" in video_data:
            music_info = {
                "title": video_data["music"].get("title"),
                "author": video_data["music"].get("authorName"),
                "duration": video_data["music"].get("duration"),
                "original": video_data["music"].get("original", False)
            }

        return {
            "hashtags": hashtags,
            "music_info": music_info,
            "hashtag_count": len(hashtags)
        }

    def extract_temporal_features(self, post_time: pd.Timestamp) -> Dict:
        """
        Extract temporal features from posting time.

        Args:
            post_time: Time when video was posted

        Returns:
            Dictionary of temporal features
        """
        return {
            "hour_of_day": post_time.hour,
            "day_of_week": post_time.dayofweek,
            "month": post_time.month,
            "is_weekend": post_time.dayofweek >= 5,
            "is_business_hours": 9 <= post_time.hour <= 17
        }

    def extract_all_features(
        self,
        video_data: Dict,
        normalize: bool = True
    ) -> Tuple[Dict, Dict]:
        """
        Extract all features from video data.

        Args:
            video_data: Raw video data dictionary
            normalize: Whether to normalize numerical features

        Returns:
            Tuple of (features dict, metadata dict)
        """
        # Track extraction metadata
        metadata = {
            "extraction_start": pd.Timestamp.now(),
            "features_extracted": []
        }

        try:
            # Extract basic features
            features = self.extract_basic_features(video_data)
            metadata["features_extracted"].append("basic")

            # Extract engagement features
            engagement = self.extract_engagement_features(video_data)
            features.update(engagement)
            metadata["features_extracted"].append("engagement")

            # Calculate engagement ratios
            ratios = self.calculate_engagement_ratios(engagement)
            features.update(ratios)
            metadata["features_extracted"].append("ratios")

            # Extract content features
            content = self.extract_content_features(video_data)
            features.update(content)
            metadata["features_extracted"].append("content")

            # Extract temporal features
            temporal = self.extract_temporal_features(features["post_time"])
            features.update(temporal)
            metadata["features_extracted"].append("temporal")

            # Normalize numerical features if requested
            if normalize:
                numerical_features = [
                    "duration",
                    "view_count", "like_count", "comment_count", "share_count",
                    "like_rate", "comment_rate", "share_rate", "engagement_rate",
                    "hashtag_count", "hour_of_day", "day_of_week", "month"
                ]

                features_array = np.array([features[f]
                                          for f in numerical_features])
                if not self._is_fitted:
                    features_array = self.scaler.fit_transform(
                        features_array.reshape(1, -1))
                    self._is_fitted = True
                else:
                    features_array = self.scaler.transform(
                        features_array.reshape(1, -1))

                for i, feature in enumerate(numerical_features):
                    features[f"{feature}_normalized"] = features_array[0, i]

                metadata["features_extracted"].append("normalized")

            # Validate against schema
            FeatureSchema(**features)
            metadata["is_valid"] = True

        except Exception as e:
            metadata["error"] = str(e)
            metadata["is_valid"] = False
            raise

        finally:
            metadata["extraction_end"] = pd.Timestamp.now()
            metadata["extraction_time_ms"] = (
                metadata["extraction_end"] - metadata["extraction_start"]
            ).total_seconds() * 1000

        return features, metadata

    def process_batch(
        self,
        video_data_list: List[Dict],
        normalize: bool = True
    ) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Process a batch of videos.

        Args:
            video_data_list: List of raw video data dictionaries
            normalize: Whether to normalize numerical features

        Returns:
            Tuple of (features DataFrame, list of metadata dicts)
        """
        all_features = []
        all_metadata = []

        for video_data in video_data_list:
            try:
                features, metadata = self.extract_all_features(
                    video_data,
                    normalize=normalize
                )
                all_features.append(features)
                all_metadata.append(metadata)
            except Exception as e:
                print(
                    f"Error processing video {video_data.get('id', 'unknown')}: {e}")
                continue

        return pd.DataFrame(all_features), all_metadata

    def save_features(
        self,
        features_df: pd.DataFrame,
        output_dir: Path,
        filename: str = "extracted_features.csv"
    ) -> Path:
        """
        Save extracted features to CSV.

        Args:
            features_df: DataFrame of extracted features
            output_dir: Output directory
            filename: Output filename

        Returns:
            Path to saved file
        """
        output_path = output_dir / filename
        features_df.to_csv(output_path, index=False)
        return output_path
