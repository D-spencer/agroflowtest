from chatbot.config import TOP_CONTEXT_CHUNKS


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_documents(documents):

    """
    Removes duplicate documents based on
    identical content.
    """

    unique = []
    seen = set()

    for doc in documents:

        content = doc.get("content", "").strip().lower()

        if content in seen:
            continue

        seen.add(content)

        unique.append(doc)

    return unique


# ============================================================
# SORT DOCUMENTS
# ============================================================

def sort_documents(documents):

    """
    Sort documents by RRF score.
    """

    return sorted(

        documents,

        key=lambda doc: doc.get("rrf_score", 0),

        reverse=True

    )


# ============================================================
# COMPRESS CONTEXT
# ============================================================

def compress_context(documents):

    """
    Compress retrieved documents before
    sending them to the LLM.
    """

    if not documents:

        return []

    documents = remove_duplicate_documents(

        documents

    )

    documents = sort_documents(

        documents

    )

    documents = documents[:TOP_CONTEXT_CHUNKS]

    print("\nContext Compression")

    print("-" * 60)

    print(

        f"Selected {len(documents)} "

        f"document(s) "

        f"for the LLM."

    )

    print("-" * 60)

    return documents