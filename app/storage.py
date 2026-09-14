import os

import redis
from psycopg import connect

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://scs:scs@localhost:5432/scs")


def redis_client():
    return redis.from_url(REDIS_URL, decode_responses=True)


def init_db() -> None:
    with connect(DATABASE_URL) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id BIGSERIAL PRIMARY KEY,
                device_id TEXT NOT NULL,
                value DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.commit()


def insert_event(device_id: str, value: float) -> None:
    with connect(DATABASE_URL) as conn:
        conn.execute("INSERT INTO events (device_id, value) VALUES (%s, %s)", (device_id, value))
        conn.commit()
