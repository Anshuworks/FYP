import os
import sys
import time
import json
import soundfile as sf

# --- PATH RESOLUTION ---
# Ensure project root is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from member1_speech.asr.transcriber import transcribe_audio

try:
    import jiwer
except ImportError:
    raise ImportError("jiwer is required for ASR evaluation. Run: pip install jiwer")


def get_audio_duration(audio_path: str) -> float:
    """Calculates audio duration in seconds."""
    try:
        data, samplerate = sf.read(audio_path)
        return len(data) / float(samplerate)
    except Exception:
        # Fallback using pyav / faster-whisper internal reader if available
        import av
        with av.open(audio_path) as container:
            stream = container.streams.audio[0]
            duration = float(stream.duration * stream.time_base)
            return duration


def normalize_text(text: str) -> str:
    """
    Standard ASR reference normalization:
    lower-casing, stripping punctuation, and removing excess whitespace.
    """
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip()
    ])
    return transformation(text)


def evaluate_asr(reference_text: str, audio_path: str) -> dict:
    """
    Evaluates Faster-Whisper ASR against a reference ground-truth text.
    Computes WER, CER, processing latency, audio duration, and RTF.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 1. Get audio duration
    audio_duration = get_audio_duration(audio_path)

    # 2. Transcribe and measure processing time
    start_time = time.perf_counter()
    hypothesis_raw, segments, detected_lang = transcribe_audio(audio_path)
    processing_time = time.perf_counter() - start_time

    # 3. Calculate Real-Time Factor (RTF)
    rtf = processing_time / audio_duration if audio_duration > 0 else 0.0

    # 4. Normalize reference and hypothesis for fair comparison
    ref_norm = normalize_text(reference_text)
    hyp_norm = normalize_text(hypothesis_raw)

    # 5. Compute Error Rates
    wer = jiwer.wer(ref_norm, hyp_norm)
    cer = jiwer.cer(ref_norm, hyp_norm)

    # Breakdown of alignment operations using jiwer 3.0+ API
    word_output = jiwer.process_words(ref_norm, hyp_norm)

    metrics = {
        "audio_file": os.path.basename(audio_path),
        "detected_language": detected_lang,
        "audio_duration_sec": round(audio_duration, 2),
        "processing_time_sec": round(processing_time, 2),
        "rtf": round(rtf, 4),
        "wer": round(wer, 4),
        "cer": round(cer, 4),
        "substitutions": word_output.substitutions,
        "deletions": word_output.deletions,
        "insertions": word_output.insertions,
        "hits": word_output.hits,
        "reference_normalized": ref_norm,
        "hypothesis_normalized": hyp_norm
    }

    return metrics


def print_evaluation_summary(metrics: dict):
    """Prints a formatted evaluation table."""
    print("\n" + "=" * 60)
    print("           SPEECH RECOGNITION BENCHMARK REPORT           ")
    print("=" * 60)
    print(f" Audio File       : {metrics['audio_file']}")
    print(f" Detected Lang    : {metrics['detected_language'].upper()}")
    print(f" Audio Duration   : {metrics['audio_duration_sec']} s")
    print(f" Processing Time  : {metrics['processing_time_sec']} s")
    print(f" Real-Time Factor : {metrics['rtf']}x (RTF < 1.0 is faster than real time)")
    print("-" * 60)
    print(f" Word Error Rate  : {metrics['wer'] * 100:.2f}%")
    print(f" Char Error Rate  : {metrics['cer'] * 100:.2f}%")
    print(f" Alignment Stats  : Hits={metrics['hits']} | Subs={metrics['substitutions']} | Del={metrics['deletions']} | Ins={metrics['insertions']}")
    print("=" * 60)


if __name__ == "__main__":
    # --- Integration Test using your sample files ---
    sample_audio = os.path.join(PROJECT_ROOT, "data", "samples", "medium.m4a")
    
    # Example snippet reference from the meeting opening
    ground_truth_sample = (
        "Mayor Patrick Terrien for the RM of Springfield meeting agenda for March the 3rd of 2026. "
        "Starting at exactly 6 p.m. This meeting is called to order. All council is present. "
        "I'll identify them and then right in the sending orders deputy mayor Fuel councillors "
        "Kaczynski Miller and Warren. We'll go to land acknowledgement there."
    )

    if os.path.exists(sample_audio):
        print(f"Running ASR evaluation on: {sample_audio}")
        results = evaluate_asr(ground_truth_sample, sample_audio)
        print_evaluation_summary(results)

        # Save results to experiments/baseline/ for your Day 20-22 quantization comparison
        os.makedirs(os.path.join(PROJECT_ROOT, "experiments", "baseline"), exist_ok=True)
        output_file = os.path.join(PROJECT_ROOT, "experiments", "baseline", "asr_baseline_metrics.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved benchmark metrics to: {output_file}")
    else:
        print(f"Sample audio not found at: {sample_audio}")
        print("Please place a test audio file in data/samples/ to run the evaluation.")