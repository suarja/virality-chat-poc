#!/usr/bin/env python3
"""
Script pour analyser les données existantes du POC.
Utilisé quand le pipeline a déjà généré les features mais qu'il manque l'agrégation.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import logging
import sys
import warnings
warnings.filterwarnings('ignore')


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def aggregate_existing_features(dataset_dir: str, feature_set: str = 'comprehensive'):
    """
    Agrège les features existantes par compte en un seul fichier.

    Args:
        dataset_dir: Chemin vers le dossier du dataset
        feature_set: Feature set à utiliser

    Returns:
        DataFrame agrégé
    """
    logger = logging.getLogger(__name__)

    features_dir = Path(dataset_dir) / "features"
    aggregated_file = features_dir / f"aggregated_{feature_set}.csv"

    # Vérifier si l'agrégation existe déjà
    if aggregated_file.exists():
        logger.info(f"Fichier agrégé existant trouvé: {aggregated_file}")
        return pd.read_csv(aggregated_file)

    # Chercher les fichiers de features par compte
    feature_files = list(features_dir.glob(f"*_features_{feature_set}.csv"))

    # Si pas de fichiers avec le pattern spécifique, chercher des fichiers CSV génériques
    if not feature_files:
        feature_files = list(features_dir.glob("*.csv"))

    if not feature_files:
        raise FileNotFoundError(
            f"Aucun fichier de features trouvé dans {features_dir}")

    logger.info(f"Agrégation de {len(feature_files)} fichiers de features...")

    # Charger et concaténer les features
    all_features = []
    for file_path in feature_files:
        account_name = file_path.stem.replace(f'_features_{feature_set}', '')
        logger.info(f"Chargement de {account_name}: {file_path}")

        df = pd.read_csv(file_path)
        df['account_name'] = account_name
        all_features.append(df)

    # Concaténer tous les DataFrames
    aggregated_df = pd.concat(all_features, ignore_index=True)

    # Sauvegarder l'agrégation
    aggregated_df.to_csv(aggregated_file, index=False)
    logger.info(f"✅ Features agrégées sauvegardées dans {aggregated_file}")

    return aggregated_df


def analyze_data_distribution(df: pd.DataFrame):
    """Analyse la distribution des données."""
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("📊 ANALYSE DE LA DISTRIBUTION DES DONNÉES")
    print("="*60)

    # Métriques de base
    print(f"\n📈 MÉTRIQUES DE BASE:")
    print(f"   • Nombre de vidéos: {len(df)}")
    print(f"   • Nombre de comptes: {df['account_name'].nunique()}")
    print(f"   • Comptes: {', '.join(df['account_name'].unique())}")

    # Distribution des vues
    if 'view_count' in df.columns:
        print(f"\n👀 DISTRIBUTION DES VUES:")
        view_stats = df['view_count'].describe()
        print(f"   • Moyenne: {view_stats['mean']:,.0f}")
        print(f"   • Médiane: {view_stats['50%']:,.0f}")
        print(f"   • Min: {view_stats['min']:,.0f}")
        print(f"   • Max: {view_stats['max']:,.0f}")
        print(f"   • Écart-type: {view_stats['std']:,.0f}")

        # Distribution par compte
        print(f"\n📱 VUES PAR COMPTE:")
        account_stats = df.groupby('account_name')['view_count'].agg(
            ['count', 'mean', 'median']).round(0)
        for account, stats in account_stats.iterrows():
            print(
                f"   • {account}: {stats['count']} vidéos, {stats['mean']:,.0f} vues moyennes")

    # Features disponibles
    feature_cols = [col for col in df.columns if col not in [
        'video_id', 'view_count', 'account_name']]
    print(f"\n🔧 FEATURES DISPONIBLES ({len(feature_cols)}):")
    for i, feature in enumerate(feature_cols[:15], 1):
        print(f"   {i:2d}. {feature}")

    if len(feature_cols) > 15:
        print(f"   ... et {len(feature_cols) - 15} autres")


def analyze_correlations(df: pd.DataFrame, target_col: str = 'view_count'):
    """Analyse les corrélations avec la variable cible."""
    logger = logging.getLogger(__name__)

    if target_col not in df.columns:
        logger.warning(f"Colonne cible '{target_col}' non trouvée")
        return None

    print("\n" + "="*60)
    print("🔗 ANALYSE DES CORRÉLATIONS")
    print("="*60)

    # Sélectionner les colonnes numériques
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != target_col]

    if not numeric_cols:
        logger.warning(
            "Aucune colonne numérique trouvée pour l'analyse des corrélations")
        return None

    # Calculer les corrélations
    correlations = df[numeric_cols + [target_col]
                      ].corr()[target_col].sort_values(ascending=False)

    print(f"\n📊 TOP 10 CORRÉLATIONS AVEC {target_col.upper()}:")
    for feature, corr in correlations.head(10).items():
        print(f"   • {feature}: {corr:.3f}")

    print(f"\n📉 TOP 5 CORRÉLATIONS NÉGATIVES:")
    for feature, corr in correlations.tail(5).items():
        print(f"   • {feature}: {corr:.3f}")

    return correlations


def create_baseline_model(df: pd.DataFrame, target_col: str = 'view_count'):
    """Crée et évalue un modèle baseline."""
    logger = logging.getLogger(__name__)

    if target_col not in df.columns:
        logger.error(f"Colonne cible '{target_col}' non trouvée")
        return None, None

    print("\n" + "="*60)
    print("🤖 MODÈLE BASELINE")
    print("="*60)

    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    except ImportError as e:
        logger.error(f"Dépendances manquantes: {e}")
        logger.info("Installer: pip install scikit-learn")
        return None, None

    # Préparer les données - exclure les colonnes non numériques
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_cols = [col for col in numeric_cols if col not in [
        'video_id', target_col, 'account_name']]

    if not feature_cols:
        logger.error("Aucune feature numérique trouvée pour le modèle")
        return None, None

    X = df[feature_cols].fillna(0)  # Remplacer les NaN par 0
    y = df[target_col]

    print(f"\n📋 FEATURES UTILISÉES ({len(feature_cols)}):")
    for i, feature in enumerate(feature_cols[:10], 1):
        print(f"   {i:2d}. {feature}")

    if len(feature_cols) > 10:
        print(f"   ... et {len(feature_cols) - 10} autres")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    print(f"\n📊 SPLIT DES DONNÉES:")
    print(f"   • Train: {len(X_train)} vidéos")
    print(f"   • Test: {len(X_test)} vidéos")

    # Modèle Random Forest
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    # Entraînement
    logger.info("Entraînement du modèle...")
    model.fit(X_train, y_train)

    # Prédictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Métriques
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

    print(f"\n📈 MÉTRIQUES DE PERFORMANCE:")
    print(f"   • R² Score (train): {train_r2:.3f}")
    print(f"   • R² Score (test):  {test_r2:.3f}")
    print(f"   • RMSE (train):     {train_rmse:,.0f}")
    print(f"   • RMSE (test):      {test_rmse:,.0f}")

    # Validation croisée
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"\n🔄 VALIDATION CROISÉE (5-fold):")
    print(f"   • R² Score moyen: {cv_scores.mean():.3f}")
    print(f"   • Écart-type: {cv_scores.std():.3f}")

    # Features importantes
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\n🏆 TOP 10 FEATURES IMPORTANTES:")
    for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']}: {row['importance']:.3f}")

    return model, {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'feature_importance': feature_importance
    }


def generate_insights(df: pd.DataFrame, model, metrics):
    """Génère des insights basés sur l'analyse."""
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("💡 INSIGHTS ET RECOMMANDATIONS")
    print("="*60)

    # Insights sur les données
    print(f"\n📊 INSIGHTS SUR LES DONNÉES:")
    print(
        f"   • Dataset: {len(df)} vidéos de {df['account_name'].nunique()} comptes")
    print(f"   • Comptes analysés: {', '.join(df['account_name'].unique())}")

    if 'view_count' in df.columns:
        print(f"   • Vues moyennes: {df['view_count'].mean():,.0f}")

    # Insights sur le modèle
    if model is not None and isinstance(metrics, dict):
        print(f"\n🤖 INSIGHTS SUR LE MODÈLE:")
        print(f"   • Performance: R² = {metrics['test_r2']:.3f}")

        if metrics['test_r2'] > 0.6:
            print(f"   • Évaluation: Excellent pour un POC")
        elif metrics['test_r2'] > 0.4:
            print(f"   • Évaluation: Bon pour un POC")
        elif metrics['test_r2'] > 0.2:
            print(f"   • Évaluation: Acceptable pour un POC")
        else:
            print(f"   • Évaluation: À améliorer")

    # Recommandations
    print(f"\n🚀 RECOMMANDATIONS POUR LA SUITE:")
    print(f"   • Prochaine étape: Augmenter le dataset à 150+ vidéos")
    print(f"   • Optimisation: Tester Gradient Boosting et XGBoost")
    print(f"   • Features: Ajouter plus de features temporelles et de contenu")
    print(f"   • Validation: Tester sur de nouveaux comptes")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Analyse des données existantes pour le POC de virality prediction"
    )

    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="Chemin vers le dossier du dataset (ex: data/dataset_poc_test)"
    )

    parser.add_argument(
        "--feature-set",
        type=str,
        default='comprehensive',
        choices=['metadata', 'gemini_basic',
                 'visual_granular', 'comprehensive'],
        help="Feature set à analyser"
    )

    parser.add_argument(
        "--target",
        type=str,
        default='view_count',
        help="Variable cible pour la prédiction"
    )

    parser.add_argument(
        "--save-model",
        action="store_true",
        help="Sauvegarder le modèle entraîné"
    )

    args = parser.parse_args()
    logger = setup_logging()

    try:
        # Agrégation des features existantes
        logger.info(f"Analyse des données depuis {args.dataset_dir}")
        df = aggregate_existing_features(args.dataset_dir, args.feature_set)

        # Analyser la distribution
        analyze_data_distribution(df)

        # Analyser les corrélations
        correlations = analyze_correlations(df, args.target)

        # Créer le modèle baseline
        model, metrics = create_baseline_model(df, args.target)

        # Générer les insights
        if model and metrics:
            generate_insights(df, model, metrics)
        else:
            generate_insights(df, None, None)

        # Sauvegarder le modèle si demandé
        if args.save_model and model:
            import joblib
            model_path = Path('models')
            model_path.mkdir(exist_ok=True)

            joblib.dump(model, model_path / 'baseline_virality_model.pkl')
            logger.info(
                f"Modèle sauvegardé dans {model_path / 'baseline_virality_model.pkl'}")

        # Résumé final
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE")
        print("="*60)
        if metrics:
            print(f"📊 Performance du modèle: R² = {metrics['test_r2']:.3f}")
        print(f"🎯 Prochaine étape: Augmenter le dataset et optimiser le modèle")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
