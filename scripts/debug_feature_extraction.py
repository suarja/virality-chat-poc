#!/usr/bin/env python3
"""
🔍 Debug Feature Extraction Script

🎯 Debug feature extraction step by step to identify issues
"""
from api.gemini_integration import gemini_service
from api.tiktok_scraper_integration import tiktok_scraper_integration
from api.feature_integration import feature_manager
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))


async def debug_feature_extraction():
    """Debug feature extraction step by step"""

    print("🔍 Debug Feature Extraction")
    print("=" * 50)

    # Test URL
    url = "https://www.tiktok.com/@swarecito/video/7505706702050823446"

    print(f"1. Testing feature manager availability:")
    print(f"   - Available: {feature_manager.available}")
    print(
        f"   - Feature extractor type: {type(feature_manager.feature_extractor)}")
    print(f"   - Feature count: {feature_manager.get_feature_count()}")

    print(f"\n2. Testing TikTok scraper:")
    try:
        video_data = await tiktok_scraper_integration.get_video_data_from_url(url)
        print(f"   - Video data keys: {list(video_data.keys())}")
        print(f"   - Duration: {video_data.get('duration', 'N/A')}")
        print(f"   - Hashtags: {len(video_data.get('hashtags', []))}")
        print(f"   - Create time: {video_data.get('createTimeISO', 'N/A')}")
    except Exception as e:
        print(f"   - Error: {e}")

    print(f"\n3. Testing Gemini analysis:")
    try:
        gemini_result = await gemini_service.analyze_video(url, use_cache=False)
        if gemini_result and gemini_result.get("success"):
            gemini_analysis = gemini_result.get("analysis")
            print(
                f"   - Gemini analysis keys: {list(gemini_analysis.keys()) if gemini_analysis else 'None'}")
        else:
            print(f"   - Gemini analysis failed: {gemini_result}")
    except Exception as e:
        print(f"   - Error: {e}")

    print(f"\n4. Testing feature extraction:")
    try:
        # Get video data
        video_data = await tiktok_scraper_integration.get_video_data_from_url(url)

        # Get Gemini analysis
        gemini_result = await gemini_service.analyze_video(url, use_cache=False)
        gemini_analysis = None
        if gemini_result and gemini_result.get("success"):
            gemini_analysis = gemini_result.get("analysis")

        # Extract features
        features = await feature_manager.extract_features_from_video_data(video_data, gemini_analysis)

        print(f"   - Features extracted: {len(features)}")
        print(f"   - Feature keys: {list(features.keys())}")
        print(f"   - Sample features:")
        for key, value in list(features.items())[:5]:
            print(f"     {key}: {value}")

    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n5. Testing direct feature extractor:")
    try:
        from features.modular_feature_system import create_feature_extractor

        # Create feature extractor directly
        extractor = create_feature_extractor('model_compatible')

        # Test with mock data
        mock_video_data = {
            'id': 'test',
            'videoMeta': {'duration': 30},
            'hashtags': [{'name': 'test'}],
            'createTimeISO': '2025-01-15T20:30:00Z'
        }

        features = extractor.extract_features(mock_video_data)
        print(f"   - Direct extraction features: {len(features)}")
        print(f"   - Direct extraction keys: {list(features.keys())}")

    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_feature_extraction())
