import json
import sqlite3
import sqlite_vss
import numpy as np
import openai
import boto3
from typing import List

db_path = './qa_pairs.db'


def lambda_handler(event, context):
    # Connect DB
    db = sqlite3.connect(db_path, timeout=10)
    db.enable_load_extension(True)
    sqlite_vss.load(db)
    vss_version = db.execute('select vss_version()').fetchone()[0]
    print('SQLite VSS Version: %s' % vss_version)

    # Get OpenAI API
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(
        Name='YOUR_SSM_OPENAI_API_KEY_NAME', WithDecryption=True)
    secret_value = parameter['Parameter']['Value']
    openai.api_key = secret_value

    parameters = event.get('queryStringParameters', {})
    search_query = parameters.get('search_query')
    if search_query:
        query_embedding = generate_embedding(search_query)
        results = search_similar_embeddings(db, query_embedding)
        answers = [row[2] for row in results]
        return {
            'statusCode': 200,
            'body': json.dumps(answers, ensure_ascii=False)
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Missing search_query parameter'
        }


def search_similar_embeddings(db, query_embedding, k=3):
    results = db.execute('''
    SELECT qa_pairs.*, vss_qa_pairs.distance
    FROM vss_qa_pairs
    JOIN qa_pairs ON vss_qa_pairs.rowid = qa_pairs.id
    WHERE vss_search(vss_qa_pairs.question_embedding, vss_search_params(?, 10))
    ORDER BY vss_qa_pairs.distance
    LIMIT ?
  ''', (serialize(query_embedding), k))
    return results.fetchall()


def serialize(vector: List[float]) -> bytes:
    """ serializes a list of floats into a compact "raw bytes" format """
    return np.asarray(vector).astype(np.float32).tobytes()


def generate_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=[text]
    )
    return response['data'][0]['embedding']
