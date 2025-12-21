#!/usr/bin/env python3
# Minimal Mistral OCR -> Markdown
# 1) Set API_KEY and PDF_PATH below
# 2) `pip install mistralai`
# 3) run: python pdf_to_md_min.py
import os

API_KEY = "Lweua75g3hli597soqbPXkioGnfQnlK2"
PDF_PATH = r".\Cours - Rappels et complements sur les fonctions reelles.pdf"
OUTPUT_MD = 'mistralocr'  # or e.g. "out.md"
from pathlib import Path
from mistralai import Mistral
import base64
from pathlib import Path


def base64_to_jpg(b64_string: str, out_path: str | Path) -> Path:
    """Decode base64 string (UTF-8 encoded) and save as JPEG."""
    out_path = Path(out_path)
    img_data = base64.b64decode(b64_string.encode("utf-8"))
    out_path.write_bytes(img_data)
    return out_path


def stitch_markdown(ocr_resp, folder) -> str:
    parts = []
    # document_annotation (if present)
    doc_anno = getattr(ocr_resp, "document_annotation", None)
    if doc_anno:
        parts.append(f"**{doc_anno}**")
    if not folder.exists():
        os.mkdir(folder)

    # pages
    for page in getattr(ocr_resp, "pages", []):
        md = getattr(page, "markdown", "")
        # Inline images if available (image placeholders pattern from Mistral OCR)
        images = {getattr(img, "id", ""): img for img in getattr(page, "images", [])}
        for _id, _i in images.items():
            b64 = getattr(_i, "image_base64", "")
            if b64:
                filename = folder / _id
                b64 = b64[b64.find('base64,')+7:]
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

        parts.append(replace_placeholder(md))
    return ("\n\n".join(p for p in parts if p).strip() + "\n") if parts else ""


def main():
    if not API_KEY or API_KEY.startswith("YOUR_"):
        raise SystemExit("Please set API_KEY.")
    pdf_path = Path(PDF_PATH)
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")
    out = Path(OUTPUT_MD) if OUTPUT_MD else Path.cwd()
    if not out.exists():
        import os
        os.mkdir(out)

    client = Mistral(api_key=API_KEY)
    # try it without upload
    print('no upload')
    base64_pdf = base64.b64encode(pdf_path.read_bytes()).decode('utf-8')
    ocr_resp_b64 = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url",
                  "document_url": f'data:application/pdf;base64,{base64_pdf}'},
        include_image_base64=True,  # keep images inline in the markdown
    )
    print(ocr_resp_b64)
    md = stitch_markdown(ocr_resp_b64, out / 'images_b64')
    out = out / (pdf_path.stem + "_b64.md")
    out.write_text(md, encoding="utf-8")
    # 1/0
    print("[1/3] Uploading PDF…")
    uploaded = client.files.upload(
        file={"file_name": pdf_path.name, "content": open(pdf_path, "rb")},
        purpose="ocr",
    )

    print("[2/3] Getting signed URL…")
    signed = client.files.get_signed_url(file_id=uploaded.id)

    print("[3/3] Running OCR…")
    ocr_resp = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed.url},
        include_image_base64=True,  # keep images inline in the markdown
    )
    images = [ocr_resp.pages[i].images[0] for i in range(len(ocr_resp.pages)) if len(ocr_resp.pages[i].images) > 0]
    print(images[0])

    md = stitch_markdown(ocr_resp, out / 'images')
    out = out / (pdf_path.stem + ".md")
    out.write_text(md, encoding="utf-8")
    print(f"[OK] Markdown saved to: {out.resolve()}")


if __name__ == "__main__":
    main()
