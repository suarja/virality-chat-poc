#!/usr/bin/env python3
"""
Prototype de l'architecture modulaire pour les features
Permet de "jongler" avec différents jeux de features de manière flexible
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FeatureCategory(Enum):
    """Catégories de features."""
    METADATA = "metadata"
    VISUAL = "visual"
    AUDIO = "audio"
    TEMPORAL = "temporal"
    PSYCHOLOGICAL = "psychological"
    CULTURAL = "cultural"
    CREATIVITY = "creativity"
    PERFORMANCE = "performance"


@dataclass
class FeatureDefinition:
    """Définition d'une feature avec métadonnées."""
    name: str
    category: FeatureCategory
    data_type: str
    description: str
    extraction_method: str
    complexity: str  # 'easy', 'moderate', 'complex'
    research_based: bool
    actionable: bool


class BaseFeatureSet(ABC):
    """Classe de base pour tous les feature sets."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.features = []

    @abstractmethod
    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features selon ce feature set."""
        pass

    def get_feature_names(self) -> List[str]:
        """Retourne la liste des noms de features de ce set."""
        return self.features

    def get_feature_count(self) -> int:
        """Retourne le nombre de features dans ce set."""
        return len(self.features)


class MetadataFeatureSet(BaseFeatureSet):
    """Feature set pour les métadonnées TikTok (features existantes)."""

    def __init__(self):
        super().__init__(
            name="metadata",
            description="Features métadonnées TikTok (durée, engagement, hashtags, etc.)"
        )
        self.features = [
            'video_id', 'title', 'description', 'duration',
            'view_count', 'like_count', 'comment_count', 'share_count',
            'like_rate', 'comment_rate', 'share_rate', 'engagement_rate',
            'hashtags', 'hashtag_count', 'music_info',
            'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'is_business_hours'
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features métadonnées (logique existante du Data Processor)."""
        features = {}

        # Métriques de base
        features['video_id'] = video_data.get('id', '')
        features['title'] = video_data.get('text', '')
        features['description'] = video_data.get('text', '')
        features['duration'] = video_data.get(
            'videoMeta', {}).get('duration', 0)

        # Métriques d'engagement
        features['view_count'] = video_data.get('playCount', 0)
        features['like_count'] = video_data.get('diggCount', 0)
        features['comment_count'] = video_data.get('commentCount', 0)
        features['share_count'] = video_data.get('shareCount', 0)

        # Calcul des ratios d'engagement
        if features['view_count'] > 0:
            features['like_rate'] = features['like_count'] / \
                features['view_count']
            features['comment_rate'] = features['comment_count'] / \
                features['view_count']
            features['share_rate'] = features['share_count'] / \
                features['view_count']
            features['engagement_rate'] = (
                features['like_count'] + features['comment_count'] + features['share_count']) / features['view_count']
        else:
            features['like_rate'] = 0
            features['comment_rate'] = 0
            features['share_rate'] = 0
            features['engagement_rate'] = 0

        # Hashtags
        hashtags = [tag['name'] for tag in video_data.get('hashtags', [])]
        features['hashtags'] = ','.join(hashtags)
        features['hashtag_count'] = len(hashtags)

        # Musique
        music_meta = video_data.get('musicMeta', {})
        features['music_info'] = f"{music_meta.get('musicAuthor', '')} - {music_meta.get('musicName', '')}"

        # Features temporelles
        post_time = video_data.get('createTimeISO', '')
        if post_time:
            import pandas as pd
            post_time = pd.to_datetime(post_time)
            features['hour_of_day'] = post_time.hour
            features['day_of_week'] = post_time.dayofweek
            features['month'] = post_time.month
            features['is_weekend'] = post_time.dayofweek >= 5
            features['is_business_hours'] = 9 <= post_time.hour <= 17

        return features


class GeminiBasicFeatureSet(BaseFeatureSet):
    """Feature set pour les features Gemini de base (features existantes)."""

    def __init__(self):
        super().__init__(
            name="gemini_basic",
            description="Features d'analyse Gemini de base (visuelles, structure, engagement)"
        )
        self.features = [
            'has_text_overlays', 'has_transitions', 'visual_quality_score',
            'has_hook', 'has_story', 'has_call_to_action',
            'viral_potential_score', 'emotional_trigger_count', 'audience_connection_score',
            'length_optimized', 'sound_quality_score', 'production_quality_score',
            'trend_alignment_score', 'estimated_hashtag_count'
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features Gemini de base (logique existante du Data Processor)."""
        features = {}

        if not gemini_analysis:
            logger.warning(
                "No Gemini analysis provided for gemini_basic feature set")
            return features

        try:
            # Visual Analysis Features
            visual = gemini_analysis.get('visual_analysis', {})
            features['has_text_overlays'] = 'text overlays' in visual.get(
                'text_overlays', '').lower()
            features['has_transitions'] = 'transitions' in visual.get(
                'transitions', '').lower()
            features['visual_quality_score'] = 1.0 if 'high quality' in visual.get(
                'style_quality', '').lower() else 0.5

            # Content Structure Features
            content = gemini_analysis.get('content_structure', {})
            features['has_hook'] = 1.0 if 'effective' in content.get(
                'hook_effectiveness', '').lower() else 0.5
            features['has_story'] = 'story' in content.get(
                'story_flow', '').lower()
            features['has_call_to_action'] = 'call to action' in content.get(
                'call_to_action', '').lower()

            # Engagement Features
            engagement = gemini_analysis.get('engagement_factors', {})
            features['viral_potential_score'] = 1.0 if 'high' in engagement.get(
                'viral_potential', '').lower() else 0.5
            features['emotional_trigger_count'] = len(
                engagement.get('emotional_triggers', '').split(','))
            features['audience_connection_score'] = 1.0 if 'strong' in engagement.get(
                'audience_connection', '').lower() else 0.5

            # Technical Features
            technical = gemini_analysis.get('technical_elements', {})
            features['length_optimized'] = 'appropriate' in technical.get(
                'length_optimization', '').lower()
            features['sound_quality_score'] = 1.0 if 'high quality' in technical.get(
                'sound_design', '').lower() else 0.5
            features['production_quality_score'] = 1.0 if 'high' in technical.get(
                'production_quality', '').lower() else 0.5

            # Trend Features
            trends = gemini_analysis.get('trend_alignment', {})
            features['trend_alignment_score'] = 1.0 if 'perfectly' in trends.get(
                'current_trends', '').lower() else 0.5
            features['estimated_hashtag_count'] = len(
                trends.get('hashtag_potential', '').split('#')) - 1

        except Exception as e:
            logger.error(f"Error extracting Gemini basic features: {e}")

        return features


class VisualGranularFeatureSet(BaseFeatureSet):
    """Feature set pour les features visuelles granulaires (nouvelles)."""

    def __init__(self):
        super().__init__(
            name="visual_granular",
            description="Features visuelles granulaires et actionnables"
        )
        self.features = [
            'human_count', 'eye_contact_with_camera', 'shot_type', 'color_vibrancy_score',
            'rule_of_thirds_score', 'depth_of_field_type', 'color_palette_type',
            'movement_intensity_score', 'composition_balance', 'lighting_quality'
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features visuelles granulaires."""
        features = {}

        if not gemini_analysis:
            logger.warning(
                "No Gemini analysis provided for visual_granular feature set")
            return features

        try:
            visual_analysis = gemini_analysis.get('visual_analysis', {})

            # Analyse de présence humaine
            human_text = visual_analysis.get('human_presence', '')
            if 'multiple people' in human_text.lower():
                features['human_count'] = 3
            elif 'two people' in human_text.lower():
                features['human_count'] = 2
            elif 'person' in human_text.lower() or 'human' in human_text.lower():
                features['human_count'] = 1
            else:
                features['human_count'] = 0

            # Contact visuel
            features['eye_contact_with_camera'] = 'eye contact' in human_text.lower()

            # Type de plan
            shot_text = visual_analysis.get('shot_type', '')
            if 'close-up' in shot_text.lower():
                features['shot_type'] = 'close_up'
            elif 'medium' in shot_text.lower():
                features['shot_type'] = 'medium'
            elif 'wide' in shot_text.lower():
                features['shot_type'] = 'wide'
            else:
                features['shot_type'] = 'unknown'

            # Score de saturation des couleurs
            color_text = visual_analysis.get('color_analysis', '')
            if 'vibrant' in color_text.lower() or 'saturated' in color_text.lower():
                features['color_vibrancy_score'] = 0.8
            elif 'bright' in color_text.lower():
                features['color_vibrancy_score'] = 0.6
            elif 'muted' in color_text.lower() or 'dull' in color_text.lower():
                features['color_vibrancy_score'] = 0.3
            else:
                features['color_vibrancy_score'] = 0.5

            # Placeholders pour les nouvelles features
            features['rule_of_thirds_score'] = 0.7  # À implémenter
            features['depth_of_field_type'] = 'medium'  # À implémenter
            features['color_palette_type'] = 'complementary'  # À implémenter
            features['movement_intensity_score'] = 0.6  # À implémenter
            features['composition_balance'] = 0.7  # À implémenter
            features['lighting_quality'] = 0.8  # À implémenter

        except Exception as e:
            logger.error(f"Error extracting visual granular features: {e}")

        return features


class ComprehensiveFeatureSet(BaseFeatureSet):
    """Feature set complet avec toutes les 34 features (Phase 1+2+3)."""

    def __init__(self):
        super().__init__(
            name="comprehensive",
            description="Feature set complet avec toutes les 34 features déterminantes"
        )
        self.features = [
            # Phase 1: Foundation
            'video_duration_optimized', 'hashtag_effectiveness_score', 'music_trend_alignment',
            'publish_timing_score', 'human_count', 'eye_contact_with_camera', 'shot_type',
            'color_vibrancy_score', 'seasonal_timing_score', 'trending_moment_alignment', 'competition_level',

            # Phase 2: Advanced
            'music_energy', 'audio_visual_sync_score', 'voice_emotion', 'rule_of_thirds_score',
            'depth_of_field_type', 'color_palette_type', 'attention_grab_strength', 'emotional_hook_strength',
            'relatability_score', 'originality_score', 'creative_technique_count', 'story_structure_type',

            # Phase 3: Innovation
            'cultural_relevance_score', 'generational_appeal', 'social_issue_relevance', 'shareability_score',
            'meme_potential', 'challenge_potential', 'completion_rate_prediction', 'virality_velocity', 'user_experience_score'
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait toutes les 34 features complètes."""
        features = {}

        # Utiliser les feature sets existants
        metadata_set = MetadataFeatureSet()
        gemini_set = GeminiBasicFeatureSet()
        visual_set = VisualGranularFeatureSet()

        # Combiner toutes les features
        features.update(metadata_set.extract(video_data, gemini_analysis))
        features.update(gemini_set.extract(video_data, gemini_analysis))
        features.update(visual_set.extract(video_data, gemini_analysis))

        # Ajouter les features avancées (placeholders)
        features.update(self._extract_advanced_features(
            video_data, gemini_analysis))

        return features

    def _extract_advanced_features(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features avancées (Phase 2+3)."""
        features = {}

        # Phase 2: Advanced features (placeholders)
        features['music_energy'] = 0.6
        features['audio_visual_sync_score'] = 0.7
        features['voice_emotion'] = 'neutral'
        features['attention_grab_strength'] = 0.6
        features['emotional_hook_strength'] = 0.7
        features['relatability_score'] = 0.5
        features['originality_score'] = 0.6
        features['creative_technique_count'] = 2
        features['story_structure_type'] = 'linear'

        # Phase 3: Innovation features (placeholders)
        features['cultural_relevance_score'] = 0.5
        features['generational_appeal'] = 'Gen Z'
        features['social_issue_relevance'] = 0.3
        features['shareability_score'] = 0.6
        features['meme_potential'] = 0.4
        features['challenge_potential'] = 0.5
        features['completion_rate_prediction'] = 0.7
        features['virality_velocity'] = 0.5
        features['user_experience_score'] = 0.6

        # Phase 1: Enhanced features (calculées)
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if duration <= 15:
            features['video_duration_optimized'] = 0.8
        elif duration <= 30:
            features['video_duration_optimized'] = 1.0
        elif duration <= 60:
            features['video_duration_optimized'] = 0.6
        else:
            features['video_duration_optimized'] = 0.3

        hashtag_count = len(video_data.get('hashtags', []))
        if 3 <= hashtag_count <= 5:
            features['hashtag_effectiveness_score'] = 1.0
        elif 1 <= hashtag_count <= 7:
            features['hashtag_effectiveness_score'] = 0.7
        else:
            features['hashtag_effectiveness_score'] = 0.3

        features['music_trend_alignment'] = 0.5  # Placeholder
        features['publish_timing_score'] = 0.8  # Placeholder
        features['seasonal_timing_score'] = 0.7  # Placeholder
        features['trending_moment_alignment'] = 0.5  # Placeholder
        features['competition_level'] = 0.5  # Placeholder

        return features


class FeatureRegistry:
    """Registre central des feature sets disponibles."""

    def __init__(self):
        self.feature_sets = {}
        self._register_default_sets()

    def _register_default_sets(self):
        """Enregistre les feature sets par défaut."""
        self.register_feature_set(MetadataFeatureSet())
        self.register_feature_set(GeminiBasicFeatureSet())
        self.register_feature_set(VisualGranularFeatureSet())
        self.register_feature_set(ComprehensiveFeatureSet())

    def register_feature_set(self, feature_set: BaseFeatureSet):
        """Enregistre un feature set."""
        self.feature_sets[feature_set.name] = feature_set
        logger.info(
            f"Registered feature set: {feature_set.name} ({feature_set.get_feature_count()} features)")

    def get_feature_set(self, name: str) -> Optional[BaseFeatureSet]:
        """Récupère un feature set par nom."""
        return self.feature_sets.get(name)

    def list_feature_sets(self) -> List[str]:
        """Liste tous les feature sets disponibles."""
        return list(self.feature_sets.keys())

    def get_feature_set_info(self, name: str) -> Dict:
        """Récupère les informations d'un feature set."""
        feature_set = self.get_feature_set(name)
        if not feature_set:
            return {}

        return {
            'name': feature_set.name,
            'description': feature_set.description,
            'feature_count': feature_set.get_feature_count(),
            'features': feature_set.get_feature_names()
        }


class FeatureExtractorManager:
    """Gestionnaire central des feature extractors."""

    def __init__(self, feature_sets: List[str]):
        self.feature_sets = feature_sets
        self.registry = FeatureRegistry()
        self.extractors = self._load_extractors()

        logger.info(
            f"Initialized FeatureExtractorManager with sets: {feature_sets}")

    def _load_extractors(self) -> Dict[str, BaseFeatureSet]:
        """Charge les extractors pour les feature sets configurés."""
        extractors = {}

        for feature_set_name in self.feature_sets:
            feature_set = self.registry.get_feature_set(feature_set_name)
            if feature_set:
                extractors[feature_set_name] = feature_set
            else:
                logger.warning(
                    f"Feature set '{feature_set_name}' not found in registry")

        return extractors

    def extract_features(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait les features selon les feature sets configurés."""
        combined_features = {}

        for feature_set_name, extractor in self.extractors.items():
            try:
                features = extractor.extract(video_data, gemini_analysis)
                combined_features.update(features)
                logger.debug(
                    f"Extracted {len(features)} features from {feature_set_name}")
            except Exception as e:
                logger.error(
                    f"Error extracting features from {feature_set_name}: {e}")

        logger.info(f"Total features extracted: {len(combined_features)}")
        return combined_features

    def get_feature_count(self) -> int:
        """Retourne le nombre total de features configurées."""
        total = 0
        for extractor in self.extractors.values():
            total += extractor.get_feature_count()
        return total

    def get_feature_names(self) -> List[str]:
        """Retourne la liste de toutes les features configurées."""
        feature_names = []
        for extractor in self.extractors.values():
            feature_names.extend(extractor.get_feature_names())
        return feature_names


# Configuration des feature sets prédéfinis
FEATURE_SETS_CONFIG = {
    "baseline": ["metadata", "gemini_basic"],
    "enhanced": ["metadata", "gemini_basic", "visual_granular"],
    "comprehensive": ["comprehensive"],
    "experimental": ["metadata", "visual_granular", "comprehensive"]
}


def create_feature_extractor(config_name: str) -> FeatureExtractorManager:
    """Crée un feature extractor avec une configuration prédéfinie."""
    if config_name not in FEATURE_SETS_CONFIG:
        raise ValueError(f"Unknown feature set configuration: {config_name}")

    feature_sets = FEATURE_SETS_CONFIG[config_name]
    return FeatureExtractorManager(feature_sets)


def main():
    """Fonction de test pour valider l'architecture modulaire."""

    print("🧪 Testing Modular Feature System")
    print("=" * 50)

    # Test avec différentes configurations
    configs = ["baseline", "enhanced", "comprehensive"]

    for config in configs:
        print(f"\n📊 Testing {config} configuration:")

        try:
            extractor = create_feature_extractor(config)
            print(f"  • Feature sets: {extractor.feature_sets}")
            print(f"  • Total features: {extractor.get_feature_count()}")
            # Afficher les 5 premiers
            print(f"  • Feature names: {extractor.get_feature_names()[:5]}...")

        except Exception as e:
            print(f"  • Error: {e}")

    # Test d'extraction avec des données mock
    print(f"\n🧪 Testing feature extraction:")

    mock_video_data = {
        'id': 'test_123',
        'text': 'Test video',
        'videoMeta': {'duration': 25.5},
        'playCount': 15000,
        'diggCount': 1200,
        'commentCount': 150,
        'shareCount': 80,
        'hashtags': [{'name': 'test'}, {'name': 'viral'}],
        'musicMeta': {'musicName': 'Test Song', 'musicAuthor': 'Test Artist'},
        'createTimeISO': '2025-01-15T20:30:00Z'
    }

    mock_gemini_analysis = {
        'visual_analysis': {
            'human_presence': 'One person visible with eye contact',
            'shot_type': 'Medium close-up',
            'color_analysis': 'Vibrant colors',
            'text_overlays': 'No text overlays',
            'transitions': 'Smooth transitions',
            'style_quality': 'High quality'
        },
        'content_structure': {
            'hook_effectiveness': 'Effective hook',
            'story_flow': 'Clear story',
            'call_to_action': 'No call to action'
        },
        'engagement_factors': {
            'viral_potential': 'High viral potential',
            'emotional_triggers': 'humor, surprise',
            'audience_connection': 'Strong connection'
        },
        'technical_elements': {
            'length_optimization': 'Appropriate length',
            'sound_design': 'High quality audio',
            'production_quality': 'High quality'
        },
        'trend_alignment': {
            'current_trends': 'Perfectly aligned',
            'hashtag_potential': '#trending #viral'
        }
    }

    try:
        extractor = create_feature_extractor("baseline")
        features = extractor.extract_features(
            mock_video_data, mock_gemini_analysis)

        print(f"  • Extracted {len(features)} features")
        print(f"  • Sample features: {list(features.keys())[:5]}")

    except Exception as e:
        print(f"  • Error: {e}")

    print("\n✅ Modular feature system test completed!")


if __name__ == "__main__":
    main()
