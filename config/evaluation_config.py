"""
Configuration settings for the evaluation framework.
"""
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# Base paths
EVALUATION_DIR = Path("data/evaluation")
METRICS_DIR = EVALUATION_DIR / "metrics"
REPORTS_DIR = EVALUATION_DIR / "reports"
MLFLOW_TRACKING_URI = "file:./mlruns"

# Feature extraction evaluation settings


class FeatureExtractionConfig(BaseModel):
    """Configuration for feature extraction evaluation."""
    required_fields: List[str] = Field(
        default=[
            "video_id",
            "title",
            "description",
            "duration",
            "view_count",
            "like_count",
            "comment_count",
            "share_count",
            "music_info",
            "hashtags",
        ],
        description="Required fields that must be present in extracted features"
    )

    completeness_threshold: float = Field(
        default=0.95,
        description="Minimum acceptable completeness score (0-1)"
    )

    accuracy_thresholds: Dict[str, float] = Field(
        default={
            "view_count": 0.99,
            "like_count": 0.99,
            "comment_count": 0.99,
            "share_count": 0.99,
        },
        description="Minimum accuracy scores for specific metrics"
    )

    performance_thresholds: Dict[str, float] = Field(
        default={
            "extraction_time_ms": 5000,  # 5 seconds
            "memory_usage_mb": 500,
        },
        description="Performance thresholds for extraction process"
    )

# Model evaluation settings


class ModelEvaluationConfig(BaseModel):
    """Configuration for model evaluation."""
    metrics: List[str] = Field(
        default=[
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
        ],
        description="Metrics to calculate for model evaluation"
    )

    thresholds: Dict[str, float] = Field(
        default={
            "accuracy": 0.8,
            "precision": 0.75,
            "recall": 0.75,
            "f1": 0.75,
            "roc_auc": 0.8,
        },
        description="Minimum acceptable scores for each metric"
    )

    performance_thresholds: Dict[str, float] = Field(
        default={
            "inference_time_ms": 100,  # 100ms per prediction
            "batch_inference_time_ms": 1000,  # 1s for batch
            "memory_usage_mb": 1000,
        },
        description="Performance thresholds for model inference"
    )

# MLflow experiment settings


class MLflowConfig(BaseModel):
    """Configuration for MLflow tracking."""
    experiment_name: str = Field(
        default="virality_prediction",
        description="Name of the MLflow experiment"
    )

    tags: Dict[str, str] = Field(
        default={
            "project": "virality_chat_poc",
            "framework_version": "1.0.0",
        },
        description="Default tags for MLflow runs"
    )

    tracking_uri: str = Field(
        default=MLFLOW_TRACKING_URI,
        description="URI for MLflow tracking server"
    )

# Report generation settings


class ReportConfig(BaseModel):
    """Configuration for evaluation reports."""
    template_path: Path = Field(
        default=Path("reports/templates/evaluation_report_template.md"),
        description="Path to report template"
    )

    output_dir: Path = Field(
        default=REPORTS_DIR,
        description="Directory for generated reports"
    )

    include_plots: bool = Field(
        default=True,
        description="Whether to include plots in reports"
    )

    plot_formats: List[str] = Field(
        default=["png", "html"],
        description="Output formats for plots"
    )

# Main evaluation configuration


class EvaluationConfig(BaseModel):
    """Main configuration for the evaluation framework."""
    feature_extraction: FeatureExtractionConfig = Field(
        default_factory=FeatureExtractionConfig,
        description="Feature extraction evaluation settings"
    )

    model: ModelEvaluationConfig = Field(
        default_factory=ModelEvaluationConfig,
        description="Model evaluation settings"
    )

    mlflow: MLflowConfig = Field(
        default_factory=MLflowConfig,
        description="MLflow configuration"
    )

    report: ReportConfig = Field(
        default_factory=ReportConfig,
        description="Report generation settings"
    )

    base_dirs: Dict[str, Path] = Field(
        default={
            "evaluation": EVALUATION_DIR,
            "metrics": METRICS_DIR,
            "reports": REPORTS_DIR,
        },
        description="Base directories for evaluation artifacts"
    )


# Create default configuration
default_config = EvaluationConfig()


def get_config(config_path: Optional[Path] = None) -> EvaluationConfig:
    """
    Get evaluation configuration.

    Args:
        config_path: Optional path to custom config file

    Returns:
        EvaluationConfig instance
    """
    if config_path and config_path.exists():
        return EvaluationConfig.parse_file(config_path)
    return default_config
