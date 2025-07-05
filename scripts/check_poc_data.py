#!/usr/bin/env python3
"""
Script simple pour vérifier les données du POC sans dépendances externes.
"""
import json
import csv
from pathlib import Path
import argparse
import logging


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def check_dataset_structure(dataset_dir: str):
    """Vérifie la structure du dataset."""
    logger = logging.getLogger(__name__)

    dataset_path = Path(dataset_dir)

    print("\n" + "="*60)
    print("📁 VÉRIFICATION DE LA STRUCTURE DU DATASET")
    print("="*60)

    # Vérifier les fichiers batch
    batch_files = list(dataset_path.glob("batch_*.json"))
    print(f"\n📦 FICHIERS BATCH ({len(batch_files)}):")
    for batch_file in batch_files:
        size_kb = batch_file.stat().st_size / 1024
        print(f"   • {batch_file.name} ({size_kb:.1f} KB)")

        # Analyser le contenu
        try:
            with open(batch_file, 'r') as f:
                data = json.load(f)
                videos_count = len(data.get('videos', []))
                accounts = data.get('accounts', [])
                print(
                    f"     - {videos_count} vidéos de {len(accounts)} comptes")
        except Exception as e:
            print(f"     - Erreur lecture: {e}")

    # Vérifier les analyses Gemini
    gemini_dir = dataset_path / "gemini_analysis"
    if gemini_dir.exists():
        analysis_dirs = list(gemini_dir.iterdir())
        print(f"\n🧠 ANALYSES GEMINI ({len(analysis_dirs)} comptes):")
        for account_dir in analysis_dirs:
            if account_dir.is_dir():
                date_dirs = list(account_dir.iterdir())
                total_analyses = 0
                for date_dir in date_dirs:
                    if date_dir.is_dir():
                        analyses = list(date_dir.glob("video_*_analysis.json"))
                        total_analyses += len(analyses)
                print(f"   • {account_dir.name}: {total_analyses} analyses")

    # Vérifier les features
    features_dir = dataset_path / "features"
    if features_dir.exists():
        feature_files = list(features_dir.glob("*_features_*.csv"))
        print(f"\n🔧 FEATURES ({len(feature_files)} fichiers):")

        # Grouper par feature set
        feature_sets = {}
        for file_path in feature_files:
            parts = file_path.stem.split('_features_')
            if len(parts) == 2:
                account = parts[0]
                feature_set = parts[1]
                if feature_set not in feature_sets:
                    feature_sets[feature_set] = []
                feature_sets[feature_set].append(account)

        for feature_set, accounts in feature_sets.items():
            print(
                f"   • {feature_set}: {len(accounts)} comptes ({', '.join(accounts)})")

            # Analyser un fichier pour voir les features
            sample_file = features_dir / \
                f"{accounts[0]}_features_{feature_set}.csv"
            if sample_file.exists():
                try:
                    with open(sample_file, 'r') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        row_count = sum(1 for row in reader)
                    print(
                        f"     - {row_count} vidéos, {len(headers)} features")
                    print(f"     - Exemples: {', '.join(headers[:5])}...")
                except Exception as e:
                    print(f"     - Erreur lecture: {e}")


