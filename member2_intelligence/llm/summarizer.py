from transformers import pipeline
import torch

def generate_summary(text):
    model_name = "facebook/bart-large-cnn"
    summarizer = pipeline("summarization", model=model_name, device=-1)
    
    words = text.split()
    # If the meeting is short enough, summarize directly
    if len(words) <= 500:
        res = summarizer(text, max_length=130, min_length=40, do_sample=False, truncation=True)
        return res[0]['summary_text']
    
    # PASS 1 (MAP): Summarize individual ~450-word sections
    chunk_size = 450
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    intermediate_summaries = []
    
    for chunk in chunks:
        res = summarizer(chunk, max_length=80, min_length=25, do_sample=False, truncation=True)
        intermediate_summaries.append(res[0]['summary_text'])
    
    # PASS 2 (REDUCE): Combine intermediate summaries into a cohesive final brief
    combined_notes = " ".join(intermediate_summaries)
    final_res = summarizer(combined_notes, max_length=150, min_length=50, do_sample=False, truncation=True)
    return final_res[0]['summary_text']