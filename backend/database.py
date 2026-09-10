import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "agriot.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def fetch_all(sql, params=()):
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

def fetch_one(sql, params=()):
    with get_connection() as conn:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None

def execute(sql, params=()):
    with get_connection() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid

def update(sql, params=()):
    with get_connection() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.rowcount
