#!/usr/bin/env python3
"""
📊 File: modular_feature_system.py
🎯 Purpose: Modular feature engineering system for TikTok virality prediction with extensible architecture
📚 Concepts: Feature Engineering, Modular Design, Object-Oriented Programming, Feature Categories
🔗 Related: docs/educational/ml_glossary.md, scripts/analyze_existing_data.py

📖 Educational Notes:
- This module demonstrates advanced software engineering principles applied to machine learning
- Shows how to create modular, extensible feature extraction systems
- Implements the Strategy pattern for different feature extraction approaches
- Provides a framework for adding new feature types without modifying existing code

🚀 Usage:
from src.features.modular_feature_system import create_feature_extractor
extractor = create_feature_extractor('comprehensive')
features = extractor.extract_features(video_data, gemini_analysis)

📈 Architecture Benefits:
- Modularity: Easy to add/remove feature sets
- Extensibility: New feature types can be added independently
- Maintainability: Clear separation of concerns
- Testability: Each feature set can be tested in isolation

🔧 Dependencies:
- Python dataclasses, enums, ABC (Abstract Base Classes)
- Custom feature extraction logic
- Gemini AI analysis integration

🎓 Key Software Engineering Concepts:
1. Abstract Base Classes (ABC) - Defines interface for feature sets
2. Strategy Pattern - Different feature extraction strategies
3. Factory Pattern - Creates appropriate feature extractors
4. Registry Pattern - Manages available feature sets
5. Separation of Concerns - Each class has a single responsibility

📚 For detailed explanations, see: docs/educational/ml_glossary.md
"""

