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
        "reports/templates"
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
    # Create .env file from template
    if Path("env.template").exists() and not Path(".env").exists():
        import shutil
        shutil.copy("env.template", ".env")
        print("✓ Created .env file from template")
        print("⚠ Please edit .env file with your API keys")
    elif Path(".env").exists():
        print("✓ .env file already exists")
    else:
        print("⚠ env.template not found")


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

    print("=" * 50)
    print("✅ Project setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Start with notebooks/01_data_exploration.ipynb")
    print("4. Run Streamlit app: streamlit run streamlit_app/app.py")


if __name__ == "__main__":
    main()
