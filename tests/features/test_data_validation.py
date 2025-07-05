#!/usr/bin/env python3
"""
Test script for data validation guards.
"""
from src.utils.data_validator import DataValidator
import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_validator():
    """Test the data validator with various scenarios."""
    print("🧪 Testing Data Validation Guards...")

    validator = DataValidator()

    # Test 1: Valid video data
    print("\n1️⃣ Testing valid video data...")
    valid_video = {
        'id': '123456789',
        'text': 'This is a test video',
        'playCount': 5000,
        'diggCount': 100,
        'commentCount': 50,
        'shareCount': 25,
        'videoMeta': {'duration': 30},
        'createTimeISO': '2024-12-01T10:00:00Z',
        'webVideoUrl': 'https://www.tiktok.com/@test/video/123456789'
    }

    is_valid, errors = validator.validate_video(valid_video)
    print(f"   Valid video: {is_valid} (errors: {errors})")

    # Test 2: Invalid video (no views)
    print("\n2️⃣ Testing invalid video (low views)...")
    invalid_video = valid_video.copy()
    invalid_video['playCount'] = 500  # Below minimum

    is_valid, errors = validator.validate_video(invalid_video)
    print(f"   Invalid video (low views): {is_valid} (errors: {errors})")

    # Test 3: Invalid video (sponsored content)
    print("\n3️⃣ Testing invalid video (sponsored content)...")
    sponsored_video = valid_video.copy()
    sponsored_video['text'] = 'This is a sponsored video #ad'

    is_valid, errors = validator.validate_video(sponsored_video)
    print(f"   Sponsored video: {is_valid} (errors: {errors})")

    # Test 4: Invalid video (missing fields)
    print("\n4️⃣ Testing invalid video (missing fields)...")
    incomplete_video = {
        'id': '123456789',
        'text': 'Test video'
        # Missing required fields
    }

    is_valid, errors = validator.validate_video(incomplete_video)
    print(f"   Incomplete video: {is_valid} (errors: {errors})")

    # Test 5: Valid account data
    print("\n5️⃣ Testing valid account data...")
    valid_account = {
        'username': 'testuser',
        'videos': [valid_video, valid_video.copy()]
    }

    is_valid, errors = validator.validate_account(valid_account)
    print(f"   Valid account: {is_valid} (errors: {errors})")

    # Test 6: Invalid account (no videos)
    print("\n6️⃣ Testing invalid account (no videos)...")
    empty_account = {
        'username': 'testuser',
        'videos': []
    }

    is_valid, errors = validator.validate_account(empty_account)
    print(f"   Empty account: {is_valid} (errors: {errors})")

    # Test 7: Filter valid videos
    print("\n7️⃣ Testing video filtering...")
    mixed_videos = [valid_video, invalid_video,
                    sponsored_video, incomplete_video]
    valid_videos = validator.filter_valid_videos(mixed_videos)
    print(f"   Filtered videos: {len(valid_videos)}/{len(mixed_videos)} valid")

    # Test 8: Gemini analysis validation
    print("\n8️⃣ Testing Gemini analysis validation...")
    valid_analysis = {
        'success': True,
        'analysis': {
            'visual_elements': 'Good lighting and composition',
            'content_structure': 'Clear narrative flow',
            'engagement_factors': 'Strong hook in first 3 seconds'
        }
    }

    is_valid, errors = validator.validate_gemini_analysis(valid_analysis)
    print(f"   Valid analysis: {is_valid} (errors: {errors})")

    # Test 9: Invalid Gemini analysis
    print("\n9️⃣ Testing invalid Gemini analysis...")
    invalid_analysis = {
        'success': False,
        'analysis': {}
    }

    is_valid, errors = validator.validate_gemini_analysis(invalid_analysis)
    print(f"   Invalid analysis: {is_valid} (errors: {errors})")

    print("\n✅ Data validation tests completed!")


if __name__ == "__main__":
    test_validator()
