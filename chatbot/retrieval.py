from chatbot.config import TOP_K

from chatbot.query_rewriter import rewrite_query
from chatbot.multi_query import generate_multi_queries

from chatbot.embeddings import create_query_embedding

from chatbot.database import (
    retrieve_documents,
    keyword_search
)

from chatbot.rrf import reciprocal_rank_fusion

from chatbot.reranker import rerank_documents

from chatbot.context_compressor import compress_context


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_context(

    question,

    embedding_model,

    supabase,

    llm,

    match_count=TOP_K

):

    # --------------------------------------------------------
    # Rewrite Query
    # --------------------------------------------------------

    try:

        search_query = rewrite_query(

            llm,

            question

        )

        if not search_query.strip():

            search_query = question

    except Exception:

        print("\nQuery rewriting failed.")
        print("Using original question.")

        search_query = question

    # --------------------------------------------------------
    # Generate Multiple Queries
    # --------------------------------------------------------

    try:

        search_queries = generate_multi_queries(

            llm,

            search_query

        )

        if not search_queries:

            search_queries = [search_query]

    except Exception:

        print("\nMulti-query generation failed.")
        print("Using rewritten query only.")

        search_queries = [search_query]

    # --------------------------------------------------------
    # Vector Search
    # Keep each ranked list for RRF
    # --------------------------------------------------------

    vector_rank_lists = []

    for query in search_queries:

        print(f"\nSearching vector index for: {query}")

        embedding = create_query_embedding(

            embedding_model,

            query

        )

        docs, _ = retrieve_documents(

            supabase=supabase,

            embedding=embedding,

            match_count=match_count

        )

        if docs:

            vector_rank_lists.append(docs)

    # --------------------------------------------------------
    # Keyword Search
    # --------------------------------------------------------

    keyword_docs = keyword_search(

        supabase=supabase,

        question=search_query,

        match_count=match_count

    )

    # --------------------------------------------------------
    # Reciprocal Rank Fusion
    # --------------------------------------------------------

    rank_lists = vector_rank_lists.copy()

    if keyword_docs:

        rank_lists.append(

            keyword_docs

        )

    documents = reciprocal_rank_fusion(

        rank_lists

    )

    # --------------------------------------------------------
    # Cross-Encoder Reranking
    # --------------------------------------------------------

    documents = rerank_documents(

        question,

        documents

    )

    # --------------------------------------------------------
    # Context Compression
    # --------------------------------------------------------

    documents = compress_context(

        documents

    )

    # --------------------------------------------------------
    # Final Score
    # --------------------------------------------------------

    if documents:

        best_score = documents[0]["rerank_score"]

    else:

        best_score = 0

    # --------------------------------------------------------
    # Debug Output
    # --------------------------------------------------------

    print("\nFinal Retrieved Documents")

    print("-" * 90)

    for index, doc in enumerate(

        documents,

        start=1

    ):

        print(

            f"{index}. "

            f"{doc.get('source', 'Unknown')} | "

            f"RRF={doc.get('rrf_score', 0):.6f} | "

            f"Rerank={doc.get('rerank_score', 0):.3f}"

        )

    print("-" * 90)

    print(

        f"Best Rerank Score: "

        f"{best_score:.3f}"

    )

    return documents, best_score