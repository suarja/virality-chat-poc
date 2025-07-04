# TikTok Virality Analysis Pipeline

## Overview

This pipeline analyzes TikTok videos to predict and understand virality factors through three main phases with advanced batch processing:

1. **Data Collection**: Scrape TikTok videos using Apify API (batch processing)
2. **Content Analysis**: Analyze videos using Google's Gemini AI (batch processing)
3. **Feature Engineering**: Extract and combine features for modeling (batch processing)

## 🆕 New Batch Processing System

### Key Features

- **Configurable Batch Sizes**: Process 1-10 accounts per batch
- **Progress Tracking**: Automatic tracking in `source.txt`
- **Error Management**: Detailed error logging in `errors.txt`
- **Resume Capability**: Continue from where it left off
- **Retry System**: Retry failed accounts or specific phases
- **Dataset Versioning**: Multiple dataset versions with independent tracking

### Architecture

```
Pipeline Flow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Batch Input   │───▶│  Phase 1:       │───▶│  Phase 2:       │
│   (N accounts)  │    │  Scraping       │    │  Gemini         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Save Raw Data  │    │  Save Analysis  │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Phase 3:       │
                                               │  Features       │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Mark Complete  │
                                               │  Update source  │
                                               └─────────────────┘
```

## Pipeline Components

### 1. Batch Tracker (`src/utils/batch_tracker.py`)

**Core Functionality:**

- Track processed accounts in `source.txt`
- Log errors by phase in `errors.txt`
- Provide batch management utilities
- Generate progress summaries

**Key Methods:**

```python
tracker = BatchTracker("dataset_name")
tracker.get_next_batch(accounts, batch_size)
tracker.mark_account_processed(account)
tracker.log_error(account, phase, error)
tracker.summarize_progress()
```

### 2. TikTok Scraping (`src/scraping/`)

- **Main Script**: Integrated into `run_pipeline.py`
- **Implementation**: `src/scraping/tiktok_scraper.py`
- **Configuration**: Set `APIFY_API_TOKEN` in `.env`
- **Output**: `data/raw/dataset_*/batch_*.json`

**Features:**

- Profile and video metadata collection
- Configurable video count per account
- Rate limiting and error handling
- Batch-based processing

### 3. Gemini Analysis (`scripts/test_gemini.py`)

- **Configuration**: Set `GOOGLE_API_KEY` in `.env`
- **Output**: `data/analysis/dataset_*/gemini_*.json`

**Analysis Components:**

- Visual elements and style
- Content structure and flow
- Engagement factors
- Technical elements
- Trend alignment
- Improvement suggestions

### 4. Feature Engineering (`src/features/`)

- **Main Script**: Integrated into `run_pipeline.py`
- **Components**:
  - `feature_extractor.py`: Basic feature extraction
  - `data_processor.py`: Combine and process data
- **Output**: `data/features/dataset_*/features.csv`

**Features Extracted:**

- Basic engagement metrics
- Engagement ratios
- Content features
- Temporal patterns
- AI-powered analysis features

## Running the Pipeline

### Basic Usage

```bash
# Run with default settings
python scripts/run_pipeline.py --dataset v1

# Custom batch size
python scripts/run_pipeline.py --dataset v1 --batch-size 3

# Custom video limits
python scripts/run_pipeline.py --dataset v1 --videos-per-account 10 --max-total-videos 300
```

### Advanced Options

```bash
# Retry failed accounts
python scripts/run_pipeline.py --dataset v1 --retry-failed

# Retry specific phase
python scripts/run_pipeline.py --dataset v1 --retry-failed --retry-phase analysis

# Test run
python scripts/run_pipeline.py --dataset test --batch-size 1 --videos-per-account 2
```

### Command Line Arguments

| Argument               | Type | Default  | Description                   |
| ---------------------- | ---- | -------- | ----------------------------- |
| `--dataset`            | str  | Required | Dataset name (e.g., v1, test) |
| `--batch-size`         | int  | 5        | Accounts per batch            |
| `--videos-per-account` | int  | 15       | Videos per account            |
| `--max-total-videos`   | int  | 500      | Maximum total videos          |
| `--retry-failed`       | flag | False    | Retry failed accounts         |
| `--retry-phase`        | str  | None     | Specific phase to retry       |

