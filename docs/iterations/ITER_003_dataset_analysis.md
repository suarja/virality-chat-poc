# 🔍 ITER_003: Dataset Analysis - Overfitting Investigation

## 📋 **Informations Générales**

- **Date d'analyse**: `2025-07-06`
- **Dataset**: `data/dataset_iter_002/features/aggregated_comprehensive.csv`
- **Taille**: 84 vidéos, 70 features
- **Objectif**: Comprendre pourquoi le modèle prédit une viralité plus élevée pour les vidéos non-virales

---

## 🚨 **Problèmes Majeurs Identifiés**

### **1. Duplication Massive de Données** ⚠️

**Problème**: 52 vidéos dupliquées sur 84 totales (62% de duplication)

**Impact**:

- Le modèle apprend sur des données dupliquées
- Biais fort vers les patterns des vidéos dupliquées
- Généralisation compromise

**Détails**:

```
Vidéos uniques: 32
Vidéos dupliquées: 52
Taux de duplication: 62%
```

### **2. Distribution Inégale par Compte** ⚠️

**Problème**: Certains comptes dominent le dataset

| Compte           | Vidéos | Vues Moyennes | Impact   |
| ---------------- | ------ | ------------- | -------- |
| `leaelui`        | 20     | 946,930       | Dominant |
| `swiss_fit.cook` | 20     | 946,930       | Dominant |
| `unefille.ia`    | 20     | 946,930       | Dominant |
| `gotaga`         | 12     | 248,582       | Modéré   |
| `marie29france_` | 12     | 248,582       | Modéré   |

**Impact**:

- Le modèle apprend principalement les patterns de 3 comptes
- Biais vers les créateurs populaires
- Mauvaise généralisation pour nouveaux créateurs

### **3. Corrélations Faibles avec les Vues** ⚠️

**Problème**: Les features extraites ne corrèlent pas bien avec les vues

| Feature                   | Corrélation | Statut         |
| ------------------------- | ----------- | -------------- |
| `duration`                | -0.322      | ❌ Négative    |
| `hashtag_count`           | -0.211      | ❌ Négative    |
| `viral_potential_score`   | 0.307       | ⚠️ Faible      |
| `emotional_trigger_count` | 0.306       | ⚠️ Faible      |
| `hour_of_day`             | 0.081       | ❌ Très faible |
| `day_of_week`             | 0.180       | ❌ Faible      |

**Impact**:

- Le modèle ne peut pas apprendre les patterns de viralité
- Prédictions basées sur des features non pertinentes
- Overfitting sur des patterns de compte plutôt que de contenu

---

## 📊 **Analyse Détaillée par Catégorie de Vues**

### **Vidéos à Fortes Vues (>1M)** - 15 vidéos (17.9%)

**Caractéristiques**:

- **Durée**: 19.2s (plus courtes)
- **Hashtags**: 2.8 (moins de hashtags)
- **Durée optimisée**: 0.8 (très optimisé)
- **Score viral**: 0.8 (élevé)

### **Vidéos à Vues Moyennes (10K-1M)** - 62 vidéos (73.8%)

**Caractéristiques**:

- **Durée**: 41.7s (plus longues)
- **Hashtags**: 6.2 (plus de hashtags)
- **Durée optimisée**: 0.67 (modérément optimisé)
- **Score viral**: 0.65 (modéré)

### **Vidéos à Faibles Vues (<10K)** - 7 vidéos (8.3%)

**Caractéristiques**:

- **Durée**: 54s (très longues)
- **Hashtags**: 3.4 (peu de hashtags)
- **Durée optimisée**: 0.57 (peu optimisé)
- **Score viral**: 0.5 (faible)

---

## 🎯 **Insights Clés**

### **1. Paradoxe de Durée** 🤔

**Observation**: Les vidéos virales sont plus courtes (19.2s) que les non-virales (54s)

**Explication Possible**:

