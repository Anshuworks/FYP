"""
Unit tests for member2_intelligence.intelligence.evidence_retriever

Tests the deterministic lexical evidence retrieval against a fixed
in-memory transcript. Fully deterministic — no models, network, or
external dependencies.
"""
import sys
import os
import copy

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from member2_intelligence.intelligence.evidence_retriever import retrieve_evidence
from member2_intelligence.intelligence.schemas import Evidence


# -- Fixture ----------------------------------------------------------------

def _make_transcript():
    """A fixed multi-segment transcript for deterministic testing."""
    return {
        "meeting_id": "test_retrieval",
        "language": "en",
        "segments": [
            {
                "id": 1,
                "speaker": "SPEAKER_00",
                "start": 0.0,
                "end": 5.5,
                "raw_text": "The budget for Q3 has been approved by the board.",
                "cleaned_text": "The budget for q3 has been approved by the board.",
                "text": "The budget for Q3 has been approved by the board.",
                "overlap": False,
            },
            {
                "id": 2,
                "speaker": "SPEAKER_01",
                "start": 6.0,
                "end": 12.0,
                "raw_text": "We need to hire two engineers before the deadline.",
                "cleaned_text": "We need to hire two engineers before the deadline.",
                "text": "We need to hire two engineers before the deadline.",
                "overlap": False,
            },
            {
                "id": 3,
                "speaker": "SPEAKER_00",
                "start": 13.0,
                "end": 18.5,
                "raw_text": "The marketing team's budget request was denied.",
                "cleaned_text": "The marketing team's budget request was denied.",
                "text": "The marketing team's budget request was denied.",
                "overlap": False,
            },
            {
                "id": 4,
                "speaker": "SPEAKER_02",
                "start": 19.0,
                "end": 25.0,
                "raw_text": "I disagree. The budget should not have been approved.",
                "cleaned_text": "I disagree. The budget should not have been approved.",
                "text": "I disagree. The budget should not have been approved.",
                "overlap": False,
            },
            {
                "id": 5,
                "speaker": "SPEAKER_01",
                "start": 26.0,
                "end": 30.0,
                "raw_text": "Let's schedule a follow-up meeting for Friday.",
                "cleaned_text": "Let's schedule a follow-up meeting for friday.",
                "text": "Let's schedule a follow-up meeting for Friday.",
                "overlap": False,
            },
        ],
    }


# -- Tests: Basic Retrieval -------------------------------------------------

def test_exact_terms_retrieve_expected_segment():
    """Query with exact terms should retrieve the matching segment."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "budget approved", top_k=1)
    assert len(results) >= 1
    # Segment 1 has both "budget" and "approved" — should rank highest
    assert results[0].segment_id == 1
    print("  PASS: exact query terms retrieve expected segment")


def test_case_insensitive_matching():
    """Case differences should not prevent matching."""
    transcript = _make_transcript()
    results_lower = retrieve_evidence(transcript, "budget approved", top_k=1)
    results_upper = retrieve_evidence(transcript, "BUDGET APPROVED", top_k=1)
    results_mixed = retrieve_evidence(transcript, "Budget Approved", top_k=1)
    assert results_lower[0].segment_id == results_upper[0].segment_id
    assert results_lower[0].segment_id == results_mixed[0].segment_id
    print("  PASS: case differences do not prevent matching")


def test_punctuation_does_not_prevent_matching():
    """Punctuation differences should not prevent matching."""
    transcript = _make_transcript()
    # "follow-up" in segment 5 should match "follow up" query
    results = retrieve_evidence(transcript, "schedule follow up meeting", top_k=1)
    assert len(results) >= 1
    assert results[0].segment_id == 5
    print("  PASS: punctuation differences do not prevent matching")


def test_multiple_segments_ranked_deterministically():
    """Multiple matching segments should be ranked by score, ties by id."""
    transcript = _make_transcript()
    # "budget" appears in segments 1, 3, 4
    results = retrieve_evidence(transcript, "budget", top_k=5)
    assert len(results) >= 2
    # Run twice to confirm determinism
    results2 = retrieve_evidence(transcript, "budget", top_k=5)
    for r1, r2 in zip(results, results2):
        assert r1.segment_id == r2.segment_id
    print("  PASS: multiple segments ranked deterministically")


def test_top_k_limits_results():
    """top_k should cap the number of returned Evidence objects."""
    transcript = _make_transcript()
    results_1 = retrieve_evidence(transcript, "budget", top_k=1)
    results_2 = retrieve_evidence(transcript, "budget", top_k=2)
    results_5 = retrieve_evidence(transcript, "budget", top_k=5)
    assert len(results_1) == 1
    assert len(results_2) == 2
    assert len(results_5) >= 2  # at most 3 segments contain "budget"
    print("  PASS: top_k limits returned evidence count")


# -- Tests: Evidence Integrity ----------------------------------------------

def test_quote_comes_from_raw_text():
    """Evidence.quote must be the segment's raw_text, not cleaned_text."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "budget approved", top_k=1)
    assert len(results) >= 1
    seg1 = transcript["segments"][0]
    assert results[0].quote == seg1["raw_text"]
    print("  PASS: Evidence.quote comes from raw_text")


