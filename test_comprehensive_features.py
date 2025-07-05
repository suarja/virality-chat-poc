#!/usr/bin/env python3
"""
Test script for the Comprehensive Feature Extractor
"""

from src.features.comprehensive_feature_extractor import ComprehensiveFeatureExtractor
import sys
from pathlib import Path
import json
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def create_mock_video_data():
    """Crée des données vidéo mock pour les tests."""
    return {
        'id': 'test_video_123',
        'title': 'Test TikTok Video',
        'description': 'This is a test video with #test #viral #content',
        'duration': 25.5,
        'createTimeISO': '2025-01-15T20:30:00Z',
        'playCount': 15000,
        'diggCount': 1200,
        'commentCount': 150,
        'shareCount': 80,
        'hashtags': [
            {'name': 'test'},
            {'name': 'viral'},
            {'name': 'content'},
            {'name': 'trending'}
        ],
        'musicMeta': {
            'musicName': 'Trending Song',
            'musicAuthor': 'Popular Artist'
        }
    }


def create_mock_gemini_analysis():
    """Crée une analyse Gemini mock pour les tests."""
    return {
        'visual_analysis': {
            'human_presence': 'One person visible with clear eye contact',
            'shot_type': 'Medium close-up shot',
            'color_analysis': 'Vibrant and saturated colors throughout',
            'depth_analysis': 'Shallow depth of field with blurred background',
            'text_overlays': 'No text overlays detected',
            'transitions': 'Smooth transitions between scenes',
            'style_quality': 'High quality production'
        },
        'content_structure': {
            'hook_effectiveness': 'Effective hook in first 3 seconds',
            'story_flow': 'Clear story progression',
            'call_to_action': 'No explicit call to action'
        },
        'engagement_factors': {
            'viral_potential': 'High viral potential',
            'emotional_triggers': 'humor, surprise, relatability',
            'audience_connection': 'Strong audience connection'
        },
        'technical_elements': {
            'length_optimization': 'Appropriate length for platform',
            'sound_design': 'High quality audio',
            'production_quality': 'High production value'
        },
        'trend_alignment': {
            'current_trends': 'Perfectly aligned with current trends',
            'hashtag_potential': '#trending #viral #content'
        }
    }


def test_phase1_features():
    """Test l'extraction des features Phase 1."""
    print("🧪 Testing Phase 1 Features...")

    extractor = ComprehensiveFeatureExtractor()
    video_data = create_mock_video_data()
    gemini_analysis = create_mock_gemini_analysis()

    features = extractor.extract_phase1_features(video_data, gemini_analysis)

    print(f"✅ Extracted {len(features)} Phase 1 features:")
    for name, value in features.items():
        print(f"  • {name}: {value}")

    return features


def test_phase2_features():
    """Test l'extraction des features Phase 2."""
    print("\n🧪 Testing Phase 2 Features...")

    extractor = ComprehensiveFeatureExtractor()
    video_data = create_mock_video_data()
    gemini_analysis = create_mock_gemini_analysis()

    features = extractor.extract_phase2_features(video_data, gemini_analysis)

    print(f"✅ Extracted {len(features)} Phase 2 features:")
    for name, value in features.items():
        print(f"  • {name}: {value}")

    return features


def test_phase3_features():
    """Test l'extraction des features Phase 3."""
    print("\n🧪 Testing Phase 3 Features...")

    extractor = ComprehensiveFeatureExtractor()
    video_data = create_mock_video_data()
    gemini_analysis = create_mock_gemini_analysis()

    features = extractor.extract_phase3_features(video_data, gemini_analysis)

    print(f"✅ Extracted {len(features)} Phase 3 features:")
    for name, value in features.items():
        print(f"  • {name}: {value}")

    return features


def test_comprehensive_extraction():
    """Test l'extraction complète de toutes les features."""
    print("\n🧪 Testing Comprehensive Feature Extraction...")

    extractor = ComprehensiveFeatureExtractor()
    video_data = create_mock_video_data()
    gemini_analysis = create_mock_gemini_analysis()

    # Test extraction complète
    all_features = extractor.extract_all_features(video_data, gemini_analysis)

    print(f"✅ Extracted {len(all_features)} total features")
    print(
        f"📊 Extraction time: {extractor.extraction_stats['extraction_time']:.2f}s")

    if extractor.extraction_stats['errors']:
        print("⚠️ Errors encountered:")
        for error in extractor.extraction_stats['errors']:
            print(f"  • {error}")

    return all_features


def test_feature_summary():
    """Test le résumé des features."""
    print("\n📊 Feature Summary:")

    extractor = ComprehensiveFeatureExtractor()
    summary = extractor.get_feature_summary()

    print(f"Total features defined: {summary['total_features_defined']}")
    print(f"Research-based features: {summary['research_based_features']}")
    print(f"Actionable features: {summary['actionable_features']}")

    print("\nFeatures by Category:")
    for category, count in summary['features_by_category'].items():
        print(f"  • {category}: {count}")

    print("\nFeatures by Complexity:")
    for complexity, count in summary['features_by_complexity'].items():
        print(f"  • {complexity}: {count}")


def test_phased_extraction():
    """Test l'extraction par phases."""
    print("\n🧪 Testing Phased Extraction...")

    extractor = ComprehensiveFeatureExtractor()
    video_data = create_mock_video_data()
    gemini_analysis = create_mock_gemini_analysis()

    # Test Phase 1 seulement
    phase1_only = extractor.extract_all_features(
        video_data, gemini_analysis, phases=[1])
    print(f"Phase 1 only: {len(phase1_only)} features")

    # Test Phase 1 + 2
    phase1_2 = extractor.extract_all_features(
        video_data, gemini_analysis, phases=[1, 2])
    print(f"Phase 1+2: {len(phase1_2)} features")

    # Test toutes les phases
    all_phases = extractor.extract_all_features(
        video_data, gemini_analysis, phases=[1, 2, 3])
    print(f"All phases: {len(all_phases)} features")


def save_test_results(features: dict, filename: str):
    """Sauvegarde les résultats de test."""
    output_dir = Path("test_results")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename
    with open(output_path, 'w') as f:
        json.dump(features, f, indent=2, default=str)

    print(f"💾 Test results saved to {output_path}")


def main():
    """Fonction principale de test."""
    print("🎯 Comprehensive Feature Extractor - Test Suite")
    print("=" * 60)

    try:
        # Test des phases individuelles
        phase1_features = test_phase1_features()
        phase2_features = test_phase2_features()
        phase3_features = test_phase3_features()

        # Test de l'extraction complète
        all_features = test_comprehensive_extraction()

        # Test du résumé
        test_feature_summary()

        # Test de l'extraction par phases
        test_phased_extraction()

        # Sauvegarde des résultats
        save_test_results(all_features, "comprehensive_features_test.json")

        print("\n✅ All tests completed successfully!")

        # Statistiques finales
        print(f"\n📈 Final Statistics:")
        print(f"• Phase 1 features: {len(phase1_features)}")
        print(f"• Phase 2 features: {len(phase2_features)}")
        print(f"• Phase 3 features: {len(phase3_features)}")
        print(f"• Total features: {len(all_features)}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
