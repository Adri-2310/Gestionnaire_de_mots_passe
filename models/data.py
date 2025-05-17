__author__ = "Adrien Mertens"
__version__ = "1.0"

import sqlite3

def init_db():
    conn = sqlite3.connect(r'..\datas.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        password TEXT NOT NULL)''')
    cursor.close()
    conn.commit()

if __name__ == '__main__':
    init_db()
