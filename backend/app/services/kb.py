from app.db import get_chroma_collection  # helper to get Chroma collection

def run_kb_search(query: str, collection_name: str = "default") -> str:
    """
    Search the knowledge base for relevant context to include in LLM prompt.

    Returns a concatenated string of top results.
    """
    collection = get_chroma_collection(collection_name)
    if not collection:
        return ""

    # Search top 3 relevant docs
    results = collection.query(
        query_texts=[query],
        n_results=3,
        include=["metadatas", "documents", "distances"]
    )

    # Flatten results into a single context string
    context_snippets = []
    for r in results["documents"][0]:
        context_snippets.append(r)

    return "\n\n".join(context_snippets)
