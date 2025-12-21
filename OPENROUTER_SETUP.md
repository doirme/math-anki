# Guide OpenRouter : Configuration et Maîtrise des Coûts

Ce guide explique comment configurer OpenRouter pour ce projet et maîtriser les coûts.

## 📋 Table des matières

1. [Créer un compte OpenRouter](#1-créer-un-compte-openrouter)
2. [Obtenir une clé API](#2-obtenir-une-clé-api)
3. [Configurer le projet](#3-configurer-le-projet)
4. [Maîtriser les coûts](#4-maîtriser-les-coûts)
5. [Modèles recommandés par tâche](#5-modèles-recommandés-par-tâche)
6. [Surveillance des coûts](#6-surveillance-des-coûts)

---

## 1. Créer un compte OpenRouter

### Étapes

1. **Aller sur le site OpenRouter**
   - Visitez : https://openrouter.ai/
   - Cliquez sur **"Sign Up"** ou **"Get Started"**

2. **Créer votre compte**
   - Vous pouvez vous inscrire avec :
     - Email + mot de passe
     - Compte Google
     - Compte GitHub
   - Acceptez les conditions d'utilisation

3. **Vérifier votre email** (si nécessaire)
   - Vérifiez votre boîte mail et cliquez sur le lien de confirmation

4. **Compléter votre profil** (optionnel mais recommandé)
   - Ajoutez des informations de facturation si vous prévoyez d'utiliser des modèles payants

---

## 2. Obtenir une clé API

### Étapes

1. **Se connecter à votre compte**
   - Allez sur https://openrouter.ai/
   - Connectez-vous avec vos identifiants

2. **Accéder aux clés API**
   - Cliquez sur votre profil (en haut à droite)
   - Sélectionnez **"Keys"** dans le menu
   - Ou allez directement sur : https://openrouter.ai/keys

3. **Créer une nouvelle clé API**
   - Cliquez sur **"Create Key"** ou **"New Key"**
   - Donnez un nom à votre clé (ex: "math-anki-dev")
   - **Important** : Copiez la clé immédiatement, elle ne sera affichée qu'une seule fois !
   - La clé ressemble à : `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

4. **Sécuriser votre clé**
   - ⚠️ **Ne partagez JAMAIS votre clé API publiquement**
   - Ne la commitez pas dans Git
   - Stockez-la uniquement dans votre fichier `.env` (voir section suivante)

---

## 3. Configurer le projet

### Étape 1 : Créer le fichier `.env`

Si vous n'avez pas encore de fichier `.env`, créez-le à la racine du projet :

```bash
# À la racine du projet math-anki
touch .env
```

### Étape 2 : Ajouter la clé API

Ouvrez le fichier `.env` et ajoutez :

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-votre-clé-api-ici
OPENROUTER_SITE=https://github.com/votre-repo/math-anki  # Optionnel
OPENROUTER_TITLE=Math-Anki  # Optionnel

# Backend LLM par défaut
LLM_BACKEND=openrouter
LLM_MODEL=openrouter/anthropic/claude-3-haiku  # Modèle économique par défaut

# Configuration des tâches spécifiques (optionnel)
# Si non défini, utilise les valeurs par défaut dans llm_config.py
LLM_TASK_BLOCK_VALIDATION_BACKEND=openrouter
LLM_TASK_BLOCK_VALIDATION_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_BLOCK_VALIDATION_TEMPERATURE=0.0

LLM_TASK_BLOCK_LINKING_BACKEND=openrouter
LLM_TASK_BLOCK_LINKING_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_BLOCK_LINKING_TEMPERATURE=0.0

LLM_TASK_EXTRACTION_BACKEND=openrouter
LLM_TASK_EXTRACTION_MODEL=openrouter/anthropic/claude-3.5-sonnet  # Plus puissant pour l'extraction
LLM_TASK_EXTRACTION_TEMPERATURE=0.0

LLM_TASK_NORMALIZATION_BACKEND=openrouter
LLM_TASK_NORMALIZATION_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_NORMALIZATION_TEMPERATURE=0.0
```

### Étape 3 : Vérifier que `.env` est dans `.gitignore`

Assurez-vous que votre fichier `.env` est ignoré par Git :

```bash
# Vérifiez que .gitignore contient :
.env
.env.local
```

### Étape 4 : Tester la configuration

Testez que tout fonctionne :

```python
from src.core.llm_client import LLMClient

# Test simple
client = LLMClient(backend="openrouter", model="openrouter/anthropic/claude-3-haiku")
response = client.generate("Bonjour, pouvez-vous me dire bonjour en retour ?")
print(response)
```

---

## 4. Maîtriser les coûts

### Stratégies de réduction des coûts

#### 1. **Utiliser des modèles économiques**

OpenRouter propose plusieurs modèles à différents prix. Voici les recommandations :

**Pour les tâches simples (validation, normalisation) :**
- `openrouter/anthropic/claude-3-haiku` - ~$0.25/$1M tokens input, ~$1.25/$1M tokens output
- `openrouter/google/gemini-flash-1.5` - ~$0.075/$1M tokens input, ~$0.30/$1M tokens output
- `openrouter/meta-llama/llama-3.1-8b-instruct:free` - **GRATUIT** (avec limitations)

**Pour les tâches complexes (extraction) :**
- `openrouter/anthropic/claude-3.5-sonnet` - ~$3/$1M tokens input, ~$15/$1M tokens output
- `openrouter/anthropic/claude-3-opus` - Plus cher mais plus puissant

#### 2. **Limiter les tokens**

Configurez des limites de tokens dans votre `.env` :

```bash
# Limiter les réponses pour éviter les coûts excessifs
LLM_TASK_EXTRACTION_MAX_TOKENS=2000
LLM_TASK_BLOCK_VALIDATION_MAX_TOKENS=500
LLM_TASK_BLOCK_LINKING_MAX_TOKENS=1000
```

#### 3. **Utiliser le cache**

Le projet utilise déjà un système de cache pour les conversions PDF. Assurez-vous qu'il est activé :

```bash
MD_CACHE_DIR=./data/cache
MD_CACHE_STRICT_HASH=true
```

#### 4. **Désactiver l'utilisation LLM pour fix_math (si non nécessaire)**

Par défaut, la réparation LaTeX par LLM est désactivée. Gardez-la désactivée sauf si nécessaire :

```bash
FIXMATH_USE_LLM=false  # Garder à false pour économiser
```

#### 5. **Utiliser Ollama en local pour le développement**

Pour le développement et les tests, utilisez Ollama (gratuit, local) :

```bash
# Pour le développement
LLM_BACKEND=ollama
LLM_MODEL=llama3:8b

# Pour la production avec OpenRouter
LLM_BACKEND=openrouter
LLM_MODEL=openrouter/anthropic/claude-3-haiku
```

#### 6. **Définir un budget quotidien/mensuel**

Sur OpenRouter, vous pouvez définir des limites de dépenses :

1. Allez sur https://openrouter.ai/settings
2. Configurez **"Spend Limits"**
3. Définissez une limite quotidienne (ex: $5/jour)
4. Définissez une limite mensuelle (ex: $50/mois)

---

## 5. Modèles recommandés par tâche

### Configuration optimale coût/performance

```bash
# Validation de blocs (tâche simple, fréquente)
LLM_TASK_BLOCK_VALIDATION_MODEL=openrouter/google/gemini-flash-1.5
LLM_TASK_BLOCK_VALIDATION_MAX_TOKENS=300

# Détection de liens (tâche simple)
LLM_TASK_BLOCK_LINKING_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_BLOCK_LINKING_MAX_TOKENS=500

# Extraction (tâche complexe, importante)
LLM_TASK_EXTRACTION_MODEL=openrouter/anthropic/claude-3.5-sonnet
LLM_TASK_EXTRACTION_MAX_TOKENS=2000

# Normalisation (tâche simple)
LLM_TASK_NORMALIZATION_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_NORMALIZATION_MAX_TOKENS=500
```

### Modèles gratuits (avec limitations)

Si vous voulez tester gratuitement :

```bash
# Modèle gratuit de Meta (avec rate limits)
LLM_TASK_BLOCK_VALIDATION_MODEL=openrouter/meta-llama/llama-3.1-8b-instruct:free
LLM_TASK_BLOCK_LINKING_MODEL=openrouter/meta-llama/llama-3.1-8b-instruct:free
```

⚠️ **Note** : Les modèles gratuits ont des limitations de taux et peuvent être plus lents.

---

## 6. Surveillance des coûts

### Sur le dashboard OpenRouter

1. **Accéder au dashboard**
   - Allez sur https://openrouter.ai/activity
   - Vous verrez :
     - Les requêtes récentes
     - Les coûts par requête
     - Le total des dépenses

2. **Vérifier les statistiques**
   - **Activity** : Historique des requêtes
   - **Credits** : Solde et dépenses
   - **Settings** : Limites de dépenses

### Dans le code (optionnel)

Vous pouvez ajouter un logging des coûts dans votre code. OpenRouter retourne des métadonnées de coût dans les headers de réponse.

Exemple de script de monitoring (à créer) :

```python
# scripts/monitor_costs.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Les métadoxes de coût sont dans les headers de réponse
# Vous pouvez les logger pour suivre les dépenses
```

### Alertes de budget

1. Configurez des alertes email dans OpenRouter :
   - Allez dans **Settings** → **Notifications**
   - Activez les alertes à 50%, 75%, 90% de votre budget

2. Vérifiez régulièrement votre dashboard (hebdomadaire recommandé)

---

## 7. Exemple de configuration complète `.env`

```bash
# ============================================
# OpenRouter Configuration
# ============================================
OPENROUTER_API_KEY=sk-or-v1-votre-clé-api
OPENROUTER_SITE=https://github.com/votre-repo/math-anki
OPENROUTER_TITLE=Math-Anki

# ============================================
# Backend LLM par défaut
# ============================================
LLM_BACKEND=openrouter
LLM_MODEL=openrouter/anthropic/claude-3-haiku

# ============================================
# Configuration des tâches (optimisé coût)
# ============================================

# Validation de blocs (simple, fréquent) - Modèle économique
LLM_TASK_BLOCK_VALIDATION_BACKEND=openrouter
LLM_TASK_BLOCK_VALIDATION_MODEL=openrouter/google/gemini-flash-1.5
LLM_TASK_BLOCK_VALIDATION_TEMPERATURE=0.0
LLM_TASK_BLOCK_VALIDATION_MAX_TOKENS=300

# Détection de liens (simple) - Modèle économique
LLM_TASK_BLOCK_LINKING_BACKEND=openrouter
LLM_TASK_BLOCK_LINKING_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_BLOCK_LINKING_TEMPERATURE=0.0
LLM_TASK_BLOCK_LINKING_MAX_TOKENS=500

# Extraction (complexe, important) - Modèle plus puissant
LLM_TASK_EXTRACTION_BACKEND=openrouter
LLM_TASK_EXTRACTION_MODEL=openrouter/anthropic/claude-3.5-sonnet
LLM_TASK_EXTRACTION_TEMPERATURE=0.0
LLM_TASK_EXTRACTION_MAX_TOKENS=2000

# Normalisation (simple) - Modèle économique
LLM_TASK_NORMALIZATION_BACKEND=openrouter
LLM_TASK_NORMALIZATION_MODEL=openrouter/anthropic/claude-3-haiku
LLM_TASK_NORMALIZATION_TEMPERATURE=0.0
LLM_TASK_NORMALIZATION_MAX_TOKENS=500

# ============================================
# Autres configurations
# ============================================
FIXMATH_USE_LLM=false  # Désactivé pour économiser
MD_CACHE_DIR=./data/cache
MD_CACHE_STRICT_HASH=true
```

---

## 8. Dépannage

### Erreur : "Missing OPENROUTER_API_KEY"

- Vérifiez que votre fichier `.env` existe
- Vérifiez que la clé est correctement nommée : `OPENROUTER_API_KEY`
- Vérifiez que vous avez bien chargé le `.env` (le projet utilise `python-dotenv`)

### Erreur : "Invalid API key"

- Vérifiez que la clé commence par `sk-or-v1-`
- Vérifiez que vous n'avez pas d'espaces avant/après la clé
- Vérifiez que la clé est active sur https://openrouter.ai/keys

### Coûts trop élevés

- Réduisez `MAX_TOKENS` pour chaque tâche
- Utilisez des modèles plus économiques (gemini-flash, haiku)
- Activez le cache pour éviter les requêtes redondantes
- Utilisez Ollama pour le développement local

---

## 9. Ressources utiles

- **OpenRouter Dashboard** : https://openrouter.ai/
- **Documentation API** : https://openrouter.ai/docs
- **Modèles disponibles** : https://openrouter.ai/models
- **Prix des modèles** : https://openrouter.ai/models (voir la colonne "Pricing")
- **Support** : https://openrouter.ai/docs/support

---

## 10. Résumé rapide

1. ✅ Créer un compte sur https://openrouter.ai/
2. ✅ Créer une clé API dans **Keys**
3. ✅ Ajouter `OPENROUTER_API_KEY=votre-clé` dans `.env`
4. ✅ Configurer `LLM_BACKEND=openrouter` dans `.env`
5. ✅ Choisir des modèles économiques selon les tâches
6. ✅ Définir des limites de budget sur OpenRouter
7. ✅ Surveiller les coûts régulièrement

**Bon développement ! 🚀**

