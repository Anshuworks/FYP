# Evidence-Meet

## Evidence-Based Meeting Summarization

Evidence-Meet is a final-year research and software engineering project focused on building a **privacy-preserving, speaker-aware, evidence-grounded meeting intelligence system**.

The goal is not to build another ordinary meeting transcription or summarization tool.

The system is designed to transform a meeting recording into structured and trustworthy meeting knowledge while maintaining a traceable connection between generated information and the original meeting evidence.

Every important generated decision, action item, claim, or summary statement should ideally be traceable back to the relevant portion of the meeting transcript, including the speaker and timestamp whenever available.

---

# 1. Project Vision

Modern meeting tools can already transcribe meetings and generate summaries.

The central problem addressed by Evidence-Meet is therefore not simply:

> "Can we summarize a meeting?"

Instead, the project asks:

> **"Can we generate useful meeting intelligence while preserving a reliable connection between the generated information and the evidence contained in the original meeting?"**

The system should therefore prioritize:

- Evidence grounding
- Traceability
- Speaker awareness
- Timestamp awareness
- Reduced hallucination
- Structured meeting intelligence
- Privacy
- Local/edge-friendly processing where practical
- Reproducible evaluation

The intended output should allow a user to move from:

**Summary → Claim/Decision/Action → Evidence → Speaker → Timestamp → Transcript**

rather than receiving an unsupported black-box summary.

---

# 2. Core Problem

A conventional meeting summarization pipeline can be represented as:

    Meeting Audio
          |
          v
      Transcript
          |
          v
      LLM Summary

This approach can produce fluent summaries, but fluency does not guarantee factual faithfulness.

Potential problems include:

- Hallucinated information
- Incorrect attribution of statements to speakers
- Missing decisions
- Missing action items
- Incorrect deadlines
- Loss of important context
- Unsupported claims
- Difficulty verifying where a statement originated
- Lack of transparency in generated summaries

Evidence-Meet is designed to introduce an explicit evidence-oriented layer into the pipeline.

The intended conceptual pipeline is:

    Meeting Audio / Video
             |
             v
      Speech Processing
             |
             v
   Speaker-Aware Transcript
             |
             v
     Transcript Processing
             |
             v
      Meeting Intelligence
             |
             v
      Candidate Claims /
      Decisions / Actions /
      Topics / Other Events
             |
             v
       Evidence Retrieval
             |
             v
     Evidence Verification
             |
             v
      Structured Knowledge
             |
             v
       Evidence-Grounded
          Summary
             |
             v
       Search / UI / Export


---

# 3. Main Objectives

The project has the following major objectives.

## 3.1 Speaker-Aware Transcription

Convert meeting audio into a timestamped transcript while preserving speaker information.

The transcript should ideally contain:

- Speaker identity/label
- Start timestamp
- End timestamp
- Spoken text
- Relevant confidence/metadata where available

Example:

```json
{
  "speaker": "SPEAKER_01",
  "start": 42.15,
  "end": 48.72,
  "text": "We should complete the prototype by Friday."
}