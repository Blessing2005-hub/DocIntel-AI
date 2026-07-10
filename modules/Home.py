import streamlit as st
from branding import show_logo


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)


# -------------------------
# BRANDING
# -------------------------

show_logo()



# -------------------------
# HOME CONTENT
# -------------------------

st.title(
    "📄 DocIntel AI"
)


st.subheader(
    "Enterprise Document Intelligence Platform"
)


st.write(
    """
DocIntel AI helps organizations store, search,
and interact with official documents using
Artificial Intelligence.
"""
)


st.divider()



# -------------------------
# FEATURES
# -------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        """
📤 Document Management

Upload and organize
official documents.
"""
    )



with col2:

    st.info(
        """
🔍 Intelligent Search

Find information quickly
using document search.
"""
    )



with col3:

    st.info(
        """
🤖 AI Assistant

Ask questions,
summarize documents,
and create briefings.
"""
    )



st.divider()


st.caption(
    "DocIntel AI | Enterprise Document Intelligence System"
)