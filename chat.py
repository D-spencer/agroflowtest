# import os
# import traceback

# from dotenv import load_dotenv
# from groq import Groq
# from supabase import create_client
# from sentence_transformers import SentenceTransformer

# # ============================================================
# # LOAD ENVIRONMENT VARIABLES
# # ============================================================

# load_dotenv()

# # ============================================================
# # CONFIGURATION
# # ============================================================

# TOP_K = 5

# SIMILARITY_THRESHOLD = 0.65

# EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# MAX_HISTORY = 10

# # ============================================================
# # SYSTEM PROMPT
# # ============================================================

# SYSTEM_PROMPT = """
# You are AgroFlow AI.

# You are an expert agricultural assistant specializing in:

# • Crop production
# • Soil science
# • Fertilizer management
# • Irrigation
# • Crop diseases
# • Pest management
# • Livestock
# • Climate-smart agriculture
# • Sustainable farming
# • Agricultural technology

# Your purpose is to answer agriculture-related questions only.

# Rules:

# 1. Always prioritize retrieved knowledge from the AgroFlow Knowledge Base.

# 2. If the retrieved knowledge completely answers the question, answer only from it.

# 3. If the retrieved knowledge partially answers the question, use it first, then supplement it with your agricultural expertise.

# 4. If no useful knowledge is retrieved, answer using your own agricultural expertise only.

# 5. Never invent facts or claim information came from the knowledge base when it did not.

# 6. Clearly distinguish between:
#    - Knowledge Base
#    - General Agricultural Knowledge

# 7. Give practical, accurate, step-by-step recommendations whenever appropriate.

# 8. Use bullet points or tables when they improve readability.

# 9. Keep answers concise but technically accurate.

# 10. If a question is unrelated to agriculture, farming, crops, livestock, soil, weather for farming, agricultural economics, food production, or other agricultural topics, politely explain that AgroFlow AI is designed specifically for agriculture and cannot assist with unrelated subjects.

# For example:
# "I'm designed specifically to assist with agriculture and farming. I can't answer questions about sports, politics, entertainment, finance, or other unrelated topics. Please ask me an agriculture-related question."
# """
# # ============================================================
# # SUPABASE
# # ============================================================

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# if not SUPABASE_URL:
#     raise ValueError("SUPABASE_URL missing")

# if not SUPABASE_KEY:
#     raise ValueError("SUPABASE_SERVICE_ROLE_KEY missing")

# supabase = create_client(
#     SUPABASE_URL,
#     SUPABASE_KEY
# )

# print("✓ Supabase Connected")

# # ============================================================
# # GROQ
# # ============================================================

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise ValueError("GROQ_API_KEY missing")

# groq = Groq(api_key=api_key)

# print("✓ Groq Connected")

# # ============================================================
# # EMBEDDING MODEL
# # ============================================================

# print("\nLoading embedding model...")

# embedding_model = SentenceTransformer(
#     EMBEDDING_MODEL
# )

# print("✓ Embedding model loaded")

# # ============================================================
# # CONVERSATION MEMORY
# # ============================================================

# conversation_history = []

# # ============================================================
# # HELPER FUNCTIONS
# # ============================================================
# def build_context(documents):

#     context = []

#     for index, doc in enumerate(documents, start=1):

#         context.append(

# f"""
# Document {index}

# Source:
# {doc["source"]}

# Similarity:
# {doc["similarity"]:.3f}

# Content:
# {doc["content"]}

# ----------------------------------------
# """
#         )

#     return "\n".join(context)

# def retrieve_documents(question):

#     print("\nGenerating question embedding...")

#     embedding = embedding_model.encode(
#         question,
#         normalize_embeddings=True,
#         convert_to_numpy=True
#     ).tolist()

#     print("Searching knowledge base...")

#     result = supabase.rpc(

#         "match_documents",

#         {
#             "query_embedding": embedding,
#             "match_count": TOP_K
#         }

#     ).execute()

#     documents = result.data

#     if not documents:
#         return [], 0

#     print("\nRetrieved Documents")

#     print("-" * 50)

#     for i, doc in enumerate(documents, start=1):

#         print(
#             f"{i}. {doc['source']}  "
#             f"(Similarity: {doc['similarity']:.3f})"
#         )

#     print("-" * 50)

#     best_similarity = documents[0]["similarity"]

#     print(f"Best Similarity: {best_similarity:.3f}")

#     return documents, best_similarity


# def ask_groq(messages):

#     print("\nSending request to Groq...")

#     response = groq.chat.completions.create(

#         model="llama-3.3-70b-versatile",

#         temperature=0.3,

#         max_tokens=1024,

#         messages=messages

#     )

#     print("✓ Response received")

#     return response.choices[0].message.content

# # ============================================================
# # CHAT LOOP
# # ============================================================

# print("\n")
# print("=" * 70)
# print("AgroFlow AI is ready.")
# print("Type 'exit' to quit.")
# print("=" * 70)

# while True:

#     try:

#         question = input("\nYou: ").strip()

#         if not question:
#             continue

#         if question.lower() == "exit":
#             print("\nGoodbye!")
#             break

#         # ----------------------------------------------------
#         # Retrieve relevant documents
#         # ----------------------------------------------------

#         documents, best_similarity = retrieve_documents(question)

#         # ----------------------------------------------------
#         # Build user prompt
#         # ----------------------------------------------------

#         if documents and best_similarity >= SIMILARITY_THRESHOLD:

#             print("\nUsing Knowledge Base...")

#             context = build_context(documents)

#             user_prompt = f"""
# The following information was retrieved from the AgroFlow Knowledge Base.

# Answer the user's question using the retrieved information as your primary source.

# If the retrieved information fully answers the question,
# do not add unnecessary external information.

# If it only partially answers,
# complete the answer using your agricultural knowledge.

# Knowledge Base

# {context}

# User Question

# {question}
# """

#         else:

#             print("\nKnowledge base not relevant enough.")
#             print("Using general agricultural knowledge...")

#             user_prompt = question

#         # ----------------------------------------------------
#         # Build conversation messages
#         # ----------------------------------------------------

#         messages = [

#             {
#                 "role": "system",
#                 "content": SYSTEM_PROMPT
#             }

#         ]

#         # Keep only recent conversation

#         messages.extend(conversation_history[-MAX_HISTORY:])

#         messages.append(

#             {
#                 "role": "user",
#                 "content": user_prompt
#             }

#         )

#         # ----------------------------------------------------
#         # Ask Groq
#         # ----------------------------------------------------

#         answer = ask_groq(messages)

#         # ----------------------------------------------------
#         # Save conversation memory
#         # ----------------------------------------------------

#         conversation_history.append(

#             {
#                 "role": "user",
#                 "content": question
#             }

#         )

#         conversation_history.append(

#             {
#                 "role": "assistant",
#                 "content": answer
#             }

#         )

#         # Prevent memory from growing forever

#         if len(conversation_history) > MAX_HISTORY * 2:

#             conversation_history = conversation_history[-MAX_HISTORY * 2:]

#         # ----------------------------------------------------
#         # Print answer
#         # ----------------------------------------------------

#         print("\n" + "=" * 70)
#         print("AgroFlow AI")
#         print("=" * 70)
#         print(answer)
#         print("=" * 70)

#     except KeyboardInterrupt:

#         print("\n\nSession terminated.")
#         break

#     except Exception:

#         print("\nAn unexpected error occurred:\n")
#         traceback.print_exc()




from chatbot.cli import run_cli


if __name__ == "__main__":
    run_cli()