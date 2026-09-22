"""
Unit tests for member2_intelligence.preprocessing.preprocessor

Tests the per-segment preprocessing stage (preprocess_transcript) and
the baseline clean_transcript function.

These tests are fully deterministic and require no audio, models,
network access, or external dependencies.
"""
import sys
import os
import copy

# Add project root to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from member2_intelligence.preprocessing.preprocessor import (
    clean_transcript,
    preprocess_transcript,
)


# ── Fixtures ──────────────────────────────────────────────────────────

def _make_transcript(segments=None):
    """Helper to build a valid Member 1 transcript dict."""
    if segments is None:
        segments = [
            {
                "id": 1,
                "speaker": "SPEAKER_00",
                "start": 0.0,
                "end": 5.5,
                "raw_text": "Um, so I think we should, uh, start the meeting.",
                "cleaned_text": "",
                "text": "Um, so I think we should, uh, start the meeting.",
                "overlap": False,
            },
            {
                "id": 2,
                "speaker": "SPEAKER_01",
                "start": 6.0,
                "end": 12.3,
                "raw_text": "Yeah, like, the budget report is, hmm, not ready yet.",
                "cleaned_text": "",
                "text": "Yeah, like, the budget report is, hmm, not ready yet.",
                "overlap": False,
            },
            {
                "id": 3,
                "speaker": "SPEAKER_00",
                "start": 13.0,
                "end": 18.0,
                "raw_text": "Alright. Let's move on to the next topic.",
                "cleaned_text": "",
                "text": "Alright. Let's move on to the next topic.",
                "overlap": False,
            },
        ]
    return {
        "meeting_id": "test_001",
        "language": "en",
        "segments": segments,
    }


# ── Tests: baseline clean_transcript ──────────────────────────────────

def test_clean_transcript_removes_fillers():
    raw = "Um, so the meeting is like starting now."
    result = clean_transcript(raw)
    assert "um" not in result.lower()
    assert "like" not in result.lower()
    print("  PASS: fillers removed")


def test_clean_transcript_normalizes_spacing():
    raw = "Hello   world ,  how  are   you ?"
    result = clean_transcript(raw)
    assert "  " not in result  # no double spaces
    print("  PASS: spacing normalized")


# ── Tests: preprocess_transcript ──────────────────────────────────────

def test_raw_text_is_unchanged():
    """raw_text is the evidence source and must never be modified."""
    transcript = _make_transcript()
    original_raw_texts = [seg["raw_text"] for seg in transcript["segments"]]

    processed = preprocess_transcript(transcript)

    for i, seg in enumerate(processed["segments"]):
        assert seg["raw_text"] == original_raw_texts[i], \
            f"FAIL: raw_text changed for segment {seg['id']}"
    print("  PASS: raw_text unchanged for all segments")


def test_speaker_is_unchanged():
    transcript = _make_transcript()
    original_speakers = [seg["speaker"] for seg in transcript["segments"]]

    processed = preprocess_transcript(transcript)

    for i, seg in enumerate(processed["segments"]):
        assert seg["speaker"] == original_speakers[i], \
            f"FAIL: speaker changed for segment {seg['id']}"
    print("  PASS: speaker unchanged for all segments")


def test_timestamps_are_unchanged():
    transcript = _make_transcript()
    original_starts = [seg["start"] for seg in transcript["segments"]]
    original_ends = [seg["end"] for seg in transcript["segments"]]

    processed = preprocess_transcript(transcript)

    for i, seg in enumerate(processed["segments"]):
        assert seg["start"] == original_starts[i], \
            f"FAIL: start changed for segment {seg['id']}"
        assert seg["end"] == original_ends[i], \
            f"FAIL: end changed for segment {seg['id']}"
    print("  PASS: timestamps unchanged for all segments")


def test_cleaned_text_is_populated():
    """cleaned_text must be a non-empty string after preprocessing."""
    transcript = _make_transcript()

    processed = preprocess_transcript(transcript)

    for seg in processed["segments"]:
        assert isinstance(seg["cleaned_text"], str), \
            f"FAIL: cleaned_text is not a string for segment {seg['id']}"
        assert len(seg["cleaned_text"]) > 0, \
            f"FAIL: cleaned_text is empty for segment {seg['id']}"
    print("  PASS: cleaned_text populated for all segments")


def test_segment_count_is_unchanged():
    transcript = _make_transcript()
    original_count = len(transcript["segments"])

    processed = preprocess_transcript(transcript)

    assert len(processed["segments"]) == original_count, \
        f"FAIL: segment count changed from {original_count} to {len(processed['segments'])}"
    print("  PASS: segment count unchanged")


