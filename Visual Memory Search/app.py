from pathlib import Path

from openai import APIError, OpenAIError, RateLimitError
import pandas as pd
import streamlit as st

from src.analyzer import analyze_screenshot
from src.search import get_embedding, search_screenshots
from src.storage import load_index, save_index, save_uploaded_file


st.set_page_config(page_title="Visual Memory Search", layout="wide")

st.title("Visual Memory Search")
st.caption("Upload screenshots, let AI understand them, then search them with natural language.")

api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key or api_key == "your_api_key_here":
    st.error("Add your OpenAI API key in .streamlit/secrets.toml before running the app.")
    st.stop()

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

                        embedding = get_embedding(searchable_text, api_key)

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
                            st.image(result["path"], use_container_width=True)
                        else:
                            st.warning("Image file not found.")

                    with col_details:
                        st.subheader(result["title"])
                        st.write(f"Score: {result['score']:.3f}")
                        st.write(f"Category: {result.get('category', 'other')}")
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
        st.dataframe(df, use_container_width=True)

        st.write("Gallery")
        gallery_cols = st.columns(3)

        for index, record in enumerate(records):
            with gallery_cols[index % 3]:
                if Path(record["path"]).exists():
                    st.image(record["path"], use_container_width=True)
                st.caption(record.get("title", record.get("filename", "")))
