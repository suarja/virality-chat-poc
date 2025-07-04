"""Unit tests for data processor."""
import json
from pathlib import Path
from datetime import datetime

import pytest
import pandas as pd

from src.features.data_processor import DataProcessor
from src.features.feature_extractor import FeatureExtractor


@pytest.fixture
def sample_raw_data():
    """Sample raw TikTok data for testing."""
    return {
        "username": "test_user",
        "scraped_at": datetime.now().timestamp(),
        "videos": [
            {
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
        ]
    }


@pytest.fixture
def sample_gemini_analysis():
    """Sample Gemini analysis data for testing."""
    return {
        "visual_analysis": {
            "text_overlays": "There are visible text overlays",
            "transitions": "There are transitions",
            "style_quality": "High quality"
        },
        "content_structure": {
            "hook_effectiveness": "Highly effective hook",
            "story_flow": "Has narrative story",
            "call_to_action": "Has explicit call to action"
        },
        "engagement_factors": {
            "viral_potential": "High viral potential",
            "emotional_triggers": "joy, excitement, surprise",
            "audience_connection": "Strong connection"
        },
        "technical_elements": {
            "length_optimization": "Appropriate length",
            "sound_design": "High quality sound",
            "production_quality": "High production quality"
        },
        "trend_alignment": {
            "current_trends": "Perfectly aligns with trends",
            "hashtag_potential": "#viral #trending #test"
        }
    }


@pytest.fixture
def data_processor():
    """Data processor instance."""
    return DataProcessor()


def test_load_raw_data(data_processor, sample_raw_data, tmp_path):
    """Test loading raw data."""
    # Save sample data
    raw_data_path = tmp_path / "test_raw_data.json"
    with open(raw_data_path, 'w') as f:
        json.dump(sample_raw_data, f)

    # Load and verify
    loaded_data = data_processor.load_raw_data(raw_data_path)
    assert loaded_data["username"] == sample_raw_data["username"]
    assert len(loaded_data["videos"]) == len(sample_raw_data["videos"])


def test_load_gemini_analysis(data_processor, sample_gemini_analysis, tmp_path):
    """Test loading Gemini analysis."""
    # Create analysis directory
    analysis_dir = tmp_path / "gemini_analysis"
    analysis_dir.mkdir()

    # Save sample analysis
    analysis_path = analysis_dir / "video_7123456789_analysis.json"
    with open(analysis_path, 'w') as f:
        json.dump({"analysis": sample_gemini_analysis}, f)

    # Load and verify
    analyses = data_processor.load_gemini_analysis(analysis_dir)
    assert len(analyses) == 1
    assert "video_7123456789_analysis" in analyses


def test_extract_gemini_features(data_processor, sample_gemini_analysis):
    """Test Gemini feature extraction."""
    features = data_processor.extract_gemini_features(sample_gemini_analysis)

    # Check visual features
    assert features["has_text_overlays"] is True
    assert features["has_transitions"] is True
    assert features["visual_quality_score"] == 1.0

    # Check content features
    assert features["has_hook"] == 1.0
    assert features["has_story"] is True
    assert features["has_call_to_action"] is True

    # Check engagement features
    assert features["viral_potential_score"] == 1.0
    assert features["emotional_trigger_count"] == 3
    assert features["audience_connection_score"] == 1.0

    # Check technical features
    assert features["length_optimized"] is True
    assert features["sound_quality_score"] == 1.0
    assert features["production_quality_score"] == 1.0

    # Check trend features
    assert features["trend_alignment_score"] == 1.0
    assert features["estimated_hashtag_count"] == 3


def test_process_video(data_processor, sample_raw_data, sample_gemini_analysis):
    """Test processing single video."""
    video_data = sample_raw_data["videos"][0]
    features, metadata = data_processor.process_video(
        video_data, sample_gemini_analysis)

    # Check basic features
    assert features["video_id"] == video_data["id"]
    assert features["title"] == video_data["title"]

    # Check Gemini features were added
    assert "viral_potential_score" in features
    assert "visual_quality_score" in features

    # Check metadata
    assert "gemini_analysis" in metadata["features_extracted"]
    assert metadata["is_valid"] is True


def test_process_dataset(
    data_processor,
    sample_raw_data,
    sample_gemini_analysis,
    tmp_path
):
    """Test processing full dataset."""
    # Setup test files
    raw_data_path = tmp_path / "test_raw_data.json"
    with open(raw_data_path, 'w') as f:
        json.dump(sample_raw_data, f)

    analysis_dir = tmp_path / "gemini_analysis"
    analysis_dir.mkdir()
    analysis_path = analysis_dir / "video_7123456789_analysis.json"
    with open(analysis_path, 'w') as f:
        json.dump({"analysis": sample_gemini_analysis}, f)

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Process dataset
    features_df, metadata_list = data_processor.process_dataset(
        raw_data_path,
        analysis_dir,
        output_dir
    )

    # Check results
    assert len(features_df) == len(sample_raw_data["videos"])
    assert len(metadata_list) == len(sample_raw_data["videos"])
    assert (output_dir / "processed_features.csv").exists()


def test_error_handling(data_processor):
    """Test error handling with invalid data."""
    invalid_data = {"id": "123"}  # Missing required fields

    with pytest.raises(Exception):
        data_processor.process_video(invalid_data)
