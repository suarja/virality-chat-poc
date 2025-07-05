#!/usr/bin/env python3
"""
Enhanced Feature Optimizer - Optimisation avec features granulaires et valeur business
Basé sur les ratios complexité vs valeur ajoutée, avec focus sur l'actionnabilité.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class FeaturePriority(Enum):
    """Priorités des features basées sur le score d'optimisation."""
    CRITICAL = "critical"      # Score > 7.0
    IMPORTANT = "important"    # Score 5.0-7.0
    MODERATE = "moderate"      # Score 3.0-5.0
    EXCLUDED = "excluded"      # Score < 3.0


@dataclass
class EnhancedFeatureDefinition:
    """Définition d'une feature avec métriques d'optimisation améliorées."""
    name: str
    category: str
    data_type: str
    predictive_power: float      # 0-10
    business_impact: float       # 0-10
    # 0-10 - NOUVEAU: Capacité à générer des insights actionnables
    actionability: float
    uniqueness: float           # 0-10
    data_access_difficulty: float  # 0-10
    processing_difficulty: float   # 0-10
    subjectivity_level: float   # 0-10
    processing_time: float      # 0-10
    memory_usage: float         # 0-10
    api_calls: float            # 0-10
    description: str = ""
    actionable_insight: str = ""  # NOUVEAU: Exemple d'insight généré


