from fastapi import APIRouter, HTTPException, UploadFile, File
from datetime import datetime
import logging
from ..models import TikTokURLRequest, TikTokAnalysis, TikTokProfileRequest
from ..services.tiktok_service import analyze_tiktok_url_service, analyze_tiktok_profile_service, analyze_video_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze-tiktok-url", response_model=TikTokAnalysis)
async def analyze_tiktok_url(request: TikTokURLRequest):
    try:
        return await analyze_tiktok_url_service(request)
    except Exception as e:
        logger.error(f"TikTok URL analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-tiktok-profile")
async def analyze_tiktok_profile(request: TikTokProfileRequest):
    try:
        return await analyze_tiktok_profile_service(request)
    except Exception as e:
        logger.error(f"TikTok profile analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Profile analysis failed: {str(e)}")

@router.post("/analyze")
async def analyze_video(video_file: UploadFile = File(...)):
    try:
        return await analyze_video_service(video_file)
    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
