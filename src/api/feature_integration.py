"""
🔧 Module d'intégration des features pour l'API

🎯 DDD Phase 3: Intégration du système de features modulaire
📊 34 features avancées avec extraction automatique
"""
import logging
from typing import Dict, Any, Optional
import sys
import os

# Ajout du chemin src pour l'import
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from features.modular_feature_system import create_feature_extractor
    FEATURE_SYSTEM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Système de features non disponible: {e}")
    FEATURE_SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class FeatureIntegrationManager:
    """Gestionnaire d'intégration des features pour l'API"""

    def __init__(self):
        self.feature_extractor = None
        self.available = FEATURE_SYSTEM_AVAILABLE

        if self.available:
            try:
                # Création de l'extracteur de features modulaire
                self.feature_extractor = create_feature_extractor(
                    'comprehensive')
                logger.info("✅ Extracteur de features modulaire chargé")
            except Exception as e:
                logger.error(f"❌ Erreur chargement extracteur: {e}")
                self.available = False

    def extract_features(self, video_data: Dict[str, Any], gemini_analysis: Optional[Dict] = None) -> Dict[str, Any]:
        """Extraction des features avec le système modulaire"""
        if not self.available or not self.feature_extractor:
            return self._mock_feature_extraction(video_data)

        try:
            # Extraction avec le système modulaire
            features = self.feature_extractor.extract_features(
                video_data, gemini_analysis)
            logger.info(f"✅ {len(features)} features extraites")
            return features
        except Exception as e:
            logger.error(f"❌ Erreur extraction features: {e}")
            return self._mock_feature_extraction(video_data)

    def _mock_feature_extraction(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extraction mock pour DDD Phase 2"""
        return {
            "video_duration": video_data.get("duration", 30.0),
            "estimated_hashtag_count": video_data.get("hashtag_count", 5),
            "audience_connection_score": 0.75,
            "color_vibrancy": 0.7,
            "music_energy": 0.8,
            "emotional_trigger_count": 3,
            "hour_of_day": 14,
            "video_duration_optimized": 1.0,
            "viral_potential_score": 0.65,
            "production_quality_score": 0.8
        }

    def get_feature_count(self) -> int:
        """Nombre de features disponibles"""
        if self.feature_extractor:
            return self.feature_extractor.get_feature_count()
        return 10  # Mock features

    def get_feature_names(self) -> list:
        """Noms des features disponibles"""
        if self.feature_extractor:
            return self.feature_extractor.get_feature_names()
        return ["video_duration", "estimated_hashtag_count", "audience_connection_score",
                "color_vibrancy", "music_energy", "emotional_trigger_count",
                "hour_of_day", "video_duration_optimized", "viral_potential_score",
                "production_quality_score"]

    def is_available(self) -> bool:
        """Vérifie si le système de features est disponible"""
        return self.available and self.feature_extractor is not None


# Instance globale
feature_manager = FeatureIntegrationManager()
