import os

import psycopg
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres import PostgresSaver


def get_checkpointer():
    db_uri = os.getenv("POSTGRES_URL")

    if not db_uri:
        raise ValueError("POSTGRES_URL is not configured")

    conn = psycopg.connect(
        db_uri,
        autocommit=True,
        row_factory=dict_row,
    )

    checkpointer = PostgresSaver(conn)
    checkpointer.setup()

    return checkpointer