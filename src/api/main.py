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
from .gemini_integration import gemini_service
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
    description="Production API for TikTok virality prediction based on 34 advanced features with Gemini AI analysis",
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

        # Check Gemini availability
        if gemini_service.is_available():
            print("✅ Gemini AI integration available")
        else:
            print("⚠️ Gemini AI not available - Using mocks")

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
        "gemini_available": gemini_service.is_available(),
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
        "gemini_available": gemini_service.is_available(),
        "simulation_service_available": True,
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }


@app.get("/info")
async def api_info():
    """Detailed API information"""
    return {
        "name": "TikTok Virality Prediction API",
        "description": "Production API for TikTok virality prediction with Gemini AI",
        "scientific_basis": {
            "r2_score": 0.457,
            "features_count": 34,
            "prediction_type": "pre_publication",
            "performance_loss": "10.6% vs full features"
        },
        "ai_components": {
            "gemini_ai": gemini_service.is_available(),
            "ml_model": ml_manager.model is not None,
            "feature_extraction": feature_manager.is_available()
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
    📊 Analyze existing TikTok video using real engagement data and Gemini AI

    **Use Case**: "How viral is this existing video and why?"

    This endpoint analyzes an already published TikTok video using:
    - ✅ Real engagement metrics (views, likes, comments, shares)
    - ✅ Gemini AI for advanced video content analysis
    - ✅ 34 advanced features automatically extracted
    - ✅ ML model trained on pre-publication features (R² = 0.457)

    **What you get**:
    - ✅ Current virality score (0-1 scale)
    - ✅ Real engagement data (views, likes, comments, shares)
    - ✅ Gemini AI content analysis (visual quality, hooks, story elements)
    - ✅ Feature importance analysis
    - ✅ Specific recommendations for improvement
    - ✅ Caching support to avoid repeated scraping

    **Example Request**:
    ```json
    {
      "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
      "use_cache": true,
      "use_gemini": true
    }
    ```

    **Example Response**:
    ```json
    {
      "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
      "video_data": {
        "playCount": 53000,
        "diggCount": 1916,
        "commentCount": 631,
        "shareCount": 302,
        "hashtags": ["chatgpt", "agent", "prompt"]
      },
      "features": {
        "audience_connection_score": 0.75,
        "visual_quality_score": 0.8,
        "has_hook": true,
        "emotional_trigger_count": 3
      },
      "prediction": {
        "virality_score": 0.75,
        "confidence": 0.85,
        "recommendations": [
          "Optimize publication timing (6-8am, 12-2pm, 6-8pm hours)",
          "Reduce hashtag count (less is better)"
        ]
      },
      "cache_used": true,
      "gemini_used": true,
      "status": "completed"
    }
    ```

    **Virality Score Interpretation**:
    - **0.0-0.3**: Low viral potential
    - **0.3-0.6**: Moderate viral potential  
    - **0.6-0.8**: High viral potential
    - **0.8-1.0**: Very high viral potential
    """
    try:
        start_time = datetime.now()
        cache_used = False
        gemini_used = False

        # 1. Get video data from TikTok (with caching)
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

        # 2. Run Gemini AI analysis (if enabled)
        gemini_analysis = None
        if request.use_gemini and gemini_service.is_available():
            try:
                gemini_result = await gemini_service.analyze_video(request.url, use_cache=request.use_cache)
                if gemini_result and gemini_result.get("success"):
                    gemini_analysis = gemini_result.get("analysis")
                    gemini_used = True
                    logger.info(f"Gemini analysis completed for {request.url}")
                else:
                    logger.warning(f"Gemini analysis failed for {request.url}")
            except Exception as e:
                logger.warning(f"Gemini analysis error: {e}")

        # 3. Extract features with Gemini analysis
        features = await feature_manager.extract_features_from_video_data(video_data, gemini_analysis)

        # 4. Get prediction from ML model
        prediction = ml_manager.predict(features)

        analysis_time = (datetime.now() - start_time).total_seconds()

        return TikTokAnalysis(
            url=request.url,
            video_data=video_data,
            features=features,
            prediction=prediction,
            analysis_time=analysis_time,
            status="completed",
            cache_used=cache_used,
            gemini_used=gemini_used
        )

    except Exception as e:
        logger.error(f"TikTok URL analysis error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze-tiktok-profile")
async def analyze_tiktok_profile(request: TikTokProfileRequest):
    """
    📊 Analyze multiple videos from a TikTok profile

    **Use Case**: "What makes this creator's videos viral?"

    This endpoint analyzes multiple videos from a TikTok account to understand
    patterns in viral content and provide insights on what makes this creator successful.

    **What you get**:
    - ✅ Analysis of multiple videos (up to max_videos)
    - ✅ Profile-level insights and patterns
    - ✅ Best performing videos identification
    - ✅ Content strategy recommendations
    - ✅ Caching support for efficiency

    **Example Request**:
    ```json
    {
      "username": "swarecito",
      "max_videos": 10,
      "use_cache": true
    }
    ```

    **Example Response**:
    ```json
    {
      "username": "swarecito",
      "profile_data": {
        "fans": 2001,
        "following": 54,
        "video": 55
      },
      "videos_analyzed": 10,
      "video_analyses": [
        {
          "video_id": "7505706702050823446",
          "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
          "prediction": {
            "virality_score": 0.75,
            "recommendations": ["Optimize timing", "Reduce hashtags"]
          }
        }
      ],
      "analysis_time": 45.2,
      "cache_used": true,
      "status": "completed"
    }
    ```
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
    🎯 Simulate different publication scenarios for virality prediction

    **Use Case**: "When should I publish this video for maximum virality?"

    This endpoint simulates different publication scenarios (timing, hashtags, content features)
    to predict which approach would maximize viral potential. Perfect for planning your next video!

    **⚠️ Important**: This is a PRE-PUBLICATION simulation that does NOT use real engagement data.
    The video URL is only used for content analysis (duration, format, etc.), not for views/likes/comments.

    **What you get**:
    - ✅ Best publication time recommendations
    - ✅ Optimal hashtag combinations
    - ✅ Expected virality improvement
    - ✅ Content optimization suggestions
    - ✅ Multiple scenario comparisons
    - ✅ Caching support for efficiency

    **Example Request**:
    ```json
    {
      "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
      "use_cache": true,
      "scenarios": [
        {
          "name": "Morning Publication",
          "description": "Publish at 9am on Monday",
          "publication_hour": 9,
          "publication_day": "monday",
          "hashtags": ["fyp", "viral", "trending"],
          "engagement_multiplier": 1.2
        },
        {
          "name": "Evening Publication",
          "description": "Publish at 8pm on Friday", 
          "publication_hour": 20,
          "publication_day": "friday",
          "hashtags": ["fyp", "comedy", "funny"],
          "engagement_multiplier": 1.5
        }
      ],
      "simulation_count": 5
    }
    ```

    **Example Response**:
    ```json
    {
      "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
      "base_virality_score": 0.65,
      "scenarios": [
        {
          "scenario_name": "Morning Publication",
          "average_virality_score": 0.72,
          "best_virality_score": 0.79,
          "recommendations": [
            "Publish at optimal hours: 9, 12, 18, 21h",
            "Add trending hashtags for better reach"
          ]
        },
        {
          "scenario_name": "Evening Publication",
          "average_virality_score": 0.81,
          "best_virality_score": 0.85,
          "recommendations": [
            "Friday evening is optimal for this content type",
            "Consider adding call-to-action for engagement"
          ]
        }
      ],
      "best_scenario": "Evening Publication",
      "best_score": 0.81,
      "summary": {
        "cache_used": true,
        "simulation_type": "pre_publication",
        "improvement_potential": 0.16
      }
    }
    ```

    **Key Differences from Analysis**:
    - 🔄 **Analysis**: Uses real post-publication data (views, likes, comments)
    - 🎯 **Simulation**: Predicts pre-publication scenarios (no engagement data)
    - 📊 **Analysis**: "Why did this video go viral?"
    - 🚀 **Simulation**: "When should I publish for maximum virality?"

    **Pre-Publication Features Used**:
    - ✅ Video duration and format
    - ✅ Publication timing (hour, day)
    - ✅ Hashtag strategy
    - ✅ Content features (overlays, transitions, CTA)
    - ✅ Engagement multipliers (simulated)

    **No Post-Publication Data Used**:
    - ❌ Real view counts
    - ❌ Real like counts
    - ❌ Real comment counts
    - ❌ Real share counts
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
