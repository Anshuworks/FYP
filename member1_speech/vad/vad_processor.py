import torch
import torchaudio
import warnings

# Suppress annoying PyTorch warnings
warnings.filterwarnings("ignore")

def detect_speech_regions(audio_path):
    """
    Scans an audio file and returns a list of timestamps containing human speech.
    Uses Silero VAD (optimized for CPU).
    """
    try:
        # Load the Silero VAD model directly from PyTorch Hub
        model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            onnx=False
        )
        
        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
        
        # Read the audio file
        wav = read_audio(audio_path)
        
        # Get speech timestamps (returns dictionaries with 'start' and 'end' in samples)
        # Using a conservative threshold to ensure we don't accidentally cut out quiet speech
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, threshold=0.3)
        
        # Convert the raw audio samples into actual seconds for our JSON schema
        regions_in_seconds = []
        for ts in speech_timestamps:
            start_sec = round(ts['start'] / 16000, 2)
            end_sec = round(ts['end'] / 16000, 2)
            regions_in_seconds.append({'start': start_sec, 'end': end_sec})
            
        return regions_in_seconds
        
    except Exception as e:
        print(f"⚠️ VAD Processing failed: {e}")
        # Fallback: if VAD fails, return a region covering a massive duration 
        # so the downstream pipeline doesn't crash, it just processes the whole file.
        return [{'start': 0.0, 'end': 99999.0}]

# --- Quick Local Testing ---
if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(current_dir, "..", "..", "data", "samples", "sample2.wav")
    
    if os.path.exists(sample_path):
        print("Testing Silero VAD...")
        regions = detect_speech_regions(sample_path)
        print(f"Found {len(regions)} speech regions:")
        for r in regions:
            print(f"[{r['start']}s -> {r['end']}s]")