from chatbot.config import RRF_SCORE_THRESHOLD

from chatbot.retrieval import retrieve_context

from chatbot.context_builder import build_context

from chatbot.context_compressor import compress_context

from chatbot.history_rewriter import rewrite_with_history

from chatbot.topic_extractor import extract_topic

from chatbot.topic_memory import (
    set_topic,
    get_topic
)

from chatbot.prompts import (
    build_rag_prompt,
    build_general_prompt
)

from chatbot.citations import build_citations

from chatbot.llm import ask_llm

from chatbot.memory import add_conversation

from chatbot.messages import build_messages

from chatbot.conversation_context import (
    add_user_message,
    add_assistant_message,
    get_history
)


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
    # Get Previous Conversation History
    # --------------------------------------------------------

    history = get_history()

    # --------------------------------------------------------
    # Extract Current Topic
    # --------------------------------------------------------

    topic = extract_topic(

        llm,

        question

    )

    if topic.upper() != "UNKNOWN":

        set_topic(topic)

    print(f"\nCurrent Topic: {get_topic()}")

    # --------------------------------------------------------
    # Rewrite Question Using Conversation History
    # --------------------------------------------------------

    standalone_question = rewrite_with_history(

        llm=llm,

        history=history,

        current_topic=get_topic(),

        question=question

    )

    # --------------------------------------------------------
    # Save Current User Message
    # --------------------------------------------------------

    add_user_message(question)

    # --------------------------------------------------------
    # Retrieve Documents
    # --------------------------------------------------------

    documents, best_rrf_score = retrieve_context(

        question=standalone_question,

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

        len(documents) > 0

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

        # Use the original user question for response generation
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
    # Save Assistant Message
    # --------------------------------------------------------

    add_assistant_message(

        answer

    )

    # --------------------------------------------------------
    # Debug Conversation History
    # --------------------------------------------------------

    print("\nConversation History")

    print("-" * 60)

    for message in get_history():

        print(

            f"{message['role'].upper()}: "

            f"{message['content'][:120]}"

        )

    print("-" * 60)

    # --------------------------------------------------------
    # Return Final Answer
    # --------------------------------------------------------

    return answer