- Les vidéos courtes ont plus de chances d'être regardées complètement
- L'algorithme TikTok favorise les vidéos avec un taux de completion élevé
- Les vidéos longues perdent l'attention plus rapidement

### **2. Paradoxe des Hashtags** 🤔

**Observation**: Les vidéos virales ont moins de hashtags (2.8) que les moyennes (6.2)

**Explication Possible**:

- Trop de hashtags peuvent être perçus comme du spam
- Les hashtags populaires créent de la concurrence
- La qualité des hashtags > la quantité

### **3. Biais de Compte** 🤔

**Observation**: 3 comptes dominent le dataset avec des patterns similaires

**Impact**:

- Le modèle apprend "être populaire" plutôt que "être viral"
- Mauvaise généralisation pour nouveaux créateurs
- Overfitting sur les patterns de compte existants

---

## 🔧 **Recommandations pour ITER_004**

### **1. Nettoyage du Dataset** 🧹

```bash
# Supprimer les duplications
python scripts/clean_dataset.py --remove-duplicates

# Équilibrer la distribution par compte
python scripts/balance_dataset.py --max-videos-per-account 10
```

### **2. Nouvelles Features** 🆕

**Features à Ajouter**:

- `completion_rate_estimate` (basé sur la durée)
- `hashtag_quality_score` (qualité vs quantité)
- `creator_popularity_bias` (corriger le biais de compte)
- `content_uniqueness_score` (éviter la duplication)

### **3. Stratégie de Collecte** 📊

**Nouvelle Approche**:

- Collecter 20 vidéos par compte maximum
- Diversifier les types de créateurs
- Inclure des créateurs émergents
- Éviter les vidéos dupliquées

### **4. Validation Croisée Stratifiée** ✅

**Nouvelle Méthode**:

- Stratifier par compte pour éviter le biais
- Tester sur des comptes non vus pendant l'entraînement
- Mesurer la généralisation réelle

---

## 📈 **Métriques de Qualité du Dataset**

### **Avant Nettoyage** (Actuel)

| Métrique                      | Valeur    | Statut      |
| ----------------------------- | --------- | ----------- |
| **Taux de duplication**       | 62%       | ❌ Critique |
| **Distribution équilibrée**   | Non       | ❌ Critique |
| **Corrélation features-vues** | <0.3      | ❌ Faible   |
| **Diversité des créateurs**   | 5 comptes | ⚠️ Limité   |

### **Après Nettoyage** (Objectif)

| Métrique                      | Valeur      | Statut |
| ----------------------------- | ----------- | ------ |
| **Taux de duplication**       | 0%          | ✅     |
| **Distribution équilibrée**   | Oui         | ✅     |
| **Corrélation features-vues** | >0.5        | ✅     |
| **Diversité des créateurs**   | 10+ comptes | ✅     |

---

## 🎯 **Plan d'Action ITER_004**

### **Phase 1: Nettoyage** (1 jour)

- [ ] Supprimer les duplications
- [ ] Équilibrer la distribution par compte
- [ ] Valider la qualité du dataset nettoyé

### **Phase 2: Nouvelles Features** (2 jours)

- [ ] Implémenter les features de qualité
- [ ] Ajouter les features de correction de biais
- [ ] Tester les nouvelles features

### **Phase 3: Nouveau Modèle** (1 jour)

- [ ] Entraîner sur le dataset nettoyé
- [ ] Validation croisée stratifiée
- [ ] Comparer avec ITER_003

### **Phase 4: Validation** (1 jour)

- [ ] Tests sur nouveaux créateurs
- [ ] Validation de la généralisation
- [ ] Documentation des résultats

---

## 📚 **Références**

- **Dataset Original**: `data/dataset_iter_002/features/aggregated_comprehensive.csv`
- **Script d'Analyse**: `scripts/analyze_dataset.py`
- **Documentation ITER_003**: `docs/iterations/ITER_003_model_optimization.md`

---

**Dernière mise à jour**: `2025-07-06`
**Statut**: `🔍 Analyse complétée - Prêt pour ITER_004`
