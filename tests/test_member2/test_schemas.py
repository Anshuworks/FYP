"""
Unit tests for member2_intelligence.intelligence.schemas

Tests the evidence-based intelligence data schema: Evidence, Claim,
Decision, ActionItem, Topic, Contradiction, and MeetingIntelligence.

Fully deterministic — no models, network, or external dependencies.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from member2_intelligence.intelligence.schemas import (
    Evidence,
    Claim,
    Decision,
    ActionItem,
    Topic,
    Contradiction,
    MeetingIntelligence,
)


# -- Helpers ----------------------------------------------------------------

def _make_evidence(**overrides):
    """Create a valid Evidence with sensible defaults, allowing overrides."""
    defaults = {
        "segment_id": 1,
        "speaker": "SPEAKER_00",
        "start": 0.0,
        "end": 5.5,
        "quote": "The budget is approved.",
    }
    defaults.update(overrides)
    return Evidence(**defaults)


def _make_evidence_b():
    """A second distinct evidence for multi-evidence tests."""
    return Evidence(
        segment_id=3,
        speaker="SPEAKER_01",
        start=12.0,
        end=18.5,
        quote="We need to revisit the timeline.",
    )


# -- Evidence tests ---------------------------------------------------------

def test_evidence_creation():
    ev = _make_evidence()
    assert ev.segment_id == 1
    assert ev.speaker == "SPEAKER_00"
    assert ev.start == 0.0
    assert ev.end == 5.5
    assert ev.quote == "The budget is approved."
    ev.validate()  # should not raise
    print("  PASS: Evidence can be created and validates")


def test_evidence_rejects_invalid_segment_id():
    for bad_id in [0, -1, "abc", None]:
        ev = _make_evidence(segment_id=bad_id)
        try:
            ev.validate()
            print(f"  FAIL: should reject segment_id={bad_id!r}")
            return
        except (ValueError, TypeError):
            pass
    print("  PASS: Evidence rejects invalid segment_id")


def test_evidence_rejects_empty_speaker():
    for bad in ["", None]:
        ev = _make_evidence(speaker=bad)
        try:
            ev.validate()
            print(f"  FAIL: should reject speaker={bad!r}")
            return
        except (ValueError, TypeError):
            pass
    print("  PASS: Evidence rejects empty/None speaker")


def test_evidence_rejects_negative_start():
    ev = _make_evidence(start=-1.0)
    try:
        ev.validate()
        print("  FAIL: should reject negative start")
        return
    except ValueError:
        pass
    print("  PASS: Evidence rejects negative start")


def test_evidence_rejects_end_before_start():
    ev = _make_evidence(start=10.0, end=5.0)
    try:
        ev.validate()
        print("  FAIL: should reject end < start")
        return
    except ValueError:
        pass
    print("  PASS: Evidence rejects end < start")


def test_evidence_rejects_empty_quote():
    for bad in ["", None]:
        ev = _make_evidence(quote=bad)
        try:
            ev.validate()
            print(f"  FAIL: should reject quote={bad!r}")
            return
        except (ValueError, TypeError):
            pass
    print("  PASS: Evidence rejects empty/None quote")


# -- Claim tests ------------------------------------------------------------

def test_claim_with_single_evidence():
    c = Claim(id="c1", text="Budget was approved.", evidence=[_make_evidence()])
    c.validate()
    assert len(c.evidence) == 1
    print("  PASS: Claim with single evidence validates")


def test_claim_with_multiple_evidence():
    c = Claim(
        id="c2",
        text="Budget approved but timeline uncertain.",
        evidence=[_make_evidence(), _make_evidence_b()],
    )
    c.validate()
    assert len(c.evidence) == 2
    print("  PASS: Claim with multiple evidence validates")


def test_claim_rejects_empty_evidence():
    c = Claim(id="c3", text="Unsupported claim.", evidence=[])
    try:
        c.validate()
        print("  FAIL: should reject empty evidence")
        return
    except ValueError:
        pass
    print("  PASS: Claim rejects empty evidence list")


# -- Decision tests ----------------------------------------------------------

def test_decision_with_evidence():
    d = Decision(
        id="d1",
        text="Decided to proceed with Phase 2.",
        evidence=[_make_evidence()],
    )
    d.validate()
    assert d.id == "d1"
    print("  PASS: Decision with evidence validates")


def test_decision_rejects_empty_evidence():
    d = Decision(id="d2", text="No proof.", evidence=[])
    try:
        d.validate()
        print("  FAIL: should reject empty evidence")
        return
    except ValueError:
        pass
    print("  PASS: Decision rejects empty evidence list")


# -- ActionItem tests --------------------------------------------------------

def test_action_item_with_owner_and_deadline():
    a = ActionItem(
        id="a1",
        task="Prepare the revised budget.",
        owner="SPEAKER_00",
        deadline="Friday",
        evidence=[_make_evidence()],
    )
    a.validate()
    assert a.owner == "SPEAKER_00"
    assert a.deadline == "Friday"
    print("  PASS: ActionItem with owner and deadline validates")


def test_action_item_missing_owner_and_deadline():
    a = ActionItem(
        id="a2",
        task="Review the document.",
        owner=None,
        deadline=None,
        evidence=[_make_evidence()],
    )
    a.validate()
    assert a.owner is None
    assert a.deadline is None
    print("  PASS: ActionItem with None owner/deadline validates")


def test_action_item_rejects_empty_evidence():
    a = ActionItem(id="a3", task="Do something.", evidence=[])
    try:
        a.validate()
        print("  FAIL: should reject empty evidence")
        return
    except ValueError:
        pass
    print("  PASS: ActionItem rejects empty evidence list")


# -- Topic tests -------------------------------------------------------------

def test_topic_with_evidence():
    t = Topic(id="t1", name="Budget Discussion", evidence=[_make_evidence()])
    t.validate()
    assert t.name == "Budget Discussion"
    print("  PASS: Topic with evidence validates")


def test_topic_rejects_empty_evidence():
    t = Topic(id="t2", name="Orphan topic.", evidence=[])
    try:
        t.validate()
        print("  FAIL: should reject empty evidence")
        return
    except ValueError:
        pass
    print("  PASS: Topic rejects empty evidence list")


# -- Contradiction tests -----------------------------------------------------

def test_contradiction_with_evidence():
    c = Contradiction(
        id="x1",
        description="Speaker 0 said approved, Speaker 1 said not approved.",
        evidence=[_make_evidence(), _make_evidence_b()],
    )
    c.validate()
    assert len(c.evidence) == 2
    print("  PASS: Contradiction with evidence validates")


def test_contradiction_rejects_empty_evidence():
    c = Contradiction(id="x2", description="No proof.", evidence=[])
    try:
        c.validate()
        print("  FAIL: should reject empty evidence")
        return
    except ValueError:
        pass
    print("  PASS: Contradiction rejects empty evidence list")


# -- MeetingIntelligence tests -----------------------------------------------

def test_meeting_intelligence_all_categories():
    mi = MeetingIntelligence(
        claims=[
            Claim(id="c1", text="Budget approved.", evidence=[_make_evidence()])
        ],
        decisions=[
            Decision(id="d1", text="Proceed with Phase 2.", evidence=[_make_evidence()])
        ],
        action_items=[
            ActionItem(id="a1", task="Revise budget.", owner=None, deadline=None,
                       evidence=[_make_evidence()])
        ],
        topics=[
            Topic(id="t1", name="Budget", evidence=[_make_evidence()])
        ],
        contradictions=[
            Contradiction(id="x1", description="Conflicting timeline statements.",
                          evidence=[_make_evidence(), _make_evidence_b()])
        ],
    )
    mi.validate()
    assert len(mi.claims) == 1
    assert len(mi.decisions) == 1
    assert len(mi.action_items) == 1
    assert len(mi.topics) == 1
    assert len(mi.contradictions) == 1
    print("  PASS: MeetingIntelligence with all categories validates")


def test_meeting_intelligence_empty():
    mi = MeetingIntelligence()
    mi.validate()  # empty is valid — no items found
    assert len(mi.claims) == 0
    print("  PASS: Empty MeetingIntelligence validates")


def test_meeting_intelligence_catches_bad_evidence_in_claim():
    """Validation should propagate to nested Evidence objects."""
    bad_ev = Evidence(segment_id=-1, speaker="X", start=0.0, end=1.0, quote="q")
    mi = MeetingIntelligence(
        claims=[Claim(id="c1", text="Bad.", evidence=[bad_ev])]
    )
    try:
        mi.validate()
        print("  FAIL: should reject bad evidence inside claim")
        return
    except ValueError:
        pass
    print("  PASS: MeetingIntelligence.validate() catches bad nested evidence")


# -- Runner ------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Running Intelligence Schema Tests")
    print("=" * 60)

    print("\n--- Evidence ---")
    test_evidence_creation()
    test_evidence_rejects_invalid_segment_id()
    test_evidence_rejects_empty_speaker()
    test_evidence_rejects_negative_start()
    test_evidence_rejects_end_before_start()
    test_evidence_rejects_empty_quote()

    print("\n--- Claim ---")
    test_claim_with_single_evidence()
    test_claim_with_multiple_evidence()
    test_claim_rejects_empty_evidence()

    print("\n--- Decision ---")
    test_decision_with_evidence()
    test_decision_rejects_empty_evidence()

    print("\n--- ActionItem ---")
    test_action_item_with_owner_and_deadline()
    test_action_item_missing_owner_and_deadline()
    test_action_item_rejects_empty_evidence()

    print("\n--- Topic ---")
    test_topic_with_evidence()
    test_topic_rejects_empty_evidence()

    print("\n--- Contradiction ---")
    test_contradiction_with_evidence()
    test_contradiction_rejects_empty_evidence()

    print("\n--- MeetingIntelligence ---")
    test_meeting_intelligence_all_categories()
    test_meeting_intelligence_empty()
    test_meeting_intelligence_catches_bad_evidence_in_claim()

    print("\n" + "=" * 60)
    print("[OK] ALL SCHEMA TESTS PASSED")
    print("=" * 60)
