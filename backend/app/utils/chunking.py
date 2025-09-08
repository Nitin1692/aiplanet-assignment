from typing import List

# Simple recursive splitter by sentence length

def split_text(text: str, max_chars: int = 1000, overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break
    return [c.strip() for c in chunks if c.strip()]