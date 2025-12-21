# Pipeline d'Analyse Sémantique - Détails Techniques

Ce document décrit le fonctionnement interne du pipeline d'analyse sémantique de `math-anki`, composé de 4 phases principales orchestrées par `SemanticAnalyzer`.

---

## Phase 1 : Création des Blocs (`block_creator.py`)

Cette phase transforme le texte brut en blocs sémantiques validés.

### 1. Pré-traitement (`_preprocess_text`)
Nettoyage et normalisation du texte pour isoler les marqueurs de structure.
*   **Action** : Insère des sauts de ligne (`\n\n`) avant les titres Markdown (`#`) et les mots-clés sémantiques (Théorème, Définition, etc.) même s'ils sont au milieu d'un paragraphe.

### 2. Segmentation Initiale (`_simple_segment`)
Découpage ligne par ligne basé sur des règles.
*   **Paragraphes** : Détection de deux lignes vides consécutives.
*   **Titres** : Déclenchement immédiat sur `#` ou `###`.
*   **Mots-clés** : Détection des mots définis dans `BLOCK_TYPE_KEYWORDS`.

### 3. Fusion des En-têtes (`_merge_headers`)
Regroupement des titres courts avec le bloc de contenu suivant pour éviter le sur-découpage.

### 4. Validation et Fusion (`_validate_and_merge`)
*   **Vérification LLM** : Utilisation d'un modèle rapide (ex: Claude Haiku) pour vérifier si le bloc est "autonome" (self-contained).
*   **Fusion Contextuelle** : Si le bloc est incomplet, il est fusionné avec ses voisins selon les recommandations du LLM.
*   **Sécurité** : Les blocs > 1500 caractères (hors preuves) sont marqués pour revue manuelle.

---

## Phase 2 : Liaison des Blocs (`block_linker.py`)

Établit les relations logiques entre les blocs validés.

*   **Heuristiques** : Détection automatique des liens directs (ex: une "Preuve" suivant immédiatement un "Théorème").
*   **Validation LLM** : Pour les relations complexes ou distantes, un LLM analyse les blocs candidats.
*   **Types de Relations** :
    *   `proves` : Preuve → Théorème.
    *   `has_proof` : Théorème → Preuve.
    *   `uses_definition` : Théorème/Preuve → Définition.
    *   `generalizes` / `specializes`.

---

## Phase 3 : Extraction Sémantique (`semantic_extractor.py`)

Transforme le texte des blocs en données structurées selon des schémas Pydantic.

*   **Définitions** : Extraction du terme défini, de l'énoncé nettoyé et des tags de domaine. Supporte le découpage automatique si un bloc contient plusieurs définitions.
*   **Théorèmes** : Isolation stricte des **Hypothèses** et de la **Conclusion**. Extraction du nom (ex: "Théorème de Bolzano-Weierstrass").
*   **Preuves** : Extraction des étapes logiques et des références aux autres théorèmes/définitions utilisés.
*   **Nettoyage** : Suppression automatique des titres et mots-clés redondants dans les énoncés.

---

## Phase 4 : Indexation des Blocs (`block_indexer.py`)

Prépare les données pour la base de données et la recherche.

*   **Normalisation des Noms** : Utilisation d'un LLM pour standardiser les noms (ex: "Thm de Cayley Hamilton" → "Cayley-Hamilton").
*   **Génération d'Embeddings** : Création de vecteurs numériques (via `sentence-transformers`) pour permettre la recherche par similarité sémantique.
*   **Tags de Domaine** : Classification automatique dans des domaines mathématiques (Algèbre, Analyse, Topologie, etc.).

---

## Configuration des Modèles par Tâche

Le pipeline permet d'utiliser des modèles différents selon la complexité de la tâche (configuré dans `llm_config.py`) :

| Tâche | Modèle Recommandé | Caractéristique |
| :--- | :--- | :--- |
| **Validation** | Claude Haiku / Gemini Flash | Rapide & Économique |
| **Liaison** | Claude Haiku | Rapide |
| **Extraction** | Claude Sonnet / DeepSeek V2 | Puissant & Précis |
| **Normalisation** | Claude Haiku | Cohérent |

### Fournisseurs de LLM Recommandés
Pour obtenir les meilleurs résultats, nous recommandons d'utiliser des modèles de haute qualité via ces plateformes :
- [OpenRouter](https://openrouter.ai/) : Accès unifié à presque tous les modèles (Claude, GPT-4, DeepSeek, etc.).
- [DeepSeek](https://www.deepseek.com/) : Excellent rapport performance/prix pour les tâches mathématiques.
- [Ollama](https://ollama.com/) : Pour faire tourner des modèles localement.

