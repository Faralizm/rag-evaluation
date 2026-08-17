# RAG Evaluation Framework

A framework for testing and evaluating the outputs of an LLM/RAG system: a labeled test dataset, an automated LLM-as-judge scoring script, tracked performance metrics, root-cause analysis of failure cases, a targeted few-shot prompt fix, and a final summary report.

## Project structure

- `test_dataset.py` — Checkpoint 1: a labeled test dataset of 17 question/expected-answer pairs, split into `normal` and `edge` categories
- `evaluate.py` — Checkpoint 2: automated evaluation script using LLM-as-judge scoring (0-5 scale)
- `metrics_evaluate.py` — Checkpoint 3: adds tracked metrics — pass-rate, average latency, average token cost
- `ROOT_CAUSE_ANALYSIS.md` — Checkpoint 4: root cause analysis of 3 low-scoring failure cases
- `fix_hallucination.py` — Checkpoint 5: few-shot prompt fix for hallucination on out-of-scope questions, with before/after comparison
- `FINAL_REPORT.md` — Checkpoint 6: final report summarizing methodology, results, root causes, and next steps

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

5. Read `ROOT_CAUSE_ANALYSIS.md` and `FINAL_REPORT.md` for the written analysis.

## How it works

### Test dataset (Checkpoint 1)
17 question/expected-answer pairs: normal questions test direct factual recall; edge cases target hallucination risk with empty input, nonsensical input, out-of-scope questions, multi-part questions, and misleading presuppositions.

### Automated evaluation (Checkpoint 2)
Each question is run through the system, then scored 0-5 by a separate Claude call acting as an impartial judge, based on explicit grading criteria.

### Tracked metrics (Checkpoint 3)
Pass-rate (≥3/5), average latency (`time.time()`), and average token cost (`response.usage`) are computed per run.

### Root cause analysis (Checkpoint 4)
3 low-scoring cases are traced to their root causes: a weak grounding prompt, a test-harness design flaw, and a test-data quality issue.

### Few-shot fix (Checkpoint 5)
The weak-prompt root cause is fixed with a system prompt + few-shot examples instructing the model to answer only from provided context. A before/after comparison confirms the fix works.

### Final report (Checkpoint 6)
`FINAL_REPORT.md` ties everything together: methodology, key results, the root-cause summary table, the fix outcome, and limitations/next steps — including the finding that most failures were evaluation-harness issues, not model issues.

## Security

API keys are loaded from a `.env` file using `python-dotenv`. `.env` is included in `.gitignore`, so no sensitive credentials will ever be pushed to GitHub.