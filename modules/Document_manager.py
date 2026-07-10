import streamlit as st
import os
import json


from login import require_admin



st.set_page_config(
    page_title="Document Manager",
    page_icon="📂",
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

METADATA_FILE = "document_metadata.json"



if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(
        UPLOAD_FOLDER
    )



# -------------------------
# LOAD METADATA
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
    "📂 Document Manager"
)


st.write(
    "Manage organization documents."
)


st.divider()



documents = load_metadata()



if documents:



    search = st.text_input(
        "🔍 Search documents"
    )



    for document in documents:



        filename = document["filename"]



        if search.lower() in filename.lower():



            path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )



            if os.path.exists(path):


                size = round(
                    os.path.getsize(path) / 1024,
                    2
                )



                col1, col2, col3, col4 = st.columns(
                    [4,2,2,1]
                )



                with col1:

                    st.write(
                        "📄",
                        filename
                    )



                with col2:

                    st.write(
                        "Uploaded by:"
                    )

                    st.write(
                        document["uploaded_by"]
                    )



                with col3:

                    st.write(
                        document["date"]
                    )

                    st.write(
                        f"{size} KB"
                    )



                with col4:


                    if st.button(
                        "🗑",
                        key=filename
                    ):



                        os.remove(
                            path
                        )


                        documents.remove(
                            document
                        )


                        save_metadata(
                            documents
                        )


                        st.success(
                            "Document deleted."
                        )


                        st.rerun()



                st.divider()



else:


    st.info(
        "No documents uploaded."
    )