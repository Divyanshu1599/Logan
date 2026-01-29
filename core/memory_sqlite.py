import sqlite3
import os

DB_PATH = "memory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_memory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_memory(key: str, value: str):
    init_memory()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def fetch_memory(key: str):
    init_memory()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
