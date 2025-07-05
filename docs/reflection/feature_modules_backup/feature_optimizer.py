#!/usr/bin/env python3
"""
Feature Optimizer - Implémentation de la stratégie d'optimisation des features
basée sur les ratios complexité vs valeur ajoutée.
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
class FeatureDefinition:
    """Définition d'une feature avec ses métriques d'optimisation."""
    name: str
    category: str
    data_type: str
    predictive_power: float      # 0-10
    business_impact: float       # 0-10
    uniqueness: float           # 0-10
    data_access_difficulty: float  # 0-10
    processing_difficulty: float   # 0-10
    subjectivity_level: float   # 0-10
    processing_time: float      # 0-10
    memory_usage: float         # 0-10
    api_calls: float            # 0-10
    description: str = ""


class FeatureOptimizer:
    """Optimiseur de features basé sur les ratios complexité vs valeur ajoutée."""

    def __init__(self):
        """Initialise l'optimiseur avec les features définies."""
        self.features = self._define_features()
        self.optimization_scores = {}
        self.selected_features = {}

    def _define_features(self) -> Dict[str, FeatureDefinition]:
        """Définit toutes les features avec leurs métriques."""

        features = {
            # Features Visuelles (Gemini)
            'close_up_presence': FeatureDefinition(
                name='close_up_presence',
                category='visual',
                data_type='bool',
                predictive_power=9.0,
                business_impact=8.5,
                uniqueness=9.5,
                data_access_difficulty=3.0,
                processing_difficulty=3.0,
                subjectivity_level=3.0,
                processing_time=2.0,
                memory_usage=2.0,
                api_calls=2.0,
                description='Présence de plans rapprochés (critique selon recherche)'
            ),

            'human_presence': FeatureDefinition(
                name='human_presence',
                category='visual',
                data_type='bool',
                predictive_power=8.5,
                business_impact=8.0,
                uniqueness=9.0,
                data_access_difficulty=2.5,
                processing_difficulty=2.5,
                subjectivity_level=2.5,
                processing_time=2.0,
                memory_usage=2.0,
                api_calls=2.0,
                description='Présence humaine dans la vidéo'
            ),

            'color_vibrancy_score': FeatureDefinition(
                name='color_vibrancy_score',
                category='visual',
                data_type='float',
                predictive_power=7.0,
                business_impact=6.5,
                uniqueness=7.5,
                data_access_difficulty=4.0,
                processing_difficulty=4.0,
                subjectivity_level=4.0,
                processing_time=3.0,
                memory_usage=3.0,
                api_calls=3.0,
                description='Score de saturation des couleurs'
            ),

            'transition_count': FeatureDefinition(
                name='transition_count',
                category='visual',
                data_type='int',
                predictive_power=7.5,
                business_impact=7.0,
                uniqueness=8.0,
                data_access_difficulty=5.0,
                processing_difficulty=5.0,
                subjectivity_level=5.0,
                processing_time=4.0,
                memory_usage=4.0,
                api_calls=4.0,
                description='Nombre de transitions dans la vidéo'
            ),

            # Features Temporelles
            'publish_hour': FeatureDefinition(
                name='publish_hour',
                category='temporal',
                data_type='int',
                predictive_power=6.0,
                business_impact=6.5,
                uniqueness=5.5,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Heure de publication (0-23)'
            ),

            'is_weekend': FeatureDefinition(
                name='is_weekend',
                category='temporal',
                data_type='bool',
                predictive_power=5.5,
                business_impact=6.0,
                uniqueness=5.0,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Publication en weekend'
            ),

            'is_peak_hours': FeatureDefinition(
                name='is_peak_hours',
                category='temporal',
                data_type='bool',
                predictive_power=6.5,
                business_impact=6.0,
                uniqueness=7.0,
                data_access_difficulty=2.0,
                processing_difficulty=2.0,
                subjectivity_level=1.5,
                processing_time=1.5,
                memory_usage=1.5,
                api_calls=1.5,
                description='Publication pendant les heures de pointe'
            ),

            'season': FeatureDefinition(
                name='season',
                category='temporal',
                data_type='str',
                predictive_power=5.0,
                business_impact=5.5,
                uniqueness=4.5,
                data_access_difficulty=1.5,
                processing_difficulty=1.5,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Saison de publication'
            ),

            # Features Métadonnées
            'video_duration': FeatureDefinition(
                name='video_duration',
                category='metadata',
                data_type='float',
                predictive_power=7.0,
                business_impact=7.5,
                uniqueness=6.5,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Durée de la vidéo en secondes'
            ),

            'hashtags_count': FeatureDefinition(
                name='hashtags_count',
                category='metadata',
                data_type='int',
                predictive_power=6.5,
                business_impact=6.0,
                uniqueness=7.0,
                data_access_difficulty=1.5,
                processing_difficulty=1.5,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Nombre de hashtags utilisés'
            ),

            'description_length': FeatureDefinition(
                name='description_length',
                category='metadata',
                data_type='int',
                predictive_power=5.5,
                business_impact=6.0,
                uniqueness=5.0,
                data_access_difficulty=1.0,
                processing_difficulty=1.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Longueur de la description'
            ),

            'account_followers': FeatureDefinition(
                name='account_followers',
                category='account',
                data_type='int',
                predictive_power=8.0,
                business_impact=7.5,
                uniqueness=7.0,
                data_access_difficulty=2.0,
                processing_difficulty=2.0,
                subjectivity_level=1.5,
                processing_time=1.5,
                memory_usage=1.5,
                api_calls=1.5,
                description='Nombre de followers du compte'
            ),

            'account_verification': FeatureDefinition(
                name='account_verification',
                category='account',
                data_type='bool',
                predictive_power=6.0,
                business_impact=6.5,
                uniqueness=5.5,
                data_access_difficulty=2.0,
                processing_difficulty=2.0,
                subjectivity_level=1.0,
                processing_time=1.0,
                memory_usage=1.0,
                api_calls=1.0,
                description='Statut de vérification du compte'
            ),
        }

        return features

    def calculate_feature_score(self, feature: FeatureDefinition) -> Dict[str, float]:
        """
        Calcule le score d'optimisation d'une feature.

        Args:
            feature: Définition de la feature

        Returns:
            Dictionnaire avec tous les scores calculés
        """

        # Valeur ajoutée (0-10)
        value_added = (
            feature.predictive_power * 0.4 +
            feature.business_impact * 0.3 +
            feature.uniqueness * 0.3
        )

        # Complexité d'extraction (0-10, plus élevé = plus complexe)
        extraction_complexity = (
            feature.data_access_difficulty * 0.4 +
            feature.processing_difficulty * 0.3 +
            feature.subjectivity_level * 0.3
        )

        # Complexité computationnelle (0-10, plus élevé = plus complexe)
        computation_complexity = (
            feature.processing_time * 0.5 +
            feature.memory_usage * 0.3 +
            feature.api_calls * 0.2
        )

        # Ratios
        value_extraction_ratio = value_added / \
            (extraction_complexity + 1)  # +1 pour éviter division par 0
        value_computation_ratio = value_added / (computation_complexity + 1)

        # Score composite
        optimization_score = (value_extraction_ratio *
                              0.6 + value_computation_ratio * 0.4) * 10

        return {
            'value_added': value_added,
            'extraction_complexity': extraction_complexity,
            'computation_complexity': computation_complexity,
            'value_extraction_ratio': value_extraction_ratio,
            'value_computation_ratio': value_computation_ratio,
            'optimization_score': optimization_score
        }

    def optimize_features(self) -> Dict[str, Any]:
        """
        Optimise toutes les features et retourne les résultats.

        Returns:
            Dictionnaire avec les features optimisées par priorité
        """

        # Calculer les scores pour toutes les features
        for name, feature in self.features.items():
            self.optimization_scores[name] = self.calculate_feature_score(
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

    def get_phase1_features(self) -> List[str]:
        """
        Retourne la liste des features sélectionnées pour la Phase 1.

        Returns:
            Liste des noms de features pour Phase 1
        """
        if not self.selected_features:
            self.optimize_features()

        # Phase 1 = Critical + Important features
        phase1_features = []
        phase1_features.extend(self.selected_features['critical'].keys())
        phase1_features.extend(self.selected_features['important'].keys())

        return phase1_features

    def generate_optimization_report(self) -> str:
        """
        Génère un rapport d'optimisation détaillé.

        Returns:
            Rapport formaté en markdown
        """
        if not self.optimization_scores:
            self.optimize_features()

        report = "# 📊 Rapport d'Optimisation des Features\n\n"

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
        report += f"- **Réduction** : {excluded_count + moderate_count}/{total_features} ({((excluded_count + moderate_count)/total_features)*100:.1f}%)\n\n"

        # Features critiques
        report += f"## 🥇 Features Critiques (Phase 1)\n\n"
        for name, feature in self.selected_features['critical'].items():
            scores = self.optimization_scores[name]
            report += f"### {name}\n"
            report += f"- **Catégorie** : {feature.category}\n"
            report += f"- **Score d'optimisation** : {scores['optimization_score']:.1f}\n"
            report += f"- **Valeur ajoutée** : {scores['value_added']:.1f}\n"
            report += f"- **Complexité extraction** : {scores['extraction_complexity']:.1f}\n"
            report += f"- **Description** : {feature.description}\n\n"

        # Features importantes
        report += f"## 🥈 Features Importantes (Phase 1)\n\n"
        for name, feature in self.selected_features['important'].items():
            scores = self.optimization_scores[name]
            report += f"### {name}\n"
            report += f"- **Catégorie** : {feature.category}\n"
            report += f"- **Score d'optimisation** : {scores['optimization_score']:.1f}\n"
            report += f"- **Valeur ajoutée** : {scores['value_added']:.1f}\n"
            report += f"- **Complexité extraction** : {scores['extraction_complexity']:.1f}\n"
            report += f"- **Description** : {feature.description}\n\n"

        return report

    def export_phase1_config(self) -> Dict[str, Any]:
        """
        Exporte la configuration des features Phase 1.

        Returns:
            Configuration pour l'implémentation
        """
        phase1_features = self.get_phase1_features()

        config = {
            'phase1_features': phase1_features,
            'feature_definitions': {},
            'extraction_strategy': {
                'direct_extraction': [],
                'simple_api_extraction': [],
                'gemini_extraction': []
            }
        }

        # Ajouter les définitions des features
        for name in phase1_features:
            feature = self.features[name]
            config['feature_definitions'][name] = {
                'category': feature.category,
                'data_type': feature.data_type,
                'description': feature.description
            }

            # Classer par stratégie d'extraction
            score = self.optimization_scores[name]['optimization_score']
            if score > 8.0:
                config['extraction_strategy']['direct_extraction'].append(name)
            elif score > 7.0:
                config['extraction_strategy']['simple_api_extraction'].append(
                    name)
            else:
                config['extraction_strategy']['gemini_extraction'].append(name)

        return config


def main():
    """Fonction principale pour tester l'optimiseur."""

    # Créer l'optimiseur
    optimizer = FeatureOptimizer()

    # Optimiser les features
    selected_features = optimizer.optimize_features()

    # Générer le rapport
    report = optimizer.generate_optimization_report()

    # Afficher le rapport
    print(report)

    # Exporter la configuration
    config = optimizer.export_phase1_config()

    print("\n" + "="*50)
    print("CONFIGURATION PHASE 1")
    print("="*50)
    print(f"Features sélectionnées : {len(config['phase1_features'])}")
    print(
        f"Extraction directe : {len(config['extraction_strategy']['direct_extraction'])}")
    print(
        f"API simple : {len(config['extraction_strategy']['simple_api_extraction'])}")
    print(
        f"Gemini : {len(config['extraction_strategy']['gemini_extraction'])}")

    return optimizer, config


if __name__ == "__main__":
    optimizer, config = main()
