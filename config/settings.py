"""
Configuration settings for Virality Chat POC
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, MODELS_DIR, REPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Configuration
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Backup option

# Scraping Configuration
TIKTOK_ACCOUNTS = [
    "@leaelui",               # Danse, lifestyle, mainstream
    "@athenasol",           # Humour, sketchs, pop culture
    "@loupernaut",            # Voyage, curiosités, info grand public
    "@unefille.ia",        # 🛑 Actu, Tutos, Outils IA 🛑
    "@pastelcuisine",       # Food, couple, vie quotidienne (moyenne audience)
    "@lindalys1_",
    "@swarecito",  # 🛑 Data, IA, Automatisation 🛑
    "@contiped",  # Je rénove vos piscine pour cet été🏝️🌊 N'hésitez pas a vous abonner✅🎯 humour❤️
    # Recettes gourmandes et faibles en calories! 🍕 50 Suivis 144.9K Followers 717.4K J'aime
    "@swiss_fit.cook",


]

# Feature Engineering
GEMINI_MODEL = "gemini-pro-vision"
MAX_VIDEOS_PER_ACCOUNT = 35  # Optimisé selon research synthesis
MIN_VIEWS_THRESHOLD = 1000

# ML Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Virality Thresholds (basé sur research synthesis)
VIRALITY_THRESHOLDS = {
    "low": 10000,        # 10K views - micro-viral
    "medium": 100000,    # 100K views - viral
    "high": 1000000,     # 1M views - méga-viral
}

# Features prioritaires (research-based)
PRIMARY_FEATURES = [
    'view_count', 'like_count', 'comment_count', 'share_count',
    'video_duration', 'hashtags_count', 'description_length',
    'account_followers', 'account_verification', 'publish_hour',
    'publish_day_of_week', 'trending_sound_usage'
]

VISUAL_FEATURES = [
    'human_presence', 'face_count', 'movement_intensity',
    'color_vibrancy', 'scene_changes', 'text_overlay_presence',
    'lighting_quality', 'video_style'
]

# Streamlit Configuration
STREAMLIT_PORT = 8501
STREAMLIT_HOST = "localhost"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
