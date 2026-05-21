import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file.")

client = genai.Client(api_key=API_KEY)
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
BASE = Path(__file__).parent


def load_prompt(name: str) -> str:
    return (BASE / "prompts" / name).read_text(encoding="utf-8")


def ask_llm(instructions: str, user_input: str, json_mode: bool = False) -> str:
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        response_mime_type="application/json" if json_mode else "text/plain",
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=user_input,
        config=config,
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")
    return response.text.strip()


def ask_json(prompt_file: str, payload: dict[str, Any]) -> dict[str, Any]:
    user_input = (
        "Return valid JSON only.\n\n"
        f"Input payload:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )
    raw = ask_llm(load_prompt(prompt_file), user_input, json_mode=True)
    return json.loads(raw)


def get_candidate_setup() -> dict[str, str]:
    print("AI Mock Interview Coach\n")
    return {
        "target_role": input("Target role: ").strip(),
        "background": input("2-3 line background/resume snippet (optional): ").strip(),
        "focus_area": input("Focus area (behavioral/technical/case/mixed): ").strip() or "mixed",
    }


def run_interview() -> None:
    profile = get_candidate_setup()
    strategy = ask_json("strategist.md", profile)
    history = []

    print(f"\nInterview plan: {strategy['interview_style']}")
    print("Type 'quit' anytime.\n")

    opening = ask_json(
        "interviewer.md",
        {
            "mode": "open",
            "profile": profile,
            "strategy": strategy,
            "history": history,
        },
    )
    question = opening["question"]

    for turn in range(1, 7):
        print(f"Interviewer: {question}")
        answer = input("You: ").strip()
        if answer.lower() == "quit":
            break

        eval_result = ask_json(
            "evaluator.md",
            {
                "profile": profile,
                "strategy": strategy,
                "history": history,
                "question": question,
                "answer": answer,
                "turn_number": turn,
            },
        )

        history.append(
            {
                "turn": turn,
                "question": question,
                "answer": answer,
                "evaluation": eval_result,
            }
        )

        if turn == 6:
            break

        next_step = ask_json(
            "interviewer.md",
            {
                "mode": "follow_up",
                "profile": profile,
                "strategy": strategy,
                "history": history,
                "latest_evaluation": eval_result,
            },
        )
        question = next_step["question"]

    final_feedback = ask_llm(
        load_prompt("coach.md"),
        json.dumps(
            {
                "profile": profile,
                "strategy": strategy,
                "history": history,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )

    print("\n" + "=" * 70)
    print("FINAL FEEDBACK\n")
    print(final_feedback)


if __name__ == "__main__":
    run_interview()