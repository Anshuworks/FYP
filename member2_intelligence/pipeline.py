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

import time
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

from member2_intelligence.intelligence.evidence_retriever import (
    retrieve_evidence,
)

from member2_intelligence.intelligence.evidence_verifier import (
    verify_claim,
)


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
        {
            meeting_id,
            language,
            segments[
                {
                    id,
                    speaker,
                    start,
                    end,
                    raw_text,
                    cleaned_text,
                    text,
                    overlap
                }
            ]
        }
    """

    structured = {
        "meeting_id": (
            audio_filename.split(".")[0]
            if "." in audio_filename
            else audio_filename
        ),
        "language": language,
        "segments": [],
    }

    for idx, block in enumerate(aligned_transcript, start=1):
        structured["segments"].append(
            {
                "id": idx,
                "speaker": block["speaker"],
                "start": block["start"],
                "end": block["end"],
                "raw_text": block["text"],
                "cleaned_text": "",
                "text": block["text"],
                "overlap": False,
            }
        )

    return structured


def _get_query_text(item: Any) -> str:
    """
    Extracts the natural-language text to use as a retrieval query
    from an intelligence item.

    Supported item types:
        Claim
        Decision
        ActionItem
        Topic
        Contradiction
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

    For each item:
        1. Extract its text as a retrieval query.
        2. Retrieve candidate transcript evidence.
        3. Structurally verify the evidence.
        4. Check whether the evidence actually supports the item text
           using the existing deterministic lexical verifier.
        5. Attach only sufficiently supported evidence.

    The existing verify_claim() function performs both:
        - structural evidence verification
        - lexical support verification

    Evidence that does not meet the SUPPORTED threshold is not attached.

    Args:
        intelligence:
            MeetingIntelligence produced by Qwen extraction.

        transcript:
            Processed structured transcript.

        top_k:
            Maximum number of evidence candidates to retrieve per item.

    Returns:
        The same MeetingIntelligence object with verified evidence attached.
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

        # ---------------------------------------------------------------
        # Step 1: Retrieve candidate evidence
        # ---------------------------------------------------------------
        candidates = retrieve_evidence(
            transcript,
            query,
            top_k=top_k,
        )

        # If nothing was retrieved, leave evidence empty.
        if not candidates:
            item.evidence = []
            continue

        # ---------------------------------------------------------------
        # Step 2: Reuse the existing Claim verifier as a generic
        # text-vs-evidence support checker.
        #
        # The verifier itself first performs structural verification
        # and then computes lexical overlap.
        # ---------------------------------------------------------------
        verification_claim = Claim(
            id=f"verification_{item.id}",
            text=query,
            evidence=candidates,
        )

        verification = verify_claim(
            verification_claim,
            transcript,
        )

        # ---------------------------------------------------------------
        # Step 3: Attach only sufficiently supported evidence.
        #
        # SUPPORTED means:
        #     best lexical overlap >= 0.50
        #
        # PARTIALLY_SUPPORTED and UNSUPPORTED are not attached.
        # ---------------------------------------------------------------
        if verification.status == "SUPPORTED":
            item.evidence = verification.verified_evidence
        else:
            item.evidence = []

    return intelligence


