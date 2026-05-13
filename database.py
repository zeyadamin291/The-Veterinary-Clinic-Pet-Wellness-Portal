import sqlite3
import os

DB_NAME = "clinic_database.db"
SCHEMA_FILE = "schema.sql"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    if not os.path.exists(SCHEMA_FILE):
        print("schema.sql missing")
        return False

    conn = connect()
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql = f.read()

    # SQLite fixes
    sql = sql.replace("INT IDENTITY(1,1) PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sql = sql.replace("INT IDENTITY(1,1)", "INTEGER")
    sql = sql.replace("MAX", "")
    sql = sql.replace("GETDATE()", "DATE('now')")

    cursor.executescript(sql)
    conn.commit()
    conn.close()
    return True


def execute_query(query, params=(), fetch=False):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, params)

    data = None
    if fetch:
        data = cursor.fetchall()

    conn.commit()
    conn.close()
    return data