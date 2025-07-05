#!/usr/bin/env python3
"""
Script pour analyser les données existantes du POC.
Utilisé quand le pipeline a déjà généré les features mais qu'il manque l'agrégation.
CORRIGÉ : Implémente la logique correcte de séparation pré-publication/post-publication.
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


def categorize_features(df: pd.DataFrame):
    """
    Catégorise les features en pré-publication et post-publication.

    Args:
        df: DataFrame avec toutes les features

    Returns:
        dict: Dictionnaire avec features pré-publication et post-publication
    """
    logger = logging.getLogger(__name__)

    # Features PRÉ-PUBLICATION (disponibles avant publication)
    pre_publication_features = [
        # Métadonnées vidéo
        'duration', 'hashtag_count', 'estimated_hashtag_count',

        # Features temporelles
        'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'is_business_hours',

        # Features Gemini (analyse visuelle)
        'has_text_overlays', 'has_transitions', 'visual_quality_score',
        'has_hook', 'has_story', 'has_call_to_action', 'viral_potential_score',
        'emotional_trigger_count', 'audience_connection_score', 'length_optimized',
        'sound_quality_score', 'production_quality_score', 'trend_alignment_score',

        # Features visuelles granulaires
        'close_up_presence', 'zoom_effects_count', 'transition_count',
        'color_vibrancy_score', 'human_presence', 'face_count',
        'text_overlay_presence', 'camera_movement_score', 'brightness_score',
        'contrast_score', 'video_duration_optimized',

        # Features transformées de dates
        'post_time_hour', 'post_time_day_of_week', 'post_time_month',
        'post_time_is_weekend', 'post_time_is_business_hours',
        'extraction_time_hour', 'extraction_time_day_of_week', 'extraction_time_month',
        'extraction_time_is_weekend', 'extraction_time_is_business_hours'
    ]

    # Features POST-PUBLICATION (disponibles seulement après publication)
    post_publication_features = [
        'view_count', 'like_count', 'comment_count', 'share_count',
        'like_rate', 'comment_rate', 'share_rate', 'engagement_rate'
    ]

    # Filtrer les features qui existent réellement dans le dataset
    available_features = df.columns.tolist()

    pre_pub_available = [
        f for f in pre_publication_features if f in available_features]
    post_pub_available = [
        f for f in post_publication_features if f in available_features]

    logger.info(f"Features pré-publication trouvées: {len(pre_pub_available)}")
    logger.info(
        f"Features post-publication trouvées: {len(post_pub_available)}")

    return {
        'pre_publication': pre_pub_available,
        'post_publication': post_pub_available,
        'all_features': available_features
    }


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
    """Crée et évalue un modèle baseline avec séparation pré-publication/post-publication."""
    logger = logging.getLogger(__name__)

    if target_col not in df.columns:
        logger.error(f"Colonne cible '{target_col}' non trouvée")
        return None, None

    print("\n" + "="*60)
    print("🤖 MODÈLE BASELINE - LOGIQUE CORRIGÉE")
    print("="*60)

    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    except ImportError as e:
        logger.error(f"Dépendances manquantes: {e}")
        logger.info("Installer: pip install scikit-learn")
        return None, None

    # Préparer les données - transformer les dates et exclure les colonnes non numériques
    df_processed = df.copy()

    # Transformer les colonnes de dates en features numériques
    date_columns = ['post_time', 'extraction_time']
    for col in date_columns:
        if col in df_processed.columns:
            try:
                # Convertir en datetime
                df_processed[col] = pd.to_datetime(df_processed[col])

                # Extraire les features temporelles
                df_processed[f'{col}_hour'] = df_processed[col].dt.hour
                df_processed[f'{col}_day_of_week'] = df_processed[col].dt.dayofweek
                df_processed[f'{col}_month'] = df_processed[col].dt.month
                df_processed[f'{col}_is_weekend'] = df_processed[col].dt.dayofweek.isin([
                                                                                        5, 6]).astype(int)
                df_processed[f'{col}_is_business_hours'] = ((df_processed[col].dt.hour >= 9) &
                                                            (df_processed[col].dt.hour <= 17)).astype(int)

                # Supprimer la colonne originale
                df_processed = df_processed.drop(columns=[col])

            except Exception as e:
                logger.warning(f"Impossible de traiter la colonne {col}: {e}")
                df_processed = df_processed.drop(columns=[col])

    # Catégoriser les features
    feature_categories = categorize_features(df_processed)

    print(f"\n📋 CATÉGORISATION DES FEATURES:")
    print(
        f"   • Pré-publication: {len(feature_categories['pre_publication'])} features")
    print(
        f"   • Post-publication: {len(feature_categories['post_publication'])} features")

    # Exclure les colonnes non numériques
    numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
    all_feature_cols = [col for col in numeric_cols if col not in [
        'video_id', target_col, 'account_name']]

    # Filtrer les features par catégorie
    pre_pub_features = [
        f for f in feature_categories['pre_publication'] if f in all_feature_cols]
    post_pub_features = [
        f for f in feature_categories['post_publication'] if f in all_feature_cols]

    print(
        f"\n🔍 FEATURES PRÉ-PUBLICATION DISPONIBLES ({len(pre_pub_features)}):")
    for i, feature in enumerate(pre_pub_features[:10], 1):
        print(f"   {i:2d}. {feature}")
    if len(pre_pub_features) > 10:
        print(f"   ... et {len(pre_pub_features) - 10} autres")

    print(
        f"\n📊 FEATURES POST-PUBLICATION DISPONIBLES ({len(post_pub_features)}):")
    for i, feature in enumerate(post_pub_features, 1):
        print(f"   {i:2d}. {feature}")

    # PHASE 1: Entraînement avec toutes les features (pour apprendre les patterns)
    print(f"\n🎯 PHASE 1: ENTRAÎNEMENT AVEC FEATURES COMPLÈTES")
    X_full = df_processed[all_feature_cols].fillna(0)
    y = df_processed[target_col]

    # Split train/test
    X_train_full, X_test_full, y_train, y_test = train_test_split(
        X_full, y, test_size=0.2, random_state=42)

    print(f"   • Train: {len(X_train_full)} vidéos")
    print(f"   • Test: {len(X_test_full)} vidéos")

    # Modèle avec toutes les features
    model_full = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    # Entraînement
    logger.info("Entraînement du modèle avec features complètes...")
    model_full.fit(X_train_full, y_train)

    # Prédictions avec features complètes
    y_pred_train_full = model_full.predict(X_train_full)
    y_pred_test_full = model_full.predict(X_test_full)

    # Métriques avec features complètes
    train_r2_full = r2_score(y_train, y_pred_train_full)
    test_r2_full = r2_score(y_test, y_pred_test_full)

    print(f"   • R² Score (train): {train_r2_full:.3f}")
    print(f"   • R² Score (test):  {test_r2_full:.3f}")

    # PHASE 2: Test avec features pré-publication seulement
    print(f"\n🎯 PHASE 2: TEST AVEC FEATURES PRÉ-PUBLICATION SEULEMENT")

    if not pre_pub_features:
        logger.error("Aucune feature pré-publication disponible pour le test")
        return None, None

    # Sélectionner seulement les features pré-publication
    X_pre_pub = df_processed[pre_pub_features].fillna(0)

    # Split train/test avec features pré-publication
    X_train_pre, X_test_pre, y_train_pre, y_test_pre = train_test_split(
        X_pre_pub, y, test_size=0.2, random_state=42)

    # Modèle avec features pré-publication seulement
    model_pre_pub = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    # Entraînement avec features pré-publication
    logger.info("Entraînement du modèle avec features pré-publication...")
    model_pre_pub.fit(X_train_pre, y_train_pre)

    # Prédictions avec features pré-publication
    y_pred_train_pre = model_pre_pub.predict(X_train_pre)
    y_pred_test_pre = model_pre_pub.predict(X_test_pre)

    # Métriques avec features pré-publication
    train_r2_pre = r2_score(y_train_pre, y_pred_train_pre)
    test_r2_pre = r2_score(y_test_pre, y_pred_test_pre)
    train_rmse_pre = np.sqrt(mean_squared_error(y_train_pre, y_pred_train_pre))
    test_rmse_pre = np.sqrt(mean_squared_error(y_test_pre, y_pred_test_pre))

    print(f"   • R² Score (train): {train_r2_pre:.3f}")
    print(f"   • R² Score (test):  {test_r2_pre:.3f}")
    print(f"   • RMSE (train):     {train_rmse_pre:,.0f}")
    print(f"   • RMSE (test):      {test_rmse_pre:,.0f}")

    # Validation croisée avec features pré-publication
    cv_scores_pre = cross_val_score(
        model_pre_pub, X_pre_pub, y, cv=5, scoring='r2')
    print(f"\n🔄 VALIDATION CROISÉE (5-fold) - Features pré-publication:")
    print(f"   • R² Score moyen: {cv_scores_pre.mean():.3f}")
    print(f"   • Écart-type: {cv_scores_pre.std():.3f}")

    # Features importantes (pré-publication)
    feature_importance_pre = pd.DataFrame({
        'feature': pre_pub_features,
        'importance': model_pre_pub.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\n🏆 TOP 10 FEATURES IMPORTANTES (PRÉ-PUBLICATION):")
    for i, (_, row) in enumerate(feature_importance_pre.head(10).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']}: {row['importance']:.3f}")

    # Comparaison des performances
    print(f"\n📊 COMPARAISON DES PERFORMANCES:")
    print(f"   • Avec features complètes: R² = {test_r2_full:.3f}")
    print(f"   • Avec features pré-publication: R² = {test_r2_pre:.3f}")
    print(
        f"   • Perte de performance: {((test_r2_full - test_r2_pre) / test_r2_full * 100):.1f}%")

    return model_pre_pub, {
        'train_r2': train_r2_pre,
        'test_r2': test_r2_pre,
        'train_rmse': train_rmse_pre,
        'test_rmse': test_rmse_pre,
        'cv_mean': cv_scores_pre.mean(),
        'cv_std': cv_scores_pre.std(),
        'feature_importance': feature_importance_pre,
        'pre_publication_features': pre_pub_features,
        'performance_comparison': {
            'full_features_r2': test_r2_full,
            'pre_publication_r2': test_r2_pre,
            'performance_loss': ((test_r2_full - test_r2_pre) / test_r2_full * 100)
        }
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
        print(f"\n🤖 INSIGHTS SUR LE MODÈLE PRÉ-PUBLICATION:")
        print(f"   • Performance: R² = {metrics['test_r2']:.3f}")

        if metrics['test_r2'] > 0.6:
            print(f"   • Évaluation: Excellent pour un POC")
        elif metrics['test_r2'] > 0.4:
            print(f"   • Évaluation: Bon pour un POC")
        elif metrics['test_r2'] > 0.2:
            print(f"   • Évaluation: Acceptable pour un POC")
        else:
            print(f"   • Évaluation: À améliorer")

        # Comparaison des performances
        if 'performance_comparison' in metrics:
            comp = metrics['performance_comparison']
            print(f"\n📈 COMPARAISON AVEC FEATURES COMPLÈTES:")
            print(
                f"   • Features complètes: R² = {comp['full_features_r2']:.3f}")
            print(
                f"   • Features pré-publication: R² = {comp['pre_publication_r2']:.3f}")
            print(
                f"   • Perte de performance: {comp['performance_loss']:.1f}%")

            if comp['performance_loss'] < 20:
                print(f"   • ✅ Bonne performance avec features pré-publication")
            elif comp['performance_loss'] < 40:
                print(f"   • ⚠️ Performance acceptable, à améliorer")
            else:
                print(f"   • ❌ Performance insuffisante, besoin de plus de features")

    # Recommandations
    print(f"\n🚀 RECOMMANDATIONS POUR LA SUITE:")
    print(f"   • Prochaine étape: Augmenter le dataset à 150+ vidéos")
    print(f"   • Optimisation: Tester Gradient Boosting et XGBoost")
    print(f"   • Features: Ajouter plus de features visuelles et temporelles")
    print(f"   • Validation: Tester sur de nouveaux comptes")
    print(f"   • API: Créer l'API de prédiction avec features pré-publication")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Analyse des données existantes pour le POC de virality prediction (CORRIGÉ)"
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

        # Créer le modèle baseline (CORRIGÉ)
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

            joblib.dump(model, model_path /
                        'pre_publication_virality_model.pkl')
            logger.info(
                f"Modèle pré-publication sauvegardé dans {model_path / 'pre_publication_virality_model.pkl'}")

        # Résumé final
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE - LOGIQUE CORRIGÉE")
        print("="*60)
        if metrics:
            print(
                f"📊 Performance du modèle pré-publication: R² = {metrics['test_r2']:.3f}")
        print(f"🎯 Prochaine étape: Augmenter le dataset et optimiser le modèle")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
