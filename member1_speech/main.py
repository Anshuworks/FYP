import os
import json
import time

# Import the three pillars of your pipeline
from asr.transcriber import transcribe_audio
from diarization.diarizer import diarize_audio
from alignment.aligner import align_and_merge

def run_pipeline(audio_filename, hf_token):
    # 1. Setup dynamic paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    audio_path = os.path.join(project_root, "data", "samples", audio_filename)
    output_dir = os.path.join(project_root, "data", "mock_transcripts")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"========== STARTING EVIDENCEMEET PIPELINE ==========")
    print(f"Processing Target: {audio_filename}")
    
    # 2. Step One: The Ears (Faster-Whisper)
    print("\n--- STEP 1: Transcribing Audio ---")
    t0 = time.perf_counter()
    # Unpacking all 3 returned values from your transcriber.py
    full_text, whisper_segments, language = transcribe_audio(audio_path)
    t_transcription = time.perf_counter() - t0
    print(f"Detected Language: {language}")
    print(f"Extracted {len(whisper_segments)} text segments in {t_transcription:.2f}s.")

    # 3. Step Two: The Clock (PyAnnote)
    print("\n--- STEP 2: Diarizing Speakers ---")
    t0 = time.perf_counter()
    diarization_intervals = diarize_audio(audio_path, hf_token)
    t_diarization = time.perf_counter() - t0
    print(f"Diarization completed in {t_diarization:.2f}s.")
    
    # 4. Step Three: The Brain (Aligner)
    print("\n--- STEP 3: Aligning & Merging ---")
    t0 = time.perf_counter()
    aligned_transcript = align_and_merge(whisper_segments, diarization_intervals)
    t_alignment = time.perf_counter() - t0
    print(f"✅ 3. Alignment Complete in {t_alignment:.2f}s")

    # 5. Format to match the drafted JSON schema
    formatted_json = {
        "meeting_id": audio_filename.split('.')[0], 
        "language": language,
        "segments": []
    }
    
    for idx, block in enumerate(aligned_transcript, start=1):
        formatted_json["segments"].append({
            "id": idx,
            "speaker": block["speaker"],
            "start": block["start"],
            "end": block["end"],
            "raw_text": block["text"], 
            "cleaned_text": "", # Blank placeholder for Member 2 to fill
            "text": block["text"],
            "overlap": False # Placeholder for future overlap detection
        })

    # 6. Save the final output for Member 2
    output_file = os.path.join(output_dir, f"{audio_filename}_transcript.json")
    with open(output_file, "w") as f:
        json.dump(formatted_json, f, indent=4)
        
    print(f"\n========== PIPELINE COMPLETE ==========")
    print(f"Saved highly structured transcript to: {output_file}")
    
    timing = {
        "transcription": round(t_transcription, 2),
        "diarization": round(t_diarization, 2),
        "alignment": round(t_alignment, 2),
        "total": round(t_transcription + t_diarization + t_alignment, 2),
    }

    print("\n--- Timing Summary ---")
    print(f"Transcription: {timing['transcription']:.2f}s")
    print(f"Diarization:   {timing['diarization']:.2f}s")
    print(f"Alignment:     {timing['alignment']:.2f}s")
    print(f"Total:         {timing['total']:.2f}s")

    # Print a quick preview (FIXED: Using aligned_transcript)
    print("\n--- Final Output Preview ---")
    for block in aligned_transcript[:5]:
        print(f"[{block['start']:05.2f}s - {block['end']:05.2f}s] {block['speaker']}: {block['text']}")

    return {
        "transcript": formatted_json,
        "timing": timing,
    }


if __name__ == "__main__":
    # Insert your Hugging Face token here
    HF_TOKEN = "your_token_here" 
    
    # Run the pipeline on the real sample file
    run_pipeline("sample2.mp3", HF_TOKEN)