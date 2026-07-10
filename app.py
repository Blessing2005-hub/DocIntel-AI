import streamlit as st
import os

from login import login
from branding import show_sidebar_branding


st.set_page_config(
    page_title="DocIntel AI",
    page_icon="📄",
    layout="wide"
)


# LOGIN FIRST

if not login():
    st.stop()



# SIDEBAR

with st.sidebar:

    show_sidebar_branding()

    st.write(
        f"Welcome: {st.session_state.username}"
    )

    st.write(
        f"Role: {st.session_state.role}"
    )

    st.divider()


    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()



# USER PAGES

pages = {

    "Main": [

        st.Page(
            "modules/Home.py",
            title="Home",
            icon="🏠"
        )

    ],


    "Documents": [

        st.Page(
            "modules/Document_Upload.py",
            title="Upload Document",
            icon="📤"
        ),

        st.Page(
            "modules/Intelligent_Search.py",
            title="Intelligent Search",
            icon="🔍"
        ),


        st.Page(
            "modules/AI_Assistant.py",
            title="AI Assistant",
            icon="🤖"
        )

    ]

}



# ADMIN ONLY

if st.session_state.role == "Admin":


    pages["Administration"] = [

        st.Page(
            "modules/Document_Manager.py",
            title="Document Manager",
            icon="📂"
        ),


        st.Page(
            "modules/Dashboard.py",
            title="Dashboard",
            icon="📊"
        )

    ]



navigation = st.navigation(pages)

navigation.run()