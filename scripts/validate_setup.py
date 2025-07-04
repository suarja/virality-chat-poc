#!/usr/bin/env python3
"""
Script de validation pour vérifier la configuration du projet
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Vérifier la version de Python"""
    print("🔍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} - Version 3.9+ requise")
        return False


def check_virtual_environment():
    """Vérifier l'environnement virtuel"""
    print("🔍 Vérification de l'environnement virtuel...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Environnement virtuel activé")
        return True
    else:
        print("❌ Environnement virtuel non activé")
        print("💡 Exécutez: source venv/bin/activate (Linux/Mac) ou venv\\Scripts\\activate (Windows)")
        return False


def check_dependencies():
    """Vérifier les dépendances"""
    print("🔍 Vérification des dépendances...")
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'streamlit',
        'plotly', 'jupyter', 'requests'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} OK")
        except ImportError:
            print(f"❌ {package} manquant")
            missing_packages.append(package)

    if missing_packages:
        print(
            f"💡 Installez les packages manquants: pip install {' '.join(missing_packages)}")
        return False
    return True


def check_project_structure():
    """Vérifier la structure du projet"""
    print("🔍 Vérification de la structure du projet...")
    required_dirs = [
        'data/raw', 'data/processed', 'data/external',
        'notebooks', 'src/scraping', 'src/features', 'src/models',
        'streamlit_app', 'config', 'logs', 'reports'
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ OK")
        else:
            print(f"❌ {dir_path}/ manquant")
            missing_dirs.append(dir_path)

    if missing_dirs:
        print("💡 Exécutez: python scripts/setup_project.py")
        return False
    return True


def check_config_files():
    """Vérifier les fichiers de configuration"""
    print("🔍 Vérification des fichiers de configuration...")

    # Vérifier .env
    if Path('.env').exists():
        print("✅ .env OK")

        # Vérifier le contenu du .env
        with open('.env', 'r') as f:
            content = f.read()
            if 'APIFY_API_TOKEN=' in content and 'GEMINI_API_KEY=' in content:
                print("✅ Clés API configurées dans .env")
            else:
                print("⚠️  Clés API à configurer dans .env")
    else:
        print("❌ .env manquant")
        print("💡 Copiez env.template vers .env et configurez vos clés API")
        return False

    # Vérifier config/settings.py
    if Path('config/settings.py').exists():
        print("✅ config/settings.py OK")
    else:
        print("❌ config/settings.py manquant")
        return False

    return True


def check_imports():
    """Vérifier les imports du projet"""
    print("🔍 Vérification des imports du projet...")

    # Ajouter src au path
    sys.path.insert(0, str(Path('src').absolute()))

    try:
        from scraping.tiktok_scraper import TikTokScraper
        print("✅ TikTokScraper importable")
    except ImportError as e:
        print(f"❌ TikTokScraper: {e}")
        return False

    try:
        from scraping.data_validator import DataValidator
        print("✅ DataValidator importable")
    except ImportError as e:
        print(f"❌ DataValidator: {e}")
        return False

    return True


def check_jupyter():
    """Vérifier Jupyter"""
    print("🔍 Vérification de Jupyter...")
    try:
        result = subprocess.run(
            ['jupyter', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Jupyter OK")
            return True
        else:
            print("❌ Jupyter non fonctionnel")
            return False
    except FileNotFoundError:
        print("❌ Jupyter non installé")
        return False


def check_streamlit():
    """Vérifier Streamlit"""
    print("🔍 Vérification de Streamlit...")
    try:
        result = subprocess.run(
            ['streamlit', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Streamlit OK")
            return True
        else:
            print("❌ Streamlit non fonctionnel")
            return False
    except FileNotFoundError:
        print("❌ Streamlit non installé")
        return False


def main():
    """Fonction principale de validation"""
    print("🚀 Validation de la configuration du projet Virality Chat POC")
    print("=" * 60)

    checks = [
        check_python_version,
        check_virtual_environment,
        check_project_structure,
        check_config_files,
        check_dependencies,
        check_imports,
        check_jupyter,
        check_streamlit
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            results.append(False)
            print()

    print("=" * 60)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"🎉 SUCCÈS! Toutes les vérifications passées ({passed}/{total})")
        print("\n🎯 Prochaines étapes:")
        print("1. Configurer les comptes TikTok dans config/settings.py")
        print("2. Lancer Jupyter: jupyter notebook notebooks/01_data_exploration.ipynb")
        print("3. Tester Streamlit: streamlit run streamlit_app/app.py")
        return True
    else:
        print(
            f"⚠️  ATTENTION! {total - passed} vérifications ont échoué ({passed}/{total})")
        print("\n🔧 Corrigez les problèmes ci-dessus avant de continuer")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
