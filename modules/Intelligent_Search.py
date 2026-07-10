import streamlit as st
import os


st.set_page_config(
    page_title="DocIntel AI - Intelligent Search",
    page_icon="🔍",
    layout="wide"
)


# -------------------------
# SETTINGS
# -------------------------

UPLOAD_FOLDER = "uploads"


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# -------------------------
# INTELLIGENT SEARCH
# -------------------------

st.subheader("🔍 Search documents")


files = sorted(
    os.listdir(UPLOAD_FOLDER)
)


search = st.text_input(
    "Search documents",
    placeholder="Type document name or keyword..."
)


st.divider()



if search:

    results = [
        file for file in files
        if search.lower() in file.lower()
    ]


    if results:

        st.success(
            f"{len(results)} document(s) found"
        )


        for file in results:

            path = os.path.join(
                UPLOAD_FOLDER,
                file
            )


            size = round(
                os.path.getsize(path) / 1024,
                2
            )


            col1, col2 = st.columns(
                [5, 2]
            )


            with col1:

                st.write(
                    f"📄 {file}"
                )


            with col2:

                st.write(
                    f"{size} KB"
                )


    else:

        st.warning(
            "No documents found."
        )


else:

    st.info(
        "Enter a keyword to search documents."
    )