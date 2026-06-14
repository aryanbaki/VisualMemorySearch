# Architecture

Visual Memory Search is organized around a small pipeline:

1. Ingest images from local files.
2. Normalize and store metadata.
3. Generate embeddings for image search.
4. Persist the searchable index.
5. Provide a UI for querying and browsing results.

The current scaffold keeps these concerns separate so each piece can be built and tested independently.
