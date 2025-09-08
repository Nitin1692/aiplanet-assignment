from typing import List
import numpy as np
from app.config import settings

# Providers
from openai import OpenAI
import google.generativeai as genai

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

_openai_client = None
_hf_model = None

if settings.OPENAI_API_KEY:
    _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

if settings.EMBEDDINGS_PROVIDER == "hf" and SentenceTransformer:
    _hf_model = SentenceTransformer(settings.HF_EMBEDDING_MODEL)


def embed_texts(texts: List[str]) -> List[List[float]]:
    provider = settings.EMBEDDINGS_PROVIDER
    if provider == "openai":
        assert _openai_client, "OpenAI API key missing"
        resp = _openai_client.embeddings.create(model=settings.OPENAI_EMBEDDING_MODEL, input=texts)
        return [d.embedding for d in resp.data]
    elif provider == "gemini":
        assert settings.GEMINI_API_KEY, "Gemini API key missing"
        model = genai.get_model(settings.GEMINI_EMBEDDING_MODEL)
        # google-generativeai uses embed_content
        out = genai.embed_content(model=settings.GEMINI_EMBEDDING_MODEL, content=texts)
        # The API returns {'embedding': [...]} when single, or batch under 'embedding'
        emb = out.get("embedding")
        if isinstance(emb, list) and isinstance(emb[0], float):
            return [emb]
        # Fallback: if batch, ensure list of vectors
        return emb  # type: ignore
    else:  # hf
        assert _hf_model, "HuggingFace model not available"
        vectors = _hf_model.encode(texts, normalize_embeddings=True)
        if isinstance(vectors, np.ndarray):
            return vectors.tolist()
        return vectors