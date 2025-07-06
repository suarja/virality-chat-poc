"""
🎯 Endpoint de Simulation Pre-Publication TikTok
📊 Simule différents scénarios de publication pour optimiser la viralité
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
from pydantic import BaseModel, Field


class SimulationScenario(BaseModel):
    """Scénario de simulation"""
    name: str = Field(..., description="Nom du scénario")
    description: str = Field(..., description="Description du scénario")

    # Paramètres de publication
    publication_hour: int = Field(..., ge=0, le=23,
                                  description="Heure de publication (0-23)")
    publication_day: str = Field(...,
                                 description="Jour de publication (monday, tuesday, etc.)")

    # Paramètres de contenu
    hashtags: List[str] = Field(
        default_factory=list, description="Hashtags à utiliser")
    trending_hashtags: List[str] = Field(
        default_factory=list, description="Hashtags trending")
    custom_hashtags: List[str] = Field(
        default_factory=list, description="Hashtags personnalisés")

    # Paramètres de simulation
    engagement_multiplier: float = Field(
        default=1.0, ge=0.1, le=10.0, description="Multiplicateur d'engagement")
    reach_multiplier: float = Field(
        default=1.0, ge=0.1, le=10.0, description="Multiplicateur de portée")

    # Paramètres de contenu
    video_length: int = Field(default=30, ge=5, le=300,
                              description="Longueur vidéo en secondes")
    has_text_overlays: bool = Field(
        default=False, description="A des overlays texte")
    has_transitions: bool = Field(
        default=False, description="A des transitions")
    has_call_to_action: bool = Field(
        default=False, description="A un call-to-action")


class SimulationRequest(BaseModel):
    """Requête de simulation"""
    video_url: str = Field(..., description="URL de la vidéo TikTok")
    scenarios: List[SimulationScenario] = Field(
        ..., description="Scénarios à tester")
    include_post_publication: bool = Field(
        default=False, description="Inclure les métriques post-publication")
    simulation_count: int = Field(
        default=5, ge=1, le=20, description="Nombre de simulations par scénario")


class SimulationResult(BaseModel):
    """Résultat de simulation"""
    scenario_name: str
    scenario_description: str
    simulations: List[Dict[str, Any]]
    average_virality_score: float
    best_virality_score: float
    worst_virality_score: float
    recommendations: List[str]


class SimulationResponse(BaseModel):
    """Réponse de simulation"""
    video_url: str
    original_virality_score: float
    scenarios: List[SimulationResult]
    best_scenario: str
    best_score: float
    summary: Dict[str, Any]


class TikTokSimulationService:
    """Service de simulation TikTok"""

    def __init__(self, feature_manager, ml_manager, tiktok_scraper_integration):
        self.feature_manager = feature_manager
        self.ml_manager = ml_manager
        self.tiktok_scraper_integration = tiktok_scraper_integration

        # Hashtags trending par défaut (à mettre à jour régulièrement)
        self.trending_hashtags = [
            "fyp", "foryou", "viral", "trending", "tiktok", "funny", "dance",
            "comedy", "food", "fashion", "beauty", "fitness", "travel", "music"
        ]

        # Heures optimales par jour (basé sur des études)
        self.optimal_hours = {
            "monday": [9, 12, 18, 21],
            "tuesday": [9, 12, 18, 21],
            "wednesday": [9, 12, 18, 21],
            "thursday": [9, 12, 18, 21],
            "friday": [9, 12, 18, 21],
            "saturday": [10, 14, 19, 22],
            "sunday": [10, 14, 19, 22]
        }

    def generate_scenario_variations(self, base_scenario: SimulationScenario) -> List[SimulationScenario]:
        """Génère des variations d'un scénario de base"""
        variations = []

        # Variation 1: Heures optimales
        for hour in self.optimal_hours.get(base_scenario.publication_day.lower(), [9, 12, 18, 21]):
            variation = base_scenario.copy()
            variation.name = f"{base_scenario.name}_optimal_hour_{hour}"
            variation.description = f"{base_scenario.description} - Heure optimale: {hour}h"
            variation.publication_hour = hour
            variations.append(variation)

        # Variation 2: Hashtags trending
        if base_scenario.trending_hashtags:
            variation = base_scenario.copy()
            variation.name = f"{base_scenario.name}_trending_hashtags"
            variation.description = f"{base_scenario.description} - Avec hashtags trending"
            variation.hashtags = base_scenario.hashtags + \
                random.sample(self.trending_hashtags, 3)
            variations.append(variation)

        # Variation 3: Engagement boost
        variation = base_scenario.copy()
        variation.name = f"{base_scenario.name}_engagement_boost"
        variation.description = f"{base_scenario.description} - Boost engagement"
        variation.engagement_multiplier = 1.5
        variation.reach_multiplier = 1.3
        variations.append(variation)

        return variations

    def simulate_video_features(self, video_data: Dict[str, Any], scenario: SimulationScenario) -> Dict[str, Any]:
        """Simule les features d'une vidéo selon le scénario"""

        # Features de base (extraction réelle)
        base_features = self.feature_manager.extract_features(video_data)

        # Simulation des features pre-publication
        simulated_features = base_features.copy()

        # Simulation de l'heure de publication
        hour_factor = self._calculate_hour_factor(scenario.publication_hour)
        simulated_features['publication_hour_factor'] = hour_factor

        # Simulation des hashtags
        hashtag_score = self._calculate_hashtag_score(scenario.hashtags)
        simulated_features['hashtag_virality_score'] = hashtag_score

        # Simulation de l'engagement
        if scenario.engagement_multiplier != 1.0:
            simulated_features['engagement_multiplier'] = scenario.engagement_multiplier

        # Simulation de la portée
        if scenario.reach_multiplier != 1.0:
            simulated_features['reach_multiplier'] = scenario.reach_multiplier

        # Features de contenu simulées
        simulated_features['video_length'] = scenario.video_length
        simulated_features['has_text_overlays'] = scenario.has_text_overlays
        simulated_features['has_transitions'] = scenario.has_transitions
        simulated_features['has_call_to_action'] = scenario.has_call_to_action

        return simulated_features

    def _calculate_hour_factor(self, hour: int) -> float:
        """Calcule le facteur d'heure optimal"""
        # Heures de pointe: 9h, 12h, 18h, 21h
        peak_hours = [9, 12, 18, 21]

        if hour in peak_hours:
            return 1.5  # Boost de 50%
        elif hour in [10, 11, 13, 14, 19, 20, 22]:
            return 1.2  # Boost de 20%
        else:
            return 0.8  # Réduction de 20%

    def _calculate_hashtag_score(self, hashtags: List[str]) -> float:
        """Calcule le score de viralité des hashtags"""
        if not hashtags:
            return 0.5

        score = 0.0
        trending_count = 0

        for hashtag in hashtags:
            if hashtag.lower() in [h.lower() for h in self.trending_hashtags]:
                trending_count += 1
                score += 0.3
            else:
                score += 0.1

        # Bonus pour le nombre optimal de hashtags (3-5)
        if 3 <= len(hashtags) <= 5:
            score += 0.2

        # Bonus pour les hashtags trending
        if trending_count >= 2:
            score += 0.3

        return min(score, 1.0)

    def generate_recommendations(self, scenario: SimulationScenario, scores: List[float]) -> List[str]:
        """Génère des recommandations basées sur les scores"""
        recommendations = []
        avg_score = sum(scores) / len(scores)

        # Recommandations d'heure
        if scenario.publication_hour not in self.optimal_hours.get(scenario.publication_day.lower(), []):
            recommendations.append(
                f"Publier à une heure optimale: {', '.join(map(str, self.optimal_hours.get(scenario.publication_day.lower(), [9, 12, 18, 21])))}h")

        # Recommandations de hashtags
        if len(scenario.hashtags) < 3:
            recommendations.append(
                "Ajouter plus de hashtags (3-5 recommandés)")
        elif len(scenario.hashtags) > 5:
            recommendations.append(
                "Réduire le nombre de hashtags (3-5 recommandés)")

        # Recommandations de contenu
        if not scenario.has_call_to_action:
            recommendations.append(
                "Ajouter un call-to-action pour augmenter l'engagement")

        if not scenario.has_text_overlays:
            recommendations.append(
                "Ajouter des overlays texte pour améliorer la rétention")

        if avg_score < 0.6:
            recommendations.append(
                "Considérer une refonte du contenu pour améliorer la viralité")

        return recommendations

    async def run_simulation(self, request: SimulationRequest) -> SimulationResponse:
        """Exécute la simulation complète"""

        # Scraper la vidéo
        video_data = await self.tiktok_scraper_integration.get_video_data_from_url(request.video_url)

        if not video_data:
            raise ValueError(
                f"Impossible de scraper la vidéo: {request.video_url}")

        # Score original
        original_features = self.feature_manager.extract_features(video_data)
        original_score = self.ml_manager.predict(
            original_features)['virality_score']

        results = []
        best_scenario = None
        best_score = 0.0

        # Tester chaque scénario
        for scenario in request.scenarios:
            scenario_results = []

            # Générer des variations du scénario
            variations = self.generate_scenario_variations(scenario)

            for variation in variations:
                for i in range(request.simulation_count):
                    # Simuler les features
                    simulated_features = self.simulate_video_features(
                        video_data, variation)

                    # Prédire la viralité
                    virality_score = self.ml_manager.predict(
                        simulated_features)['virality_score']

                    # Ajouter du bruit pour la variance
                    noise = random.uniform(-0.05, 0.05)
                    virality_score = max(0.0, min(1.0, virality_score + noise))

                    simulation_result = {
                        "variation": variation.name,
                        "features": simulated_features,
                        "virality_score": virality_score,
                        "publication_hour": variation.publication_hour,
                        "hashtags": variation.hashtags,
                        "engagement_multiplier": variation.engagement_multiplier
                    }

                    scenario_results.append(simulation_result)

            # Calculer les statistiques du scénario
            scores = [r["virality_score"] for r in scenario_results]
            avg_score = sum(scores) / len(scores)

            if avg_score > best_score:
                best_score = avg_score
                best_scenario = scenario.name

            # Générer les recommandations
            recommendations = self.generate_recommendations(scenario, scores)

            result = SimulationResult(
                scenario_name=scenario.name,
                scenario_description=scenario.description,
                simulations=scenario_results,
                average_virality_score=avg_score,
                best_virality_score=max(scores),
                worst_virality_score=min(scores),
                recommendations=recommendations
            )

            results.append(result)

        # Résumé
        summary = {
            "total_simulations": len(request.scenarios) * request.simulation_count,
            "scenarios_tested": len(request.scenarios),
            "improvement_potential": best_score - original_score,
            "recommendations_count": sum(len(r.recommendations) for r in results)
        }

        return SimulationResponse(
            video_url=request.video_url,
            original_virality_score=original_score,
            scenarios=results,
            best_scenario=best_scenario or "Aucun",
            best_score=best_score,
            summary=summary
        )

    async def simulate_virality(self, request: SimulationRequest) -> SimulationResponse:
        """Simulate virality prediction with different parameters"""
        return await self.run_simulation(request)