## Directory Structure

```
.
├── src/
│   ├── scraping/
│   │   ├── tiktok_scraper.py
│   │   └── data_validator.py
│   ├── features/
│   │   ├── feature_extractor.py
│   │   └── data_processor.py
│   └── utils/
│       └── batch_tracker.py
├── scripts/
│   ├── run_pipeline.py
│   ├── test_batch_system.py
│   └── test_gemini.py
├── data/
│   ├── dataset_v1/
│   │   ├── source.txt          # Processed accounts
│   │   ├── errors.txt          # Error tracking
│   │   └── metadata.json       # Dataset metadata
│   ├── raw/
│   │   └── dataset_v1/
│   │       └── batch_*.json    # Consolidated video data
│   ├── analysis/
│   │   └── dataset_v1/
│   │       └── gemini_*.json   # AI analysis results
│   └── features/
│       └── dataset_v1/
│           └── features.csv    # Final feature dataset
├── logs/
│   ├── pipeline_v1.log         # Pipeline logs
│   └── errors.log              # Error logs
└── docs/
    └── gemini_analysis/        # Legacy analysis files
```

## Configuration

1. Create `.env` file:

```bash
APIFY_API_TOKEN=your_apify_token
GOOGLE_API_KEY=your_gemini_key
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Output Files

### 1. Dataset Tracking (`data/dataset_*/`)

- **source.txt**: List of successfully processed accounts
- **errors.txt**: Error details by account and phase
- **metadata.json**: Dataset configuration and statistics

### 2. Raw TikTok Data (`data/raw/dataset_*/`)

- **batch\_\*.json**: Consolidated video data per batch
- Format: `batch_YYYYMMDD_HHMMSS.json`

### 3. Gemini Analysis (`data/analysis/dataset_*/`)

- **gemini\_\*.json**: Analysis results per video
- Format: `gemini_video_id_analysis.json`

### 4. Processed Features (`data/features/dataset_*/`)

- **features.csv**: Consolidated feature dataset
- **metadata.json**: Feature extraction metadata

## Error Handling

The pipeline includes comprehensive error handling:

- **Phase-specific error tracking**
- **Automatic retry capabilities**
- **Detailed error logging**
- **Progress preservation**
- **Batch-level error isolation**

### Error Recovery

```bash
# Check for errors
cat data/dataset_v1/errors.txt

# Retry all failed accounts
python scripts/run_pipeline.py --dataset v1 --retry-failed

# Retry only analysis phase
python scripts/run_pipeline.py --dataset v1 --retry-failed --retry-phase analysis
```

## Monitoring

Monitor pipeline progress through:

1. **Console output** with emoji indicators
2. **Detailed logs** in `logs/pipeline_*.log`
3. **Progress tracking** in `source.txt`
4. **Error monitoring** in `errors.txt`
5. **Summary statistics** after each batch

### Progress Commands

```bash
# Check processing status
cat data/dataset_v1/source.txt

# Monitor logs in real-time
tail -f logs/pipeline_v1.log

# Check error count
wc -l data/dataset_v1/errors.txt
```

## Quality Control

### Data Validation

- **Minimum views threshold**: 1,000 views
- **Maximum video age**: 6 months
- **Required fields completeness**
- **Data type validation**
- **Range checks**

### Feature Validation

- **Completeness checks** (null values)
- **Range validation** (outliers)
- **Cross-feature correlation analysis**
- **Temporal consistency**

## Next Steps

### 1. Feature Enhancement

- [ ] Add audio analysis features
- [ ] Implement trend detection
- [ ] Add cross-platform metrics
- [ ] Enhance visual analysis

### 2. Pipeline Optimization

- [ ] Add parallel processing
- [ ] Implement caching
- [ ] Add incremental processing
- [ ] Optimize memory usage

### 3. Model Development

- [ ] Implement baseline models
- [ ] Add feature selection
- [ ] Create ensemble models
- [ ] Add interpretability tools

### 4. Monitoring & Alerting

- [ ] Add performance metrics
- [ ] Implement alerting system
- [ ] Add dashboard
- [ ] Create automated reports
