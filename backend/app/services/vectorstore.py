import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
from typing import List

_chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

def get_collection(name: str):
    return _chroma_client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def add_texts(collection_name: str, texts: List[str], ids: List[str], metadatas: List[dict] | None = None):
    col = get_collection(collection_name)
    col.add(documents=texts, ids=ids, metadatas=metadatas or [{} for _ in texts])


def similarity_search(collection_name: str, query: str, k: int = 4):
    col = get_collection(collection_name)
    res = col.query(query_texts=[query], n_results=k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return list(zip(docs, metas))