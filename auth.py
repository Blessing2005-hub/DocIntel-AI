import sqlite3
import hashlib
from datetime import datetime

from database import get_connection


# -------------------------
# PASSWORD SECURITY
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
            role
            )

            VALUES (?,?,?)
            """,

            (
                username,
                hash_password(password),
                role
            )
        )


        connection.commit()

        return True


    except sqlite3.IntegrityError:

        return False


    finally:

        connection.close()



# -------------------------
# LOGIN CHECK
# -------------------------

def authenticate(
        username,
        password
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT username, role
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

        return {
            "username": user[0],
            "role": user[1]
        }


    return None