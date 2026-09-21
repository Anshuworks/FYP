import os
import json

def get_optimal_speaker(segment_start, segment_end, diarization_intervals):
    """
    Finds the speaker whose diarization interval overlaps the most with the given text segment.
    """
    max_overlap = 0
    best_speaker = "UNKNOWN_SPEAKER"
    
    for interval in diarization_intervals:
        # Calculate how much the two timeframes overlap
        overlap = max(0, min(segment_end, interval["end"]) - max(segment_start, interval["start"]))
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_speaker = interval["speaker"]
            
    return best_speaker

def align_and_merge(transcript_segments, diarization_intervals):
    """
    Aligns text segments with speakers and merges contiguous speech by the same person.
    """
    if not transcript_segments:
        return []

    # Step 1: Tag every individual sentence with a speaker
    aligned_raw = []
    for seg in transcript_segments:
        speaker = get_optimal_speaker(seg["start"], seg["end"], diarization_intervals)
        aligned_raw.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": speaker,
            "text": seg["text"].strip()
        })

    # Step 2: Merge consecutive segments from the same speaker into clean blocks
    merged_blocks = []
    current_block = aligned_raw[0].copy()
    
    for next_seg in aligned_raw[1:]:
        # If the same person is still talking, merge the text and extend the end time
        if next_seg["speaker"] == current_block["speaker"]:
            current_block["end"] = next_seg["end"]
            current_block["text"] += " " + next_seg["text"]
        else:
            # Person changed! Save the block and start a new one
            merged_blocks.append(current_block)
            current_block = next_seg.copy()
            
    # Append the final block
    merged_blocks.append(current_block)
    
    return merged_blocks

# --- Integration Test ---
if __name__ == "__main__":
    # 1. Simulated output from PyAnnote (Notice the fragmentation)
    mock_diarization = [
        {"start": 0.0, "end": 2.5, "speaker": "SPEAKER_04"},
        {"start": 2.8, "end": 5.1, "speaker": "SPEAKER_04"}, # Same speaker, split by pause
        {"start": 5.5, "end": 8.0, "speaker": "SPEAKER_00"},
        {"start": 8.1, "end": 10.0, "speaker": "SPEAKER_00"}
    ]
    
    # 2. Simulated output from Faster-Whisper
    mock_whisper = [
        {"start": 0.5, "end": 2.3, "text": "Come in, sit down."},
        {"start": 3.0, "end": 5.0, "text": "You look exhausted."},
        {"start": 5.6, "end": 7.5, "text": "Doctor, I can't sleep."},
        {"start": 8.2, "end": 9.8, "text": "The fever won't break."}
    ]
    
    print("Aligning and merging data...\n")
    final_transcript = align_and_merge(mock_whisper, mock_diarization)
    
    # 3. Print the finalized, clean format
    for block in final_transcript:
        print(f"[{block['start']:05.2f}s - {block['end']:05.2f}s] {block['speaker']}: {block['text']}")
        
    # Optional: Save to JSON for Member 2's LLM
    os.makedirs("../../data/mock_transcripts", exist_ok=True)
    with open("../../data/mock_transcripts/final_output.json", "w") as f:
        json.dump(final_transcript, f, indent=4)