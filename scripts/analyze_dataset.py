#!/usr/bin/env python3
"""
📊 Dataset Analysis Script - ITER_004

🎯 Analyze the current dataset situation and provide recommendations for ITER_004

📋 **Fonctionnalités**:
- Analyse de la taille et qualité du dataset actuel
- Évaluation de la diversité des comptes
- Analyse des corrélations avec les vues
- Recommandations pour ITER_004
- Comparaison avec les objectifs

🔧 **Utilisation**:
```bash
# Analyse du dataset nettoyé
python scripts/analyze_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv

# Analyse avec recommandations détaillées
python scripts/analyze_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --detailed

# Analyse comparative
python scripts/analyze_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --compare data/dataset_test_randomization/features/aggregated_comprehensive.csv
```

📊 **Situation Actuelle ITER_002**:
- Dataset nettoyé: 20 vidéos (2 comptes)
- Problèmes identifiés: Manque de diversité, corrélations faibles
- Objectif ITER_004: 100+ vidéos de 10+ comptes diversifiés
"""
import pandas as pd
import numpy as np
import argparse
import os
from pathlib import Path
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


def analyze_iter_004_situation(df, detailed=False):
    """Analyze the current situation for ITER_004"""

    print("🎯 ITER_004 Dataset Analysis")
    print("=" * 50)

    # Basic statistics
    print(f"\n📊 Basic Statistics:")
    print(f"  Total videos: {len(df)}")
    print(f"  Unique accounts: {df['account_name'].nunique()}")
    print(f"  Features: {len(df.columns)}")
    print(
        f"  View count range: {df['view_count'].min():,.0f} - {df['view_count'].max():,.0f}")
    print(f"  Average views: {df['view_count'].mean():,.0f}")

    # Account distribution
    print(f"\n👥 Account Distribution:")
    account_counts = df['account_name'].value_counts()
    for account, count in account_counts.items():
        avg_views = df[df['account_name'] == account]['view_count'].mean()
        print(f"  {account}: {count} videos (avg: {avg_views:,.0f} views)")

    # Feature correlation analysis
    print(f"\n🎯 Feature Correlation with View Count:")
    key_features = [
        'duration', 'hashtag_count', 'hour_of_day', 'day_of_week',
        'video_duration_optimized', 'viral_potential_score',
        'audience_connection_score', 'emotional_trigger_count',
        'like_count', 'comment_count', 'share_count'
    ]

    correlations = {}
    for feature in key_features:
        if feature in df.columns:
            corr = df[feature].corr(df['view_count'])
            correlations[feature] = corr
            if not pd.isna(corr):
                print(f"  {feature}: {corr:.3f}")
            else:
                print(f"  {feature}: NaN (no correlation)")

    # ITER_004 recommendations
    print(f"\n🚀 ITER_004 Recommendations:")

    # Current problems
    print(f"\n❌ Current Problems:")
    if len(df) < 50:
        print(f"  - Dataset too small ({len(df)} videos, need 100+)")
    if df['account_name'].nunique() < 5:
        print(
            f"  - Too few accounts ({df['account_name'].nunique()}, need 10+)")

    # Check correlations
    strong_correlations = [
        f for f, c in correlations.items() if not pd.isna(c) and abs(c) > 0.3]
    if len(strong_correlations) < 3:
        print(
            f"  - Weak feature correlations (only {len(strong_correlations)} strong correlations)")

    # Recommendations
    print(f"\n✅ Recommendations:")
    print(f"  - Collect 100+ videos from 10+ diverse accounts")
    print(f"  - Use randomization to avoid bias")
    print(f"  - Focus on accounts from different categories")
    print(f"  - Implement enhanced feature engineering")
    print(f"  - Use stratified cross-validation")

    # Data collection plan
    print(f"\n📋 Data Collection Plan:")
    print(f"  - Target: 150 videos from 15 accounts")
    print(f"  - Categories: Lifestyle, Tech, Food, Gaming, Humor, Travel")
    print(f"  - Videos per account: 10 (balanced)")
    print(f"  - Use: python scripts/run_pipeline.py --dataset iter_004_diverse --enable-diversity --max-accounts 15")

    if detailed:
        # Detailed analysis
        print(f"\n🔍 Detailed Analysis:")

        # View count distribution
        print(f"\n📈 View Count Distribution:")
        print(df['view_count'].describe())

        # Account performance
        print(f"\n🏆 Account Performance:")
        account_performance = df.groupby('account_name').agg({
            'view_count': ['count', 'mean', 'std', 'min', 'max'],
            'like_count': ['mean'],
            'comment_count': ['mean']
        }).round(0)
        print(account_performance)

        # Feature importance analysis
        print(f"\n🎯 Top Feature Correlations:")
        sorted_correlations = sorted(correlations.items(), key=lambda x: abs(
            x[1]) if not pd.isna(x[1]) else 0, reverse=True)
        for feature, corr in sorted_correlations[:10]:
            if not pd.isna(corr):
                print(f"  {feature}: {corr:.3f}")

    return correlations


