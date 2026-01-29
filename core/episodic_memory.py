import sqlite3
from datetime import datetime, timedelta

DB_PATH = "memory.db"
TABLE_NAME = "episodic_memory"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_episodic_memory():
    conn = get_connection()
    cursor  = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            details TEXT,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def log_event(event_type, details):
    """
    Log a single episodic event.
    details MUST be text.
    """
    init_episodic_memory()

    details_text = str(details)

    conn = get_connection()
    cursor = conn.cursor()

    # NO f-strings with values below
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} (event_type, details, timestamp) VALUES (?, ?, ?)",
        (event_type, details_text, datetime.now().isoformat()),
    )

    conn.commit()
    conn.close()


def get_recent_events(limit=5):
    init_episodic_memory()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT event_type, details, timestamp
        FROM {TABLE_NAME}
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_events_since(hours: int):
    """
    Return episodic events from the last N hours.
    """
    init_episodic_memory()

    since_time = (datetime.now() - timedelta(hours=hours)).isoformat() 

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT event_type, details, timestamp
        FROM episodic_memory
        WHERE timestamp >= ?
        ORDER BY id DESC
        """,
        (since_time,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_events_today():
    """
    Return episodic events from today.
    """
    init_episodic_memory()

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT event_type, details, timestamp
        FROM episodic_memory
        WHERE timestamp >= ?
        ORDER BY id DESC
        """,
        (today_start,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
