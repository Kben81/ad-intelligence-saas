import sqlite3

DB_NAME = "app.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # ANALYSES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        keyword TEXT,
        trend REAL,
        competition INTEGER,
        buzz REAL,
        opportunity REAL,
        level TEXT,
        platform TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    conn.close()
    return user is not None


def save_analysis(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO analyses (
        user, keyword, trend, competition,
        buzz, opportunity, level, platform, date
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["user"],
        data["keyword"],
        data["trend"],
        data["competition"],
        data["buzz"],
        data["opportunity"],
        data["level"],
        data["platform"],
        data["date"]
    ))

    conn.commit()
    conn.close()


def get_history(user, limit=20):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT keyword, trend, competition, buzz,
           opportunity, level, platform, date
    FROM analyses
    WHERE user = ?
    ORDER BY id DESC
    LIMIT ?
    """, (user, limit))

    rows = c.fetchall()
    conn.close()
    return rows