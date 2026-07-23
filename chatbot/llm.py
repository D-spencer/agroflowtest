import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ============================================================
# GROQ CONFIGURATION
# ============================================================

from chatbot.config import (
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

# ============================================================
# CREATE CLIENT
# ============================================================

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY missing"
        )

    client = Groq(

        api_key=api_key

    )

    print("✓ Groq Connected")

    return client


# ============================================================
# GENERATE RESPONSE
# ============================================================

def ask_llm(

    client,

    messages,

    temperature=TEMPERATURE,

    max_tokens=MAX_TOKENS

):

    print("\nSending request to Groq...")

    response = client.chat.completions.create(

    model=LLM_MODEL,

    temperature=temperature,

    max_tokens=max_tokens,

    messages=messages

    )

    print("✓ Response received")

    return response.choices[0].message.content