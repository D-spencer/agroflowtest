from dotenv import load_dotenv
from supabase import create_client

import os

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================

from chatbot.config import (
    TOP_K
)

# ============================================================
# SUPABASE
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL missing")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY missing")


def get_supabase():

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(

    supabase,

    embedding,

    match_count=TOP_K

):

    print("\nSearching knowledge base...")

    result = supabase.rpc(

        "match_documents",

        {

            "query_embedding": embedding,

            "match_count": match_count

        }

    ).execute()

    documents = result.data

    if not documents:

        print("No matching documents found.")

        return [], 0

    print("\nRetrieved Documents")

    print("-" * 60)

    for index, doc in enumerate(documents, start=1):

        print(

            f"{index}. "

            f"{doc['source']} "

            f"(Similarity: {doc['similarity']:.3f})"

        )

    print("-" * 60)

    best_similarity = documents[0]["similarity"]

    print(f"Best Similarity: {best_similarity:.3f}")

    return documents, best_similarity


# ============================================================
# KEYWORD SEARCH
# ============================================================

def keyword_search(

    supabase,

    question,

    match_count=5

):

    print("\nSearching keyword index...")

    result = supabase.rpc(

        "keyword_search",

        {

            "search_query": question,

            "match_count": match_count

        }

    ).execute()

    documents = result.data or []

    print(

        f"Keyword search found {len(documents)} document(s)."

    )

    return documents