"""
Member 2 Intelligence Pipeline

Orchestrates the Member 2 processing stages:
  Stage 1: Build structured transcript from Member 1 alignment data
  Stage 2: Per-segment preprocessing (preprocess_transcript)
  Stage 3: Extract concatenated cleaned text
  Stage 4: Baseline BART summarization (generate_summary)
  Stage 5: Qwen intelligence extraction + evidence retrieval + verification

This module bridges Member 1's structured transcript output and
Member 2's intelligence components. It constructs the contract-compliant
structured transcript from Member 1's in-memory outputs, then runs
each processing stage in order.

The structured transcript is the official input boundary for Member 2.
All intelligence stages receive and preserve the full segment structure
(id, speaker, start, end, raw_text, cleaned_text, text, overlap).
"""
import traceback
from typing import Dict, List, Any, Optional, Callable

from member2_intelligence.preprocessing.preprocessor import preprocess_transcript
from member2_intelligence.llm.summarizer import generate_summary
from member2_intelligence.intelligence.schemas import (
    MeetingIntelligence,
    Claim,
    Decision,
    ActionItem,
    Topic,
    Contradiction,
    Evidence,
)
from member2_intelligence.intelligence.extractor import (
    extract_intelligence,
    ExtractionError,
)
from member2_intelligence.intelligence.evidence_retriever import retrieve_evidence
from member2_intelligence.intelligence.evidence_verifier import verify_evidence


def build_structured_transcript(
    aligned_transcript: List[Dict[str, Any]],
    language: str,
    audio_filename: str,
) -> Dict[str, Any]:
    """
    Builds a contract-compliant structured transcript dictionary from
    Member 1's in-memory alignment output.

    This replicates the same JSON structure that member1_speech/main.py
    writes to disk, so that Member 2 always receives a consistent format
    regardless of whether the pipeline runs via CLI or Streamlit.

    Args:
        aligned_transcript: The merged speaker blocks from align_and_merge().
            Each block has keys: 'speaker', 'start', 'end', 'text'.
        language: ISO 639-1 language code detected by Whisper (e.g. 'en').
        audio_filename: Original audio filename (used to derive meeting_id).

    Returns:
        A structured transcript dict matching the Member 1 contract:
        {meeting_id, language, segments[{id, speaker, start, end,
         raw_text, cleaned_text, text, overlap}]}
    """
    structured = {
        "meeting_id": audio_filename.split('.')[0] if '.' in audio_filename else audio_filename,
        "language": language,
        "segments": [],
    }

    for idx, block in enumerate(aligned_transcript, start=1):
        structured["segments"].append({
            "id": idx,
            "speaker": block["speaker"],
            "start": block["start"],
            "end": block["end"],
            "raw_text": block["text"],
            "cleaned_text": "",        # Placeholder — filled by preprocess_transcript
            "text": block["text"],
            "overlap": False,          # Placeholder — future overlap detection
        })

    return structured


def _get_query_text(item: Any) -> str:
    """
    Extracts the natural-language text to use as a retrieval query
    from an intelligence item (Claim, Decision, ActionItem, Topic,
    or Contradiction).
    """
    if isinstance(item, Claim):
        return item.text
    elif isinstance(item, Decision):
        return item.text
    elif isinstance(item, ActionItem):
        return item.task
    elif isinstance(item, Topic):
        return item.name
    elif isinstance(item, Contradiction):
        return item.description
    return ""


def attach_evidence(
    intelligence: MeetingIntelligence,
    transcript: Dict[str, Any],
    top_k: int = 3,
) -> MeetingIntelligence:
    """
    Attaches verified evidence from the transcript to each intelligence item.

    For each item (claim, decision, action item, topic, contradiction):
      1. Uses its text/description/task/name as a retrieval query.
      2. Calls retrieve_evidence() to find matching transcript segments.
      3. Verifies each candidate with verify_evidence().
      4. Attaches only structurally verified Evidence objects.

    Evidence that fails verification is silently discarded — the item
    retains only verified evidence. If no evidence passes verification,
    the item's evidence list remains empty.

    This function mutates the intelligence object in place and also
    returns it for convenience.

    Args:
        intelligence: The MeetingIntelligence with empty evidence lists
                      (as returned by extract_intelligence).
        transcript:   The processed structured transcript dictionary.
        top_k:        Maximum number of evidence candidates to retrieve
                      per item. Defaults to 3.

    Returns:
        The same MeetingIntelligence object with evidence attached.
    """
    all_items: List[Any] = (
        intelligence.claims
        + intelligence.decisions
        + intelligence.action_items
        + intelligence.topics
        + intelligence.contradictions
    )

    for item in all_items:
        query = _get_query_text(item)
        if not query:
            continue

        # Retrieve candidate evidence from the transcript
        candidates = retrieve_evidence(transcript, query, top_k=top_k)

        # Attach only verified evidence
        verified = [ev for ev in candidates if verify_evidence(transcript, ev)]
        item.evidence = verified

    return intelligence


def run_intelligence_pipeline(
    aligned_transcript: List[Dict[str, Any]],
    language: str,
    audio_filename: str,
    generate_fn: Optional[Callable[..., str]] = None,
) -> Dict[str, Any]:
    """
    Runs the full Member 2 intelligence pipeline on Member 1's output.

    Stages:
      1. Build structured transcript from in-memory alignment data
      2. Per-segment preprocessing (populates cleaned_text)
      3. Extract concatenated cleaned text
      4. Baseline BART summarization (unchanged)
      5. Qwen intelligence extraction + evidence retrieval + verification

    Args:
        aligned_transcript: The merged speaker blocks from align_and_merge().
        language: ISO 639-1 language code from Whisper.
        audio_filename: Original audio filename.
        generate_fn: Optional callable for LLM generation. Defaults to
                     Qwen via Ollama. Useful for testing with a mock.

    Returns:
        A dict containing:
          - 'transcript': The fully processed structured transcript
                          (with cleaned_text populated per segment)
          - 'cleaned_text': Concatenated cleaned text from all segments
                            (for display and baseline summarization)
          - 'summary': The baseline BART summary string
          - 'intelligence': MeetingIntelligence with verified evidence
                            attached (or empty if extraction failed)
          - 'intelligence_error': Error message string if Qwen extraction
                                  failed, or None on success
    """
    # Stage 1: Build structured transcript matching the Member 1 contract
    structured = build_structured_transcript(
        aligned_transcript, language, audio_filename
    )

    # Stage 2: Per-segment preprocessing (fills cleaned_text, preserves evidence)
    processed = preprocess_transcript(structured)

    # Stage 3: Extract concatenated cleaned text for baseline summarizer
    cleaned_text = " ".join(
        seg["cleaned_text"] for seg in processed["segments"]
        if seg["cleaned_text"]
    )

    # Stage 4: Baseline BART summarization (unchanged)
    summary_text = generate_summary(cleaned_text) if cleaned_text else ""

    # Stage 5: Qwen intelligence extraction + evidence attachment
    intelligence = MeetingIntelligence()
    intelligence_error = None

    if processed.get("segments"):
        try:
            intelligence = extract_intelligence(
                processed, generate_fn=generate_fn
            )
            attach_evidence(intelligence, processed)
        except (ExtractionError, Exception) as e:
            intelligence_error = f"Intelligence extraction failed: {e}"
            intelligence = MeetingIntelligence()

    return {
        "transcript": processed,
        "cleaned_text": cleaned_text,
        "summary": summary_text,
        "intelligence": intelligence,
        "intelligence_error": intelligence_error,
    }

