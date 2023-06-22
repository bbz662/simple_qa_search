import sqlite3
import sqlite_vss
import os

db_path = '/data/qa_pairs.db'

if not os.path.isfile(db_path):
    db = sqlite3.connect(db_path, timeout=10)
    db.enable_load_extension(True)
    sqlite_vss.load(db)
    vss_version = db.execute('select vss_version()').fetchone()[0]
    print('SQLite VSS Version:', vss_version)

    db.execute('''
      CREATE TABLE IF NOT EXISTS qa_pairs(
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        reference TEXT,
        created_at DATETIME,
        updated_at DATETIME
      );
    ''')

    db.execute('''
      CREATE VIRTUAL TABLE IF NOT EXISTS vss_qa_pairs USING vss0(
        question_embedding(1536)
      );
    ''')

    db.close()
else:
    print('qa_pairs.db already exists')
