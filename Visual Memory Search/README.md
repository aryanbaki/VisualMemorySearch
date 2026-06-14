# Visual Memory Search

A starter project for searching personal visual memories: screenshots, photos, saved images, and other visual notes.

## Project Structure

```text
Visual Memory Search/
├── app.py
├── config/
│   └── settings.example.toml
├── data/
│   ├── indexes/
│   ├── processed/
│   └── raw/
├── docs/
│   └── architecture.md
├── src/
│   └── visual_memory_search/
│       ├── core/
│       ├── services/
│       ├── storage/
│       └── ui/
└── tests/
```

## First Milestone

1. Upload or point the app at image files.
2. Extract image metadata and visual embeddings.
3. Store embeddings in a searchable index.
4. Search memories with natural language and image similarity.
