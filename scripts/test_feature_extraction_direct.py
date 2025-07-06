#!/usr/bin/env python3
"""
🔍 Direct Feature Extraction Test

🎯 Test feature extraction directly with real data to identify issues
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

# Import after adding path


async def test_feature_extraction():
    """Test feature extraction with real data"""

    print("🔍 Testing Feature Extraction with Real Data")
    print("=" * 60)

    # Test URL
    url = "https://www.tiktok.com/@swarecito/video/7505706702050823446"

    try:
        print("1. Getting video data from TikTok...")
        video_data = await tiktok_scraper_integration.get_video_data_from_url(url)
        print(f"   ✅ Video data retrieved - Keys: {list(video_data.keys())}")
        print(f"   📊 Duration: {video_data.get('duration', 'N/A')}")
        print(f"   📊 Hashtags: {len(video_data.get('hashtags', []))}")
        print(f"   📊 Create time: {video_data.get('createTimeISO', 'N/A')}")

        print("\n2. Getting Gemini analysis...")
        gemini_result = await gemini_service.analyze_video(url, use_cache=False)
        gemini_analysis = None
        if gemini_result and gemini_result.get("success"):
            gemini_analysis = gemini_result.get("analysis")
            print(
                f"   ✅ Gemini analysis retrieved - Keys: {list(gemini_analysis.keys()) if gemini_analysis else 'None'}")
        else:
            print(f"   ⚠️ Gemini analysis failed: {gemini_result}")

        print("\n3. Testing feature extraction...")
        print(f"   🔍 Feature manager available: {feature_manager.available}")
        print(
            f"   🔍 Feature extractor type: {type(feature_manager.feature_extractor)}")

        # Test extraction
        features = await feature_manager.extract_features_from_video_data(video_data, gemini_analysis)

        print(f"   ✅ Features extracted: {len(features)}")
        print(f"   📊 Feature keys: {list(features.keys())}")
        print(f"   📊 Sample features:")
        for key, value in list(features.items())[:5]:
            print(f"     {key}: {value}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_feature_extraction())
