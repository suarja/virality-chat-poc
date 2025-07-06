"""
🎯 Pre-Publication Virality Simulation Service
📊 Simulates different publication scenarios for virality prediction
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
from pydantic import BaseModel, Field


class SimulationScenario(BaseModel):
    """Simulation scenario for pre-publication testing"""
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")

    # Publication parameters
    publication_hour: int = Field(..., ge=0, le=23,
                                  description="Publication hour (0-23)")
    publication_day: str = Field(...,
                                 description="Publication day (monday, tuesday, etc.)")

    # Content parameters
    hashtags: List[str] = Field(
        default_factory=list, description="Hashtags to use")
    trending_hashtags: List[str] = Field(
        default_factory=list, description="Trending hashtags")
    custom_hashtags: List[str] = Field(
        default_factory=list, description="Custom hashtags")

    # Simulation parameters
    engagement_multiplier: float = Field(
        default=1.0, ge=0.1, le=10.0, description="Engagement multiplier")
    reach_multiplier: float = Field(
        default=1.0, ge=0.1, le=10.0, description="Reach multiplier")

    # Content features
    video_length: int = Field(default=30, ge=5, le=300,
                              description="Video length in seconds")
    has_text_overlays: bool = Field(
        default=False, description="Has text overlays")
    has_transitions: bool = Field(
        default=False, description="Has transitions")
    has_call_to_action: bool = Field(
        default=False, description="Has call-to-action")


class SimulationRequest(BaseModel):
    """Simulation request for pre-publication testing"""
    video_url: str = Field(...,
                           description="Reference TikTok video URL (for content analysis only)")
    scenarios: List[SimulationScenario] = Field(
        ..., description="Scenarios to test")
    use_cache: bool = Field(
        default=True, description="Use cached video data if available")
    simulation_count: int = Field(
        default=5, ge=1, le=20, description="Number of simulations per scenario")


class SimulationResult(BaseModel):
    """Simulation result"""
    scenario_name: str
    scenario_description: str
    simulations: List[Dict[str, Any]]
    average_virality_score: float
    best_virality_score: float
    worst_virality_score: float
    recommendations: List[str]


class SimulationResponse(BaseModel):
    """Simulation response"""
    video_url: str
    base_virality_score: float
    scenarios: List[SimulationResult]
    best_scenario: str
    best_score: float
    summary: Dict[str, Any]


class TikTokSimulationService:
    """TikTok pre-publication simulation service"""

    def __init__(self, feature_manager, ml_manager, tiktok_scraper_integration):
        self.feature_manager = feature_manager
        self.ml_manager = ml_manager
        self.tiktok_scraper_integration = tiktok_scraper_integration

        # Default trending hashtags (update regularly)
        self.trending_hashtags = [
            "fyp", "foryou", "viral", "trending", "tiktok", "funny", "dance",
            "comedy", "food", "fashion", "beauty", "fitness", "travel", "music"
        ]

        # Optimal hours by day (based on studies)
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
        """Generate variations of a base scenario"""
        variations = []

        # Variation 1: Optimal hours
        for hour in self.optimal_hours.get(base_scenario.publication_day.lower(), [9, 12, 18, 21]):
            variation = base_scenario.copy()
            variation.name = f"{base_scenario.name}_optimal_hour_{hour}"
            variation.description = f"{base_scenario.description} - Optimal hour: {hour}h"
            variation.publication_hour = hour
            variations.append(variation)

        # Variation 2: Trending hashtags
        if base_scenario.trending_hashtags:
            variation = base_scenario.copy()
            variation.name = f"{base_scenario.name}_trending_hashtags"
            variation.description = f"{base_scenario.description} - With trending hashtags"
            variation.hashtags = base_scenario.hashtags + \
                random.sample(self.trending_hashtags, 3)
            variations.append(variation)

        # Variation 3: Engagement boost
        variation = base_scenario.copy()
        variation.name = f"{base_scenario.name}_engagement_boost"
        variation.description = f"{base_scenario.description} - Engagement boost"
        variation.engagement_multiplier = 1.5
        variation.reach_multiplier = 1.3
        variations.append(variation)

        return variations

    def create_pre_publication_features(self, video_data: Dict[str, Any], scenario: SimulationScenario) -> Dict[str, Any]:
        """Create pre-publication features without using real engagement data"""

        # Start with basic content features (no engagement data)
        pre_publication_features = {
            # Content features (from video analysis)
            "video_duration": video_data.get("duration", scenario.video_length),
            "estimated_hashtag_count": len(scenario.hashtags),
            "video_length": scenario.video_length,

            # Publication timing features
            "publication_hour": scenario.publication_hour,
            "publication_day_factor": self._calculate_day_factor(scenario.publication_day),
            "hour_factor": self._calculate_hour_factor(scenario.publication_hour),

            # Content quality features
            "has_text_overlays": scenario.has_text_overlays,
            "has_transitions": scenario.has_transitions,
            "has_call_to_action": scenario.has_call_to_action,

            # Hashtag strategy
            "hashtag_virality_score": self._calculate_hashtag_score(scenario.hashtags),
            "trending_hashtag_count": len([h for h in scenario.hashtags if h.lower() in [t.lower() for t in self.trending_hashtags]]),

            # Engagement multipliers
            "engagement_multiplier": scenario.engagement_multiplier,
            "reach_multiplier": scenario.reach_multiplier,

            # Pre-publication content features (no real engagement)
            "audience_connection_score": 0.7,  # Simulated
            "color_vibrancy": 0.8,  # Simulated
            "music_energy": 0.75,  # Simulated
            "emotional_trigger_count": 3,  # Simulated
            "video_duration_optimized": 1.0 if 15 <= scenario.video_length <= 60 else 0.8,
            "viral_potential_score": 0.65,  # Simulated
            "production_quality_score": 0.8  # Simulated
        }

        return pre_publication_features

    def _calculate_day_factor(self, day: str) -> float:
        """Calculate optimal day factor"""
        # Weekends are generally better for entertainment content
        weekend_days = ["saturday", "sunday"]
        if day.lower() in weekend_days:
            return 1.3  # 30% boost
        else:
            return 1.0  # Normal

    def _calculate_hour_factor(self, hour: int) -> float:
        """Calculate optimal hour factor"""
        # Peak hours: 9h, 12h, 18h, 21h
        peak_hours = [9, 12, 18, 21]

        if hour in peak_hours:
            return 1.5  # 50% boost
        elif hour in [10, 11, 13, 14, 19, 20, 22]:
            return 1.2  # 20% boost
        else:
            return 0.8  # 20% reduction

    def _calculate_hashtag_score(self, hashtags: List[str]) -> float:
        """Calculate hashtag virality score"""
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

        # Bonus for optimal hashtag count (3-5)
        if 3 <= len(hashtags) <= 5:
            score += 0.2

        # Bonus for trending hashtags
        if trending_count >= 2:
            score += 0.3

        return min(score, 1.0)

    def generate_recommendations(self, scenario: SimulationScenario, scores: List[float]) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        avg_score = sum(scores) / len(scores)

        # Timing recommendations
        if scenario.publication_hour not in self.optimal_hours.get(scenario.publication_day.lower(), []):
            recommendations.append(
                f"Publish at optimal hours: {', '.join(map(str, self.optimal_hours.get(scenario.publication_day.lower(), [9, 12, 18, 21])))}h")

        # Hashtag recommendations
        if len(scenario.hashtags) < 3:
            recommendations.append(
                "Add more hashtags (3-5 recommended)")
        elif len(scenario.hashtags) > 5:
            recommendations.append(
                "Reduce hashtag count (3-5 recommended)")

        # Content recommendations
        if not scenario.has_call_to_action:
            recommendations.append(
                "Add call-to-action to increase engagement")

        if not scenario.has_text_overlays:
            recommendations.append(
                "Add text overlays to improve retention")

        if avg_score < 0.6:
            recommendations.append(
                "Consider content redesign to improve virality")

        return recommendations

    async def run_simulation(self, request: SimulationRequest) -> SimulationResponse:
        """Run complete pre-publication simulation"""

        # Get video data for content analysis only (not engagement)
        video_data = None
        cache_used = False

        if request.use_cache:
            cached_data = await self.tiktok_scraper_integration.get_cached_video_data(request.video_url)
            if cached_data:
                video_data = cached_data
                cache_used = True
            else:
                # Fetch video data for content analysis only
                video_data = await self.tiktok_scraper_integration.get_video_data_from_url(request.video_url)
                # Cache the data
                await self.tiktok_scraper_integration.cache_video_data(request.video_url, video_data)
        else:
            # Always fetch fresh data
            video_data = await self.tiktok_scraper_integration.get_video_data_from_url(request.video_url)

        if not video_data:
            raise ValueError(f"Cannot analyze video: {request.video_url}")

        # Create base pre-publication features (no engagement data)
        base_features = self.create_pre_publication_features(video_data, SimulationScenario(
            name="base",
            description="Base scenario",
            publication_hour=12,
            publication_day="monday",
            hashtags=[],
            video_length=video_data.get("duration", 30)
        ))

        # Calculate base score (pre-publication)
        base_score = self.ml_manager.predict(base_features)['virality_score']

        results = []
        best_scenario = None
        best_score = 0.0

        # Test each scenario
        for scenario in request.scenarios:
            scenario_results = []

            # Generate scenario variations
            variations = self.generate_scenario_variations(scenario)

            for variation in variations:
                for i in range(request.simulation_count):
                    # Create pre-publication features for this scenario
                    simulated_features = self.create_pre_publication_features(
                        video_data, variation)

                    # Predict virality
                    virality_score = self.ml_manager.predict(
                        simulated_features)['virality_score']

                    # Add noise for variance
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

            # Calculate scenario statistics
            scores = [r["virality_score"] for r in scenario_results]
            avg_score = sum(scores) / len(scores)

            if avg_score > best_score:
                best_score = avg_score
                best_scenario = scenario.name

            # Generate recommendations
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

        # Summary
        summary = {
            "total_simulations": len(request.scenarios) * request.simulation_count,
            "scenarios_tested": len(request.scenarios),
            "improvement_potential": best_score - base_score,
            "recommendations_count": sum(len(r.recommendations) for r in results),
            "cache_used": cache_used,
            "simulation_type": "pre_publication"
        }

        return SimulationResponse(
            video_url=request.video_url,
            base_virality_score=base_score,
            scenarios=results,
            best_scenario=best_scenario or "None",
            best_score=best_score,
            summary=summary
        )

    async def simulate_virality(self, request: SimulationRequest) -> SimulationResponse:
        """Simulate virality prediction with different parameters"""
        return await self.run_simulation(request)
