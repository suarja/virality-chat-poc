#!/usr/bin/env python3
"""
Script pour agréger les features de plusieurs comptes en un seul fichier.
Utile pour combiner les résultats du système modulaire.
"""
import pandas as pd
import argparse
import logging
from pathlib import Path
from typing import List, Optional


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def aggregate_features(
    dataset_dir: str,
    feature_set: str,
    output_file: Optional[str] = None,
    add_account_column: bool = True
) -> pd.DataFrame:
    """
    Agréger tous les fichiers de features d'un feature set donné.

    Args:
        dataset_dir: Chemin vers le dossier du dataset
        feature_set: Nom du feature set (metadata, visual_granular, etc.)
        output_file: Fichier de sortie (optionnel)
        add_account_column: Ajouter une colonne avec le nom du compte

    Returns:
        DataFrame avec toutes les features agrégées
    """
    logger = logging.getLogger(__name__)

    # Construire le chemin vers le dossier features
    features_dir = Path(dataset_dir) / "features"

    if not features_dir.exists():
        raise FileNotFoundError(f"Dossier features non trouvé: {features_dir}")

    # Chercher tous les fichiers du feature set
    pattern = f"*_features_{feature_set}.csv"
    feature_files = list(features_dir.glob(pattern))

    if not feature_files:
        raise FileNotFoundError(
            f"Aucun fichier trouvé pour le pattern: {pattern}")

    logger.info(
        f"Trouvé {len(feature_files)} fichiers de features pour {feature_set}")

    all_features = []

    for file_path in feature_files:
        try:
            # Extraire le nom du compte du nom de fichier
            account_name = file_path.stem.split('_features_')[0]

            # Charger les features
            df = pd.read_csv(file_path)

            # Ajouter une colonne avec le nom du compte si demandé
            if add_account_column:
                df['account_name'] = account_name

            all_features.append(df)
            logger.info(f"✅ Chargé {len(df)} features pour {account_name}")

        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement de {file_path}: {e}")
            continue

    if not all_features:
        raise ValueError("Aucune feature chargée avec succès")

    # Combiner tous les DataFrames
    aggregated_df = pd.concat(all_features, ignore_index=True)

    logger.info(
        f"✅ Agrégation terminée: {len(aggregated_df)} features au total")
    logger.info(
        f"   • Comptes: {aggregated_df['account_name'].nunique() if add_account_column else 'N/A'}")
    logger.info(f"   • Colonnes: {len(aggregated_df.columns)}")

    # Sauvegarder si un fichier de sortie est spécifié
    if output_file:
        output_path = Path(output_file)
        aggregated_df.to_csv(output_path, index=False)
        logger.info(f"💾 Features agrégées sauvegardées dans: {output_path}")

    return aggregated_df


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Agréger les features de plusieurs comptes en un seul fichier"
    )

    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="Chemin vers le dossier du dataset (ex: data/dataset_mon_dataset)"
    )

    parser.add_argument(
        "--feature-set",
        type=str,
        required=True,
        choices=['metadata', 'gemini_basic',
                 'visual_granular', 'comprehensive'],
        help="Feature set à agréger"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Fichier de sortie (optionnel, sinon affichage dans la console)"
    )

    parser.add_argument(
        "--no-account-column",
        action="store_true",
        help="Ne pas ajouter de colonne avec le nom du compte"
    )

    parser.add_argument(
        "--show-stats",
        action="store_true",
        help="Afficher les statistiques des features agrégées"
    )

    args = parser.parse_args()
    logger = setup_logging()

    try:
        # Agréger les features
        aggregated_df = aggregate_features(
            dataset_dir=args.dataset_dir,
            feature_set=args.feature_set,
            output_file=args.output,
            add_account_column=not args.no_account_column
        )

        # Afficher les statistiques si demandé
        if args.show_stats:
            logger.info("\n📊 Statistiques des Features Agrégées:")
            logger.info(f"   • Total de features: {len(aggregated_df)}")
            logger.info(f"   • Colonnes: {list(aggregated_df.columns)}")

            if 'account_name' in aggregated_df.columns:
                logger.info(
                    f"   • Comptes uniques: {aggregated_df['account_name'].unique()}")
                logger.info(f"   • Features par compte:")
                for account in aggregated_df['account_name'].unique():
                    count = len(
                        aggregated_df[aggregated_df['account_name'] == account])
                    logger.info(f"     - {account}: {count} features")

        # Afficher un aperçu si pas de fichier de sortie
        if not args.output:
            logger.info("\n👀 Aperçu des Features Agrégées:")
            print(aggregated_df.head())

        logger.info("✅ Agrégation terminée avec succès!")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'agrégation: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
