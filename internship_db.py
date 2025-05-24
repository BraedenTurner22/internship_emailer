import sqlite3
from typing import Dict

DB_PATH = 'internships.db'

def init_db(path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute('''
      CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        location TEXT,
        application_link TEXT UNIQUE
      )
    ''')
    conn.commit()
    return conn

def internship_exists(conn: sqlite3.Connection, link: str) -> bool:
    cur = conn.execute(
        'SELECT 1 FROM internships WHERE application_link = ?',
        (link,)
    )
    return cur.fetchone() is not None

def insert_internship(conn: sqlite3.Connection, job: Dict[str, str]) -> None:
    conn.execute(
        '''
        INSERT OR IGNORE INTO internships
          (company, role, location, application_link)
        VALUES (?, ?, ?, ?)
        ''',
        (
          job['Company'],
          job['Role'],
          job['Location'],
          job['Application Link']
        )
    )
    conn.commit()