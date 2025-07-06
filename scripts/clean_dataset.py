#!/usr/bin/env python3
"""
🧹 Dataset Cleaning Script - ITER_004

🎯 Clean the training dataset by removing duplicates and balancing account distribution

📋 **Fonctionnalités**:
- Suppression des vidéos dupliquées (basé sur video_id)
- Équilibrage de la distribution par compte
- Limitation du nombre de vidéos par compte
- Génération de rapports détaillés
- Analyse des corrélations avec les vues

🔧 **Utilisation**:
```bash
# Nettoyage basique
python scripts/clean_dataset.py --input data/dataset_iter_002/features/aggregated_comprehensive.csv --output data/dataset_iter_004_clean/cleaned_dataset.csv

# Nettoyage avec limite de 10 vidéos par compte
python scripts/clean_dataset.py --input data/dataset_iter_002/features/aggregated_comprehensive.csv --output data/dataset_iter_004_clean/cleaned_dataset.csv --max-videos-per-account 10

# Nettoyage avec analyse
python scripts/clean_dataset.py --input data/dataset_iter_002/features/aggregated_comprehensive.csv --output data/dataset_iter_004_clean/cleaned_dataset.csv --max-videos-per-account 10 --analyze
```

📊 **Résultats ITER_002**:
- Dataset original: 84 vidéos (62% duplications)
- Après nettoyage: 20 vidéos (0% duplications)
- Distribution: 2 comptes équilibrés (10 vidéos chacun)
- Corrélations faibles avec les vues (problème identifié)

🎯 **Objectifs ITER_004**:
- Collecter plus de vidéos de comptes diversifiés
- Améliorer la qualité des features
- Réduire le biais par compte
"""
import pandas as pd
import numpy as np
import argparse
import os
from pathlib import Path


def clean_dataset(input_file, output_file, max_videos_per_account=20):
    """Clean the dataset by removing duplicates and balancing accounts"""

    print("🧹 Cleaning Dataset")
    print("=" * 50)

    # Load dataset
    print(f"📂 Loading dataset: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Original shape: {df.shape}")

    # Check for duplicates
    print(f"\n🔍 Checking for duplicates...")
    duplicates = df.duplicated(subset=['video_id']).sum()
    print(f"Duplicate videos found: {duplicates}")

    # Remove duplicates
    print(f"\n🗑️ Removing duplicates...")
    df_clean = df.drop_duplicates(subset=['video_id'], keep='first')
    print(f"After removing duplicates: {df_clean.shape}")

    # Analyze account distribution
    print(f"\n👥 Account distribution before balancing:")
    account_counts = df_clean['account_name'].value_counts()
    print(account_counts)

    # Balance accounts - LESS RESTRICTIVE
    print(
        f"\n⚖️ Balancing accounts (max {max_videos_per_account} per account)...")
    balanced_dfs = []

    for account in df_clean['account_name'].unique():
        account_data = df_clean[df_clean['account_name'] == account]

        if len(account_data) > max_videos_per_account:
            # Sort by view count and take top videos
            account_data_sorted = account_data.sort_values(
                'view_count', ascending=False)
            account_data_balanced = account_data_sorted.head(
                max_videos_per_account)
            print(
                f"  {account}: {len(account_data)} → {len(account_data_balanced)} videos")
        else:
            account_data_balanced = account_data
            print(f"  {account}: {len(account_data)} videos (kept all)")

        balanced_dfs.append(account_data_balanced)

    # Combine balanced data
    df_balanced = pd.concat(balanced_dfs, ignore_index=True)
    print(f"\nFinal balanced shape: {df_balanced.shape}")

    # Final account distribution
    print(f"\n👥 Account distribution after balancing:")
    final_account_counts = df_balanced['account_name'].value_counts()
    print(final_account_counts)

    # Save cleaned dataset
    print(f"\n💾 Saving cleaned dataset: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_balanced.to_csv(output_file, index=False)

    # Generate cleaning report
    report_file = output_file.replace('.csv', '_cleaning_report.txt')
    with open(report_file, 'w') as f:
        f.write("Dataset Cleaning Report\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Original dataset: {df.shape}\n")
        f.write(f"Duplicates removed: {duplicates}\n")
        f.write(f"After deduplication: {df_clean.shape}\n")
        f.write(f"Final balanced: {df_balanced.shape}\n")
        f.write(f"Videos removed: {len(df) - len(df_balanced)}\n")
        f.write(
            f"Reduction: {((len(df) - len(df_balanced)) / len(df) * 100):.1f}%\n\n")

        f.write("Account Distribution:\n")
        f.write("-" * 20 + "\n")
        for account, count in final_account_counts.items():
            f.write(f"{account}: {count} videos\n")

    print(f"📊 Cleaning report saved: {report_file}")

    return df_balanced


def analyze_cleaned_dataset(df):
    """Analyze the cleaned dataset"""

    print("\n📊 Analysis of Cleaned Dataset")
    print("=" * 40)

    # View count analysis
    print(f"\n📈 View Count Statistics:")
    print(df['view_count'].describe())

    # Account analysis
    print(f"\n👥 Account Analysis:")
    account_stats = df.groupby('account_name').agg({
        'view_count': ['count', 'mean', 'min', 'max'],
        'like_count': ['mean'],
        'comment_count': ['mean']
    }).round(0)
    print(account_stats)

    # Check for duplicates
    duplicates = df.duplicated(subset=['video_id']).sum()
    print(f"\n🔍 Duplicate videos in cleaned dataset: {duplicates}")

    # Feature correlation analysis
    print(f"\n🎯 Feature Correlation with View Count:")
    key_features = [
        'duration', 'hashtag_count', 'hour_of_day', 'day_of_week',
        'video_duration_optimized', 'viral_potential_score',
        'audience_connection_score', 'emotional_trigger_count'
    ]

    for feature in key_features:
        if feature in df.columns:
            corr = df[feature].corr(df['view_count'])
            print(f"  {feature}: {corr:.3f}")


def main():
    parser = argparse.ArgumentParser(description='Clean the training dataset')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    parser.add_argument('--max-videos-per-account', type=int, default=10,
                        help='Maximum videos per account (default: 10)')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze the cleaned dataset')

    args = parser.parse_args()

    # Clean dataset
    df_cleaned = clean_dataset(
        args.input, args.output, args.max_videos_per_account)

    # Analyze if requested
    if args.analyze:
        analyze_cleaned_dataset(df_cleaned)


if __name__ == "__main__":
    main()
