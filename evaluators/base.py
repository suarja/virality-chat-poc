"""
Base evaluator class for the virality prediction system.

This module provides the foundation for all evaluators in the system,
defining common interfaces and functionality.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypeVar, Generic
from datetime import datetime
import json
import logging

import mlflow
from pydantic import BaseModel

# Type variables for generic typing
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')
MetricType = TypeVar('MetricType', bound=float)


class EvaluationResult(BaseModel):
    """Structured evaluation result."""
    metric_name: str
    value: float
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = {}


@dataclass
class EvaluationContext:
    """Context for evaluation runs."""
    input_data: Any
    expected_output: Optional[Any] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseEvaluator(Generic[InputType, OutputType, MetricType], ABC):
    """Base class for all evaluators in the system.

    Attributes:
        name: Unique identifier for the evaluator
        description: Human-readable description of what this evaluator does
        version: Version of the evaluator implementation
        metrics: List of metric names this evaluator produces
    """

    def __init__(
        self,
        name: str,
        description: str,
        version: str = "0.1.0",
        metrics: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.version = version
        self.metrics = metrics or []

        # Setup logging
        self.logger = logging.getLogger(f"evaluator.{name}")

        # Initialize MLflow
        mlflow.set_experiment(f"evaluator_{name}")

    @abstractmethod
    async def evaluate(
        self,
        context: EvaluationContext
    ) -> List[EvaluationResult]:
        """Evaluate the input and return a list of evaluation results.

        Args:
            context: Evaluation context containing input data and metadata

        Returns:
            List of evaluation results
        """
        pass

    def log_results(self, results: List[EvaluationResult]) -> None:
        """Log evaluation results to MLflow and local storage.

        Args:
            results: List of evaluation results to log
        """
        # Log to MLflow
        with mlflow.start_run(run_name=f"{self.name}_eval"):
            for result in results:
                mlflow.log_metric(
                    result.metric_name,
                    result.value,
                    step=int(result.timestamp.timestamp())
                )
                mlflow.log_params(result.metadata)

        # Log to local storage
        for result in results:
            self.logger.info(
                "Evaluation result",
                extra={
                    "metric_name": result.metric_name,
                    "value": result.value,
                    "metadata": result.metadata
                }
            )

    def save_results(
        self,
        results: List[EvaluationResult],
        filepath: str
    ) -> None:
        """Save evaluation results to a JSON file.

        Args:
            results: List of evaluation results to save
            filepath: Path to save the results to
        """
        with open(filepath, 'w') as f:
            json.dump(
                [result.dict() for result in results],
                f,
                indent=2,
                default=str
            )

    @classmethod
    def load_results(cls, filepath: str) -> List[EvaluationResult]:
        """Load evaluation results from a JSON file.

        Args:
            filepath: Path to load the results from

        Returns:
            List of evaluation results
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            return [EvaluationResult(**result) for result in data]
