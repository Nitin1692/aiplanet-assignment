import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ai-workflow-backend")
    APP_ENV: str = os.getenv("APP_ENV", "dev")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/ai_workflow")

    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", ".chroma")

    EMBEDDINGS_PROVIDER: str = os.getenv("EMBEDDINGS_PROVIDER", "openai")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")
    GEMINI_CHAT_MODEL: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-1.5-flash")

    HF_EMBEDDING_MODEL: str = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    SERPAPI_KEY: str | None = os.getenv("SERPAPI_KEY")
    BRAVE_API_KEY: str | None = os.getenv("BRAVE_API_KEY")
    USE_WEB_SEARCH: bool = os.getenv("USE_WEB_SEARCH", "false").lower() == "true"

settings = Settings()