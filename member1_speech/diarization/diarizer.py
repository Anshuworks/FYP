import os
import shutil
import subprocess
import torch

# --- WINDOWS PYTHON 3.8+ DLL FIX FOR TORCHCODEC ---
# Python 3.8+ ignores the system PATH for DLLs. We must explicitly inject it so it finds FFmpeg.
ffmpeg_exe_path = shutil.which("ffmpeg")
if ffmpeg_exe_path:
    ffmpeg_bin_dir = os.path.dirname(ffmpeg_exe_path)
    try:
        os.add_dll_directory(ffmpeg_bin_dir)
    except AttributeError:
        pass # Ignored if not on Windows
else:
    print("⚠️ WARNING: FFmpeg not found in PATH! Please restart your VS Code terminal.")

# Now we can safely import the audio libraries
from pyannote.audio import Pipeline


def diarize_audio(audio_path: str, hf_token: str):
    """
    Runs PyAnnote speaker diarization on the provided audio file.
    Optimized to fallback to CPU gracefully and bypass compressed audio bugs.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # --- FIX FOR COMPRESSED AUDIO SAMPLE MISMATCH ---
    # Convert .m4a/.mp3 to a standard 16kHz Mono WAV file
    wav_path = audio_path.rsplit('.', 1)[0] + ".wav"
    print(f"Converting {os.path.basename(audio_path)} to uncompressed WAV format...")
    subprocess.run([
        "ffmpeg", "-y", "-i", audio_path, 
        "-ac", "1", "-ar", "16000", 
        "-loglevel", "error", wav_path
    ], check=True)
    # ------------------------------------------------

    print("Loading PyAnnote Diarization pipeline...")
    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=hf_token
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load PyAnnote. Error: {e}")

    # Explicitly map to CPU since you are running an Intel i5 without CUDA
    device = torch.device("cpu")
    pipeline.to(device)

    print(f"Running diarization on {os.path.basename(wav_path)}...")
    print("NOTE: PyAnnote on CPU is intensive. This may take 1.5x - 2.5x the audio length.")
    
    # Run the model on the clean WAV file
    output = pipeline(wav_path)
    
    # PyAnnote 4.x returns a wrapper; we need to extract the actual speaker diarization object
    diarization = output.speaker_diarization

    # Extract results into a clean, structured list of dictionaries
    speaker_intervals = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_intervals.append({
            "speaker": speaker,
            "start": round(turn.start, 2),
            "end": round(turn.end, 2)
        })

    print(f"Diarization complete! Found {len(set([s['speaker'] for s in speaker_intervals]))} unique speakers.")
    return speaker_intervals


# --- Integration Test ---
if __name__ == "__main__":
    # 1. PASTE YOUR ACTUAL HUGGING FACE TOKEN HERE
    HF_TOKEN = "your_token_here" 
    
    # 2. Dynamic path resolution to data/samples/sample2.mp3
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
    test_audio = os.path.join(PROJECT_ROOT, "data", "samples", "sample2.mp3")
    
    print(f"Testing diarization with audio: {test_audio}")
    
    # 3. Run diarization
    intervals = diarize_audio(test_audio, HF_TOKEN)
    
    # 4. Print the first 5 speaker turns to verify
    print(f"\n--- All Speaker Turns ---")
    for interval in intervals:
        print(f"[{interval['start']:05.2f}s -> {interval['end']:05.2f}s] {interval['speaker']}")