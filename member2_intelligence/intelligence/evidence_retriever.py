"""
Deterministic Evidence Retriever

Given a structured transcript and a natural-language query, retrieves
the transcript segments most likely to support the query and converts
them into Evidence objects (from schemas.py).

Uses transparent lexical matching only — no LLMs, no embeddings, no
external dependencies. Ranking is fully deterministic: identical input
always produces identical output.

Evidence.quote always comes from raw_text — never generated or paraphrased.
"""
import re
import string
from typing import Dict, List, Any, Optional

from member2_intelligence.intelligence.schemas import Evidence


# ---------------------------------------------------------------------------
# Stop words — minimal set to reduce noise in lexical matching.
# Kept small and explicit to stay transparent.
# ---------------------------------------------------------------------------

_STOP_WORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "must",
    "i", "me", "my", "we", "our", "you", "your", "he", "him", "his",
    "she", "her", "it", "its", "they", "them", "their",
    "this", "that", "these", "those",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "as",
    "into", "about", "between", "through", "during", "before", "after",
    "and", "but", "or", "nor", "not", "no", "so", "if", "then", "than",
    "too", "very", "just",
})


# ---------------------------------------------------------------------------
# Text normalization and tokenization
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase and strip punctuation from text."""
    text = text.lower()
    # Replace punctuation with spaces so "can't" becomes "can t"
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    return text


def _tokenize(text: str) -> List[str]:
    """Normalize, split, and remove stop words. Returns deduplicated tokens
    in their original encounter order (for determinism)."""
    normalized = _normalize(text)
    words = normalized.split()
    seen = set()
    tokens = []
    for w in words:
        if w and w not in _STOP_WORDS and w not in seen:
            seen.add(w)
            tokens.append(w)
    return tokens


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score_segment(query_tokens: List[str], segment_text: str) -> float:
    """
    Computes a relevance score between a query and a segment's text.

    Score = (number of query tokens found in the segment text)
            / (total query tokens)

    This gives a value in [0.0, 1.0] representing the fraction of query
    terms that appear in the segment. A score of 0.0 means no overlap.

    Args:
        query_tokens: Pre-tokenized query terms (no stop words).
        segment_text: The raw text of the segment.

    Returns:
        A float score in [0.0, 1.0].
    """
    if not query_tokens:
        return 0.0

    segment_normalized = _normalize(segment_text)
    # Use word-boundary matching to avoid partial matches
    # (e.g. "budget" should not match inside "budgeting" — but for
    # simplicity and recall, we use substring-in-tokens approach)
    segment_words = set(segment_normalized.split())

    matches = sum(1 for qt in query_tokens if qt in segment_words)
    return matches / len(query_tokens)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def retrieve_evidence(
    transcript: Dict[str, Any],
    query: str,
    top_k: int = 3,
    min_score: float = 0.0,
) -> List[Evidence]:
    """
    Retrieves transcript segments that best match the query and returns
    them as Evidence objects.

    Uses deterministic lexical matching: tokenizes the query and each
    segment, computes term-overlap scores, and returns the top-k
    segments above min_score.

    Evidence.quote always comes from the segment's raw_text — never
    generated or paraphrased. All Evidence fields are copied directly
    from the matching segment.

    Args:
        transcript: The complete structured transcript dictionary
                    (Member 1 contract format) with 'segments'.
        query:      A natural-language query or claim to search for.
        top_k:      Maximum number of Evidence objects to return.
                    Defaults to 3.
        min_score:  Minimum relevance score (0.0–1.0) for a segment
                    to be included. Defaults to 0.0 (any non-zero
                    overlap is included). Segments with score == 0.0
                    are always excluded.

    Returns:
        A list of Evidence objects, ranked by relevance score
        (descending). Ties are broken by segment id (ascending)
        for determinism. Returns an empty list if no segments match
        or if the query/transcript is empty.
    """
    # Guard: empty query or empty/missing transcript
    if not query or not query.strip():
        return []

    segments = transcript.get("segments", [])
    if not segments:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    # Score each segment
    scored: List[tuple] = []  # (score, segment_id, segment_dict)
    for segment in segments:
        raw_text = segment.get("raw_text", "")
        if not raw_text:
            continue

        score = _score_segment(query_tokens, raw_text)
        if score > 0.0 and score >= min_score:
            scored.append((score, segment["id"], segment))

    if not scored:
        return []

    # Sort: highest score first, then by segment id ascending for tie-breaking
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Build Evidence objects from top-k results
    results: List[Evidence] = []
    for score, seg_id, segment in scored[:top_k]:
        results.append(Evidence(
            segment_id=segment["id"],
            speaker=segment["speaker"],
            start=segment["start"],
            end=segment["end"],
            quote=segment["raw_text"],
        ))

    return results
