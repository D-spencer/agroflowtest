# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def build_context(documents):

    """
    Convert retrieved documents into
    a formatted context for the LLM.
    """

    if not documents:

        return ""

    context = []

    for index, doc in enumerate(documents, start=1):

        title = doc.get("title", "Unknown")

        category = doc.get("category", "General")

        section = doc.get("section", "General")

        source = doc.get("source", "Unknown")

        similarity = doc.get("similarity", 0)

        page_start = doc.get("page_start")

        page_end = doc.get("page_end")

        content = doc.get("content", "")

        context.append(

f"""
==================================================

Document {index}

Title:
{title}

Category:
{category}

Section:
{section}

Source:
{source}

Pages:
{page_start}-{page_end}

Similarity:
{similarity:.3f}

Content:
{content}

==================================================
"""

        )

    return "\n".join(context)