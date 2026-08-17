# RAG Evaluation Framework

A framework for testing and evaluating the outputs of an LLM/RAG system, including a labeled test dataset and an automated LLM-as-judge scoring script.

## Project structure

- `test_dataset.py` — Checkpoint 1: a labeled test dataset of 17 question/expected-answer pairs, split into `normal` (directly answerable) and `edge` (ambiguous, multi-part, out-of-scope, or misleading questions) categories
- `evaluate.py` — Checkpoint 2: automated evaluation script that runs every question through the system and scores the actual answer against the expected answer using an LLM-as-judge (0-5 scale), reporting per-question and per-category average scores

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
```

## How it works

### Test dataset (Checkpoint 1)

`test_dataset.py` defines 17 question/expected-answer pairs. Normal questions test direct factual recall; edge cases specifically target hallucination risk with empty input, nonsensical input, out-of-scope questions, multi-part compound questions, and misleading questions with false presuppositions.

### Automated evaluation (Checkpoint 2)

`evaluate.py` sends each question through the system, then uses a separate Claude call as an impartial judge to score the actual answer against the expected answer/behavior on a 0-5 scale, based on explicit grading criteria in the judge prompt. Results are aggregated into overall, normal-only, and edge-only average scores, making it easy to see whether the system handles straightforward and adversarial cases differently.

## Security

API keys are loaded from a `.env` file using `python-dotenv`. `.env` is included in `.gitignore`, so no sensitive credentials will ever be pushed to GitHub.