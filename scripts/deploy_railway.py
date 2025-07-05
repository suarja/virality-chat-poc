#!/usr/bin/env python3
"""
🚀 Script de Déploiement Railway - DDD Approach

🎯 Déploiement automatique de l'API TikTok Virality sur Railway
📊 R² = 0.457 - Prédiction pré-publication scientifiquement validée

Usage:
    python scripts/deploy_railway.py
"""
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


def check_railway_cli():
    """Vérifie si Railway CLI est installé"""
    result = run_command("railway --version", "Vérification Railway CLI")
    if result is None:
        print("❌ Railway CLI non installé. Installation...")
        install_result = run_command(
            "npm install -g @railway/cli", "Installation Railway CLI")
        if install_result is None:
            print("❌ Impossible d'installer Railway CLI")
            return False
    return True


def run_tests():
    """Lance les tests avant déploiement"""
    print("🧪 Lancement des tests...")
    test_result = run_command("pytest tests/api/ -v", "Tests API")
    if test_result is None:
        print("⚠️ Tests échoués, continuer quand même? (y/n)")
        response = input().lower()
        if response != 'y':
            print("❌ Déploiement annulé")
            return False
    return True


def deploy_to_railway():
    """Déploie sur Railway"""
    print("🚀 Déploiement sur Railway...")

    # Vérifier si on est dans un projet Railway
    if not os.path.exists(".railway"):
        print("📦 Initialisation projet Railway...")
        init_result = run_command("railway init", "Initialisation Railway")
        if init_result is None:
            return False

    # Déployer
    deploy_result = run_command("railway up", "Déploiement Railway")
    if deploy_result is None:
        return False

    # Obtenir l'URL
    url_result = run_command("railway domain", "Récupération URL")
    if url_result:
        print(f"🌐 API déployée: {url_result.strip()}")

    return True


def main():
    """Fonction principale"""
    print("🚀 Déploiement DDD - TikTok Virality API")
    print("=" * 50)

    # Vérifications préalables
    if not check_railway_cli():
        sys.exit(1)

    # Tests
    if not run_tests():
        sys.exit(1)

    # Déploiement
    if deploy_to_railway():
        print("🎉 Déploiement réussi!")
        print("\n📋 Prochaines étapes:")
        print("1. Tester l'API: curl https://your-app.railway.app/health")
        print("2. Vérifier la documentation: https://your-app.railway.app/docs")
        print("3. Tester la prédiction: POST https://your-app.railway.app/predict")
    else:
        print("❌ Déploiement échoué")
        sys.exit(1)


if __name__ == "__main__":
    main()
