from __future__ import annotations
from pathlib import Path
from typing import Optional
import os
import time
import requests


def marker_pdf_to_markdown(
    pdf_path: Path,
    *,
    api_key: Optional[str] = None,
    timeout: float = 300.0,
    poll_interval: float = 2.0,
) -> Optional[str]:
    """
    Convert PDF to Markdown using Datalab Marker API.
    
    Args:
        pdf_path: Path to PDF file
        api_key: Marker API key (defaults to MARKER_API_KEY env var or config)
        timeout: Maximum time to wait for conversion (seconds)
        poll_interval: Time between status checks (seconds)
    
    Returns:
        Markdown string if successful, None otherwise
    """
    # Try provided key, then env var, then config
    if not api_key:
        api_key = os.getenv("MARKER_API_KEY")
    if not api_key:
        try:
            from .config import settings
            api_key = getattr(settings, "marker_api_key", None)
        except Exception:
            pass
    
    # Default API key provided by user
    if not api_key:
        api_key = "R2Pqv9_EXOmKWR8oSKY-YlaZFPDdkOag6BkY8tDqYlQ"
    
    if not api_key:
        return None
    
    base_url = "https://www.datalab.to/api/v1/marker"
    
    try:
        # 1. Submit PDF
        with open(pdf_path, "rb") as f:
            files = {"file": (pdf_path.name, f, "application/pdf")}
            headers = {"X-Api-Key": api_key}
            
            response = requests.post(
                base_url,
                files=files,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()
            submission_data = response.json()
        
        # 2. Get check URL
        check_url = submission_data.get("request_check_url")
        if not check_url:
            return None
        
        # 3. Poll for completion
        start_time = time.time()
        while time.time() - start_time < timeout:
            headers = {"X-Api-Key": api_key}
            status_response = requests.get(check_url, headers=headers, timeout=30.0)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data.get("status", "").lower()
            
            if status == "complete":
                # Get the markdown content
                markdown = status_data.get("markdown") or status_data.get("result", {}).get("markdown")
                if markdown:
                    return markdown
                # Sometimes the markdown is in a different field
                return status_data.get("content") or None
            
            elif status == "failed" or status == "error":
                return None
            
            # Still processing, wait and retry
            time.sleep(poll_interval)
        
        # Timeout
        return None
        
    except Exception:
        return None

