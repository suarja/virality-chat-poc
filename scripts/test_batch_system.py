#!/usr/bin/env python3
"""
Test script for batch processing system.
"""
from src.utils.batch_tracker import BatchTracker
import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_batch_tracker():
    """Test the batch tracker functionality."""
    print("🧪 Testing Batch Tracker System...")

    # Initialize tracker for test dataset
    tracker = BatchTracker("test")

    # Test accounts
    test_accounts = ["@test1", "@test2", "@test3", "@test4", "@test5"]

    print(f"📋 Test accounts: {test_accounts}")

    # Test 1: Get next batch
    print("\n1️⃣ Testing get_next_batch...")
    batch = tracker.get_next_batch(test_accounts, 3)
    print(f"   First batch: {batch}")

    # Test 2: Mark accounts as processed
    print("\n2️⃣ Testing mark_account_processed...")
    for account in batch:
        tracker.mark_account_processed(account)

    # Test 3: Get next batch (should skip processed accounts)
    print("\n3️⃣ Testing get_next_batch after processing...")
    next_batch = tracker.get_next_batch(test_accounts, 3)
    print(f"   Next batch: {next_batch}")

    # Test 4: Log some errors
    print("\n4️⃣ Testing error logging...")
    tracker.log_error("@test1", "scraping", "API rate limit exceeded")
    tracker.log_error("@test2", "analysis", "Video not found")

    # Test 5: Get failed accounts
    print("\n5️⃣ Testing get_failed_accounts...")
    failed = tracker.get_failed_accounts()
    print(f"   Failed accounts: {failed}")

    # Test 6: Get summary
    print("\n6️⃣ Testing summarize_progress...")
    summary = tracker.summarize_progress()
    print(f"   Summary: {summary}")

    print("\n✅ Batch tracker tests completed!")


def test_directory_structure():
    """Test that the correct directory structure is created."""
    print("\n📁 Testing directory structure...")

    dataset_dir = Path("data/dataset_test")
    source_file = dataset_dir / "source.txt"
    errors_file = dataset_dir / "errors.txt"

    print(f"   Dataset directory: {dataset_dir.exists()}")
    print(f"   Source file: {source_file.exists()}")
    print(f"   Errors file: {errors_file.exists()}")

    if source_file.exists():
        with open(source_file) as f:
            processed = f.read().strip().split('\n') if f.read().strip() else []
        print(f"   Processed accounts: {processed}")

    if errors_file.exists():
        with open(errors_file) as f:
            errors = f.read().strip().split('\n') if f.read().strip() else []
        print(f"   Error entries: {len(errors)}")


def cleanup_test_data():
    """Clean up test data."""
    print("\n🧹 Cleaning up test data...")

    test_dir = Path("data/dataset_test")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
        print("   Test directory removed")

    # Also clean up any test logs
    test_log = Path("logs/pipeline_test.log")
    if test_log.exists():
        test_log.unlink()
        print("   Test log removed")


if __name__ == "__main__":
    try:
        test_batch_tracker()
        test_directory_structure()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    finally:
        cleanup_test_data()
