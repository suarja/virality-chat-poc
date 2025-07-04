#!/usr/bin/env python3
"""
Setup script for Virality Chat POC project
"""
import os
import sys
from pathlib import Path
import subprocess


def create_directories():
    """Create project directory structure"""
    directories = [
        "data/raw",
        "data/processed",
        "data/external",
        "models",
        "logs",
        "reports/generated",
        "reports/templates",
        "docs/gemini_analysis"  # New directory for Gemini analysis results
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def setup_environment():
    """Setup Python environment"""
    print("Setting up Python environment...")

    # Check if virtual environment exists
    if not Path("venv").exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

    # Install requirements
    if Path("requirements.txt").exists():
        print("Installing requirements...")
        if os.name == 'nt':  # Windows
            pip_cmd = ["venv\\Scripts\\pip",
                       "install", "-r", "requirements.txt"]
        else:  # Unix/Linux/Mac
            pip_cmd = ["venv/bin/pip", "install", "-r", "requirements.txt"]

        try:
            subprocess.run(pip_cmd, check=True)
            print("✓ Requirements installed")
        except subprocess.CalledProcessError:
            print("⚠ Failed to install requirements automatically")
            print("Please run: pip install -r requirements.txt")
    else:
        print("⚠ requirements.txt not found")


def setup_config():
    """Setup configuration files"""
    # Create .env file from template if it doesn't exist
    if Path("env.template").exists() and not Path(".env").exists():
        import shutil
        shutil.copy("env.template", ".env")
        print("✓ Created .env file from template")
        print("⚠ Please edit .env file with your API keys (APIFY_API_TOKEN and GOOGLE_API_KEY)")
    elif Path(".env").exists():
        print("✓ .env file already exists")
    else:
        # Create minimal .env template
        with open(".env", "w") as f:
            f.write("# API Keys\n")
            f.write("APIFY_API_TOKEN=your_apify_token_here\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
        print("✓ Created minimal .env file")
        print("⚠ Please edit .env file with your API keys")


def setup_documentation():
    """Setup documentation files"""
    docs_path = Path("docs")
    docs_path.mkdir(exist_ok=True)

    # Create or update README.md if it doesn't exist
    readme_path = Path("README.md")
    if not readme_path.exists():
        with open(readme_path, "w") as f:
            f.write("# Virality Chat POC\n\n")
            f.write("## Overview\n")
            f.write(
                "TikTok video analysis tool using Gemini AI for virality prediction.\n\n")
            f.write("## Setup\n")
            f.write("1. Clone the repository\n")
            f.write("2. Run setup script: `python scripts/setup_project.py`\n")
            f.write("3. Configure API keys in `.env`:\n")
            f.write("   - APIFY_API_TOKEN for TikTok scraping\n")
            f.write("   - GOOGLE_API_KEY for Gemini AI\n")
            f.write("4. Activate virtual environment:\n")
            f.write("   - Windows: `venv\\Scripts\\activate`\n")
            f.write("   - Unix/Mac: `source venv/bin/activate`\n")
            f.write("5. Validate setup: `python scripts/validate_setup.py`\n\n")
            f.write("## Features\n")
            f.write("- TikTok video scraping\n")
            f.write("- Video analysis with Gemini AI\n")
            f.write("- Virality prediction\n")
            f.write("- Interactive dashboard\n")
        print("✓ Created README.md")

    # Create Gemini documentation
    gemini_docs_path = docs_path / "gemini_analysis.md"
    if not gemini_docs_path.exists():
        with open(gemini_docs_path, "w") as f:
            f.write("# Gemini Video Analysis\n\n")
            f.write("## Overview\n")
            f.write(
                "This document describes the video analysis capabilities using Google's Gemini AI.\n\n")
            f.write("## Features\n")
            f.write("- Visual content analysis\n")
            f.write("- Engagement factor detection\n")
            f.write("- Trend identification\n")
            f.write("- Virality potential assessment\n\n")
            f.write("## Usage\n")
            f.write("1. Ensure GOOGLE_API_KEY is set in .env\n")
            f.write("2. Use test_gemini.py for initial testing\n")
            f.write("3. Check docs/gemini_analysis/ for analysis results\n\n")
            f.write("## Cost Optimization\n")
            f.write("- Low resolution mode: ~$0.55/500 videos\n")
            f.write("- Normal resolution mode: ~$0.85/500 videos\n")
            f.write("- Recommended: Start with test phase (50 videos)\n")
        print("✓ Created Gemini documentation")


def main():
    """Main setup function"""
    print("🚀 Setting up Virality Chat POC project...")
    print("=" * 50)

    create_directories()
    print()

    setup_environment()
    print()

    setup_config()
    print()

    setup_documentation()
    print()

    print("=" * 50)
    print("✅ Project setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys:")
    print("   - APIFY_API_TOKEN for TikTok scraping")
    print("   - GOOGLE_API_KEY for Gemini AI")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Test Gemini setup: python test_gemini.py")
    print("4. Start with notebooks/01_data_exploration.ipynb")
    print("5. Run Streamlit app: streamlit run streamlit_app/app.py")


if __name__ == "__main__":
    main()
