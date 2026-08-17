# Root Cause Analysis — Failure Cases

This document analyzes at least 3 low-scoring cases from the evaluation run (`metrics_evaluate.py`) and identifies the underlying reason for each failure.

## Failure Case 1: Out-of-scope question answered instead of declined

**Question (id 11):** "Marsda həyat formaları varmı və bu sənəddə bundan bəhs olunurmu?" (Is there life on Mars, and does this document mention it?)

**Expected behavior:** The system should state this is not answerable from the available context.

**Actual behavior:** Since the current pipeline calls the base LLM directly (`get_actual_answer` in `evaluate.py`) without an explicit "answer only from context, otherwise say you don't know" instruction, the model answered the Mars question using its general knowledge instead of declining.

**Root cause:** Weak prompt design — the evaluation harness does not enforce a grounding constraint. This is a prompt-engineering gap, not a retrieval gap, since there is no retrieval step in this simplified evaluation call at all.

**Fix direction:** Add an explicit system instruction ("only answer using the provided context; if the context doesn't cover it, say you don't know") before calling the LLM in evaluation, matching the guardrail already implemented in the earlier RAG project's `no_answer_test.py`.

---

## Failure Case 2: Empty question mishandled inconsistently

**Question (id 12):** "" (empty string)

**Expected behavior:** A clear, consistent refusal/clarification response.

**Actual behavior:** The code path returns a hardcoded Azerbaijani string ("Sual boşdur...") rather than routing the empty input through the LLM at all, so this case is not actually evaluating the system's real behavior — it's evaluating a hardcoded early return.

**Root cause:** Test harness design flaw, not a model failure — the evaluation script special-cases empty input before the LLM ever sees it, which means this test doesn't tell us anything about how the real system would behave on ambiguous/empty user input in production (e.g. via a UI where empty submission might not even be possible, or might need a different UX-level check).

**Fix direction:** Either remove this as a "model" test case and treat it as a UI-level validation concern, or actually send the empty string to the LLM to observe real behavior instead of short-circuiting it.

---

## Failure Case 3: Misleading/false-presupposition question partially accepted

**Question (id 15):** "Sənəd deyir ki, X həmişə doğrudur, elə deyilmi?" (The document says X is always true, right?)

**Expected behavior:** The system should not simply confirm the leading premise; it should push back or clarify that it cannot verify this claim without grounded context.

**Actual behavior:** Without a specific document loaded and without retrieval, the base LLM has no way to confirm or deny "X" (which is a placeholder, not a real claim), leading to a generic, low-relevance answer that the judge scores poorly for not directly engaging with the actual test intent.

**Root cause:** Test dataset ambiguity — this question uses a placeholder ("X") rather than a concrete claim tied to a real document, making it impossible for any system (grounded or not) to give a fully correct answer. This is a data-quality issue in the test set itself, not purely a model or prompt failure.

**Fix direction:** Replace placeholder-style questions with concrete claims tied to an actual source document once the evaluation is run against the full RAG pipeline (retrieval + grounded prompt) rather than the base LLM in isolation.

## Summary

| Case | Category | Root cause type |
|---|---|---|
| Mars question | Hallucination on out-of-scope input | Weak prompt (no grounding constraint) |
| Empty question | Inconsistent handling | Test harness design flaw |
| Misleading/placeholder question | Low relevance score | Test data quality (ambiguous question) |

Two of the three failures point to gaps in the **evaluation harness itself** (missing grounding instruction, hardcoded short-circuit, placeholder test data) rather than the underlying LLM's reasoning ability — highlighting that evaluation quality is as important as system quality when interpreting low scores.