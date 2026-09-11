import os
# --- CPU OPTIMIZATION FOR INTEL i5 ---
# Restrict threads to prevent contention on Efficient cores
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

import torch
# Restrict PyTorch threads
torch.set_num_threads(4)

from faster_whisper import WhisperModel
import time

def transcribe_audio(audio_file_path):
    """
    Transcribes audio using the Faster-Whisper 'base' model.
    Optimized for CPU execution with VAD filtering and Word-Level Timestamps.
    """
    model_size = "base"
    
    print("Loading Faster-Whisper model...")
    try:
        model = WhisperModel(model_size, device="cpu", compute_type="int8", local_files_only=True)
    except Exception:
        print("Model not found locally. Downloading...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8", local_files_only=False)
    
    print(f"Starting transcription for {audio_file_path}...")
    
    # Run transcription with VAD and Word Timestamps
    segments_generator, info = model.transcribe(
        audio_file_path, 
        beam_size=5, 
        task="transcribe",
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500), # Native VAD tuned
        word_timestamps=True # CRITICAL: Required for future speaker alignment
    )
    
    segments_list = []
    full_transcript = ""
    
    for segment in segments_generator:
        # We now store the segment AND its word-level breakdown
        segment_data = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "words": [{"word": w.word, "start": w.start, "end": w.end} for w in segment.words]
        }
        segments_list.append(segment_data)
        full_transcript += segment.text + " "
        
    print("Transcription complete.")
    return full_transcript.strip(), segments_list, info.language

# --- Simple Local Test ---
if __name__ == "__main__":
    # Point this to a real audio file on your machine to test
    test_audio = "meeting.m4a" 
    text, segments, lang = transcribe_audio(test_audio)
    print(segments[0]) # Should print the first segment with word-level timestamps
    pass