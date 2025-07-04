"""
Utilities for generating evaluation reports.
"""
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import plotly.graph_objects as go
from jinja2 import Template

from config.evaluation_config import ReportConfig, get_config
from utils.mlflow_utils import MLflowTracker


class ReportGenerator:
    """Generator for evaluation reports."""

    def __init__(
        self,
        config: Optional[ReportConfig] = None,
        mlflow_tracker: Optional[MLflowTracker] = None
    ):
        """
        Initialize report generator.

        Args:
            config: Report configuration
            mlflow_tracker: Optional MLflow tracker instance
        """
        self.config = config or get_config().report
        self.mlflow_tracker = mlflow_tracker or MLflowTracker()

        # Load template
        with open(self.config.template_path) as f:
            self.template = Template(f.read())

    def _create_metrics_table(self, metrics: Dict[str, float]) -> str:
        """Create markdown table from metrics."""
        df = pd.DataFrame(
            [(k, f"{v:.4f}") for k, v in metrics.items()],
            columns=["Metric", "Value"]
        )
        return df.to_markdown(index=False)

    def _create_trend_plot(
        self,
        metric_history: List[Dict[str, Any]],
        metric_name: str
    ) -> go.Figure:
        """Create trend plot for a metric."""
        df = pd.DataFrame(metric_history)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df[metric_name],
                mode="lines+markers",
                name=metric_name
            )
        )

        fig.update_layout(
            title=f"{metric_name} Trend",
            xaxis_title="Time",
            yaxis_title="Value"
        )

        return fig

    def _save_plot(
        self,
        fig: go.Figure,
        filename: str,
        formats: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Save plot in specified formats.

        Args:
            fig: Plotly figure
            filename: Base filename
            formats: Output formats (default: png, html)

        Returns:
            List of saved file paths
        """
        formats = formats or self.config.plot_formats
        paths = []

        for fmt in formats:
            path = self.config.output_dir / f"{filename}.{fmt}"
            if fmt == "html":
                fig.write_html(path)
            else:
                fig.write_image(path)
            paths.append(path)

        return paths

    def generate_report(
        self,
        evaluation_type: str,
        metrics: Dict[str, float],
        component_name: str,
        version: str,
        dataset_size: int,
        environment: str,
        data_quality: Dict[str, Any],
        performance_metrics: Dict[str, Any],
        error_analysis: Dict[str, Any],
        metric_history: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        critical_issues: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None,
        next_steps: Optional[List[str]] = None,
        additional_notes: Optional[str] = None
    ) -> Path:
        """
        Generate evaluation report.

        Args:
            evaluation_type: Type of evaluation
            metrics: Current metrics
            component_name: Name of evaluated component
            version: Component version
            dataset_size: Size of evaluation dataset
            environment: Evaluation environment
            data_quality: Data quality metrics
            performance_metrics: Performance metrics
            error_analysis: Error analysis results
            metric_history: Optional metric history for trends
            critical_issues: Optional list of critical issues
            warnings: Optional list of warnings
            recommendations: Optional list of recommendations
            next_steps: Optional list of next steps
            additional_notes: Optional additional notes

        Returns:
            Path to generated report
        """
        # Generate plots if needed
        plot_paths = []
        if self.config.include_plots and metric_history:
            for metric_name, history in metric_history.items():
                fig = self._create_trend_plot(history, metric_name)
                paths = self._save_plot(
                    fig,
                    f"{evaluation_type}_{metric_name}_trend"
                )
                plot_paths.extend(paths)

        # Prepare template variables
        template_vars = {
            "evaluation_type": evaluation_type,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "component_name": component_name,
            "version": version,
            "dataset_size": dataset_size,
            "environment": environment,
            "metrics_table": self._create_metrics_table(metrics),
            "data_quality_table": self._create_metrics_table(data_quality),
            "performance_metrics_table": self._create_metrics_table(performance_metrics),
            "error_analysis": error_analysis,
            "critical_issues": critical_issues or [],
            "warnings": warnings or [],
            "recommendations": recommendations or [],
            "next_steps": next_steps or [],
            "additional_notes": additional_notes or "",
            "mlflow_experiment_id": self.mlflow_tracker.experiment.experiment_id,
            "mlflow_run_id": (
                self.mlflow_tracker.active_run.info.run_id
                if self.mlflow_tracker.active_run
                else None
            ),
            "artifacts_location": str(self.config.output_dir),
            "framework_version": "1.0.0"
        }

        # Generate report
        report_content = self.template.render(**template_vars)

        # Save report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.config.output_dir / \
            f"{evaluation_type}_report_{timestamp}.md"
        report_path.write_text(report_content)

        # Log report and plots to MLflow
        if self.mlflow_tracker.active_run:
            self.mlflow_tracker.log_artifact(report_path)
            for plot_path in plot_paths:
                self.mlflow_tracker.log_artifact(plot_path)

        return report_path


def get_report_generator(
    mlflow_tracker: Optional[MLflowTracker] = None
) -> ReportGenerator:
    """
    Get report generator instance.

    Args:
        mlflow_tracker: Optional MLflow tracker instance

    Returns:
        ReportGenerator instance
    """
    return ReportGenerator(mlflow_tracker=mlflow_tracker)
