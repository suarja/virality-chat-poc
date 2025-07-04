"""
MLflow utilities for tracking experiments and metrics.
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

import mlflow
from mlflow.entities import Run
from mlflow.tracking import MlflowClient

from config.evaluation_config import MLflowConfig, get_config


class MLflowTracker:
    """Wrapper for MLflow tracking functionality."""

    def __init__(
        self,
        config: Optional[MLflowConfig] = None,
        experiment_name: Optional[str] = None,
        run_name: Optional[str] = None
    ):
        """
        Initialize MLflow tracker.

        Args:
            config: MLflow configuration
            experiment_name: Optional experiment name override
            run_name: Optional run name
        """
        self.config = config or get_config().mlflow
        self.client = MlflowClient(tracking_uri=self.config.tracking_uri)

        # Set tracking URI
        mlflow.set_tracking_uri(self.config.tracking_uri)

        # Set experiment
        self.experiment_name = experiment_name or self.config.experiment_name
        self.experiment = self._get_or_create_experiment()

        # Set run
        self.run_name = run_name
        self.active_run: Optional[Run] = None

    def _get_or_create_experiment(self) -> mlflow.entities.Experiment:
        """Get existing experiment or create new one."""
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        if experiment is None:
            experiment_id = mlflow.create_experiment(self.experiment_name)
            experiment = mlflow.get_experiment(experiment_id)
        return experiment

    def start_run(
        self,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Run:
        """
        Start a new MLflow run.

        Args:
            run_name: Optional name for the run
            tags: Optional tags to set

        Returns:
            MLflow Run object
        """
        # Combine default and custom tags
        run_tags = self.config.tags.copy()
        if tags:
            run_tags.update(tags)

        # Start run
        self.active_run = mlflow.start_run(
            experiment_id=self.experiment.experiment_id,
            run_name=run_name or self.run_name,
            tags=run_tags
        )

        return self.active_run

    def end_run(self) -> None:
        """End current MLflow run."""
        if self.active_run:
            mlflow.end_run()
            self.active_run = None

    def log_metric(
        self,
        key: str,
        value: Union[float, int],
        step: Optional[int] = None
    ) -> None:
        """
        Log a metric value.

        Args:
            key: Metric name
            value: Metric value
            step: Optional step number
        """
        mlflow.log_metric(key, value, step=step)

    def log_metrics(
        self,
        metrics: Dict[str, Union[float, int]],
        step: Optional[int] = None
    ) -> None:
        """
        Log multiple metrics.

        Args:
            metrics: Dictionary of metric names and values
            step: Optional step number
        """
        mlflow.log_metrics(metrics, step=step)

    def log_param(self, key: str, value: Any) -> None:
        """
        Log a parameter value.

        Args:
            key: Parameter name
            value: Parameter value
        """
        mlflow.log_param(key, value)

    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log multiple parameters.

        Args:
            params: Dictionary of parameter names and values
        """
        mlflow.log_params(params)

    def log_artifact(self, local_path: Union[str, Path]) -> None:
        """
        Log a local file or directory as an artifact.

        Args:
            local_path: Path to the local file or directory
        """
        mlflow.log_artifact(str(local_path))

    def log_dict(self, dictionary: Dict[str, Any], filename: str) -> None:
        """
        Log a dictionary as a JSON artifact.

        Args:
            dictionary: Dictionary to log
            filename: Name of the JSON file
        """
        # Create temporary file
        temp_path = Path("temp.json")
        with open(temp_path, "w") as f:
            json.dump(dictionary, f, indent=2)

        # Log and cleanup
        try:
            self.log_artifact(temp_path)
        finally:
            temp_path.unlink()

    def __enter__(self) -> 'MLflowTracker':
        """Context manager entry."""
        self.start_run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.end_run()


def get_tracker(
    experiment_name: Optional[str] = None,
    run_name: Optional[str] = None
) -> MLflowTracker:
    """
    Get MLflow tracker instance.

    Args:
        experiment_name: Optional experiment name
        run_name: Optional run name

    Returns:
        MLflowTracker instance
    """
    return MLflowTracker(experiment_name=experiment_name, run_name=run_name)
