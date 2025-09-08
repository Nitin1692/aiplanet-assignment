# app/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/aiworkflow"
)

def get_connection():
    """Return a new database connection."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn





from chromadb import Client
from chromadb.config import Settings

_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        # NEW: Settings object now handles persistence & backend
        _chroma_client = Client(
            settings=Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="./chroma_db",
                anonymized_telemetry=False
            )
        )
    return _chroma_client

def get_chroma_collection(name: str):
    client = get_chroma_client()
    try:
        return client.get_collection(name)
    except Exception:
        # create collection if it doesn't exist
        return client.create_collection(name)



