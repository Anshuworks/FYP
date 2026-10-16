"""Targeted tests for the two fixed Streamlit UI controls:
1. Navigation restore: Fixed, always-visible expand/menu button when navigation is collapsed.
2. Hugging Face token entry: Clearly labelled, secure password input with environment fallback.
"""

import os
import pytest
from streamlit.testing.v1 import AppTest
from app.theme import get_theme_css

APP_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "app", "app.py")
)


def test_navigation_restore_css_both_themes():
    """Verify that both dark and light themes define the fixed navigation restore button."""
    for theme_mode in ["dark", "light"]:
        css = get_theme_css(theme_mode)

        # 1. Verify stHeader is NOT blanket-hidden with display: none
        assert '[data-testid="stHeader"] { display: none !important; }' not in css
        assert '#MainMenu, [data-testid="stHeader"], footer' not in css

        # 2. Verify selective branding suppression
        assert '#MainMenu, footer, [data-testid="stToolbarActions"]' in css
        assert '[data-testid="stHeader"]' in css
        assert "pointer-events: none !important;" in css

        # 3. Verify always-visible fixed restore button selectors
        assert '[data-testid="stExpandSidebarButton"]' in css
        assert '[data-testid="stSidebarCollapsedControl"]' in css

        # 4. Verify fixed positioning tokens
        assert "position: fixed !important;" in css
        assert "top: 14px !important;" in css
        assert "left: 14px !important;" in css
        assert "z-index: 100000 !important;" in css
        assert "display: flex !important;" in css
        assert "visibility: visible !important;" in css
        assert "pointer-events: auto !important;" in css

        # 5. Verify theme tokens applied to button
        assert "var(--bg-card)" in css
        assert "var(--border-glass)" in css
        assert "var(--text-primary)" in css


def test_huggingface_token_control_contract():
    """Verify Hugging Face token entry is clearly labelled, password masked, and secure."""
    # Test with custom environment token
    test_secret = "hf_SecretDummyToken12345"
    os.environ["HF_TOKEN"] = test_secret
    try:
        at = AppTest.from_file(APP_PATH, default_timeout=60).run()
        assert not at.exception, f"App threw exception on load: {at.exception}"

        # 1. Token input exists in sidebar with key 'hf_token_input'
        token_inputs = [ti for ti in at.sidebar.text_input if ti.key == "hf_token_input"]
        assert len(token_inputs) == 1, "Expected exactly 1 hf_token_input widget in sidebar"

        token_input = token_inputs[0]
        # 2. Must be clearly labelled
        assert "Hugging Face Token" in token_input.label
        # 3. Must be password type (masked)
        assert getattr(token_input, "type", None) == "password" or token_input.proto.type in (1, "password") or token_input.proto.autocomplete == "new-password"
        # 4. Must fall back to environment variable
        assert token_input.value == test_secret

        # 5. Must NEVER leak the secret in any markdown element
        for md in at.markdown:
            assert test_secret not in str(md.value), f"Secret leaked in markdown: {md.value}"
        for cap in at.caption:
            assert test_secret not in str(cap.value), f"Secret leaked in caption: {cap.value}"

    finally:
        os.environ.pop("HF_TOKEN", None)


def test_upload_area_shows_token_accessibility_status():
    """Verify that uploading audio displays token status and clear access instructions."""
    # Run with empty token
    os.environ.pop("HF_TOKEN", None)
    at = AppTest.from_file(APP_PATH, default_timeout=60).run()
    assert not at.exception

    # Upload audio file
    at.file_uploader[0].upload("sample.wav", b"RIFF dummy bytes").run(timeout=30)
    assert not at.exception

    # Upload area should have a warning directing user to navigation menu
    all_warnings = [w.value for w in at.warning]
    assert any("Hugging Face Token required" in w and "navigation menu" in w for w in all_warnings), (
        f"Expected token warning in upload area. Found warnings: {all_warnings}"
    )
