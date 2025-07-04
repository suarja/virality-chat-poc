"""Unit tests for feature extractor."""
import json
from pathlib import Path
from datetime import datetime

import pytest
import pandas as pd

from src.features.feature_extractor import FeatureExtractor, FeatureSchema


@pytest.fixture
def sample_video_data():
    """Sample video data for testing."""
    return {
        "id": "7123456789",
        "title": "Test video #test",
        "description": "Test description",
        "duration": 30,
        "createTime": int(datetime.now().timestamp()),
        "stats": {
            "playCount": 1000,
            "diggCount": 100,
            "commentCount": 50,
            "shareCount": 25
        },
        "challenges": [
            {"title": "test"},
            {"title": "sample"}
        ],
        "music": {
            "title": "Test Sound",
            "authorName": "Test Author",
            "duration": 30,
            "original": True
        }
    }


@pytest.fixture
def feature_extractor():
    """Feature extractor instance."""
    return FeatureExtractor()


def test_extract_basic_features(feature_extractor, sample_video_data):
    """Test basic feature extraction."""
    features = feature_extractor.extract_basic_features(sample_video_data)

    assert features["video_id"] == sample_video_data["id"]
    assert features["title"] == sample_video_data["title"]
    assert features["description"] == sample_video_data["description"]
    assert features["duration"] == float(sample_video_data["duration"])
    assert isinstance(features["post_time"], pd.Timestamp)
    assert isinstance(features["extraction_time"], pd.Timestamp)


def test_extract_engagement_features(feature_extractor, sample_video_data):
    """Test engagement feature extraction."""
    features = feature_extractor.extract_engagement_features(sample_video_data)

    assert features["view_count"] == sample_video_data["stats"]["playCount"]
    assert features["like_count"] == sample_video_data["stats"]["diggCount"]
    assert features["comment_count"] == sample_video_data["stats"]["commentCount"]
    assert features["share_count"] == sample_video_data["stats"]["shareCount"]


def test_calculate_engagement_ratios(feature_extractor):
    """Test engagement ratio calculations."""
    engagement_features = {
        "view_count": 1000,
        "like_count": 100,
        "comment_count": 50,
        "share_count": 25
    }

    ratios = feature_extractor.calculate_engagement_ratios(engagement_features)

    assert ratios["like_rate"] == 0.1  # 100/1000
    assert ratios["comment_rate"] == 0.05  # 50/1000
    assert ratios["share_rate"] == 0.025  # 25/1000
    assert ratios["engagement_rate"] == 0.175  # (100+50+25)/1000


def test_extract_content_features(feature_extractor, sample_video_data):
    """Test content feature extraction."""
    features = feature_extractor.extract_content_features(sample_video_data)

    assert len(features["hashtags"]) == 2
    assert "test" in features["hashtags"]
    assert features["hashtag_count"] == 2
    assert features["music_info"]["title"] == sample_video_data["music"]["title"]


def test_extract_temporal_features(feature_extractor):
    """Test temporal feature extraction."""
    post_time = pd.Timestamp.now()
    features = feature_extractor.extract_temporal_features(post_time)

    assert 0 <= features["hour_of_day"] <= 23
    assert 0 <= features["day_of_week"] <= 6
    assert 1 <= features["month"] <= 12
    assert isinstance(features["is_weekend"], bool)
    assert isinstance(features["is_business_hours"], bool)


def test_extract_all_features(feature_extractor, sample_video_data):
    """Test complete feature extraction pipeline."""
    features, metadata = feature_extractor.extract_all_features(
        sample_video_data)

    # Validate against schema
    feature_schema = FeatureSchema(**features)

    # Check metadata
    assert "extraction_start" in metadata
    assert "features_extracted" in metadata
    assert "extraction_time_ms" in metadata
    assert "is_valid" in metadata
    assert metadata["is_valid"] is True


def test_process_batch(feature_extractor, sample_video_data):
    """Test batch processing."""
    batch = [sample_video_data, sample_video_data]  # Use same data twice
    features_df, metadata_list = feature_extractor.process_batch(batch)

    assert len(features_df) == 2
    assert len(metadata_list) == 2
    assert all(m["is_valid"] for m in metadata_list)


def test_save_features(feature_extractor, tmp_path):
    """Test feature saving."""
    features_df = pd.DataFrame({
        "video_id": ["1", "2"],
        "title": ["Test 1", "Test 2"]
    })

    output_path = feature_extractor.save_features(
        features_df,
        tmp_path,
        "test_features.csv"
    )

    assert output_path.exists()
    loaded_df = pd.read_csv(output_path)
    assert len(loaded_df) == len(features_df)


def test_error_handling(feature_extractor):
    """Test error handling with invalid data."""
    invalid_data = {"id": "123"}  # Missing required fields

    with pytest.raises(Exception):
        feature_extractor.extract_all_features(invalid_data)
