# modal_app.py
import hashlib
import json
import time

import modal

app = modal.App("pdf-multiconvert")
store = modal.Dict.from_name("pdf-jobs", create_if_missing=True)
vol   = modal.Volume.from_name("pdf-cache", create_if_missing=True)

image = (modal.Image.debian_slim()
         .apt_install("tesseract-ocr", "poppler-utils")  # si besoin
         .pip_install("docling", "pypdf2", "pdfminer.six"))

@app.function(image=image, timeout=900)
@modal.concurrent_inputs(8)
@modal.fastapi_endpoint(method="POST")
def submit(pdf_bytes: bytes, filename: str = "input.pdf") -> dict:
    job_id = hashlib.sha1(pdf_bytes).hexdigest()[:16]
    # persist the input PDF in volume (write-once)
    with vol.mount("/data"):
        path = f"/data/in/{job_id}_{filename}"
        import os; os.makedirs("/data/in", exist_ok=True)
        open(path, "wb").write(pdf_bytes)
    store[job_id] = {"status": "calculating", "created_at": time.time(), "filename": filename}
    # spawn async worker
    _worker.spawn(job_id, path)
    return {"job_id": job_id, "status": "accepted"}

@app.function(image=image, timeout=1200)
def _worker(job_id: str, pdf_path: str):
    try:
        # Docling conversion
        from docling.document_converter import DocumentConverter
        conv = DocumentConverter()
        doc  = conv.convert(pdf_path)
        md   = doc.render_as_markdown() if hasattr(doc,"render_as_markdown") else ""

        payload = {
            "docling_md": md,
            "meta": {"filename": pdf_path.split("/")[-1], "job_id": job_id}
        }
        with vol.mount("/data"):
            outp = f"/data/out/{job_id}.json"
            import os; os.makedirs("/data/out", exist_ok=True)
            open(outp, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False))

        store[job_id] = {"status": "done", "result_url": f"/fetch?job_id={job_id}"}
    except Exception as e:
        store[job_id] = {"status": "error", "error": str(e)}

@app.function(image=image, timeout=60)
@modal.fastapi_endpoint(method="GET")
def status(job_id: str) -> dict:
    if job_id not in store:
        return {"status": "unknown"}
    return store[job_id]

@app.function(image=image, timeout=60)
@modal.fastapi_endpoint(method="GET")
def fetch(job_id: str) -> dict:
    # renvoie le JSON packagé (persisté)
    if job_id not in store or store[job_id].get("status") != "done":
        return {"status": "not_ready"}
    import json
    import os
    with vol.mount("/data"):
        p = f"/data/out/{job_id}.json"
        if not os.path.exists(p):
            return {"status": "missing"}
        return json.load(open(p, "r", encoding="utf-8"))
