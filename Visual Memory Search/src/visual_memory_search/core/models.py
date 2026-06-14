from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class VisualMemory(BaseModel):
    id: str
    source_path: Path
    title: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
