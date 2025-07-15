from datetime import datetime
import logging
from fastapi import UploadFile
from ..models import FeatureExtraction, ViralityPrediction
from ..feature_integration import feature_manager
from ..ml_model import ml_manager

logger = logging.getLogger(__name__)

async def extract_features_service(video_file: UploadFile) -> FeatureExtraction:
    start_time = datetime.now()
    features = await feature_manager.extract_features_from_file(video_file)
    extraction_time = (datetime.now() - start_time).total_seconds()
    return FeatureExtraction(
        features=features,
        count=len(features),
        extraction_time=extraction_time
    )

def predict_virality_service(features: dict) -> ViralityPrediction:
    prediction = ml_manager.predict(features)
    return ViralityPrediction(
        virality_score=prediction.get("virality_score", 0.0),
        confidence=prediction.get("confidence", 0.0),
        r2_score=prediction.get("r2_score", 0.457),
        features_importance=prediction.get("features_importance", {}),
        recommendations=prediction.get("recommendations", [])
    )
