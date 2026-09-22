# Member 1 Interface Specification

> **Version:** 1.0  
> **Date:** 2026-09-22  
> **Status:** CURRENT — describes the actual implemented output  
> **Source of truth:** [`member1_speech/main.py`](file:///c:/Users/Hp/Downloads/FYP/member1_speech/main.py)

---

## 1. Overview

Member 1's pipeline processes raw meeting audio and produces a structured JSON transcript file. This JSON is the **sole interface** between Member 1 and Member 2.

**Pipeline:**
```
Audio → Faster-Whisper ASR → PyAnnote Diarization → Alignment/Merge → Structured JSON
```

**Output location:** `data/mock_transcripts/{audio_filename}_transcript.json`

---

## 2. JSON Schema — Top Level

```json
{
  "meeting_id": "<string>",
  "language": "<string>",
  "segments": [ <Segment>, ... ]
}
```

| Field | Type | Description | Source |
|---|---|---|---|
| `meeting_id` | `string` | Derived from the audio filename by stripping the file extension. Example: `"sample2"` from `"sample2.mp3"`. | `audio_filename.split('.')[0]` in `main.py` line 38 |
| `language` | `string` | ISO 639-1 language code detected by Faster-Whisper. Example: `"en"`. | `info.language` from `transcriber.py` |
| `segments` | `array<Segment>` | Ordered list of speaker-attributed transcript segments. Sorted by chronological order (ascending `start` time). | Constructed in `main.py` lines 43–53 |

---

## 3. JSON Schema — Segment Object

```json
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
```

| Field | Type | Description | Current Status |
|---|---|---|---|
| `id` | `integer` | 1-indexed sequential segment identifier. Assigned during formatting in `main.py`. | **CURRENT** — always present, always sequential starting at 1 |
| `speaker` | `string` | Speaker label assigned by PyAnnote diarization. Format: `"SPEAKER_XX"` where `XX` is a zero-padded integer (e.g., `"SPEAKER_00"`, `"SPEAKER_04"`). | **CURRENT** — see Speaker Semantics below |
| `start` | `float` | Segment start time in **seconds from the beginning of the audio file**. Precision: typically 2 decimal places (centisecond resolution from PyAnnote). | **CURRENT** — always present |
| `end` | `float` | Segment end time in **seconds from the beginning of the audio file**. Same precision as `start`. Guaranteed: `end >= start`. | **CURRENT** — always present |
| `raw_text` | `string` | The aligned and merged text from Faster-Whisper for this segment. | **CURRENT** — see Text Field Semantics below |
| `cleaned_text` | `string` | **Placeholder.** Currently always set to `""` (empty string). | **CURRENT** — always empty string. See notes below |
| `text` | `string` | Currently identical to `raw_text`. | **CURRENT** — see Text Field Semantics below |
| `overlap` | `boolean` | **Placeholder.** Currently always set to `false`. | **CURRENT** — always `false`. See notes below |

---

## 4. Timestamp Semantics

- **Unit:** Seconds from the start of the audio file.
- **Type:** `float` (IEEE 754 double-precision).
- **Resolution:** Typically centisecond (2 decimal places), originating from PyAnnote's `round(turn.start, 2)` and Whisper's segment timestamps.
- **Monotonicity:** Segments are ordered by ascending `start` time. There is no guarantee that `segments[n].end < segments[n+1].start` — gaps between segments are expected (silence or unattributed audio), and in some cases adjacent segments may have the same `start`/`end` boundary (e.g., segment 3 ends at `23.88` and segment 4 starts at `23.88` in the real output).
- **Alignment note:** Timestamps originate from Whisper's word-level timestamps, then aggregated by the aligner's max-overlap speaker assignment against PyAnnote intervals.

---

## 5. Speaker Semantics

- **Format:** `"SPEAKER_XX"` — an arbitrary label assigned by PyAnnote's diarization model.
- **Consistency within a meeting:** The same physical speaker will generally receive the same label within a single audio file.
- **Inconsistency across meetings:** Speaker labels are **not** stable across different audio files. `SPEAKER_00` in one meeting is unrelated to `SPEAKER_00` in another.
- **No real names:** Labels are anonymous identifiers. No speaker name resolution or mapping is currently implemented.
- **Numbering is not sequential:** PyAnnote may assign non-contiguous labels (e.g., `SPEAKER_00`, `SPEAKER_02`, `SPEAKER_04` without `SPEAKER_01` or `SPEAKER_03`). The numeric portion has no semantic meaning.
- **`"UNKNOWN_SPEAKER"`:** If the aligner cannot match a text segment to any diarization interval (zero overlap with all intervals), the speaker is set to `"UNKNOWN_SPEAKER"`. This is a fallback in `aligner.py`.

---

## 6. Text Field Semantics — `raw_text` vs `text` vs `cleaned_text`

### Current Implementation Reality

| Field | Current Value | Intended Purpose |
|---|---|---|
| `raw_text` | `block["text"]` from aligner | The original transcribed text as produced by Whisper + alignment. Contains filler words, ASR artifacts, etc. |
| `text` | `block["text"]` from aligner | **Currently identical to `raw_text`.** Intended as the "best available" text for display and processing. |
| `cleaned_text` | `""` (empty string) | **Placeholder.** Intended to hold the preprocessed/cleaned version of the text after filler removal and normalization. |

### Important Notes

1. **`raw_text` and `text` are currently always identical.** Both are set to `block["text"]` in `main.py` lines 49 and 51. There is no current logic that differentiates them.
2. **`cleaned_text` is never populated by Member 1.** The comment in `main.py` line 50 says: `"Blank placeholder for Member 2 to fill"`. The intent is for Member 2's preprocessing to populate this field, but **this does not currently happen**.
3. **In the Streamlit app (`app.py`)**, Member 2's `clean_transcript()` operates on the **full concatenated `raw_text`** from Whisper, not on individual segment texts. The structured JSON fields are not used by Member 2's current code.

---

## 7. The `overlap` Field

- **Current value:** Always `false`.
- **Current implementation:** Hardcoded as `False` in `main.py` line 52 with the comment: `"Placeholder for future overlap detection"`.
- **Intended meaning [PLANNED]:** Whether this segment's time range overlaps with another speaker's segment, indicating simultaneous speech.
- **No overlap detection logic exists** in any current code.

---

## 8. Example — Real Pipeline Output

From [`data/mock_transcripts/sample2.mp3_transcript.json`](file:///c:/Users/Hp/Downloads/FYP/data/mock_transcripts/sample2.mp3_transcript.json):

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
            "raw_text": "Come in. Sit down. Sarah, look at me. You look exhausted. Tell me what's going on.",
            "cleaned_text": "",
            "text": "Come in. Sit down. Sarah, look at me. You look exhausted. Tell me what's going on.",
            "overlap": false
        },
        {
            "id": 2,
            "speaker": "SPEAKER_00",
            "start": 9.51,
            "end": 16.7,
            "raw_text": "Doctor, I can't sleep. The fever won't break. Every breath hurts.",
            "cleaned_text": "",
            "text": "Doctor, I can't sleep. The fever won't break. Every breath hurts.",
            "overlap": false
        },
        {
            "id": 3,
            "speaker": "SPEAKER_03",
            "start": 17.96,
            "end": 23.88,
            "raw_text": "She's been coughing until she can't breathe. She kept saying it was nothing. Look at her. It is not nothing.",
            "cleaned_text": "",
            "text": "She's been coughing until she can't breathe. She kept saying it was nothing. Look at her. It is not nothing.",
            "overlap": false
        }
    ]
}
```

---

## 9. What Member 2 Is Allowed to Assume

| Assumption | Guaranteed? |
|---|---|
| Top-level `meeting_id`, `language`, and `segments` fields always exist | ✅ Yes |
| `segments` is a non-empty array (at least 1 segment) | ✅ Yes (if audio contains speech) |
| Every segment has all 8 fields (`id`, `speaker`, `start`, `end`, `raw_text`, `cleaned_text`, `text`, `overlap`) | ✅ Yes |
| `id` values are sequential integers starting from 1 | ✅ Yes |
| `segments` are ordered by ascending `start` time | ✅ Yes |
| `start` and `end` are non-negative floats | ✅ Yes |
| `end >= start` for every segment | ✅ Yes |
| `speaker` is a non-empty string | ✅ Yes |
| `raw_text` and `text` are non-empty strings | ✅ Yes (Whisper always produces text for detected speech) |
| `language` is an ISO 639-1 code | ✅ Yes |
| `cleaned_text` is a string (currently always `""`) | ✅ Yes |
| `overlap` is a boolean (currently always `false`) | ✅ Yes |

---

## 10. What Member 2 Must NOT Assume

| Do NOT Assume | Reason |
|---|---|
| Speaker labels are stable across different audio files | PyAnnote assigns arbitrary labels per run |
| Speaker labels are sequential (0, 1, 2...) | PyAnnote may skip numbers |
| `SPEAKER_00` is always the first speaker in the meeting | Label assignment is not ordered by first appearance |
| `raw_text` is grammatically correct or clean | Whisper ASR output contains filler words and artifacts |
| `raw_text` and `text` are different | They are currently identical; this may change in the future |
| `cleaned_text` contains useful data | It is currently always `""` |
| `overlap` is meaningful | It is currently always `false` |
| Segment timestamps have no gaps | Silence between segments is expected |
| Segments never share a boundary timestamp | Adjacent segments may have matching `start`/`end` values |
| The number of unique speakers is known or bounded | It depends on PyAnnote's detection |
| The JSON file will always be on disk | In the Streamlit app, the data flows in-memory without file I/O |
