"""
Cross-Encoder Reranker

Uses a CrossEncoder model to rerank the retrieved
documents according to their relevance to the user's
question.
"""

from sentence_transformers import CrossEncoder

from chatbot.config import RERANKER_MODEL


# ============================================================
# LOAD RERANKER
# ============================================================

print("\nLoading Cross-Encoder Reranker...")

reranker = CrossEncoder(

    RERANKER_MODEL

)

print("✓ Cross-Encoder loaded")


# ============================================================
# RERANK DOCUMENTS
# ============================================================

def rerank_documents(

    question,

    documents

):

    """
    Rerank retrieved documents using a CrossEncoder.

    Parameters
    ----------
    question : str
        User question.

    documents : list
        Retrieved documents.

    Returns
    -------
    list
        Documents sorted by reranker relevance score.
    """

    if not documents:

        return []

    # --------------------------------------------------------
    # Build Question-Document Pairs
    # --------------------------------------------------------

    pairs = [

        (

            question,

            doc.get("content", "")

        )

        for doc in documents

    ]

    # --------------------------------------------------------
    # Predict Relevance Scores
    # --------------------------------------------------------

    scores = reranker.predict(

        pairs

    )

    # --------------------------------------------------------
    # Attach Scores
    # --------------------------------------------------------

    for doc, score in zip(

        documents,

        scores

    ):

        doc["rerank_score"] = float(score)

    # --------------------------------------------------------
    # Sort by Score
    # --------------------------------------------------------

    documents.sort(

        key=lambda x: x["rerank_score"],

        reverse=True

    )

    # --------------------------------------------------------
    # Display Rankings
    # --------------------------------------------------------

    print("\nCross-Encoder Ranking")

    print("-" * 70)

    for index, doc in enumerate(

        documents,

        start=1

    ):

        print(

            f"{index}. "

            f"{doc.get('source', 'Unknown')} | "

            f"Rerank={doc['rerank_score']:.3f}"

        )

    print("-" * 70)

    print(

        f"Best Rerank Score: "

        f"{documents[0]['rerank_score']:.3f}"

    )

    return documents