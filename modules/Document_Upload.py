import streamlit as st
import os
import json
from datetime import datetime

from login import require_login
from indexer import rebuild_index


st.set_page_config(
    page_title="Upload Document",
    page_icon="📤",
    layout="wide"
)


# -------------------------
# SECURITY
# -------------------------

require_login()


# -------------------------
# SETTINGS
# -------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


METADATA_FILE = os.path.join(
    BASE_DIR,
    "document_metadata.json"
)


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# -------------------------
# METADATA FUNCTIONS
# -------------------------

def load_metadata():

    if os.path.exists(METADATA_FILE):

        with open(
            METADATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return []



def save_metadata(data):

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )



# -------------------------
# PAGE
# -------------------------

st.title(
    "📤 Upload Document"
)


st.write(
    "Share documents with your organization."
)


st.divider()



# -------------------------
# FILE UPLOADER
# -------------------------

files = st.file_uploader(

    "Select documents",

    type=[

        # Documents
        "pdf",
        "docx",
        "doc",
        "txt",
        "rtf",

        # Spreadsheets
        "xlsx",
        "xls",
        "csv",

        # Presentations
        "pptx",
        "ppt",

        # Images
        "png",
        "jpg",
        "jpeg",
        "webp"

    ],

    accept_multiple_files=True

)



# -------------------------
# SAVE FILES
# -------------------------

if files:


    metadata = load_metadata()


    uploaded = 0


    for file in files:


        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.name
        )


        # Save file

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                file.getbuffer()
            )


        # Save metadata

        metadata.append({

            "filename": file.name,

            "uploaded_by": st.session_state.username,

            "role": st.session_state.role,

            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )

        })


        uploaded += 1



    save_metadata(
        metadata
    )


    # Build AI index

    count = rebuild_index()



    st.success(
        f"{uploaded} document(s) uploaded successfully."
    )


    st.success(
        f"AI index updated. {count} document(s) indexed."
    )