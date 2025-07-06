#!/usr/bin/env python3
"""
🔍 Dataset Analysis Script

🎯 Analyze the training dataset to understand overfitting and model behavior
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_dataset():
    """Analyze the training dataset"""

    print("🔍 Analyzing Training Dataset")
    print("=" * 50)

    # Load dataset
    df = pd.read_csv(
        'data/dataset_iter_002/features/aggregated_comprehensive.csv')

    print(f"Dataset shape: {df.shape}")
    print(f"Accounts: {df['account_name'].unique()}")

    # View count analysis
    print("\n📊 View Count Analysis:")
    print(df['view_count'].describe())

    # Account analysis
    print("\n👥 Account Analysis:")
    account_stats = df.groupby('account_name').agg({
        'view_count': ['count', 'mean', 'min', 'max'],
        'like_count': ['mean'],
        'comment_count': ['mean']
    }).round(0)
    print(account_stats)

    # Check for duplicates
    print(f"\n🔍 Duplicate videos: {df.duplicated(subset=['video_id']).sum()}")

    # Analyze key features
    print("\n🎯 Key Features Analysis:")

    # Features that should correlate with views
    key_features = [
        'duration', 'hashtag_count', 'hour_of_day', 'day_of_week',
        'video_duration_optimized', 'viral_potential_score',
        'audience_connection_score', 'emotional_trigger_count'
    ]

    for feature in key_features:
        if feature in df.columns:
            corr = df[feature].corr(df['view_count'])
            print(f"{feature}: {corr:.3f}")

    # Analyze by view count categories
    print("\n📈 Analysis by View Categories:")

    # High views (>1M)
    high_views = df[df['view_count'] > 1000000]
    print(
        f"High views (>1M): {len(high_views)} videos ({len(high_views)/len(df)*100:.1f}%)")

    # Medium views (10K-1M)
    medium_views = df[(df['view_count'] >= 10000) &
                      (df['view_count'] <= 1000000)]
    print(
        f"Medium views (10K-1M): {len(medium_views)} videos ({len(medium_views)/len(df)*100:.1f}%)")

    # Low views (<10K)
    low_views = df[df['view_count'] < 10000]
    print(
        f"Low views (<10K): {len(low_views)} videos ({len(low_views)/len(df)*100:.1f}%)")

    # Analyze features by view category
    print("\n🔍 Feature Analysis by View Category:")

    for feature in key_features:
        if feature in df.columns:
            print(f"\n{feature}:")
            print(f"  High views: {high_views[feature].mean():.3f}")
            print(f"  Medium views: {medium_views[feature].mean():.3f}")
            print(f"  Low views: {low_views[feature].mean():.3f}")

    # Check for potential issues
    print("\n⚠️ Potential Issues:")

    # Check if all videos from same accounts have similar features
    print("\nAccount Feature Consistency:")
    for account in df['account_name'].unique():
        account_data = df[df['account_name'] == account]
        print(f"\n{account}:")
        for feature in ['duration', 'hashtag_count', 'hour_of_day']:
            if feature in account_data.columns:
                std = account_data[feature].std()
                print(f"  {feature} std: {std:.3f}")

    # Check for feature leakage
    print("\n🔍 Feature Leakage Check:")
    if 'engagement_rate' in df.columns:
        engagement_corr = df['engagement_rate'].corr(df['view_count'])
        print(f"Engagement rate correlation with views: {engagement_corr:.3f}")
        if abs(engagement_corr) > 0.8:
            print("⚠️ HIGH CORRELATION: Potential feature leakage!")

    return df


if __name__ == "__main__":
    df = analyze_dataset()
