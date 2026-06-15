import base64
import json
import mimetypes
from pathlib import Path
from typing import Union

from openai import OpenAI


VISION_MODEL = "gpt-4.1-mini"


def image_to_base64(path: Union[str, Path]) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_screenshot(path: Union[str, Path], api_key: str) -> dict:
    client = OpenAI(api_key=api_key)
    image_path = Path(path)
    image_base64 = image_to_base64(path)
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"

    prompt = """
Analyze this screenshot for a visual memory search app.

Return only valid JSON with these fields:
{
  "title": "short screenshot title",
  "ocr_text": "all readable text you can see",
  "visual_description": "describe UI layout, colors, buttons, charts, errors, icons, and important objects",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "category": "login/error/dashboard/code/email/form/other",
  "search_summary": "one paragraph that combines OCR and visual meaning"
}
"""

    response = client.responses.create(
        model=VISION_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    text = response.output_text.strip()
    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "title": "Screenshot",
            "ocr_text": "",
            "visual_description": text,
            "keywords": [],
            "category": "other",
            "search_summary": text,
        }
