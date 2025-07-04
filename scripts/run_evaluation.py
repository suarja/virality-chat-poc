#!/usr/bin/env python3
"""
Script for automated evaluation runs.
"""
from utils.report_utils import get_report_generator
from utils.mlflow_utils import get_tracker
from models.evaluation import evaluate_predictions
from features.evaluation import evaluate_feature_extraction
from config.evaluation_config import get_config
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import evaluation modules


def main():
    """Run evaluation pipeline."""
    # Get configuration
    config = get_config()

    # Initialize MLflow tracker
    tracker = get_tracker(experiment_name="automated_evaluation")

    # Initialize report generator
    report_gen = get_report_generator(mlflow_tracker=tracker)

    try:
        # Load and evaluate features
        import pandas as pd
        features_df = pd.read_csv(
            project_root / "data/processed/extracted_features.csv")

        with tracker:
            feature_eval_results = evaluate_feature_extraction(
                features_df,
                expected_schema=config.feature_extraction.required_fields
            )

        print("Feature Extraction Evaluation Results:")
        print(f"Completeness: {feature_eval_results['completeness']:.2%}")
        print(f"Accuracy: {feature_eval_results['accuracy']:.2%}")
        print(
            f"Average Latency: {feature_eval_results['avg_latency_ms']:.2f}ms")

        # Load and evaluate predictions
        import numpy as np
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support

        # Load actual predictions (replace with your model's predictions)
        predictions_df = pd.read_csv(
            project_root / "data/processed/model_predictions.csv")
        y_true = predictions_df["true_label"].values
        y_pred = predictions_df["predicted_label"].values

        with tracker:
            pred_eval_results = evaluate_predictions(
                y_true=y_true,
                y_pred=y_pred,
                model_metadata={"name": "virality_predictor_v1"}
            )

        print("\nPrediction Evaluation Results:")
        print(f"Accuracy: {pred_eval_results['accuracy']:.2%}")
        print(f"Precision: {pred_eval_results['precision']:.2%}")
        print(f"Recall: {pred_eval_results['recall']:.2%}")
        print(f"F1 Score: {pred_eval_results['f1']:.2%}")

        # Generate report
        report_path = report_gen.generate_report(
            evaluation_type="full_system",
            metrics={
                **feature_eval_results,
                **pred_eval_results
            },
            component_name="virality_predictor",
            version="1.0.0",
            dataset_size=len(y_true),
            environment="production",
            data_quality={
                "missing_rate": feature_eval_results["missing_rate"],
                "invalid_rate": feature_eval_results["invalid_rate"]
            },
            performance_metrics={
                "feature_extraction_latency_ms": feature_eval_results["avg_latency_ms"],
                "prediction_latency_ms": pred_eval_results["avg_inference_time_ms"]
            },
            error_analysis={
                "feature_errors": feature_eval_results["error_details"],
                "prediction_errors": pred_eval_results["error_analysis"]
            }
        )

        print(f"\nEvaluation report generated at: {report_path}")

        # Check thresholds and alert if needed
        alert_thresholds = {
            "completeness": 0.95,
            "accuracy": 0.80,
            "f1": 0.75
        }

        alerts = []
        if feature_eval_results["completeness"] < alert_thresholds["completeness"]:
            alerts.append(
                f"Feature completeness below threshold: {feature_eval_results['completeness']:.2%}")

        if pred_eval_results["accuracy"] < alert_thresholds["accuracy"]:
            alerts.append(
                f"Model accuracy below threshold: {pred_eval_results['accuracy']:.2%}")

        if pred_eval_results["f1"] < alert_thresholds["f1"]:
            alerts.append(
                f"Model F1 score below threshold: {pred_eval_results['f1']:.2%}")

        if alerts:
            print("\n⚠️ ALERTS:")
            for alert in alerts:
                print(f"- {alert}")
            sys.exit(1)

        print("\n✅ All metrics within acceptable thresholds")
        return 0

    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
