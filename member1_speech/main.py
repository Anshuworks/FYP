import os
import json

# Import the FOUR pillars of your pipeline (VAD added!)
from vad.vad_processor import detect_speech_regions
from asr.transcriber import transcribe_audio
from diarization.diarizer import diarize_audio
from alignment.aligner import align_and_merge

def run_pipeline(audio_filename, hf_token):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    # Standardize input to WAV to ensure VAD reads it cleanly
    raw_audio_path = os.path.join(project_root, "data", "samples", audio_filename)
    # Note: If it's an MP3, your FFmpeg script in Diarizer will eventually convert it, 
    # but for VAD it's best if we test against the WAV version if it exists, or just pass the original.
    
    output_dir = os.path.join(project_root, "data", "mock_transcripts")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"========== STARTING EVIDENCEMEET PIPELINE ==========")
    print(f"Processing Target: {audio_filename}")
    
    # --- STEP 1: Voice Activity Detection (VAD) ---
    print("\n--- STEP 1: Detecting Speech (VAD) ---")
    speech_regions = detect_speech_regions(raw_audio_path)
    total_speech_time = sum(r['end'] - r['start'] for r in speech_regions)
    print(f"Found {len(speech_regions)} speech segments (Total speech: {total_speech_time:.2f}s).")
    
    # --- STEP 2: The Ears (Faster-Whisper) ---
    print("\n--- STEP 2: Transcribing Audio ---")
    # In a fully optimized production app, you would ONLY send the 'speech_regions' to Whisper.
    # For this FYP iteration, we use VAD for profiling and metadata.
    full_text, whisper_segments, language = transcribe_audio(raw_audio_path)
    print(f"Detected Language: {language}")
    print(f"Extracted {len(whisper_segments)} text segments.")

    # --- STEP 3: The Clock (PyAnnote) ---
    print("\n--- STEP 3: Diarizing Speakers ---")
    diarization_intervals = diarize_audio(raw_audio_path, hf_token)
    
    # --- STEP 4: The Brain (Aligner) ---
    print("\n--- STEP 4: Aligning & Merging ---")
    aligned_transcript = align_and_merge(whisper_segments, diarization_intervals)
    print("✅ Alignment Complete") 

    # --- FORMAT AND SAVE JSON ---
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
            "cleaned_text": "", 
            "text": block["text"],
            "overlap": False 
        })

    output_file = os.path.join(output_dir, f"{audio_filename}_transcript.json")
    with open(output_file, "w") as f:
        json.dump(formatted_json, f, indent=4)
        
    print(f"\n========== PIPELINE COMPLETE ==========")
    print(f"Saved highly structured transcript to: {output_file}")


if __name__ == "__main__":
    HF_TOKEN = "your_token_here" 
    run_pipeline("sample2.mp3", HF_TOKEN)