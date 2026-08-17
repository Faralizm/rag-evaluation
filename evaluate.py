import os

from anthropic import Anthropic
from dotenv import load_dotenv

from test_dataset import TEST_DATASET

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_actual_answer(question):
    """
    QEYD: Bu, real RAG pipeline-ının yerini tutan sadələşdirilmiş çağırışdır.
    """
    if not question.strip():
        return "Sual boşdur, cavab verilə bilmir."

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def llm_judge_score(question, expected_answer, actual_answer):
    """
    LLM-as-judge: başqa bir Claude çağırışı ilə actual_answer-in
    expected_answer-ə nə dərəcədə uyğun olduğunu 0-5 şkalada qiymətləndirir.
    """
    judge_prompt = f"""You are grading an AI system's answer against an expected answer.
Score from 0 (completely wrong/irrelevant) to 5 (fully correct and appropriate).
Respond with ONLY the number, nothing else.

Question: {question}
Expected answer (or expected behavior): {expected_answer}
Actual answer given: {actual_answer}

Score (0-5):"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    try:
        return int(response.content[0].text.strip())
    except ValueError:
        return 0


def run_evaluation():
    results = []
    for item in TEST_DATASET:
        actual = get_actual_answer(item["question"])
        score = llm_judge_score(item["question"], item["expected_answer"], actual)

        results.append({
            "id": item["id"],
            "category": item["category"],
            "question": item["question"],
            "score": score,
        })
        print(f"#{item['id']} [{item['category']}] Score: {score}/5 - {item['question'][:50]}")

    avg_score = sum(r["score"] for r in results) / len(results)
    normal_avg = sum(r["score"] for r in results if r["category"] == "normal") / sum(1 for r in results if r["category"] == "normal")
    edge_avg = sum(r["score"] for r in results if r["category"] == "edge") / sum(1 for r in results if r["category"] == "edge")

    print(f"\n--- Yekun nəticələr ---")
    print(f"Ümumi orta bal: {avg_score:.2f}/5")
    print(f"Normal suallar üzrə orta: {normal_avg:.2f}/5")
    print(f"Edge case-lər üzrə orta: {edge_avg:.2f}/5")

    return results


if __name__ == "__main__":
    run_evaluation()