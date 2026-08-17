# RAG Evaluation Framework

A framework for testing and evaluating the outputs of an LLM/RAG system: a labeled test dataset, an automated LLM-as-judge scoring script, tracked performance metrics, root-cause analysis of failure cases, and a targeted few-shot prompt fix for one identified failure category.

## Project structure

- `test_dataset.py` — Checkpoint 1: a labeled test dataset of 17 question/expected-answer pairs, split into `normal` (directly answerable) and `edge` (ambiguous, multi-part, out-of-scope, or misleading questions) categories
- `evaluate.py` — Checkpoint 2: automated evaluation script that runs every question through the system and scores the actual answer against the expected answer using an LLM-as-judge (0-5 scale)
- `metrics_evaluate.py` — Checkpoint 3: extends the evaluation with tracked metrics — pass-rate, average latency, and average token cost per question
- `ROOT_CAUSE_ANALYSIS.md` — Checkpoint 4: root cause analysis of 3 low-scoring failure cases from the evaluation run
- `fix_hallucination.py` — Checkpoint 5: few-shot prompt fix for the hallucination-on-out-of-scope-questions failure identified in Checkpoint 4, with a before/after comparison

## How to run it

1. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

(Mac/Linux: `source venv/bin/activate`)

2. Install the dependencies:

```
pip install anthropic python-dotenv
```

3. Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=your_key_here
```

`.env` is listed in `.gitignore`, so it will never be pushed to GitHub.

4. Run each stage:

```
python test_dataset.py
python evaluate.py
python metrics_evaluate.py
python fix_hallucination.py
```

5. Review `ROOT_CAUSE_ANALYSIS.md` for the failure analysis.

## How it works

### Test dataset (Checkpoint 1)

`test_dataset.py` defines 17 question/expected-answer pairs. Normal questions test direct factual recall; edge cases specifically target hallucination risk with empty input, nonsensical input, out-of-scope questions, multi-part compound questions, and misleading questions with false presuppositions.

### Automated evaluation (Checkpoint 2)

`evaluate.py` sends each question through the system, then uses a separate Claude call as an impartial judge to score the actual answer against the expected answer/behavior on a 0-5 scale.

### Tracked metrics (Checkpoint 3)

`metrics_evaluate.py` additionally tracks pass-rate (≥3/5 threshold), average latency (via `time.time()`), and average token cost (via `response.usage`).

### Root cause analysis (Checkpoint 4)

`ROOT_CAUSE_ANALYSIS.md` documents 3 low-scoring cases and traces each to its underlying cause: a weak grounding prompt, a hardcoded test-harness short-circuit, and an ambiguous placeholder test question.

### Few-shot fix (Checkpoint 5)

`fix_hallucination.py` addresses the weak-prompt root cause with a before/after comparison. The "before" version calls the model with no system prompt; the "after" version adds a system prompt framing the assistant as document-only, plus 2 few-shot examples of correct refusal behavior. Running the same out-of-scope question through both confirms the fix works: the before version answers from general knowledge, the after version correctly declines.

## Security

API keys are loaded from a `.env` file using `python-dotenv`. `.env` is included in `.gitignore`, so no sensitive credentials will ever be pushed to GitHub.