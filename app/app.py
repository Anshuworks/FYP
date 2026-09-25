import streamlit as st
import os
import sys
import time

# Add the parent directory to sys.path so Python can find the modular folders
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import all modules (Member 1 & Member 2)
from member1_speech.asr.transcriber import transcribe_audio
from member1_speech.diarization.diarizer import diarize_audio
from member1_speech.alignment.aligner import align_and_merge
from member2_intelligence.pipeline import run_intelligence_pipeline

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
    1. Speech-to-Text (Whisper)
    2. Speaker Diarization (PyAnnote)
    3. Speaker Alignment
    4. Text Preprocessing
    5. NLP Summarization
    """)
    
    st.divider()
    # SECURE TOKEN INPUT (No hardcoding required!)
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

# Session state initialization for retaining pipeline results across reruns
if "processed_data" not in st.session_state:
    st.session_state["processed_data"] = None
if "current_file" not in st.session_state:
    st.session_state["current_file"] = None

if uploaded_file is not None:
    # Reset state if a new file is uploaded
    if st.session_state["current_file"] != uploaded_file.name:
        st.session_state["processed_data"] = None
        st.session_state["current_file"] = uploaded_file.name

    st.audio(uploaded_file)
    
    process_clicked = st.button("🚀 Process Meeting Audio", use_container_width=True)

    if process_clicked:
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
                # Stage 1: Transcription
                t0 = time.perf_counter()
                raw_text, segments, lang_code = transcribe_audio(temp_filename)
                t_transcription = time.perf_counter() - t0
                st.write(f"✅ 1. Transcription — {t_transcription:.2f} sec")
                
                # Stage 2: Speaker Diarization
                t0 = time.perf_counter()
                diarization_intervals = diarize_audio(temp_filename, hf_token)
                t_diarization = time.perf_counter() - t0
                unique_speakers = sorted(list(set(s["speaker"] for s in diarization_intervals)))
                num_speakers = len(unique_speakers)
                st.write(f"✅ 2. Speaker Diarization — {t_diarization:.2f} sec")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;👥 {num_speakers} speakers detected")
                
                # Stage 3: Speaker Alignment
                t0 = time.perf_counter()
                aligned_transcript = align_and_merge(segments, diarization_intervals)
                t_alignment = time.perf_counter() - t0
                st.write(f"✅ 3. Speaker Alignment — {t_alignment:.2f} sec")

                # --- MEMBER 2: INTELLIGENCE PIPELINE ---
                member1_timing = {
                    "transcription": t_transcription,
                    "diarization": t_diarization,
                    "alignment": t_alignment,
                }

                def on_stage_complete(stage_name, duration):
                    if stage_name == "preprocessing":
                        st.write(f"✅ 4. Text Preprocessing — {duration:.2f} sec")
                    elif stage_name == "bart_summary":
                        st.write(f"✅ 5. BART Baseline Summary — {duration:.2f} sec")
                    elif stage_name == "qwen_extraction":
                        st.write(f"✅ 6. Qwen Intelligence — {duration:.2f} sec")
                    elif stage_name == "evidence":
                        st.write(f"✅ 7. Evidence Retrieval & Verification — {duration:.2f} sec")

                intelligence_result = run_intelligence_pipeline(
                    aligned_transcript,
                    lang_code,
                    uploaded_file.name,
                    member1_timing=member1_timing,
                    stage_callback=on_stage_complete,
                )

                processed_transcript = intelligence_result["transcript"]
                cleaned_text = intelligence_result["cleaned_text"]
                summary_text = intelligence_result["summary"]
                timing = intelligence_result["timing"]

                total_seconds = timing["total"]
                total_min = int(total_seconds // 60)
                rem_sec = total_seconds % 60
                total_str = f"{total_min} min {rem_sec:.2f} sec"

                st.write("")
                st.write("🚀 **Pipeline Complete!**")
                st.write(f"Total processing time: {total_str}")

                status_box.update(label="🚀 Pipeline Complete!", state="complete", expanded=False)

        # Cleanup temp files
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        wav_filename = temp_filename.rsplit('.', 1)[0] + ".wav"
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

        # Store in session state for persistence across user interactions (e.g. speaker renaming)
        st.session_state["processed_data"] = {
            "aligned_transcript": aligned_transcript,
            "unique_speakers": unique_speakers,
            "cleaned_text": cleaned_text,
            "summary_text": summary_text,
            "timing": timing,
            "total_str": total_str,
        }

    # Display processing stages summary when results exist but process wasn't just run
    if st.session_state["processed_data"] is not None and not process_clicked:
        data = st.session_state["processed_data"]
        t = data["timing"]
        with st.expander("🔍 See Processing Stages", expanded=False):
            st.write(f"✅ 1. Transcription — {t.get('transcription', 0.0):.2f} sec")
            st.write(f"✅ 2. Speaker Diarization — {t.get('diarization', 0.0):.2f} sec")
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;👥 {len(data['unique_speakers'])} speakers detected")
            st.write(f"✅ 3. Speaker Alignment — {t.get('alignment', 0.0):.2f} sec")
            st.write(f"✅ 4. Text Preprocessing — {t.get('preprocessing', 0.0):.2f} sec")
            st.write(f"✅ 5. BART Baseline Summary — {t.get('bart_summary', 0.0):.2f} sec")
            st.write(f"✅ 6. Qwen Intelligence — {t.get('qwen_extraction', 0.0):.2f} sec")
            st.write(f"✅ 7. Evidence Retrieval & Verification — {t.get('evidence', 0.0):.2f} sec")
            st.write("")
            st.write("🚀 **Pipeline Complete!**")
            st.write(f"Total processing time: {data['total_str']}")

    # --- DISPLAY RESULTS ---
    if st.session_state["processed_data"] is not None:
        data = st.session_state["processed_data"]
        summary_text = data["summary_text"]
        cleaned_text = data["cleaned_text"]
        aligned_transcript = data["aligned_transcript"]
        unique_speakers = data["unique_speakers"]

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

            # --- 3. SPEAKER COUNT ---
            st.markdown(f"#### 👥 {len(unique_speakers)} Speakers Detected")

            # --- 4. MANUAL SPEAKER NAME MAPPING ---
            with st.expander("🏷️ Edit Speaker Names (Optional)", expanded=False):
                st.caption("Map detected speaker IDs to names for transcript display:")
                speaker_name_map = {}
                for spk in unique_speakers:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**{spk}** →")
                    with col2:
                        custom_name = st.text_input(
                            f"Name for {spk}",
                            key=f"speaker_input_{spk}",
                            placeholder="Enter name",
                            label_visibility="collapsed",
                        )
                    if custom_name and custom_name.strip():
                        speaker_name_map[spk] = custom_name.strip()
                    else:
                        speaker_name_map[spk] = spk

            # Upgrade to dynamic Chat Bubbles!
            avatars = ["🧑‍💼", "👩‍💻", "👨‍🏫", "👩‍🔬", "🕵️", "🧑‍⚕️"]
            speaker_avatars = {}
            
            for block in aligned_transcript:
                speaker_id = block["speaker"]
                display_name = speaker_name_map.get(speaker_id, speaker_id)
                if speaker_id not in speaker_avatars:
                    speaker_avatars[speaker_id] = avatars[len(speaker_avatars) % len(avatars)]
                
                with st.chat_message(name=display_name, avatar=speaker_avatars[speaker_id]):
                    st.caption(f"{display_name} • {block['start']:05.2f}s - {block['end']:05.2f}s")
                    st.write(block["text"])

else:
    st.info("Upload an audio file to start the transcription and summarization pipeline.")