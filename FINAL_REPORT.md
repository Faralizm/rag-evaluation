# Final Evaluation Report — RAG Evaluation Framework

## Methodology

1. **Test dataset** (`test_dataset.py`): 17 question/expected-answer pairs, split into 10 "normal" questions (directly answerable factual/summary questions) and 7 "edge" cases (empty input, nonsensical input, out-of-scope questions, multi-part compound questions, misleading questions with false presuppositions).

2. **Automated scoring** (`evaluate.py`, `metrics_evaluate.py`): each question was sent through the system, and the actual answer was scored against the expected answer/behavior using an LLM-as-judge approach — a separate Claude call graded each response 0-5 against explicit criteria. Alongside correctness, three operational metrics were tracked per question: pass-rate (score ≥3/5), latency (wall-clock time per API call), and token cost (input + output tokens via the API's usage field).

3. **Root cause analysis** (`ROOT_CAUSE_ANALYSIS.md`): the 3 lowest-scoring cases were manually reviewed to identify whether the failure stemmed from the model itself, the prompt design, or the evaluation harness/test data.

4. **Targeted fix** (`fix_hallucination.py`): the most actionable root cause (weak grounding prompt causing hallucination on out-of-scope questions) was addressed via few-shot prompt optimization, with a documented before/after comparison on the same test question.

## Key Results

- Overall average judge score and per-category (normal vs edge) averages were computed by `metrics_evaluate.py` (see console output from that run for exact figures on this run).
- The system consistently performed better on normal, directly-answerable questions than on edge cases, which is expected — edge cases are explicitly designed to be harder and probe hallucination risk.
- The single largest, most fixable failure category was **ungrounded answering on out-of-scope questions** — this was the target of the Checkpoint 5 fix.

## Root Causes Identified

| # | Failure type | Root cause category |
|---|---|---|
| 1 | Hallucination on out-of-scope question | Weak prompt (no grounding constraint) |
| 2 | Inconsistent empty-input handling | Evaluation harness design flaw |
| 3 | Low relevance on misleading/placeholder question | Test data quality issue |

An important finding: **2 of 3 identified failures were evaluation-harness or test-data issues, not genuine model reasoning failures.** This is a common and easy-to-miss trap in LLM evaluation — a low score doesn't always mean the model is wrong; sometimes the test itself is flawed.

## Fix Applied and Result

The grounding-prompt fix (few-shot system prompt instructing the model to answer only from provided context and decline otherwise) was tested against the same out-of-scope question that originally failed. The "before" version answered using general world knowledge; the "after" version correctly declined to answer, confirming the fix resolves the specific root cause without requiring fine-tuning or additional infrastructure.

## Limitations and Next Steps

- This evaluation was run against a simplified LLM call rather than the full RAG pipeline (retrieval + grounded context) from the earlier project; a production evaluation should run against the actual retrieval-augmented endpoint.
- LLM-as-judge scoring has known biases (e.g., verbosity bias) and should ideally be supplemented with human spot-checks on a sample of results.
- The empty-input and placeholder-question test cases should be redesigned per the recommendations in `ROOT_CAUSE_ANALYSIS.md` before the next evaluation cycle.