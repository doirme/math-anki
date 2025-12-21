# Project Structure

This document outlines the file structure of the `math-anki` project.

## Root Directory
- `pyproject.toml`: Project configuration and dependencies (Poetry).
- `README.md`: General project overview.
- `PROJECT_STRUCTURE.md`: This file.
- `.env`: Environment variables (API keys, configuration).

## Source Code (`src/`)
The source code is organized into top-level packages.

### `src/cli.py`
- **Description**: Main entry point for the command-line interface.
- **Commands**:
    - `ingest`: Converts PDF to Markdown using various backends.
    - `build`: Runs the semantic analysis pipeline to generate flashcards.
    - `export`: Exports generated cards to Anki (`.apkg`).
    - `fixmath`: Utility to repair LaTeX in Markdown files.

### `src/core/`
Core logic for semantic analysis, PDF conversion, and LLM interaction.
- `semantic_analyzer.py`: Orchestrator for the semantic analysis pipeline (Block Creation -> Linking -> Extraction -> Indexing).
- `block_creator.py`: Identifies and validates semantic blocks (definitions, theorems, proofs) using internal segmentation and LLM validation.
- `block_linker.py`: Links related blocks (e.g., a proof to its theorem).
- `semantic_extractor.py`: Extracts structured data from blocks using LLMs.
- `block_indexer.py`: Generates embeddings and indexes blocks for retrieval.
- `semantic_schemas.py`: Pydantic models for blocks, extracted data, and indexes.
- `pdf_to_md.py`: Utilities for converting PDFs to Markdown (supports Marker, Mistral OCR, Docling).
- `math_fix.py`: Utilities for repairing malformed LaTeX math.
- `llm_client.py`: Client for interacting with LLM APIs (OpenAI, OpenRouter, Ollama).
- `llm_config.py`: Configuration manager for LLM tasks.
- `config.py`: Global application settings (loaded from `.env`).
- `enums.py`: Enumerations for block types, relations, etc.
- `json_utils.py`: Helper for robust JSON extraction from LLM outputs.
- `cards.py`: Logic for generating Anki card content from extracted data.

### `src/db/`
Database layer for persisting analysis results.
- `database.py`: Database connection and session management (SQLAlchemy/SQLModel).
- `models.py`: Database models (tables) for blocks, documents, etc.
- `persister.py`: Logic for saving analysis results to the database.
- `uow.py`: Unit of Work pattern implementation.

### `src/exporters/`
- `anki_export.py`: Logic for creating `.apkg` files using `genanki`.

### `src/ui/`
- `streamlit_app.py`: Main Streamlit application for interactive usage.

## Tests (`tests/`)
- `visual_debug_app.py`: Streamlit app for visualizing the semantic analysis pipeline steps.
- `test_*.py`: Unit and integration tests for various components.
