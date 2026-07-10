import streamlit as st

from auth import authenticate


# -------------------------
# LOGIN SYSTEM
# -------------------------

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


    if st.session_state.logged_in:
        return True



    st.title("🔐 DocIntel AI Login")


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if st.button("Login"):


        user = authenticate(
            username,
            password
        )


        if user:


            st.session_state.logged_in = True

            st.session_state.username = user["username"]

            st.session_state.role = user["role"]


            st.success(
                "Login successful"
            )


            st.rerun()


        else:

            st.error(
                "Invalid username or password"
            )


    return False



# -------------------------
# ROLE SECURITY
# -------------------------

def require_login():

    if not login():

        st.stop()



def require_admin():

    require_login()


    if st.session_state.role != "Admin":

        st.error(
            "Admin access required"
        )

        st.stop()