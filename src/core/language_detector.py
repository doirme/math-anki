"""
Language detection and management for semantic analysis.
"""
from __future__ import annotations
from typing import Optional
import re

# Try to use langdetect, fallback to simple heuristic
try:
    from langdetect import detect, LangDetectException
    _HAS_LANGDETECT = True
except ImportError:
    _HAS_LANGDETECT = False


def detect_language(text: str) -> str:
    """
    Detect the language of text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code: "fr", "en", "es", etc. Defaults to "fr" if detection fails.
    """
    if not text or len(text.strip()) < 10:
        return "fr"  # Default to French
    
    # Try langdetect first
    if _HAS_LANGDETECT:
        try:
            # Use first 1000 chars for faster detection
            sample = text[:1000] if len(text) > 1000 else text
            lang = detect(sample)
            return lang
        except LangDetectException:
            pass
    
    # Fallback: simple heuristic based on common words
    text_lower = text.lower()
    
    # French indicators
    french_words = ["définition", "théorème", "démonstration", "proposition", "lemme", 
                    "corollaire", "exercice", "preuve", "soit", "alors", "donc", "ainsi"]
    french_count = sum(1 for word in french_words if word in text_lower)
    
    # English indicators
    english_words = ["definition", "theorem", "proof", "proposition", "lemma",
                     "corollary", "exercise", "let", "then", "therefore", "thus"]
    english_count = sum(1 for word in english_words if word in text_lower)
    
    if french_count > english_count:
        return "fr"
    elif english_count > french_count:
        return "en"
    else:
        return "fr"  # Default to French


def get_language_name(lang_code: str) -> str:
    """Get full language name from code."""
    lang_map = {
        "fr": "French",
        "en": "English",
        "es": "Spanish",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
    }
    return lang_map.get(lang_code, "French")  # Default to French


def format_language_instruction(lang_code: str) -> str:
    """
    Format instruction for LLM to respond in specific language.
    
    Args:
        lang_code: Language code ("fr", "en", etc.)
    
    Returns:
        Instruction string for prompts
    """
    lang_name = get_language_name(lang_code)
    return f"IMPORTANT: Respond in {lang_name} ({lang_code}). All output text, field values, and JSON content must be in {lang_name}."

