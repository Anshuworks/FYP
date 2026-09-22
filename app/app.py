import streamlit as st
import os
import sys
import time

# Add the parent directory to sys.path so Python can find the modular folders
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import all modules (Member 1 & Member 2)
from member1_speech.vad.vad_processor import detect_speech_regions  # <-- NEW: Imported VAD
from member1_speech.asr.transcriber import transcribe_audio
from member1_speech.diarization.diarizer import diarize_audio
from member1_speech.alignment.aligner import align_and_merge
from member2_intelligence.preprocessing.preprocessor import clean_transcript
from member2_intelligence.llm.summarizer import generate_summary 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EvidenceMeet | AI Assistant",
    page_icon="🎙️",
    layout="centered"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Project Info")
    st.info("""
    **Modules Implemented:**
    1. Voice Activity Detection (VAD)
    2. Speech-to-Text (Whisper)
    3. Speaker Diarization (PyAnnote)
    4. Speaker Alignment
    5. Text Preprocessing
    6. NLP Summarization
    """)
    
    st.divider()
    # SECURE TOKEN INPUT
    hf_token = st.text_input("🔑 Hugging Face Token", type="password", help="Required for PyAnnote Diarization")
    
    st.divider()
    st.write("**Team members:**")
    st.write("- Anshu Kumar (29)")
    st.write("- Aman Kumar (27)")

# --- HEADER ---
st.title("🎙️ EvidenceMeet: Meeting Intelligence")
st.markdown("Automated edge-based transcription, diarization, and summarization.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Upload meeting audio", 
    type=["mp3", "wav", "m4a", "opus"],
    help="Upload your meeting recording here."
)

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("🚀 Process Meeting Audio", use_container_width=True):
        
        if not hf_token:
            st.error("⚠️ Please enter your Hugging Face Token in the sidebar to run the pipeline!")
            st.stop()
            
        file_ext = uploaded_file.name.split('.')[-1]
        temp_filename = f"temp_audio.{file_ext}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.expander("🔍 See Processing Stages", expanded=True):
            with st.status("Running EvidenceMeet Pipeline...", expanded=True) as status_box:
                
                # --- MEMBER 1: SPEECH PIPELINE ---
                st.write("⏳ 1. Running Voice Activity Detection (Silero VAD)...")
                speech_regions = detect_speech_regions(temp_filename)
                total_speech = sum(r['end'] - r['start'] for r in speech_regions)
                st.write(f"✅ 1. VAD Complete: Detected {len(speech_regions)} speech segments ({total_speech:.2f}s total speech).")

                st.write("⏳ 2. Initializing Whisper Model...")
                raw_text, segments, lang_code = transcribe_audio(temp_filename)
                st.write(f"✅ 2. Transcription Finished (Detected: **{lang_code.upper()}**)")
                
                st.write("⏳ 3. Running Speaker Diarization (PyAnnote)...")
                diarization_intervals = diarize_audio(temp_filename, hf_token)
                st.write(f"✅ 3. Diarization Complete. Found {len(set([s['speaker'] for s in diarization_intervals]))} speakers.")
                
                st.write("⏳ 4. Aligning Speakers with Text...")
                aligned_transcript = align_and_merge(segments, diarization_intervals)
                st.write("✅ 4. Alignment Complete")

                # --- MEMBER 2: INTELLIGENCE PIPELINE ---
                st.write("⏳ 5. Preprocessing & Cleaning Text...")
                cleaned_text = clean_transcript(raw_text)
                st.write("✅ 5. Cleaning Complete (Fillers Removed)")

                st.write("⏳ 6. Summarizing Transcript...")
                summary_text = generate_summary(cleaned_text)
                st.write("✅ 6. Summarization Complete!")

                status_box.update(label="🚀 Pipeline Complete!", state="complete", expanded=False)

        # --- DISPLAY RESULTS ---
        st.divider()
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "✨ Cleaned Text", "💬 Smart Transcript"])

        with tab1:
            st.subheader("Meeting Summary")
            st.success(summary_text)
            st.download_button("📥 Download Summary", summary_text, file_name="meeting_summary.txt")

        with tab2:
            st.subheader("Cleaned Meeting Transcript")
            st.text_area(label="Final Output", value=cleaned_text, height=350, label_visibility="collapsed")
            st.download_button("📥 Download Cleaned Text", cleaned_text, file_name="cleaned_transcript.txt")

        with tab3:
            st.subheader("Diarized Meeting Log")
            avatars = ["🧑‍💼", "👩‍💻", "👨‍🏫", "👩‍🔬", "🕵️", "🧑‍⚕️"]
            speaker_avatars = {}
            
            for block in aligned_transcript:
                speaker = block["speaker"]
                if speaker not in speaker_avatars:
                    speaker_avatars[speaker] = avatars[len(speaker_avatars) % len(avatars)]
                
                with st.chat_message(name=speaker, avatar=speaker_avatars[speaker]):
                    st.caption(f"{speaker} • {block['start']:05.2f}s - {block['end']:05.2f}s")
                    st.write(block["text"])

        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        wav_filename = temp_filename.rsplit('.', 1)[0] + ".wav"
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

else:
    st.info("Upload an audio file to start the transcription and summarization pipeline.")