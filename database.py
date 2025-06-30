import sqlite3

def init_db():
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cv_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            age TEXT,
            titre TEXT,
            ville TEXT,
            email TEXT,
            telephone TEXT,
            profil TEXT,
            experiences TEXT,
            competences TEXT,
            langues TEXT,
            formations TEXT,
            interets TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
