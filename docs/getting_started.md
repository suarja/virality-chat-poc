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
# Run the validation script
python scripts/validate_setup.py

# Test Jupyter (if needed)
jupyter --version
```

**✅ Validation**: All commands should execute without errors.

## 🎯 Running the Pipeline

### Phase 1: Data Collection

```bash
# Run the scraping script with default settings (uses config/settings.py values)
python scripts/run_scraping.py

# Or with custom parameters
python scripts/run_scraping.py --accounts @username1 @username2 --max-videos 50

# Check the results
ls -la data/raw/
```

**✅ Validation**:

- Check `data/raw/` for individual JSON files (format: `tiktok_username_*.json`)
- A consolidated file will be created (format: `tiktok_consolidated_YYYYMMDD_HHMMSS.json`)

### Phase 2: AI Analysis

```bash
# Run Gemini analysis on scraped videos
python scripts/run_pipeline.py --skip-scraping

# Or run analysis on specific accounts
python scripts/run_pipeline.py --accounts @username1 @username2 --max-videos 50 --skip-scraping
```

**✅ Validation**:

- Check `docs/gemini_analysis/` for analysis files
- Each video will have its own JSON file (format: `video_N_analysis_YYYYMMDD_HHMMSS.json`)

### Phase 3: Evaluation

```bash
# Run evaluation on the collected data
python scripts/run_evaluation.py

# Check the evaluation results
cat logs/evaluation.log
```

**✅ Validation**:

- Check `logs/evaluation.log` for detailed evaluation results
- Review any warnings or quality issues identified

### Complete Pipeline

Run all phases at once:

```bash
# Run complete pipeline with default settings
python scripts/run_pipeline.py

# Run with custom parameters
python scripts/run_pipeline.py \
    --accounts @username1 @username2 \
    --max-videos 50
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

### Getting Help

1. Check the logs in `logs/` directory
2. Run `python scripts/validate_setup.py --verbose`
3. See [project documentation](docs/)