def aggregate_features_simple(dataset_dir: str, feature_set: str = 'comprehensive'):
    """Agrège les features de manière simple."""
    logger = logging.getLogger(__name__)

    features_dir = Path(dataset_dir) / "features"
    aggregated_file = features_dir / f"aggregated_{feature_set}.csv"

    # Vérifier si l'agrégation existe déjà
    if aggregated_file.exists():
        logger.info(f"Fichier agrégé existant: {aggregated_file}")
        return aggregated_file

    # Chercher les fichiers de features
    feature_files = list(features_dir.glob(f"*_features_{feature_set}.csv"))

    if not feature_files:
        logger.error(f"Aucun fichier de features trouvé pour {feature_set}")
        return None

    logger.info(f"Agrégation de {len(feature_files)} fichiers...")

    # Lire le premier fichier pour obtenir les headers
    with open(feature_files[0], 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)

    # Ajouter la colonne account_name si elle n'existe pas
    if 'account_name' not in headers:
        headers.append('account_name')

    # Créer le fichier agrégé
    with open(aggregated_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        # Concaténer tous les fichiers
        for file_path in feature_files:
            account_name = file_path.stem.replace(
                f'_features_{feature_set}', '')
            logger.info(f"Agrégation de {account_name}")

            with open(file_path, 'r') as source_f:
                reader = csv.reader(source_f)
                source_headers = next(reader)  # Skip header

                for row in reader:
                    # Ajouter le nom du compte
                    if len(row) < len(headers) - 1:
                        row.extend([''] * (len(headers) - 1 - len(row)))
                    row.append(account_name)
                    writer.writerow(row)

    logger.info(f"✅ Features agrégées dans {aggregated_file}")
    return aggregated_file


def analyze_aggregated_data(aggregated_file: Path):
    """Analyse simple des données agrégées."""
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("📊 ANALYSE DES DONNÉES AGRÉGÉES")
    print("="*60)

    try:
        with open(aggregated_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)

            # Compter les lignes
            rows = list(reader)
            row_count = len(rows)

            print(f"\n📈 MÉTRIQUES DE BASE:")
            print(f"   • Nombre de vidéos: {row_count}")
            print(f"   • Nombre de features: {len(headers)}")

            # Analyser les comptes
            account_col_idx = headers.index(
                'account_name') if 'account_name' in headers else -1
            if account_col_idx >= 0:
                accounts = set(row[account_col_idx]
                               for row in rows if len(row) > account_col_idx)
                print(f"   • Nombre de comptes: {len(accounts)}")
                print(f"   • Comptes: {', '.join(accounts)}")

                # Compter par compte
                account_counts = {}
                for row in rows:
                    if len(row) > account_col_idx:
                        account = row[account_col_idx]
                        account_counts[account] = account_counts.get(
                            account, 0) + 1

                print(f"\n📱 VIDÉOS PAR COMPTE:")
                for account, count in account_counts.items():
                    print(f"   • {account}: {count} vidéos")

            # Analyser les features
            print(f"\n🔧 FEATURES DISPONIBLES:")
            feature_headers = [h for h in headers if h not in [
                'video_id', 'account_name']]
            for i, feature in enumerate(feature_headers[:15], 1):
                print(f"   {i:2d}. {feature}")

            if len(feature_headers) > 15:
                print(f"   ... et {len(feature_headers) - 15} autres")

            # Chercher les colonnes de vues
            view_columns = [h for h in headers if 'view' in h.lower()]
            if view_columns:
                print(f"\n👀 COLONNES DE VUES TROUVÉES:")
                for col in view_columns:
                    print(f"   • {col}")

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Vérification simple des données du POC"
    )

    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="Chemin vers le dossier du dataset"
    )

    parser.add_argument(
        "--feature-set",
        type=str,
        default='comprehensive',
        help="Feature set à analyser"
    )

    parser.add_argument(
        "--aggregate",
        action="store_true",
        help="Agréger les features"
    )

    args = parser.parse_args()
    logger = setup_logging()

    try:
        # Vérifier la structure
        check_dataset_structure(args.dataset_dir)

        # Agrégation si demandée
        if args.aggregate:
            aggregated_file = aggregate_features_simple(
                args.dataset_dir, args.feature_set)
            if aggregated_file:
                analyze_aggregated_data(aggregated_file)

        print("\n" + "="*60)
        print("✅ VÉRIFICATION TERMINÉE")
        print("="*60)
        print("🎯 Prochaines étapes:")
        print("   1. Installer les dépendances: pip install pandas numpy scikit-learn")
        print("   2. Analyser avec: python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test")
        print("   3. Créer un modèle baseline")

    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
