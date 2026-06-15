from pathlib import Path

from openai import APIError, OpenAIError, RateLimitError
import pandas as pd
import streamlit as st

from src.analyzer import analyze_screenshot
from src.demo_mode import analyze_screenshot_locally, search_screenshots_locally
from src.search import get_embedding, search_screenshots
from src.storage import load_index, save_index, save_uploaded_file


st.set_page_config(page_title="Visual Memory Search", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --space-0: #060916;
        --space-1: #0b1230;
        --space-2: #121a45;
        --panel: rgba(13, 20, 49, 0.88);
        --panel-strong: rgba(20, 30, 70, 0.94);
        --text: #f7fbff;
        --muted: #b8c5e8;
        --line: rgba(174, 207, 255, 0.22);
        --accent: #7dd3fc;
        --accent-2: #c084fc;
        --accent-3: #f8d477;
        --danger: #ff6b8a;
        --success: #68e3b0;
    }

    .stApp {
        color: var(--text);
        background:
            radial-gradient(circle at 8% 18%, rgba(125, 211, 252, 0.16) 0 1px, transparent 2px),
            radial-gradient(circle at 18% 72%, rgba(248, 212, 119, 0.22) 0 1px, transparent 2px),
            radial-gradient(circle at 32% 12%, rgba(255, 255, 255, 0.38) 0 1px, transparent 2px),
            radial-gradient(circle at 58% 24%, rgba(192, 132, 252, 0.24) 0 1px, transparent 2px),
            radial-gradient(circle at 78% 16%, rgba(255, 255, 255, 0.32) 0 1px, transparent 2px),
            radial-gradient(circle at 86% 76%, rgba(125, 211, 252, 0.22) 0 1px, transparent 2px),
            linear-gradient(145deg, #050713 0%, #0a1030 44%, #171142 100%);
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(circle, rgba(255, 255, 255, 0.42) 0 1px, transparent 1.6px),
            radial-gradient(circle, rgba(125, 211, 252, 0.36) 0 1px, transparent 1.8px),
            radial-gradient(circle, rgba(248, 212, 119, 0.32) 0 1px, transparent 1.8px);
        background-size: 140px 140px, 220px 220px, 310px 310px;
        background-position: 12px 18px, 72px 48px, 160px 90px;
        opacity: 0.42;
        z-index: 0;
    }

    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1180px;
        padding-top: 2.25rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(7, 12, 33, 0.96), rgba(17, 18, 58, 0.96));
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text);
    }

    .cosmic-hero {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.35rem 1.5rem 1.45rem;
        margin-bottom: 1.25rem;
        background:
            linear-gradient(135deg, rgba(18, 26, 69, 0.88), rgba(47, 31, 93, 0.78)),
            radial-gradient(circle at 92% 12%, rgba(248, 212, 119, 0.18), transparent 28%);
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
    }

    .cosmic-kicker {
        margin: 0 0 0.55rem;
        color: var(--accent-3);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .cosmic-title {
        margin: 0;
        color: var(--text);
        font-size: 3.1rem;
        line-height: 1.02;
        font-weight: 900;
        letter-spacing: 0;
        text-shadow: 0 0 28px rgba(125, 211, 252, 0.28);
    }

    .cosmic-caption {
        margin: 0.85rem 0 0;
        max-width: 780px;
        color: var(--muted);
        font-size: 1.12rem;
        line-height: 1.55;
        font-weight: 600;
    }

    h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] p,
    label,
    .stCaptionContainer,
    .stMetric label,
    .stMetric [data-testid="stMetricValue"] {
        color: var(--text);
    }

    p, span, div {
        color: inherit;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        gap: 0.4rem;
        border-bottom: 1px solid var(--line);
    }

    div[data-testid="stTabs"] button[role="tab"] {
        color: var(--muted);
        border-radius: 8px 8px 0 0;
        padding: 0.85rem 1rem;
        font-weight: 800;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--text);
        background: linear-gradient(135deg, rgba(125, 211, 252, 0.18), rgba(192, 132, 252, 0.18));
        border-bottom: 3px solid var(--accent);
    }

    div[data-testid="stFileUploaderDropzone"],
    div[data-testid="stForm"],
    div[data-testid="stExpander"],
    div[data-testid="stDataFrame"],
    div[data-testid="stAlert"],
    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stFileUploaderDropzone"] {
        padding: 1.15rem;
    }

    div[data-testid="stFileUploaderDropzone"] * {
        color: var(--text);
    }

    div[data-testid="stFileUploaderDropzone"] small,
    div[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] {
        color: var(--muted);
    }

    .stButton > button,
    div[data-testid="stFileUploader"] button {
        color: #06101f;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border: 0;
        border-radius: 8px;
        padding: 0.72rem 1rem;
        font-weight: 900;
        box-shadow: 0 12px 35px rgba(125, 211, 252, 0.24);
    }

    .stButton > button:hover,
    div[data-testid="stFileUploader"] button:hover {
        color: #020617;
        border: 0;
        filter: brightness(1.08);
        transform: translateY(-1px);
    }

    .stTextInput input {
        color: var(--text);
        background: rgba(8, 13, 35, 0.9);
        border: 1px solid rgba(125, 211, 252, 0.36);
        border-radius: 8px;
        min-height: 3.1rem;
        font-size: 1.02rem;
    }

    .stTextInput input::placeholder {
        color: rgba(184, 197, 232, 0.76);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line);
        background: var(--panel-strong);
        border-radius: 8px;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.24);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        color: var(--text);
        background: rgba(255, 107, 138, 0.14);
        border: 1px solid rgba(255, 107, 138, 0.38);
        box-shadow: none;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 107, 138, 0.24);
        color: var(--text);
    }

    .stAlert {
        color: var(--text);
    }

    .stAlert p {
        color: var(--text);
        font-weight: 650;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .cosmic-title {
            font-size: 2.2rem;
        }

        .cosmic-caption {
            font-size: 1rem;
        }
    }
    </style>

    <div class="cosmic-hero">
        <p class="cosmic-kicker">Night-sky screenshot memory</p>
        <h1 class="cosmic-title">Visual Memory Search</h1>
        <p class="cosmic-caption">
            Upload screenshots, let AI map the text and visual context, then search your visual memory
            with natural language.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key = st.secrets.get("OPENAI_API_KEY", "")
