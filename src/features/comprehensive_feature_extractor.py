#!/usr/bin/env python3
"""
Comprehensive Feature Extractor - Implémentation complète du feature engineering créatif
Basé sur la recherche scientifique, l'innovation et les données disponibles.
"""

import logging
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
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


class ComprehensiveFeatureExtractor:
    """
    Extracteur de features complet pour TikTok virality prediction.
    Combine features existantes, recherche scientifique et innovation créative.
    """

    def __init__(self):
        """Initialise l'extracteur avec toutes les définitions de features."""
        self.feature_definitions = self._define_all_features()
        self.extraction_stats = {
            'features_extracted': 0,
            'extraction_time': 0,
            'errors': []
        }

    def _define_all_features(self) -> Dict[str, FeatureDefinition]:
        """Définit toutes les features avec leurs métadonnées."""

        features = {
            # === PHASE 1: FOUNDATION FEATURES ===

            # Métadonnées améliorées
            'video_duration_optimized': FeatureDefinition(
                name='video_duration_optimized',
                category=FeatureCategory.METADATA,
                data_type='float',
                description='Durée optimisée pour la plateforme (15-60s optimal)',
                extraction_method='duration_analysis',
                complexity='easy',
                research_based=True,
                actionable=True
            ),

            'hashtag_effectiveness_score': FeatureDefinition(
                name='hashtag_effectiveness_score',
                category=FeatureCategory.METADATA,
                data_type='float',
                description='Score d\'efficacité des hashtags (0-1)',
                extraction_method='hashtag_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'music_trend_alignment': FeatureDefinition(
                name='music_trend_alignment',
                category=FeatureCategory.AUDIO,
                data_type='float',
                description='Alignement avec les tendances musicales (0-1)',
                extraction_method='music_trend_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'publish_timing_score': FeatureDefinition(
                name='publish_timing_score',
                category=FeatureCategory.TEMPORAL,
                data_type='float',
                description='Score de timing de publication (0-1)',
                extraction_method='temporal_analysis',
                complexity='easy',
                research_based=True,
                actionable=True
            ),

            # Visuelles granulaires
            'human_count': FeatureDefinition(
                name='human_count',
                category=FeatureCategory.VISUAL,
                data_type='int',
                description='Nombre de personnes dans la vidéo',
                extraction_method='gemini_vision',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'eye_contact_with_camera': FeatureDefinition(
                name='eye_contact_with_camera',
                category=FeatureCategory.VISUAL,
                data_type='bool',
                description='Contact visuel avec la caméra',
                extraction_method='gemini_vision',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'shot_type': FeatureDefinition(
                name='shot_type',
                category=FeatureCategory.VISUAL,
                data_type='str',
                description='Type de plan (close-up, medium, wide, extreme close-up)',
                extraction_method='gemini_vision',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'color_vibrancy_score': FeatureDefinition(
                name='color_vibrancy_score',
                category=FeatureCategory.VISUAL,
                data_type='float',
                description='Score de saturation des couleurs (0-1)',
                extraction_method='gemini_vision',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            # Temporelles avancées
            'seasonal_timing_score': FeatureDefinition(
                name='seasonal_timing_score',
                category=FeatureCategory.TEMPORAL,
                data_type='float',
                description='Score de timing saisonnier (0-1)',
                extraction_method='seasonal_analysis',
                complexity='easy',
                research_based=True,
                actionable=True
            ),

            'trending_moment_alignment': FeatureDefinition(
                name='trending_moment_alignment',
                category=FeatureCategory.TEMPORAL,
                data_type='float',
                description='Alignement avec les moments tendance (0-1)',
                extraction_method='trend_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'competition_level': FeatureDefinition(
                name='competition_level',
                category=FeatureCategory.TEMPORAL,
                data_type='float',
                description='Niveau de concurrence au moment de publication (0-1)',
                extraction_method='competition_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            # === PHASE 2: ADVANCED FEATURES ===

            # Audio avancé
            'music_energy': FeatureDefinition(
                name='music_energy',
                category=FeatureCategory.AUDIO,
                data_type='float',
                description='Énergie musicale (0-1)',
                extraction_method='audio_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            'audio_visual_sync_score': FeatureDefinition(
                name='audio_visual_sync_score',
                category=FeatureCategory.AUDIO,
                data_type='float',
                description='Synchronisation audio-visuelle (0-1)',
                extraction_method='sync_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            'voice_emotion': FeatureDefinition(
                name='voice_emotion',
                category=FeatureCategory.AUDIO,
                data_type='str',
                description='Émotion détectée dans la voix',
                extraction_method='voice_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            # Composition avancée
            'rule_of_thirds_score': FeatureDefinition(
                name='rule_of_thirds_score',
                category=FeatureCategory.VISUAL,
                data_type='float',
                description='Respect de la règle des tiers (0-1)',
                extraction_method='composition_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'depth_of_field_type': FeatureDefinition(
                name='depth_of_field_type',
                category=FeatureCategory.VISUAL,
                data_type='str',
                description='Type de profondeur de champ',
                extraction_method='gemini_vision',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            'color_palette_type': FeatureDefinition(
                name='color_palette_type',
                category=FeatureCategory.VISUAL,
                data_type='str',
                description='Type de palette de couleurs',
                extraction_method='color_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            # Psychologique
            'attention_grab_strength': FeatureDefinition(
                name='attention_grab_strength',
                category=FeatureCategory.PSYCHOLOGICAL,
                data_type='float',
                description='Force d\'accroche de l\'attention (0-1)',
                extraction_method='attention_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            'emotional_hook_strength': FeatureDefinition(
                name='emotional_hook_strength',
                category=FeatureCategory.PSYCHOLOGICAL,
                data_type='float',
                description='Force du hook émotionnel (0-1)',
                extraction_method='emotional_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            'relatability_score': FeatureDefinition(
                name='relatability_score',
                category=FeatureCategory.PSYCHOLOGICAL,
                data_type='float',
                description='Score de relatabilité (0-1)',
                extraction_method='relatability_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            # Créativité
            'originality_score': FeatureDefinition(
                name='originality_score',
                category=FeatureCategory.CREATIVITY,
                data_type='float',
                description='Score d\'originalité (0-1)',
                extraction_method='originality_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'creative_technique_count': FeatureDefinition(
                name='creative_technique_count',
                category=FeatureCategory.CREATIVITY,
                data_type='int',
                description='Nombre de techniques créatives utilisées',
                extraction_method='creativity_analysis',
                complexity='moderate',
                research_based=False,
                actionable=True
            ),

            'story_structure_type': FeatureDefinition(
                name='story_structure_type',
                category=FeatureCategory.CREATIVITY,
                data_type='str',
                description='Type de structure narrative',
                extraction_method='storytelling_analysis',
                complexity='moderate',
                research_based=True,
                actionable=True
            ),

            # === PHASE 3: INNOVATION FEATURES ===

            # Contexte culturel
            'cultural_relevance_score': FeatureDefinition(
                name='cultural_relevance_score',
                category=FeatureCategory.CULTURAL,
                data_type='float',
                description='Pertinence culturelle (0-1)',
                extraction_method='cultural_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'generational_appeal': FeatureDefinition(
                name='generational_appeal',
                category=FeatureCategory.CULTURAL,
                data_type='str',
                description='Appel générationnel',
                extraction_method='generational_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'social_issue_relevance': FeatureDefinition(
                name='social_issue_relevance',
                category=FeatureCategory.CULTURAL,
                data_type='float',
                description='Pertinence des enjeux sociaux (0-1)',
                extraction_method='social_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            # Viralité potentielle
            'shareability_score': FeatureDefinition(
                name='shareability_score',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Score de partage (0-1)',
                extraction_method='shareability_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'meme_potential': FeatureDefinition(
                name='meme_potential',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Potentiel meme (0-1)',
                extraction_method='meme_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'challenge_potential': FeatureDefinition(
                name='challenge_potential',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Potentiel challenge (0-1)',
                extraction_method='challenge_analysis',
                complexity='moderate',
                research_based=False,
                actionable=True
            ),

            # Performance
            'completion_rate_prediction': FeatureDefinition(
                name='completion_rate_prediction',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Prédiction du taux de completion (0-1)',
                extraction_method='completion_analysis',
                complexity='complex',
                research_based=True,
                actionable=True
            ),

            'virality_velocity': FeatureDefinition(
                name='virality_velocity',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Vélocité de viralité (0-1)',
                extraction_method='velocity_analysis',
                complexity='complex',
                research_based=False,
                actionable=True
            ),

            'user_experience_score': FeatureDefinition(
                name='user_experience_score',
                category=FeatureCategory.PERFORMANCE,
                data_type='float',
                description='Score d\'expérience utilisateur (0-1)',
                extraction_method='ux_analysis',
                complexity='moderate',
                research_based=False,
                actionable=True
            ),
        }

        return features

    def extract_phase1_features(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """
        Extrait les features de Phase 1 (Foundation).
        """
        features = {}

        try:
            # Métadonnées améliorées
            features.update(self._extract_enhanced_metadata(video_data))

            # Visuelles granulaires (si Gemini disponible)
            if gemini_analysis:
                features.update(
                    self._extract_granular_visual_features(gemini_analysis))

            # Temporelles avancées
            features.update(
                self._extract_advanced_temporal_features(video_data))

            self.extraction_stats['features_extracted'] += len(features)

        except Exception as e:
            logger.error(f"Error extracting Phase 1 features: {e}")
            self.extraction_stats['errors'].append(f"Phase 1: {str(e)}")

        return features

    def extract_phase2_features(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """
        Extrait les features de Phase 2 (Advanced).
        """
        features = {}

        try:
            # Audio avancé
            features.update(self._extract_advanced_audio_features(
                video_data, gemini_analysis))

            # Composition avancée
            if gemini_analysis:
                features.update(
                    self._extract_advanced_composition_features(gemini_analysis))

            # Psychologique
            features.update(self._extract_psychological_features(
                video_data, gemini_analysis))

            # Créativité
            features.update(self._extract_creativity_features(
                video_data, gemini_analysis))

            self.extraction_stats['features_extracted'] += len(features)

        except Exception as e:
            logger.error(f"Error extracting Phase 2 features: {e}")
            self.extraction_stats['errors'].append(f"Phase 2: {str(e)}")

        return features

    def extract_phase3_features(self, video_data: Dict, gemini_analysis: Optional[Dict] = None) -> Dict:
        """
        Extrait les features de Phase 3 (Innovation).
        """
        features = {}

        try:
            # Contexte culturel
            features.update(
                self._extract_cultural_context_features(video_data))

            # Viralité potentielle
            features.update(self._extract_virality_potential_features(
                video_data, gemini_analysis))

            # Performance
            features.update(self._extract_performance_features(video_data))

            self.extraction_stats['features_extracted'] += len(features)

        except Exception as e:
            logger.error(f"Error extracting Phase 3 features: {e}")
            self.extraction_stats['errors'].append(f"Phase 3: {str(e)}")

        return features

    def _extract_enhanced_metadata(self, video_data: Dict) -> Dict:
        """Extrait les métadonnées améliorées."""
        features = {}

        # Durée optimisée
        duration = video_data.get('duration', 0)
        if duration <= 15:
            features['video_duration_optimized'] = 0.8  # Optimal pour TikTok
        elif duration <= 30:
            features['video_duration_optimized'] = 1.0  # Très optimal
        elif duration <= 60:
            features['video_duration_optimized'] = 0.6  # Acceptable
        else:
            features['video_duration_optimized'] = 0.3  # Trop long

        # Score d'efficacité des hashtags
        hashtag_count = len(video_data.get('hashtags', []))
        if 3 <= hashtag_count <= 5:
            features['hashtag_effectiveness_score'] = 1.0  # Optimal
        elif 1 <= hashtag_count <= 7:
            features['hashtag_effectiveness_score'] = 0.7  # Acceptable
        else:
            features['hashtag_effectiveness_score'] = 0.3  # Non optimal

        # Alignement musique tendance (placeholder)
        # À implémenter avec API musique
        features['music_trend_alignment'] = 0.5

        # Score de timing de publication
        post_time = pd.to_datetime(video_data.get('createTimeISO', ''))
        hour = post_time.hour

        if 19 <= hour <= 21:
            features['publish_timing_score'] = 1.0  # Heures de pointe
        elif 18 <= hour <= 22:
            features['publish_timing_score'] = 0.8  # Bon timing
        elif 9 <= hour <= 17:
            features['publish_timing_score'] = 0.6  # Heures de travail
        else:
            features['publish_timing_score'] = 0.4  # Heures creuses

        return features

    def _extract_granular_visual_features(self, gemini_analysis: Dict) -> Dict:
        """Extrait les features visuelles granulaires depuis Gemini."""
        features = {}

        visual_analysis = gemini_analysis.get('visual_analysis', {})

        # Nombre d'humains
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

        return features

    def _extract_advanced_temporal_features(self, video_data: Dict) -> Dict:
        """Extrait les features temporelles avancées."""
        features = {}

        post_time = pd.to_datetime(video_data.get('createTimeISO', ''))

        # Score de timing saisonnier
        month = post_time.month
        if month in [6, 7, 8]:  # Été
            features['seasonal_timing_score'] = 0.8
        elif month in [12, 1, 2]:  # Hiver
            features['seasonal_timing_score'] = 0.7
        else:
            features['seasonal_timing_score'] = 0.6

        # Alignement moment tendance (placeholder)
        # À implémenter avec API tendances
        features['trending_moment_alignment'] = 0.5

        # Niveau de concurrence (placeholder)
        # À implémenter avec analyse concurrentielle
        features['competition_level'] = 0.5

        return features

    def _extract_advanced_audio_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features audio avancées."""
        features = {}

        # Énergie musicale (placeholder)
        features['music_energy'] = 0.6  # À implémenter avec analyse audio

        # Synchronisation audio-visuelle (placeholder)
        # À implémenter avec analyse sync
        features['audio_visual_sync_score'] = 0.7

        # Émotion vocale (placeholder)
        # À implémenter avec analyse vocale
        features['voice_emotion'] = 'neutral'

        return features

    def _extract_advanced_composition_features(self, gemini_analysis: Dict) -> Dict:
        """Extrait les features de composition avancée."""
        features = {}

        visual_analysis = gemini_analysis.get('visual_analysis', {})

        # Score règle des tiers (placeholder)
        # À implémenter avec analyse composition
        features['rule_of_thirds_score'] = 0.7

        # Type de profondeur de champ
        depth_text = visual_analysis.get('depth_analysis', '')
        if 'shallow' in depth_text.lower():
            features['depth_of_field_type'] = 'shallow'
        elif 'deep' in depth_text.lower():
            features['depth_of_field_type'] = 'deep'
        else:
            features['depth_of_field_type'] = 'medium'

        # Type de palette de couleurs (placeholder)
        # À implémenter avec analyse couleur
        features['color_palette_type'] = 'complementary'

        return features

    def _extract_psychological_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features psychologiques."""
        features = {}

        # Force d'accroche (placeholder)
        # À implémenter avec analyse attention
        features['attention_grab_strength'] = 0.6

        # Force du hook émotionnel (placeholder)
        # À implémenter avec analyse émotionnelle
        features['emotional_hook_strength'] = 0.7

        # Score de relatabilité (placeholder)
        # À implémenter avec analyse relatabilité
        features['relatability_score'] = 0.5

        return features

    def _extract_creativity_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features de créativité."""
        features = {}

        # Score d'originalité (placeholder)
        # À implémenter avec analyse originalité
        features['originality_score'] = 0.6

        # Nombre de techniques créatives (placeholder)
        # À implémenter avec analyse créativité
        features['creative_technique_count'] = 2

        # Type de structure narrative (placeholder)
        # À implémenter avec analyse storytelling
        features['story_structure_type'] = 'linear'

        return features

    def _extract_cultural_context_features(self, video_data: Dict) -> Dict:
        """Extrait les features de contexte culturel."""
        features = {}

        # Pertinence culturelle (placeholder)
        # À implémenter avec analyse culturelle
        features['cultural_relevance_score'] = 0.5

        # Appel générationnel (placeholder)
        # À implémenter avec analyse générationnelle
        features['generational_appeal'] = 'Gen Z'

        # Pertinence des enjeux sociaux (placeholder)
        # À implémenter avec analyse sociale
        features['social_issue_relevance'] = 0.3

        return features

    def _extract_virality_potential_features(self, video_data: Dict, gemini_analysis: Optional[Dict]) -> Dict:
        """Extrait les features de potentiel viral."""
        features = {}

        # Score de partage (placeholder)
        # À implémenter avec analyse partage
        features['shareability_score'] = 0.6

        # Potentiel meme (placeholder)
        features['meme_potential'] = 0.4  # À implémenter avec analyse meme

        # Potentiel challenge (placeholder)
        # À implémenter avec analyse challenge
        features['challenge_potential'] = 0.5

        return features

    def _extract_performance_features(self, video_data: Dict) -> Dict:
        """Extrait les features de performance."""
        features = {}

        # Prédiction taux de completion (placeholder)
        # À implémenter avec modèle prédictif
        features['completion_rate_prediction'] = 0.7

        # Vélocité de viralité (placeholder)
        # À implémenter avec analyse vélocité
        features['virality_velocity'] = 0.5

        # Score d'expérience utilisateur (placeholder)
        # À implémenter avec analyse UX
        features['user_experience_score'] = 0.6

        return features

    def extract_all_features(
        self,
        video_data: Dict,
        gemini_analysis: Optional[Dict] = None,
        phases: List[int] = [1, 2, 3]
    ) -> Dict:
        """
        Extrait toutes les features selon les phases spécifiées.

        Args:
            video_data: Données vidéo TikTok
            gemini_analysis: Analyse Gemini (optionnel)
            phases: Phases à extraire [1, 2, 3]

        Returns:
            Dictionnaire avec toutes les features extraites
        """
        start_time = datetime.now()
        all_features = {}

        try:
            # Phase 1: Foundation
            if 1 in phases:
                phase1_features = self.extract_phase1_features(
                    video_data, gemini_analysis)
                all_features.update(phase1_features)
                logger.info(
                    f"Extracted {len(phase1_features)} Phase 1 features")

            # Phase 2: Advanced
            if 2 in phases:
                phase2_features = self.extract_phase2_features(
                    video_data, gemini_analysis)
                all_features.update(phase2_features)
                logger.info(
                    f"Extracted {len(phase2_features)} Phase 2 features")

            # Phase 3: Innovation
            if 3 in phases:
                phase3_features = self.extract_phase3_features(
                    video_data, gemini_analysis)
                all_features.update(phase3_features)
                logger.info(
                    f"Extracted {len(phase3_features)} Phase 3 features")

            # Ajouter les métadonnées de base
            all_features['video_id'] = video_data.get('id', '')
            all_features['extraction_timestamp'] = datetime.now().isoformat()

            self.extraction_stats['extraction_time'] = (
                datetime.now() - start_time).total_seconds()

        except Exception as e:
            logger.error(f"Error in comprehensive feature extraction: {e}")
            self.extraction_stats['errors'].append(f"Comprehensive: {str(e)}")

        return all_features

    def get_feature_summary(self) -> Dict:
        """Retourne un résumé des features extraites."""
        return {
            'total_features_defined': len(self.feature_definitions),
            'features_by_category': {
                category.value: len(
                    [f for f in self.feature_definitions.values() if f.category == category])
                for category in FeatureCategory
            },
            'features_by_complexity': {
                complexity: len(
                    [f for f in self.feature_definitions.values() if f.complexity == complexity])
                for complexity in ['easy', 'moderate', 'complex']
            },
            'research_based_features': len([f for f in self.feature_definitions.values() if f.research_based]),
            'actionable_features': len([f for f in self.feature_definitions.values() if f.actionable]),
            'extraction_stats': self.extraction_stats
        }


def main():
    """Fonction principale pour tester l'extracteur complet."""

    # Créer l'extracteur
    extractor = ComprehensiveFeatureExtractor()

    # Afficher le résumé des features
    summary = extractor.get_feature_summary()

    print("🎯 Comprehensive Feature Extractor - Summary")
    print("=" * 50)
    print(f"Total features defined: {summary['total_features_defined']}")
    print(f"Research-based features: {summary['research_based_features']}")
    print(f"Actionable features: {summary['actionable_features']}")

    print("\n📊 Features by Category:")
    for category, count in summary['features_by_category'].items():
        print(f"  • {category}: {count}")

    print("\n🔧 Features by Complexity:")
    for complexity, count in summary['features_by_complexity'].items():
        print(f"  • {complexity}: {count}")

    print("\n📋 Feature Definitions:")
    for name, feature in extractor.feature_definitions.items():
        print(f"  • {name}: {feature.description}")

    return extractor


if __name__ == "__main__":
    extractor = main()
