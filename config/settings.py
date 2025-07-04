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
    # 🎭 LIFESTYLE & DANSE
    "@leaelui",               # Danse, lifestyle, mainstream (7M+ followers)
    "@lea_mary",              # Lifestyle, mode, beauté
    "@camillelv",             # Lifestyle, mode française
    "@maeva_cook",            # Lifestyle, cuisine, quotidien

    # 😂 HUMOUR & ENTERTAINMENT
    "@athenasol",             # Humour, sketchs, pop culture
    "@mcfly_et_carlito",      # Duo humour, challenges
    "@julfou_",               # Humour, parodies
    "@cyprien",               # Humour, gaming, tech

    # 🏠 VOYAGE & DÉCOUVERTE
    "@loupernaut",            # Voyage, curiosités, info grand public
    "@partirdemain",          # Voyage, aventure
    "@thomas.pesquet",        # Espace, science, découverte

    # 🤖 TECH & IA
    "@unefille.ia",           # Actu, Tutos, Outils IA
    "@swarecito",             # Data, IA, Automatisation
    "@underscore_",           # Dev, tech, programmation
    "@hubertiming",           # Tech, innovation

    # 🍕 FOOD & CUISINE
    "@pastelcuisine",         # Food, couple, vie quotidienne
    "@swiss_fit.cook",        # Recettes gourmandes faibles calories
    "@chef.michel",           # Cuisine française traditionnelle
    "@healthyfood_creation",  # Cuisine healthy, nutrition

    # 🎮 GAMING & ESPORT
    "@gotaga",                # Gaming, esport français
    "@domingo",               # Gaming, humour gaming
    "@squeezie",              # Gaming, divertissement

    # 💪 FITNESS & SPORT
    "@tibo_inshape",          # Fitness, musculation
    "@sissy.mua",             # Fitness féminin, lifestyle
    "@coaching_nutrition",    # Fitness, nutrition

    # 🎨 ART & CRÉATIVITÉ
    "@art_side",              # Art, créativité
    "@diy_queen_",            # DIY, créativité manuelle

    # 🏢 BUSINESS & ENTREPRENEURIAT
    "@contiped",              # Rénovation piscines + humour
    "@business_life_",        # Business, entrepreneuriat
    "@lindalys1_",            # Personnel/lifestyle

    # 🎵 MUSIQUE & DANSE
    "@wejdene",               # Musique, danse
    "@aya_nakamura",          # Musique française

    # 🔬 ÉDUCATION & SCIENCE
    "@dirtybiology",          # Science, biologie
    "@scienceetonnante",      # Science, vulgarisation
]

# Configuration pour tests
TEST_ACCOUNTS = [
    "@leaelui",               # Test principal - compte stable
    "@athenasol",             # Test secondaire - humour
    "@unefille.ia",           # Test tech - niche spécialisée
]

# Feature Engineering
GEMINI_MODEL = "gemini-pro-vision"
MAX_VIDEOS_PER_ACCOUNT = 15  # Optimisé pour 33 comptes = ~500 vidéos total
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
