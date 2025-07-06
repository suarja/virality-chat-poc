#!/usr/bin/env python3
"""
⚖️ Dataset Balancing Script - ITER_004

🎯 Balance the dataset by diversifying accounts and ensuring better representation

📋 **Fonctionnalités**:
- Équilibrage de la distribution par compte
- Sélection des meilleures vidéos par compte (basé sur vues)
- Analyse de la diversité du dataset
- Génération de rapports de balancement
- Validation de la qualité du dataset équilibré

🔧 **Utilisation**:
```bash
# Équilibrage basique
python scripts/balance_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --output data/dataset_iter_004_clean/balanced_dataset.csv

# Équilibrage avec limite de 10 vidéos par compte
python scripts/balance_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --output data/dataset_iter_004_clean/balanced_dataset.csv --max-videos-per-account 10

# Équilibrage avec comptes cibles spécifiques
python scripts/balance_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --output data/dataset_iter_004_clean/balanced_dataset.csv --target-accounts @swiss_fit.cook @marie29france_ --max-videos-per-account 10

# Équilibrage avec analyse
python scripts/balance_dataset.py --input data/dataset_iter_004_clean/cleaned_dataset.csv --output data/dataset_iter_004_clean/balanced_dataset.csv --max-videos-per-account 10 --analyze
```

📊 **Résultats ITER_002**:
- Dataset nettoyé: 20 vidéos (2 comptes)
- Distribution équilibrée: 10 vidéos par compte
- Problème identifié: Manque de diversité des comptes
- Corrélations faibles avec les vues

🎯 **Objectifs ITER_004**:
- Collecter des données de 10+ comptes différents
- Assurer une représentation équilibrée par catégorie
- Améliorer la qualité des features
- Réduire le biais par compte
"""
import pandas as pd
import numpy as np
import argparse
import os
from pathlib import Path


def balance_dataset(input_file, output_file, target_accounts=None, max_videos_per_account=10):
    """Balance the dataset by diversifying accounts"""

    print("⚖️ Balancing Dataset")
    print("=" * 50)

    # Load cleaned dataset
    print(f"📂 Loading cleaned dataset: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Current shape: {df.shape}")

    # Analyze current distribution
    print(f"\n👥 Current account distribution:")
    current_accounts = df['account_name'].value_counts()
    print(current_accounts)

    # Define target accounts if not provided
    if target_accounts is None:
        # We need to collect data from more diverse accounts
        # For now, we'll work with what we have but plan for expansion
        target_accounts = list(current_accounts.index)
        print(f"\n🎯 Target accounts: {target_accounts}")

    # Balance each account
    print(
        f"\n⚖️ Balancing accounts (max {max_videos_per_account} per account)...")
    balanced_dfs = []

    for account in target_accounts:
        if account in df['account_name'].values:
            account_data = df[df['account_name'] == account]

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
        else:
            print(f"  {account}: No data available")

    # Combine balanced data
    if balanced_dfs:
        df_balanced = pd.concat(balanced_dfs, ignore_index=True)
    else:
        df_balanced = df.copy()

    print(f"\nFinal balanced shape: {df_balanced.shape}")

    # Final account distribution
    print(f"\n👥 Final account distribution:")
    final_account_counts = df_balanced['account_name'].value_counts()
    print(final_account_counts)

    # Save balanced dataset
    print(f"\n💾 Saving balanced dataset: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_balanced.to_csv(output_file, index=False)

    # Generate balancing report
    report_file = output_file.replace('.csv', '_balancing_report.txt')
    with open(report_file, 'w') as f:
        f.write("Dataset Balancing Report\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Input dataset: {df.shape}\n")
        f.write(f"Output dataset: {df_balanced.shape}\n")
        f.write(f"Max videos per account: {max_videos_per_account}\n\n")

        f.write("Account Distribution:\n")
        f.write("-" * 20 + "\n")
        for account, count in final_account_counts.items():
            f.write(f"{account}: {count} videos\n")

        f.write(f"\nTotal unique accounts: {len(final_account_counts)}\n")
        f.write(
            f"Average videos per account: {len(df_balanced)/len(final_account_counts):.1f}\n")

    print(f"📊 Balancing report saved: {report_file}")

    return df_balanced


def analyze_balanced_dataset(df):
    """Analyze the balanced dataset"""

    print("\n📊 Analysis of Balanced Dataset")
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
    print(f"\n🔍 Duplicate videos in balanced dataset: {duplicates}")

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
            if not pd.isna(corr):
                print(f"  {feature}: {corr:.3f}")
            else:
                print(f"  {feature}: NaN (no correlation)")

    # Diversity analysis
    print(f"\n🌍 Diversity Analysis:")
    print(f"  Unique accounts: {df['account_name'].nunique()}")
    print(
        f"  Videos per account (avg): {len(df)/df['account_name'].nunique():.1f}")
    print(
        f"  View count range: {df['view_count'].min():,.0f} - {df['view_count'].max():,.0f}")


def main():
    parser = argparse.ArgumentParser(
        description='Balance the training dataset')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    parser.add_argument('--max-videos-per-account', type=int, default=10,
                        help='Maximum videos per account (default: 10)')
    parser.add_argument('--target-accounts', nargs='+',
                        help='Target accounts to include')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze the balanced dataset')

    args = parser.parse_args()

    # Balance dataset
    df_balanced = balance_dataset(
        args.input, args.output, args.target_accounts, args.max_videos_per_account)

    # Analyze if requested
    if args.analyze:
        analyze_balanced_dataset(df_balanced)


if __name__ == "__main__":
    main()
