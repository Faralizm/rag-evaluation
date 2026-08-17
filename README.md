# RAG Evaluation Framework

A framework for testing and evaluating the outputs of the previous RAG pipeline (`rag-document-chat`), including a labeled test dataset covering both normal and edge-case questions.

## Project structure

- `test_dataset.py` — Checkpoint 1: a labeled test dataset of 17 question/expected-answer pairs, split into `normal` (directly answerable from the document) and `edge` (ambiguous, multi-part, out-of-scope, or misleading questions) categories

## How to run it

1. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate   # Mac/Linux: source venv/bin/activate
```

2. Run the dataset to verify it loads correctly:
```bash
   python test_dataset.py
```

## How it works

`test_dataset.py` defines `TEST_DATASET`, a list of dictionaries each containing an `id`, `category` (`normal` or `edge`), a `question`, and an `expected_answer`. This dataset will be used by the automated evaluation script (next checkpoint) to run each question through the RAG pipeline and score the actual output against the expected answer.

Edge cases specifically cover: questions with no answer in the source document, empty/malformed input, multi-part compound questions, and misleading questions with false presuppositions — designed to test whether the RAG system correctly declines to hallucinate rather than fabricating a plausible-sounding answer.