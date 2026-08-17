import os
import time

from anthropic import Anthropic
from dotenv import load_dotenv

from test_dataset import TEST_DATASET

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PASS_THRESHOLD = 3  


def get_actual_answer_with_metrics(question):
    """
    Cavabı alır, həm də latency (vaxt) və token istifadəsini ölçür.
    """
    if not question.strip():
        return "Sual boşdur, cavab verilə bilmir.", 0.0, 0, 0

    start_time = time.time()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    latency = time.time() - start_time

    answer = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    return answer, latency, input_tokens, output_tokens


def llm_judge_score(question, expected_answer, actual_answer):
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


def run_evaluation_with_metrics():
    results = []

    for item in TEST_DATASET:
        answer, latency, in_tok, out_tok = get_actual_answer_with_metrics(item["question"])
        score = llm_judge_score(item["question"], item["expected_answer"], answer)

        results.append({
            "id": item["id"],
            "category": item["category"],
            "score": score,
            "passed": score >= PASS_THRESHOLD,
            "latency_sec": latency,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
        })

        print(f"#{item['id']} [{item['category']}] Score: {score}/5 | Latency: {latency:.2f}s | Tokens: {in_tok + out_tok}")

    # --- Metriklərin hesablanması ---
    total = len(results)
    pass_count = sum(1 for r in results if r["passed"])
    pass_rate = pass_count / total * 100

    avg_latency = sum(r["latency_sec"] for r in results) / total
    avg_tokens = sum(r["total_tokens"] for r in results) / total

    accuracy_by_category = {}
    for category in ["normal", "edge"]:
        cat_results = [r for r in results if r["category"] == category]
        if cat_results:
            accuracy_by_category[category] = sum(r["score"] for r in cat_results) / len(cat_results)

    print("\n" + "=" * 50)
    print("İZLƏNİLƏN METRİKLƏR")
    print("=" * 50)
    print(f"Pass-rate (bal >= {PASS_THRESHOLD}/5): {pass_rate:.1f}% ({pass_count}/{total})")
    print(f"Orta latency: {avg_latency:.2f} saniyə")
    print(f"Orta token xərci (sorğu başına): {avg_tokens:.0f} token")
    print(f"Normal suallar üzrə orta bal: {accuracy_by_category.get('normal', 0):.2f}/5")
    print(f"Edge case-lər üzrə orta bal: {accuracy_by_category.get('edge', 0):.2f}/5")

    return results


if __name__ == "__main__":
    run_evaluation_with_metrics()