class EnhancedFeatureOptimizer:
    """Optimiseur de features amélioré avec focus sur l'actionnabilité."""

    def __init__(self):
        """Initialise l'optimiseur avec les features granulaires définies."""
        self.features = self._define_enhanced_features()
        self.optimization_scores = {}
        self.selected_features = {}

    def _define_enhanced_features(self) -> Dict[str, EnhancedFeatureDefinition]:
        """Définit les features granulaires avec leurs métriques."""

        features = {
            # Features Humaines Granulaires
            'human_count': EnhancedFeatureDefinition(
                name='human_count',
                category='human',
                data_type='int',
                predictive_power=7.5,
                business_impact=8.0,
                actionability=9.0,  # Très actionnable
                uniqueness=7.0,
                data_access_difficulty=3.0,
                processing_difficulty=3.0,
                subjectivity_level=2.0,
                processing_time=2.0,
                memory_usage=2.0,
                api_calls=2.0,
                description='Nombre de personnes dans la vidéo',
                actionable_insight='Incluez 2-3 personnes pour maximiser l\'engagement (+30% views)'
            ),

            'eye_contact_with_camera': EnhancedFeatureDefinition(
                name='eye_contact_with_camera',
                category='human',
                data_type='bool',
                predictive_power=8.5,
                business_impact=8.5,
                actionability=9.5,  # Très actionnable
                uniqueness=8.5,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=3.0,
                processing_time=3.0,
                memory_usage=3.0,
                api_calls=3.0,
                description='Contact visuel avec la caméra',
                actionable_insight='Augmentez le contact visuel avec la caméra (+40% engagement)'
            ),

            'hand_gestures_count': EnhancedFeatureDefinition(
                name='hand_gestures_count',
                category='human',
                data_type='int',
                predictive_power=7.0,
                business_impact=7.5,
                actionability=8.5,  # Très actionnable
                uniqueness=8.0,
                data_access_difficulty=4.5,
                processing_difficulty=4.5,
                subjectivity_level=3.5,
                processing_time=3.5,
                memory_usage=3.5,
                api_calls=3.5,
                description='Nombre de gestes des mains expressifs',
                actionable_insight='Ajoutez des gestes des mains expressifs (+25% rétention)'
            ),

            'emotional_intensity': EnhancedFeatureDefinition(
                name='emotional_intensity',
                category='human',
                data_type='float',
                predictive_power=8.0,
                business_impact=8.0,
                actionability=8.0,  # Actionnable
                uniqueness=8.5,
                data_access_difficulty=5.0,
                processing_difficulty=5.0,
                subjectivity_level=4.0,
                processing_time=4.0,
                memory_usage=4.0,
                api_calls=4.0,
                description='Intensité émotionnelle (0-1)',
                actionable_insight='Augmentez l\'intensité émotionnelle (+35% engagement)'
            ),

            # Features Composition Granulaires
            'shot_type': EnhancedFeatureDefinition(
                name='shot_type',
                category='composition',
                data_type='str',
                predictive_power=8.0,
                business_impact=8.5,
                actionability=9.0,  # Très actionnable
                uniqueness=7.5,
                data_access_difficulty=3.5,
                processing_difficulty=3.5,
                subjectivity_level=3.0,
                processing_time=3.0,
                memory_usage=3.0,
                api_calls=3.0,
                description='Type de plan (close-up, medium, wide, extreme close-up)',
                actionable_insight='Utilisez des plans rapprochés (close-up) pour les visages (+35% engagement)'
            ),

            'face_occupancy_ratio': EnhancedFeatureDefinition(
                name='face_occupancy_ratio',
                category='composition',
                data_type='float',
                predictive_power=7.5,
                business_impact=7.5,
                actionability=8.5,  # Très actionnable
                uniqueness=8.0,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=3.0,
                processing_time=3.5,
                memory_usage=3.5,
                api_calls=3.5,
                description='% d\'écran occupé par le visage',
                actionable_insight='Augmentez la taille du visage à 60-70% de l\'écran (+25% rétention)'
            ),

            'rule_of_thirds_compliance': EnhancedFeatureDefinition(
                name='rule_of_thirds_compliance',
                category='composition',
                data_type='float',
                predictive_power=6.5,
                business_impact=7.0,
                actionability=8.0,  # Actionnable
                uniqueness=7.0,
                data_access_difficulty=4.5,
                processing_difficulty=4.5,
                subjectivity_level=3.5,
                processing_time=4.0,
                memory_usage=4.0,
                api_calls=4.0,
                description='Respect de la règle des tiers (0-1)',
                actionable_insight='Respectez la règle des tiers pour un cadrage optimal (+20% qualité perçue)'
            ),

            'camera_angle': EnhancedFeatureDefinition(
                name='camera_angle',
                category='composition',
                data_type='str',
                predictive_power=7.0,
                business_impact=7.0,
                actionability=8.5,  # Très actionnable
                uniqueness=7.5,
                data_access_difficulty=3.5,
                processing_difficulty=3.5,
                subjectivity_level=3.0,
                processing_time=3.0,
                memory_usage=3.0,
                api_calls=3.0,
                description='Angle de caméra (face, profil, 3/4, plongée, contre-plongée)',
                actionable_insight='Utilisez des angles de face pour plus d\'engagement (+20% likes)'
            ),

            # Features Couleur Granulaires
            'dominant_colors': EnhancedFeatureDefinition(
                name='dominant_colors',
                category='color',
                data_type='list',
                predictive_power=7.0,
                business_impact=7.5,
                actionability=9.0,  # Très actionnable
                uniqueness=8.0,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=3.0,
                processing_time=3.5,
                memory_usage=3.5,
                api_calls=3.5,
                description='Couleurs dominantes (RGB)',
                actionable_insight='Utilisez des couleurs chaudes (#FF6B6B, #FFA500) pour plus d\'engagement (+15% likes)'
            ),

            'lighting_quality': EnhancedFeatureDefinition(
                name='lighting_quality',
                category='color',
                data_type='float',
                predictive_power=8.0,
                business_impact=8.5,
                actionability=9.0,  # Très actionnable
                uniqueness=7.5,
                data_access_difficulty=4.5,
                processing_difficulty=4.5,
                subjectivity_level=4.0,
                processing_time=4.0,
                memory_usage=4.0,
                api_calls=4.0,
                description='Qualité de l\'éclairage (0-1)',
                actionable_insight='Améliorez l\'éclairage pour une meilleure qualité (+30% partage)'
            ),

            'warm_cool_balance': EnhancedFeatureDefinition(
                name='warm_cool_balance',
                category='color',
                data_type='float',
                predictive_power=6.5,
                business_impact=7.0,
                actionability=8.5,  # Très actionnable
                uniqueness=7.0,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=3.5,
                processing_time=3.5,
                memory_usage=3.5,
                api_calls=3.5,
                description='Balance chaud/froid (-1 à 1)',
                actionable_insight='Utilisez des tons chauds pour plus d\'engagement (+20% views)'
            ),

            # Features Transitions Granulaires
            'transition_types': EnhancedFeatureDefinition(
                name='transition_types',
                category='transitions',
                data_type='list',
                predictive_power=7.5,
                business_impact=7.5,
                actionability=9.0,  # Très actionnable
                uniqueness=8.0,
                data_access_difficulty=4.5,
                processing_difficulty=4.5,
                subjectivity_level=3.5,
                processing_time=4.0,
                memory_usage=4.0,
                api_calls=4.0,
                description='Types de transitions (cut, fade, wipe, zoom, etc.)',
                actionable_insight='Utilisez des effets de zoom pour dynamiser (+20% engagement)'
            ),

            'transition_smoothness': EnhancedFeatureDefinition(
                name='transition_smoothness',
                category='transitions',
                data_type='float',
                predictive_power=7.0,
                business_impact=7.0,
                actionability=8.5,  # Très actionnable
                uniqueness=7.5,
                data_access_difficulty=5.0,
                processing_difficulty=5.0,
                subjectivity_level=4.0,
                processing_time=4.5,
                memory_usage=4.5,
                api_calls=4.5,
                description='Fluidité des transitions (0-1)',
                actionable_insight='Ajoutez des transitions fluides toutes les 3-5 secondes (+25% rétention)'
            ),

            'text_readability_score': EnhancedFeatureDefinition(
                name='text_readability_score',
                category='transitions',
                data_type='float',
                predictive_power=8.0,
                business_impact=8.5,
                actionability=9.5,  # Très actionnable
                uniqueness=8.0,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=3.5,
                processing_time=3.5,
                memory_usage=3.5,
                api_calls=3.5,
                description='Lisibilité du texte (0-1)',
                actionable_insight='Incluez du texte lisible pour expliquer (+40% partage)'
            ),

            # Features Temporelles (conservées)
            'publish_hour': EnhancedFeatureDefinition(
                name='publish_hour',
                category='temporal',
                data_type='int',
                predictive_power=6.0,
                business_impact=6.5,
                actionability=7.0,  # Modérément actionnable
                uniqueness=5.5,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Heure de publication (0-23)',
                actionable_insight='Publiez entre 19h-21h pour maximiser l\'engagement (+25% views)'
            ),

            'is_weekend': EnhancedFeatureDefinition(
                name='is_weekend',
                category='temporal',
                data_type='bool',
                predictive_power=5.5,
                business_impact=6.0,
                actionability=7.5,  # Actionnable
                uniqueness=5.0,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Publication en weekend',
                actionable_insight='Publiez le weekend pour plus d\'engagement (+20% likes)'
            ),

            # Features Métadonnées (conservées)
            'video_duration': EnhancedFeatureDefinition(
                name='video_duration',
                category='metadata',
                data_type='float',
                predictive_power=7.0,
                business_impact=7.5,
                actionability=8.0,  # Actionnable
                uniqueness=6.5,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Durée de la vidéo en secondes',
                actionable_insight='Optimisez la durée entre 15-30 secondes (+30% completion rate)'
            ),

            'hashtags_count': EnhancedFeatureDefinition(
                name='hashtags_count',
                category='metadata',
                data_type='int',
                predictive_power=6.5,
                business_impact=6.0,
                actionability=8.5,  # Très actionnable
                uniqueness=7.0,
                data_access_difficulty=1.5,
                processing_difficulty=1.5,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Nombre de hashtags utilisés',
                actionable_insight='Utilisez 3-5 hashtags pertinents (+25% discoverability)'
            ),
        }

        return features

    def calculate_enhanced_feature_score(self, feature: EnhancedFeatureDefinition) -> Dict[str, float]:
        """
        Calcule le score d'optimisation amélioré avec focus sur l'actionnabilité.
        """

        # Valeur ajoutée améliorée (inclut l'actionnabilité)
        value_added = (
            feature.predictive_power * 0.3 +
            feature.business_impact * 0.25 +
            feature.actionability * 0.25 +  # NOUVEAU: Poids important pour l'actionnabilité
            feature.uniqueness * 0.2
        )

        # Complexité d'extraction (inchangée)
        extraction_complexity = (
            feature.data_access_difficulty * 0.4 +
            feature.processing_difficulty * 0.3 +
            feature.subjectivity_level * 0.3
        )

        # Complexité computationnelle (inchangée)
        computation_complexity = (
            feature.processing_time * 0.5 +
            feature.memory_usage * 0.3 +
            feature.api_calls * 0.2
        )

        # Ratios
        value_extraction_ratio = value_added / (extraction_complexity + 1)
        value_computation_ratio = value_added / (computation_complexity + 1)

        # Score composite avec bonus pour l'actionnabilité
        base_score = (value_extraction_ratio * 0.6 +
                      value_computation_ratio * 0.4) * 10

        # Bonus pour l'actionnabilité (features très actionnables ont un bonus)
        actionability_bonus = feature.actionability * \
            0.5 if feature.actionability > 8.0 else 0

        optimization_score = base_score + actionability_bonus

        return {
            'value_added': value_added,
            'actionability': feature.actionability,
            'extraction_complexity': extraction_complexity,
            'computation_complexity': computation_complexity,
            'value_extraction_ratio': value_extraction_ratio,
            'value_computation_ratio': value_computation_ratio,
            'base_score': base_score,
            'actionability_bonus': actionability_bonus,
            'optimization_score': optimization_score
        }

    def optimize_enhanced_features(self) -> Dict[str, Any]:
        """
        Optimise toutes les features avec le nouveau scoring.
        """

        # Calculer les scores pour toutes les features
        for name, feature in self.features.items():
            self.optimization_scores[name] = self.calculate_enhanced_feature_score(
                feature)

        # Classer les features par priorité
        critical_features = {}
        important_features = {}
        moderate_features = {}
        excluded_features = {}

        for name, scores in self.optimization_scores.items():
            score = scores['optimization_score']
            feature = self.features[name]

            if score > 7.0:
                critical_features[name] = feature
            elif score > 5.0:
                important_features[name] = feature
            elif score > 3.0:
                moderate_features[name] = feature
            else:
                excluded_features[name] = feature

        self.selected_features = {
            'critical': critical_features,
            'important': important_features,
            'moderate': moderate_features,
            'excluded': excluded_features
        }

        return self.selected_features

    def get_enhanced_phase1_features(self) -> List[str]:
        """
        Retourne la liste des features sélectionnées pour la Phase 1 améliorée.
        """
        if not self.selected_features:
            self.optimize_enhanced_features()

        # Phase 1 améliorée = Critical + Important features
        phase1_features = []
        phase1_features.extend(self.selected_features['critical'].keys())
        phase1_features.extend(self.selected_features['important'].keys())

        return phase1_features

    def generate_enhanced_optimization_report(self) -> str:
        """
        Génère un rapport d'optimisation amélioré avec focus sur l'actionnabilité.
        """
        if not self.optimization_scores:
            self.optimize_enhanced_features()

        report = "# 📊 Rapport d'Optimisation Amélioré - Features Granulaires\n\n"

        # Résumé
        total_features = len(self.features)
        critical_count = len(self.selected_features['critical'])
        important_count = len(self.selected_features['important'])
        moderate_count = len(self.selected_features['moderate'])
        excluded_count = len(self.selected_features['excluded'])

        report += f"## 📈 Résumé\n\n"
        report += f"- **Total features évaluées** : {total_features}\n"
        report += f"- **Features critiques** : {critical_count} (Phase 1)\n"
        report += f"- **Features importantes** : {important_count} (Phase 1)\n"
        report += f"- **Features modérées** : {moderate_count} (Phase 2)\n"
        report += f"- **Features exclues** : {excluded_count}\n"
        report += f"- **Actionnabilité moyenne** : {np.mean([f.actionability for f in self.features.values()]):.1f}/10\n\n"

        # Features critiques avec insights
        report += f"## 🥇 Features Critiques (Phase 1) - Avec Insights Actionnables\n\n"
        for name, feature in self.selected_features['critical'].items():
            scores = self.optimization_scores[name]
            report += f"### {name}\n"
            report += f"- **Catégorie** : {feature.category}\n"
            report += f"- **Score d'optimisation** : {scores['optimization_score']:.1f}\n"
            report += f"- **Valeur ajoutée** : {scores['value_added']:.1f}\n"
            report += f"- **Actionnabilité** : {feature.actionability:.1f}/10\n"
            report += f"- **Complexité extraction** : {scores['extraction_complexity']:.1f}\n"
            report += f"- **Insight actionnable** : {feature.actionable_insight}\n\n"

        # Features importantes avec insights
        report += f"## 🥈 Features Importantes (Phase 1) - Avec Insights Actionnables\n\n"
        for name, feature in self.selected_features['important'].items():
            scores = self.optimization_scores[name]
            report += f"### {name}\n"
            report += f"- **Catégorie** : {feature.category}\n"
            report += f"- **Score d'optimisation** : {scores['optimization_score']:.1f}\n"
            report += f"- **Valeur ajoutée** : {scores['value_added']:.1f}\n"
            report += f"- **Actionnabilité** : {feature.actionability:.1f}/10\n"
            report += f"- **Complexité extraction** : {scores['extraction_complexity']:.1f}\n"
            report += f"- **Insight actionnable** : {feature.actionable_insight}\n\n"

        return report


def main():
    """Fonction principale pour tester l'optimiseur amélioré."""

    # Créer l'optimiseur amélioré
    optimizer = EnhancedFeatureOptimizer()

    # Optimiser les features
    selected_features = optimizer.optimize_enhanced_features()

    # Générer le rapport
    report = optimizer.generate_enhanced_optimization_report()

    # Afficher le rapport
    print(report)

    # Afficher les features sélectionnées
    phase1_features = optimizer.get_enhanced_phase1_features()
    print(f"\n{'='*60}")
    print("FEATURES PHASE 1 AMÉLIORÉES")
    print(f"{'='*60}")
    print(f"Total features sélectionnées : {len(phase1_features)}")
    print(f"Features : {', '.join(phase1_features)}")

    return optimizer, phase1_features


if __name__ == "__main__":
    optimizer, features = main()
