"""
Data processor for combining TikTok data and Gemini analysis
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from .feature_extractor import FeatureExtractor


class DataProcessor:
    """Process and combine TikTok data with Gemini analysis."""

    def __init__(self, feature_extractor: Optional[FeatureExtractor] = None):
        """
        Initialize data processor.

        Args:
            feature_extractor: Optional FeatureExtractor instance
        """
        self.feature_extractor = feature_extractor or FeatureExtractor()

    def load_raw_data(self, raw_data_path: Path) -> Dict:
        """
        Load raw TikTok data.

        Args:
            raw_data_path: Path to raw data JSON file

        Returns:
            Dictionary containing raw data
        """
        with open(raw_data_path, 'r') as f:
            return json.load(f)

    def load_gemini_analysis(self, analysis_dir: Path) -> Dict[str, Dict]:
        """
        Load Gemini analysis files.

        Args:
            analysis_dir: Directory containing analysis JSON files

        Returns:
            Dictionary mapping video IDs to their analysis
        """
        analyses = {}
        for file_path in analysis_dir.glob('video_*_analysis_*.json'):
            with open(file_path, 'r') as f:
                analysis = json.load(f)
                # Extract video ID from analysis and map it
                video_data = analysis.get('analysis', {})
                if video_data:
                    analyses[file_path.stem] = video_data
        return analyses

    def extract_gemini_features(self, analysis: Dict) -> Dict:
        """
        Extract features from Gemini analysis.

        Args:
            analysis: Gemini analysis dictionary

        Returns:
            Dictionary of extracted features
        """
        features = {}

        # Visual Analysis Features
        visual = analysis.get('visual_analysis', {})
        features.update({
            'has_text_overlays': 'no visible text overlays' not in visual.get('text_overlays', '').lower(),
            'has_transitions': 'no noticeable transitions' not in visual.get('transitions', '').lower(),
            'visual_quality_score': self._extract_quality_score(visual.get('style_quality', ''))
        })

        # Content Structure Features
        content = analysis.get('content_structure', {})
        features.update({
            'has_hook': self._assess_hook_effectiveness(content.get('hook_effectiveness', '')),
            'has_story': 'no narrative story' not in content.get('story_flow', '').lower(),
            'has_call_to_action': 'no explicit call to action' not in content.get('call_to_action', '').lower()
        })

        # Engagement Factors
        engagement = analysis.get('engagement_factors', {})
        features.update({
            'viral_potential_score': self._extract_viral_potential(engagement.get('viral_potential', '')),
            'emotional_trigger_count': self._count_emotional_triggers(engagement.get('emotional_triggers', '')),
            'audience_connection_score': self._assess_audience_connection(engagement.get('audience_connection', ''))
        })

        # Technical Elements
        technical = analysis.get('technical_elements', {})
        features.update({
            'length_optimized': 'appropriate' in technical.get('length_optimization', '').lower(),
            'sound_quality_score': self._extract_quality_score(technical.get('sound_design', '')),
            'production_quality_score': self._extract_quality_score(technical.get('production_quality', ''))
        })

        # Trend Alignment
        trends = analysis.get('trend_alignment', {})
        features.update({
            'trend_alignment_score': self._assess_trend_alignment(trends.get('current_trends', '')),
            'estimated_hashtag_count': self._estimate_hashtag_count(trends.get('hashtag_potential', ''))
        })

        return features

    def _extract_quality_score(self, text: str) -> float:
        """Extract quality score from text description."""
        if 'high' in text.lower():
            return 1.0
        elif 'good' in text.lower():
            return 0.8
        elif 'medium' in text.lower() or 'moderate' in text.lower():
            return 0.6
        elif 'low' in text.lower():
            return 0.4
        else:
            return 0.5

    def _assess_hook_effectiveness(self, text: str) -> float:
        """Assess hook effectiveness from description."""
        if 'highly effective' in text.lower():
            return 1.0
        elif 'effective' in text.lower():
            return 0.8
        elif 'moderate' in text.lower():
            return 0.6
        elif 'weak' in text.lower():
            return 0.4
        else:
            return 0.5

    def _extract_viral_potential(self, text: str) -> float:
        """Extract viral potential score from text."""
        if 'high' in text.lower():
            return 1.0
        elif 'moderate to high' in text.lower():
            return 0.8
        elif 'moderate' in text.lower():
            return 0.6
        elif 'low' in text.lower():
            return 0.4
        else:
            return 0.5

    def _count_emotional_triggers(self, text: str) -> int:
        """Count number of emotional triggers mentioned."""
        emotional_keywords = ['joy', 'happiness', 'excitement', 'surprise',
                              'curiosity', 'nostalgia', 'empathy', 'amusement']
        return sum(1 for keyword in emotional_keywords if keyword in text.lower())

    def _assess_audience_connection(self, text: str) -> float:
        """Assess audience connection strength."""
        if 'strong' in text.lower():
            return 1.0
        elif 'good' in text.lower():
            return 0.8
        elif 'moderate' in text.lower():
            return 0.6
        elif 'weak' in text.lower():
            return 0.4
        else:
            return 0.5

    def _assess_trend_alignment(self, text: str) -> float:
        """Assess how well content aligns with trends."""
        if 'perfectly aligns' in text.lower():
            return 1.0
        elif 'aligns' in text.lower():
            return 0.8
        elif 'somewhat aligns' in text.lower():
            return 0.6
        elif 'barely aligns' in text.lower():
            return 0.4
        else:
            return 0.5

    def _estimate_hashtag_count(self, text: str) -> int:
        """Estimate number of hashtags from description."""
        return len([word for word in text.split() if word.startswith('#')])

    def process_video(
        self,
        video_data: Dict,
        gemini_analysis: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        Process a single video, combining TikTok data with Gemini analysis.

        Args:
            video_data: Raw video data dictionary
            gemini_analysis: Optional Gemini analysis dictionary

        Returns:
            Tuple of (combined features dict, metadata dict)
        """
        # Extract basic features
        features, metadata = self.feature_extractor.extract_all_features(
            video_data)

        # Add Gemini analysis features if available
        if gemini_analysis:
            gemini_features = self.extract_gemini_features(gemini_analysis)
            features.update(gemini_features)
            metadata['features_extracted'].append('gemini_analysis')

        return features, metadata

    def process_dataset(
        self,
        raw_data_path: Path,
        gemini_analysis_dir: Path,
        output_dir: Path
    ) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Process entire dataset.

        Args:
            raw_data_path: Path to raw data JSON
            gemini_analysis_dir: Directory containing Gemini analyses
            output_dir: Directory to save processed features

        Returns:
            Tuple of (features DataFrame, list of metadata dicts)
        """
        # Load data
        raw_data = self.load_raw_data(raw_data_path)
        gemini_analyses = self.load_gemini_analysis(gemini_analysis_dir)

        all_features = []
        all_metadata = []

        # Process each video
        for video in raw_data.get('videos', []):
            video_id = video['id']
            gemini_analysis = gemini_analyses.get(f'video_{video_id}_analysis')

            try:
                features, metadata = self.process_video(video, gemini_analysis)
                all_features.append(features)
                all_metadata.append(metadata)
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")
                continue

        # Create DataFrame
        features_df = pd.DataFrame(all_features)

        # Save features
        output_path = output_dir / 'processed_features.csv'
        features_df.to_csv(output_path, index=False)

        return features_df, all_metadata
