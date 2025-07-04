# TikTok Virality Analysis Pipeline

A comprehensive pipeline for analyzing TikTok videos to predict and understand virality factors using batch processing, AI analysis, and robust data validation.

## 🚀 Features

### ✅ Batch Processing System

- **Configurable batch sizes** (1-10 accounts per batch)
- **Progress tracking** with automatic resume capability
- **Error handling** with detailed logging and retry mechanisms
- **Dataset versioning** for multiple experiments

### ✅ Data Validation Guards

- **Account validation** (username, video count, data integrity)
- **Video filtering** (minimum views, age limits, sponsored content detection)
- **Quality thresholds** (engagement metrics, duration limits)
- **Analysis validation** (Gemini completeness checks)

### ✅ AI-Powered Analysis

- **Google Gemini integration** for video content analysis
- **Visual element detection** (lighting, composition, movement)
- **Content structure analysis** (narrative flow, engagement factors)
- **Technical quality assessment** (audio, transitions, style)

### ✅ Feature Engineering

- **Engagement metrics** (views, likes, comments, shares)
- **Temporal features** (posting time, day patterns)
- **Content features** (hashtags, descriptions, music)
- **AI-derived features** (visual analysis, content categories)

## 📋 Quick Start

### 1. Setup

```bash
# Clone and setup
git clone <repository-url>
cd virality-chat-poc
python scripts/setup_project.py

# Activate environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### 2. Test Installation

```bash
# Test batch processing system
python scripts/test_batch_system.py

# Test data validation
python scripts/test_data_validation.py

# Validate setup
python scripts/validate_setup.py
```

### 3. Run Pipeline

```bash
# Basic run (5 accounts per batch, 15 videos per account)
python scripts/run_pipeline.py --dataset v1

# Custom configuration
python scripts/run_pipeline.py \
    --dataset v1 \
    --batch-size 3 \
    --videos-per-account 10 \
    --max-total-videos 300

# Test run
python scripts/run_pipeline.py \
    --dataset test \
    --batch-size 1 \
    --videos-per-account 2
```

## 🏗️ Architecture

```
Pipeline Flow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Batch Input   │───▶│  Phase 1:       │───▶│  Phase 2:       │
│   (N accounts)  │    │  Scraping +     │    │  Gemini         │
│                 │    │  Validation     │    │  Analysis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Save Raw Data  │    │  Save Analysis  │
                       │  + Track        │    │  + Validate     │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Phase 3:       │
                                               │  Features       │
                                               │  Extraction     │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Mark Complete  │
                                               │  Update source  │
                                               └─────────────────┘
```

## 📊 Data Quality Controls

### Validation Rules

- **Minimum views**: 1,000 per video
- **Maximum age**: 6 months
- **Duration limits**: 1-600 seconds
- **Content filtering**: No sponsored content
- **Required fields**: All metadata present
- **Analysis quality**: Complete Gemini analysis

### Error Handling

- **Automatic retry**: Failed accounts retry mechanism
- **Progress preservation**: Resume from where it left off
- **Detailed logging**: Complete error tracking
- **Quality assurance**: Data validation at each step

## 📁 Directory Structure

```
.
├── src/
│   ├── scraping/
│   │   └── tiktok_scraper.py      # TikTok data collection
│   ├── features/
│   │   └── data_processor.py      # Feature extraction
│   └── utils/
│       ├── batch_tracker.py       # Progress tracking
│       └── data_validator.py      # Data validation
├── scripts/
│   ├── run_pipeline.py            # Main pipeline
│   ├── test_batch_system.py       # Batch tests
│   └── test_data_validation.py    # Validation tests
├── data/
│   ├── dataset_v1/
│   │   ├── source.txt             # Processed accounts
│   │   ├── errors.txt             # Error tracking
│   │   └── metadata.json          # Dataset info
│   ├── raw/
│   │   └── dataset_v1/
│   │       └── batch_*.json       # Raw video data
│   ├── analysis/
│   │   └── dataset_v1/
│   │       └── gemini_*.json      # AI analysis
│   └── features/
│       └── dataset_v1/
│           └── features.csv       # Final dataset
├── logs/
│   ├── pipeline_*.log             # Pipeline logs
│   └── errors.log                 # Error logs
└── docs/
    ├── getting_started.md         # Setup guide
    ├── pipeline.md                # Technical docs
    └── features_tracking.md       # Feature status
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
APIFY_API_TOKEN=your_apify_token
GOOGLE_API_KEY=your_gemini_key

# Optional
DEBUG=True
LOG_LEVEL=INFO
```

### Settings (`config/settings.py`)

```python
# Account configuration
TIKTOK_ACCOUNTS = ["@account1", "@account2", ...]

# Processing limits
MAX_VIDEOS_PER_ACCOUNT = 15
MIN_VIEWS_THRESHOLD = 1000

# Quality thresholds
VIRALITY_THRESHOLDS = {
    'low': 10000,
    'medium': 100000,
    'high': 1000000,
}
```

## 📈 Monitoring

### Progress Tracking

```bash
# Check processing status
cat data/dataset_v1/source.txt

# Monitor errors
cat data/dataset_v1/errors.txt

# View logs
tail -f logs/pipeline_v1.log
```

### Quality Metrics

```bash
# Dataset quality report
python scripts/validate_dataset.py --dataset v1

# Feature completeness check
python scripts/check_features.py --dataset v1
```

## 🧪 Testing

### Unit Tests

```bash
# Test batch processing
python scripts/test_batch_system.py

# Test data validation
python scripts/test_data_validation.py

# Test scraping
python scripts/test_scraping.py

# Test Gemini analysis
python scripts/test_gemini.py
```

### Integration Tests

```bash
# Full pipeline test
python scripts/run_pipeline.py --dataset test --batch-size 1

# Error recovery test
python scripts/run_pipeline.py --dataset v1 --retry-failed
```

## 🚨 Troubleshooting

### Common Issues

1. **API Rate Limits**: Automatic retry with exponential backoff
2. **Network Errors**: Logged and retried automatically
3. **Data Corruption**: Filtered out by validation guards
4. **Memory Issues**: Batch processing prevents memory overflow

### Debug Commands

```bash
# Check API keys
python scripts/validate_setup.py

# Test individual components
python scripts/test_scraping.py
python scripts/test_gemini.py

# Validate data quality
python scripts/test_data_validation.py
```

## 📚 Documentation

- **[Getting Started](docs/getting_started.md)**: Setup and first run
- **[Pipeline Guide](docs/pipeline.md)**: Technical implementation
- **[Features Tracking](docs/features_tracking.md)**: Development status
- **[Research Synthesis](docs/articles/research_synthesis.md)**: Academic foundation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Research based on academic papers in `docs/articles/`
- Powered by Google Gemini AI
- Data collection via Apify API
