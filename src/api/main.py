"""
🚀 TikTok Virality Prediction API

🎯 Production-ready API for TikTok virality prediction
📊 R² = 0.457 - Scientifically validated pre-publication prediction
🔬 34 advanced features automatically extracted

📚 Documentation: https://railway.app/docs
🔗 OpenAPI: /docs
"""
from .tiktok_scraper_integration import tiktok_scraper_integration
from .feature_integration import feature_manager
from .ml_model import ml_manager
from .simulation_endpoint import TikTokSimulationService, SimulationRequest, SimulationResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# FastAPI Configuration with Swagger UI
app = FastAPI(
    title="TikTok Virality Prediction API",
    description="Production API for TikTok virality prediction based on 34 advanced features",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url="/redoc"
)

# Custom Swagger UI with Dark Mode


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": 3,
            "displayRequestDuration": True,
            "docExpansion": "list",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "syntaxHighlight.theme": "monokai",
            "theme": "dark"
        }
    )

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models


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


class TikTokProfileRequest(BaseModel):
    username: str
    max_videos: int = 10
    use_cache: bool = Field(
        default=True,
        description="Use cached data if available"
    )


class TikTokAnalysis(BaseModel):
    url: str
    video_data: Dict[str, Any]
    features: Dict[str, Any]
    prediction: Dict[str, Any]
    analysis_time: float
    status: str
    cache_used: bool = False


# Import ML manager
# Simulation service
simulation_service = TikTokSimulationService(
    feature_manager, ml_manager, tiktok_scraper_integration)


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        # Load ML model
        model_loaded = ml_manager.load_model()
        feature_extractor_loaded = ml_manager.load_feature_extractor()

        if model_loaded:
            print("✅ ML model loaded successfully")
        else:
            print("⚠️ ML model not found - Using mocks")

        if feature_extractor_loaded:
            print("✅ Feature extractor loaded")
        else:
            print("⚠️ Feature extractor not found - Using mocks")

    except Exception as e:
        print(f"⚠️ Model loading error: {e}")


@app.get("/")
async def root():
    """Home page with project information"""
    return {
        "message": "TikTok Virality Prediction API",
        "version": "1.0.0",
        "status": "active",
        "r2_score": 0.457,
        "features_count": 34,
        "docs": "/docs",
        "health": "/health",
        "simulation": "/simulate-virality"
    }


