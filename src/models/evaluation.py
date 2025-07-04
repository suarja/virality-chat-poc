"""
Model evaluation module.

This module provides evaluation functionality for model predictions,
tightly integrated with the model training and prediction process.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
from pydantic import BaseModel


@dataclass
class PredictionMetrics:
    """Core metrics for prediction quality."""
    accuracy: float
    precision: float
    recall: float
    f1: float
    latency: float  # prediction time in seconds

    def to_dict(self) -> Dict[str, float]:
        return {
            "prediction_accuracy": self.accuracy,
            "prediction_precision": self.precision,
            "prediction_recall": self.recall,
            "prediction_f1": self.f1,
            "prediction_latency": self.latency
        }


class PredictionEvalResult(BaseModel):
    """Evaluation result for a batch of predictions."""
    model_name: str
    metrics: PredictionMetrics
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = {}


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    prediction_time: Optional[float] = None,
    model_name: str = "virality_predictor",
    metadata: Optional[Dict] = None
) -> PredictionEvalResult:
    """
    Evaluate model predictions against ground truth.

    Args:
        y_true: Ground truth labels
        y_pred: Model predictions
        prediction_time: Time taken for predictions
        model_name: Name of the model being evaluated
        metadata: Additional metadata about the evaluation

    Returns:
        Evaluation result with metrics
    """
    # Setup logging
    logger = logging.getLogger("model_evaluation")

    # Calculate metrics
    metrics = PredictionMetrics(
        accuracy=accuracy_score(y_true, y_pred),
        precision=precision_score(y_true, y_pred, average='weighted'),
        recall=recall_score(y_true, y_pred, average='weighted'),
        f1=f1_score(y_true, y_pred, average='weighted'),
        latency=prediction_time or 0.0
    )

    # Log to MLflow
    with mlflow.start_run(run_name=f"{model_name}_eval"):
        mlflow.log_metrics(metrics.to_dict())
        if metadata:
            mlflow.log_params(metadata)

    # Log details
    logger.info(
        "Model prediction evaluation",
        extra={
            "model_name": model_name,
            "metrics": metrics.to_dict(),
            "metadata": metadata or {}
        }
    )

    return PredictionEvalResult(
        model_name=model_name,
        metrics=metrics,
        metadata=metadata or {}
    )
