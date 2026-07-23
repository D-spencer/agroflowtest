import traceback

from chatbot.database import get_supabase

from chatbot.embeddings import load_embedding_model

from chatbot.llm import get_llm

from chatbot.chat_engine import chat


# ============================================================
# START CLI
# ============================================================

def run_cli():

    print("\n" + "=" * 70)
    print("AgroFlow AI is ready.")
    print("Type 'exit' to quit.")
    print("=" * 70)

    # --------------------------------------------------------
    # Initialize Components
    # --------------------------------------------------------

    supabase = get_supabase()

    print("✓ Supabase Connected")

    embedding_model = load_embedding_model()

    llm = get_llm()

    # --------------------------------------------------------
    # Chat Loop
    # --------------------------------------------------------

    while True:

        try:

            question = input("\nYou: ").strip()

            if not question:
                continue

            if question.lower() in {

                "exit",

                "quit",

                "bye"

            }:

                print("\nGoodbye!")

                break

            answer = chat(

                question=question,

                supabase=supabase,

                embedding_model=embedding_model,

                llm=llm

            )

            print("\n" + "=" * 70)
            print("AgroFlow AI")
            print("=" * 70)
            print(answer)
            print("=" * 70)

        except KeyboardInterrupt:

            print("\n\nSession terminated.")

            break

        except Exception:

            print("\nAn unexpected error occurred:\n")

            traceback.print_exc()