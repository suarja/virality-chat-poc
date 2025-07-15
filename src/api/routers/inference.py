from fastapi import APIRouter, HTTPException, UploadFile, File
from datetime import datetime
import logging
from ..models import FeatureExtraction, ViralityPrediction
from ..services.inference_service import extract_features_service, predict_virality_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/extract-features", response_model=FeatureExtraction)
async def extract_features(video_file: UploadFile = File(...)):
    try:
        return await extract_features_service(video_file)
    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        raise HTTPException(status_code=500, detail=f"Feature extraction failed: {str(e)}")

@router.post("/predict", response_model=ViralityPrediction)
async def predict_virality(features: dict):
    try:
        return predict_virality_service(features)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
