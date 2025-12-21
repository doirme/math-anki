from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import List, Optional

# Optional imports (we guard them)
try:
    from .marker_client import marker_pdf_to_markdown
    _HAS_MARKER = True
except Exception:
    _HAS_MARKER = False

try:
    from .mistral_ocr_client import ocr_pdf_to_markdown_mistral
    _HAS_MISTRAL_CLIENT = True
except Exception:
    _HAS_MISTRAL_CLIENT = False

# Keep your existing Modal docling function
try:
    from .docling_modal import run_docling  # modal.Function decorated (your existing)
    _HAS_DOCLING_MODAL = True
except Exception:
    _HAS_DOCLING_MODAL = False

# Settings (cache dir, llm fix, etc.)
try:
    from .config import settings
    _HAS_SETTINGS = True
except Exception:
    _HAS_SETTINGS = False


# ===================== Cache utilities =====================

def _sha256_file(p: Path, chunk: int = 2**20) -> str:
    """Compute SHA256 hash of file. Returns empty string if file doesn't exist."""
    if not p.exists():
        return ""
    h = hashlib.sha256()
    try:
        with p.open("rb") as f:
            while True:
                b = f.read(chunk)
                if not b:
                    break
                h.update(b)
    except Exception:
        return ""
    return h.hexdigest()

def _get_cache_dir() -> Optional[Path]:
    if _HAS_SETTINGS:
        try:
            return settings.get_cache_dir()  # type: ignore[attr-defined]
        except Exception:
            pass
    env = os.getenv("MD_CACHE_DIR")
    if not env:
        return None
    p = Path(env).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p

def _cache_candidates(pdf_path: Path, strict_hash: bool = True) -> List[Path]:
    cache_dir = _get_cache_dir()
    if not cache_dir:
        return []
    h8 = _sha256_file(pdf_path)
    if not h8:  # File doesn't exist or can't be hashed
        return []
    h8 = h8[:8]
    stem = pdf_path.stem
    cands = [cache_dir / f"{stem}.{h8}.md"]
    if not strict_hash:
        cands.append(cache_dir / f"{stem}.md")
    return cands

def _read_cached_markdown(pdf_path: Path, strict_hash: bool = True) -> Optional[str]:
    for c in _cache_candidates(pdf_path, strict_hash=strict_hash):
        if c.exists() and c.stat().st_size > 0:
            try:
                return c.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
    return None

