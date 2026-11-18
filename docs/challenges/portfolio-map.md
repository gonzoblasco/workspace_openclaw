# Portfolio map

Two public, local-first projects. They share a thesis: **the model is not the product; the constraint is.**

| Repo | What it proves | Verify in 5 minutes |
|---|---|---|
| [memoria-oral](https://github.com/gonzoblasco/memoria-oral) | Local speech intelligence with an ethical frame | `uv run pytest -q` (8 tests), then its privacy check (0 sockets) |
| [localdoc-agent](https://github.com/gonzoblasco/localdoc-agent) | Retrieval with citations that cannot be hallucinated | `uv run pytest -q` (10 tests), then `eval/results.json` in that repo (18/18) |

## memoria-oral

**Problem:** family voices are irrecuperable, and commercial transcription sends them to subprocessors in other jurisdictions.

**What it does:** records an interview, transcribes it with `whisper.cpp` on the machine, finds the gaps in the story against a checklist, and asks the next question with a local LLM.

**The non-obvious decisions:**

- `whisper.cpp` over a hosted API: the audio never leaves the laptop.
- A checklist, not a better model: the question quality saturates early; coverage is the real lever.
- Consent before code: the UI blocks transcription without an explicit checkbox.

**Measured:** 7.1 s audio → 1.63 s compute (4.4× real time), 0 `lsof` connections during transcription, timestamps verified against `afinfo`.

**Honest limits:** voseo is inconsistent on a 4B model; the bundled demo audio is synthetic; no diarization.

## localdoc-agent

**Problem:** an LLM answering questions about contracts will invent a page number and a quote, and a confident wrong answer is worse than no answer.

**What it does:** hybrid retrieval (BM25 + KNN + RRF) over SQLite, then an LLM answer whose citations are checked by substring containment. Invalid quote → retry once → refusal.

**The non-obvious decisions:**

- Verification is deterministic (`verify.py`), not a second LLM.
- Arithmetic is code (`calc.py`), not the model: a 12B reliably fails to add two contract totals.
- Smaller is not faster: `qwen3.5:9b` took >90 s with a 262k context while `gemma4:12b` answered in ~50 s.

**Measured:** 18/18 on an 18-question eval; 4B model scores 4/18 at 6.8 s (speed/accuracy data is in the repo).

**Honest limits:** PDFs need selectable text; ~50 s per answer; the eval is small and self-authored.

## Why these two together

One is about **people**, the other about **correctness**. Both are about the same engineering habit: state the constraint, then measure whether the build respects it — and publish the measurement even when it embarrasses the design.

## Build process

Both were planned with a step-based planner, implemented by role agents (developer, designer, auditor, critic), and every claim in their docs was verified against the running code rather than accepted from a subagent's report. That process produced its own lesson, documented in `localdoc-agent`'s README: three times a delegate reported a module it never wrote, and the fix was procedural, not technical.
