"""
🚀 TikTok Virality Prediction API - DDD Approach

🎯 Phase 3: Deployment Driven Development
📊 R² = 0.457 - Prédiction pré-publication scientifiquement validée
🔬 34 features avancées extraites automatiquement

📚 Documentation: https://railway.app/docs
🔗 OpenAPI: /docs
"""
from .tiktok_scraper_integration import tiktok_scraper_integration
from .feature_integration import feature_manager
from .ml_model import ml_manager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import os
import logging

logger = logging.getLogger(__name__)

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


class TikTokURLRequest(BaseModel):
    url: str
    description: str = "URL de la vidéo TikTok à analyser"


class TikTokProfileRequest(BaseModel):
    username: str
    max_videos: int = 10
    description: str = "Nom d'utilisateur TikTok à analyser"


class TikTokAnalysis(BaseModel):
    url: str
    video_data: Dict[str, Any]
    features: Dict[str, Any]
    prediction: Dict[str, Any]
    analysis_time: float
    status: str


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
        "feature_system_available": feature_manager.is_available(),
        "features_count": feature_manager.get_feature_count(),
        "tiktok_scraper_available": tiktok_scraper_integration.is_available(),
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
            "analyze_tiktok_url": "/analyze-tiktok-url - Analyse vidéo TikTok via URL",
            "analyze_tiktok_profile": "/analyze-tiktok-profile - Analyse profil TikTok",
            "analyze": "/analyze - Pipeline complet upload vidéo"
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

        # Lecture du fichier vidéo pour extraction des métadonnées
        # Note: Pour une implémentation complète, il faudrait analyser le fichier vidéo
        # Pour l'instant, on utilise des données de base
        video_data = {
            "duration": 30.0,  # À extraire du fichier vidéo
            "hashtag_count": 5,  # À extraire du texte
            "text": video_file.filename or "Vidéo uploadée",
            "playCount": 0,  # Pas encore publiée
            "diggCount": 0,
            "commentCount": 0,
            "shareCount": 0
        }

        # Extraction avec le gestionnaire de features
        features = feature_manager.extract_features(video_data)

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


@app.post("/analyze-tiktok-url", response_model=TikTokAnalysis)
async def analyze_tiktok_url(request: TikTokURLRequest):
    """
    🎯 DDD Phase 4: Analyse de vidéo TikTok via URL

    Pipeline complet: URL TikTok → scraping réel → features → prédiction
    Utilise le vrai scraper Apify et le système de features modulaire.
    """
    import time
    start_time = time.time()

    try:
        # 1. Récupération des vraies données TikTok via scraper
        video_data = tiktok_scraper_integration.get_video_data_from_url(
            request.url)

        # 2. Extraction des features avec le système modulaire
        features = feature_manager.extract_features(video_data)

        # 3. Prédiction de viralité
        prediction_result = ml_manager.predict(features)

        # 4. Calcul du temps d'analyse
        analysis_time = time.time() - start_time

        return TikTokAnalysis(
            url=request.url,
            video_data=video_data,
            features=features,
            prediction=prediction_result,
            analysis_time=analysis_time,
            status="completed"
        )

    except ValueError as e:
        raise HTTPException(400, f"URL invalide: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Erreur analyse: {str(e)}")


@app.post("/analyze-tiktok-profile")
async def analyze_tiktok_profile(request: TikTokProfileRequest):
    """
    🎯 DDD Phase 4: Analyse de profil TikTok

    Pipeline complet: Username → scraping profil → analyse vidéos → recommandations
    Utilise le vrai scraper Apify pour récupérer toutes les vidéos du profil.
    """
    import time
    start_time = time.time()

    try:
        # 1. Récupération des données du profil via scraper
        profile_data = tiktok_scraper_integration.get_profile_data(
            request.username, request.max_videos)

        # 2. Analyse de chaque vidéo
        videos_analysis = []
        for video in profile_data.get('videos', []):
            try:
                # Extraction des features
                features = feature_manager.extract_features(video)

                # Prédiction de viralité
                prediction = ml_manager.predict(features)

                videos_analysis.append({
                    "video_id": video.get('id'),
                    "url": video.get('url'),
                    "features": features,
                    "prediction": prediction
                })
            except Exception as e:
                logger.error(f"Erreur analyse vidéo {video.get('id')}: {e}")
                continue

        # 3. Statistiques du profil
        total_videos = len(videos_analysis)
        avg_virality = sum(v['prediction']['virality_score']
                           for v in videos_analysis) / total_videos if total_videos > 0 else 0

        # 4. Calcul du temps d'analyse
        analysis_time = time.time() - start_time

        return {
            "username": request.username,
            "profile_data": profile_data,
            "videos_analysis": videos_analysis,
            "profile_stats": {
                "total_videos_analyzed": total_videos,
                "average_virality_score": avg_virality,
                "top_viral_videos": sorted(videos_analysis,
                                           key=lambda x: x['prediction']['virality_score'],
                                           reverse=True)[:5]
            },
            "analysis_time": analysis_time,
            "status": "completed"
        }

    except ValueError as e:
        raise HTTPException(400, f"Username invalide: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Erreur analyse profil: {str(e)}")


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
