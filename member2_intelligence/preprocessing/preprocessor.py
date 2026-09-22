import re
import copy
from typing import Dict, List, Any


def clean_transcript(text: str) -> str:
    """
    [BASELINE] Cleans raw transcript text by removing filler words,
    fixing spacing, and normalizing characters.

    This is the original baseline cleaning function.
    It operates on a single flat string and returns a cleaned string.

    Args:
        text: Raw transcript text to clean.

    Returns:
        Cleaned text with fillers removed, spacing normalized,
        and sentences capitalized.
    """
    fillers = [r'\bum\b', r'\buh\b', r'\behr\b', r'\bhmm\b', r'\blike\b']
    cleaned_text = text
    for filler in fillers:
        cleaned_text = re.sub(filler, '', cleaned_text, flags=re.IGNORECASE)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s([?.!,])', r'\1', cleaned_text)
    cleaned_text = '. '.join([s.strip().capitalize() for s in cleaned_text.split('.') if s.strip()])

    return cleaned_text + "."


def preprocess_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies per-segment preprocessing to a structured Member 1 transcript.

    For each segment, populates the 'cleaned_text' field using the baseline
    clean_transcript() function applied to 'raw_text'. All other fields
    (id, speaker, start, end, raw_text, text, overlap) are preserved exactly.

    This function preserves evidence traceability: raw_text is never modified,
    and all segment metadata (speaker, timestamps, IDs) is carried through
    unchanged.

    Args:
        transcript: The complete Member 1 structured transcript dictionary
                    containing 'meeting_id', 'language', and 'segments'.

    Returns:
        A new transcript dictionary (deep copy) with 'cleaned_text' populated
        for every segment. The original input is not mutated.

    Raises:
        ValueError: If transcript is missing required top-level fields
                    ('meeting_id', 'language', 'segments').
        ValueError: If any segment is missing required fields
                    ('id', 'speaker', 'start', 'end', 'raw_text', 'text').
    """
    # Validate top-level structure
    required_top_fields = ["meeting_id", "language", "segments"]
    for field in required_top_fields:
        if field not in transcript:
            raise ValueError(f"Transcript missing required field: '{field}'")

    # Deep copy to avoid mutating the original
    result = copy.deepcopy(transcript)

    # Validate and process each segment
    required_segment_fields = ["id", "speaker", "start", "end", "raw_text", "text"]
    for segment in result["segments"]:
        for field in required_segment_fields:
            if field not in segment:
                raise ValueError(
                    f"Segment missing required field: '{field}'. "
                    f"Segment data: {segment}"
                )

        # Apply baseline cleaning to raw_text → cleaned_text
        segment["cleaned_text"] = clean_transcript(segment["raw_text"])

    return result


# --- Integration Test ---
if __name__ == "__main__":
    # Test 1: Baseline clean_transcript (preserved behavior)
    print("=== Test 1: Baseline clean_transcript ===")
    raw_input = "Um, so the meeting is like starting now... uh, we should, uh, talk about the budget."
    result = clean_transcript(raw_input)
    print("Raw: ", raw_input)
    print("Cleaned: ", result)

    # Test 2: Structured per-segment preprocessing
    print("\n=== Test 2: preprocess_transcript ===")
    mock_transcript = {
        "meeting_id": "test_001",
        "language": "en",
        "segments": [
            {
                "id": 1,
                "speaker": "SPEAKER_00",
                "start": 0.0,
                "end": 5.5,
                "raw_text": "Um, so I think we should, uh, start the meeting.",
                "cleaned_text": "",
                "text": "Um, so I think we should, uh, start the meeting.",
                "overlap": False
            },
            {
                "id": 2,
                "speaker": "SPEAKER_01",
                "start": 6.0,
                "end": 12.3,
                "raw_text": "Yeah, like, the budget report is, hmm, not ready yet.",
                "cleaned_text": "",
                "text": "Yeah, like, the budget report is, hmm, not ready yet.",
                "overlap": False
            }
        ]
    }

    processed = preprocess_transcript(mock_transcript)

    for seg in processed["segments"]:
        print(f"\n  Segment {seg['id']} ({seg['speaker']}):")
        print(f"    raw_text:     {seg['raw_text']}")
        print(f"    cleaned_text: {seg['cleaned_text']}")
        print(f"    start/end:    {seg['start']}s - {seg['end']}s")

    # Verify original was not mutated
    assert mock_transcript["segments"][0]["cleaned_text"] == "", \
        "FAIL: Original transcript was mutated!"
    print("\n[OK] Original transcript was NOT mutated.")