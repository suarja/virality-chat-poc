#!/usr/bin/env python3
"""
Script de test pour le pipeline avec agrégation automatique.
Teste le pipeline end-to-end et vérifie que l'agrégation est automatique.
"""
import subprocess
import sys
from pathlib import Path
import logging


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def run_command(command, description):
    """Exécute une commande et log le résultat."""
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 {description}")
    logger.info(f"Commande: {command}")

    try:
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"✅ {description} - Succès")
            if result.stdout:
                logger.info(f"Sortie: {result.stdout.strip()}")
        else:
            logger.error(f"❌ {description} - Échec")
            logger.error(f"Erreur: {result.stderr.strip()}")
            return False

    except Exception as e:
        logger.error(f"❌ {description} - Exception: {e}")
        return False

    return True


def test_pipeline_with_aggregation():
    """Teste le pipeline avec agrégation automatique."""
    logger = logging.getLogger(__name__)

    print("\n" + "="*80)
    print("🚀 TEST PIPELINE AVEC AGRÉGATION AUTOMATIQUE")
    print("="*80)

    # Test 1: Pipeline complet avec agrégation automatique
    logger.info("\n📋 Test 1: Pipeline complet avec agrégation automatique")

    pipeline_cmd = [
        "python3", "scripts/run_pipeline.py",
        "--dataset", "poc_test_aggregation",
        "--batch-size", "1",
        "--videos-per-account", "3",
        "--max-total-videos", "6",
        "--feature-system", "modular",
        "--feature-set", "comprehensive"
    ]

    success = run_command(" ".join(pipeline_cmd), "Pipeline avec agrégation")

    if not success:
        logger.error("❌ Le pipeline a échoué. Arrêt du test.")
        return False

    # Test 2: Vérification de l'agrégation automatique
    logger.info("\n📋 Test 2: Vérification de l'agrégation automatique")

    dataset_dir = Path("data/dataset_poc_test_aggregation")
    features_dir = dataset_dir / "features"
    aggregated_file = features_dir / "aggregated_comprehensive.csv"

    if aggregated_file.exists():
        logger.info(f"✅ Fichier agrégé trouvé: {aggregated_file}")

        # Analyser le fichier agrégé
        try:
            import csv
            with open(aggregated_file, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = list(reader)

            logger.info(f"📊 Contenu du fichier agrégé:")
            logger.info(f"   • Headers: {len(headers)} colonnes")
            logger.info(f"   • Lignes: {len(rows)} vidéos")

            # Vérifier la colonne account_name
            if 'account_name' in headers:
                account_col_idx = headers.index('account_name')
                accounts = set(row[account_col_idx]
                               for row in rows if len(row) > account_col_idx)
                logger.info(f"   • Comptes: {', '.join(accounts)}")

                # Compter par compte
                account_counts = {}
                for row in rows:
                    if len(row) > account_col_idx:
                        account = row[account_col_idx]
                        account_counts[account] = account_counts.get(
                            account, 0) + 1

                logger.info(f"   • Vidéos par compte:")
                for account, count in account_counts.items():
                    logger.info(f"     - {account}: {count} vidéos")

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse du fichier agrégé: {e}")
            return False
    else:
        logger.error(f"❌ Fichier agrégé manquant: {aggregated_file}")
        return False

    # Test 3: Vérification de la structure complète
    logger.info("\n📋 Test 3: Vérification de la structure complète")

    files_to_check = [
        features_dir / "aggregated_comprehensive.csv",
        dataset_dir / "gemini_analysis",
        dataset_dir / "batch_*.json"
    ]

    all_files_exist = True
    for file_pattern in files_to_check:
        if file_pattern.name == "batch_*.json":
            batch_files = list(dataset_dir.glob("batch_*.json"))
            if batch_files:
                logger.info(f"✅ Fichiers batch trouvés: {len(batch_files)}")
            else:
                logger.error(f"❌ Aucun fichier batch trouvé")
                all_files_exist = False
        elif file_pattern.name == "gemini_analysis":
            if file_pattern.exists():
                analysis_dirs = list(file_pattern.iterdir())
                logger.info(
                    f"✅ Dossiers d'analyse trouvés: {len(analysis_dirs)}")
            else:
                logger.error(f"❌ Dossier d'analyse non trouvé")
                all_files_exist = False
        else:
            if file_pattern.exists():
                logger.info(f"✅ Fichier trouvé: {file_pattern}")
            else:
                logger.error(f"❌ Fichier manquant: {file_pattern}")
                all_files_exist = False

    if not all_files_exist:
        logger.error("❌ Certains fichiers sont manquants.")
        return False

    # Test 4: Vérification des features individuelles
    logger.info("\n📋 Test 4: Vérification des features individuelles")

    feature_files = list(features_dir.glob("*_features_comprehensive.csv"))
    if feature_files:
        logger.info(
            f"✅ Fichiers de features individuels trouvés: {len(feature_files)}")
        for file_path in feature_files:
            account_name = file_path.stem.replace(
                '_features_comprehensive', '')
            logger.info(f"   • {account_name}: {file_path}")
    else:
        logger.warning("⚠️ Aucun fichier de features individuel trouvé")

    # Résumé final
    print("\n" + "="*80)
    print("✅ TEST PIPELINE AVEC AGRÉGATION TERMINÉ")
    print("="*80)
    print("📊 Résultats:")
    print("   • Pipeline: ✅ Fonctionnel")
    print("   • Agrégation automatique: ✅ Fonctionnelle")
    print("   • Fichiers: ✅ Générés")
    print("   • Structure: ✅ Correcte")
    print("\n🎯 Prochaines étapes:")
    print("   1. Analyser les données avec: python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test_aggregation")
    print("   2. Créer un modèle baseline")
    print("   3. Augmenter le dataset pour l'entraînement")

    return True


def main():
    """Main function."""
    logger = setup_logging()

    try:
        success = test_pipeline_with_aggregation()
        return 0 if success else 1

    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
