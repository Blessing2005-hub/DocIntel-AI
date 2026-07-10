import sqlite3
import os
from datetime import datetime


DATABASE_FOLDER = "database"

DATABASE_FILE = os.path.join(
    DATABASE_FOLDER,
    "docintel.db"
)



# -------------------------
# CREATE DATABASE
# -------------------------

def get_connection():

    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)

    return sqlite3.connect(
        DATABASE_FILE
    )



def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()



    # Users table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT

    )
    """)



    # Documents table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        uploaded_by TEXT,

        upload_date TEXT,

        file_path TEXT

    )
    """)



    # Audit logs

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        action TEXT,

        timestamp TEXT

    )
    """)



    connection.commit()

    connection.close()




# -------------------------
# ADD DOCUMENT
# -------------------------

def add_document(
        filename,
        username,
        path
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO documents
        (
        filename,
        uploaded_by,
        upload_date,
        file_path
        )

        VALUES (?,?,?,?)
        """,

        (
            filename,
            username,
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),
            path
        )

    )


    connection.commit()

    connection.close()



# -------------------------
# GET DOCUMENTS
# -------------------------

def get_documents():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM documents
        """
    )


    data = cursor.fetchall()


    connection.close()


    return data