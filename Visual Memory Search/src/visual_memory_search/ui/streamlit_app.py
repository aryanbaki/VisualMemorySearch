import streamlit as st

from visual_memory_search.services.search import search_memories


def main() -> None:
    st.set_page_config(page_title="Visual Memory Search")
    st.title("Visual Memory Search")

    query = st.text_input("Search your visual memories")

    if query:
        results = search_memories(query)
        st.caption(f"{len(results)} result(s)")
    else:
        st.caption("Add images and search by what you remember seeing.")
