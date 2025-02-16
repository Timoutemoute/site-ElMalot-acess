import sqlite3

def init_db():
    conn = sqlite3.connect('immobilier.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    # Ajouter un utilisateur admin par défaut
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ('admin', 'admin123', 'admin'))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()