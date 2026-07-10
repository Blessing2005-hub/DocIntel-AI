import streamlit as st
import json
import os
import difflib


from login import require_login


st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# -------------------------
# SECURITY
# -------------------------

require_login()



# -------------------------
# LOAD INDEX
# -------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


INDEX_FILE = os.path.join(
    BASE_DIR,
    "document_index.json"
)



def load_documents():

    if os.path.exists(INDEX_FILE):

        with open(
            INDEX_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return []



documents = load_documents()



# -------------------------
# LANGUAGE UNDERSTANDING
# -------------------------

def correct_word(word):

    common_words = {

        "summerise": "summarise",
        "summarize": "summarise",
        "sumarise": "summarise",
        "brief": "brief",
        "brif": "brief",
        "explane": "explain",
        "explain": "explain",
        "point": "points"

    }


    word = word.lower()


    if word in common_words:

        return common_words[word]


    matches = difflib.get_close_matches(
        word,
        common_words.keys(),
        n=1,
        cutoff=0.75
    )


    if matches:

        return common_words[matches[0]]


    return word




def detect_request(question):

    words = [
        correct_word(word)
        for word in question.lower().split()
    ]


    text = " ".join(words)



    if "summarise" in text:

        return "summary"



    if "brief" in text or "overview" in text:

        return "brief"



    if "point" in text:

        return "points"



    if "explain" in text:

        return "explain"



    return "answer"




# -------------------------
# AI FUNCTIONS
# -------------------------

def summarize(text):

    sentences = text.split(".")


    return ".".join(
        sentences[:5]
    ) + "."




def briefing(text):

    words = text.split()


    return " ".join(
        words[:150]
    ) + "..."




def key_points(text):

    sentences = text.split(".")


    return [
        s.strip()
        for s in sentences[:7]
        if s.strip()
    ]



# -------------------------
# PAGE
# -------------------------

st.title(
    "🤖 DocIntel AI Assistant"
)



st.write(
"""
Ask questions or request tasks from your documents.

Examples:

• Summarize the procurement policy

• Give me a briefing on this document

• Extract key points

• Explain this information
"""
)



st.divider()



question = st.text_area(
    "What would you like me to do?"
)



if question:


    if not documents:

        st.warning(
            "No indexed documents available."
        )

        st.stop()



    matched = []



    # Search documents

    for document in documents:


        content = document.get(
            "content",
            ""
        ).lower()


        words = question.split()


        score = 0


        for word in words:

            word = correct_word(word)


            if word in content:

                score += 1



        if score > 0:

            matched.append(document)




    if matched:


        request_type = detect_request(
            question
        )



        for document in matched:


            st.subheader(
                "📄 "
                + document["filename"]
            )


            content = document["content"]



            if request_type == "summary":

                st.write(
                    "### Summary"
                )

                st.write(
                    summarize(content)
                )



            elif request_type == "brief":

                st.write(
                    "### Briefing"
                )

                st.write(
                    briefing(content)
                )



            elif request_type == "points":

                st.write(
                    "### Key Points"
                )


                for point in key_points(content):

                    st.write(
                        "• " + point
                    )



            elif request_type == "explain":

                st.write(
                    "### Explanation"
                )

                st.write(
                    content[:1000]
                )



            else:

                st.write(
                    content[:1000]
                )



            st.divider()



    else:


        st.warning(
            "I could not find information related to your request."
        )