from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging
import numpy as np
import pandas as pd
from datetime import datetime
import re

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
        """Extrait les features avancées avec logique intelligente du comprehensive extractor."""
        features = {}

        try:
            # Phase 1: Enhanced features (calculées intelligemment)
            features.update(self._extract_enhanced_phase1_features(video_data))

            # Phase 2: Advanced features (avec logique intelligente)
            features.update(self._extract_advanced_phase2_features(
                video_data, gemini_analysis))

            # Phase 3: Innovation features (avec logique intelligente)
            features.update(self._extract_innovation_phase3_features(
                video_data, gemini_analysis))

        except Exception as e:
            logger.error(f"Error extracting advanced features: {e}")
            # Return default values if extraction fails
            for feature in self.features:
                if feature not in features:
                    features[feature] = 0.5  # Default neutral value

        return features

    def _extract_enhanced_phase1_features(self, video_data: Dict) -> Dict:
        """Extrait les features Phase 1 améliorées avec logique intelligente."""
        features = {}

        # Video duration optimization - based on TikTok best practices
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if duration <= 15:
            # Good for quick engagement
            features['video_duration_optimized'] = 0.8
        elif duration <= 30:
            features['video_duration_optimized'] = 1.0  # Optimal for TikTok
        elif duration <= 60:
            features['video_duration_optimized'] = 0.6  # Acceptable
        else:
            features['video_duration_optimized'] = 0.3  # Too long for TikTok

        # Hashtag effectiveness - based on research
        hashtag_count = len(video_data.get('hashtags', []))
        if 3 <= hashtag_count <= 5:
            features['hashtag_effectiveness_score'] = 1.0  # Optimal range
        elif 1 <= hashtag_count <= 7:
            features['hashtag_effectiveness_score'] = 0.7  # Good range
        else:
            # Too few or too many
            features['hashtag_effectiveness_score'] = 0.3

        # Music trend alignment - placeholder for future music analysis
        features['music_trend_alignment'] = 0.5

        # Publish timing score - based on hour of day
        post_time = video_data.get('createTimeISO', '')
        if post_time:
            import pandas as pd
            post_time = pd.to_datetime(post_time)
            hour = post_time.hour
            # Peak hours: 7-9 AM, 12-2 PM, 7-9 PM
            if (7 <= hour <= 9) or (12 <= hour <= 14) or (19 <= hour <= 21):
                features['publish_timing_score'] = 0.9
            elif (9 <= hour <= 12) or (14 <= hour <= 19):
                features['publish_timing_score'] = 0.7
            else:
                features['publish_timing_score'] = 0.4
        else:
            features['publish_timing_score'] = 0.5

        # Seasonal timing score - based on month
        if post_time:
            month = post_time.month
            # Peak months: March-May, September-November
            if month in [3, 4, 5, 9, 10, 11]:
                features['seasonal_timing_score'] = 0.8
            else:
                features['seasonal_timing_score'] = 0.6
        else:
            features['seasonal_timing_score'] = 0.7

        # Trending moment alignment - placeholder for trend analysis
        features['trending_moment_alignment'] = 0.5

        # Competition level - based on hashtag popularity
        hashtags = [tag['name'].lower()
                    for tag in video_data.get('hashtags', [])]
        popular_hashtags = ['fyp', 'foryou', 'viral', 'trending', 'tiktok']
        popular_count = sum(1 for tag in hashtags if tag in popular_hashtags)
        features['competition_level'] = min(popular_count * 0.2, 1.0)

        return features

    def _extract_advanced_phase2_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features Phase 2 avancées avec logique intelligente."""
        features = {}

        # Audio-visual features (placeholders for future audio analysis)
        features['music_energy'] = 0.6
        features['audio_visual_sync_score'] = 0.7
        features['voice_emotion'] = 'neutral'

        # Visual composition features (placeholders for future analysis)
        features['rule_of_thirds_score'] = 0.7
        features['depth_of_field_type'] = 'shallow'
        features['color_palette_type'] = 'vibrant'

        # Psychological features - based on content analysis
        features.update(self._extract_psychological_features(
            video_data, gemini_analysis))

        # Creativity features - based on content structure
        features.update(self._extract_creativity_features(
            video_data, gemini_analysis))

        return features

    def _extract_innovation_phase3_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features Phase 3 d'innovation avec logique intelligente."""
        features = {}

        # Cultural context features
        features.update(self._extract_cultural_context_features(video_data))

        # Virality potential features
        features.update(self._extract_virality_potential_features(
            video_data, gemini_analysis))

        # Performance features
        features.update(self._extract_performance_features(video_data))

        return features

    def _extract_psychological_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features psychologiques basées sur l'analyse du contenu."""
        features = {}

        # Attention grab strength - based on hook presence and visual impact
        hook_present = gemini_analysis.get('content_structure', {}).get(
            'hook_effectiveness', '').lower() if gemini_analysis else ''
        visual_quality = gemini_analysis.get('visual_analysis', {}).get(
            'style_quality', '').lower() if gemini_analysis else ''

        attention_score = 0.5  # Base score
        if 'effective' in hook_present:
            attention_score += 0.3
        if 'high quality' in visual_quality:
            attention_score += 0.2
        features['attention_grab_strength'] = min(attention_score, 1.0)

        # Emotional hook strength - based on emotional triggers
        emotional_triggers = gemini_analysis.get('engagement_factors', {}).get(
            'emotional_triggers', '') if gemini_analysis else ''
        trigger_count = len([t for t in emotional_triggers.split(
            ',') if t.strip()]) if emotional_triggers else 0
        features['emotional_hook_strength'] = min(
            0.3 + (trigger_count * 0.2), 1.0)

        # Relatability score - based on content type and audience connection
        audience_connection = gemini_analysis.get('engagement_factors', {}).get(
            'audience_connection', '').lower() if gemini_analysis else ''
        features['relatability_score'] = 0.8 if 'strong' in audience_connection else 0.5

        return features

    def _extract_creativity_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features de créativité basées sur la structure du contenu."""
        features = {}

        # Originality score - based on content uniqueness
        content_structure = gemini_analysis.get(
            'content_structure', {}) if gemini_analysis else {}
        story_flow = content_structure.get('story_flow', '').lower()
        transitions = gemini_analysis.get('visual_analysis', {}).get(
            'transitions', '').lower() if gemini_analysis else ''

        originality_score = 0.5  # Base score
        if 'unique' in story_flow or 'creative' in story_flow:
            originality_score += 0.3
        if 'smooth' in transitions or 'creative' in transitions:
            originality_score += 0.2
        features['originality_score'] = min(originality_score, 1.0)

        # Creative technique count - count of creative elements
        creative_elements = 0
        if gemini_analysis:
            if 'transitions' in gemini_analysis.get('visual_analysis', {}):
                creative_elements += 1
            if 'text_overlays' in gemini_analysis.get('visual_analysis', {}):
                creative_elements += 1
            if 'call_to_action' in gemini_analysis.get('content_structure', {}):
                creative_elements += 1
        features['creative_technique_count'] = creative_elements

        # Story structure type - categorize narrative structure
        if gemini_analysis:
            story_flow = gemini_analysis.get(
                'content_structure', {}).get('story_flow', '').lower()
            if 'linear' in story_flow:
                features['story_structure_type'] = 'linear'
            elif 'circular' in story_flow:
                features['story_structure_type'] = 'circular'
            else:
                features['story_structure_type'] = 'linear'  # Default
        else:
            features['story_structure_type'] = 'linear'

        return features

    def _extract_cultural_context_features(self, video_data: Dict) -> Dict:
        """Extrait les features de contexte culturel basées sur le contenu et le timing."""
        features = {}

        # Cultural relevance score - based on hashtags and content
        hashtags = [tag['name'].lower()
                    for tag in video_data.get('hashtags', [])]
        cultural_keywords = ['trend', 'viral', 'fyp', 'foryou', 'tiktok']
        cultural_matches = sum(1 for tag in hashtags if any(
            keyword in tag for keyword in cultural_keywords))
        features['cultural_relevance_score'] = min(
            cultural_matches / max(len(hashtags), 1), 1.0)

        # Generational appeal - based on content characteristics
        # Simple heuristic: shorter videos tend to appeal more to Gen Z
        duration = video_data.get('videoMeta', {}).get('duration', 60)
        if duration <= 15:
            features['generational_appeal'] = 'Gen Z'
        elif duration <= 30:
            features['generational_appeal'] = 'Gen Z/Millennial'
        else:
            features['generational_appeal'] = 'Millennial'

        # Social issue relevance - placeholder for future implementation
        features['social_issue_relevance'] = 0.3  # Default low relevance

        return features

    def _extract_virality_potential_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features de potentiel viral basées sur les caractéristiques du contenu."""
        features = {}

        # Shareability score - based on content characteristics
        viral_potential = gemini_analysis.get('engagement_factors', {}).get(
            'viral_potential', '').lower() if gemini_analysis else ''
        features['shareability_score'] = 0.8 if 'high' in viral_potential else 0.5

        # Meme potential - based on content type and structure
        content_type = video_data.get('text', '').lower()
        meme_keywords = ['meme', 'funny', 'lol', 'haha', '😂', '🤣']
        meme_matches = sum(
            1 for keyword in meme_keywords if keyword in content_type)
        features['meme_potential'] = min(meme_matches * 0.2, 1.0)

        # Challenge potential - based on content characteristics
        challenge_keywords = ['challenge', 'try', 'test', 'dare']
        challenge_matches = sum(
            1 for keyword in challenge_keywords if keyword in content_type)
        features['challenge_potential'] = min(challenge_matches * 0.3, 1.0)

        return features

    def _extract_performance_features(self, video_data: Dict) -> Dict:
        """Extrait les features de performance basées sur le contenu et les métadonnées."""
        features = {}

        # Completion rate prediction - based on video length and engagement
        duration = video_data.get('videoMeta', {}).get('duration', 60)
        # Shorter videos tend to have higher completion rates
        if duration <= 15:
            features['completion_rate_prediction'] = 0.8
        elif duration <= 30:
            features['completion_rate_prediction'] = 0.7
        elif duration <= 60:
            features['completion_rate_prediction'] = 0.6
        else:
            features['completion_rate_prediction'] = 0.5

        # Virality velocity - based on content characteristics
        # Placeholder for future implementation
        features['virality_velocity'] = 0.5

        # User experience score - based on video quality and structure
        # Placeholder for future implementation
        features['user_experience_score'] = 0.6

        return features


