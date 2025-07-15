"""
🚀 TikTok Virality Prediction API

🎯 Production-ready API for TikTok virality prediction
📊 R² = 0.457 - Scientifically validated pre-publication prediction
🔬 34 advanced features automatically extracted

📚 Documentation: https://railway.app/docs
🔗 OpenAPI: /docs
"""
# Load environment variables from .env file
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from dotenv import load_dotenv
import logging
import os

from .routers import analysis, inference, simulation, video_inference
from .ml_model import ml_manager
from .gemini_integration import gemini_service

load_dotenv()

logger = logging.getLogger(__name__)

# --- Hugging Face Inference Configuration ---
HF_INFERENCE_ENDPOINT_URL = os.getenv("HF_INFERENCE_ENDPOINT_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# --- API Authentication Configuration ---
# Moved to src/api/dependencies.py
# --- End API Authentication Configuration ---

app = FastAPI(
    title="TikTok Virality Prediction API",
    description="Production API for TikTok virality prediction based on 34 advanced features with Gemini AI analysis",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url="/redoc"
)


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])
app.include_router(simulation.router, prefix="/simulation",
                   tags=["Simulation"])
app.include_router(video_inference.router, prefix="/video",
                   tags=["Video Inference"])


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
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
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check for Railway"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model_loaded": ml_manager.model is not None,
        "feature_extractor_loaded": ml_manager.feature_extractor is not None,
        "gemini_available": gemini_service.is_available(),
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
