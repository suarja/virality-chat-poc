# TikTok Virality Analysis Pipeline

## Overview

This pipeline analyzes TikTok videos to predict and understand virality factors through three main phases:

1. **Data Collection**: Scrape TikTok videos using Apify API
2. **Content Analysis**: Analyze videos using Google's Gemini AI
3. **Feature Engineering**: Extract and combine features for modeling

## Pipeline Components

### 1. TikTok Scraping (`src/scraping/`)

- **Main Script**: `scripts/run_scraping.py`
- **Implementation**: `src/scraping/tiktok_scraper.py`
- **Configuration**: Set `APIFY_API_TOKEN` in `.env`
- **Output**: `data/raw/tiktok_*.json`

Features:

- Profile and video metadata collection
- Configurable video count per account
- Rate limiting and error handling
- Consolidated results with metadata

### 2. Gemini Analysis (`scripts/test_gemini.py`)

- **Configuration**: Set `GOOGLE_API_KEY` in `.env`
- **Output**: `docs/gemini_analysis/video_*_analysis_*.json`

Analysis Components:

- Visual elements and style
- Content structure and flow
- Engagement factors
- Technical elements
- Trend alignment
- Improvement suggestions

### 3. Feature Engineering (`src/features/`)

- **Main Script**: `src/run_feature_extraction.py`
- **Components**:
  - `feature_extractor.py`: Basic feature extraction
  - `data_processor.py`: Combine and process data
- **Output**: `data/processed/processed_features.csv`

Features Extracted:

- Basic engagement metrics
- Engagement ratios
- Content features
- Temporal patterns
- AI-powered analysis features

## Running the Pipeline

### Option 1: Complete Pipeline

Use the unified pipeline script:

```bash
python scripts/run_pipeline.py \
    --accounts @username1 @username2 \
    --max-videos 50 \
    --output-dir data/processed
```

Arguments:

- `--accounts`: TikTok accounts to analyze
- `--max-videos`: Maximum videos per account (default: 50)
- `--skip-scraping`: Skip TikTok scraping phase
- `--skip-gemini`: Skip Gemini analysis phase
- `--output-dir`: Output directory (default: data/processed)

### Option 2: Individual Components

1. **Run Scraping**:

```bash
python scripts/run_scraping.py
```

2. **Run Gemini Analysis**:

```bash
python scripts/test_gemini.py
```

3. **Run Feature Extraction**:

```bash
python src/run_feature_extraction.py \
    --raw-data data/raw/test_leaelui_100642.json \
    --gemini-analysis docs/gemini_analysis \
    --output-dir data/processed
```

## Directory Structure

```
.
├── src/
│   ├── scraping/
│   │   ├── tiktok_scraper.py
│   │   └── data_validator.py
│   └── features/
│       ├── feature_extractor.py
│       └── data_processor.py
├── scripts/
│   ├── run_pipeline.py
│   ├── run_scraping.py
│   └── test_gemini.py
├── data/
│   ├── raw/                  # TikTok data
│   └── processed/            # Feature sets
├── docs/
│   └── gemini_analysis/      # AI analysis
└── logs/                     # Pipeline logs
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

1. **Raw TikTok Data** (`data/raw/`):

- Individual files: `tiktok_username_*.json`
- Consolidated: `tiktok_consolidated_*.json`

2. **Gemini Analysis** (`docs/gemini_analysis/`):

- Analysis files: `video_*_analysis_*.json`
- Analysis logs: `logs/gemini_analysis.log`

3. **Processed Features** (`data/processed/`):

- Feature sets: `processed_features.csv`
- Processing logs: `logs/pipeline.log`

## Error Handling

The pipeline includes comprehensive error handling:

- Detailed logging at each phase
- Rate limiting for API calls
- Data validation checks
- Process metadata tracking

## Monitoring

Monitor pipeline progress through:

1. Console output with emoji indicators
2. Detailed logs in `logs/` directory
3. Metadata in output files
4. Summary statistics after each phase

## Next Steps

1. **Data Quality**:

- Implement data quality checks
- Add data versioning
- Set up automated validation

2. **Pipeline Optimization**:

- Add parallel processing
- Implement caching
- Add incremental processing

3. **Feature Engineering**:

- Add more derived features
- Implement feature selection
- Add feature importance analysis
