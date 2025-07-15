from datetime import datetime
import logging
from fastapi import UploadFile
from ..models import TikTokURLRequest, TikTokAnalysis, TikTokProfileRequest
from ..gemini_integration import gemini_service
from ..ml_model import ml_manager
from ..feature_integration import feature_manager
from ..tiktok_scraper_integration import tiktok_scraper_integration

logger = logging.getLogger(__name__)

async def analyze_tiktok_url_service(request: TikTokURLRequest) -> TikTokAnalysis:
    start_time = datetime.now()
    cache_used = False
    gemini_used = False

    if request.use_cache:
        cached_data = await tiktok_scraper_integration.get_cached_video_data(request.url)
        if cached_data:
            video_data = cached_data
            cache_used = True
            logger.info(f"Using cached data for URL: {request.url}")
        else:
            video_data = await tiktok_scraper_integration.get_video_data_from_url(request.url)
            await tiktok_scraper_integration.cache_video_data(request.url, video_data)
    else:
        video_data = await tiktok_scraper_integration.get_video_data_from_url(request.url)

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

    features = await feature_manager.extract_features_from_video_data(video_data, gemini_analysis)
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

async def analyze_tiktok_profile_service(request: TikTokProfileRequest):
    start_time = datetime.now()
    cache_used = False

    if request.use_cache:
        cached_data = await tiktok_scraper_integration.get_cached_profile_data(request.username)
        if cached_data:
            profile_data = cached_data
            cache_used = True
            logger.info(f"Using cached data for profile: {request.username}")
        else:
            profile_data = await tiktok_scraper_integration.get_profile_data(request.username, request.max_videos)
            await tiktok_scraper_integration.cache_profile_data(request.username, profile_data)
    else:
        profile_data = await tiktok_scraper_integration.get_profile_data(request.username, request.max_videos)

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
            logger.warning(f"Failed to analyze video {video.get('id')}: {e}")
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

async def analyze_video_service(video_file: UploadFile):
    start_time = datetime.now()
    features = await feature_manager.extract_features_from_file(video_file)
    prediction = ml_manager.predict(features)
    analysis_time = (datetime.now() - start_time).total_seconds()

    return {
        "filename": video_file.filename,
        "features": features,
        "prediction": prediction,
        "analysis_time": analysis_time,
        "status": "completed"
    }
