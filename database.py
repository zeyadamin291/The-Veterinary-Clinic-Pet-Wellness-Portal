import os
import sqlite3

DB_NAME = "clinic_database.db"
SCHEMA_FILE = "schema.sql"

def establish_bulletproof_connection():
    """Initializes the database safely without wiping existing data records."""
    db_exists = os.path.exists(DB_NAME)
    
    if db_exists:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Owner';")
            has_tables = cursor.fetchone()
            conn.close()
            if has_tables:
                return True
        except Exception:
            pass

    if not os.path.exists(SCHEMA_FILE):
        return False
        
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Patches for T-SQL compatibility
        sql_script = sql_script.replace("(MAX)", "").replace("(max)", "")
        sql_script = sql_script.replace("INT IDENTITY(1,1) PRIMARY KEY", "INTEGER PRIMARY KEY")
        sql_script = sql_script.replace("int identity(1,1) primary key", "integer primary key")
        sql_script = sql_script.replace("INT IDENTITY(1,1)", "INTEGER PRIMARY KEY")
        sql_script = sql_script.replace("identity(1,1)", "INTEGER PRIMARY KEY")
        sql_script = sql_script.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        sql_script = sql_script.replace("create table", "create table if not exists")

        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False
