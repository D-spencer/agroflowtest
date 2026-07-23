from chatbot.config import RRF_SCORE_THRESHOLD

from chatbot.retrieval import retrieve_context

from chatbot.context_builder import build_context

from chatbot.context_compressor import compress_context

from chatbot.prompts import (
    build_rag_prompt,
    build_general_prompt
)

from chatbot.citations import build_citations

from chatbot.llm import ask_llm

from chatbot.memory import add_conversation

from chatbot.messages import build_messages


# ============================================================
# ASK CHATBOT
# ============================================================

def chat(

    question,

    supabase,

    embedding_model,

    llm

):

    # --------------------------------------------------------
    # Retrieve Documents
    # --------------------------------------------------------

    documents, best_rrf_score = retrieve_context(

        question=question,

        embedding_model=embedding_model,

        supabase=supabase,

        llm=llm

    )

    # --------------------------------------------------------
    # Compress Retrieved Context
    # --------------------------------------------------------

    documents = compress_context(

        documents

    )

    # --------------------------------------------------------
    # Decide Whether to Use Knowledge Base
    # --------------------------------------------------------

    using_knowledge_base = (

        documents

        and

        best_rrf_score >= RRF_SCORE_THRESHOLD

    )

    # --------------------------------------------------------
    # Build Prompt
    # --------------------------------------------------------

    if using_knowledge_base:

        print("\nUsing RRF Search Results...")

        print(

            f"RRF Score: "

            f"{best_rrf_score:.6f}"

        )

        context = build_context(

            documents

        )

        user_prompt = build_rag_prompt(

            context,

            question

        )

    else:

        print(

            f"\nRRF score "

            f"{best_rrf_score:.6f} "

            f"is below threshold "

            f"({RRF_SCORE_THRESHOLD})"

        )

        print(

            "Using general agricultural knowledge..."

        )

        user_prompt = build_general_prompt(

            question

        )

    # --------------------------------------------------------
    # Build Conversation Messages
    # --------------------------------------------------------

    messages = build_messages(

        user_prompt

    )

    # --------------------------------------------------------
    # Ask LLM
    # --------------------------------------------------------

    answer = ask_llm(

        client=llm,

        messages=messages

    )

    # --------------------------------------------------------
    # Append Citations
    # --------------------------------------------------------

    if using_knowledge_base:

        citations = build_citations(

            documents

        )

        if citations:

            answer += f"\n\n{citations}"

    # --------------------------------------------------------
    # Save Conversation
    # --------------------------------------------------------

    add_conversation(

        question,

        answer

    )

    # --------------------------------------------------------
    # Return Final Answer
    # --------------------------------------------------------

    return answer