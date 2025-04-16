
import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, car TEXT)")
conn.commit()

def set_user_car(user_id: int, car: str):
    cursor.execute("REPLACE INTO users (user_id, car) VALUES (?, ?)", (user_id, car))
    conn.commit()

def get_user_car(user_id: int):
    cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None
