from pydantic import BaseModel, Field
from typing import Dict, List, Any

class ViralityPrediction(BaseModel):
    virality_score: float
    confidence: float
    r2_score: float = 0.457
    features_importance: Dict[str, float]
    recommendations: List[str]


class FeatureExtraction(BaseModel):
    features: Dict[str, object]
    count: int
    extraction_time: float


class TikTokURLRequest(BaseModel):
    url: str = Field(
        default="https://www.tiktok.com/@swarecito/video/7505706702050823446",
        description="TikTok video URL to analyze"
    )
    use_cache: bool = Field(
        default=True,
        description="Use cached data if available (recommended for testing)"
    )
    use_gemini: bool = Field(
        default=True,
        description="Use Gemini AI for advanced video analysis"
    )


class TikTokProfileRequest(BaseModel):
    username: str
    max_videos: int = 10
    use_cache: bool = Field(
        default=True,
        description="Use cached data if available"
    )
    use_gemini: bool = Field(
        default=True,
        description="Use Gemini AI for advanced video analysis"
    )


class TikTokAnalysis(BaseModel):
    url: str
    video_data: Dict[str, Any]
    features: Dict[str, Any]
    prediction: Dict[str, Any]
    analysis_time: float
    status: str
    cache_used: bool = False
    gemini_used: bool = False

class VideoInferenceResponse(BaseModel):
    result: str
    inference_time: float