has_api_key = bool(api_key and api_key != "your_api_key_here")
default_demo_mode = st.secrets.get("DEMO_MODE", True)

records = load_index()


def show_openai_error(error: OpenAIError) -> None:
    if isinstance(error, RateLimitError):
        error_payload = getattr(error, "body", {}) or {}
        error_code = error_payload.get("code") if isinstance(error_payload, dict) else None

        if error_code == "insufficient_quota":
            st.error("OpenAI API quota or billing is not active for this API key.")
            st.info(
                "Check your API billing, credits, and usage limits in the OpenAI Platform dashboard. "
                "ChatGPT Pro does not include API usage."
            )
            return

        st.error("OpenAI rate limit reached. Wait a bit, then try again with fewer screenshots.")
        return

    if isinstance(error, APIError):
        st.error("OpenAI returned an API error. Check the message below and try again.")
        st.code(str(error), language="text")
        return

    st.error("OpenAI request failed. Check your API key, billing, and network connection.")
    st.code(str(error), language="text")

with st.sidebar:
    st.header("App Controls")
    demo_mode = st.toggle("Demo mode - no API credits", value=bool(default_demo_mode))

    if demo_mode:
        st.info("Demo mode uses local image metadata and local text search. No OpenAI API calls are made.")
    elif not has_api_key:
        st.error("Add OPENAI_API_KEY in .streamlit/secrets.toml or turn demo mode back on.")
        st.stop()

    st.write(f"Indexed screenshots: {len(records)}")

    if st.button("Clear index"):
        save_index([])
        st.success("Index cleared.")
        st.rerun()

tab_upload, tab_search, tab_dashboard = st.tabs(["Upload & Analyze", "Search", "Dashboard"])

