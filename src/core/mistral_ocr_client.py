from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import os
import base64
import io
import asyncio
import concurrent.futures
import fitz  # PyMuPDF
from dataclasses import dataclass

# ---------- Low-level single-call to Mistral OCR ----------
@dataclass
class Page:
    index : int
    markdown : str
    images : list

class MarkDownDocument(list[Page]):
    def __init__(self, ocr_md):
        super().__init__()
        pages = getattr(ocr_md, 'pages', None)
        if pages:
            for _p in pages:
                self.append(Page(index=getattr(_p, 'index', 0),
                                 markdown=getattr(_p, 'markdown', ""),
                                 images=getattr(_p, 'images', []))
                            )

    def __str__(self):
        return ("\n\n".join(p.markdown for p in self if p).strip() + "\n") if len(self) > 0 else ""

    def extract_images(self, folder: Path):
        " create jpg files in the designated folder and replace markdown with links to these files"

        if not folder.exists():
            os.mkdir(folder)

        # pages
        for page in self:
            # Inline images if available (image placeholders pattern from Mistral OCR)
            images = {getattr(img, "id", ""): img for img in getattr(page, "images", [])}
            for _id, _i in images.items():
                b64 = getattr(_i, "image_base64", "")
                if b64:
                    filename = folder / f'page_{page.index}_{_id}.jpg'
                    b64 = b64[b64.find('base64,') + 7:]
                    with open(filename, 'wb') as file:
                        img_data = base64.b64decode(b64.encode("utf-8"))
                        file.write(img_data)
                images[_id] = str(filename.absolute())

            def replace_placeholder(md_text: str) -> str:
                import re
                def repl(m):
                    img_id = m.group(1)
                    img = images.get(img_id)
                    if not isinstance(img, str):
                        return m.group(0)
                    # anno = getattr(img, "image_annotation", "")
                    # Inline image + optional annotation
                    block = f"![Figure]({img})"
                    return block

                return re.sub(r"!\[[^\]]*\]\(([A-Za-z0-9._/-]+)\)", repl, md_text)

            page.markdown=replace_placeholder(page.markdown)


def _base64_to_jpg(b64_string: str, out_path: str | Path) -> Path:
    """Decode base64 string (UTF-8 encoded) and save as JPEG."""
    out_path = Path(out_path)
    img_data = base64.b64decode(b64_string.encode("utf-8"))
    out_path.write_bytes(img_data)
    return out_path


def _mistral_ocr_call(pdf_bytes: bytes,
                      model: str = "mistral-ocr-latest",
                      include_images: bool = False,
                      timeout: float = 120.0) -> MarkDownDocument:
    """
    Blocking call to Mistral OCR for a (sub)PDF (bytes).
    Returns list of pages: [{"index": int, "markdown": str, ...}, ...]
    Requires env MISTRAL_API_KEY and `pip install mistralai`.
    """
    from mistralai import Mistral  # imported here to avoid hard dep if unused

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY env var is required to call Mistral OCR.")

    client = Mistral(api_key=api_key, timeout=timeout)

    data_url = "data:application/pdf;base64," + base64.b64encode(pdf_bytes).decode("utf-8")
    document = {"type": "document_url", "document_url": data_url}

    resp = client.ocr.process(
        model=model,
        document=document,
        include_image_base64=bool(include_images),
    )

    return MarkDownDocument(resp)


# ---------- Chunking utilities (by page count) ----------

def _split_pdf_into_chunks(pdf_path: Path, max_pages_per_chunk: int) -> List[Tuple[int, bytes]]:
    """
    Returns a list of (start_page_idx, pdf_bytes) chunks. start_page_idx is 0-based.
    """
    chunks: List[Tuple[int, bytes]] = []
    with fitz.open(pdf_path) as doc:
        n = len(doc)
        if n == 0:
            return []
        start = 0
        while start < n:
            end = min(start + max_pages_per_chunk, n)
            sub = fitz.open()
            sub.insert_pdf(doc, from_page=start, to_page=end - 1)
            bio = io.BytesIO()
            sub.save(bio)
            chunks.append((start, bio.getvalue()))
            start = end
    return chunks


# ---------- Public high-level API: async parallel OCR + stitch ----------

async def ocr_pdf_to_markdown_mistral(
    pdf: str | Path,
    *,
    model: str = "mistral-ocr-latest",
    include_images: bool = False,
    images_folder: (Path, None) = None,
    max_pages_per_chunk: int = 200,
    max_workers: int = 4,
    timeout: float = 120.0,
) -> str:
    """
    High-level: split the PDF into chunks (by page), OCR each chunk in parallel,
    then stitch per-page Markdown back together with '# [Page N]' headers.
    """
    pdf_path = Path(pdf)
    # Split
    chunks = _split_pdf_into_chunks(pdf_path, max_pages_per_chunk=max_pages_per_chunk)
    if not chunks:
        return ""

    loop = asyncio.get_running_loop()
    stitched_pages: Dict[int, str] = {}

    def run_one(args: Tuple[int, bytes]) -> Tuple[int, List[Dict[str, Any]]]:
        start_idx, pdf_bytes = args
        pages = _mistral_ocr_call(pdf_bytes, model=model, include_images=include_images, timeout=timeout)
        if images_folder:
            pages.extract_images(images_folder)  # TODO: add folder informationhere
        # Adjust page indices to global indices
        adjusted = []
        for k, p in enumerate(pages):
            idx = p.get("index", k)
            # If index not provided, compute relative
            if idx is None:
                idx = k
            adjusted.append({"index": start_idx + int(idx), "markdown": p.get("markdown") or ""})
        return start_idx, adjusted

    # Run in a thread pool (mistralai client is blocking)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = [loop.run_in_executor(pool, run_one, c) for c in chunks]
        results = await asyncio.gather(*tasks)

    # Collect and stitch in order
    for _start, pages in results:
        for p in pages:
            stitched_pages[int(p["index"])] = p["markdown"] or ""

    # Ensure order
    if not stitched_pages:
        return ""

    final = []
    for page_idx in sorted(stitched_pages):
        mdp = stitched_pages[page_idx]
        final.append(f"# [Page {page_idx+1}]\n\n{mdp}".rstrip())

    return "\n\n".join(final).strip()
