# Visual Memory Search

Visual Memory Search is a Streamlit app that lets users upload screenshots, analyze them with AI, and search through them using natural language.

## What The App Does

1. Upload screenshots.
2. Analyze screenshot text and visual UI.
3. Store screenshot metadata locally.
4. Create embeddings from searchable screenshot summaries.
5. Search screenshots using natural language.
6. Return the top 5 matches with image previews, confidence scores, and explanations.

## Tech Stack

- Python
- Streamlit
- OpenAI vision and embeddings
- Pandas
- NumPy
- scikit-learn
- Pillow

## Project Structure

```text
Visual Memory Search/
  app.py
  requirements.txt
  README.md
  .gitignore
  .streamlit/
    secrets.toml
  src/
    __init__.py
    analyzer.py
    search.py
    storage.py
  data/
    index.json
    screenshots/
      .gitkeep
```

## File Purpose

`app.py` is the main Streamlit dashboard.

`src/analyzer.py` sends screenshots to the AI model and returns structured screenshot analysis.

`src/search.py` creates embeddings and ranks screenshots using cosine similarity.

`src/storage.py` saves uploaded screenshots and loads/saves the local JSON index.

`data/index.json` stores screenshot metadata and embeddings during local development.

`data/screenshots/` stores uploaded screenshot image files during local development.

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your OpenAI API key in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

Run the app:

```bash
streamlit run app.py
```

## Demo Flow

Upload 5 to 10 screenshots, click Analyze, then try searches like:

- login error
- blue button
- dashboard chart
- authentication warning
- table with user data
- code editor

The core loop is:

```text
screenshot -> AI understanding -> embedding -> search result -> visual proof
```
