import ollama
import pandas as pd
from pathlib import Path
from datetime import datetime

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

PROMPTS_FILE = DATASET_DIR / "prompts.csv"
RESPONSES_FILE = DATASET_DIR / "llm_responses.csv"
COMPARISON_FILE = DATASET_DIR / "response_comparison.csv"
HISTORY_FILE = DATASET_DIR / "conversation_history.txt"

MODEL = "llama3.2"


def generate_response(prompt):
    """Generate a response using the local Ollama model."""
    result = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return result["message"]["content"]


def main():
    prompts_df = pd.read_csv(PROMPTS_FILE)
    responses = []

    print(f"Using local model: {MODEL}")
    print("Generating responses...\n")

    with open(HISTORY_FILE, "w", encoding="utf-8") as history:
        history.write(f"Local LLM Conversation History\nModel: {MODEL}\n")
        history.write(f"Date: {datetime.now()}\n\n")

        for _, row in prompts_df.iterrows():
            prompt = str(row["prompt"])

            print(f"Prompt {row['id']}: {prompt}")

            try:
                answer = generate_response(prompt)
                status = "Success"
            except Exception as error:
                answer = f"ERROR: {error}"
                status = "Failed"

            print(f"Response: {answer}\n")
            print("-" * 60)

            responses.append({
                "id": row["id"],
                "domain": row["domain"],
                "prompt_type": row["prompt_type"],
                "prompt": prompt,
                "response": answer,
                "response_length_words": len(answer.split()),
                "status": status
            })

            history.write(f"Prompt: {prompt}\n")
            history.write(f"Response: {answer}\n")
            history.write("-" * 60 + "\n\n")

    responses_df = pd.DataFrame(responses)
    responses_df.to_csv(RESPONSES_FILE, index=False)

    # Compare simple and detailed prompts within each domain
    comparison = []

    for domain in prompts_df["domain"].unique():
        domain_rows = responses_df[responses_df["domain"] == domain]

        simple = domain_rows[domain_rows["prompt_type"] == "Simple"]
        detailed = domain_rows[domain_rows["prompt_type"] == "Detailed"]

        if not simple.empty and not detailed.empty:
            simple_row = simple.iloc[0]
            detailed_row = detailed.iloc[0]

            comparison.append({
                "domain": domain,
                "simple_prompt": simple_row["prompt"],
                "simple_response_words": simple_row["response_length_words"],
                "detailed_prompt": detailed_row["prompt"],
                "detailed_response_words": detailed_row["response_length_words"],
                "simple_status": simple_row["status"],
                "detailed_status": detailed_row["status"],
                "observation": (
                    "Compare relevance, clarity, factual accuracy, "
                    "and detail after reviewing both responses."
                )
            })

    pd.DataFrame(comparison).to_csv(COMPARISON_FILE, index=False)

    print("\nProject execution completed.")
    print(f"Responses saved to: {RESPONSES_FILE}")
    print(f"Comparison saved to: {COMPARISON_FILE}")
    print(f"Conversation history saved to: {HISTORY_FILE}")


if __name__ == "__main__":
    main()