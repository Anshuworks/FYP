from pprint import pprint

from member2_intelligence.pipeline import attach_evidence
from member2_intelligence.intelligence.extractor import extract_intelligence


# ---------------------------------------------------------
# Controlled meeting transcript
# ---------------------------------------------------------

transcript = {
    "meeting_id": "controlled_test",
    "language": "en",
    "segments": [
        {
            "id": 1,
            "speaker": "SPEAKER_00",
            "start": 0.0,
            "end": 5.0,
            "raw_text": "We need to finish the backend implementation by Friday.",
            "cleaned_text": "We need to finish the backend implementation by Friday.",
            "text": "We need to finish the backend implementation by Friday.",
            "overlap": False,
        },
        {
            "id": 2,
            "speaker": "SPEAKER_01",
            "start": 5.0,
            "end": 10.0,
            "raw_text": "I will complete the API integration by Friday.",
            "cleaned_text": "I will complete the API integration by Friday.",
            "text": "I will complete the API integration by Friday.",
            "overlap": False,
        },
        {
            "id": 3,
            "speaker": "SPEAKER_00",
            "start": 10.0,
            "end": 15.0,
            "raw_text": "Agreed. We will deploy the application on Monday.",
            "cleaned_text": "Agreed. We will deploy the application on Monday.",
            "text": "Agreed. We will deploy the application on Monday.",
            "overlap": False,
        },
    ],
}


# ---------------------------------------------------------
# Ask Qwen to extract intelligence
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 1: QWEN EXTRACTION")
print("=" * 70)

intelligence = extract_intelligence(transcript)

print("\nClaims:")
for item in intelligence.claims:
    print(f"  - {item.text}")

print("\nDecisions:")
for item in intelligence.decisions:
    print(f"  - {item.text}")

print("\nAction Items:")
for item in intelligence.action_items:
    print(
        f"  - {item.task}"
        f" | owner={item.owner}"
        f" | deadline={item.deadline}"
    )

print("\nTopics:")
for item in intelligence.topics:
    print(f"  - {item.name}")

print("\nContradictions:")
for item in intelligence.contradictions:
    print(f"  - {item.description}")


# ---------------------------------------------------------
# Attach evidence using our deterministic pipeline
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 2: EVIDENCE RETRIEVAL + VERIFICATION")
print("=" * 70)

attach_evidence(intelligence, transcript)


# ---------------------------------------------------------
# Display final verified intelligence
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL VERIFIED INTELLIGENCE")
print("=" * 70)


def print_item(label, item, text):
    print(f"\n{label}: {text}")

    if item.evidence:
        for ev in item.evidence:
            print(
                f"    Evidence:"
                f" segment={ev.segment_id}"
                f" | speaker={ev.speaker}"
                f" | {ev.start:.1f}s-{ev.end:.1f}s"
            )
            print(f'    Quote: "{ev.quote}"')
    else:
        print("    Evidence: NONE")


for item in intelligence.claims:
    print_item("CLAIM", item, item.text)

for item in intelligence.decisions:
    print_item("DECISION", item, item.text)

for item in intelligence.action_items:
    print_item("ACTION", item, item.task)

for item in intelligence.topics:
    print_item("TOPIC", item, item.name)

for item in intelligence.contradictions:
    print_item("CONTRADICTION", item, item.description)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)