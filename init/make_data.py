import sqlite3
import sqlite_vss
import numpy as np
import openai
import os
import json
from datetime import datetime
from typing import List

db_path = '/data/qa_pairs.db'

db = sqlite3.connect(db_path, timeout=10)
db.enable_load_extension(True)
sqlite_vss.load(db)
vss_version = db.execute('select vss_version()').fetchone()[0]
print('SQLite VSS Version: %s' % vss_version)

openai.api_key = os.getenv('OPENAI_API_KEY')


def serialize(vector: List[float]) -> bytes:
    """ serializes a list of floats into a compact "raw bytes" format """
    return np.asarray(vector).astype(np.float32).tobytes()


def generate_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=[text]
    )
    return response['data'][0]['embedding']


def insert_qa(question, answer, reference):
    current_time = datetime.now()
    question_embedding = generate_embedding(question)

    with db:
        db.execute('''
      INSERT INTO qa_pairs(question, answer, reference, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?)
    ''', (question, answer, reference, current_time, current_time))

        last_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

        db.execute('''
      INSERT INTO vss_qa_pairs(rowid, question_embedding)
      VALUES (?, ?)
    ''', (last_id, serialize(question_embedding)))


with open('qa_list.json') as f:
    qa_list = json.load(f)

for qa in qa_list:
    phrase_id = insert_qa(qa['question'], qa['answer'], qa['reference'])
