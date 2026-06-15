# Visual Memory Search

Visual Memory Search is a Streamlit app that lets users upload screenshots, analyze them with AI, and search through them using natural language.

The app also includes a no-cost demo mode for public demos. Demo mode does not call OpenAI. It uses local image metadata and local text similarity so visitors can try the upload, gallery, dashboard, and search flow without using API credits.

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

For a deployed demo that does not spend API credits, use:

```toml
DEMO_MODE = true
```

In demo mode, the OpenAI key is optional because no OpenAI API calls are made.

Run the app:

```bash
streamlit run app.py
```

## Run With Your Own OpenAI Credits

By default, the app starts in demo mode so it does not spend OpenAI API credits. Demo mode is useful for trying the interface, uploading screenshots, viewing the dashboard, and testing local search.

To use the full AI version, each person should use their own OpenAI API key. The full AI version sends screenshots to OpenAI for visual analysis and creates embeddings for semantic search, so it can create API charges on that person's OpenAI API account.

### 1. Get An OpenAI API Key

Create or sign in to an OpenAI Platform account:

```text
https://platform.openai.com/api-keys
```

Create a new secret key and keep it private. Do not paste it into `app.py`, GitHub, Discord, screenshots, or public docs.

### 2. Add Local Secrets

Create this file if it does not already exist:

```text
.streamlit/secrets.toml
```

Paste this into it:

```toml
OPENAI_API_KEY = "paste_your_api_key_here"
DEMO_MODE = false
```

`DEMO_MODE = false` tells the app to use the real OpenAI vision and embedding pipeline.

### 3. Install And Run

Use these commands from the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then upload a few screenshots and click `Analyze screenshots`.

### 4. Set A Budget Limit

Before testing a lot of screenshots, set a small OpenAI API budget or usage limit:

```text
https://platform.openai.com/settings/organization/limits
```

ChatGPT Plus or Pro does not include OpenAI API usage. The API is billed separately through the OpenAI Platform account connected to the API key.

## Streamlit Cloud Secrets

If you deploy this app publicly, keep demo mode on unless you intentionally want to pay for users' API calls.

For a no-cost public demo, add this in Streamlit Cloud secrets:

```toml
DEMO_MODE = true
```

Do not add `OPENAI_API_KEY` for the public demo unless you are comfortable with visitors using your API credits.

If someone forks the project and wants the full AI version, they should add their own secrets in their own Streamlit app:

```toml
OPENAI_API_KEY = "their_api_key_here"
DEMO_MODE = false
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