class ModelCompatibleFeatureSet(BaseFeatureSet):
    """Feature set compatible avec le modèle ML (exactement 16 features)."""

    def __init__(self):
        super().__init__(
            name="model_compatible",
            description="Features exactement compatibles avec le modèle ML (16 features)"
        )
        self.features = [
            'duration', 'hashtag_count', 'estimated_hashtag_count', 'hour_of_day',
            'day_of_week', 'month', 'visual_quality_score', 'has_hook',
            'viral_potential_score', 'emotional_trigger_count',
            'audience_connection_score', 'sound_quality_score',
            'production_quality_score', 'trend_alignment_score', 'color_vibrancy_score',
            'video_duration_optimized'
        ]

    def extract(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """Extrait exactement les 16 features attendues par le modèle ML."""
        features = {}

        # 1. duration
        features['duration'] = video_data.get(
            'videoMeta', {}).get('duration', 0)

        # 2. hashtag_count
        hashtags = video_data.get('hashtags', [])
        # Handle both string list and dict list formats
        if hashtags and isinstance(hashtags[0], dict):
            hashtags = [tag['name'] for tag in hashtags]
        features['hashtag_count'] = len(hashtags)

        # 3. estimated_hashtag_count (même que hashtag_count pour compatibilité)
        features['estimated_hashtag_count'] = features['hashtag_count']

        # 4-6. Features temporelles
        post_time = video_data.get('createTimeISO', '')
        if post_time:
            import pandas as pd
            post_time = pd.to_datetime(post_time)
            features['hour_of_day'] = post_time.hour
            features['day_of_week'] = post_time.dayofweek
            features['month'] = post_time.month
        else:
            features['hour_of_day'] = 12  # Default
            features['day_of_week'] = 0   # Monday
            features['month'] = 1         # January

        # 7-16. Features Gemini (avec fallbacks)
        if gemini_analysis:
            # visual_quality_score
            visual = gemini_analysis.get('visual_analysis', {})
            features['visual_quality_score'] = 0.8 if 'high quality' in str(
                visual).lower() else 0.6

            # has_hook
            content = gemini_analysis.get('content_structure', {})
            features['has_hook'] = 1.0 if 'hook' in str(
                content).lower() else 0.0

            # viral_potential_score
            engagement = gemini_analysis.get('engagement_factors', {})
            features['viral_potential_score'] = 0.7 if 'viral' in str(
                engagement).lower() else 0.5

            # emotional_trigger_count
            features['emotional_trigger_count'] = 3 if 'emotional' in str(
                engagement).lower() else 1

            # audience_connection_score
            features['audience_connection_score'] = 0.7 if 'connection' in str(
                engagement).lower() else 0.5

            # sound_quality_score
            technical = gemini_analysis.get('technical_elements', {})
            features['sound_quality_score'] = 0.8 if 'sound' in str(
                technical).lower() else 0.6

            # production_quality_score
            features['production_quality_score'] = 0.8 if 'quality' in str(
                technical).lower() else 0.6

            # trend_alignment_score
            trend = gemini_analysis.get('trend_alignment', {})
            features['trend_alignment_score'] = 0.6 if 'trend' in str(
                trend).lower() else 0.4

            # color_vibrancy_score
            features['color_vibrancy_score'] = 0.7 if 'color' in str(
                visual).lower() else 0.5

            # video_duration_optimized
            features['video_duration_optimized'] = 1.0 if 15 <= features['duration'] <= 60 else 0.0
        else:
            # Fallbacks si pas d'analyse Gemini
            features['visual_quality_score'] = 0.6
            features['has_hook'] = 0.0
            features['viral_potential_score'] = 0.5
            features['emotional_trigger_count'] = 1
            features['audience_connection_score'] = 0.5
            features['sound_quality_score'] = 0.6
            features['production_quality_score'] = 0.6
            features['trend_alignment_score'] = 0.4
            features['color_vibrancy_score'] = 0.5
            features['video_duration_optimized'] = 1.0 if 15 <= features['duration'] <= 60 else 0.0

        return features


class EnhancedFeatureSet(BaseFeatureSet):
    """Enhanced feature set with quality-based features"""

    def __init__(self):
        super().__init__("enhanced_quality",
                         "Enhanced quality-based features for viral prediction")

    def extract(self, video_data: Dict[str, Any], gemini_analysis: Optional[Dict] = None) -> Dict[str, Any]:
        """Extract enhanced features from video data"""

        features = {}

        # 1. Hashtag Quality Score (quality vs quantity)
        features['hashtag_quality_score'] = self._calculate_hashtag_quality(
            video_data)

        # 2. Creator Popularity Bias Correction
        features['creator_popularity_bias'] = self._calculate_creator_bias(
            video_data)

        # 3. Content Uniqueness Score
        features['content_uniqueness_score'] = self._calculate_content_uniqueness(
            video_data, gemini_analysis)

        # 4. Completion Rate Estimate
        features['completion_rate_estimate'] = self._calculate_completion_rate(
            video_data)

        # 5. Engagement Velocity Score
        features['engagement_velocity_score'] = self._calculate_engagement_velocity(
            video_data)

        # 6. Trend Alignment Score
        features['trend_alignment_score'] = self._calculate_trend_alignment(
            video_data, gemini_analysis)

        # 7. Emotional Impact Score
        features['emotional_impact_score'] = self._calculate_emotional_impact(
            gemini_analysis)

        # 8. Shareability Score
        features['shareability_score'] = self._calculate_shareability(
            video_data, gemini_analysis)

        return features

    def _calculate_hashtag_quality(self, video_data: Dict[str, Any]) -> float:
        """Calculate hashtag quality score (quality vs quantity)"""

        hashtags = video_data.get('hashtags', [])
        if not hashtags:
            return 0.0

        # Handle both string list and dict list formats
        if isinstance(hashtags[0], dict):
            hashtags = [tag['name'] for tag in hashtags]

        hashtag_count = len(hashtags)

        # Quality indicators
        quality_indicators = 0

        # Popular hashtags (indicate trend following)
        popular_hashtags = ['fyp', 'viral', 'trending', 'foryou', 'foryoupage']
        popular_count = sum(
            1 for tag in hashtags if tag.lower() in popular_hashtags)

        # Specific hashtags (indicate niche content)
        specific_count = hashtag_count - popular_count

        # Balance score: prefer specific over popular
        if hashtag_count > 0:
            specific_ratio = specific_count / hashtag_count
            quality_indicators += specific_ratio * 0.5

        # Optimal hashtag count (3-5 is ideal)
        if 3 <= hashtag_count <= 5:
            quality_indicators += 0.3
        elif hashtag_count > 5:
            quality_indicators += 0.1  # Too many hashtags

        # Length of hashtags (longer = more specific)
        avg_length = np.mean([len(tag) for tag in hashtags]) if hashtags else 0
        if avg_length > 8:
            quality_indicators += 0.2

        return min(quality_indicators, 1.0)

    def _calculate_creator_bias(self, video_data: Dict[str, Any]) -> float:
        """Calculate creator popularity bias correction"""

        # Get creator stats if available
        creator_stats = video_data.get('authorStats', {})

        if not creator_stats:
            return 0.5  # Neutral bias

        follower_count = creator_stats.get('followerCount', 0)
        video_count = creator_stats.get('videoCount', 0)

        # Calculate bias based on creator size
        if follower_count > 1000000:  # Mega creator
            return 0.2  # High bias correction needed
        elif follower_count > 100000:  # Popular creator
            return 0.4  # Medium bias correction
        elif follower_count > 10000:  # Growing creator
            return 0.6  # Low bias correction
        else:  # Emerging creator
            return 0.8  # Minimal bias correction

    def _calculate_content_uniqueness(self, video_data: Dict[str, Any], gemini_analysis: Optional[Dict] = None) -> float:
        """Calculate content uniqueness score"""

        uniqueness_score = 0.5  # Base score

        if gemini_analysis:
            # Analyze content originality
            content_analysis = gemini_analysis.get('content_analysis', {})

            # Originality indicators
            if content_analysis.get('is_original', False):
                uniqueness_score += 0.3

            if content_analysis.get('creative_technique_count', 0) > 2:
                uniqueness_score += 0.2

            # Avoid common patterns
            if content_analysis.get('uses_trending_format', False):
                uniqueness_score -= 0.1

            if content_analysis.get('is_generic', False):
                uniqueness_score -= 0.2

        # Duration uniqueness (very short or very long videos)
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if duration < 10 or duration > 60:
            uniqueness_score += 0.1

        return max(0.0, min(1.0, uniqueness_score))

    def _calculate_completion_rate(self, video_data: Dict[str, Any]) -> float:
        """Estimate completion rate based on video characteristics"""

        duration = video_data.get('videoMeta', {}).get('duration', 0)

        # Optimal duration for completion (15-30 seconds)
        if 15 <= duration <= 30:
            return 0.9
        elif 10 <= duration <= 45:
            return 0.7
        elif duration < 10:
            return 0.8  # Very short videos often get completed
        elif duration > 60:
            return 0.3  # Long videos have lower completion rates
        else:
            return 0.5

    def _calculate_engagement_velocity(self, video_data: Dict[str, Any]) -> float:
        """Calculate engagement velocity score"""

        view_count = video_data.get('stats', {}).get('playCount', 0)
        like_count = video_data.get('stats', {}).get('diggCount', 0)
        comment_count = video_data.get('stats', {}).get('commentCount', 0)

        if view_count == 0:
            return 0.0

        # Engagement rate
        engagement_rate = (like_count + comment_count * 2) / view_count

        # Normalize to 0-1 scale
        # High engagement: > 0.1, Medium: 0.05-0.1, Low: < 0.05
        if engagement_rate > 0.1:
            return 1.0
        elif engagement_rate > 0.05:
            return 0.7
        elif engagement_rate > 0.02:
            return 0.4
        else:
            return 0.1

    def _calculate_trend_alignment(self, video_data: Dict[str, Any], gemini_analysis: Optional[Dict] = None) -> float:
        """Calculate trend alignment score"""

        trend_score = 0.5  # Base score

        # Check hashtags for trending topics
        hashtags = video_data.get('hashtags', [])
        if isinstance(hashtags[0], dict):
            hashtags = [tag['name'] for tag in hashtags]

        trending_hashtags = ['fyp', 'viral',
                             'trending', 'foryou', 'foryoupage']
        trending_count = sum(
            1 for tag in hashtags if tag.lower() in trending_hashtags)

        if trending_count > 0:
            trend_score += 0.2

        if gemini_analysis:
            # Check if content aligns with current trends
            content_analysis = gemini_analysis.get('content_analysis', {})
            if content_analysis.get('trend_alignment', False):
                trend_score += 0.3

        return min(trend_score, 1.0)

    def _calculate_emotional_impact(self, gemini_analysis: Optional[Dict] = None) -> float:
        """Calculate emotional impact score"""

        if not gemini_analysis:
            return 0.5

        emotional_score = 0.5  # Base score

        # Emotional triggers
        emotional_triggers = gemini_analysis.get('emotional_triggers', [])
        if emotional_triggers:
            emotional_score += len(emotional_triggers) * 0.1

        # Emotional intensity
        emotional_intensity = gemini_analysis.get(
            'emotional_intensity', 'neutral')
        if emotional_intensity == 'high':
            emotional_score += 0.3
        elif emotional_intensity == 'medium':
            emotional_score += 0.2

        return min(emotional_score, 1.0)

    def _calculate_shareability(self, video_data: Dict[str, Any], gemini_analysis: Optional[Dict] = None) -> float:
        """Calculate shareability score"""

        shareability_score = 0.5  # Base score

        # Duration factor (shorter videos are more shareable)
        duration = video_data.get('videoMeta', {}).get('duration', 0)
        if duration <= 30:
            shareability_score += 0.2
        elif duration > 60:
            shareability_score -= 0.1

        if gemini_analysis:
            # Content factors
            content_analysis = gemini_analysis.get('content_analysis', {})

            if content_analysis.get('has_hook', False):
                shareability_score += 0.2

            if content_analysis.get('has_story', False):
                shareability_score += 0.1

            if content_analysis.get('relatability_score', 0) > 0.7:
                shareability_score += 0.2

        return min(shareability_score, 1.0)


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
        self.register_feature_set(ModelCompatibleFeatureSet())
        self.register_feature_set(EnhancedFeatureSet())

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
    "model_compatible": ["model_compatible"],
    "enhanced_quality": ["enhanced_quality"],
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
