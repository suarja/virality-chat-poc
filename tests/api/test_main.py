"""
🧪 Tests pour l'API TikTok Virality - DDD Approach

🎯 Tests des endpoints pour validation DDD
📊 R² = 0.457 - Prédiction pré-publication scientifiquement validée
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root():
    """Test endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "TikTok Virality Prediction API"
    assert data["r2_score"] == 0.457
    assert data["features_count"] == 34


def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "model_loaded" in data


def test_info():
    """Test endpoint info"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TikTok Virality Prediction API"
    assert data["scientific_basis"]["r2_score"] == 0.457
    assert data["scientific_basis"]["features_count"] == 34


def test_predict_mock():
    """Test prédiction avec données mock"""
    features = {
        "video_duration": 30.0,
        "hashtag_count": 5,
        "human_presence": True,
        "eye_contact": True,
        "color_vibrancy": 0.75,
        "music_energy": 0.8,
        "audience_connection_score": 0.85
    }

    response = client.post("/predict", json=features)
    assert response.status_code == 200
    data = response.json()
    assert "virality_score" in data
    assert "confidence" in data
    assert data["r2_score"] == 0.457
    assert "features_importance" in data
    assert "recommendations" in data


def test_docs_accessible():
    """Test accessibilité documentation OpenAPI"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_accessible():
    """Test accessibilité ReDoc"""
    response = client.get("/redoc")
    assert response.status_code == 200
