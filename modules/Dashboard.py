import streamlit as st
import os


from login import require_admin


st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)


# -------------------------
# SECURITY
# -------------------------

require_admin()



# -------------------------
# SETTINGS
# -------------------------

UPLOAD_FOLDER = "uploads"



if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(
        UPLOAD_FOLDER
    )



# -------------------------
# COLLECT DATA
# -------------------------

files = os.listdir(
    UPLOAD_FOLDER
)


total_documents = len(files)


total_size = 0


file_types = {}



for file in files:


    path = os.path.join(
        UPLOAD_FOLDER,
        file
    )


    total_size += os.path.getsize(
        path
    )


    extension = os.path.splitext(
        file
    )[1].lower()


    if extension:

        file_types[extension] = file_types.get(
            extension,
            0
        ) + 1



storage_mb = round(
    total_size / (1024*1024),
    2
)



# -------------------------
# PAGE
# -------------------------

st.title(
    "📊 DocIntel AI Dashboard"
)


st.write(
    "System overview and document statistics."
)


st.divider()



# -------------------------
# METRICS
# -------------------------

col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "Total Documents",
        total_documents
    )



with col2:

    st.metric(
        "Storage Used",
        f"{storage_mb} MB"
    )



with col3:

    st.metric(
        "System Status",
        "Active"
    )



st.divider()



# -------------------------
# FILE TYPES
# -------------------------

st.subheader(
    "📁 Document Types"
)


if file_types:


    for file_type, amount in file_types.items():

        st.write(
            f"{file_type}: {amount}"
        )


else:

    st.info(
        "No documents uploaded."
    )