import sqlite3
import hashlib
from datetime import datetime

from database import get_connection



# -------------------------
# PASSWORD HASHING
# -------------------------

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# -------------------------
# CREATE USER
# -------------------------

def create_user(
        username,
        password,
        role="Employee"
):

    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO users
            (
            username,
            password,
            role,
            status,
            created_date
            )

            VALUES (?,?,?,?,?)
            """,

            (
                username,
                hash_password(password),
                role,
                "Active",
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )
            )
        )


        connection.commit()

        return True



    except sqlite3.IntegrityError:

        return False



    finally:

        connection.close()



# -------------------------
# AUTHENTICATE USER
# -------------------------

def authenticate(
        username,
        password
):

    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT username, role, status

        FROM users

        WHERE username=?
        AND password=?
        """,

        (
            username,
            hash_password(password)
        )
    )


    user = cursor.fetchone()


    connection.close()



    if user:

        if user[2] == "Active":

            return {

                "username": user[0],

                "role": user[1]

            }


    return None



# -------------------------
# GET USERS
# -------------------------

def get_users():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT id,
               username,
               role,
               status,
               created_date

        FROM users
        """
    )


    users = cursor.fetchall()


    connection.close()


    return users