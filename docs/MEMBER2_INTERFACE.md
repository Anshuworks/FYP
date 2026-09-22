# Member 2 Interface Specification

> **Version:** 1.0  
> **Date:** 2026-09-22  
> **Status:** CURRENT baseline documented + PLANNED future stages  
> **Source of truth:**  
> - [`member2_intelligence/preprocessing/preprocessor.py`](file:///c:/Users/Hp/Downloads/FYP/member2_intelligence/preprocessing/preprocessor.py)  
> - [`member2_intelligence/llm/summarizer.py`](file:///c:/Users/Hp/Downloads/FYP/member2_intelligence/llm/summarizer.py)

---

## 1. Input — What Member 2 Currently Receives

### 1.1 Defined Input (Structured JSON)

Member 1 produces a structured JSON transcript (see [`MEMBER1_INTERFACE.md`](file:///c:/Users/Hp/Downloads/FYP/docs/MEMBER1_INTERFACE.md) for the full specification):

```json
{
  "meeting_id": "sample2",
  "language": "en",
  "segments": [
    {
      "id": 1,
      "speaker": "SPEAKER_04",
      "start": 0.0,
      "end": 8.55,
      "raw_text": "Come in. Sit down. Sarah, look at me.",
      "cleaned_text": "",
      "text": "Come in. Sit down. Sarah, look at me.",
      "overlap": false
    }
  ]
}
```

### 1.2 Actual Input Used (CURRENT DISCREPANCY)

> **[IMPORTANT]** In the current Streamlit app ([`app/app.py`](file:///c:/Users/Hp/Downloads/FYP/app/app.py) lines 89–93), Member 2 does **not** consume the structured JSON. Instead:
>
> - `clean_transcript()` receives `raw_text` — the **full concatenated text** from Whisper's `transcribe_audio()` return value.
> - `generate_summary()` receives the output of `clean_transcript()` — a single cleaned string.
>
> The per-segment structure with speaker labels, timestamps, and segment IDs is **not used** by any current Member 2 code.

This is a known gap that the future evidence-grounded pipeline will address.

---

## 2. Current Baseline — Preprocessing

**[CURRENT/BASELINE]**

**File:** [`member2_intelligence/preprocessing/preprocessor.py`](file:///c:/Users/Hp/Downloads/FYP/member2_intelligence/preprocessing/preprocessor.py)

**Function:** `clean_transcript(text: str) -> str`

**Input:** A single string of raw transcript text.

**Processing steps (in order):**

| Step | Operation | Implementation |
|---|---|---|
| 1 | Filler word removal | Removes `um`, `uh`, `ehr`, `hmm`, `like` using word-boundary regex (`\b`), case-insensitive |
| 2 | Whitespace normalization | Collapses multiple spaces into one (`\s+` → `' '`) |
| 3 | Punctuation spacing fix | Removes space before `? . ! ,` characters |
| 4 | Sentence capitalization | Splits on `.`, strips/capitalizes each sentence, rejoins with `. ` |
| 5 | Trailing period | Appends `.` to the result |

**Output:** A single cleaned string.

**Limitations:**
- Operates on flat text, not per-segment
- Destroys all speaker and timestamp information
- `like` is always removed, even when used grammatically (e.g., "I like this idea")
- Sentence splitting on `.` is fragile (e.g., "Dr. Smith" or "3.5 percent")

---

## 3. Current Baseline — BART Summarization

**[CURRENT/BASELINE]**

**File:** [`member2_intelligence/llm/summarizer.py`](file:///c:/Users/Hp/Downloads/FYP/member2_intelligence/llm/summarizer.py)

**Function:** `generate_summary(text: str) -> str`

**Model:** `facebook/bart-large-cnn`  
**Device:** CPU (`device=-1`)

**Strategy:**

| Text Length | Strategy | Parameters |
|---|---|---|
| ≤ 500 words | **Direct** — single-pass summarization | `max_length=130`, `min_length=40`, `do_sample=False`, `truncation=True` |
| > 500 words | **Map-Reduce** — chunk → summarize → combine → summarize | Chunk size: 450 words. Map: `max_length=80`, `min_length=25`. Reduce: `max_length=150`, `min_length=50` |

**Input:** A single cleaned text string (output of `clean_transcript()`).

**Output:** A single summary string (`str`).

**Limitations:**
- No awareness of speakers, timestamps, or segment boundaries
- Summary is not evidence-grounded — no traceability to source segments
- Model is re-instantiated on every call (no caching)
- No error handling for empty input or model loading failures
- BART has a 1024-token input limit per chunk; `truncation=True` silently drops excess tokens

> **This baseline summarizer must be preserved** as a reference and fallback throughout all future development.

---

## 4. Future Planned Intelligence Stages

**[PLANNED]** — None of the following are implemented. This section documents the intended architecture direction.

### 4.1 Planned Pipeline Stages

```
Structured JSON (from Member 1)
    │
    ▼
[Stage 1] Per-Segment Preprocessing
    │   Clean each segment's text individually, preserving segment boundaries
    ▼
[Stage 2] Claim Extraction
    │   Identify factual claims, opinions, and assertions per segment
    ▼
[Stage 3] Decision Detection
    │   Detect decisions made during the meeting
    ▼
[Stage 4] Action Item Extraction
    │   Extract assigned tasks, deadlines, responsibilities
    ▼
[Stage 5] Evidence Retrieval
    │   Link extracted items back to supporting transcript segments
    ▼
[Stage 6] Evidence Verification
    │   Validate that evidence actually supports the extracted information
    ▼
[Stage 7] Contradiction Detection
    │   Identify conflicting statements across speakers or time
    ▼
[Stage 8] Evidence-Grounded Summary
        Generate a summary where every claim is backed by transcript evidence
```

> **These stages are a design goal.** Their order, granularity, and implementation details are subject to change during development.

### 4.2 Planned Per-Segment Preprocessing

**[PLANNED]** — Preprocessing should evolve to operate per-segment rather than on flat text, so that segment boundaries, speakers, and timestamps are preserved for evidence retrieval.

---

## 5. Expected Future Outputs

**[PLANNED]** — The following output structures are design goals, not implemented code.

### 5.1 Evidence Object

Every piece of extracted intelligence (claim, decision, action item, etc.) must reference one or more **evidence objects** linking it back to the original transcript.

```json
{
  "segment_id": 4,
  "speaker": "SPEAKER_04",
  "start": 23.88,
  "end": 38.28,
  "quote": "Temperature is 38.5. Throats inflamed. This is influenza. Not a cold."
}
```

| Field | Type | Description |
|---|---|---|
| `segment_id` | `integer` | The `id` of the transcript segment that provides the evidence |
| `speaker` | `string` | The speaker from the source segment |
| `start` | `float` | Start timestamp of the source segment (seconds) |
| `end` | `float` | End timestamp of the source segment (seconds) |
| `quote` | `string` | The relevant portion of text from the segment that supports the claim |

### 5.2 Claim Object (Example)

```json
{
  "claim_id": 1,
  "type": "diagnosis",
  "text": "The patient has influenza, not a cold.",
  "confidence": 0.95,
  "evidence": [
    {
      "segment_id": 4,
      "speaker": "SPEAKER_04",
      "start": 23.88,
      "end": 38.28,
      "quote": "This is influenza. Not a cold."
    }
  ]
}
```

### 5.3 Action Item Object (Example)

```json
{
  "action_id": 1,
  "text": "Return to the doctor if fever hasn't broken by Thursday.",
  "assigned_to": "SPEAKER_01",
  "deadline": "Thursday",
  "evidence": [
    {
      "segment_id": 8,
      "speaker": "SPEAKER_05",
      "start": 60.25,
      "end": 65.83,
      "quote": "if that fever hasn't broken by Thursday, you come straight back to me."
    }
  ]
}
```

> **All of the above are PLANNED examples.** Field names, structure, and contents are subject to design review before implementation.

---

## 6. Evidence Object Requirements

**[PLANNED]** — Design requirements for all evidence objects in the future system:

1. **Mandatory traceability:** Every extracted intelligence item (claim, decision, action item, summary statement) must include at least one evidence object.
2. **Valid segment reference:** `segment_id` must reference an actual `id` in the source transcript JSON.
3. **Quote accuracy:** The `quote` text must be a substring of (or semantically equivalent to) the `text` or `raw_text` field of the referenced segment. Preferably an exact substring.
4. **Speaker consistency:** The `speaker` in the evidence must match the `speaker` of the referenced segment.
5. **Timestamp consistency:** `start` and `end` in the evidence must match the referenced segment's timestamps.
6. **Multiple evidence:** A single intelligence item may be supported by multiple evidence objects from different segments.
7. **No orphan claims:** Intelligence items without evidence objects are considered invalid.

---

## 7. Compatibility Principles

### 7.1 Backward Compatibility with Member 1

- Member 2 must accept any valid transcript JSON conforming to the schema in [`MEMBER1_INTERFACE.md`](file:///c:/Users/Hp/Downloads/FYP/docs/MEMBER1_INTERFACE.md).
- Member 2 must tolerate `cleaned_text` being `""` (empty string).
- Member 2 must tolerate `overlap` being `false` for all segments.
- Member 2 must tolerate `raw_text` and `text` being identical.
- Member 2 must handle meetings with any number of speakers (including 1).
- Member 2 must not fail on valid but short transcripts (e.g., a single segment).

### 7.2 Baseline Preservation

- The current BART summarizer (`generate_summary`) must remain functional and accessible throughout all development.
- New intelligence components should be **additive** — they supplement the baseline, not replace it.
- The baseline output should be available for comparison during evaluation.

### 7.3 Future Pipeline Integration

- Member 2's `pipeline.py` (currently empty) is reserved for orchestrating the full intelligence pipeline.
- Each intelligence stage should be an independent, testable module.
- The pipeline should support running individual stages or the full chain.
- All stages must preserve the original segment structure — no merging or destroying of Member 1's segments.

### 7.4 Interface Stability

- If Member 2 requires changes to Member 1's output schema, the request must go through the contract change process defined in [`PROJECT_CONTRACT.md`](file:///c:/Users/Hp/Downloads/FYP/docs/PROJECT_CONTRACT.md) Section 7.
- Member 2 must never modify Member 1's code or the Streamlit application without explicit agreement.
