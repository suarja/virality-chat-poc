# 🏗️ Codebase Guidelines - TikTok Virality Prediction POC

## 🎯 **Règles de Développement (80/20)**

### **🏆 Philosophie Simple**

> _"Keep it simple, document everything, learn from each iteration"_

### **📋 Règles Obligatoires**

#### **1. 🔄 Commits Réguliers**

- ✅ **Commiter à chaque feature complète** (pas de gros commits)
- ✅ **Messages clairs** : "feat: add model versioning" / "fix: correct feature extraction"
- ✅ **Jamais de code non commité** en fin de session

#### **2. 📚 Documentation Systématique**

- ✅ **Vérifier la codebase** avant de créer un fichier
- ✅ **Consulter les README** existants dans chaque dossier
- ✅ **Mettre à jour** les README correspondants
- ✅ **Demander confirmation** si doute sur l'emplacement

#### **3. 🏗️ Structure Simple**

- ✅ **Une seule API flagship** (pas de multi-environnement complexe)
- ✅ **Changement de modèle** = une variable à modifier
- ✅ **Tests validés** avant déploiement production
- ✅ **Documentation à chaque itération**

#### **4. 🎓 Approche Éducative**

- ✅ **Expliquer chaque concept** ML utilisé
- ✅ **Contexte réel** pour chaque décision
- ✅ **Progression logique** (simple → complexe)
- ✅ **Exemples pratiques** du projet TikTok

#### **5. 🔬 Approche Scientifique**

- ✅ **Hypothèses claires** pour chaque itération
- ✅ **Variables expérimentales** documentées
- ✅ **Protocole reproductible** pour chaque test
- ✅ **Insights documentés** systématiquement
- ✅ **Template d'itération** utilisé pour chaque expérience

### **🚫 Règles Anti-Complexité**

- ❌ **Pas de sur-ingénierie** (80/20 rule)
- ❌ **Pas de fichiers sans documentation**
- ❌ **Pas de duplication** de fonctionnalités
- ❌ **Pas de changements** sans tests
- ❌ **Pas d'expérimentation** sans protocole

---

## 🎯 **Objectives**

### **Primary Goals**

1. **🧹 Clean & Organize** - Remove obsolete files, organize structure
2. **📚 Document Everything** - Add summaries to all important files/folders
3. **🎓 Educational Approach** - Explain ML concepts with glossary and references
4. **🔧 API Preparation** - Prepare for backend API development
5. **🌍 English Translation** - Gradually translate all content to English
6. **🔗 Modularity** - Ensure components can be used independently

### **Educational Philosophy**

> _"Like a physics professor explaining complex concepts through practical examples"_

- Every technical term explained (R², cross-validation, feature importance, etc.)
- Real-world context for each concept
- Progressive complexity (basic → advanced)
- Practical examples from our TikTok virality prediction

---

## 📊 **Current Codebase Analysis**

### **🔍 Structure Overview**

```
virality-chat-poc/
├── 📁 src/                    # Main source code
│   ├── features/              # Feature engineering modules
│   ├── utils/                 # Utility functions
│   ├── api/                   # API framework (future)
│   ├── models/                # ML models
│   └── scraping/              # Data collection
├── 📁 scripts/                # Execution scripts
├── 📁 tests/                  # Test suite
├── 📁 notebooks/              # Jupyter notebooks
├── 📁 config/                 # Configuration files
├── 📁 data/                   # Datasets and processed data
├── 📁 docs/                   # Documentation (recently reorganized)
├── 📁 streamlit_app/          # Demo application
└── 📁 reports/                # Generated reports
```

### **📈 File Count Analysis**

- **Total Python Files**: ~50+ files
- **Documentation Files**: ~30+ files
- **Configuration Files**: ~10 files
- **Test Files**: ~5 files
- **Notebooks**: ~10 files

---

## 🗂️ **Reorganization Strategy**

### **Phase 1: Documentation & Education** 📚

1. **Create Educational Glossary** - Define all ML concepts
2. **Add File Summaries** - Every important file gets a header comment
3. **Create Learning Path** - Progressive documentation structure
4. **Translate to English** - Start with key files

### **Phase 2: Code Cleanup** 🧹

1. **Identify Obsolete Files** - Mark for deletion/review
2. **Consolidate Duplicates** - Merge similar functionality
3. **Standardize Naming** - Consistent file/folder naming
4. **Remove Dead Code** - Unused functions and imports

### **Phase 3: API Preparation** 🔧

1. **Choose Framework** - FastAPI vs Flask analysis
2. **Design API Structure** - Endpoints and data flow
3. **Prepare Modular Components** - Independent modules
4. **Create API Documentation** - OpenAPI/Swagger specs

### **Phase 4: Testing & Validation** ✅

1. **Expand Test Coverage** - Unit and integration tests
2. **Create Validation Framework** - Model validation pipeline
3. **Performance Testing** - API and model performance
4. **Documentation Testing** - Ensure all examples work

---

## 🎓 **Educational Framework**

### **📖 ML Concepts Glossary**

```markdown
## R² Score (Coefficient of Determination)

**Definition**: A statistical measure that represents the proportion of variance in the dependent variable that's predictable from the independent variable(s).

**In Our Context**:

- R² = 0.457 means our model explains 45.7% of the variance in TikTok view counts
- Range: 0 to 1 (higher is better)
- Our result: Good for a small dataset (8 videos)

**Formula**: R² = 1 - (SS_res / SS_tot)

- SS_res = Sum of squared residuals
- SS_tot = Total sum of squares

**Reference**: [Link to detailed explanation]
```

