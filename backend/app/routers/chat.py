from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_connection

router = APIRouter()

class ChatMessageCreate(BaseModel):
    session_id: int
    role: str
    content: str


@router.post("/session/{workflow_id}")
def create_session(workflow_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO chat_sessions (workflow_id) VALUES (%s) RETURNING id;",
            (workflow_id,)
        )
        session_id = cur.fetchone()
        conn.commit()
        return {"session_id": session_id.get("id")}
    finally:
        cur.close()
        conn.close()


@router.delete("/session/{session_id}")
def delete_session(session_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM chat_sessions WHERE id = %s RETURNING id;", (session_id,))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    finally:
        cur.close()
        conn.close()


@router.post("/message")
def add_message(msg: ChatMessageCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO chat_messages (session_id, role, content)
               VALUES (%s, %s, %s) RETURNING id;""",
            (msg.session_id, msg.role, msg.content)
        )
        message_id = cur.fetchone()
        conn.commit()
        return {"id": message_id, "message": "Message added successfully"}
    finally:
        cur.close()
        conn.close()


@router.get("/session/{session_id}/messages")
def list_messages(session_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, role, content, created_at
               FROM chat_messages
               WHERE session_id = %s ORDER BY created_at ASC;""",
            (session_id,)
        )
        rows = cur.fetchall()
        messages = [
            {"id": r[0], "role": r[1], "content": r[2], "created_at": r[3]}
            for r in rows
        ]
        return {"messages": messages}
    finally:
        cur.close()
        conn.close()


@router.delete("/message/{message_id}")
def delete_message(message_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM chat_messages WHERE id = %s RETURNING id;", (message_id,))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Message not found")
        return {"message": "Message deleted successfully"}
    finally:
        cur.close()
        conn.close()
