# math-anki 🧮🎴

Pipeline local pour convertir des PDF de cours/exercices de mathématiques en cartes Anki (.apkg) structurées et intelligentes.

## 🌟 Vue d'ensemble

`math-anki` utilise une approche de **Segmentation Sémantique** assistée par LLM pour transformer des documents mathématiques non structurés en une base de connaissances structurée. Le pipeline identifie les théorèmes, définitions, preuves et exercices, établit leurs relations (ex: lien Théorème ↔ Preuve) et extrait les données dans des schémas stricts.

## 🚀 Installation Rapide

```bash
# 1. Cloner et installer les dépendances
pip install poetry
poetry install

# 2. Configurer l'environnement
cp .env.example .env
# Éditez .env avec vos clés API (OpenRouter recommandé)
```

> [!TIP]
> Pour les PDF scannés, installez `Tesseract` et `ocrmypdf` sur votre système.

## 🛠️ Utilisation

### Pipeline CLI

```bash
# 1) Ingestion : PDF → Markdown + DB
poetry run math-anki ingest ./data/raw/cours.pdf

# 2) Analyse & Build : Extraction sémantique & Génération de cartes
poetry run math-anki build --deck "Maths::Analyse"

# 3) Export : Génération du fichier .apkg
poetry run math-anki export --out ./data/cards/Analyse.apkg
```

### Interface Utilisateur (Streamlit)

```bash
poetry run streamlit run src/math_anki/ui/streamlit_app.py
```

## 📚 Documentation Détaillée

Pour approfondir le fonctionnement et la configuration du projet :

### 🏗️ Architecture & Technique
- **[Structure du Projet](PROJECT_STRUCTURE.md)** : Organisation des fichiers et des modules.
- **[Algorithme de Segmentation](ALGORITHM_EXPLANATION.md)** : Détails sur le découpage intelligent des blocs.
- **[Schéma de la Base de Données](DB_SCHEMA.md)** : Comment les données sémantiques sont stockées.

### ⚙️ Configuration
- **[Configuration OpenRouter](OPENROUTER_SETUP.md)** : Guide complet pour l'accès aux LLMs.

## 🧠 Concepts Clés

Le système repose sur un pipeline en 4 phases :
1. **Block Creation** : Segmentation intelligente avec validation par LLM.
2. **Block Linking** : Détection des relations (Théorème ↔ Preuve, Définition ↔ Usage).
3. **Semantic Extraction** : Extraction structurée (Hypothèses, Conclusion, Tags).
4. **Block Indexing** : Indexation vectorielle pour la recherche de similarité.

---
*Développé pour transformer l'apprentissage des mathématiques par la puissance des LLMs et d'Anki.*

