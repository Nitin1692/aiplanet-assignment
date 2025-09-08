from typing import Optional, List
from app.config import settings
from openai import OpenAI
import google.generativeai as genai

_openai_client = None
if settings.OPENAI_API_KEY:
    _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


SYSTEM_PROMPT = (
    "You are an AI assistant embedded in a visual workflow tool. "
    "Answer clearly. If context is provided, ground your answer in it and cite brief snippets."
)


def chat_completion(
    query: str,
    context: Optional[str] = None,
    custom_prompt: Optional[str] = None,
    provider: str | None = None,
    history: Optional[List[dict]] = None,
) -> str:
    provider = provider or settings.LLM_PROVIDER
    prompt = custom_prompt or SYSTEM_PROMPT

    if provider == "openai":
        assert _openai_client, "OpenAI API key missing"
        messages = []
        messages.append({"role": "system", "content": prompt})
        if context:
            messages.append({"role": "system", "content": f"Context:\n{context}"})
        for m in (history or []):
            messages.append(m)
        messages.append({"role": "user", "content": query})
        resp = _openai_client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content

    else:  # gemini
        assert settings.GEMINI_API_KEY, "Gemini API key missing"
        model = genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)
        parts = []
        parts.append(prompt)
        if context:
            parts.append(f"Context:\n{context}")
        if history:
            # Flatten simple user/assistant history
            hist_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
            parts.append(hist_text)
        parts.append(f"USER: {query}")
        resp = model.generate_content("\n\n".join(parts))
        return resp.text