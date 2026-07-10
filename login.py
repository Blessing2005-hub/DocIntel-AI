import streamlit as st
import json
import os
import hashlib


USERS_FILE = "users.json"


# -------------------------
# DATABASE FUNCTIONS
# -------------------------

def load_users():

    if os.path.exists(USERS_FILE):

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return []



def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )



def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# -------------------------
# LOGIN SYSTEM
# -------------------------

def login():


    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "role" not in st.session_state:
        st.session_state.role = ""



    if st.session_state.logged_in:

        return True



    st.title("🔐 DocIntel AI")


    option = st.radio(
        "Choose an option",
        [
            "Sign In",
            "Create Account"
        ]
    )



    # -------------------------
    # SIGN IN
    # -------------------------

    if option == "Sign In":


        email = st.text_input(
            "Work Email"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button("Sign In"):


            users = load_users()


            for user in users:


                if (
                    user["email"] == email
                    and user["password"] == hash_password(password)
                ):


                    st.session_state.logged_in = True

                    st.session_state.username = user["name"]

                    st.session_state.role = user["role"]


                    st.rerun()



            st.error(
                "Invalid email or password"
            )



    # -------------------------
    # CREATE ACCOUNT
    # -------------------------

    else:


        st.subheader(
            "Create Organization Account"
        )


        name = st.text_input(
            "Full Name"
        )


        company = st.text_input(
            "Organization Name"
        )


        ec = st.text_input(
            "Company EC Number"
        )


        email = st.text_input(
            "Work Email"
        )


        password = st.text_input(
            "Create Password",
            type="password"
        )


        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )


        role = st.selectbox(
            "Role",
            [
                "Employee",
                "Admin"
            ]
        )



        if st.button("Create Account"):


            users = load_users()


            if password != confirm:

                st.error(
                    "Passwords do not match"
                )

                return False



            if any(
                user["email"] == email
                for user in users
            ):

                st.error(
                    "Account already exists"
                )

                return False



            new_user = {

                "name": name,

                "company": company,

                "ec": ec,

                "email": email,

                "password": hash_password(password),

                "role": role

            }



            users.append(
                new_user
            )


            save_users(
                users
            )


            st.success(
                "Account created. You can now sign in."
            )


    return False



# -------------------------
# SECURITY
# -------------------------

def require_login():

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.error(
            "Please sign in first."
        )

        st.stop()



def require_admin():

    require_login()


    if st.session_state.role != "Admin":

        st.error(
            "Admin access required."
        )

        st.stop()