"""
EvidenceMeet — Centralized CSS Theme
Defines Dark and Light themes with design tokens, glassmorphism, responsive
typography, and component styles. Injected via inject_theme().
"""

def get_theme_css(theme: str = "dark") -> str:
    """Generate complete CSS for the requested theme ('dark' or 'light')."""
    is_light = (theme.lower() == "light")

    if is_light:
        tokens = """
  --bg-app:          #f8fafc;
  --bg-sidebar:      linear-gradient(180deg, #f1f5f9 0%, #ffffff 100%);
  --bg-card:         #ffffff;
  --bg-card-hover:   #f8fafc;
  --bg-input:        #ffffff;
  --bg-header:       linear-gradient(135deg, #ffffff 0%, rgba(124, 58, 237, 0.08) 100%);
  --border-glass:    rgba(124, 58, 237, 0.18);
  --border-focus:    #7c3aed;
  --border-subtle:   #e2e8f0;
  --text-primary:    #0f172a;
  --text-secondary:  #334155;
  --text-muted:      #64748b;
  --accent-violet:   #7c3aed;
  --accent-violet-light: #6d28d9;
  --accent-blue:     #2563eb;
  --accent-cyan:     #0891b2;
  --accent-emerald:  #059669;
  --accent-amber:    #d97706;
  --accent-rose:     #dc2626;
  --badge-ver-bg:    rgba(16, 185, 129, 0.12);
  --badge-ver-bd:    rgba(16, 185, 129, 0.45);
  --badge-ver-tx:    #047857;
  --badge-par-bg:    rgba(245, 158, 11, 0.12);
  --badge-par-bd:    rgba(245, 158, 11, 0.45);
  --badge-par-tx:    #b45309;
  --badge-unv-bg:    rgba(239, 68, 68, 0.12);
  --badge-unv-bd:    rgba(239, 68, 68, 0.45);
  --badge-unv-tx:    #b91c1c;
  --audio-filter:    none;
  --tbl-th-bg:       #ede9fe;
  --tbl-th-tx:       #4338ca;
  --tbl-row-hover:   rgba(124, 58, 237, 0.05);
  --tbl-border:      #e2e8f0;
  --shadow-card:     0 4px 20px rgba(0, 0, 0, 0.06);
  --shadow-glow:     0 0 24px rgba(124, 58, 237, 0.14);
  --code-bg:         rgba(124, 58, 237, 0.08);
  --code-tx:         #4338ca;
  --quote-bg:        rgba(124, 58, 237, 0.04);
  --quote-tx:        #1d4ed8;
  --title-gradient:  linear-gradient(135deg, #0f172a 0%, #6d28d9 60%, #2563eb 100%);
  --btn-proc-bg:     linear-gradient(135deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
  --btn-proc-hover:  linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
  --btn-proc-tx:     #064e3b;
  --btn-proc-bd:     rgba(16, 185, 129, 0.45);
  --btn-proc-shadow: 0 3px 12px rgba(16, 185, 129, 0.20);
  --btn-proc-shadow-hov: 0 5px 16px rgba(16, 185, 129, 0.30);
  --btn-sec-bg:      #ffffff;
  --btn-sec-hover:   #f1f5f9;
  --btn-sec-tx:      #1e293b;
  --btn-sec-bd:      #cbd5e1;
  --btn-sec-shadow:  0 1px 3px rgba(0, 0, 0, 0.06);
  --btn-sec-shadow-hov: 0 3px 8px rgba(0, 0, 0, 0.10);
  --tooltip-bg:      rgba(15, 23, 42, 0.95);
  --tooltip-tx:      #f8fafc;
  --tooltip-bd:      rgba(16, 185, 129, 0.40);
  --alert-info-bg:   #eff6ff;
  --alert-info-tx:   #1e40af;
  --alert-info-bd:   #bfdbfe;
  --alert-warn-bg:   #fffbeb;
  --alert-warn-tx:   #92400e;
  --alert-warn-bd:   #fde68a;
  --alert-succ-bg:   #f0fdf4;
  --alert-succ-tx:   #166534;
  --alert-succ-bd:   #bbf7d0;
  --anchor-jump-bg:  rgba(217, 119, 6, 0.10);
  --anchor-jump-bd:  rgba(217, 119, 6, 0.35);
  --anchor-jump-tx:  #92400e;
"""
    else:
        tokens = """
  --bg-app:          #0a0f1d;
  --bg-sidebar:      linear-gradient(180deg, #0d1527 0%, #0a0f1d 100%);
  --bg-card:         #131c31;
  --bg-card-hover:   #18243e;
  --bg-input:        #0e1526;
  --bg-header:       linear-gradient(135deg, #131d33 0%, rgba(99, 102, 241, 0.16) 100%);
  --border-glass:    rgba(148, 163, 184, 0.16);
  --border-focus:    #818cf8;
  --border-subtle:   rgba(148, 163, 184, 0.08);
  --text-primary:    #f8fafc;
  --text-secondary:  #cbd5e1;
  --text-muted:      #94a3b8;
  --accent-violet:   #818cf8;
  --accent-violet-light: #a5b4fc;
  --accent-blue:     #60a5fa;
  --accent-cyan:     #22d3ee;
  --accent-emerald:  #34d399;
  --accent-amber:    #fbbf24;
  --accent-rose:     #f87171;
  --badge-ver-bg:    rgba(52, 211, 153, 0.15);
  --badge-ver-bd:    rgba(52, 211, 153, 0.40);
  --badge-ver-tx:    #34d399;
  --badge-par-bg:    rgba(251, 191, 36, 0.15);
  --badge-par-bd:    rgba(251, 191, 36, 0.40);
  --badge-par-tx:    #fbbf24;
  --badge-unv-bg:    rgba(248, 113, 113, 0.15);
  --badge-unv-bd:    rgba(248, 113, 113, 0.40);
  --badge-unv-tx:    #f87171;
  --audio-filter:    invert(0.85) hue-rotate(200deg);
  --tbl-th-bg:       #17223b;
  --tbl-th-tx:       #c7d2fe;
  --tbl-row-hover:   rgba(99, 102, 241, 0.08);
  --tbl-border:      rgba(148, 163, 184, 0.12);
  --shadow-card:     0 4px 24px rgba(0, 0, 0, 0.40);
  --shadow-glow:     0 0 32px rgba(99, 102, 241, 0.18);
  --code-bg:         #1a2540;
  --code-tx:         #c7d2fe;
  --quote-bg:        #162038;
  --quote-tx:        #93c5fd;
  --title-gradient:  linear-gradient(135deg, #f8fafc 0%, #c7d2fe 60%, #93c5fd 100%);
  --btn-proc-bg:     linear-gradient(135deg, #059669 0%, #10b981 40%, #34d399 100%);
  --btn-proc-hover:  linear-gradient(135deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
  --btn-proc-tx:     #022c22;
  --btn-proc-bd:     rgba(52, 211, 153, 0.45);
  --btn-proc-shadow: 0 3px 14px rgba(16, 185, 129, 0.25);
  --btn-proc-shadow-hov: 0 6px 20px rgba(16, 185, 129, 0.35);
  --btn-sec-bg:      #17223b;
  --btn-sec-hover:   #1e2c4c;
  --btn-sec-tx:      #f1f5f9;
  --btn-sec-bd:      rgba(148, 163, 184, 0.25);
  --btn-sec-shadow:  0 2px 8px rgba(0, 0, 0, 0.20);
  --btn-sec-shadow-hov: 0 4px 12px rgba(0, 0, 0, 0.30);
  --tooltip-bg:      rgba(10, 16, 34, 0.96);
  --tooltip-tx:      #e2e8f0;
  --tooltip-bd:      rgba(52, 211, 153, 0.35);
  --alert-info-bg:   rgba(37, 99, 235, 0.16);
  --alert-info-tx:   #93c5fd;
  --alert-info-bd:   rgba(96, 165, 250, 0.35);
  --alert-warn-bg:   rgba(217, 119, 6, 0.16);
  --alert-warn-tx:   #fde68a;
  --alert-warn-bd:   rgba(251, 191, 36, 0.35);
  --alert-succ-bg:   rgba(5, 150, 105, 0.16);
  --alert-succ-tx:   #6ee7b7;
  --alert-succ-bd:   rgba(52, 211, 153, 0.35);
  --anchor-jump-bg:  rgba(251, 191, 36, 0.15);
  --anchor-jump-bd:  rgba(251, 191, 36, 0.40);
  --anchor-jump-tx:  #fbbf24;
"""

    return f"""
<style>
/* ── Google Fonts ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Design Tokens ────────────────────────────────────── */
:root {{
{tokens}
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* ── Global Reset & Base ──────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {{
  background: var(--bg-app) !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', sans-serif !important;
}}

[data-testid="stMain"] {{
  background: transparent !important;
}}

/* Hide default streamlit header / footer branding while preserving navigation controls */
#MainMenu, footer, [data-testid="stToolbarActions"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
  display: none !important;
}}

/* Allow stHeader to pass through clicks except for navigation controls */
[data-testid="stHeader"] {{
  background: transparent !important;
  color: transparent !important;
  pointer-events: none !important;
  height: 0 !important;
  min-height: 0 !important;
  border: none !important;
  z-index: 99999 !important;
}}

[data-testid="stHeader"] > * {{
  pointer-events: none !important;
}}

[data-testid="stToolbar"] {{
  background: transparent !important;
  pointer-events: none !important;
}}

/* ── Always-visible Fixed Navigation Restore / Expand Button ── */
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] {{
  display: flex !important;
  visibility: visible !important;
  pointer-events: auto !important;
  position: fixed !important;
  top: 14px !important;
  left: 14px !important;
  z-index: 100000 !important;
  width: 38px !important;
  height: 38px !important;
  align-items: center !important;
  justify-content: center !important;
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-card) !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  opacity: 1 !important;
}}

[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover {{
  background: var(--bg-card-hover) !important;
  border-color: var(--border-focus) !important;
  transform: scale(1.05) !important;
  box-shadow: var(--shadow-glow) !important;
}}

[data-testid="stExpandSidebarButton"] button,
[data-testid="stSidebarCollapsedControl"] button {{
  background: transparent !important;
  border: none !important;
  color: var(--text-primary) !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}}

[data-testid="stExpandSidebarButton"] svg,
[data-testid="stExpandSidebarButton"] span,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] span {{
  color: var(--text-primary) !important;
  fill: var(--text-primary) !important;
  font-size: 1.25rem !important;
}}

[data-testid="stExpandSidebarButton"]:hover svg,
[data-testid="stExpandSidebarButton"]:hover span,
[data-testid="stSidebarCollapsedControl"]:hover svg,
[data-testid="stSidebarCollapsedControl"]:hover span {{
  color: var(--accent-violet) !important;
  fill: var(--accent-violet) !important;
}}

/* ── Sidebar Collapse Button inside Sidebar ── */
[data-testid="stSidebarCollapseButton"] button {{
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  transition: var(--transition) !important;
}}

[data-testid="stSidebarCollapseButton"] button:hover {{
  background: var(--bg-card-hover) !important;
  color: var(--accent-violet) !important;
}}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg-app); }}
::-webkit-scrollbar-thumb {{ background: var(--accent-violet); border-radius: 999px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent-violet-light); }}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {{
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-glass) !important;
}}
[data-testid="stSidebar"] * {{
  color: var(--text-primary) !important;
}}
[data-testid="stSidebar"] .stTextInput input {{
  background: var(--bg-input) !important;
  border: 1px solid var(--border-glass) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
}}
[data-testid="stSidebar"] .stTextInput input:focus {{
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.20) !important;
}}
[data-testid="stSidebar"] hr {{ border-color: var(--border-glass) !important; }}

/* ── File Uploader ────────────────────────────────────── */
[data-testid="stFileUploader"] {{
  background: var(--bg-card) !important;
  border: 2px dashed var(--border-glass) !important;
  border-radius: var(--radius-lg) !important;
  padding: 14px !important;
  transition: var(--transition) !important;
  backdrop-filter: blur(12px) !important;
  box-shadow: var(--shadow-card) !important;
}}
[data-testid="stFileUploader"]:hover {{
  border-color: var(--border-focus) !important;
  box-shadow: var(--shadow-glow) !important;
}}
[data-testid="stFileUploaderDropzone"] {{
  background: var(--bg-card) !important;
  border: 1px dashed var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
}}
[data-testid="stFileUploader"] * {{ color: var(--text-secondary) !important; }}
[data-testid="stFileUploaderDropzone"] button {{
  background: var(--btn-sec-bg) !important;
  color: var(--btn-sec-tx) !important;
  border: 1px solid var(--btn-sec-bd) !important;
  box-shadow: var(--btn-sec-shadow) !important;
}}
[data-testid="stFileUploaderDropzone"] button * {{
  color: var(--btn-sec-tx) !important;
}}
[data-testid="stFileUploaderDropzone"] button:hover {{
  background: var(--btn-sec-hover) !important;
  border-color: var(--border-focus) !important;
}}

/* ── Primary Process Button (Soft Mint / Light-Green Gradient) ── */
button[data-testid="stBaseButton-primary"],
button[data-testid="baseButton-primary"],
div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"],
.stButton button[kind="primary"],
div[data-testid="stTooltipHoverTarget"] button[kind="primary"],
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-primary"],
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-primary"] {{
  background: var(--btn-proc-bg) !important;
  color: var(--btn-proc-tx) !important;
  border: 1px solid var(--btn-proc-bd) !important;
  border-radius: 12px !important;
  font-family: 'Inter', -apple-system, sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  padding: 0.65rem 1.4rem !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: var(--btn-proc-shadow) !important;
  letter-spacing: 0.015em !important;
  cursor: pointer !important;
}}

/* Ensure inner label text and icons have readable high-contrast dark green color */
button[data-testid="stBaseButton-primary"] *,
button[data-testid="baseButton-primary"] *,
div[data-testid="stButton"] button[kind="primary"] *,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] *,
.stButton button[kind="primary"] *,
div[data-testid="stTooltipHoverTarget"] button[kind="primary"] *,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-primary"] *,
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-primary"] * {{
  color: var(--btn-proc-tx) !important;
  font-weight: 700 !important;
}}

/* Restrained Hover transition */
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="baseButton-primary"]:hover,
div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover,
.stButton button[kind="primary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[kind="primary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-primary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-primary"]:hover {{
  background: var(--btn-proc-hover) !important;
  transform: translateY(-1px) !important;
  box-shadow: var(--btn-proc-shadow-hov) !important;
  border-color: rgba(52, 211, 153, 0.65) !important;
}}

button[data-testid="stBaseButton-primary"]:hover *,
button[data-testid="baseButton-primary"]:hover *,
div[data-testid="stButton"] button[kind="primary"]:hover *,
div[data-testid="stTooltipHoverTarget"] button[kind="primary"]:hover * {{
  color: var(--btn-proc-tx) !important;
}}

/* Active / Click */
button[data-testid="stBaseButton-primary"]:active,
button[data-testid="baseButton-primary"]:active,
div[data-testid="stButton"] button[kind="primary"]:active,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:active,
.stButton button[kind="primary"]:active,
div[data-testid="stTooltipHoverTarget"] button[kind="primary"]:active,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-primary"]:active {{
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.18) !important;
}}

/* Restrained Focus / Focus-Visible */
button[data-testid="stBaseButton-primary"]:focus-visible,
button[data-testid="baseButton-primary"]:focus-visible,
div[data-testid="stButton"] button[kind="primary"]:focus-visible,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:focus-visible,
.stButton button[kind="primary"]:focus-visible,
div[data-testid="stTooltipHoverTarget"] button[kind="primary"]:focus-visible,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-primary"]:focus-visible {{
  outline: 2px solid #34d399 !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.25) !important;
}}

/* ── Tooltip Component (Subtle, Compact, Non-intrusive) ─ */
div[data-testid="stTooltipContent"],
div[data-testid="stTooltipContent"] > div,
div[data-baseweb="tooltip"],
div[data-baseweb="tooltip"] > div,
[data-baseweb="popover"] div[role="tooltip"] {{
  background: var(--tooltip-bg) !important;
  color: var(--tooltip-tx) !important;
  border: 1px solid var(--tooltip-bd) !important;
  border-radius: 8px !important;
  font-size: 0.74rem !important;
  line-height: 1.35 !important;
  padding: 5px 10px !important;
  max-width: 290px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.40) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  pointer-events: none !important;
  letter-spacing: 0.01em !important;
  z-index: 99999 !important;
}}

div[data-testid="stTooltipContent"] p,
div[data-baseweb="tooltip"] p,
[data-baseweb="popover"] div[role="tooltip"] p {{
  font-size: 0.74rem !important;
  line-height: 1.35 !important;
  color: var(--tooltip-tx) !important;
  margin: 0 !important;
  padding: 0 !important;
}}

/* Immediately hide tooltips when button is clicked / active */
body:has(button[data-testid="stBaseButton-primary"]:active) div[data-testid="stTooltipContent"],
body:has(button[data-testid="stBaseButton-primary"]:active) div[data-baseweb="tooltip"],
body:has(button[data-testid="stBaseButton-primary"]:active) [data-baseweb="popover"],
body:has(button[kind="primary"]:active) div[data-testid="stTooltipContent"],
body:has(button[kind="primary"]:active) div[data-baseweb="tooltip"],
body:has(button[kind="primary"]:active) [data-baseweb="popover"] {{
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
}}

/* ── Standard / Secondary / Action Buttons ─────────────── */
button[data-testid="stBaseButton-secondary"],
button[data-testid="baseButton-secondary"],
div[data-testid="stButton"] button[kind="secondary"],
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"],
.stButton button[kind="secondary"],
div[data-testid="stTooltipHoverTarget"] button[kind="secondary"],
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-secondary"],
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-secondary"],
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]),
.stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]) {{
  background: var(--btn-sec-bg) !important;
  color: var(--btn-sec-tx) !important;
  border: 1px solid var(--btn-sec-bd) !important;
  border-radius: var(--radius-md) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 0.52rem 1.15rem !important;
  transition: var(--transition) !important;
  box-shadow: var(--btn-sec-shadow) !important;
  cursor: pointer !important;
}}

/* Inner text and icons must always inherit high-contrast readable color */
button[data-testid="stBaseButton-secondary"] *,
button[data-testid="baseButton-secondary"] *,
div[data-testid="stButton"] button[kind="secondary"] *,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] *,
.stButton button[kind="secondary"] *,
div[data-testid="stTooltipHoverTarget"] button[kind="secondary"] *,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-secondary"] *,
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-secondary"] *,
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]) *,
.stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]) * {{
  color: var(--btn-sec-tx) !important;
}}

/* Hover transition */
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover,
div[data-testid="stButton"] button[kind="secondary"]:hover,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover,
.stButton button[kind="secondary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[kind="secondary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[data-testid="stBaseButton-secondary"]:hover,
div[data-testid="stTooltipHoverTarget"] button[data-testid="baseButton-secondary"]:hover,
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]):hover,
.stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]):hover {{
  background: var(--btn-sec-hover) !important;
  border-color: var(--border-focus) !important;
  transform: translateY(-1px) !important;
  box-shadow: var(--btn-sec-shadow-hov) !important;
}}

button[data-testid="stBaseButton-secondary"]:hover *,
button[data-testid="baseButton-secondary"]:hover *,
div[data-testid="stButton"] button[kind="secondary"]:hover *,
div[data-testid="stTooltipHoverTarget"] button[kind="secondary"]:hover *,
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]):hover * {{
  color: var(--btn-sec-tx) !important;
}}

/* Active state */
button[data-testid="stBaseButton-secondary"]:active,
button[data-testid="baseButton-secondary"]:active,
div[data-testid="stButton"] button[kind="secondary"]:active,
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]):active {{
  transform: translateY(0) !important;
  box-shadow: none !important;
}}

/* Focus state */
button[data-testid="stBaseButton-secondary"]:focus-visible,
button[data-testid="baseButton-secondary"]:focus-visible,
div[data-testid="stButton"] button[kind="secondary"]:focus-visible,
div[data-testid="stTooltipHoverTarget"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not([data-testid="baseButton-primary"]):focus-visible {{
  outline: 2px solid var(--border-focus) !important;
  outline-offset: 2px !important;
}}

/* Download buttons */
[data-testid="stDownloadButton"] > button,
[data-testid="stDownloadButton"] button {{
  background: rgba(34, 211, 238, 0.12) !important;
  border: 1px solid rgba(34, 211, 238, 0.35) !important;
  color: var(--accent-cyan) !important;
  font-weight: 600 !important;
  box-shadow: none !important;
}}
[data-testid="stDownloadButton"] > button *,
[data-testid="stDownloadButton"] button * {{
  color: var(--accent-cyan) !important;
  font-weight: 600 !important;
}}
[data-testid="stDownloadButton"] > button:hover,
[data-testid="stDownloadButton"] button:hover {{
  background: rgba(34, 211, 238, 0.22) !important;
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 4px 14px rgba(34, 211, 238, 0.25) !important;
  transform: translateY(-1px) !important;
}}
[data-testid="stDownloadButton"] > button:hover *,
[data-testid="stDownloadButton"] button:hover * {{
  color: var(--accent-cyan) !important;
}}

/* ── Tabs ─────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {{
  background: var(--bg-card) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--border-glass) !important;
  padding: 4px !important;
  gap: 3px !important;
  backdrop-filter: blur(12px) !important;
  box-shadow: var(--shadow-card) !important;
}}
[data-testid="stTabs"] [role="tab"] {{
  background: transparent !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.84rem !important;
  padding: 0.5rem 0.95rem !important;
  border: none !important;
  transition: var(--transition) !important;
}}
[data-testid="stTabs"] [role="tab"] * {{
  color: var(--text-secondary) !important;
}}
[data-testid="stTabs"] [role="tab"]:hover {{
  color: var(--accent-violet) !important;
  background: rgba(124, 58, 237, 0.08) !important;
}}
[data-testid="stTabs"] [role="tab"]:hover * {{
  color: var(--accent-violet) !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
  background: linear-gradient(135deg, var(--accent-violet), #4f46e5) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.40) !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] * {{
  color: #ffffff !important;
}}

/* ── Metrics ──────────────────────────────────────────── */
[data-testid="stMetric"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
  padding: 16px 20px !important;
  backdrop-filter: blur(12px) !important;
  transition: var(--transition) !important;
  box-shadow: var(--shadow-card) !important;
}}
[data-testid="stMetric"]:hover {{
  border-color: var(--border-focus) !important;
  box-shadow: var(--shadow-glow) !important;
  transform: translateY(-2px) !important;
}}
[data-testid="stMetricLabel"] {{
  color: var(--text-secondary) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.06em !important;
}}
[data-testid="stMetricLabel"] * {{
  color: var(--text-secondary) !important;
}}
[data-testid="stMetricValue"] {{
  color: var(--text-primary) !important;
  font-size: 1.55rem !important;
  font-weight: 700 !important;
  font-family: 'JetBrains Mono', monospace !important;
}}
[data-testid="stMetricValue"] * {{
  color: var(--text-primary) !important;
}}

/* ── Expanders (Collapsible sections) ─────────────────── */
[data-testid="stExpander"],
details[data-testid="stExpander"],
details {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
  backdrop-filter: blur(12px) !important;
  margin-bottom: 12px !important;
  overflow: hidden !important;
  transition: var(--transition) !important;
  box-shadow: var(--shadow-card) !important;
}}
[data-testid="stExpander"]:hover,
details[data-testid="stExpander"]:hover,
details:hover {{
  border-color: var(--border-focus) !important;
}}
[data-testid="stExpander"] summary,
details[data-testid="stExpander"] summary,
details summary {{
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  font-weight: 600 !important;
  padding: 14px 18px !important;
  font-size: 0.95rem !important;
}}
[data-testid="stExpander"] summary *,
details summary * {{
  color: var(--text-primary) !important;
}}
[data-testid="stExpander"] summary:hover,
details summary:hover {{
  color: var(--accent-violet) !important;
}}
[data-testid="stExpander"] summary:hover *,
details summary:hover * {{
  color: var(--accent-violet) !important;
}}
[data-testid="stExpander"] summary svg,
details summary svg {{
  fill: var(--accent-violet) !important;
}}
[data-testid="stExpander"] [data-testid="stExpanderDetails"],
details [data-testid="stExpanderDetails"],
details > div:not(summary) {{
  background: var(--bg-card) !important;
  padding: 14px 18px !important;
  border-top: 1px solid var(--border-glass) !important;
}}

/* Bordered container boxes */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div {{
  background: var(--bg-card) !important;
  border-color: var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
}}

/* ── Alerts & Notifications ───────────────────────────── */
[data-testid="stAlert"] {{
  border-radius: var(--radius-md) !important;
  border-width: 1px 1px 1px 4px !important;
  border-style: solid !important;
  backdrop-filter: blur(8px) !important;
  font-size: 0.88rem !important;
  padding: 12px 18px !important;
  box-shadow: var(--shadow-card) !important;
}}
/* Alert Info */
div[data-testid="stAlert"]:has([data-testid="stNotificationContentInfo"]),
[data-testid="stAlert"]:has([data-testid="stIconMaterialInfo"]),
div[data-testid="stAlert"]:has(svg[data-testid="stIconInfo"]),
.stAlert:has(.stAlert-info) {{
  background: var(--alert-info-bg) !important;
  border-color: var(--alert-info-bd) !important;
  border-left-color: var(--accent-blue) !important;
}}
div[data-testid="stAlert"]:has([data-testid="stNotificationContentInfo"]) *,
[data-testid="stAlert"]:has([data-testid="stIconMaterialInfo"]) *,
div[data-testid="stAlert"]:has(svg[data-testid="stIconInfo"]) * {{
  color: var(--alert-info-tx) !important;
}}
/* Alert Warning */
div[data-testid="stAlert"]:has([data-testid="stNotificationContentWarning"]),
[data-testid="stAlert"]:has([data-testid="stIconMaterialWarning"]),
div[data-testid="stAlert"]:has(svg[data-testid="stIconWarning"]),
.stAlert:has(.stAlert-warning) {{
  background: var(--alert-warn-bg) !important;
  border-color: var(--alert-warn-bd) !important;
  border-left-color: var(--accent-amber) !important;
}}
div[data-testid="stAlert"]:has([data-testid="stNotificationContentWarning"]) *,
[data-testid="stAlert"]:has([data-testid="stIconMaterialWarning"]) *,
div[data-testid="stAlert"]:has(svg[data-testid="stIconWarning"]) * {{
  color: var(--alert-warn-tx) !important;
}}
/* Alert Success */
div[data-testid="stAlert"]:has([data-testid="stNotificationContentSuccess"]),
[data-testid="stAlert"]:has([data-testid="stIconMaterialSuccess"]),
div[data-testid="stAlert"]:has(svg[data-testid="stIconSuccess"]),
.stAlert:has(.stAlert-success) {{
  background: var(--alert-succ-bg) !important;
  border-color: var(--alert-succ-bd) !important;
  border-left-color: var(--accent-emerald) !important;
}}
div[data-testid="stAlert"]:has([data-testid="stNotificationContentSuccess"]) *,
[data-testid="stAlert"]:has([data-testid="stIconMaterialSuccess"]) *,
div[data-testid="stAlert"]:has(svg[data-testid="stIconSuccess"]) * {{
  color: var(--alert-succ-tx) !important;
}}
/* Alert Error */
div[data-testid="stAlert"]:has([data-testid="stNotificationContentError"]),
[data-testid="stAlert"]:has([data-testid="stIconMaterialError"]),
div[data-testid="stAlert"]:has(svg[data-testid="stIconError"]),
.stAlert:has(.stAlert-error) {{
  background: var(--badge-unv-bg) !important;
  border-color: var(--badge-unv-bd) !important;
  border-left-color: var(--accent-rose) !important;
}}
div[data-testid="stAlert"]:has([data-testid="stNotificationContentError"]) *,
[data-testid="stAlert"]:has([data-testid="stIconMaterialError"]) * {{
  color: var(--badge-unv-tx) !important;
}}

/* ── Text Inputs & Textareas ──────────────────────────── */
.stTextInput input, .stTextArea textarea {{
  background: var(--bg-input) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.88rem !important;
  transition: var(--transition) !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color: var(--border-focus) !important;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.18) !important;
  outline: none !important;
}}
.stTextInput label, .stTextArea label {{
  color: var(--text-secondary) !important;
  font-size: 0.82rem !important;
}}

/* ── Radio & Toggles (Theme Switcher) ─────────────────── */
[data-testid="stRadio"] [role="radiogroup"] {{
  gap: 8px !important;
}}
[data-testid="stRadio"] label {{
  color: var(--text-primary) !important;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
}}

/* ── Audio Player ─────────────────────────────────────── */
audio {{
  width: 100% !important;
  border-radius: var(--radius-sm) !important;
  outline: none !important;
  filter: var(--audio-filter) !important;
}}

/* ── Status & Progress ────────────────────────────────── */
[data-testid="stStatus"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
  backdrop-filter: blur(12px) !important;
}}
[data-testid="stStatus"] * {{ color: var(--text-primary) !important; }}

/* ── Chat Messages (Smart Transcript) ────────────────── */
[data-testid="stChatMessage"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: var(--radius-md) !important;
  padding: 12px 16px !important;
  margin-bottom: 8px !important;
  backdrop-filter: blur(8px) !important;
  transition: var(--transition) !important;
  box-shadow: var(--shadow-card) !important;
}}
[data-testid="stChatMessage"]:hover {{
  border-color: var(--border-focus) !important;
  transform: translateX(2px) !important;
}}
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"] .stMarkdown p {{
  color: var(--text-primary) !important;
}}

/* ── Tables ───────────────────────────────────────────── */
[data-testid="stTable"] table, .stDataFrame table {{
  background: var(--bg-card) !important;
  border-collapse: separate !important;
  border-spacing: 0 !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  width: 100% !important;
}}
[data-testid="stTable"] th, .stDataFrame th {{
  background: var(--tbl-th-bg) !important;
  color: var(--tbl-th-tx) !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  padding: 12px 16px !important;
  border-bottom: 1px solid var(--border-glass) !important;
}}
[data-testid="stTable"] td, .stDataFrame td {{
  color: var(--text-primary) !important;
  padding: 11px 16px !important;
  font-size: 0.86rem !important;
  border-bottom: 1px solid var(--tbl-border) !important;
  font-family: 'JetBrains Mono', monospace !important;
}}
[data-testid="stTable"] tr:last-child td {{ border-bottom: none !important; }}
[data-testid="stTable"] tr:hover td {{ background: var(--tbl-row-hover) !important; }}

/* ── Dividers ─────────────────────────────────────────── */
hr {{ border-color: var(--border-glass) !important; }}

/* ── Markdown Headings & Text ─────────────────────────── */
h1 {{ font-size: 1.95rem !important; font-weight: 800 !important; color: var(--text-primary) !important; }}
h2 {{ font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text-primary) !important; }}
h3 {{ font-size: 1.15rem !important; font-weight: 700 !important; color: var(--accent-violet) !important; }}
h4 {{ font-size: 0.98rem !important; font-weight: 600 !important; color: var(--text-secondary) !important; }}
p, li {{ color: var(--text-secondary) !important; font-size: 0.9rem !important; }}
strong {{ color: var(--text-primary) !important; }}
code,
[data-testid="stMarkdownContainer"] code,
.stMarkdown code,
[data-testid="stCaptionContainer"] code,
[data-testid="stExpanderDetails"] code,
div[data-testid="stChatMessageContent"] code {{
  background: var(--code-bg) !important;
  color: var(--code-tx) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: 6px !important;
  padding: 2px 7px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82em !important;
  font-weight: 500 !important;
}}
blockquote,
[data-testid="stMarkdownContainer"] blockquote,
.stMarkdown blockquote,
[data-testid="stExpanderDetails"] blockquote {{
  border-left: 3px solid var(--accent-violet) !important;
  background: var(--quote-bg) !important;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
  padding: 10px 16px !important;
  margin: 8px 0 !important;
  color: var(--quote-tx) !important;
}}
blockquote *,
[data-testid="stMarkdownContainer"] blockquote *,
.stMarkdown blockquote * {{
  color: var(--quote-tx) !important;
}}
blockquote em,
[data-testid="stMarkdownContainer"] blockquote em {{
  color: var(--accent-blue) !important;
  font-style: italic !important;
}}

/* ── Caption ──────────────────────────────────────────── */
[data-testid="stCaptionContainer"] {{
  color: var(--text-muted) !important;
  font-size: 0.78rem !important;
}}

/* ── Spinner ──────────────────────────────────────────── */
[data-testid="stSpinner"] > div {{ border-top-color: var(--accent-violet) !important; }}

/* ── Custom Component Classes ─────────────────────────── */

/* Intelligence section header */
.em-section-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  background: var(--code-bg);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  margin: 14px 0 10px 0;
  backdrop-filter: blur(8px);
}}
.em-section-icon {{ font-size: 1.25rem; }}
.em-section-title {{
  font-family: 'Inter', sans-serif;
  font-size: 0.98rem;
  font-weight: 700;
  color: var(--accent-violet);
  margin: 0;
}}
.em-section-count {{
  margin-left: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: 999px;
  padding: 2px 10px;
}}

/* Intelligence item card */
.em-item-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 16px 20px;
  margin-bottom: 12px;
  backdrop-filter: blur(12px);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-card);
}}
.em-item-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 3px; height: 100%;
  background: linear-gradient(180deg, var(--accent-violet), var(--accent-blue));
  border-radius: 3px 0 0 3px;
}}
.em-item-card:hover {{
  border-color: var(--border-focus);
  box-shadow: var(--shadow-glow);
  transform: translateX(3px);
}}
.em-item-card.em-verified::before   {{ background: linear-gradient(180deg, var(--accent-emerald), #047857); }}
.em-item-card.em-partial::before    {{ background: linear-gradient(180deg, var(--accent-amber), #b45309); }}
.em-item-card.em-unverified::before {{ background: linear-gradient(180deg, var(--accent-rose), #b91c1c); }}

/* Verification badge pill */
.em-badge {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.03em;
}}
.em-badge-verified   {{ background: var(--badge-ver-bg); border: 1px solid var(--badge-ver-bd); color: var(--badge-ver-tx); }}
.em-badge-partial    {{ background: var(--badge-par-bg); border: 1px solid var(--badge-par-bd); color: var(--badge-par-tx); }}
.em-badge-unverified {{ background: var(--badge-unv-bg); border: 1px solid var(--badge-unv-bd); color: var(--badge-unv-tx); }}

/* Header branding */
.em-header-brand {{
  background: var(--bg-header);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-xl);
  padding: 24px 32px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-card);
}}
.em-header-brand::after {{
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 180px; height: 180px;
  background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
  pointer-events: none;
}}
.em-header-title {{
  font-family: 'Inter', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  background: var(--title-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 4px 0;
  line-height: 1.2;
}}
.em-header-sub {{
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  color: var(--text-muted);
  margin: 0;
  font-weight: 400;
}}

/* Sidebar brand pill */
.em-sidebar-brand {{
  background: var(--code-bg);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin-bottom: 14px;
  text-align: center;
}}
.em-sidebar-brand-name {{
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  background: var(--title-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.em-sidebar-brand-tagline {{ font-size: 0.70rem; color: var(--text-muted); }}

/* Module chip */
.em-module-chip {{
  display: inline-block;
  background: var(--code-bg);
  border: 1px solid var(--border-glass);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--accent-violet);
  padding: 2px 10px;
  margin: 3px 3px 0 0;
  font-family: 'Inter', sans-serif;
}}

/* Team member row */
.em-team-row {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--code-bg);
  border-radius: var(--radius-sm);
  margin: 4px 0;
  border: 1px solid var(--border-glass);
  font-size: 0.82rem;
}}

/* Stat pill */
.em-stat-pill {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--code-bg);
  border: 1px solid var(--border-glass);
  border-radius: 999px;
  padding: 5px 14px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
  margin: 3px 3px 3px 0;
}}
.em-stat-pill span {{ color: var(--accent-violet); }}

/* Gradient divider */
.em-gradient-divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-violet), var(--accent-blue), transparent);
  border: none;
  margin: 18px 0;
  opacity: 0.6;
}}

/* Highlighted transcript segment (pulsing animation) */
.em-highlight-segment {{
  padding: 10px 16px;
  background: var(--anchor-jump-bg) !important;
  border-left: 4px solid var(--accent-amber) !important;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin: 8px 0;
  color: var(--text-primary) !important;
  animation: em-pulse-border 2s ease-in-out infinite;
}}
.em-highlight-segment strong {{
  color: var(--text-primary) !important;
}}
@keyframes em-pulse-border {{
  0%, 100% {{ border-left-color: var(--accent-amber); box-shadow: none; }}
  50% {{ border-left-color: var(--accent-amber); box-shadow: 0 0 14px rgba(251, 191, 36, 0.35); }}
}}

/* Anchor jump link in transcript */
.em-anchor-jump {{
  display: inline-block;
  padding: 5px 12px;
  background: var(--anchor-jump-bg) !important;
  border: 1px solid var(--anchor-jump-bd) !important;
  border-radius: var(--radius-sm);
  color: var(--anchor-jump-tx) !important;
  text-decoration: none !important;
  font-size: 0.80rem;
  font-weight: 600;
  margin-top: 4px;
  transition: var(--transition);
}}
.em-anchor-jump:hover {{
  background: var(--anchor-jump-bd) !important;
  color: var(--anchor-jump-tx) !important;
}}

/* Smooth fade-in */
@keyframes em-fadein {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.em-fadein {{ animation: em-fadein 0.4s ease-out both; }}
</style>
"""


def inject_theme(theme: str = "dark"):
    """Inject the requested theme into the Streamlit app ('dark' or 'light')."""
    import streamlit as st
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)
