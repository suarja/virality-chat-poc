# 🧠 Services Architecture

## 📋 **Vue d'Ensemble**

Ce dossier contient les services réutilisables du projet TikTok Virality Prediction. Ces services sont conçus pour être utilisés par :

- **Pipeline de données** (`scripts/run_pipeline.py`)
- **API FastAPI** (`src/api/`)
- **Scripts d'analyse** (`scripts/test_gemini.py`)
- **Tests et validation**

## 🔧 **Services Disponibles**

### **🧠 Gemini Service** (`gemini_service.py`)

**Fonction** : Analyse de vidéos TikTok avec Gemini AI

**Utilisation** :

```python
from src.services.gemini_service import analyze_tiktok_video

# Analyser une vidéo
result = analyze_tiktok_video("https://www.tiktok.com/@user/video/123")
```

**Fonctionnalités** :

- ✅ Analyse complète du contenu vidéo
- ✅ Extraction de features visuelles et structurelles
- ✅ Gestion d'erreurs robuste
- ✅ Cache intégré
- ✅ Fallback vers mocks si indisponible

**Dépendances** :

- `google-generativeai` (Gemini API)
- `GOOGLE_API_KEY` dans les variables d'environnement

## 🏗️ **Architecture**

### **Avant (Problématique)**

```
scripts/test_gemini.py  ← Logique Gemini isolée
scripts/run_pipeline.py ← Import direct de test_gemini
src/api/               ← Import impossible (scripts/ pas dans PYTHONPATH)
```

### **Après (Solution)**

```
src/services/gemini_service.py  ← Service centralisé
├── scripts/run_pipeline.py     ← Import: from src.services.gemini_service
├── src/api/gemini_integration.py ← Import: from src.services.gemini_service
└── scripts/test_gemini.py      ← Import: from src.services.gemini_service
```

## 🚀 **Avantages de cette Architecture**

### **1. Réutilisabilité**

- Un seul service utilisé partout
- Pas de duplication de code
- Maintenance centralisée

### **2. Modularité**

- Services indépendants
- Facile à tester individuellement
- Ajout de nouveaux services simple

### **3. Robustesse**

- Gestion d'erreurs centralisée
- Fallbacks automatiques
- Logs cohérents

### **4. Performance**

- Cache partagé
- Instances réutilisées
- Optimisations centralisées

## 📊 **Utilisation dans le Pipeline**

```python
# Dans run_pipeline.py
from src.services.gemini_service import analyze_tiktok_video

def run_gemini_phase(videos, account, tracker):
    for video in videos:
        result = analyze_tiktok_video(video_url)
        # Traitement du résultat...
```

## 🌐 **Utilisation dans l'API**

```python
# Dans gemini_integration.py
from src.services.gemini_service import analyze_tiktok_video

class GeminiIntegrationService:
    async def analyze_video(self, video_url):
        result = analyze_tiktok_video(video_url)
        # Cache et traitement...
```

## 🧪 **Utilisation dans les Tests**

```python
# Dans test_gemini.py
from src.services.gemini_service import analyze_tiktok_video

def main():
    result = analyze_tiktok_video(test_url)
    # Validation et sauvegarde...
```

## 🔧 **Configuration**

### **Variables d'Environnement**

```bash
# .env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### **Installation des Dépendances**

```bash
pip install google-generativeai
```

## 📈 **Monitoring et Logs**

Tous les services utilisent le même système de logging :

- **Niveau INFO** : Opérations normales
- **Niveau WARNING** : Problèmes non-critiques
- **Niveau ERROR** : Erreurs critiques

### **Exemple de Logs**

```
✅ Gemini service initialized successfully
🧠 Analyzing video: https://www.tiktok.com/@user/video/123
📤 Sending request to Gemini...
📥 Received response from Gemini
✅ Successfully parsed JSON response
```

## 🚨 **Gestion d'Erreurs**

### **Erreurs Communes**

1. **API Key manquante** → Fallback vers mocks
2. **Réseau indisponible** → Retry automatique
3. **JSON invalide** → Nettoyage automatique
4. **Rate limiting** → Délai automatique

### **Fallbacks**

- Si Gemini indisponible → Mocks automatiques
- Si cache corrompu → Régénération
- Si service défaillant → Logs détaillés

## 🔮 **Futurs Services**

### **Services Prévus**

- **Cache Service** : Gestion centralisée du cache
- **Validation Service** : Validation de données
- **Metrics Service** : Collecte de métriques
- **Notification Service** : Notifications d'erreurs

### **Pattern d'Implémentation**

```python
class NewService:
    def __init__(self):
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        # Vérification de disponibilité
        pass

    def process(self, data):
        if not self.available:
            return self._mock_process(data)
        # Logique réelle
        pass
```

## 📚 **Documentation Technique**

### **Structure de Réponse Gemini**

```json
{
  "success": true,
  "analysis": {
    "visual_analysis": {...},
    "content_structure": {...},
    "engagement_factors": {...},
    "technical_elements": {...},
    "trend_alignment": {...},
    "improvement_suggestions": {...}
  },
  "raw_response": "...",
  "timestamp": "2025-01-06T10:15:55.258Z"
}
```

### **Codes d'Erreur**

- `GEMINI_UNAVAILABLE` : Service indisponible
- `API_KEY_MISSING` : Clé API manquante
- `JSON_PARSE_ERROR` : Erreur de parsing
- `NETWORK_ERROR` : Erreur réseau

---

**Architecture créée le 6 janvier 2025 - Services centralisés pour TikTok Virality Prediction**
