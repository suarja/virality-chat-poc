"""
TikTok video virality analysis using Gemini.
"""

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

__version__ = "0.1.0"

__all__ = [
    'GeminiAnalysis',
    'GeminiResponse',
    'BatchAnalysisResult',
    'VisualAnalysis',
    'ContentStructure',
    'EngagementFactors',
    'TechnicalElements',
    'TrendAlignment',
    'AnalysisMetrics',
    'generate_analysis_prompt',
    'parse_gemini_response',
    'analyze_video',
    'process_videos'
]
