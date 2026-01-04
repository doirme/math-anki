# Description des Éléments Sémantiques

Ce document détaille la structure et le contenu des éléments sémantiques extraits et stockés dans la base de données de `math-anki`.

## 1. Bloc Sémantique (`SemanticBlock`)

C’est l'unité de base. Chaque bloc correspond à un concept mathématique identifiable.

| Champ | Description | Usage dans les cartes |
| :--- | :--- | :--- |
| `kind` | Type (Théorème, Définition, Lemme, Corollaire, Preuve, etc.) | Détermine le template de carte utilisé. |
| `name` | Nom du résultat (ex: "Théorème de Bolzano-Weierstrass"). | Utilisé pour les questions de type "Quel est le nom de...". |
| `summary` | Énoncé complet (en Markdown/LaTeX). | Contenu principal du "Verso" de la carte. |
| `tags` | Liste de domaines (ex: "Algèbre Linéaire", "Espaces Vectoriels"). | Permet d'ajouter du contexte aux questions. |

## 2. Structure Interne pour les Théorèmes

Les théorèmes (et lemmes/propositions) sont décomposés en sous-blocs liés :

- **Hypothèses (`hypotheses_id`)** : 
    - Contient uniquement les pré-requis (ex: "Soit $f$ une fonction continue sur $[a, b]$").
    - Utilisé pour les questions : "Sous quelles hypothèses... ?".
- **Conclusion (`conclusion_id`)** : 
    - Contient le résultat final (ex: "Alors $f$ est bornée et atteint ses bornes").
    - Utilisé comme "Indice" ou "Question" pour retrouver les hypothèses ou le nom.
- **Preuve (`relations_to` avec prédicat `proves`)** :
    - Lien vers un bloc de type `proof`.
    - Utilisé pour générer des cartes de démonstration.

## 3. Contexte et Localisation

Chaque bloc est attaché à :
- **Un Document (`document_id`)** : Permet de connaître la source.
- **Un Chemin de Titres (`heading_path`)** : (Stocké dans le `TextBlock` parent). Fournit la hiérarchie Markdown (ex: `# Chapitre 1 > ## Topologie`).
- **Des Blocs Contexte** : Blocs non sémantiques (remarques, introductions) qui précèdent le bloc sémantique.

> [!IMPORTANT]
> Le manque de contexte actuel vient du fait que le `heading_path` ou les `tags` de domaine ne sont pas systématiquement inclus dans le front des cartes générées.
