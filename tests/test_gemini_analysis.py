"""
Tests for the Gemini analysis pipeline.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pytest
from pydantic import ValidationError

from virality_chat_poc.models.gemini_analysis import (
    GeminiAnalysis, GeminiResponse, BatchAnalysisResult,
    VisualAnalysis, ContentStructure, EngagementFactors,
    TechnicalElements, TrendAlignment, AnalysisMetrics
)
from virality_chat_poc.run_gemini_analysis import (
    generate_analysis_prompt,
    parse_gemini_response,
    analyze_video,
    process_videos
)

# Test data
MOCK_VIDEO_DATA = {
    'id': 'test123',
    'duration': 30,
    'description': 'Test video',
    'music_info': {'title': 'Test song'}
}

MOCK_GEMINI_RESPONSE = """
Clear text overlays with good contrast

Smooth transitions between scenes

High quality visuals throughout

Strong hook in first 3 seconds

Clear narrative progression

Clear call-to-action at end

High viral potential

Joy, excitement, inspiration, motivation

Strong audience engagement through relatability

Appropriate length for content

Professional sound mixing

High production value

Aligns with current fitness trends

#fitness #motivation #healthylifestyle #workout
"""


@pytest.fixture
def mock_video_data() -> Dict:
    """Fixture for mock video data."""
    return MOCK_VIDEO_DATA.copy()


@pytest.fixture
def mock_gemini_response() -> str:
    """Fixture for mock Gemini response."""
    return MOCK_GEMINI_RESPONSE.strip()


def test_visual_analysis_validation():
    """Test VisualAnalysis model validation."""
    # Valid data
    valid_data = {
        'text_overlays': 'Clear text with good contrast',
        'transitions': 'Smooth transitions',
        'style_quality': 'High quality visuals'
    }
    analysis = VisualAnalysis(**valid_data)
    assert analysis.text_overlays == valid_data['text_overlays']

    # Invalid style quality
    with pytest.raises(ValidationError):
        VisualAnalysis(
            text_overlays='Clear text',
            transitions='Smooth',
            style_quality='Invalid quality'  # Missing quality level
        )


def test_content_structure_validation():
    """Test ContentStructure model validation."""
    # Valid data
    valid_data = {
        'hook_effectiveness': 'Strong hook in first 3 seconds',
        'story_flow': 'Clear progression',
        'call_to_action': 'Clear CTA'
    }
    content = ContentStructure(**valid_data)
    assert content.hook_effectiveness == valid_data['hook_effectiveness']

    # Invalid hook effectiveness
    with pytest.raises(ValidationError):
        ContentStructure(
            hook_effectiveness='Hook exists',  # Missing effectiveness level
            story_flow='Clear',
            call_to_action='CTA'
        )


def test_engagement_factors_validation():
    """Test EngagementFactors model validation."""
    # Valid data
    valid_data = {
        'viral_potential': 'High potential',
        'emotional_triggers': 'joy, excitement, motivation',
        'audience_connection': 'Strong connection'
    }
    factors = EngagementFactors(**valid_data)
    assert factors.emotional_triggers == valid_data['emotional_triggers']

    # Invalid emotional triggers
    with pytest.raises(ValidationError):
        EngagementFactors(
            viral_potential='High',
            emotional_triggers='no commas here',  # Missing commas
            audience_connection='Strong'
        )


def test_technical_elements_validation():
    """Test TechnicalElements model validation."""
    # Valid data
    valid_data = {
        'length_optimization': 'appropriate length',
        'sound_design': 'Professional audio',
        'production_quality': 'High quality'
    }
    elements = TechnicalElements(**valid_data)
    assert elements.length_optimization == valid_data['length_optimization']

    # Invalid length optimization
    with pytest.raises(ValidationError):
        TechnicalElements(
            length_optimization='some length',  # Missing optimization assessment
            sound_design='Good',
            production_quality='High'
        )


def test_trend_alignment_validation():
    """Test TrendAlignment model validation."""
    # Valid data
    valid_data = {
        'current_trends': 'Aligns with trends',
        'hashtag_potential': '#trending #viral'
    }
    alignment = TrendAlignment(**valid_data)
    assert alignment.hashtag_potential == valid_data['hashtag_potential']

    # Invalid hashtag potential
    with pytest.raises(ValidationError):
        TrendAlignment(
            current_trends='Trending',
            hashtag_potential='no hashtags here'  # Missing hashtags
        )


def test_analysis_metrics_calculation():
    """Test AnalysisMetrics score calculation."""
    metrics = AnalysisMetrics(
        completeness_score=0.9,
        consistency_score=0.8,
        specificity_score=0.7,
        actionability_score=0.6
    )

    # Test overall score calculation
    expected_score = (
        0.9 * 0.3 +  # completeness
        0.8 * 0.2 +  # consistency
        0.7 * 0.3 +  # specificity
        0.6 * 0.2    # actionability
    )
    assert metrics.overall_score == pytest.approx(expected_score)


def test_generate_analysis_prompt(mock_video_data):
    """Test analysis prompt generation."""
    prompt = generate_analysis_prompt(mock_video_data)

    # Check prompt structure
    assert 'Visual Analysis' in prompt
    assert 'Content Structure' in prompt
    assert 'Engagement Factors' in prompt
    assert 'Technical Elements' in prompt
    assert 'Trend Alignment' in prompt

    # Check video details
    assert str(mock_video_data['duration']) in prompt
    assert mock_video_data['description'] in prompt
    assert mock_video_data['music_info']['title'] in prompt


def test_parse_gemini_response(mock_gemini_response):
    """Test Gemini response parsing."""
    video_id = 'test123'
    result = parse_gemini_response(mock_gemini_response, video_id)

    # Check successful parsing
    assert result.success
    assert result.video_id == video_id
    assert result.analysis is not None

    # Check metrics
    assert result.metrics is not None
    assert 0 <= result.metrics['completeness_score'] <= 1
    assert 0 <= result.metrics['consistency_score'] <= 1
    assert 0 <= result.metrics['specificity_score'] <= 1
    assert 0 <= result.metrics['actionability_score'] <= 1


@pytest.mark.asyncio
async def test_analyze_video(mock_video_data, tmp_path):
    """Test video analysis."""
    # Mock Gemini model
    class MockGeminiModel:
        async def generate_content(self, prompt):
            class MockResponse:
                text = MOCK_GEMINI_RESPONSE
            return MockResponse()

    model = MockGeminiModel()
    result = await analyze_video(model, mock_video_data, tmp_path)

    # Check analysis result
    assert result.success
    assert result.video_id == mock_video_data['id']
    assert result.analysis is not None

    # Check file creation
    output_file = tmp_path / f"video_{mock_video_data['id']}_analysis.json"
    assert output_file.exists()

    # Verify file content
    with output_file.open('r') as f:
        saved_data = json.load(f)
        assert saved_data['success']
        assert saved_data['video_id'] == mock_video_data['id']


@pytest.mark.asyncio
async def test_process_videos(tmp_path):
    """Test batch video processing."""
    # Create mock raw data
    raw_data = {
        'videos': [
            MOCK_VIDEO_DATA,
            {**MOCK_VIDEO_DATA, 'id': 'test456'}
        ]
    }
    raw_data_file = tmp_path / 'raw_data.json'
    with raw_data_file.open('w') as f:
        json.dump(raw_data, f)

    # Mock Gemini model
    class MockGeminiModel:
        async def generate_content(self, prompt):
            class MockResponse:
                text = MOCK_GEMINI_RESPONSE
            return MockResponse()

    # Patch setup_gemini to return mock model
    import virality_chat_poc.run_gemini_analysis as run_gemini_analysis
    original_setup = run_gemini_analysis.setup_gemini
    run_gemini_analysis.setup_gemini = lambda: MockGeminiModel()

    try:
        # Run batch processing
        output_dir = tmp_path / 'output'
        output_dir.mkdir()
        result = await process_videos(raw_data_file, output_dir)

        # Check batch results
        assert result.total_videos == 2
        assert result.successful_analyses == 2
        assert result.failed_analyses == 0
        assert 0 <= result.average_quality_score <= 1
        assert len(result.results) == 2

        # Check processing duration
        assert result.processing_duration > 0
        assert result.success_rate == 1.0

    finally:
        # Restore original setup function
        run_gemini_analysis.setup_gemini = original_setup
