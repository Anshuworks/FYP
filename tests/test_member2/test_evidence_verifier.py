"""
Unit tests for member2_intelligence.intelligence.evidence_verifier

Tests structural evidence verification and lexical claim support
classification. Fully deterministic — no models, network, or external
dependencies.
"""
import sys
import os
import copy

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from member2_intelligence.intelligence.schemas import Evidence, Claim
from member2_intelligence.intelligence.evidence_verifier import (
    verify_evidence,
    verify_claim,
    VerificationResult,
    THRESHOLD_SUPPORTED,
    THRESHOLD_PARTIAL,
)


# -- Fixture ----------------------------------------------------------------

def _make_transcript():
    """A fixed multi-segment transcript for deterministic testing."""
    return {
        "meeting_id": "test_verify",
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
                "raw_text": "The marketing team requested additional funding.",
                "cleaned_text": "The marketing team requested additional funding.",
                "text": "The marketing team requested additional funding.",
                "overlap": False,
            },
        ],
    }


def _valid_evidence(seg_index=0):
    """Create a valid Evidence matching transcript segment at given index."""
    t = _make_transcript()
    seg = t["segments"][seg_index]
    return Evidence(
        segment_id=seg["id"],
        speaker=seg["speaker"],
        start=seg["start"],
        end=seg["end"],
        quote=seg["raw_text"],
    )


# -- Tests: verify_evidence (structural) ------------------------------------

def test_valid_evidence_accepted():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    assert verify_evidence(transcript, ev) is True
    print("  PASS: valid evidence is accepted")


def test_wrong_segment_id_rejected():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    ev.segment_id = 999  # does not exist
    assert verify_evidence(transcript, ev) is False
    print("  PASS: wrong segment_id is rejected")


def test_wrong_speaker_rejected():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    ev.speaker = "SPEAKER_99"
    assert verify_evidence(transcript, ev) is False
    print("  PASS: wrong speaker is rejected")


def test_wrong_start_rejected():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    ev.start = 99.0
    assert verify_evidence(transcript, ev) is False
    print("  PASS: wrong start timestamp is rejected")


def test_wrong_end_rejected():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    ev.end = 99.0
    assert verify_evidence(transcript, ev) is False
    print("  PASS: wrong end timestamp is rejected")


def test_paraphrased_quote_rejected():
    """A quote that paraphrases the original must be rejected."""
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    ev.quote = "The Q3 budget was approved."  # paraphrase, not exact raw_text
    assert verify_evidence(transcript, ev) is False
    print("  PASS: paraphrased quote is rejected")


def test_exact_raw_text_quote_accepted():
    """Quote that exactly matches raw_text must be accepted."""
    transcript = _make_transcript()
    ev = _valid_evidence(1)  # segment 2
    assert ev.quote == "We need to hire two engineers before the deadline."
    assert verify_evidence(transcript, ev) is True
    print("  PASS: exact raw_text quote is accepted")


def test_all_segments_verifiable():
    """Every segment in the transcript should produce verifiable evidence."""
    transcript = _make_transcript()
    for i in range(len(transcript["segments"])):
        ev = _valid_evidence(i)
        assert verify_evidence(transcript, ev) is True
    print("  PASS: all segments produce verifiable evidence")


# -- Tests: verify_claim (lexical support) -----------------------------------

def test_strong_support_returns_supported():
    """Claim with high lexical overlap should return SUPPORTED."""
    transcript = _make_transcript()
    # Claim closely mirrors segment 1
    claim = Claim(
        id="c1",
        text="The budget for Q3 has been approved.",
        evidence=[_valid_evidence(0)],
    )
    result = verify_claim(claim, transcript)
    assert result.status == "SUPPORTED", f"Expected SUPPORTED, got {result.status} (score={result.score:.2f})"
    assert len(result.verified_evidence) == 1
    assert result.score >= THRESHOLD_SUPPORTED
    print("  PASS: strong lexical support returns SUPPORTED")


def test_partial_support_returns_partially_supported():
    """Claim with moderate overlap should return PARTIALLY_SUPPORTED."""
    transcript = _make_transcript()
    # Shares "budget" and "board" with segment 1, but adds unrelated terms
    # that dilute the score into the partial range
    claim = Claim(
        id="c2",
        text="The budget was reviewed and discussed extensively by the board last week.",
        evidence=[_valid_evidence(0)],
    )
    result = verify_claim(claim, transcript)
    assert result.status == "PARTIALLY_SUPPORTED", \
        f"Expected PARTIALLY_SUPPORTED, got {result.status} (score={result.score:.2f})"
    assert result.score >= THRESHOLD_PARTIAL
    assert result.score < THRESHOLD_SUPPORTED
    print("  PASS: partial lexical support returns PARTIALLY_SUPPORTED")


def test_unsupported_claim_returns_unsupported():
    """Claim with no lexical overlap should return UNSUPPORTED."""
    transcript = _make_transcript()
    # Claim completely unrelated to segment 1
    claim = Claim(
        id="c3",
        text="Quantum computing will revolutionize cryptography.",
        evidence=[_valid_evidence(0)],
    )
    result = verify_claim(claim, transcript)
    assert result.status == "UNSUPPORTED", \
        f"Expected UNSUPPORTED, got {result.status} (score={result.score:.2f})"
    assert result.score < THRESHOLD_PARTIAL
    print("  PASS: unsupported claim returns UNSUPPORTED")