with tab_upload:
    st.subheader("Upload screenshots")

    uploaded_files = st.file_uploader(
        "Upload PNG or JPG screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.write(f"{len(uploaded_files)} file(s) selected.")

        if st.button("Analyze screenshots"):
            progress = st.progress(0)
            had_error = False

            for index, uploaded_file in enumerate(uploaded_files):
                file_path = save_uploaded_file(uploaded_file)

                with st.spinner(f"Analyzing {uploaded_file.name}..."):
                    try:
                        if demo_mode:
                            analysis = analyze_screenshot_locally(file_path)
                        else:
                            analysis = analyze_screenshot(file_path, api_key)

                        searchable_text = " ".join(
                            [
                                analysis.get("title", ""),
                                analysis.get("ocr_text", ""),
                                analysis.get("visual_description", ""),
                                " ".join(analysis.get("keywords", [])),
                                analysis.get("search_summary", ""),
                            ]
                        )

                        embedding = [] if demo_mode else get_embedding(searchable_text, api_key)

                        record = {
                            "filename": uploaded_file.name,
                            "path": file_path,
                            "title": analysis.get("title", uploaded_file.name),
                            "ocr_text": analysis.get("ocr_text", ""),
                            "visual_description": analysis.get("visual_description", ""),
                            "keywords": analysis.get("keywords", []),
                            "category": analysis.get("category", "other"),
                            "search_summary": analysis.get("search_summary", ""),
                            "embedding": embedding,
                            "analysis_mode": "demo" if demo_mode else "openai",
                        }

                        records.append(record)
                        save_index(records)
                    except OpenAIError as error:
                        show_openai_error(error)
                        had_error = True
                        break

                progress.progress((index + 1) / len(uploaded_files))

            if not had_error:
                st.success("Screenshots analyzed and indexed.")
                st.rerun()

with tab_search:
    st.subheader("Search screenshots")

    query = st.text_input(
        "Search with natural language",
        placeholder="Example: login error, dashboard chart, blue button, code editor",
    )

    if query:
        try:
            if demo_mode:
                results = search_screenshots_locally(query, records, top_k=5)
            else:
                results = search_screenshots(query, records, api_key, top_k=5)
        except OpenAIError as error:
            show_openai_error(error)
            st.stop()

        if not results:
            st.warning("No results found yet.")
        else:
            for result in results:
                with st.container(border=True):
                    col_image, col_details = st.columns([1, 2])

                    with col_image:
                        if Path(result["path"]).exists():
                            st.image(result["path"], width="stretch")
                        else:
                            st.warning("Image file not found.")

                    with col_details:
                        st.subheader(result["title"])
                        st.write(f"Score: {result['score']:.3f}")
                        st.write(f"Category: {result.get('category', 'other')}")
                        st.write(f"Mode: {result.get('analysis_mode', 'openai')}")
                        st.write("Keywords:", ", ".join(result.get("keywords", [])))
                        st.write("Why it matched:")
                        st.write(result.get("search_summary", ""))

                        with st.expander("OCR text"):
                            st.write(result.get("ocr_text", ""))

                        with st.expander("Visual description"):
                            st.write(result.get("visual_description", ""))

with tab_dashboard:
    st.subheader("Screenshot Index Dashboard")

    if not records:
        st.info("Upload and analyze screenshots first.")
    else:
        df = pd.DataFrame(
            [
                {
                    "filename": record.get("filename"),
                    "title": record.get("title"),
                    "category": record.get("category"),
                    "keywords": ", ".join(record.get("keywords", [])),
                    "summary": record.get("search_summary", ""),
                }
                for record in records
            ]
        )

        col_count, col_categories, col_keywords = st.columns(3)

        with col_count:
            st.metric("Screenshots Indexed", len(records))

        with col_categories:
            st.metric("Categories", df["category"].nunique())

        with col_keywords:
            avg_keywords = df["keywords"].apply(lambda value: len(value.split(",")) if value else 0).mean()
            st.metric("Avg Keywords", f"{avg_keywords:.1f}")

        st.write("Category breakdown")
        st.bar_chart(df["category"].value_counts())

        st.write("Indexed screenshots")
        st.dataframe(df, width="stretch")

        st.write("Gallery")
        gallery_cols = st.columns(3)

        for index, record in enumerate(records):
            with gallery_cols[index % 3]:
                if Path(record["path"]).exists():
                    st.image(record["path"], width="stretch")
                st.caption(record.get("title", record.get("filename", "")))
