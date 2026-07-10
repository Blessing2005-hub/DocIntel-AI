import streamlit as st
import os


def show_logo():

    logo_path = "logo.jpg"

    if os.path.exists(logo_path):

        st.image(
            logo_path,
            width=180
        )

    else:

        st.warning(
            "Logo not found. Add logo.jpg to the main project folder."
        )


def show_sidebar_branding():

    logo_path = "logo.jpg.jpg"

    if os.path.exists(logo_path):

        st.sidebar.image(
            logo_path,
            width=150
        )