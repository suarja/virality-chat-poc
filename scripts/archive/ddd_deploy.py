# ARCHIVE: Script DDD historique. Non maintenu. Voir pipeline principal et CI/CD actuelle.
#!/usr/bin/env python3
"""
🚀 Script de Déploiement DDD Progressif - Railway

🎯 Déploiement par étapes avec gestion des erreurs
📊 R² = 0.457 - Prédiction pré-publication scientifiquement validée

Usage:
    python scripts/ddd_deploy.py --step 1  # Health Check API
    python scripts/ddd_deploy.py --step 2  # Feature Extraction
    python scripts/ddd_deploy.py --step 3  # Model Prediction
    python scripts/ddd_deploy.py --step 4  # Full Pipeline
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Exécute une commande avec feedback"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True,
                                check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur: {e}")
        print(f"Stderr: {e.stderr}")
        return None


def setup_step_1():
    """Étape 1 DDD: Health Check API"""
    print("🎯 Étape 1 DDD: Health Check API")
    print("=" * 50)

    # Copier requirements minimal
    run_command("cp requirements-minimal.txt requirements.txt",
                "Copie requirements minimal")

    # Commit et push
    run_command("git add requirements.txt", "Ajout requirements minimal")
    run_command(
        'git commit -m "🚀 DDD Step 1: Health Check API - Requirements minimal"', "Commit Step 1")
    run_command("git push", "Push vers GitHub")

    print("✅ Étape 1 déployée - Attendre validation Railway")


def setup_step_2():
    """Étape 2 DDD: Feature Extraction API"""
    print("🎯 Étape 2 DDD: Feature Extraction API")
    print("=" * 50)

    # Ajouter dépendances de base
    with open("requirements.txt", "w") as f:
        f.write("""# DDD Step 2: Feature Extraction API
fastapi==0.115.14
uvicorn[standard]==0.35.0
python-multipart==0.0.20
pydantic==2.11.7
python-dotenv==1.0.1
Pillow==10.4.0
opencv-python-headless==4.9.0.80
""")

    # Commit et push
    run_command("git add requirements.txt", "Ajout requirements Step 2")
    run_command(
        'git commit -m "🚀 DDD Step 2: Feature Extraction API - Ajout OpenCV"', "Commit Step 2")
    run_command("git push", "Push vers GitHub")

    print("✅ Étape 2 déployée - Attendre validation Railway")


def setup_step_3():
    """Étape 3 DDD: Model Prediction API"""
    print("🎯 Étape 3 DDD: Model Prediction API")
    print("=" * 50)

    # Ajouter dépendances ML
    with open("requirements.txt", "w") as f:
        f.write("""# DDD Step 3: Model Prediction API
fastapi==0.115.14
uvicorn[standard]==0.35.0
python-multipart==0.0.20
pydantic==2.11.7
python-dotenv==1.0.1
Pillow==10.4.0
opencv-python-headless==4.9.0.80
scikit-learn==1.4.0
pandas==2.2.0
numpy==1.26.4
""")

    # Commit et push
    run_command("git add requirements.txt", "Ajout requirements Step 3")
    run_command(
        'git commit -m "🚀 DDD Step 3: Model Prediction API - Ajout ML dependencies"', "Commit Step 3")
    run_command("git push", "Push vers GitHub")

    print("✅ Étape 3 déployée - Attendre validation Railway")


def setup_step_4():
    """Étape 4 DDD: Full Pipeline API"""
    print("🎯 Étape 4 DDD: Full Pipeline API")
    print("=" * 50)

    # Utiliser requirements complet
    run_command("cp requirements.txt requirements-full.txt",
                "Backup requirements complet")
    run_command("cp requirements.txt requirements.txt",
                "Copie requirements complet")

    # Commit et push
    run_command("git add requirements.txt", "Ajout requirements Step 4")
    run_command(
        'git commit -m "🚀 DDD Step 4: Full Pipeline API - Requirements complet"', "Commit Step 4")
    run_command("git push", "Push vers GitHub")

    print("✅ Étape 4 déployée - Attendre validation Railway")


def test_railway_deployment():
    """Test du déploiement Railway"""
    print("🧪 Test du déploiement Railway...")

    # Obtenir l'URL Railway
    url_result = run_command("railway domain", "Récupération URL Railway")
    if url_result:
        url = url_result.strip()
        print(f"🌐 URL Railway: {url}")

        # Test health check
        health_result = run_command(f"curl {url}/health", "Test Health Check")
        if health_result:
            print("✅ Health Check réussi")
        else:
            print("❌ Health Check échoué")
    else:
        print("⚠️ Impossible de récupérer l'URL Railway")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="DDD Deployment Script")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4],
                        help="Étape DDD à déployer")
    parser.add_argument("--test", action="store_true",
                        help="Tester le déploiement Railway")

    args = parser.parse_args()

    if args.test:
        test_railway_deployment()
        return

    if args.step == 1:
        setup_step_1()
    elif args.step == 2:
        setup_step_2()
    elif args.step == 3:
        setup_step_3()
    elif args.step == 4:
        setup_step_4()
    else:
        print("🎯 DDD Deployment Script")
        print("=" * 30)
        print("Usage:")
        print("  python scripts/ddd_deploy.py --step 1  # Health Check API")
        print("  python scripts/ddd_deploy.py --step 2  # Feature Extraction")
        print("  python scripts/ddd_deploy.py --step 3  # Model Prediction")
        print("  python scripts/ddd_deploy.py --step 4  # Full Pipeline")
        print("  python scripts/ddd_deploy.py --test    # Test Railway")


if __name__ == "__main__":
    main()
