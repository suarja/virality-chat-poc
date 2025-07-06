#!/usr/bin/env python3
"""
🧪 Test New Features Script

🎯 Test the new enhanced quality features on the cleaned dataset
"""
from features.modular_feature_system import create_feature_extractor
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))


def test_new_features():
    """Test the new enhanced features"""

    print("🧪 Testing New Enhanced Features")
    print("=" * 50)

    # Test feature extractor
    print("1. Testing enhanced_quality feature extractor...")
    try:
        extractor = create_feature_extractor("enhanced_quality")
        print(f"✅ Feature extractor created successfully")
        print(f"   Feature sets: {extractor.feature_sets}")
        print(f"   Total features: {extractor.get_feature_count()}")
        print(f"   Feature names: {extractor.get_feature_names()}")
    except Exception as e:
        print(f"❌ Error creating feature extractor: {e}")
        return

    # Test with sample data
    print("\n2. Testing feature extraction with sample data...")

    sample_video_data = {
        'id': 'test_123',
        'videoMeta': {'duration': 25.5},
        'stats': {
            'playCount': 15000,
            'diggCount': 1200,
            'commentCount': 150
        },
        'hashtags': [{'name': 'fyp'}, {'name': 'viral'}, {'name': 'trending'}],
        'authorStats': {
            'followerCount': 50000,
            'videoCount': 100
        },
        'createTimeISO': '2025-01-15T20:30:00Z'
    }

    sample_gemini_analysis = {
        'content_analysis': {
            'is_original': True,
            'creative_technique_count': 3,
            'uses_trending_format': False,
            'is_generic': False,
            'has_hook': True,
            'has_story': True,
            'relatability_score': 0.8,
            'trend_alignment': True
        },
        'emotional_triggers': ['humor', 'surprise'],
        'emotional_intensity': 'high'
    }

    try:
        features = extractor.extract_features(
            sample_video_data, sample_gemini_analysis)
        print(f"✅ Features extracted successfully: {len(features)} features")
        print(f"   Sample features:")
        for feature, value in features.items():
            print(f"     {feature}: {value}")
    except Exception as e:
        print(f"❌ Error extracting features: {e}")

    # Test with cleaned dataset
    print("\n3. Testing with cleaned dataset...")

    try:
        df = pd.read_csv('data/dataset_iter_004_clean/balanced_dataset.csv')
        print(f"✅ Loaded cleaned dataset: {df.shape}")

        # Test with first video
        first_video = df.iloc[0]
        video_data = {
            'id': first_video['video_id'],
            'videoMeta': {'duration': first_video['duration']},
            'stats': {
                'playCount': first_video['view_count'],
                'diggCount': first_video['like_count'],
                'commentCount': first_video['comment_count']
            },
            'hashtags': eval(first_video['hashtags']) if pd.notna(first_video['hashtags']) else [],
            'createTimeISO': '2025-01-15T20:30:00Z'
        }

        features = extractor.extract_features(video_data)
        print(
            f"✅ Features extracted from real video: {len(features)} features")
        print(
            f"   Video: {first_video['video_id']} ({first_video['view_count']} views)")
        print(f"   Sample features:")
        for feature, value in list(features.items())[:5]:
            print(f"     {feature}: {value}")

    except Exception as e:
        print(f"❌ Error testing with cleaned dataset: {e}")


if __name__ == "__main__":
    test_new_features()