def _write_cache_markdown(pdf_path: Path, md: str, source: str) -> None:
    cache_dir = _get_cache_dir()
    if not cache_dir:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    h8 = _sha256_file(pdf_path)[:8]
    stem = pdf_path.stem
    strict = cache_dir / f"{stem}.{h8}.md"
    alias  = cache_dir / f"{stem}.md"
    strict.write_text(md or "", encoding="utf-8")
    if not alias.exists():
        alias.write_text(md or "", encoding="utf-8")
    meta = {
        "pdf": str(pdf_path),
        "hash8": h8,
        "mtime_pdf": pdf_path.stat().st_mtime if pdf_path.exists() else None,
        "size_pdf": pdf_path.stat().st_size if pdf_path.exists() else None,
        "cached_at": time.time(),
        "source": source,
    }
    strict.with_suffix(".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# ===================== Backend functions =====================

def _run_marker(pdf_path: Path) -> Optional[str]:
    """Convert PDF to Markdown using Marker API."""
    if not _HAS_MARKER:
        return None
    try:
        md = marker_pdf_to_markdown(pdf_path)
        if md and md.strip():
            return md
    except Exception:
        pass
    return None

def _run_mistral_ocr(pdf_path: Path, *, chunk_pages: int = 200, workers: int = 4, include_images: bool = False) -> Optional[str]:
    """Convert PDF to Markdown using Mistral OCR API."""
    if not _HAS_MISTRAL_CLIENT:
        return None
    try:
        import asyncio
        md = asyncio.run(
            ocr_pdf_to_markdown_mistral(
                pdf_path,
                model="mistral-ocr-latest",
                include_images=include_images,
                max_pages_per_chunk=chunk_pages,
                max_workers=workers,
            )
        )
        if md and md.strip():
            return md
    except Exception:
        pass
    return None

def _run_docling_modal(pdf_path: Path) -> Optional[str]:
    """Call your existing Modal Docling function. It should return markdown string."""
    if not _HAS_DOCLING_MODAL:
        return None
    try:
        md = run_docling.remote(pdf_path.read_bytes(), pdf_path.name)  # decorate: .remote()
        if isinstance(md, str) and md.strip():
            return md
    except Exception:
        return None
    return None

# ===================== Normalize / math-fix =====================

_MATH_INLINE = re.compile(r"(\$[^$]+\$|\\\([^\)]+\\\))", re.S)
_MATH_BLOCK  = re.compile(r"(\$\$[\s\S]+?\$\$|\\\[([\s\S]+?)\\\])", re.S)

def _reflow_math(text: str) -> str:
    def _fix(seg: str) -> str:
        seg = seg.replace("\r", "")
        seg = re.sub(r"(?<!\\)\n", " ", seg)
        seg = re.sub(r"\s{2,}", " ", seg)
        return seg
    text = _MATH_BLOCK.sub(lambda m: _fix(m.group(1)), text)
    text = _MATH_INLINE.sub(lambda m: _fix(m.group(1)), text)
    return text

def _dehyphenate(text: str) -> str:
    text = text.replace("-\n", "")
    text = re.sub(r"([A-Za-z])\n([A-Za-z])", r"\1 \2", text)
    return text

def _light_ocr_fixes(text: str) -> str:
    text = text.replace("R n", r"\mathbb{R}^n")
    text = re.sub(r"\bT\s+([a-zA-Z])∈N\s*\[", r"\\bigcap_{\1\\in\\mathbb{N}}[", text)
    return text

def normalize_markdown(md: str) -> str:
    if not isinstance(md, str):
        md = "" if md is None else str(md)
    md = _dehyphenate(md)
    md = _reflow_math(md)
    md = _light_ocr_fixes(md)
    return md

# ===================== Public API =====================

def pdf_to_markdown(
    pdf: str | Path,
    *,
    prefer: str = "marker",  # Default: Marker API
    strict_cache_hash: bool = True,
    mistral_chunk_pages: int = 200,
    mistral_workers: int = 4,
    mistral_include_images: bool = False,
    fix_math: bool = True,
) -> str:
    """
    Convert PDF to Markdown using waterfall: Marker → Mistral OCR → Docling
    
    Backend order:
      1) Marker API (datalab.to) - primary, most efficient
      2) Mistral OCR API - fallback if Marker fails
      3) Docling Modal - last resort fallback
    
    Args:
        pdf: Path to PDF file
        prefer: Preferred backend ("marker", "mistral_ocr", "docling_modal")
        strict_cache_hash: Use strict hash matching for cache
        mistral_chunk_pages: Pages per chunk for Mistral (if used)
        mistral_workers: Worker threads for Mistral (if used)
        mistral_include_images: Include images in Mistral output (if used)
        fix_math: Apply LaTeX math formula repairs
    
    Returns:
        Markdown string (empty if all backends fail)
    """
    from .math_fix import fix_math_in_markdown, llm_fn_from_settings

    pdf_path = Path(pdf)

    # 1) Check cache first
    cached = _read_cached_markdown(pdf_path, strict_hash=strict_cache_hash)
    if cached:
        return cached

    md_raw: Optional[str] = None
    source = "unknown"

    # 2) Try backends in waterfall order
    pref = str(prefer).lower()

    # Try Marker first (unless explicitly skipped)
    if pref in ("marker", "auto") and not md_raw:
        md_raw = _run_marker(pdf_path)
        if md_raw:
            source = "marker"

    # Try Mistral OCR (if preferred or as fallback)
    if (pref == "mistral_ocr" or (pref in ("marker", "auto") and not md_raw)):
        md_raw = _run_mistral_ocr(
            pdf_path,
            chunk_pages=mistral_chunk_pages,
            workers=mistral_workers,
            include_images=mistral_include_images,
        )
        if md_raw:
            source = "mistral-ocr"

    # Try Docling Modal (if preferred or as final fallback)
    if (pref == "docling_modal" or (pref in ("marker", "mistral_ocr", "auto") and not md_raw)):
        md_raw = _run_docling_modal(pdf_path)
        if md_raw:
            source = "docling-modal"

    # If all backends failed, return empty
    if not md_raw:
        return ""

    # 3) Normalize and fix math
    md = normalize_markdown(md_raw)
    if fix_math:
        try:
            llm = llm_fn_from_settings() if (_HAS_SETTINGS and settings.fixmath_use_llm) else None
        except Exception:
            llm = None
        md, _, _ = fix_math_in_markdown(md, llm=llm, aggressive=False)

    # 4) Write to cache
    if md:
        _write_cache_markdown(pdf_path, md, source=source)

    return md
