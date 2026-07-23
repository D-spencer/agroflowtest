"""
Citation utilities for AgroFlow AI.

Responsible for formatting and displaying
knowledge base sources.
"""


# ============================================================
# FORMAT SINGLE CITATION
# ============================================================

def format_citation(document):

    title = document.get("title", "Unknown Document")

    section = document.get("section", "General")

    source = document.get("source", "Unknown")

    page_start = document.get("page_start")

    page_end = document.get("page_end")

    citation = []

    citation.append(f"📄 {title}")

    citation.append(f"   Source : {source}")

    citation.append(f"   Section: {section}")

    if page_start is not None:

        if page_start == page_end:

            citation.append(
                f"   Page   : {page_start}"
            )

        else:

            citation.append(
                f"   Pages  : {page_start}-{page_end}"
            )

    return "\n".join(citation)


# ============================================================
# REMOVE DUPLICATE SOURCES
# ============================================================

def remove_duplicate_sources(documents):

    unique = []
    seen = set()

    for doc in documents:

        key = (

            doc.get("source"),

            doc.get("page_start"),

            doc.get("page_end")

        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(doc)

    return unique


# ============================================================
# BUILD SOURCES SECTION
# ============================================================

def build_citations(documents):

    if not documents:

        return ""

    documents = remove_duplicate_sources(documents)

    lines = []

    lines.append("")
    lines.append("")
    lines.append("Sources")
    lines.append("-" * 40)

    for index, document in enumerate(documents, start=1):

        lines.append(f"{index}.")

        lines.append(

            format_citation(document)

        )

        lines.append("")

    return "\n".join(lines)