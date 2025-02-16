import sqlite3

def init_db():
    conn = sqlite3.connect('immobilier.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS properties
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect('immobilier.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('immobilier.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

if __name__ == '__main__':
    init_db()