from pathlib import Path
from typing import Union

from PIL import Image, ImageStat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_screenshot_locally(path: Union[str, Path]) -> dict:
    image_path = Path(path)

    with Image.open(image_path) as image:
        width, height = image.size
        image_rgb = image.convert("RGB")
        mean_red, mean_green, mean_blue = ImageStat.Stat(image_rgb).mean

    orientation = "wide" if width >= height else "tall"
    brightness = (mean_red + mean_green + mean_blue) / 3
    tone = "dark" if brightness < 90 else "bright" if brightness > 175 else "balanced"
    dominant_color = max(
        [("red", mean_red), ("green", mean_green), ("blue", mean_blue)],
        key=lambda item: item[1],
    )[0]

    keywords = [
        image_path.stem.replace("_", " ").replace("-", " "),
        orientation,
        tone,
        dominant_color,
        "screenshot",
    ]

    search_summary = (
        f"{image_path.name} is a {orientation} {tone} screenshot with a dominant {dominant_color} tone. "
        f"The file is {width} by {height} pixels. This local demo analysis uses filename and image "
        "metadata instead of paid AI vision, so it is best for showing the upload, dashboard, gallery, "
        "and search flow without spending API credits."
    )

    return {
        "title": image_path.stem.replace("_", " ").replace("-", " ").title(),
        "ocr_text": "Demo mode does not run OCR or paid vision analysis.",
        "visual_description": search_summary,
        "keywords": keywords,
        "category": "demo",
        "search_summary": search_summary,
    }


def search_screenshots_locally(query: str, records: list[dict], top_k: int = 5) -> list[dict]:
    searchable_records = []
    documents = []

    for record in records:
        document = " ".join(
            [
                record.get("title", ""),
                record.get("ocr_text", ""),
                record.get("visual_description", ""),
                " ".join(record.get("keywords", [])),
                record.get("search_summary", ""),
                record.get("filename", ""),
            ]
        ).strip()

        if document:
            searchable_records.append(record)
            documents.append(document)

    if not searchable_records:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([query, *documents])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = [
        {**record, "score": float(score)}
        for record, score in zip(searchable_records, scores)
    ]
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_k]
