"""Main agent logic for answering questions.

The implementation follows the specification in the task description.  It
retrieves relevant chunks, constructs a prompt for the LLM, parses the JSON
response, verifies citations, and retries once if needed.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

import ollama

from .retrieve import hybrid_search
from .verify import verify_citations


def _format_chunks(chunks: List[Any]) -> str:
    """Return a string with chunks delimited as <untrusted> blocks.

    The function accepts a list where each element is either a ``(id, text)``
    tuple or a dict with ``id`` and ``text`` keys.
    """
    parts: List[str] = []
    for c in chunks:
        if isinstance(c, dict):
            cid = c.get("id")
            txt = c.get("text", "")
        else:
            cid, txt = c
        parts.append(f"<untrusted>\n{cid}\n{txt}\n</untrusted>")
    return "\n".join(parts)


def answer_question(conn, query: str) -> Dict[str, Any]:
    """Answer a question using hybrid search and the Gemma4 LLM.

    Returns a dict with ``answer``, ``citations``, ``sources`` and
    ``confidence``.  If citation verification fails after one retry the answer
    is a refusal.
    """
    chunks = hybrid_search(conn, query, top_k=8)
    if not chunks:
        raise RuntimeError("No chunks retrieved for query")

    context = _format_chunks(chunks)
    prompt = (
        "Answer the following question using the provided context.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\n\n"
        "Provide a JSON object with keys: answer (str), citations (list of {chunk_id, quote}), confidence (float)."
    )

    def call():
        return ollama.chat(
            model="gemma4:12b",
            messages=[{"role": "user", "content": prompt}],
            format="json",
        )

    def parse(response: Dict[str, Any]) -> Dict[str, Any]:
        content = response.get("message", {}).get("content", "")
        try:
            data = json.loads(content)
        except Exception as exc:
            raise RuntimeError(f"LLM returned invalid JSON: {exc}")
        return data

    try:
        resp = call()
    except Exception as exc:
        raise RuntimeError(f"Ollama request failed: {exc}")

    payload = parse(resp)
    answer = payload.get("answer", "")
    citations = payload.get("citations", [])
    confidence = payload.get("confidence", 0.0)

    # map id to chunk text for verification
    chunks_by_id = {
        (c.get("id") if isinstance(c, dict) else c[0]): (c.get("text") if isinstance(c, dict) else c[1])
        for c in chunks
    }
    valid, invalid = verify_citations(citations, chunks_by_id)
    if invalid:
        # retry once
        try:
            resp = call()
        except Exception as exc:
            raise RuntimeError(f"Ollama retry failed: {exc}")
        payload = parse(resp)
        answer = payload.get("answer", "")
        citations = payload.get("citations", [])
        confidence = payload.get("confidence", 0.0)
        valid, invalid = verify_citations(citations, chunks_by_id)
        if invalid:
            return {
                "answer": "I cannot provide a reliable answer.",
                "citations": [],
                "sources": [],
                "confidence": 0.0,
            }

    sources = [chunks_by_id.get(cit["chunk_id"]) for cit in valid]
    return {"answer": answer, "citations": valid, "sources": sources, "confidence": confidence}

