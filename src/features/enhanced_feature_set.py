#!/usr/bin/env python3
"""
🆕 Enhanced Feature Set

🎯 New quality-based features to improve viral prediction
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from .modular_feature_system import BaseFeatureSet


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
