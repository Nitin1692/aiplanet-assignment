from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models import create_document, get_connection

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), collection: str = Form(...)):
    content = await file.read()
    text_chars = len(content.decode("utf-8", errors="ignore"))

    doc_id = create_document(file.filename, collection, text_chars)
    return {"id": doc_id, "filename": file.filename, "chars": text_chars}


@router.get("/")
def list_documents():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, filename, collection, text_chars, created_at FROM documents;")
        rows = cur.fetchall()
        docs = [
            {"id": r[0], "filename": r[1], "collection": r[2], "text_chars": r[3], "created_at": r[4]}
            for r in rows
        ]
        return {"documents": docs}
    finally:
        cur.close()
        conn.close()


@router.delete("/{doc_id}")
def delete_document(doc_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM documents WHERE id = %s RETURNING id;", (doc_id,))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Document deleted successfully"}
    finally:
        cur.close()
        conn.close()
