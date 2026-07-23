"""
History-Aware Question Rewriter

Converts follow-up questions into
standalone questions using recent
conversation history and the current topic.
"""

from chatbot.llm import ask_llm


# ============================================================
# SYSTEM PROMPT
# ============================================================

HISTORY_REWRITE_SYSTEM_PROMPT = """
You are an expert agricultural AI assistant.

Your task is to rewrite the user's latest question
into a complete standalone agricultural question.

You are given:

1. The current agricultural topic.
2. The recent conversation history.
3. The user's latest question.

Use BOTH the current topic and the conversation history
to resolve ambiguous references such as:

- it
- they
- them
- this
- that
- these
- those
- the crop
- the plant
- the disease
- the animal

Rules:

1. Preserve the original meaning.

2. Prefer the current topic whenever it clearly resolves
   the user's question.

3. Use conversation history when the topic alone
   is insufficient.

4. If the latest question is already complete,
   return it unchanged.

5. Return ONLY the rewritten standalone question.

Do not answer the question.

Do not explain your reasoning.
"""


# ============================================================
# BUILD HISTORY
# ============================================================

def build_history(history):

    lines = []

    for message in history:

        role = message["role"].capitalize()

        content = message["content"]

        lines.append(

            f"{role}: {content}"

        )

    return "\n".join(lines)


# ============================================================
# REWRITE QUESTION
# ============================================================

def rewrite_with_history(

    llm,

    history,

    current_topic,

    question

):

    # --------------------------------------------------------
    # No history and no topic
    # --------------------------------------------------------

    if not history and not current_topic:

        return question

    history_text = build_history(history)

    if not current_topic:

        current_topic = "UNKNOWN"

    messages = [

        {

            "role": "system",

            "content": HISTORY_REWRITE_SYSTEM_PROMPT

        },

        {

            "role": "user",

            "content":

f"""
Current Topic:

{current_topic}

Conversation History:

{history_text}

Current Question:

{question}

Rewrite the current question into a standalone agricultural question.

Return ONLY the rewritten question.
"""

        }

    ]

    rewritten = ask_llm(

        client=llm,

        messages=messages,

        temperature=0,

        max_tokens=100

    )

    rewritten = rewritten.strip()

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not rewritten:

        rewritten = question

    # --------------------------------------------------------
    # Debug
    # --------------------------------------------------------

    print("\nHistory Rewriter")

    print("-" * 60)

    print(f"Current Topic : {current_topic}")

    print(f"Original      : {question}")

    print(f"Standalone    : {rewritten}")

    print("-" * 60)

    return rewritten