from pathlib import Path

from visual_memory_search.core.models import VisualMemory


def ingest_image(path: Path) -> VisualMemory:
    return VisualMemory(id=path.stem, source_path=path, title=path.name)
