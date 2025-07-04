# TikTok Video Virality Analysis

> Predict and understand TikTok video virality through AI analysis and feature engineering

## Overview

This project implements a complete pipeline for analyzing TikTok video virality:

1. **Data Collection**: Automated TikTok video scraping
2. **Content Analysis**: AI-powered video analysis using Google's Gemini
3. **Feature Engineering**: Comprehensive feature extraction and processing

## Features

- **TikTok Data Collection**:
  - Profile and video metadata scraping
  - Configurable video count per account
  - Rate limiting and error handling
- **AI Video Analysis**:
  - Visual elements and style analysis
  - Content structure evaluation
  - Engagement factor prediction
  - Technical quality assessment
  - Trend alignment analysis
- **Feature Engineering**:
  - Basic engagement metrics
  - Engagement ratios
  - Content features
  - Temporal patterns
  - AI-powered analysis features

## Quick Start

1. **Setup Environment**:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure API Keys**:

```bash
# Create .env file
cp .env.template .env

# Add your API keys
APIFY_API_TOKEN=your_apify_token
GOOGLE_API_KEY=your_gemini_key
```

3. **Run Complete Pipeline**:

```bash
# Run with default settings
python scripts/run_pipeline.py --accounts @username1 @username2

# Or run individual components
python scripts/run_scraping.py        # 1. Scrape TikTok
python scripts/test_gemini.py         # 2. Run AI analysis
python src/run_feature_extraction.py  # 3. Extract features
```

## Project Structure

```
.
├── src/
│   ├── scraping/              # TikTok scraping
│   │   ├── tiktok_scraper.py
│   │   └── data_validator.py
│   └── features/              # Feature engineering
│       ├── feature_extractor.py
│       └── data_processor.py
├── scripts/                   # Pipeline scripts
│   ├── run_pipeline.py       # Complete pipeline
│   ├── run_scraping.py       # TikTok scraping
│   └── test_gemini.py        # Gemini analysis
├── data/
│   ├── raw/                  # TikTok data
│   └── processed/            # Feature sets
├── docs/
│   ├── pipeline.md           # Pipeline documentation
│   └── gemini_analysis/      # AI analysis results
├── notebooks/                # Analysis notebooks
│   ├── 01_feature_extraction_demo.ipynb
│   └── 02_data_processing_demo.ipynb
├── logs/                     # Pipeline logs
├── requirements.txt
└── README.md
```

## Documentation

- [Pipeline Documentation](docs/pipeline.md): Complete pipeline details
- [Feature Engineering](docs/feature_engineering.md): Feature documentation
- [Gemini Analysis](docs/gemini_analysis/README.md): AI analysis details

## Usage Examples

### 1. Complete Pipeline

Run the entire analysis pipeline:

```bash
python scripts/run_pipeline.py \
    --accounts @username1 @username2 \
    --max-videos 50 \
    --output-dir data/processed
```

Options:

- `--accounts`: TikTok accounts to analyze
- `--max-videos`: Maximum videos per account
- `--skip-scraping`: Skip TikTok scraping
- `--skip-gemini`: Skip Gemini analysis
- `--output-dir`: Output directory

### 2. Individual Components

Run components separately:

1. **TikTok Scraping**:

```bash
python scripts/run_scraping.py
```

2. **Gemini Analysis**:

```bash
python scripts/test_gemini.py
```

3. **Feature Extraction**:

```bash
python src/run_feature_extraction.py \
    --raw-data data/raw/test_leaelui_100642.json \
    --gemini-analysis docs/gemini_analysis \
    --output-dir data/processed
```

## Output

The pipeline generates:

1. **Raw Data** (`data/raw/`):

   - TikTok video metadata
   - Profile information
   - Engagement metrics

2. **AI Analysis** (`docs/gemini_analysis/`):

   - Visual content analysis
   - Engagement predictions
   - Improvement suggestions

3. **Features** (`data/processed/`):
   - Processed feature sets
   - Validation metadata
   - Processing logs

## Development

1. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

2. Run tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific component
pytest tests/features/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details
