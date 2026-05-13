import sqlite3

DB_NAME = "clinic_database.db"

def execute_query(query, params=(), fetch=False, return_last_id=False):
    """Unified transaction processing wrapper for database operations."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    results = None
    try:
        cursor.execute(query, params)
        if fetch:
            results = cursor.fetchall()
        conn.commit()
        if return_last_id:
            results = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[SQL Error] {e}")
    finally:
        conn.close()
    return results
