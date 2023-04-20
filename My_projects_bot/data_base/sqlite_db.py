import sqlite3
import sqlite3 as sq


def sql_Start():
    global base, cur
    base = sq.connect("history.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute(
        "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, query TEXT"
        ", created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    base.commit()


def add_history_record(user_id: int, query: str):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, query) VALUES (?, ?)", (user_id, query))
    conn.commit()
    conn.close()