def run_intelligence_pipeline(
    aligned_transcript: List[Dict[str, Any]],
    language: str,
    audio_filename: str,
    generate_fn: Optional[Callable[..., str]] = None,
    member1_timing: Optional[Dict[str, float]] = None,
    stage_callback: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """
    Runs the full Member 2 intelligence pipeline on Member 1's output.

    Stages:
        1. Build structured transcript from in-memory alignment data
        2. Per-segment preprocessing
        3. Extract concatenated cleaned text
        4. Baseline BART summarization
        5. Qwen intelligence extraction
        6. Evidence retrieval
        7. Evidence verification and attachment

    Args:
        aligned_transcript:
            The merged speaker blocks from align_and_merge().

        language:
            ISO 639-1 language code from Whisper.

        audio_filename:
            Original audio filename.

        generate_fn:
            Optional callable for LLM generation.
            Defaults to Qwen via Ollama.
            Useful for testing with a mock.

        member1_timing:
            Optional dictionary with timing from Member 1 stages:
            {"transcription": float, "diarization": float, "alignment": float}.

        stage_callback:
            Optional callback invoked after each stage completes:
            callback(stage_name, duration_seconds).

    Returns:
        A dictionary containing:

        transcript:
            Fully processed structured transcript.

        cleaned_text:
            Concatenated cleaned text.

        summary:
            Baseline BART summary.

        intelligence:
            MeetingIntelligence with verified evidence attached.

        intelligence_error:
            Error message if Qwen extraction fails,
            otherwise None.

        timing:
            Dictionary containing elapsed durations (in seconds) for each stage.
    """

    # ===============================================================
    # Stage 1: Build structured transcript
    # ===============================================================

    structured = build_structured_transcript(
        aligned_transcript,
        language,
        audio_filename,
    )

    # ===============================================================
    # Stage 2: Per-segment preprocessing & Stage 3: Cleaned text
    # ===============================================================

    t_start_preproc = time.perf_counter()
    processed = preprocess_transcript(structured)

    cleaned_text = " ".join(
        seg["cleaned_text"]
        for seg in processed["segments"]
        if seg["cleaned_text"]
    )
    t_preprocessing = time.perf_counter() - t_start_preproc

    if stage_callback:
        stage_callback("preprocessing", round(t_preprocessing, 2))

    # ===============================================================
    # Stage 4: Baseline BART summarization
    #
    # IMPORTANT:
    # BART remains unchanged and is preserved as our baseline.
    # ===============================================================

    t_start_bart = time.perf_counter()
    summary_text = (
        generate_summary(cleaned_text)
        if cleaned_text
        else ""
    )
    t_bart = time.perf_counter() - t_start_bart

    if stage_callback:
        stage_callback("bart_summary", round(t_bart, 2))

    # ===============================================================
    # Stage 5: Qwen intelligence extraction
    #           + evidence retrieval
    #           + evidence verification
    # ===============================================================

    intelligence = MeetingIntelligence()
    intelligence_error = None
    t_qwen = 0.0
    t_evidence = 0.0

    if processed.get("segments"):
        try:
            # -------------------------------------------------------
            # 5A. Extract claims, decisions, action items,
            #     topics and contradictions using Qwen.
            #
            # Qwen initially produces empty evidence lists.
            # -------------------------------------------------------

            t_start_qwen = time.perf_counter()
            intelligence = extract_intelligence(
                processed,
                generate_fn=generate_fn,
            )
            t_qwen = time.perf_counter() - t_start_qwen

            if stage_callback:
                stage_callback("qwen_extraction", round(t_qwen, 2))

            # -------------------------------------------------------
            # 5B. Retrieve and verify real transcript evidence.
            # -------------------------------------------------------

            t_start_evidence = time.perf_counter()
            attach_evidence(
                intelligence,
                processed,
            )
            t_evidence = time.perf_counter() - t_start_evidence

            if stage_callback:
                stage_callback("evidence", round(t_evidence, 2))

        except (ExtractionError, Exception) as e:
            if t_qwen == 0.0:
                t_qwen = time.perf_counter() - t_start_qwen
            intelligence_error = (
                f"Intelligence extraction failed: {e}"
            )

            intelligence = MeetingIntelligence()

    # ===============================================================
    # Stage Timing Compilation
    # ===============================================================

    timing: Dict[str, float] = {}

    if member1_timing:
        for k in ("transcription", "diarization", "alignment"):
            if k in member1_timing:
                timing[k] = round(member1_timing[k], 2)

    timing["preprocessing"] = round(t_preprocessing, 2)
    timing["bart_summary"] = round(t_bart, 2)
    timing["qwen_extraction"] = round(t_qwen, 2)
    timing["evidence"] = round(t_evidence, 2)
    timing["total"] = round(sum(timing.values()), 2)

    # ===============================================================
    # Final pipeline result
    # ===============================================================

    return {
        "transcript": processed,
        "cleaned_text": cleaned_text,
        "summary": summary_text,
        "intelligence": intelligence,
        "intelligence_error": intelligence_error,
        "timing": timing,
    }