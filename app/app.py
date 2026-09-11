import streamlit as st
import os
import sys
import time

# Add the parent directory to sys.path so Python can find the modular folders
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now import using the new directory paths
from member1_speech.asr.transcriber import transcribe_audio
from member2_intelligence.preprocessing.preprocessor import clean_transcript
from member2_intelligence.llm.summarizer import generate_summary 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="centered"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Project Info")
    st.info("""
    **Modules Implemented:**
    1. Speech-to-Text 
    2. Text Preprocessing
    3. NLP Summarization
    
    """)
    st.divider()
    st.write("**Team members:**")
    st.write("- Anshu Kumar (29)")
    st.write("- Aman Kumar (27)")

# --- HEADER ---
st.title("🎙️ AI Meeting Transcription & Summarization")
st.markdown("Automated documentation system for modern meetings.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Upload meeting audio", 
    type=["mp3", "wav", "m4a", "opus"],
    help="Upload your meeting recording here."
)

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("🚀 Process Meeting Audio", use_container_width=True):
      
        file_ext = uploaded_file.name.split('.')[-1]
        temp_filename = f"temp_audio.{file_ext}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.expander("🔍 See Processing Stages", expanded=True):
            with st.status("Running Pipeline...", expanded=True) as status_box:
                
                # 1. Initializing
                st.write("⏳ 1. Initializing Model...")
                raw_text, segments, lang_code = transcribe_audio(temp_filename)
                st.write("✅ 1. Model Initialized")
                time.sleep(2)

                # 2 & 3. Language
                st.write("⏳ 2. Detecting Language...")
                time.sleep(0)
                st.write(f"✅ 3. Detected Language: **{lang_code.upper()}**")
                time.sleep(2)

                # 4. Transcribing
                st.write("✅ 4. Transcription Finished")
                time.sleep(0.5)

                # 5. Preprocessing
                st.write("⏳ 5. Preprocessing Text...")
                time.sleep(0.5) 
                
                # 6. Cleaning
                cleaned_text = clean_transcript(raw_text)
                st.write("✅ 6. Cleaning Transcript (Fillers Removed)")
                time.sleep(0.5)

                # 7. Text Ready
                st.write("✅ 7. Text Processing Complete")
                time.sleep(0.5)

                # 8. Summarizing (New Module 3 Stage)
                st.write("⏳ 8. Summarizing Transcript (Using BART)...")
                summary_text = generate_summary(cleaned_text)
                
                # 9. Summary Complete
                st.write("✅ 9. Summarization Complete!")

                status_box.update(label="🚀 All 9 Stages Complete!", state="complete", expanded=False)

        # --- DISPLAY RESULTS ---
        st.divider()
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "✨ Cleaned Transcript", "🕒 Detailed Timestamps"])

        with tab1:
            st.subheader("Meeting Summary")
            st.success(summary_text)
            st.download_button("📥 Download Summary", summary_text, file_name="meeting_summary.txt")

        with tab2:
            st.subheader("Cleaned Meeting Transcript")
            st.text_area(
                label="Final Output", 
                value=cleaned_text, 
                height=350, 
                label_visibility="collapsed"
            )
            st.download_button("📥 Download Transcript", cleaned_text, file_name="meeting_transcript.txt")

        with tab3:
            st.subheader("Transcript with Timestamps")
            ts_display = ""
            for s in segments:
                # FIX: Access dictionary keys instead of object attributes
                start_time = f"{int(s['start'] // 60):02d}:{int(s['start'] % 60):02d}"
                end_time = f"{int(s['end'] // 60):02d}:{int(s['end'] % 60):02d}"
                ts_display += f"**[{start_time} -> {end_time}]** {s['text']}\n\n"
            st.markdown(ts_display)

        if os.path.exists(temp_filename):
            os.remove(temp_filename)

else:
    st.info("Upload an audio file to start the transcription and summarization pipeline.")