import sqlite3
from datetime import datetime

DB = "app.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free',
        created_at TEXT
    )
    """)

    # ANALYSES
    c.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        keyword TEXT,
        trend REAL,
        competition INTEGER,
        opportunity REAL,
        platform TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------
# USER SYSTEM
# -----------------------
def create_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO users (username, password, plan, created_at)
        VALUES (?, ?, 'free', ?)
        """, (username, password, str(datetime.now())))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    SELECT username, plan FROM users
    WHERE username=? AND password=?
    """, (username, password))

    user = c.fetchone()
    conn.close()

    return user


def get_plan(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT plan FROM users WHERE username=?", (username,))
    result = c.fetchone()

    conn.close()
    return result[0] if result else "free"


# -----------------------
# ANALYTICS
# -----------------------
def save_analysis(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO analyses (
        username, keyword, trend, competition,
        opportunity, platform, date
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["username"],
        data["keyword"],
        data["trend"],
        data["competition"],
        data["opportunity"],
        data["platform"],
        data["date"]
    ))

    conn.commit()
    conn.close()


def get_user_analyses(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    SELECT keyword, trend, competition, opportunity, platform, date
    FROM analyses
    WHERE username=?
    ORDER BY id DESC
    LIMIT 20
    """, (username,))

    rows = c.fetchall()
    conn.close()

    return rows