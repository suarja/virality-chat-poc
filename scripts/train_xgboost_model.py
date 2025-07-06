#!/usr/bin/env python3
"""
🚀 XGBoost Model Training Script - ITER_003

🎯 Purpose: Train XGBoost model on ITER_002 dataset (84 videos)
📊 Expected: R² > 0.875 (improvement over RandomForest 0.855)
🔧 Usage: python3 scripts/train_xgboost_model.py
"""

# No need to import ModularFeatureSystem for this script
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import logging
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_iter_002_data():
    """Load ITER_002 dataset (84 videos)"""
    dataset_path = project_root / \
        "data/dataset_iter_002/features/aggregated_comprehensive.csv"

    if not dataset_path.exists():
        logger.error(f"❌ Dataset not found: {dataset_path}")
        logger.info(
            "💡 Run ITER_002 first: python3 scripts/run_pipeline.py --dataset iter_002")
        return None

    logger.info(f"📊 Loading dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)
    logger.info(f"✅ Loaded {len(df)} videos")

    return df


def prepare_features(df):
    """Prepare features for XGBoost training"""
    # Use the same 16 features as RandomForest
    feature_columns = [
        'duration', 'hashtag_count', 'estimated_hashtag_count', 'hour_of_day',
        'day_of_week', 'month', 'visual_quality_score', 'has_hook',
        'viral_potential_score', 'emotional_trigger_count',
        'audience_connection_score', 'sound_quality_score',
        'production_quality_score', 'trend_alignment_score', 'color_vibrancy_score',
        'video_duration_optimized'
    ]

    # Target variable: normalized view count
    target_column = 'view_count'

    # Check if all features exist
    missing_features = [
        col for col in feature_columns if col not in df.columns]
    if missing_features:
        logger.error(f"❌ Missing features: {missing_features}")
        return None, None

    # Prepare X and y
    X = df[feature_columns].fillna(0)
    y = df[target_column]

    # Normalize target (log transformation for view counts)
    y_normalized = np.log1p(y)  # log(1 + x) to handle zeros

    logger.info(f"✅ Features prepared: {X.shape}")
    logger.info(
        f"✅ Target range: {y_normalized.min():.2f} - {y_normalized.max():.2f}")

    return X, y_normalized


def train_xgboost_model(X, y):
    """Train XGBoost model with hyperparameter tuning"""
    logger.info("🤖 Training XGBoost model...")

    # XGBoost parameters (optimized for virality prediction)
    xgb_params = {
        'n_estimators': 200,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse'
    }

    # Train XGBoost
    xgb_model = xgb.XGBRegressor(**xgb_params)

    # Cross-validation
    cv_scores = cross_val_score(xgb_model, X, y, cv=5, scoring='r2')
    logger.info(f"📊 Cross-validation R² scores: {cv_scores}")
    logger.info(
        f"📊 Mean CV R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Train final model
    xgb_model.fit(X, y)

    return xgb_model, cv_scores


def compare_with_randomforest(X, y):
    """Compare XGBoost with RandomForest"""
    logger.info("🔍 Comparing XGBoost vs RandomForest...")

    # RandomForest parameters (same as ITER_002)
    rf_params = {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    }

    # Train RandomForest
    rf_model = RandomForestRegressor(**rf_params)
    rf_cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='r2')

    logger.info(
        f"🌲 RandomForest CV R²: {rf_cv_scores.mean():.3f} ± {rf_cv_scores.std():.3f}")

    return rf_model, rf_cv_scores


def evaluate_model(model, X, y, model_name):
    """Evaluate model performance"""
    logger.info(f"📈 Evaluating {model_name}...")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train and predict
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    logger.info(f"📊 {model_name} Performance:")
    logger.info(f"   - R² Score: {r2:.3f}")
    logger.info(f"   - MAE: {mae:.3f}")
    logger.info(f"   - RMSE: {rmse:.3f}")

    return r2, mae, rmse


def save_model(model, model_name, performance_metrics):
    """Save trained model"""
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)

    # Save XGBoost model
    model_path = models_dir / f"iter_003_xgboost_model.pkl"
    joblib.dump(model, model_path)
    logger.info(f"💾 Model saved: {model_path}")

    # Save performance metrics
    metrics_path = models_dir / f"iter_003_xgboost_metrics.json"
    import json
    with open(metrics_path, 'w') as f:
        json.dump(performance_metrics, f, indent=2)
    logger.info(f"💾 Metrics saved: {metrics_path}")

    return model_path


def main():
    """Main training pipeline"""
    logger.info("🚀 Starting XGBoost Training - ITER_003")

    # 1. Load data
    df = load_iter_002_data()
    if df is None:
        return False

    # 2. Prepare features
    X, y = prepare_features(df)
    if X is None:
        return False

    # 3. Train XGBoost
    xgb_model, xgb_cv_scores = train_xgboost_model(X, y)

    # 4. Compare with RandomForest
    rf_model, rf_cv_scores = compare_with_randomforest(X, y)

    # 5. Evaluate both models
    xgb_r2, xgb_mae, xgb_rmse = evaluate_model(xgb_model, X, y, "XGBoost")
    rf_r2, rf_mae, rf_rmse = evaluate_model(rf_model, X, y, "RandomForest")

    # 6. Performance comparison
    logger.info("🏆 Performance Comparison:")
    logger.info(
        f"   XGBoost  R²: {xgb_r2:.3f} (CV: {xgb_cv_scores.mean():.3f})")
    logger.info(
        f"   RandomForest R²: {rf_r2:.3f} (CV: {rf_cv_scores.mean():.3f})")

    improvement = xgb_r2 - rf_r2
    logger.info(f"   Improvement: {improvement:+.3f}")

    # 7. Save best model
    if xgb_r2 > rf_r2:
        logger.info("✅ XGBoost performs better - saving XGBoost model")
        performance_metrics = {
            "model_type": "XGBoost",
            "iteration": "ITER_003",
            "r2_score": xgb_r2,
            "mae": xgb_mae,
            "rmse": xgb_rmse,
            "cv_r2_mean": xgb_cv_scores.mean(),
            "cv_r2_std": xgb_cv_scores.std(),
            "improvement_over_rf": improvement,
            "dataset_size": len(df),
            "features_count": X.shape[1]
        }
        save_model(xgb_model, "XGBoost", performance_metrics)
    else:
        logger.info("⚠️ RandomForest performs better - keeping RandomForest")

    logger.info("🎉 XGBoost training completed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
