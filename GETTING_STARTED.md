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
# Test module imports
python -c "from src.scraping.tiktok_scraper import TikTokScraper; print('✅ Import OK')"
python -c "from src.features.data_processor import DataProcessor; print('✅ Import OK')"

# Test Jupyter
jupyter --version
```

**✅ Validation**: All commands should execute without errors.

## 🎯 Running the Pipeline

### Phase 1: Data Collection

#### 1.1 Configure TikTok Accounts

```bash
# Edit the settings file
nano config/settings.py
```

Add TikTok accounts to analyze:

```python
TIKTOK_ACCOUNTS = [
    "@username1",
    "@username2"
]
MAX_VIDEOS_PER_ACCOUNT = 50
```

#### 1.2 Run TikTok Scraping

```bash
# Run the scraping script
python scripts/run_scraping.py
```

**✅ Validation**: Check `data/raw/` for JSON files.

### Phase 2: AI Analysis

```bash
# Run Gemini analysis
python scripts/test_gemini.py
```

**✅ Validation**: Check `docs/gemini_analysis/` for analysis files.

### Phase 3: Feature Engineering

```bash
# Run feature extraction
python src/run_feature_extraction.py \
    --raw-data data/raw/test_leaelui_100642.json \
    --gemini-analysis docs/gemini_analysis \
    --output-dir data/processed
```

**✅ Validation**: Check `data/processed/` for feature files.

### Complete Pipeline

Run all phases at once:

```bash
python scripts/run_pipeline.py \
    --accounts @username1 @username2 \
    --max-videos 50 \
    --output-dir data/processed
```

## 🔧 Useful Commands

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

### Development

```bash
# Format code
black src/
black scripts/

# Run tests
pytest tests/

# Run specific test file
pytest tests/features/test_feature_extractor.py
```

### Git and Versioning

```bash
# Check status
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "✨ feat: description"  # New feature
git commit -m "🐛 fix: description"   # Bug fix
git commit -m "📝 docs: description"  # Documentation
git commit -m "♻️ refactor: description"  # Refactoring
git commit -m "🧪 test: description"  # Testing

# Push to repo
git push origin main
```

## 🚨 Common Issues Troubleshooting

### Issue 1: Import Error

**Symptom**: `ModuleNotFoundError: No module named 'src'`

**Solution**:

```bash
# Add src folder to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or in Python code
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

### Issue 2: Missing API Keys

**Symptom**: `ValueError: API token is required`

**Solution**:

1. Check `.env` file exists
2. Verify API keys are correctly filled
3. Restart Python environment

### Issue 3: Missing Dependencies

**Symptom**: `ModuleNotFoundError: No module named 'package'`

**Solution**:

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install missing package
pip install package_name
```

## 📊 Project Status Check

### Startup Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] API keys configured
- [ ] Python modules importable
- [ ] Jupyter working
- [ ] Git configured

### Diagnostic Command

```bash
python scripts/validate_setup.py
```

## 🎯 Next Steps

After setup:

1. **Start with exploration**: Check example notebooks
2. **Test scraping**: Scrape a few test videos
3. **Validate data**: Check data quality
4. **Iterate**: Progressively improve each component

## 📞 Support

If you encounter issues:

1. Check this documentation
2. Check logs in `logs/`
3. Check GitHub issues
4. Create new issue with error details

---

**Ready to start? Follow the steps above and validate each before moving to the next!** 🚀
