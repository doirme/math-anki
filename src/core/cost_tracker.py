from __future__ import annotations
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..db.models import LLMUsage

class CostTracker:
    """
    Tracks LLM usage and costs.
    """
    def __init__(self, session: Session):
        self.session = session

    def track_usage(
        self,
        task_name: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cost_usd: float = 0.0
    ):
        """
        Record LLM usage to the database.
        """
        usage = LLMUsage(
            task_name=task_name,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd
        )
        self.session.add(usage)
        self.session.commit()
