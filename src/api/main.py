"""
🚀 TikTok Virality Prediction API

🎯 Production-ready API for TikTok virality prediction
📊 R² = 0.457 - Scientifically validated pre-publication prediction
🔬 34 advanced features automatically extracted

📚 Documentation: https://railway.app/docs
🔗 OpenAPI: /docs
"""
# Load environment variables from .env file
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
import base64
from dotenv import load_dotenv
import time
import logging
import os
import httpx # Import httpx

from .routers import analysis, inference, simulation
from .ml_model import ml_manager
from .gemini_integration import gemini_service

load_dotenv()

logger = logging.getLogger(__name__)

# --- Hugging Face Inference Configuration ---
HF_INFERENCE_ENDPOINT_URL = os.getenv("HF_INFERENCE_ENDPOINT_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Nous n'avons plus besoin de hf_inference_client ici
# hf_inference_client = None
# if HF_INFERENCE_ENDPOINT_URL and HF_API_TOKEN:
#     hf_inference_client = InferenceClient(model=HF_INFERENCE_ENDPOINT_URL, token=HF_API_TOKEN)
# --- End Hugging Face Configuration ---

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
app.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])

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

@app.get("/infer")
async def infer_on_sample_video():
    """
    Performs inference on a sample video using a remote Hugging Face Endpoint.
    The server remains non-blocking and delegates the heavy computation.
    """
    start_time = time.time()
    video_path = "static/video-test.mp4"
    prompt = "Describe this video in detail"

    if not HF_INFERENCE_ENDPOINT_URL or not HF_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Hugging Face Inference Endpoint is not configured on the server. Please set HF_INFERENCE_ENDPOINT_URL and HF_API_TOKEN environment variables."
        )

    try:
        with open(video_path, "rb") as f:
            encoded_video = base64.b64encode(f.read()).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "video", "data": encoded_video}
                ]
            }
        ]

        payload = {
            "inputs": messages,
            "parameters": {
                "max_new_tokens": 128
            }
        }

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(HF_INFERENCE_ENDPOINT_URL, json=payload, headers=headers, timeout=300.0)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
            raw_response = response.json()
        
        result_text = raw_response.get("generated_text", "No text generated.")

    except FileNotFoundError:
        logger.error(f"Video file not found at {video_path}")
        raise HTTPException(status_code=404, detail=f"Video file not found at {video_path}")
    except httpx.RequestError as e:
        logger.error(f"HTTP request error to Hugging Face Inference Endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed due to network error: {str(e)}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP status error from Hugging Face Inference Endpoint: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Inference failed with HTTP error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error(f"Hugging Face inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

    end_time = time.time()
    inference_time = end_time - start_time
    print(f"Remote inference time: {inference_time:.2f} seconds")
    return {"result": result_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
