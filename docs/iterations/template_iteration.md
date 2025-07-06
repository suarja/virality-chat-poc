# 🔬 Template d'Itération Scientifique - TikTok Virality Prediction

## 📋 **Informations Générales**

- **Itération ID**: `ITER_001`
- **Date de début**: `YYYY-MM-DD`
- **Date de fin**: `YYYY-MM-DD`
- **Responsable**: `[Nom]`
- **Version du modèle**: `v1.0.0`

---

## 🎯 **Hypothèse de Recherche**

### **Question Principale**

> [Formuler la question de recherche principale de cette itération]

### **Hypothèses Testées**

1. **H1**: [Hypothèse 1]
2. **H2**: [Hypothèse 2]
3. **H3**: [Hypothèse 3]

### **Objectifs Spécifiques**

- [ ] Objectif 1
- [ ] Objectif 2
- [ ] Objectif 3

---

## 📊 **Variables Expérimentales**

### **Variables Constantes**

| Variable                | Valeur      | Justification                         |
| ----------------------- | ----------- | ------------------------------------- |
| **Nombre de vidéos**    | `[X]`       | [Pourquoi cette taille d'échantillon] |
| **Nombre de comptes**   | `[X]`       | [Pourquoi ce nombre de comptes]       |
| **Période de scraping** | `[X] jours` | [Pourquoi cette période]              |
| **Feature set**         | `[Nom]`     | [Pourquoi ce set de features]         |
| **Modèle ML**           | `[Type]`    | [Pourquoi ce modèle]                  |

### **Variables Manipulées**

| Variable       | Valeur Testée | Valeur Contrôle | Justification                    |
| -------------- | ------------- | --------------- | -------------------------------- |
| **Variable 1** | `[Valeur]`    | `[Valeur]`      | [Pourquoi tester cette variable] |
| **Variable 2** | `[Valeur]`    | `[Valeur]`      | [Pourquoi tester cette variable] |

---

## 🔬 **Protocole Expérimental**

### **Phase 1: Exploration Locale**

```bash
# Scripts à exécuter
python3 scripts/test_pipeline_minimal.py
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_test --feature-set comprehensive
```

**Objectifs**:

- [ ] Valider le pipeline end-to-end
- [ ] Vérifier la qualité des données
- [ ] Identifier les problèmes potentiels

### **Phase 2: Création du Dataset**

```bash
# Scripts à exécuter
python3 scripts/run_pipeline.py --dataset poc_training --batch-size 3 --videos-per-account 15 --max-total-videos 150 --feature-set comprehensive
```

**Paramètres**:

- **Dataset**: `poc_training`
- **Batch size**: `3`
- **Vidéos par compte**: `15`
- **Total vidéos**: `150`
- **Feature set**: `comprehensive`

### **Phase 3: Entraînement du Modèle**

```bash
# Scripts à exécuter
python3 scripts/analyze_existing_data.py --dataset-dir data/dataset_poc_training --feature-set comprehensive --save-model
```

**Métriques à surveiller**:

- R² Score
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- Feature importance

### **Phase 4: Documentation et Contenu Éducatif**

- [ ] Mettre à jour `docs/educational/ml_glossary.md`
- [ ] Créer contenu TikTok éducatif
- [ ] Documenter les insights dans `docs/content-creation/`

### **Phase 5: Mise en Production API**

```bash
# Scripts à exécuter
python3 scripts/test_api_fixed.py
# Déploiement Railway
railway up
```

---

## 📈 **Résultats et Insights**

### **Métriques de Performance**

| Métrique        | Valeur    | Seuil Acceptable | Statut |
| --------------- | --------- | ---------------- | ------ |
| **R² Score**    | `[X.XXX]` | `> 0.4`          | ✅/❌  |
| **MAE**         | `[X.XXX]` | `< 0.3`          | ✅/❌  |
| **RMSE**        | `[X.XXX]` | `< 0.4`          | ✅/❌  |
| **Latence API** | `[X]s`    | `< 2s`           | ✅/❌  |

### **Insights Principaux**

1. **Insight 1**: [Description de l'insight]

   - **Impact**: [Impact sur le modèle/API]
   - **Action**: [Action à prendre]

2. **Insight 2**: [Description de l'insight]
   - **Impact**: [Impact sur le modèle/API]
   - **Action**: [Action à prendre]

### **Features les Plus Importantes**

1. `[Feature 1]` - Importance: `[X%]`
2. `[Feature 2]` - Importance: `[X%]`
3. `[Feature 3]` - Importance: `[X%]`

---

## 🎬 **Contenu Éducatif Créé**

### **Vidéos TikTok**

- **Vidéo 1**: [Titre] - [URL] - [Objectif éducatif]
- **Vidéo 2**: [Titre] - [URL] - [Objectif éducatif]

### **Articles/Posts**

- **Article 1**: [Titre] - [Lien] - [Thème]
- **Article 2**: [Titre] - [Lien] - [Thème]

### **Documentation Mise à Jour**

- [ ] `docs/educational/ml_glossary.md` - [Nouveaux termes ajoutés]
- [ ] `docs/content-creation/README.md` - [Nouveaux exemples]
- [ ] `docs/quick_start.md` - [Nouvelles instructions]

---

## 🔄 **Itération Suivante**

### **Améliorations Identifiées**

1. **Amélioration 1**: [Description]

   - **Priorité**: [Haute/Moyenne/Basse]
   - **Effort estimé**: [X jours]

2. **Amélioration 2**: [Description]
   - **Priorité**: [Haute/Moyenne/Basse]
   - **Effort estimé**: [X jours]

### **Variables à Tester**

1. **Variable 1**: [Description] - [Justification]
2. **Variable 2**: [Description] - [Justification]

### **Objectifs de la Prochaine Itération**

- [ ] Objectif 1
- [ ] Objectif 2
- [ ] Objectif 3

---

## 📚 **Références et Liens**

### **Documentation Référencée**

- **Codebase Guidelines**: `docs/project-management/codebase_guidelines.md`
- **Educational Content**: `docs/content-creation/README.md`
- **ML Glossary**: `docs/educational/ml_glossary.md`
- **API Documentation**: `src/api/README.md`

### **Scripts Utilisés**

- **Pipeline**: `scripts/run_pipeline.py`
- **Analysis**: `scripts/analyze_existing_data.py`
- **Testing**: `scripts/test_pipeline_minimal.py`
- **API Testing**: `scripts/test_api_fixed.py`

### **Données et Modèles**

- **Dataset**: `data/dataset_poc_training/`
- **Modèle**: `models/v1.0.0/`
- **Features**: `data/features/`

---

## ✅ **Checklist de Validation**

### **Avant de Commencer**

- [ ] Template rempli complètement
- [ ] Hypothèses clairement définies
- [ ] Variables expérimentales identifiées
- [ ] Protocole validé

### **Pendant l'Expérimentation**

- [ ] Données collectées selon le protocole
- [ ] Métriques enregistrées
- [ ] Insights documentés
- [ ] Contenu éducatif créé

### **Après l'Expérimentation**

- [ ] Résultats analysés
- [ ] Documentation mise à jour
- [ ] Prochaine itération planifiée
- [ ] Commit avec message descriptif

---

**Template créé le**: `2025-07-06`
**Dernière mise à jour**: `2025-07-06`
**Version du template**: `v1.0.0`