def test_evidence_fields_match_source_segment():
    """speaker, start, end, segment_id must come from the original segment."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "hire engineers deadline", top_k=1)
    assert len(results) >= 1
    ev = results[0]
    seg2 = transcript["segments"][1]  # segment about hiring
    assert ev.segment_id == seg2["id"]
    assert ev.speaker == seg2["speaker"]
    assert ev.start == seg2["start"]
    assert ev.end == seg2["end"]
    assert ev.quote == seg2["raw_text"]
    print("  PASS: Evidence fields match source segment exactly")


def test_evidence_objects_are_valid():
    """All returned Evidence objects should pass validation."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "budget", top_k=5)
    for ev in results:
        ev.validate()  # should not raise
    print("  PASS: all returned Evidence objects pass validation")


# -- Tests: Edge Cases -------------------------------------------------------

def test_empty_query_returns_no_evidence():
    transcript = _make_transcript()
    assert retrieve_evidence(transcript, "", top_k=3) == []
    assert retrieve_evidence(transcript, "   ", top_k=3) == []
    print("  PASS: empty/whitespace query returns no evidence")


def test_empty_transcript_returns_no_evidence():
    empty = {"meeting_id": "empty", "language": "en", "segments": []}
    assert retrieve_evidence(empty, "budget", top_k=3) == []
    print("  PASS: empty transcript returns no evidence")


def test_no_meaningful_overlap_returns_no_evidence():
    """A query with zero term overlap should return nothing."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "quantum entanglement superconductor", top_k=3)
    assert results == []
    print("  PASS: unrelated query returns no evidence")


def test_missing_raw_text_skipped():
    """Segments with empty raw_text should be silently skipped."""
    transcript = {
        "meeting_id": "t", "language": "en",
        "segments": [
            {"id": 1, "speaker": "S0", "start": 0.0, "end": 1.0,
             "raw_text": "", "cleaned_text": "", "text": "", "overlap": False},
            {"id": 2, "speaker": "S1", "start": 2.0, "end": 3.0,
             "raw_text": "The budget is ready.", "cleaned_text": "",
             "text": "The budget is ready.", "overlap": False},
        ],
    }
    results = retrieve_evidence(transcript, "budget", top_k=3)
    assert len(results) == 1
    assert results[0].segment_id == 2
    print("  PASS: segments with empty raw_text are skipped")


def test_top_k_larger_than_matches():
    """top_k larger than matching segments should return all matches."""
    transcript = _make_transcript()
    results = retrieve_evidence(transcript, "follow up meeting friday", top_k=100)
    # Should return however many match, not crash
    assert len(results) >= 1
    assert len(results) <= len(transcript["segments"])
    print("  PASS: top_k > available matches returns all matches")


def test_input_transcript_not_mutated():
    """retrieve_evidence must not modify the input transcript."""
    transcript = _make_transcript()
    original = copy.deepcopy(transcript)
    retrieve_evidence(transcript, "budget approved", top_k=3)
    assert transcript == original
    print("  PASS: input transcript not mutated")


# -- Runner ------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Running Evidence Retriever Tests")
    print("=" * 60)

    print("\n--- Basic Retrieval ---")
    test_exact_terms_retrieve_expected_segment()
    test_case_insensitive_matching()
    test_punctuation_does_not_prevent_matching()
    test_multiple_segments_ranked_deterministically()
    test_top_k_limits_results()

    print("\n--- Evidence Integrity ---")
    test_quote_comes_from_raw_text()
    test_evidence_fields_match_source_segment()
    test_evidence_objects_are_valid()

    print("\n--- Edge Cases ---")
    test_empty_query_returns_no_evidence()
    test_empty_transcript_returns_no_evidence()
    test_no_meaningful_overlap_returns_no_evidence()
    test_missing_raw_text_skipped()
    test_top_k_larger_than_matches()
    test_input_transcript_not_mutated()

    print("\n" + "=" * 60)
    print("[OK] ALL EVIDENCE RETRIEVER TESTS PASSED")
    print("=" * 60)
