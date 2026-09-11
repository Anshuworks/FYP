import re

def clean_transcript(text):
    """
    Cleans raw transcript text by removing filler words, 
    fixing spacing, and normalizing characters.
    """
    fillers = [r'\bum\b', r'\buh\b', r'\behr\b', r'\bhmm\b', r'\blike\b']
    cleaned_text = text
    for filler in fillers:
        cleaned_text = re.sub(filler, '', cleaned_text, flags=re.IGNORECASE)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s([?.!,])', r'\1', cleaned_text)
    cleaned_text = '. '.join([s.strip().capitalize() for s in cleaned_text.split('.') if s.strip()])
    
    return cleaned_text + "."

# --- Integration Test ---
if __name__ == "__main__":
    raw_input = "Um, so the meeting is like starting now... uh, we should, uh, talk about the budget."
    result = clean_transcript(raw_input)
    print("Raw: ", raw_input)
    print("Cleaned: ", result)