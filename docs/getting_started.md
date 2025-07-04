# 🚀 Getting Started - TikTok Virality Analysis

## ✅ Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **Git** installed
- An **Apify** account (for TikTok scraping)
- A **Google Gemini** API key (for video analysis)

## 📋 Setup Steps

### Step 1: Clone and Configure Project

```bash
# Clone the project if not done already
git clone <your-repo-url>
cd virality-chat-poc

# Run the automated setup script
python scripts/setup_project.py
```

**✅ Validation**: You should see:

```
✓ Created directory: data/raw
✓ Created directory: data/processed
✓ Created directory: docs/gemini_analysis
✓ Created directory: logs
✓ Virtual environment created
✓ Requirements installed
✓ Created .env file from template
```

### Step 2: Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

**✅ Validation**: Your terminal should show `(venv)` at the start of the line.

### Step 3: Configure API Keys

```bash
# Edit the .env file
nano .env  # or your preferred editor
```

Fill in with your actual API keys:

```env
APIFY_API_TOKEN=your_apify_token_here
GOOGLE_API_KEY=your_gemini_key_here
DEBUG=True
LOG_LEVEL=INFO
```

**✅ Validation**: Verify that `.env` exists and contains your keys.

### Step 4: Test Installation

```bash
# Test the batch processing system
python scripts/test_batch_system.py

# Run the validation script
python scripts/validate_setup.py

# Test Jupyter (if needed)
jupyter --version
```

**✅ Validation**: All commands should execute without errors.

## 🎯 Running the Pipeline

### New Batch Processing System

The pipeline now uses a sophisticated batch processing system that:

- **Processes accounts in configurable batches** (default: 5 accounts per batch)
- **Tracks progress** in `source.txt` to avoid reprocessing
- **Logs errors** in `errors.txt` for debugging and retry
- **Supports resuming** from where it left off
- **Limits total videos** to prevent excessive processing

### Basic Pipeline Run

```bash
# Run with default settings (5 accounts per batch, 15 videos per account)
python scripts/run_pipeline.py --dataset v1

# Run with custom batch size
python scripts/run_pipeline.py --dataset v1 --batch-size 3

# Run with custom video limits
python scripts/run_pipeline.py --dataset v1 --videos-per-account 10 --max-total-videos 300
```

### Advanced Pipeline Options

```bash
# Retry failed accounts from previous runs
python scripts/run_pipeline.py --dataset v1 --retry-failed

# Retry only specific phase for failed accounts
python scripts/run_pipeline.py --dataset v1 --retry-failed --retry-phase analysis

# Small test run
python scripts/run_pipeline.py --dataset test --batch-size 1 --videos-per-account 2
```

### Pipeline Output Structure

```
data/
├── dataset_v1/
│   ├── source.txt          # List of processed accounts
│   ├── errors.txt          # Error tracking
│   └── metadata.json       # Dataset metadata
├── raw/
│   └── dataset_v1/
│       └── batch_*.json    # Consolidated video data
├── analysis/
│   └── dataset_v1/
│       └── gemini_*.json   # Gemini analysis results
└── features/
    └── dataset_v1/
        └── features.csv    # Final feature dataset
```

### Monitoring Progress

```bash
# Check processing status
cat data/dataset_v1/source.txt

# Check for errors
cat data/dataset_v1/errors.txt

# View pipeline logs
tail -f logs/pipeline_v1.log

# View error logs
tail -f logs/errors.log
```

## 🔧 Development Commands

### Environment Management

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate environment
deactivate

# Install new dependencies
pip install package_name
pip freeze > requirements.txt  # Update requirements.txt
```

### Testing

```bash
# Test batch processing system
python scripts/test_batch_system.py

# Run scraping tests
python scripts/test_scraping.py

# Run Gemini analysis tests
python scripts/test_gemini.py

# Run all unit tests
pytest

# Run with coverage
pytest --cov=src tests/
```

### Code Quality

```bash
# Format code
black src/ tests/ scripts/

# Run linting
flake8 src/ tests/ scripts/
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Add to PYTHONPATH if needed
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **API Key Issues**

   - Check `.env` file exists and is properly formatted
   - Verify API keys are valid
   - Restart Python environment

3. **Missing Dependencies**
   ```bash
   # Reinstall all dependencies
   pip install -r requirements.txt
   ```

4. **Batch Processing Issues**

   - Check `source.txt` for processed accounts
   - Review `errors.txt` for specific error details
   - Use `--retry-failed` to retry failed accounts

### Getting Help

1. Check the logs in `logs/` directory
2. Review `data/dataset_*/errors.txt` for specific errors
3. Run `python scripts/validate_setup.py --verbose`
4. See [project documentation](docs/)

## 📊 Dataset Management

### Creating New Datasets

```bash
# Create a new dataset
python scripts/run_pipeline.py --dataset v2 --batch-size 3

# Continue processing existing dataset
python scripts/run_pipeline.py --dataset v1 --batch-size 5
```

### Dataset Versioning

- Each dataset has its own directory structure
- Progress is tracked independently per dataset
- Features are consolidated per dataset
- Easy to compare different dataset versions

### Quality Control

- Minimum 1,000 views per video
- Maximum 6 months video age
- Automatic duplicate detection
- Error tracking and reporting
