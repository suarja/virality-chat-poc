"""
Streamlit Demo App for Virality Chat POC
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.append('../src')

# Page config
st.set_page_config(
    page_title="Virality Chat POC",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main app function"""

    # Header
    st.markdown('<h1 class="main-header">📱 Virality Chat POC</h1>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choisir une page",
        ["🏠 Accueil", "📊 Exploration", "🤖 Prédiction", "📈 Insights"]
    )

    if page == "🏠 Accueil":
        show_home()
    elif page == "📊 Exploration":
        show_exploration()
    elif page == "🤖 Prédiction":
        show_prediction()
    elif page == "📈 Insights":
        show_insights()


def show_home():
    """Home page"""
    st.header("Bienvenue sur Virality Chat POC")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Objectif</h3>
            <p>Prédire la viralité des vidéos TikTok</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 IA</h3>
            <p>Analyse vidéo avec Gemini</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 ML</h3>
            <p>Modèles interprétables</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Project description
    st.subheader("À propos du projet")
    st.write("""
    Ce POC démontre la faisabilité de prédire la viralité des vidéos TikTok en combinant :
    - Scraping automatisé des données TikTok
    - Analyse vidéo avancée via IA multimodale
    - Modèles de machine learning interprétables
    - Interface utilisateur intuitive
    """)

    # Status
    st.subheader("Statut du projet")
    progress = st.progress(0)
    status_text = st.empty()

    # TODO: Update with real project status
    progress.progress(25)
    status_text.text("Phase 1: Collecte des données en cours...")


def show_exploration():
    """Data exploration page"""
    st.header("📊 Exploration des données")

    # TODO: Add data exploration visualizations
    st.info("Section en développement - Visualisations des données à venir")

    # Placeholder metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Vidéos collectées", "0", "En cours")
    with col2:
        st.metric("Comptes analysés", "0", "En cours")
    with col3:
        st.metric("Features extraites", "0", "En cours")
    with col4:
        st.metric("Taux de viralité", "0%", "En cours")


def show_prediction():
    """Prediction page"""
    st.header("🤖 Prédiction de viralité")

    # TODO: Add prediction interface
    st.info("Section en développement - Interface de prédiction à venir")

    # Placeholder form
    with st.form("prediction_form"):
        st.subheader("Analyser une vidéo")

        video_url = st.text_input("URL de la vidéo TikTok")
        analyze_button = st.form_submit_button("Analyser")

        if analyze_button and video_url:
            st.warning("Fonctionnalité en développement")


def show_insights():
    """Insights page"""
    st.header("📈 Insights et recommandations")

    # TODO: Add insights and recommendations
    st.info("Section en développement - Insights à venir")

    # Placeholder insights
    st.subheader("Facteurs de viralité identifiés")
    st.write("- Timing de publication")
    st.write("- Utilisation de hashtags populaires")
    st.write("- Durée optimale des vidéos")
    st.write("- Engagement initial")


if __name__ == "__main__":
    main()
