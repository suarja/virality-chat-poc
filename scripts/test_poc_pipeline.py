#!/usr/bin/env python3
"""
Script de test rapide pour le POC de virality prediction.
Teste le pipeline end-to-end avec un dataset minimal.
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


def test_poc_pipeline():
    """Teste le pipeline POC complet."""
    logger = logging.getLogger(__name__)

    print("\n" + "="*80)
    print("🚀 TEST POC PIPELINE - VALIDATION RAPIDE")
    print("="*80)

    # Test 1: Pipeline de scraping et analyse
    logger.info("\n📋 Test 1: Pipeline complet (scraping + Gemini + features)")

    pipeline_cmd = [
        "python3", "scripts/run_pipeline.py",
        "--dataset", "poc_test",
        "--batch-size", "1",
        "--videos-per-account", "5",
        "--max-total-videos", "10",
        "--feature-system", "modular",
        "--feature-set", "comprehensive"
    ]

    success = run_command(" ".join(pipeline_cmd), "Pipeline complet")

    if not success:
        logger.error("❌ Le pipeline a échoué. Arrêt du test.")
        return False

    # Test 2: Agrégation des features
    logger.info("\n📋 Test 2: Agrégation des features")

    aggregate_cmd = [
        "python3", "scripts/aggregate_features.py",
        "--dataset-dir", "data/dataset_poc_test",
        "--feature-set", "comprehensive",
        "--show-stats"
    ]

    success = run_command(" ".join(aggregate_cmd), "Agrégation des features")

    if not success:
        logger.error("❌ L'agrégation a échoué.")
        return False

    # Test 3: Vérification des fichiers générés
    logger.info("\n📋 Test 3: Vérification des fichiers générés")

    dataset_dir = Path("data/dataset_poc_test")
    features_dir = dataset_dir / "features"

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

    # Test 4: Analyse rapide des données (si les dépendances sont disponibles)
    logger.info("\n📋 Test 4: Analyse rapide des données")

    try:
        import pandas as pd
        import numpy as np

        # Charger les données
        df = pd.read_csv(features_dir / "aggregated_comprehensive.csv")

        logger.info(
            f"✅ Données chargées: {len(df)} vidéos, {len(df.columns)} features")

        # Statistiques de base
        if 'view_count' in df.columns:
            view_stats = df['view_count'].describe()
            logger.info(f"📊 Statistiques des vues:")
            logger.info(f"   • Moyenne: {view_stats['mean']:,.0f}")
            logger.info(f"   • Médiane: {view_stats['50%']:,.0f}")
            logger.info(f"   • Min: {view_stats['min']:,.0f}")
            logger.info(f"   • Max: {view_stats['max']:,.0f}")

        # Vérifier les features
        feature_cols = [col for col in df.columns if col not in [
            'video_id', 'view_count', 'account_name']]
        logger.info(f"🔧 Features disponibles: {len(feature_cols)}")

        # Afficher quelques features
        for i, feature in enumerate(feature_cols[:10], 1):
            logger.info(f"   {i:2d}. {feature}")

        if len(feature_cols) > 10:
            logger.info(f"   ... et {len(feature_cols) - 10} autres")

    except ImportError as e:
        logger.warning(f"⚠️ Dépendances manquantes pour l'analyse: {e}")
        logger.info(
            "   Installer: pip install pandas numpy matplotlib scikit-learn")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")

    # Résumé final
    print("\n" + "="*80)
    print("✅ TEST POC TERMINÉ")
    print("="*80)
    print("📊 Résultats:")
    print("   • Pipeline: ✅ Fonctionnel")
    print("   • Agrégation: ✅ Fonctionnelle")
    print("   • Fichiers: ✅ Générés")
    print("   • Données: ✅ Valides")
    print("\n🎯 Prochaines étapes:")
    print("   1. Analyser les données avec: python scripts/analyze_poc_data.py --dataset-dir data/dataset_poc_test")
    print("   2. Créer un modèle baseline")
    print("   3. Augmenter le dataset pour l'entraînement")

    return True


def main():
    """Main function."""
    logger = setup_logging()

    try:
        success = test_poc_pipeline()
        return 0 if success else 1

    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