def analyze_duplication_patterns(df):
    """Analyze duplication patterns in the dataset"""

    print("🔍 Duplication Pattern Analysis")
    print("=" * 50)

    # Basic duplication stats
    total_videos = len(df)
    unique_videos = df['video_id'].nunique()
    duplicates = df.duplicated(subset=['video_id']).sum()

    print(f"📊 Basic Stats:")
    print(f"  Total videos: {total_videos}")
    print(f"  Unique video IDs: {unique_videos}")
    print(f"  Duplicates: {duplicates}")
    print(f"  Duplication rate: {(duplicates/total_videos)*100:.1f}%")

    # Account distribution
    print(f"\n👥 Account Distribution:")
    account_counts = df['account_name'].value_counts()
    for account, count in account_counts.items():
        print(f"  {account}: {count} videos")

    # Find most duplicated videos
    print(f"\n🎬 Most Duplicated Videos:")
    video_counts = df['video_id'].value_counts()
    most_duplicated = video_counts[video_counts > 1].head(5)

    for video_id, count in most_duplicated.items():
        accounts = df[df['video_id'] == video_id]['account_name'].unique()
        print(f"  Video {video_id}: {count} times, accounts: {list(accounts)}")

    # Analyze by account
    print(f"\n📋 Duplication by Account:")
    for account in df['account_name'].unique():
        account_videos = df[df['account_name'] == account]
        account_unique = account_videos['video_id'].nunique()
        account_total = len(account_videos)
        duplication_rate = ((account_total - account_unique) /
                            account_total) * 100 if account_total > 0 else 0

        print(
            f"  {account}: {account_total} total, {account_unique} unique ({duplication_rate:.1f}% duplication)")

    return {
        'total_videos': total_videos,
        'unique_videos': unique_videos,
        'duplicates': duplicates,
        'duplication_rate': (duplicates/total_videos)*100 if total_videos > 0 else 0
    }


def main():
    parser = argparse.ArgumentParser(
        description='Analyze dataset for ITER_004')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--detailed', action='store_true',
                        help='Detailed analysis')
    parser.add_argument('--compare', help='Compare with another dataset')
    parser.add_argument('--analyze-duplications',
                        action='store_true', help='Analyze duplication patterns')

    args = parser.parse_args()

    # Load dataset
    print(f"📂 Loading dataset: {args.input}")
    df = pd.read_csv(args.input)

    # Analyze duplications if requested
    if args.analyze_duplications:
        duplication_stats = analyze_duplication_patterns(df)
        return

    # Analyze ITER_004 situation
    correlations = analyze_iter_004_situation(df, args.detailed)

    # Compare if requested
    if args.compare:
        print(f"\n🔄 Comparison Analysis:")
        print(f"📂 Loading comparison dataset: {args.compare}")
        df_compare = pd.read_csv(args.compare)

        print(f"\n📊 Comparison Summary:")
        print(
            f"  Current: {len(df)} videos, {df['account_name'].nunique()} accounts")
        print(
            f"  Compare: {len(df_compare)} videos, {df_compare['account_name'].nunique()} accounts")

        # Check for new accounts
        current_accounts = set(df['account_name'].unique())
        compare_accounts = set(df_compare['account_name'].unique())
        new_accounts = compare_accounts - current_accounts

        if new_accounts:
            print(f"\n🆕 New accounts in comparison dataset:")
            for account in new_accounts:
                print(f"  - {account}")
        else:
            print(f"\nℹ️ No new accounts found")


if __name__ == "__main__":
    main()
