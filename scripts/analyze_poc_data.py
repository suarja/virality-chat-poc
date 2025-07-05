#!/usr/bin/env python3
"""
Script d'analyse rapide pour le POC de virality prediction.
Utilisé dans la Phase 1 pour valider les données et créer un modèle baseline.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import warnings
import joblib
warnings.filterwarnings('ignore')


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def load_and_prepare_data(dataset_dir: str, feature_set: str = 'comprehensive'):
    """
    Charge et prépare les données pour l'analyse.

    Args:
        dataset_dir: Chemin vers le dossier du dataset
        feature_set: Feature set à utiliser

    Returns:
        DataFrame préparé pour l'analyse
    """
    logger = logging.getLogger(__name__)

    # Chercher le fichier agrégé ou agréger si nécessaire
    features_dir = Path(dataset_dir) / "features"
    aggregated_file = features_dir / f"aggregated_{feature_set}.csv"

    if aggregated_file.exists():
        logger.info(f"Chargement du fichier agrégé: {aggregated_file}")
        df = pd.read_csv(aggregated_file)
    else:
        logger.info("Fichier agrégé non trouvé, agrégation en cours...")
        from aggregate_features import aggregate_features
        df = aggregate_features(dataset_dir, feature_set)

    logger.info(
        f"Données chargées: {len(df)} vidéos, {len(df.columns)} features")
    return df


def analyze_data_distribution(df: pd.DataFrame):
    """
    Analyse la distribution des données et des métriques clés.

    Args:
        df: DataFrame avec les features
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("📊 ANALYSE DE LA DISTRIBUTION DES DONNÉES")
    print("="*60)

    # Métriques de base
    print(f"\n📈 MÉTRIQUES DE BASE:")
    print(f"   • Nombre de vidéos: {len(df)}")
    print(f"   • Nombre de comptes: {df['account_name'].nunique()}")
    print(f"   • Période: {df['month'].min()} - {df['month'].max()}")

    # Distribution des vues
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

    # Engagement
    if 'engagement_rate' in df.columns:
        print(f"\n💬 ENGAGEMENT:")
        engagement_stats = df['engagement_rate'].describe()
        print(f"   • Taux d'engagement moyen: {engagement_stats['mean']:.3f}")
        print(f"   • Médiane: {engagement_stats['50%']:.3f}")


def analyze_correlations(df: pd.DataFrame, target_col: str = 'view_count'):
    """
    Analyse les corrélations avec la variable cible.

    Args:
        df: DataFrame avec les features
        target_col: Colonne cible (par défaut 'view_count')
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("🔗 ANALYSE DES CORRÉLATIONS")
    print("="*60)

    # Sélectionner les colonnes numériques
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != target_col]

    # Calculer les corrélations
    correlations = df[numeric_cols + [target_col]
                      ].corr()[target_col].sort_values(ascending=False)

    print(f"\n📊 TOP 10 CORRÉLATIONS AVEC {target_col.upper()}:")
    for feature, corr in correlations.head(10).items():
        print(f"   • {feature}: {corr:.3f}")

    print(f"\n📉 TOP 10 CORRÉLATIONS NÉGATIVES:")
    for feature, corr in correlations.tail(10).items():
        print(f"   • {feature}: {corr:.3f}")

    # Visualisation des corrélations
    plt.figure(figsize=(12, 8))
    top_correlations = correlations.head(15)
    plt.barh(range(len(top_correlations)), top_correlations.values)
    plt.yticks(range(len(top_correlations)), top_correlations.index)
    plt.xlabel('Corrélation')
    plt.title(f'Top 15 Corrélations avec {target_col}')
    plt.tight_layout()
    plt.savefig('correlations_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    return correlations


def create_baseline_model(df: pd.DataFrame, target_col: str = 'view_count'):
    """
    Crée et évalue un modèle baseline.

    Args:
        df: DataFrame avec les features
        target_col: Colonne cible

    Returns:
        Modèle entraîné et métriques
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("🤖 MODÈLE BASELINE")
    print("="*60)

    # Préparer les données
    feature_cols = [col for col in df.columns if col not in [
        'video_id', target_col, 'account_name']]
    X = df[feature_cols].fillna(0)  # Remplacer les NaN par 0
    y = df[target_col]

    print(f"\n📋 FEATURES UTILISÉES ({len(feature_cols)}):")
    for i, feature in enumerate(feature_cols, 1):
        print(f"   {i:2d}. {feature}")

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
    train_rmse = mean_squared_error(y_train, y_pred_train, squared=False)
    test_rmse = mean_squared_error(y_test, y_pred_test, squared=False)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)

    print(f"\n📈 MÉTRIQUES DE PERFORMANCE:")
    print(f"   • R² Score (train): {train_r2:.3f}")
    print(f"   • R² Score (test):  {test_r2:.3f}")
    print(f"   • RMSE (train):     {train_rmse:,.0f}")
    print(f"   • RMSE (test):      {test_rmse:,.0f}")
    print(f"   • MAE (train):      {train_mae:,.0f}")
    print(f"   • MAE (test):       {test_mae:,.0f}")

    # Validation croisée
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"\n🔄 VALIDATION CROISÉE (5-fold):")
    print(f"   • R² Score moyen: {cv_scores.mean():.3f}")
    print(f"   • Écart-type: {cv_scores.std():.3f}")
    print(
        f"   • Intervalle: [{cv_scores.mean() - 2*cv_scores.std():.3f}, {cv_scores.mean() + 2*cv_scores.std():.3f}]")

    # Features importantes
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\n🏆 TOP 10 FEATURES IMPORTANTES:")
    for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']}: {row['importance']:.3f}")

    # Visualisation des features importantes
    plt.figure(figsize=(12, 8))
    top_features = feature_importance.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance')
    plt.title('Top 15 Features Importantes')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()

    return model, {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'feature_importance': feature_importance
    }