### **📚 Learning Path Structure**

1. **Beginner Level** - Basic concepts and setup
2. **Intermediate Level** - Feature engineering and model training
3. **Advanced Level** - API development and deployment
4. **Expert Level** - Research and optimization

### **🔗 Cross-References System**

- Every concept links to glossary
- Every file links to related documentation
- Every example links to working code
- Progressive complexity indicators

---

## 🔧 **API Framework Analysis**

### **FastAPI vs Flask Comparison**

| **Criteria**       | **FastAPI**    | **Flask** | **Recommendation**      |
| ------------------ | -------------- | --------- | ----------------------- |
| **Learning Curve** | Moderate       | Easy      | FastAPI (better for ML) |
| **Performance**    | Excellent      | Good      | FastAPI                 |
| **Documentation**  | Auto-generated | Manual    | FastAPI                 |
| **Type Safety**    | Built-in       | External  | FastAPI                 |
| **ML Integration** | Excellent      | Good      | FastAPI                 |
| **Deployment**     | Easy           | Easy      | Tie                     |

### **Recommended Stack**

```python
# FastAPI + Pydantic + MLflow
FastAPI (Web Framework)
├── Pydantic (Data Validation)
├── MLflow (Model Management)
├── Uvicorn (ASGI Server)
└── Docker (Containerization)
```

### **API Structure Design**

```
/api/v1/
├── /health          # Health check
├── /predict         # Virality prediction
├── /analyze         # Video analysis
├── /features        # Feature extraction
├── /models          # Model management
└── /docs            # Auto-generated docs
```

---

## 🗑️ **Cleanup Strategy**

### **Files to Review (Potential Deletion)**

- `test_*.py` files in scripts/ (consolidate into tests/)
- Duplicate feature extractors in src/features/
- Obsolete notebooks in notebooks/
- Old configuration files

### **Files to Consolidate**

- Multiple feature extractors → Single modular system
- Test scripts → Proper test suite
- Configuration files → Centralized config

### **Files to Keep (Critical)**

- `scripts/analyze_existing_data.py` (core analysis)
- `src/features/modular_feature_system.py` (main system)
- `config/settings.py` (configuration)
- All documentation files

---

## 📝 **Documentation Standards**

### **File Header Template**

```python
"""
📊 File: [filename.py]
🎯 Purpose: [Brief description of what this file does]
📚 Concepts: [ML concepts used in this file]
🔗 Related: [Links to related files/documentation]

📖 Educational Notes:
- [Explain key concepts used]
- [Link to glossary entries]
- [Provide context for beginners]

🚀 Usage:
[Example of how to use this file]

📈 Performance:
[Any performance considerations]

🔧 Dependencies:
[List of key dependencies]
"""
```

### **Folder README Template**

```markdown
# 📁 [Folder Name]

## 🎯 Purpose

[What this folder contains and why]

## 📚 Key Concepts

[List of ML concepts used in this folder]

## 🔗 Related Documentation

[Links to relevant docs]

## 🚀 Getting Started

[How to use files in this folder]

## 📈 Educational Path

[Progressive learning path through this folder]
```

---

## 🔄 **Workflow de Développement**

### **Avant de Commencer**

1. **Lire** les guidelines
2. **Vérifier** la structure existante
3. **Consulter** les README pertinents
4. **Planifier** les changements

### **Pendant le Développement**

1. **Documenter** chaque étape
2. **Tester** régulièrement
3. **Commiter** fréquemment
4. **Mettre à jour** les README

### **Après le Développement**

1. **Valider** les tests
2. **Documenter** les changements
3. **Mettre à jour** la documentation
4. **Commiter** final

---

## 🔬 **Workflow d'Itération Scientifique**

### **Avant de Commencer une Itération**
1. **Copier le template**: `cp docs/iterations/template_iteration.md docs/iterations/ITER_XXX_description.md`
2. **Définir les hypothèses**: Basées sur les insights précédents
3. **Planifier les variables**: Constantes vs manipulées
4. **Valider le protocole**: Avec l'équipe

### **Pendant l'Itération**
1. **Suivre le protocole**: Phase par phase
2. **Documenter les résultats**: Métriques et insights
3. **Créer le contenu**: TikTok et documentation
4. **Tester l'API**: Validation end-to-end

### **Après l'Itération**
1. **Analyser les résultats**: Comparaison avec objectifs
2. **Mettre à jour la documentation**: Tous les fichiers concernés
3. **Planifier la suivante**: Basée sur les insights
4. **Commiter avec message clair**: "feat: ITER_XXX - [description]"

### **Références Itérations**
- **Template**: `docs/iterations/template_iteration.md`
- **README Itérations**: `docs/iterations/README.md`
- **Itération Actuelle**: `docs/iterations/ITER_001_initial_poc.md`

---

## 📊 **Checklist de Qualité**

### **Avant Commit**

- [ ] Code fonctionne localement
- [ ] Tests passent
- [ ] Documentation mise à jour
- [ ] README mis à jour si nécessaire
- [ ] Message de commit clair

### **Avant Déploiement**

- [ ] Tests de régression passent
- [ ] Performance acceptable
- [ ] Documentation complète
- [ ] Variables d'environnement configurées

_Plan created on July 5, 2025 - Educational codebase reorganization for TikTok Virality Prediction POC_
_Updated on July 6, 2025 - Added development rules and 80/20 philosophy_
