from datetime import datetime
from app.db import get_connection

# ---------- TABLE CREATION ----------

def init_tables():
    """Create tables if they don't exist"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS workflows (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            nodes JSON NOT NULL,
            edges JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            workflow_id INTEGER NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL, -- 'user' | 'assistant' | 'system'
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(512) NOT NULL,
            collection VARCHAR(255) NOT NULL, -- chroma collection name
            text_chars INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
    finally:
        cur.close()
        conn.close()


# ---------- WORKFLOWS ----------

def create_workflow(name: str, nodes: dict, edges: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO workflows (name, nodes, edges)
               VALUES (%s, %s, %s) RETURNING id;""",
            (name, nodes, edges)
        )
        workflow_id = cur.fetchone()[0]
        conn.commit()
        return workflow_id
    finally:
        cur.close()
        conn.close()


def get_workflows():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, nodes, edges, created_at FROM workflows ORDER BY id;")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


# ---------- DOCUMENTS ----------

def create_document(filename: str, collection: str, text_chars: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO documents (filename, collection, text_chars)
               VALUES (%s, %s, %s) RETURNING id;""",
            (filename, collection, text_chars)
        )
        doc_id = cur.fetchone()[0]
        conn.commit()
        return doc_id
    finally:
        cur.close()
        conn.close()
