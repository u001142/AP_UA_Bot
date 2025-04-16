import sqlite3
from datetime import datetime

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    car TEXT,
    lang TEXT,
    premium INTEGER DEFAULT 0,
    ask_count INTEGER DEFAULT 0,
    last_ask TEXT
)
""")
conn.commit()

def set_user_language(user_id: int, lang: str):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()

def get_user_language(user_id: int):
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def set_user_car(user_id: int, car: str):
    cursor.execute("UPDATE users SET car = ? WHERE user_id = ?", (car, user_id))
    conn.commit()

def get_user_car(user_id: int):
    cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def set_premium(user_id: int):
    cursor.execute("UPDATE users SET premium = 1 WHERE user_id = ?", (user_id,))
    conn.commit()

def is_premium(user_id: int) -> bool:
    cursor.execute("SELECT premium FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1

def increment_and_get_ask_count(user_id: int) -> int:
    today = datetime.utcnow().strftime('%Y-%m-%d')
    cursor.execute("SELECT last_ask FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    last = row[0] if row else None
    if last != today:
        cursor.execute("UPDATE users SET ask_count = 1, last_ask = ? WHERE user_id = ?", (today, user_id))
    else:
        cursor.execute("UPDATE users SET ask_count = ask_count + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT ask_count FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()[0]