def generate_insights(df: pd.DataFrame, model, feature_importance):
    """
    Génère des insights basés sur l'analyse.

    Args:
        df: DataFrame avec les features
        model: Modèle entraîné
        feature_importance: DataFrame avec l'importance des features
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("💡 INSIGHTS ET RECOMMANDATIONS")
    print("="*60)

    # Insights sur les données
    print(f"\n📊 INSIGHTS SUR LES DONNÉES:")
    print(
        f"   • Dataset: {len(df)} vidéos de {df['account_name'].nunique()} comptes")
    print(f"   • Période: {df['month'].min()} - {df['month'].max()}")
    print(f"   • Vues moyennes: {df['view_count'].mean():,.0f}")

    # Insights sur les features importantes
    print(f"\n🎯 FEATURES CLÉS POUR LA VIRALITÉ:")
    top_features = feature_importance.head(5)
    for _, row in top_features.iterrows():
        feature = row['feature']
        importance = row['importance']

        if 'engagement' in feature.lower():
            print(
                f"   • {feature} ({importance:.3f}): L'engagement est crucial")
        elif 'duration' in feature.lower():
            print(
                f"   • {feature} ({importance:.3f}): La durée optimale compte")
        elif 'hashtag' in feature.lower():
            print(
                f"   • {feature} ({importance:.3f}): Le nombre de hashtags influence")
        else:
            print(f"   • {feature} ({importance:.3f}): Feature importante")

    # Recommandations
    print(f"\n🚀 RECOMMANDATIONS POUR LA SUITE:")
    print(
        f"   • Modèle baseline: R² = {model.cv_scores.mean():.3f} (acceptable pour POC)")
    print(f"   • Prochaine étape: Augmenter le dataset à 150+ vidéos")
    print(f"   • Optimisation: Tester Gradient Boosting et XGBoost")
    print(f"   • Features: Ajouter plus de features temporelles et de contenu")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Analyse rapide des données pour le POC de virality prediction"
    )

    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="Chemin vers le dossier du dataset (ex: data/dataset_poc_validation)"
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
        # Charger les données
        logger.info(f"Chargement des données depuis {args.dataset_dir}")
        df = load_and_prepare_data(args.dataset_dir, args.feature_set)

        # Analyser la distribution
        analyze_data_distribution(df)

        # Analyser les corrélations
        correlations = analyze_correlations(df, args.target)

        # Créer le modèle baseline
        model, metrics = create_baseline_model(df, args.target)

        # Générer les insights
        generate_insights(df, model, metrics['feature_importance'])

        # Sauvegarder le modèle si demandé
        if args.save_model:
            model_path = Path('models')
            model_path.mkdir(exist_ok=True)

            joblib.dump(model, model_path / 'baseline_virality_model.pkl')
            logger.info(
                f"Modèle sauvegardé dans {model_path / 'baseline_virality_model.pkl'}")

        # Résumé final
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE")
        print("="*60)
        print(f"📊 Performance du modèle: R² = {metrics['test_r2']:.3f}")
        print(f"🎯 Prochaine étape: Augmenter le dataset et optimiser le modèle")
        print(f"📁 Visualisations sauvegardées: correlations_analysis.png, feature_importance.png")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
