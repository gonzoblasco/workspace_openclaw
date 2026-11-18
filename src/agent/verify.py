"""Verification utilities for the agent.

This module provides a function to verify that citations returned by the LLM
actually appear in the retrieved chunks.  The verification is deliberately
conservative: a citation is considered valid only when the exact quoted text
appears as a substring of the corresponding chunk after normalising whitespace.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Tuple, Dict, Any


def _normalize(text: str) -> str:
    """Normalize a string for substring matching.

    The function collapses consecutive whitespace characters into a single
    space and strips leading/trailing whitespace.  This mirrors the behaviour
    used elsewhere in the code‑base for text ingestion.
    """
    return re.sub(r"\s+", " ", text).strip()


def verify_citations(
    citations: Iterable[Dict[str, Any]],
    chunks_by_id: Dict[int, str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Separate valid and invalid citations.

    Parameters
    ----------
    citations:
        An iterable of dictionaries with at least ``chunk_id`` (int) and
        ``quote`` (str).
    chunks_by_id:
        Mapping from ``chunk_id`` to the raw chunk text.

    Returns
    -------
    tuple[list, list]
        ``(valid, invalid)`` where each list contains the original citation
        dictionaries.
    """
    valid: List[Dict[str, Any]] = []
    invalid: List[Dict[str, Any]] = []

    for cit in citations:
        cid = cit.get("chunk_id")
        quote = cit.get("quote", "")
        chunk = chunks_by_id.get(cid, "")
        if not chunk:
            invalid.append(cit)
            continue
        if _normalize(quote) in _normalize(chunk):
            valid.append(cit)
        else:
            invalid.append(cit)
    return valid, invalid

