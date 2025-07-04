# Evaluation Framework Documentation

## 1. Data Storage Structure

```
memory-bank/
├── evaluation/
│   ├── metrics/                    # Stores evaluation metrics and results
│   │   ├── feature_extraction/     # Feature extraction quality metrics
│   │   ├── prediction/             # Prediction accuracy metrics
│   │   └── system/                 # System performance metrics
│   │
│   ├── datasets/                   # Test datasets and ground truth
│   │   ├── golden_set/            # Curated set of known viral videos
│   │   ├── edge_cases/            # Edge case videos for testing
│   │   └── benchmarks/            # Benchmark datasets
│   │
│   ├── reports/                    # Evaluation reports
│   │   ├── daily/                 # Daily evaluation summaries
│   │   ├── weekly/                # Weekly trend analysis
│   │   └── monthly/               # Monthly performance reviews
│   │
│   └── configs/                    # Evaluation configurations
│       ├── feature_extractors/     # Feature extraction settings
│       ├── predictors/             # Prediction model settings
│       └── system/                 # System evaluation settings
```

## 2. Data Formats

### 2.1 Metrics Storage

```json
{
  "evaluation_id": "eval_20240315_001",
  "timestamp": "2024-03-15T10:00:00Z",
  "metrics": {
    "feature_extraction": {
      "completeness": 0.95,
      "accuracy": 0.88,
      "consistency": 0.92
    },
    "prediction": {
      "accuracy": 0.85,
      "calibration": 0.9,
      "timeliness": 0.95
    },
    "system": {
      "latency": 120, // ms
      "resource_usage": 0.75,
      "error_rate": 0.02
    }
  }
}
```

### 2.2 Dataset Format

```json
{
  "dataset_id": "golden_001",
  "videos": [
    {
      "video_id": "vid_001",
      "url": "https://...",
      "ground_truth": {
        "virality_score": 0.95,
        "engagement_metrics": {
          "views": 1000000,
          "likes": 100000,
          "shares": 50000
        }
      }
    }
  ]
}
```

### 2.3 Report Format

```markdown
# Daily Evaluation Report: 2024-03-15

## Summary

- Overall System Score: 0.89
- Feature Extraction Quality: 0.92
- Prediction Accuracy: 0.85
- System Performance: 0.90

## Detailed Metrics

[...]
```

## 3. Data Access Patterns

### 3.1 Metrics Access

- Real-time metrics stored in memory-bank/evaluation/metrics/{category}/current.json
- Historical metrics archived in memory-bank/evaluation/metrics/{category}/archive/YYYY-MM-DD.json

### 3.2 Dataset Access

- Golden dataset loaded at startup
- Edge cases and benchmarks loaded on-demand during evaluation runs

### 3.3 Report Generation

- Automated daily reports at 00:00 UTC
- Weekly reports generated every Monday
- Monthly reports on the 1st of each month

## 4. Data Retention

### 4.1 Metrics Retention

- Real-time metrics: 24 hours
- Daily aggregates: 90 days
- Weekly aggregates: 1 year
- Monthly aggregates: indefinite

### 4.2 Dataset Retention

- Golden dataset: permanent
- Edge cases: permanent
- Benchmark results: 1 year

### 4.3 Report Retention

- Daily reports: 90 days
- Weekly reports: 1 year
- Monthly reports: indefinite

## 5. Implementation Notes

### 5.1 Creating New Evaluations

```python
from memory_bank.evaluation import Evaluator

evaluator = Evaluator(
    config_path="memory-bank/evaluation/configs/default.json",
    output_path="memory-bank/evaluation/metrics"
)
```

### 5.2 Accessing Results

```python
from memory_bank.evaluation import MetricsReader

reader = MetricsReader("memory-bank/evaluation/metrics")
latest_results = reader.get_latest()
historical_trend = reader.get_trend("feature_extraction", days=30)
```

### 5.3 Generating Reports

```python
from memory_bank.evaluation import ReportGenerator

generator = ReportGenerator(
    metrics_path="memory-bank/evaluation/metrics",
    output_path="memory-bank/evaluation/reports"
)
generator.create_daily_report()
```
