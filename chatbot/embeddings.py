from sentence_transformers import SentenceTransformer

# ============================================================
# CONFIGURATION
# ============================================================

from chatbot.config import EMBEDDING_MODEL


# ============================================================
# LOAD MODEL
# ============================================================

def load_embedding_model():

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print("✓ Embedding model loaded")

    return model


# ============================================================
# CREATE QUESTION EMBEDDING
# ============================================================

def create_query_embedding(

    embedding_model,

    question

):

    print("\nGenerating question embedding...")

    embedding = embedding_model.encode(

        question,

        normalize_embeddings=True,

        convert_to_numpy=True

    )

    return embedding.tolist()


# ============================================================
# CREATE MULTIPLE QUERY EMBEDDINGS
# (For future Multi-Query RAG)
# ============================================================

def create_query_embeddings(

    embedding_model,

    questions

):

    embeddings = embedding_model.encode(

        questions,

        normalize_embeddings=True,

        convert_to_numpy=True

    )

    return embeddings.tolist()