def test_segment_ids_are_unchanged():
    transcript = _make_transcript()
    original_ids = [seg["id"] for seg in transcript["segments"]]

    processed = preprocess_transcript(transcript)

    result_ids = [seg["id"] for seg in processed["segments"]]
    assert result_ids == original_ids, \
        f"FAIL: segment IDs changed from {original_ids} to {result_ids}"
    print("  PASS: segment IDs unchanged")


def test_original_transcript_not_mutated():
    """preprocess_transcript must not mutate the input dict."""
    transcript = _make_transcript()
    original = copy.deepcopy(transcript)

    preprocess_transcript(transcript)

    assert transcript == original, "FAIL: original transcript was mutated!"
    print("  PASS: original transcript not mutated")


def test_top_level_fields_preserved():
    transcript = _make_transcript()

    processed = preprocess_transcript(transcript)

    assert processed["meeting_id"] == transcript["meeting_id"]
    assert processed["language"] == transcript["language"]
    assert "segments" in processed
    print("  PASS: meeting_id, language, segments preserved")


def test_empty_segments_list():
    """An empty segments list should be handled without error."""
    transcript = _make_transcript(segments=[])

    processed = preprocess_transcript(transcript)

    assert processed["segments"] == []
    print("  PASS: empty segments list handled")


def test_single_segment():
    """A transcript with one segment should work correctly."""
    single_seg = [{
        "id": 1,
        "speaker": "SPEAKER_00",
        "start": 0.0,
        "end": 3.0,
        "raw_text": "Uh, hello everyone.",
        "cleaned_text": "",
        "text": "Uh, hello everyone.",
        "overlap": False,
    }]
    transcript = _make_transcript(segments=single_seg)

    processed = preprocess_transcript(transcript)

    assert len(processed["segments"]) == 1
    assert processed["segments"][0]["raw_text"] == "Uh, hello everyone."
    assert len(processed["segments"][0]["cleaned_text"]) > 0
    print("  PASS: single-segment transcript handled")


def test_overlap_field_preserved():
    transcript = _make_transcript()

    processed = preprocess_transcript(transcript)

    for seg in processed["segments"]:
        assert seg["overlap"] == False, \
            f"FAIL: overlap changed for segment {seg['id']}"
    print("  PASS: overlap field preserved")


def test_missing_top_level_field_raises():
    """Missing required top-level fields must raise ValueError."""
    for missing_field in ["meeting_id", "language", "segments"]:
        transcript = _make_transcript()
        del transcript[missing_field]
        try:
            preprocess_transcript(transcript)
            print(f"  FAIL: no error for missing '{missing_field}'")
            return
        except ValueError:
            pass  # expected
    print("  PASS: missing top-level fields raise ValueError")


def test_missing_segment_field_raises():
    """Missing required segment fields must raise ValueError."""
    for missing_field in ["id", "speaker", "start", "end", "raw_text", "text"]:
        seg = {
            "id": 1, "speaker": "SPEAKER_00", "start": 0.0,
            "end": 3.0, "raw_text": "Hello.", "cleaned_text": "",
            "text": "Hello.", "overlap": False,
        }
        del seg[missing_field]
        transcript = _make_transcript(segments=[seg])
        try:
            preprocess_transcript(transcript)
            print(f"  FAIL: no error for missing segment field '{missing_field}'")
            return
        except ValueError:
            pass  # expected
    print("  PASS: missing segment fields raise ValueError")


# ── Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Running Member 2 Preprocessing Tests")
    print("=" * 60)

    print("\n--- Baseline clean_transcript ---")
    test_clean_transcript_removes_fillers()
    test_clean_transcript_normalizes_spacing()

    print("\n--- preprocess_transcript: Evidence Preservation ---")
    test_raw_text_is_unchanged()
    test_speaker_is_unchanged()
    test_timestamps_are_unchanged()
    test_cleaned_text_is_populated()
    test_segment_count_is_unchanged()
    test_segment_ids_are_unchanged()
    test_original_transcript_not_mutated()
    test_top_level_fields_preserved()
    test_overlap_field_preserved()

    print("\n--- preprocess_transcript: Edge Cases ---")
    test_empty_segments_list()
    test_single_segment()

    print("\n--- preprocess_transcript: Validation ---")
    test_missing_top_level_field_raises()
    test_missing_segment_field_raises()

    print("\n" + "=" * 60)
    print("[OK] ALL TESTS PASSED")
    print("=" * 60)
