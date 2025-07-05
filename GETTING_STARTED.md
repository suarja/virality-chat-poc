# Virality Chat POC - Getting Started

## QuickStart : Analyse des données existantes

Après avoir extrait et agrégé les features avec le pipeline, vous pouvez analyser et visualiser les données sans relancer le pipeline.

### 1. Installer les dépendances

```bash
python3 scripts/setup_project.py
```

### 2. Activer l'environnement virtuel

```bash
source venv/bin/activate
```

### 3. Lancer l'analyse sur un dataset existant

```bash
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive
```

- Le script cherche automatiquement les fichiers de features agrégés ou CSV dans le dossier `features/` du dataset.
- Il affiche :
  - Statistiques descriptives
  - Corrélations
  - Modèle baseline (Random Forest)
  - Insights et recommandations

### 4. Pour d'autres datasets

Adaptez le chemin `--dataset-dir` et le `--feature-set` selon vos besoins.

---

## Autres commandes utiles

- **Extraction et agrégation automatique** :
  - Voir la documentation du pipeline principal (`scripts/run_pipeline.py`)
- **Vérification de la structure** :
  - Utilisez `scripts/validate_setup.py` pour vérifier l'installation et la structure des dossiers.

---

## Notes

- Le script d'analyse ne relance jamais le scraping ni l'extraction, il ne fait qu'analyser les features déjà présentes.
- Pour toute question, voir la documentation ou les scripts dans le dossier `scripts/`.
