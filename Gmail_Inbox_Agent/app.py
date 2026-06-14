from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "mock_emails.csv"


def load_mock_emails() -> pd.DataFrame:
    """Load demo inbox data until Gmail integration is implemented."""
    return pd.read_csv(DATA_PATH)


st.set_page_config(page_title="Gmail Inbox Agent", layout="wide")

st.title("Gmail Inbox Agent")
st.caption(
    "A starter Streamlit app for reviewing, grouping, prioritizing, and eventually archiving Gmail inbox messages."
)

with st.sidebar:
    st.header("Demo Mode")
    st.write("Using fake inbox data. Gmail connection will be added in a later iteration.")

emails = load_mock_emails()

st.info("Gmail connection will be added in a later iteration. No credentials are needed yet.")
st.dataframe(emails, use_container_width=True)
