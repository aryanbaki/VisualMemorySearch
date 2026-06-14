from pathlib import Path

from visual_memory_search.services.ingestion import ingest_image


def test_ingest_image_uses_file_name_as_title() -> None:
    memory = ingest_image(Path("example.png"))

    assert memory.id == "example"
    assert memory.title == "example.png"
