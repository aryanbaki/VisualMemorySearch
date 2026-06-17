# Visual Memory Search

Visual Memory Search is a Streamlit app for uploading screenshots and finding them later with natural language search. It turns screenshots into searchable records, shows a gallery of saved images, and returns matching screenshots with scores and short explanations.

The app includes Demo Mode for public deployment. Demo Mode uses local sample logic and does not call OpenAI, so visitors can try the interface without using API credits.

## Technologies Used

- Python
- Streamlit
- OpenAI API for screenshot analysis and embeddings
- Pandas
- NumPy
- scikit-learn
- Pillow
- Local JSON storage

## Features

- Upload screenshot images.
- Analyze screenshot text, layout, and visual context.
- Save screenshot metadata in a local index.
- Search screenshots with plain English queries.
- Rank results with similarity scores.
- Show image previews beside search results.
- Use Demo Mode for a public no-cost version.
- Use full AI mode locally with an OpenAI API key.
- Keep screenshots and generated index files out of Git.

## How I Built It

I built the project as a Streamlit app because it let me create the upload, dashboard, gallery, and search workflow quickly in Python. The app separates the main interface from the helper modules:

- `app.py` controls the Streamlit screens and user actions.
- `src/analyzer.py` handles AI screenshot analysis.
- `src/search.py` handles embeddings and similarity search.
- `src/storage.py` saves uploaded files and the screenshot index.
- `src/demo_mode.py` keeps the public demo usable without an API key.

The main idea was to make screenshots work like searchable memory. Instead of remembering the exact file name, the user can search for what was on the screen, such as a login error, dashboard chart, blue button, or settings page.

## What I Learned

- How to organize a Streamlit app into smaller Python modules.
- How image uploads work in a web app.
- How AI-generated descriptions can make images searchable.
- How embeddings and cosine similarity can rank search results.
- How to keep API keys out of source code.
- How to build a public demo mode that does not spend API credits.
- How important it is to separate local data from files that should be committed.

## What I Would Improve

- Add user accounts so each person has a private screenshot library.
- Store files in cloud storage instead of local folders.
- Add tags, folders, and manual notes for each screenshot.
- Add OCR fallback for screenshots that do not need full AI vision.
- Add filters for date, app name, and screenshot type.
- Add a persistent database for deployed versions.
- Add a queue for analyzing many screenshots at once.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints in the terminal.

## Demo Mode

Demo Mode is best for public demos because it does not require an OpenAI API key.

Create `.streamlit/secrets.toml` locally if you want to force demo mode:

```toml
DEMO_MODE = true
```

## Full AI Mode

Full AI Mode uses OpenAI for screenshot analysis and embeddings.

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_api_key_here"
DEMO_MODE = false
```

Do not commit `.streamlit/secrets.toml`.

## Deploy

This app is ready for Streamlit Community Cloud.

Use these settings when creating the app:

- Repository: `aryanbaki/VisualMemorySearch`
- Branch: `main`
- Main file path: `app.py`

For a free public demo, add this Streamlit secret:

```toml
DEMO_MODE = true
```

Deploy from Streamlit Cloud:

```text
https://share.streamlit.io/
```

The deployed app can be shared after Streamlit finishes building it.

## Live App

Open the deployed project here:

```text
https://visualmemorysearch.streamlit.app/
```