def test_multiple_evidence_handled():
    """A claim with multiple evidence objects should verify each independently."""
    transcript = _make_transcript()
    claim = Claim(
        id="c4",
        text="The budget was approved and hiring engineers is needed.",
        evidence=[_valid_evidence(0), _valid_evidence(1)],
    )
    result = verify_claim(claim, transcript)
    assert len(result.verified_evidence) == 2
    # Should be at least partially supported since terms overlap both segments
    assert result.status in ("SUPPORTED", "PARTIALLY_SUPPORTED")
    print("  PASS: multiple evidence objects handled correctly")


def test_mixed_valid_invalid_evidence():
    """Valid evidence should still count when some evidence is invalid."""
    transcript = _make_transcript()
    good_ev = _valid_evidence(0)
    bad_ev = Evidence(segment_id=999, speaker="X", start=0.0, end=1.0, quote="fake")
    claim = Claim(
        id="c5",
        text="The budget for Q3 has been approved.",
        evidence=[bad_ev, good_ev],
    )
    result = verify_claim(claim, transcript)
    assert len(result.verified_evidence) == 1  # only the good one
    assert result.verified_evidence[0].segment_id == good_ev.segment_id
    assert result.status == "SUPPORTED"
    print("  PASS: valid evidence still counts when mixed with invalid")


def test_all_evidence_invalid_returns_unsupported():
    """If all evidence fails structural checks, claim is UNSUPPORTED."""
    transcript = _make_transcript()
    bad_ev = Evidence(segment_id=999, speaker="X", start=0.0, end=1.0, quote="fake")
    claim = Claim(id="c6", text="Something.", evidence=[bad_ev])
    result = verify_claim(claim, transcript)
    assert result.status == "UNSUPPORTED"
    assert len(result.verified_evidence) == 0
    print("  PASS: all-invalid evidence returns UNSUPPORTED")


# -- Tests: Edge Cases -------------------------------------------------------

def test_empty_claim_text():
    transcript = _make_transcript()
    claim = Claim(id="c7", text="", evidence=[_valid_evidence(0)])
    result = verify_claim(claim, transcript)
    assert result.status == "UNSUPPORTED"
    assert "empty" in result.reason.lower()
    print("  PASS: empty claim text returns UNSUPPORTED")


def test_empty_evidence_list():
    transcript = _make_transcript()
    claim = Claim(id="c8", text="Some claim.", evidence=[])
    result = verify_claim(claim, transcript)
    assert result.status == "UNSUPPORTED"
    assert "no evidence" in result.reason.lower()
    print("  PASS: empty evidence list returns UNSUPPORTED")


def test_empty_transcript():
    empty = {"meeting_id": "empty", "language": "en", "segments": []}
    ev = Evidence(segment_id=1, speaker="S", start=0.0, end=1.0, quote="q")
    claim = Claim(id="c9", text="Something.", evidence=[ev])
    result = verify_claim(claim, transcript=empty)
    assert result.status == "UNSUPPORTED"
    print("  PASS: empty transcript returns UNSUPPORTED")


def test_transcript_not_mutated():
    transcript = _make_transcript()
    original = copy.deepcopy(transcript)
    claim = Claim(
        id="c10",
        text="The budget for Q3 has been approved.",
        evidence=[_valid_evidence(0)],
    )
    verify_claim(claim, transcript)
    assert transcript == original
    print("  PASS: transcript not mutated")


def test_claim_not_mutated():
    transcript = _make_transcript()
    ev = _valid_evidence(0)
    claim = Claim(id="c11", text="The budget was approved.", evidence=[ev])
    original_text = claim.text
    original_ev_count = len(claim.evidence)
    verify_claim(claim, transcript)
    assert claim.text == original_text
    assert len(claim.evidence) == original_ev_count
    print("  PASS: claim not mutated")


def test_verification_result_has_score():
    """VerificationResult should expose the numeric score for debugging."""
    transcript = _make_transcript()
    claim = Claim(
        id="c12",
        text="The budget for Q3 has been approved.",
        evidence=[_valid_evidence(0)],
    )
    result = verify_claim(claim, transcript)
    assert isinstance(result.score, float)
    assert 0.0 <= result.score <= 1.0
    print("  PASS: VerificationResult exposes numeric score")


# -- Runner ------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Running Evidence Verifier Tests")
    print("=" * 60)

    print("\n--- Structural Verification (verify_evidence) ---")
    test_valid_evidence_accepted()
    test_wrong_segment_id_rejected()
    test_wrong_speaker_rejected()
    test_wrong_start_rejected()
    test_wrong_end_rejected()
    test_paraphrased_quote_rejected()
    test_exact_raw_text_quote_accepted()
    test_all_segments_verifiable()

    print("\n--- Claim Verification (verify_claim) ---")
    test_strong_support_returns_supported()
    test_partial_support_returns_partially_supported()
    test_unsupported_claim_returns_unsupported()
    test_multiple_evidence_handled()
    test_mixed_valid_invalid_evidence()
    test_all_evidence_invalid_returns_unsupported()

    print("\n--- Edge Cases ---")
    test_empty_claim_text()
    test_empty_evidence_list()
    test_empty_transcript()
    test_transcript_not_mutated()
    test_claim_not_mutated()
    test_verification_result_has_score()

    print("\n" + "=" * 60)
    print("[OK] ALL EVIDENCE VERIFIER TESTS PASSED")
    print("=" * 60)
