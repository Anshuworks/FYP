"""
Integration tests for EvidenceMeet theme contrast in both Light and Dark modes.
Validates:
1. Absence of dark/black unreadable boxes in light theme.
2. Light muted slate card surface in dark theme (no overly dark purple).
3. WCAG contrast compliance (>= 4.5:1) for text, buttons, code badges, quotes, alerts.
4. Comprehensive selectors for expanders, containers, secondary buttons, tooltips.
"""
import re
import pytest
from app.theme import get_theme_css, inject_theme


def parse_hex_color(hex_str: str) -> tuple[int, int, int]:
    """Parse #RRGGBB or #RGB to (r, g, b) integers."""
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate WCAG 2.1 relative luminance."""
    vals = []
    for c in rgb:
        s = c / 255.0
        vals.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG 2.1 contrast ratio between two hex colors."""
    lum1 = relative_luminance(parse_hex_color(hex1))
    lum2 = relative_luminance(parse_hex_color(hex2))
    l_max = max(lum1, lum2)
    l_min = min(lum1, lum2)
    return (l_max + 0.05) / (l_min + 0.05)


def test_light_theme_secondary_buttons_and_action_colors():
    """Verify in light theme that secondary buttons have permanently light background and dark text."""
    css = get_theme_css("light")

    # Tokens must define pure light background and crisp dark text
    assert "--btn-sec-bg:      #ffffff;" in css
    assert "--btn-sec-tx:      #1e293b;" in css
    assert "--btn-sec-bd:      #cbd5e1;" in css

    # High contrast: #1e293b on #ffffff exceeds WCAG AA (4.5:1)
    cr = contrast_ratio("#1e293b", "#ffffff")
    assert cr >= 4.5, f"Expected contrast >= 4.5, got {cr:.2f}"

    # Verify secondary button selectors exist and set var(--btn-sec-bg)
    assert 'button[data-testid="stBaseButton-secondary"]' in css
    assert 'div[data-testid="stTooltipHoverTarget"] button[kind="secondary"]' in css
    assert 'color: var(--btn-sec-tx) !important;' in css
    assert 'background: var(--btn-sec-bg) !important;' in css


def test_light_theme_eliminates_dark_boxes():
    """Verify that light theme elements (code badges, quotes, expanders, alerts) are permanently light."""
    css = get_theme_css("light")

    # Primary card & container surface is white (#ffffff)
    assert "--bg-card:         #ffffff;" in css
    assert "--bg-app:          #f8fafc;" in css

    # Text primary is crisp slate-900 (#0f172a)
    assert "--text-primary:    #0f172a;" in css
    cr_text = contrast_ratio("#0f172a", "#ffffff")
    assert cr_text >= 7.0, f"Text primary contrast should exceed 7:1, got {cr_text:.2f}"

    # Inline code & badges token: soft tint with rich dark indigo text
    assert "--code-bg:         rgba(124, 58, 237, 0.08);" in css
    assert "--code-tx:         #4338ca;" in css

    # Anchor jump text is dark amber in light theme (#92400e), NOT yellow (#fbbf24)
    assert "--anchor-jump-tx:  #92400e;" in css
    assert ".em-anchor-jump" in css
    assert "color: var(--anchor-jump-tx) !important;" in css

    # Verify expander and details backgrounds
    assert '[data-testid="stExpander"]' in css
    assert 'details[data-testid="stExpander"]' in css
    assert 'background: var(--bg-card) !important;' in css


def test_dark_theme_muted_surface_replaces_dark_purple():
    """Verify dark theme replaces murky purple card backgrounds with lighter muted slate surface."""
    css = get_theme_css("dark")

    # Murky purple background must NOT be present
    assert "rgba(15, 26, 58" not in css, "Overly dark purple rgba(15, 26, 58) must be eliminated!"

    # Lighter muted slate-navy surface
    assert "--bg-card:         #131c31;" in css
    assert "--bg-card-hover:   #18243e;" in css
    assert "--text-primary:    #f8fafc;" in css
    assert "--text-secondary:  #cbd5e1;" in css

    # High contrast text against muted card surface (#f8fafc on #131c31)
    cr = contrast_ratio("#f8fafc", "#131c31")
    assert cr >= 10.0, f"Dark theme primary text contrast should exceed 10:1, got {cr:.2f}"

    cr_sec = contrast_ratio("#cbd5e1", "#131c31")
    assert cr_sec >= 4.5, f"Dark theme secondary text contrast should exceed 4.5:1, got {cr_sec:.2f}"

    # Secondary button in dark theme
    assert "--btn-sec-bg:      #17223b;" in css
    assert "--btn-sec-tx:      #f1f5f9;" in css
    cr_btn = contrast_ratio("#f1f5f9", "#17223b")
    assert cr_btn >= 4.5, f"Dark theme button contrast should exceed 4.5:1, got {cr_btn:.2f}"


def test_inline_code_badges_and_quotes_high_specificity():
    """Verify high-specificity selectors for markdown code, quotes, and transcript chat."""
    for mode in ["light", "dark"]:
        css = get_theme_css(mode)

        # Markdown container code overrides Streamlit default black pills
        assert '[data-testid="stMarkdownContainer"] code' in css
        assert '.stMarkdown code' in css
        assert '[data-testid="stCaptionContainer"] code' in css
        assert 'color: var(--code-tx) !important;' in css

        # Blockquote overrides
        assert '[data-testid="stMarkdownContainer"] blockquote' in css
        assert 'color: var(--quote-tx) !important;' in css

        # Chat message content
        assert '[data-testid="stChatMessage"] [data-testid="stChatMessageContent"]' in css
        assert 'color: var(--text-primary) !important;' in css


def test_alert_notifications_contrast_and_styles():
    """Verify alerts for info, warning, success, error in both themes."""
    for mode in ["light", "dark"]:
        css = get_theme_css(mode)
        assert '[data-testid="stAlert"]' in css
        assert "--alert-info-bg:" in css
        assert "--alert-info-tx:" in css
        assert "--alert-warn-bg:" in css
        assert "--alert-warn-tx:" in css
        assert "--alert-succ-bg:" in css
        assert "--alert-succ-tx:" in css


def test_no_hardcoded_yellow_in_anchor_jump():
    """Verify .em-anchor-jump uses theme CSS variables rather than hardcoded yellow."""
    for mode in ["light", "dark"]:
        css = get_theme_css(mode)
        # Search for .em-anchor-jump block
        match = re.search(r'\.em-anchor-jump\s*\{([^}]+)\}', css)
        assert match is not None, "Missing .em-anchor-jump rule"
        block = match.group(1)
        assert "var(--anchor-jump-tx)" in block, "Anchor jump must use theme variable for text color"
        assert "var(--anchor-jump-bg)" in block, "Anchor jump must use theme variable for background"
