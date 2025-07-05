"""
🚀 TikTok Virality Prediction API - DDD Approach

🎯 Phase 3: Deployment Driven Development
📊 R² = 0.457 - Prédiction pré-publication scientifiquement validée
🔬 34 features avancées extraites automatiquement

📚 Documentation: https://railway.app/docs
🔗 OpenAPI: /docs
"""
from .ml_model import ml_manager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os

# Configuration FastAPI
app = FastAPI(
    title="TikTok Virality Prediction API",
    description="API de prédiction de viralité TikTok basée sur 34 features avancées",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS pour développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic


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


# Import du gestionnaire ML


@app.on_event("startup")
async def startup_event():
    """Chargement du modèle au démarrage"""
    try:
        # Chargement du modèle ML
        model_loaded = ml_manager.load_model()
        feature_extractor_loaded = ml_manager.load_feature_extractor()

        if model_loaded:
            print("✅ Modèle ML chargé avec succès")
        else:
            print("⚠️ Modèle ML non trouvé - Utilisation des mocks")

        if feature_extractor_loaded:
            print("✅ Extracteur de features chargé")
        else:
            print("⚠️ Extracteur non trouvé - Utilisation des mocks")

    except Exception as e:
        print(f"⚠️ Erreur chargement modèle: {e}")


@app.get("/")
async def root():
    """Page d'accueil avec informations du projet"""
    return {
        "message": "TikTok Virality Prediction API",
        "version": "1.0.0",
        "status": "active",
        "r2_score": 0.457,
        "features_count": 34,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check pour Railway"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model_loaded": ml_manager.model is not None,
        "feature_extractor_loaded": ml_manager.feature_extractor is not None,
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }


@app.get("/info")
async def api_info():
    """Informations détaillées sur l'API"""
    return {
        "name": "TikTok Virality Prediction API",
        "description": "API de prédiction de viralité TikTok",
        "scientific_basis": {
            "r2_score": 0.457,
            "features_count": 34,
            "prediction_type": "pre_publication",
            "performance_loss": "10.6% vs full features"
        },
        "endpoints": {
            "health": "/health - Health check",
            "extract_features": "/extract-features - Extraction des features",
            "predict": "/predict - Prédiction de viralité",
            "analyze": "/analyze - Pipeline complet"
        },
        "documentation": {
            "openapi": "/docs",
            "redoc": "/redoc"
        }
    }


@app.post("/extract-features", response_model=FeatureExtraction)
async def extract_features(video_file: UploadFile = File(...)):
    """
    🎯 Étape 2 DDD: Extraction des 34 features d'une vidéo

    Extrait automatiquement les features pré-publication nécessaires
    pour la prédiction de viralité.
    """
    try:
        # Validation du fichier
        if video_file.filename and not video_file.filename.endswith(('.mp4', '.mov', '.avi')):
            raise HTTPException(400, "Format vidéo non supporté")

        # TODO: Implémenter extraction features
        # features = feature_extractor.extract(video_file)

        # Mock pour test DDD
        features = {
            "video_duration": 30.0,
            "hashtag_count": 5,
            "human_presence": True,
            "eye_contact": True,
            "color_vibrancy": 0.75,
            "music_energy": 0.8,
            "audience_connection_score": 0.85
        }

        return FeatureExtraction(
            features=features,
            count=len(features),
            extraction_time=1.5
        )

    except Exception as e:
        raise HTTPException(500, f"Erreur extraction features: {str(e)}")


@app.post("/predict", response_model=ViralityPrediction)
async def predict_virality(features: Dict[str, object]):
    """
    🎯 Étape 3 DDD: Prédiction de viralité

    Prédit la viralité d'une vidéo basée sur les features extraites.
    R² = 0.457 avec seulement 10.6% de perte vs features complètes.
    """
    try:
        # Utilisation du gestionnaire ML
        prediction_result = ml_manager.predict(features)
        
        return ViralityPrediction(**prediction_result)

    except Exception as e:
        raise HTTPException(500, f"Erreur prédiction: {str(e)}")


@app.post("/analyze")
async def analyze_video(video_file: UploadFile = File(...)):
    """
    🎯 Étape 4 DDD: Pipeline complet vidéo → prédiction

    Pipeline complet: upload vidéo → extraction features → prédiction → recommandations
    """
    try:
        # 1. Extraction des features
        features_response = await extract_features(video_file)
        features = features_response.features

        # 2. Prédiction de viralité
        prediction_response = await predict_virality(features)

        # 3. Résultats complets
        return {
            "video_info": {
                "filename": video_file.filename,
                "size": video_file.size,
                "content_type": video_file.content_type
            },
            "features": features,
            "prediction": prediction_response,
            "pipeline_time": features_response.extraction_time + 0.5
        }

    except Exception as e:
        raise HTTPException(500, f"Erreur pipeline: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
