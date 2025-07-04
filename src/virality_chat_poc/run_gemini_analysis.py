"""
Run Gemini analysis on TikTok videos.
"""
import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import google.generativeai as genai
from dotenv import load_dotenv
import os

from virality_chat_poc.models.gemini_analysis import (
    GeminiAnalysis, GeminiResponse, BatchAnalysisResult,
    VisualAnalysis, ContentStructure, EngagementFactors,
    TechnicalElements, TrendAlignment, AnalysisMetrics
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gemini_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_gemini() -> genai.GenerativeModel:
    """Initialize Gemini model."""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model


def generate_analysis_prompt(video_data: Dict) -> str:
    """Generate prompt for video analysis."""
    return f"""
Analyze this TikTok video's viral potential. Consider:

Video Details:
- Duration: {video_data['duration']} seconds
- Description: {video_data['description']}
- Music: {video_data['music_info']['title']}

Provide a structured analysis covering:

1. Visual Analysis
- Text overlays and their effectiveness
- Transitions and effects
- Overall visual style and quality

2. Content Structure
- Hook effectiveness (first 3 seconds)
- Story flow and progression
- Call-to-action effectiveness

3. Engagement Factors
- Viral potential assessment
- Emotional triggers
- Audience connection elements

4. Technical Elements
- Length optimization
- Sound design quality
- Production value

5. Trend Alignment
- Current trend relevance
- Hashtag strategy potential

Format your response with clear sections and specific observations.
"""


def parse_gemini_response(response: str, video_id: str) -> GeminiResponse:
    """Parse Gemini's response into structured analysis."""
    try:
        # Extract sections from response
        sections = response.strip().split('\n\n')

        # Parse Visual Analysis
        visual = VisualAnalysis(
            text_overlays=next(s for s in sections if 'text' in s.lower()),
            transitions=next(s for s in sections if 'transition' in s.lower()),
            style_quality=next(s for s in sections if 'quality' in s.lower())
        )

        # Parse Content Structure
        content = ContentStructure(
            hook_effectiveness=next(
                s for s in sections if 'hook' in s.lower()),
            story_flow=next(
                s for s in sections if 'progression' in s.lower() or 'flow' in s.lower()),
            call_to_action=next(
                s for s in sections if 'call-to-action' in s.lower() or 'cta' in s.lower())
        )

        # Parse Engagement Factors
        engagement = EngagementFactors(
            viral_potential=next(s for s in sections if 'viral' in s.lower()),
            emotional_triggers=next(
                s for s in sections if 'joy' in s.lower() or 'emotion' in s.lower()),
            audience_connection=next(
                s for s in sections if 'audience' in s.lower() or 'engagement' in s.lower())
        )

        # Parse Technical Elements
        technical = TechnicalElements(
            length_optimization=next(
                s for s in sections if 'length' in s.lower()),
            sound_design=next(
                s for s in sections if 'sound' in s.lower() or 'audio' in s.lower()),
            production_quality=next(
                s for s in sections if 'production' in s.lower())
        )

        # Parse Trend Alignment
        trends = TrendAlignment(
            current_trends=next(s for s in sections if 'trend' in s.lower()),
            hashtag_potential=next(s for s in sections if '#' in s)
        )

        # Create analysis object
        analysis = GeminiAnalysis(
            visual_elements=visual,
            content_structure=content,
            engagement_factors=engagement,
            technical_elements=technical,
            trend_alignment=trends
        )

        # Calculate metrics
        metrics = AnalysisMetrics(
            completeness_score=0.9,  # Example scores
            consistency_score=0.85,
            specificity_score=0.8,
            actionability_score=0.75
        )

        return GeminiResponse(
            success=True,
            video_id=video_id,
            analysis=analysis,
            metrics=metrics.model_dump(),
            error=None
        )

    except Exception as e:
        logger.error(
            f"Error parsing Gemini response for video {video_id}: {str(e)}")
        return GeminiResponse(
            success=False,
            video_id=video_id,
            analysis=None,
            metrics=None,
            error=str(e)
        )


async def analyze_video(
    model: genai.GenerativeModel,
    video_data: Dict,
    output_dir: Path
) -> GeminiResponse:
    """Analyze a single video."""
    try:
        # Generate and get response
        prompt = generate_analysis_prompt(video_data)
        response = await model.generate_content(prompt)

        # Parse response
        result = parse_gemini_response(response.text, video_data['id'])

        # Save result
        output_file = output_dir / f"video_{video_data['id']}_analysis.json"
        with output_file.open('w') as f:
            json.dump(result.model_dump(), f, indent=2)

        return result

    except Exception as e:
        logger.error(f"Error analyzing video {video_data['id']}: {str(e)}")
        return GeminiResponse(
            success=False,
            video_id=video_data['id'],
            analysis=None,
            metrics=None,
            error=str(e)
        )


async def process_videos(
    raw_data_file: Path,
    output_dir: Path
) -> BatchAnalysisResult:
    """Process multiple videos."""
    start_time = datetime.now()

    try:
        # Load raw data
        with raw_data_file.open('r') as f:
            raw_data = json.load(f)

        # Setup model
        model = setup_gemini()

        # Process each video
        results = []
        for video in raw_data['videos']:
            result = await analyze_video(model, video, output_dir)
            results.append(result)

        # Calculate batch metrics
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        # Calculate average quality score
        quality_scores = []
        for result in successful:
            if result.metrics:
                metrics = result.metrics
                avg_score = sum(metrics.values()) / len(metrics)
                quality_scores.append(avg_score)

        avg_quality = sum(quality_scores) / \
            len(quality_scores) if quality_scores else 0

        return BatchAnalysisResult(
            success=True,
            total_videos=len(results),
            successful_analyses=len(successful),
            failed_analyses=len(failed),
            average_quality_score=avg_quality,
            processing_duration=(datetime.now() - start_time).total_seconds(),
            success_rate=len(successful) / len(results) if results else 0,
            results=results,
            error=None
        )

    except Exception as e:
        logger.error(f"Error processing videos: {str(e)}")
        return BatchAnalysisResult(
            success=False,
            total_videos=0,
            successful_analyses=0,
            failed_analyses=0,
            average_quality_score=0,
            processing_duration=(datetime.now() - start_time).total_seconds(),
            success_rate=0,
            results=[],
            error=str(e)
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process TikTok videos with Gemini analysis')
    parser.add_argument('input_file', type=str,
                        help='Path to raw data JSON file')
    parser.add_argument('output_dir', type=str,
                        help='Directory for analysis output')
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    import asyncio
    result = asyncio.run(process_videos(input_path, output_path))

    if result.success:
        logger.info(
            f"Successfully processed {result.successful_analyses} videos")
        logger.info(
            f"Average quality score: {result.average_quality_score:.2f}")
    else:
        logger.error(f"Batch processing failed: {result.error}")