@app.get("/health")
async def health_check():
    """Health check for Railway"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model_loaded": ml_manager.model is not None,
        "feature_extractor_loaded": ml_manager.feature_extractor is not None,
        "feature_system_available": feature_manager.is_available(),
        "features_count": feature_manager.get_feature_count(),
        "tiktok_scraper_available": tiktok_scraper_integration.is_available(),
        "simulation_service_available": True,
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }


@app.get("/info")
async def api_info():
    """Detailed API information"""
    return {
        "name": "TikTok Virality Prediction API",
        "description": "Production API for TikTok virality prediction",
        "scientific_basis": {
            "r2_score": 0.457,
            "features_count": 34,
            "prediction_type": "pre_publication",
            "performance_loss": "10.6% vs full features"
        },
        "endpoints": {
            "health": "/health - Health check",
            "extract_features": "/extract-features - Feature extraction",
            "predict": "/predict - Virality prediction",
            "analyze_tiktok_url": "/analyze-tiktok-url - TikTok video analysis via URL",
            "analyze_tiktok_profile": "/analyze-tiktok-profile - TikTok profile analysis",
            "simulate_virality": "/simulate-virality - Pre-publication simulation",
            "analyze": "/analyze - Complete video upload pipeline"
        },
        "documentation": {
            "openapi": "/docs",
            "redoc": "/redoc"
        }
    }


@app.post("/extract-features", response_model=FeatureExtraction)
async def extract_features(video_file: UploadFile = File(...)):
    """
    Extract 34 advanced features from a video file

    This endpoint processes uploaded video files and extracts comprehensive
    features for virality prediction including visual, audio, and metadata features.
    """
    try:
        start_time = datetime.now()

        # Extract features using the feature manager
        features = await feature_manager.extract_features_from_file(video_file)

        extraction_time = (datetime.now() - start_time).total_seconds()

        return FeatureExtraction(
            features=features,
            count=len(features),
            extraction_time=extraction_time
        )

    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Feature extraction failed: {str(e)}")


@app.post("/predict", response_model=ViralityPrediction)
async def predict_virality(features: Dict[str, object]):
    """
    Predict virality score from extracted features

    Uses the trained ML model to predict virality based on the provided features.
    Returns prediction score, confidence, and feature importance analysis.
    """
    try:
        # Get prediction from ML manager
        prediction = ml_manager.predict(features)

        return ViralityPrediction(
            virality_score=prediction.get("virality_score", 0.0),
            confidence=prediction.get("confidence", 0.0),
            r2_score=prediction.get("r2_score", 0.457),
            features_importance=prediction.get("features_importance", {}),
            recommendations=prediction.get("recommendations", [])
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/analyze-tiktok-url", response_model=TikTokAnalysis)
async def analyze_tiktok_url(request: TikTokURLRequest):
    """
    Analyze TikTok video from URL

    Fetches video data from TikTok URL, extracts features, and predicts virality.
    Supports caching to avoid repeated scraping of the same videos.
    """
    try:
        start_time = datetime.now()
        cache_used = False

        # Check cache first if enabled
        if request.use_cache:
            cached_data = await tiktok_scraper_integration.get_cached_video_data(request.url)
            if cached_data:
                video_data = cached_data
                cache_used = True
                logger.info(f"Using cached data for URL: {request.url}")
            else:
                # Fetch fresh data from TikTok
                video_data = await tiktok_scraper_integration.get_video_data_from_url(request.url)
                # Cache the new data
                await tiktok_scraper_integration.cache_video_data(request.url, video_data)
        else:
            # Always fetch fresh data
            video_data = await tiktok_scraper_integration.get_video_data_from_url(request.url)

        # Extract features from video data
        features = await feature_manager.extract_features_from_video_data(video_data)

        # Get prediction
        prediction = ml_manager.predict(features)

        analysis_time = (datetime.now() - start_time).total_seconds()

        return TikTokAnalysis(
            url=request.url,
            video_data=video_data,
            features=features,
            prediction=prediction,
            analysis_time=analysis_time,
            status="completed",
            cache_used=cache_used
        )

    except Exception as e:
        logger.error(f"TikTok URL analysis error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze-tiktok-profile")
async def analyze_tiktok_profile(request: TikTokProfileRequest):
    """
    Analyze TikTok profile and its videos

    Fetches profile data and analyzes multiple videos from a TikTok account.
    Supports caching to avoid repeated scraping.
    """
    try:
        start_time = datetime.now()
        cache_used = False

        # Check cache first if enabled
        if request.use_cache:
            cached_data = await tiktok_scraper_integration.get_cached_profile_data(request.username)
            if cached_data:
                profile_data = cached_data
                cache_used = True
                logger.info(
                    f"Using cached data for profile: {request.username}")
            else:
                # Fetch fresh data from TikTok
                profile_data = await tiktok_scraper_integration.get_profile_data(request.username, request.max_videos)
                # Cache the new data
                await tiktok_scraper_integration.cache_profile_data(request.username, profile_data)
        else:
            # Always fetch fresh data
            profile_data = await tiktok_scraper_integration.get_profile_data(request.username, request.max_videos)

        # Analyze each video
        video_analyses = []
        for video in profile_data.get("videos", []):
            try:
                features = await feature_manager.extract_features_from_video_data(video)
                prediction = ml_manager.predict(features)

                video_analyses.append({
                    "video_id": video.get("id"),
                    "url": video.get("webVideoUrl"),
                    "features": features,
                    "prediction": prediction
                })
            except Exception as e:
                logger.warning(
                    f"Failed to analyze video {video.get('id')}: {e}")
                continue

        analysis_time = (datetime.now() - start_time).total_seconds()

        return {
            "username": request.username,
            "profile_data": profile_data.get("profile_info", {}),
            "videos_analyzed": len(video_analyses),
            "video_analyses": video_analyses,
            "analysis_time": analysis_time,
            "cache_used": cache_used,
            "status": "completed"
        }

    except Exception as e:
        logger.error(f"TikTok profile analysis error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Profile analysis failed: {str(e)}")


@app.post("/analyze")
async def analyze_video(video_file: UploadFile = File(...)):
    """
    Complete video analysis pipeline

    Upload a video file for complete analysis including feature extraction
    and virality prediction. This is the main endpoint for video analysis.
    """
    try:
        start_time = datetime.now()

        # Extract features
        features = await feature_manager.extract_features_from_file(video_file)

        # Get prediction
        prediction = ml_manager.predict(features)

        analysis_time = (datetime.now() - start_time).total_seconds()

        return {
            "filename": video_file.filename,
            "features": features,
            "prediction": prediction,
            "analysis_time": analysis_time,
            "status": "completed"
        }

    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Video analysis failed: {str(e)}")


@app.post("/simulate-virality", response_model=SimulationResponse)
async def simulate_virality(request: SimulationRequest):
    """
    Simulate virality prediction with different parameters

    Allows testing different scenarios by modifying video parameters
    like publication time, hashtags, and engagement multipliers.
    """
    try:
        return await simulation_service.simulate_virality(request)
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Simulation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
