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
        'pandas', 'numpy', 'sklearn', 'streamlit',
        'plotly', 'jupyter', 'requests', 'google.generativeai',
        'dotenv'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai
            elif package == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(package.replace('-', '_'))
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
        'streamlit_app', 'config', 'logs', 'reports',
        'docs/gemini_analysis'  # New required directory
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
            api_keys = {
                'APIFY_API_TOKEN': 'Apify',
                'GOOGLE_API_KEY': 'Gemini'
            }
            all_keys_present = True
            for key, service in api_keys.items():
                if f'{key}=' in content:
                    print(f"✅ Clé API {service} configurée dans .env")
                else:
                    print(f"⚠️  Clé API {service} manquante dans .env")
                    all_keys_present = False
            if not all_keys_present:
                return False
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

    # Ajouter le projet root au path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "src"))

    try:
        from scraping.tiktok_scraper import TikTokScraper
        print("✅ TikTokScraper importable")

        # Test d'initialisation (sans token pour éviter l'erreur)
        try:
            # Test avec un token factice pour vérifier la logique
            os.environ['APIFY_API_TOKEN'] = 'test_token'
            scraper = TikTokScraper()
            print("✅ TikTokScraper initialisable")
        except ImportError as e:
            if "apify-client" in str(e):
                print("⚠️  apify-client requis mais module TikTokScraper fonctionne")
            else:
                raise
        except Exception as e:
            if "apify-client" in str(e) or "Apify API token" in str(e):
                print("✅ TikTokScraper logique OK (erreur attendue sans vraie clé API)")
            else:
                print(f"❌ TikTokScraper erreur inattendue: {e}")
                return False
        finally:
            # Nettoyer la variable d'environnement test
            if 'APIFY_API_TOKEN' in os.environ and os.environ['APIFY_API_TOKEN'] == 'test_token':
                del os.environ['APIFY_API_TOKEN']

    except ImportError as e:
        print(f"❌ TikTokScraper: {e}")
        return False

    # Test Gemini import and initialization
    try:
        import google.generativeai as genai
        print("✅ Gemini AI importable")

        # Test initialization with dummy key
        try:
            os.environ['GOOGLE_API_KEY'] = 'test_key'
            genai.configure(api_key='test_key')
            print("✅ Gemini AI initialisable")
        except Exception as e:
            if "invalid api key" in str(e).lower():
                print("✅ Gemini AI logique OK (erreur attendue sans vraie clé API)")
            else:
                print(f"❌ Gemini AI erreur inattendue: {e}")
                return False
        finally:
            if 'GOOGLE_API_KEY' in os.environ and os.environ['GOOGLE_API_KEY'] == 'test_key':
                del os.environ['GOOGLE_API_KEY']

    except ImportError as e:
        print(f"❌ Gemini AI: {e}")
        return False

    try:
        from scraping.data_validator import DataValidator
        print("✅ DataValidator importable")

        # Test d'initialisation
        validator = DataValidator()
        print("✅ DataValidator initialisable")
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


def check_documentation():
    """Vérifier la documentation"""
    print("🔍 Vérification de la documentation...")
    required_docs = [
        'README.md',
        'docs/gemini_analysis.md'
    ]

    missing_docs = []
    for doc_path in required_docs:
        if Path(doc_path).exists():
            print(f"✅ {doc_path} OK")
        else:
            print(f"❌ {doc_path} manquant")
            missing_docs.append(doc_path)

    if missing_docs:
        print("💡 Exécutez: python scripts/setup_project.py")
        return False
    return True


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
        check_streamlit,
        check_documentation  # New check
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
        print("2. Tester Gemini: python test_gemini.py")
        print("3. Lancer Jupyter: jupyter notebook notebooks/01_data_exploration.ipynb")
        print("4. Tester Streamlit: streamlit run streamlit_app/app.py")
        return True
    else:
        print(
            f"⚠️  ATTENTION! {total - passed} vérifications ont échoué ({passed}/{total})")
        print("\n🔧 Corrigez les problèmes ci-dessus avant de continuer")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
