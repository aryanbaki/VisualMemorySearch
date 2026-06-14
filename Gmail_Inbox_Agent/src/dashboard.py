import pandas as pd
import streamlit as st


def render_email_table(emails: pd.DataFrame) -> None:
    """Render the main inbox review table in Streamlit."""
    st.dataframe(emails, use_container_width=True)


def render_status_message() -> None:
    """Show the current scaffold status to the user."""
    st.info("Demo mode is active. Gmail connection will be added later.")
