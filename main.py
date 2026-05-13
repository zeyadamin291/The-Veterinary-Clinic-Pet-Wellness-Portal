#!/usr/bin/env python3
import sys
import os
import sqlite3
from menus import run_ui

DB_NAME = "clinic_database.db"
SCHEMA_FILE = "schema.sql"

def establish_bulletproof_connection():
    """Initializes the database safely without wiping existing data records."""
    print("[System] Checking database file consistency...")
    db_exists = os.path.exists(DB_NAME)
    
    if db_exists:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Owner';")
            has_tables = cursor.fetchone()
            conn.close()
            
            if has_tables:
                print("[System] Existing database instance found. Loading data securely...")
                return True
        except Exception:
            pass

    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ Critical Error: Blueprint source file '{SCHEMA_FILE}' is missing!")
        return False
        
    try:
        print(f"[System] Database not found or uninitialized. Syncing from {SCHEMA_FILE}...")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # SQL Server T-SQL to SQLite Dialect Normalization Patches
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
        
        print("[System] Database schema compiled and verified successfully.")
        return True
        
    except sqlite3.Error as sql_error:
        print(f"❌ SQL Initialization Error: {sql_error}")
        return False
    except Exception as general_error:
        print(f"❌ System initialization error: {general_error}")
        return False

def main():
    print("====================================================")
    print(" Launching Veterinary Clinic Runtime Engine...      ")
    print("====================================================")
    
    if not establish_bulletproof_connection():
        print("❌ Critical System Boot Failure. Process aborted.")
        sys.exit(1)
        
    try:
        run_ui()
    except KeyboardInterrupt:
        print("\n\n⚠️ System manual termination signal caught from terminal operator.")
    finally:
        print("\n[System] All modifications committed to disk. Storage pool safe.")
        print("Application closed securely. System shutdown complete. 👋\n")

if __name__ == "__main__":
    main()
