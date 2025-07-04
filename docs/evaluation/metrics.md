# Evaluation Metrics Documentation

## Overview

This document details the metrics used to evaluate our TikTok virality prediction system, including their definitions, implementation, and interpretation.

## Feature Extraction Metrics

### Visual Analysis Quality

```python
class VisualAnalysisMetrics:
    """
    Evaluates the quality of visual feature extraction from TikTok videos.
    """
    def __init__(self):
        self.metrics = {
            'object_detection': {
                'precision': 0.0,
                'recall': 0.0,
                'confidence': 0.0
            },
            'scene_understanding': {
                'accuracy': 0.0,
                'completeness': 0.0
            },
            'movement_analysis': {
                'accuracy': 0.0,
                'temporal_consistency': 0.0
            }
        }
```

### Audio Analysis Quality

```python
class AudioAnalysisMetrics:
    """
    Evaluates the quality of audio feature extraction.
    """
    def __init__(self):
        self.metrics = {
            'speech_recognition': {
                'word_error_rate': 0.0,
                'confidence': 0.0
            },
            'music_detection': {
                'accuracy': 0.0,
                'genre_classification': 0.0
            },
            'sound_effects': {
                'detection_rate': 0.0,
                'classification_accuracy': 0.0
            }
        }
```

### Text Analysis Quality

```python
class TextAnalysisMetrics:
    """
    Evaluates the quality of text feature extraction from captions, hashtags, etc.
    """
    def __init__(self):
        self.metrics = {
            'caption_analysis': {
                'sentiment_accuracy': 0.0,
                'topic_classification': 0.0
            },
            'hashtag_analysis': {
                'relevance_score': 0.0,
                'trend_correlation': 0.0
            }
        }
```

## Prediction Quality Metrics

### Virality Score Metrics

```python
class ViralityMetrics:
    """
    Evaluates the accuracy of virality predictions.
    """
    def __init__(self):
        self.metrics = {
            'engagement_prediction': {
                'mae': 0.0,  # Mean Absolute Error
                'rmse': 0.0,  # Root Mean Square Error
                'r2': 0.0    # R-squared score
            },
            'trend_prediction': {
                'accuracy': 0.0,
                'f1_score': 0.0,
                'auc_roc': 0.0
            },
            'time_to_viral': {
                'mae_hours': 0.0,
                'prediction_horizon': 0.0
            }
        }
```

## System Performance Metrics

### Processing Efficiency

```python
class SystemMetrics:
    """
    Evaluates system performance and resource utilization.
    """
    def __init__(self):
        self.metrics = {
            'processing_time': {
                'feature_extraction_ms': 0.0,
                'prediction_ms': 0.0,
                'total_latency_ms': 0.0
            },
            'resource_usage': {
                'cpu_utilization': 0.0,
                'memory_usage_mb': 0.0,
                'api_calls_per_video': 0
            },
            'reliability': {
                'success_rate': 0.0,
                'error_rate': 0.0,
                'retry_rate': 0.0
            }
        }
```

## Implementation Details

### 1. Metric Collection

```python
class MetricCollector:
    def __init__(self):
        self.visual_metrics = VisualAnalysisMetrics()
        self.audio_metrics = AudioAnalysisMetrics()
        self.text_metrics = TextAnalysisMetrics()
        self.virality_metrics = ViralityMetrics()
        self.system_metrics = SystemMetrics()

    def collect_batch_metrics(self, batch_results):
        """
        Collects metrics for a batch of processed videos.
        """
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'batch_id': str(uuid.uuid4()),
            'sample_size': len(batch_results),
            'metrics': {
                'visual': self.visual_metrics.compute(batch_results),
                'audio': self.audio_metrics.compute(batch_results),
                'text': self.text_metrics.compute(batch_results),
                'virality': self.virality_metrics.compute(batch_results),
                'system': self.system_metrics.compute(batch_results)
            }
        }
        return metrics
```

### 2. Metric Storage

```python
class MetricStorage:
    def __init__(self, base_path="data/evaluation/metrics"):
        self.base_path = base_path
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def save_metrics(self, metrics):
        """
        Saves metrics to appropriate storage location.
        """
        # Daily metrics
        daily_path = f"{self.base_path}/daily/{self.current_date}.json"
        self._save_json(daily_path, metrics)

        # Update running averages
        self._update_running_averages(metrics)
```

### 3. Metric Analysis

```python
class MetricAnalyzer:
    def __init__(self):
        self.thresholds = self._load_thresholds()

    def analyze_metrics(self, metrics):
        """
        Analyzes metrics against thresholds and historical data.
        """
        analysis = {
            'status': 'green',  # green, yellow, red
            'alerts': [],
            'improvements': [],
            'degradations': []
        }

        # Check each metric against thresholds
        for category, values in metrics.items():
            self._check_thresholds(category, values, analysis)

        return analysis
```

## Interpretation Guidelines

### Visual Analysis Metrics

- **Completeness**: >95% indicates good feature coverage
- **Accuracy**: >90% indicates reliable feature extraction
- **Consistency**: >85% indicates stable processing

### Prediction Metrics

- **Accuracy**: >80% indicates good prediction quality
- **Calibration**: >85% indicates reliable confidence scores
- **Timeliness**: <2hrs indicates good early prediction

### System Metrics

- **Latency**: <3min per video is acceptable
- **Resource Usage**: <70% is efficient
- **Error Rate**: <5% is reliable

## Alert Thresholds

```yaml
thresholds:
  critical:
    accuracy: 0.75
    latency_ms: 240000 # 4 minutes
    error_rate: 0.08
  warning:
    accuracy: 0.85
    latency_ms: 180000 # 3 minutes
    error_rate: 0.05
```
