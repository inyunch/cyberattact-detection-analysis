"""
Centralized theme configuration following DESIGN_RULES.md
This module provides consistent color palettes and theming across the dashboard.
"""

# Design System Colors - Based on DESIGN_RULES.md
COLORS = {
    # Backgrounds
    "bg_primary": "#141B2D",
    "bg_secondary": "#1F2A40",
    "bg_tertiary": "#0F1520",
    "bg_hover": "#2A3650",

    # Text Colors
    "text_primary": "#E8EAF0",
    "text_secondary": "#A0A7B8",
    "text_muted": "#6C7489",

    # Accent Colors
    "accent_blue": "#00D9FF",
    "accent_green": "#00FFB3",
    "accent_purple": "#7B61FF",
    "accent_orange": "#FF9F43",
    "accent_red": "#FF5370",

    # Borders & Dividers
    "border_color": "#2E3A52",

    # Chart Palette (5 colors for variety)
    "chart_palette": ["#00D9FF", "#00FFB3", "#7B61FF", "#FF9F43", "#60A5FA"],
}

# Shadow definitions
SHADOWS = {
    "sm": "0 2px 8px rgba(0, 0, 0, 0.3)",
    "md": "0 4px 16px rgba(0, 0, 0, 0.4)",
    "lg": "0 8px 32px rgba(0, 0, 0, 0.5)",
    "glow": "0 8px 32px rgba(0, 217, 255, 0.2)",
}

# Gradients
GRADIENTS = {
    "primary": "linear-gradient(135deg, #00D9FF 0%, #00FFB3 100%)",
    "background": "linear-gradient(180deg, #141B2D 0%, #0A0F1C 100%)",
    "active": "linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%)",
}

# Typography
FONTS = {
    "primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "monospace": "'JetBrains Mono', 'Consolas', 'Monaco', monospace",
}

# Transitions
TRANSITIONS = {
    "fast": "0.15s cubic-bezier(0.4, 0, 0.2, 1)",
    "base": "0.25s cubic-bezier(0.4, 0, 0.2, 1)",
    "slow": "0.35s cubic-bezier(0.4, 0, 0.2, 1)",
}


import streamlit as st

def get_plotly_theme():
    """
    Returns Plotly theme configuration matching design rules.
    Use this for all Plotly charts to ensure consistency.
    """
    return {
        "paper_bgcolor": COLORS["bg_secondary"],
        "plot_bgcolor": COLORS["bg_secondary"],
        "font": {
            "family": FONTS["primary"],
            "size": 12,
            "color": COLORS["text_primary"]
        },
        "xaxis": {
            "gridcolor": COLORS["border_color"],
            "zeroline": False,
            "title_font": {"size": 12, "color": COLORS["text_muted"]},
            "tickfont": {"size": 11, "color": COLORS["text_secondary"]}
        },
        "yaxis": {
            "gridcolor": COLORS["border_color"],
            "zeroline": False,
            "title_font": {"size": 12, "color": COLORS["text_muted"]},
            "tickfont": {"size": 11, "color": COLORS["text_secondary"]}
        },
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "font": {"size": 11, "color": COLORS["text_secondary"]}
        },
        "colorway": COLORS["chart_palette"],
        "margin": {"t": 40, "b": 30, "l": 30, "r": 30}
    }


def apply_plotly_theme(fig, title: str = None):
    """
    Apply consistent theme to a Plotly figure with optional title.

    Args:
        fig: Plotly figure object
        title: Chart title. If None (default), extracts from fig.layout.title.text if present.
               If empty string "", no title is displayed.
               If non-empty string, uses that as the title.

    Returns:
        Modified figure with theme applied
    """
    theme = get_plotly_theme()

    # Extract existing title from plotly express if title parameter not provided
    final_title = None
    if title is None:
        # Try to extract existing title
        try:
            existing = getattr(fig.layout, 'title', None)
            if existing:
                existing_text = getattr(existing, 'text', None)
                if existing_text and isinstance(existing_text, str):
                    text = existing_text.strip()
                    # Only use if it's a valid, non-empty string
                    if text and text.lower() not in ("undefined", "none", "null", "nan"):
                        final_title = text
        except Exception:
            pass
    elif isinstance(title, str):
        text = title.strip()
        # Only use if it's a valid, non-empty string
        if text and text.lower() not in ("undefined", "none", "null", "nan"):
            final_title = text

    # Apply theme first
    fig.update_layout(**theme)

    # Add title outside the chart area if we have a valid one
    if final_title:
        fig.update_layout(
            title=dict(
                text=final_title,
                x=0.5,
                y=0.98,
                xanchor='center',
                yanchor='top',
                font=dict(
                    size=13,
                    color=COLORS["text_primary"],
                    family=FONTS["primary"],
                    weight=600
                ),
                pad=dict(t=10, l=0, b=15)
            ),
            margin=dict(t=60, b=50, l=50, r=50)
        )
    else:
        # No title - use smaller top margin
        fig.update_layout(margin=dict(t=40, b=50, l=50, r=50))

    return fig


def add_inplot_title(fig, text: str):
    """Add a top-left, in-plot title annotation using the same style as apply_plotly_theme.
    Does nothing if text is empty/undefined/null.
    """
    if text is None:
        return fig
    t = str(text).strip()
    if t == "" or t.lower() in ("undefined", "none", "null"):
        return fig
    ann = dict(
        text=t,
        x=0.01, y=0.99,
        xref='paper', yref='paper',
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left',
        font=dict(size=16, color=COLORS["text_primary"], family=FONTS["primary"]),
        bgcolor='rgba(15,21,32,0.55)'
    )
    try:
        existing_anns = list(fig.layout.annotations) if getattr(fig.layout, 'annotations', None) else []
        # remove previous title-like anno
        filtered = []
        for a in existing_anns:
            try:
                keep = not (getattr(a, 'xref', None) == 'paper' and getattr(a, 'yref', None) == 'paper' and getattr(a, 'x', 1) <= 0.02 and getattr(a, 'y', 0) >= 0.98)
            except Exception:
                keep = True
            if keep:
                filtered.append(a)
        filtered.insert(0, ann)
        fig.update_layout(annotations=filtered, margin=dict(t=48), xaxis=dict(automargin=True), yaxis=dict(automargin=True))
    except Exception:
        # fallback to classic layout title
        fig.update_layout(title=dict(text=t, x=0, xanchor='left'))
    return fig

def st_observation_box(observation_text: str, main_text: str):
    st.markdown(f"""
    <div style="
        background-color: {COLORS["bg_tertiary"]}; /* Dark background */
        border-left: 5px solid {COLORS["accent_blue"]}; /* Blue border */
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        color: {COLORS["text_primary"]}; /* Default text color */
    ">
        <span style="color: black;"><strong>{observation_text}</strong></span> {main_text}
    </div>
    """, unsafe_allow_html=True)

def st_dark_box(text: str):
    st.markdown(f"""
    <div style="
        background-color: {COLORS["bg_tertiary"]}; /* Dark background */
        border-left: 5px solid {COLORS["border_color"]}; /* A subtle border */
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        color: {COLORS["text_primary"]}; /* Default text color */
    ">
        {text}
    </div>
    """, unsafe_allow_html=True)

def apply_dashboard_css(sidebar_width: int = 300):
    """
    Apply comprehensive dashboard CSS styling using Streamlit markdown.
    This centralizes all UI styling to maintain consistency across the application.

    Args:
        sidebar_width: Width of the sidebar in pixels (default 300).
    """

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* CSS Variables */
        :root {{
            --bg-primary: {COLORS["bg_primary"]};
            --bg-secondary: {COLORS["bg_secondary"]};
            --bg-tertiary: {COLORS["bg_tertiary"]};
            --bg-hover: {COLORS["bg_hover"]};
            --text-primary: {COLORS["text_primary"]};
            --text-secondary: {COLORS["text_secondary"]};
            --text-muted: {COLORS["text_muted"]};
            --accent-blue: {COLORS["accent_blue"]};
            --accent-green: {COLORS["accent_green"]};
            --accent-purple: {COLORS["accent_purple"]};
            --accent-orange: {COLORS["accent_orange"]};
            --accent-red: {COLORS["accent_red"]};
            --border-color: {COLORS["border_color"]};
            --shadow-sm: {SHADOWS["sm"]};
            --shadow-md: {SHADOWS["md"]};
            --shadow-lg: {SHADOWS["lg"]};
            --transition-fast: {TRANSITIONS["fast"]};
            --transition-base: {TRANSITIONS["base"]};
        }}

        /* Global Styles */
        * {{
            font-family: {FONTS["primary"]};
        }}

        /* Main Content */
        .main {{
            background: {GRADIENTS["background"]};
        }}

        .block-container {{
            padding: 3rem 2rem;
            max-width: 100%;
        }}

        /* Ensure all content containers have dark backgrounds */
        .element-container,
        .stElementContainer,
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="column"] {{
            background-color: transparent !important;
        }}

        /* Column containers should not have light backgrounds */
        .row-widget.stHorizontal > div,
        [data-testid="column"] > div {{
            background-color: transparent !important;
        }}

        /* Override any Streamlit default white/light backgrounds */
        .stApp,
        .stApp > header,
        .stApp [data-testid="stAppViewContainer"],
        .stApp [data-testid="stHeader"],
        section[tabindex="0"],
        .main .block-container {{
            background-color: transparent !important;
        }}

        /* Ensure no white backgrounds anywhere */
        div[style*="background-color: white"],
        div[style*="background-color: #fff"],
        div[style*="background-color: #ffffff"],
        div[style*="background: white"],
        div[style*="background: #fff"],
        div[style*="background: #ffffff"] {{
            background-color: transparent !important;
            background: transparent !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {GRADIENTS["background"]};
            border-right: 1px solid var(--border-color);
            min-width: {sidebar_width}px !important;
            width: {sidebar_width}px !important;
            max-width: {sidebar_width}px !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: {GRADIENTS["background"]};
            padding-top: 0rem;
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 0rem;
        }}

        /* Remove white background from navigation component containers */
        [data-testid="stSidebar"] .stElementContainer,
        [data-testid="stSidebar"] .element-container,
        [data-testid="stSidebar"] iframe,
        [data-testid="stSidebar"] .stCustomComponentV1,
        [data-testid="stSidebar"] [class*="st-emotion-cache"],
        [data-testid="stSidebar"] div[class*="e1mlolmg"],
        [data-testid="stSidebar"] div[class*="e196pkbe"],
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        /* Hide entire sidebar header section */
        [data-testid="stSidebarHeader"],
        [data-testid="stLogoSpacer"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stSidebar"] button[kind="header"],
        [data-testid="stSidebar"] button[kind="headerNoPadding"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary);
            font-family: {FONTS["primary"]};
            letter-spacing: -0.02em;
        }}

        h1 {{
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.2;
            background: {GRADIENTS["primary"]};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            border: none;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}

        h2 {{
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.3;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }}

        h3 {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.4;
            color: var(--text-primary);
        }}

        h4 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        h5, h6 {{
            color: var(--text-secondary);
        }}

        /* Streamlit Markdown Headings - Only for markdown content */
        .stMarkdown h1,
        [data-testid="stMarkdownContainer"] h1 {{
            color: var(--text-primary) !important;
            background: {GRADIENTS["primary"]};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stMarkdown h2,
        [data-testid="stMarkdownContainer"] h2 {{
            color: var(--text-secondary) !important;
        }}

        .stMarkdown h3,
        [data-testid="stMarkdownContainer"] h3 {{
            color: var(--accent-blue) !important;
        }}

        .stMarkdown h4,
        [data-testid="stMarkdownContainer"] h4 {{
            color: var(--accent-green) !important;
        }}

        .stMarkdown h5,
        [data-testid="stMarkdownContainer"] h5 {{
            color: var(--text-secondary) !important;
        }}

        .stMarkdown h6,
        [data-testid="stMarkdownContainer"] h6 {{
            color: var(--text-secondary) !important;
        }}

        /* Streamlit Markdown Text Elements */
        .stMarkdown p,
        [data-testid="stMarkdownContainer"] p {{
            color: var(--text-secondary) !important;
        }}

        .stMarkdown strong,
        [data-testid="stMarkdownContainer"] strong {{
            color: var(--text-primary) !important;
        }}

        .stMarkdown li,
        [data-testid="stMarkdownContainer"] li {{
            color: var(--text-secondary) !important;
        }}

        p, li, span {{
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.6;
        }}

        /* Metric Cards */
        [data-testid="stMetric"] {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 14px;
            box-shadow: var(--shadow-md);
            transition: all var(--transition-base);
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 140px;
            text-align: center;
        }}

        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
            border-color: var(--accent-blue);
        }}

        [data-testid="stMetric"] label {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}

        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 2.0rem;
            font-weight: 800;
            color: var(--text-primary);
            font-family: {FONTS["monospace"]};
            letter-spacing: -0.02em;
        }}

        /* Charts & DataFrames */
        .stPlotlyChart, [data-testid="stDataFrame"] {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 12px;
            box-shadow: var(--shadow-md);
        }}

        /* Plotly Chart Titles */
        .stPlotlyChart .gtitle,
        .stPlotlyChart text.gtitle,
        .js-plotly-plot .plotly text.gtitle {{
            fill: var(--text-primary) !important;
        }}

        /* All SVG text in Plotly charts should be visible */
        .stPlotlyChart svg text,
        .js-plotly-plot svg text {{
            fill: var(--text-secondary) !important;
        }}

        .stPlotlyChart svg text.gtitle {{
            fill: var(--text-primary) !important;
        }}

        /* Expanders */
        [data-testid="stExpander"] {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
        }}

        [data-testid="stExpander"] summary {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        /* Buttons */
        .stButton > button {{
            background: {GRADIENTS["primary"]};
            color: var(--bg-primary);
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            font-family: {FONTS["primary"]};
            transition: all var(--transition-fast);
            box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 217, 255, 0.4);
        }}

        .stButton > button:active {{
            transform: translateY(0);
        }}

        /* Secondary Buttons */
        .stButton > button[kind="secondary"] {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            box-shadow: none;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            color: var(--accent-blue);
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 8px;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: var(--text-secondary);
            font-weight: 500;
            transition: all var(--transition-fast);
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background: var(--bg-hover);
            color: var(--text-primary);
        }}

        .stTabs [aria-selected="true"] {{
            background: {GRADIENTS["active"]};
            color: var(--text-primary);
            font-weight: 600;
            box-shadow: inset 0 0 20px rgba(0, 217, 255, 0.1);
        }}

        /* Input Fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stMultiSelect > div {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
        }}

        /* Slider */
        .stSlider > div > div > div > div {{
            background: var(--accent-blue);
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--border-color);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--bg-hover);
        }}

        /* Sidebar Navigation Buttons */
        div[data-testid="stSidebar"] .stButton > button,
        div[data-testid="stSidebar"] .stButton button,
        div[data-testid="stSidebar"] button {{
            background: transparent !important;
            background-color: transparent !important;
            background-image: {GRADIENTS["active"]} !important;
            color: {COLORS["accent_blue"]} !important;
            border: 1.5px solid rgba(0, 217, 255, 0.5) !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            padding: 10px 16px !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            margin: 0 0 4px 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }}

        div[data-testid="stSidebar"] .stButton > button:hover,
        div[data-testid="stSidebar"] button:hover {{
            background-image: linear-gradient(135deg, rgba(0, 217, 255, 0.25) 0%, rgba(0, 255, 179, 0.25) 100%) !important;
            border-color: {COLORS["accent_blue"]} !important;
            color: {COLORS["accent_green"]} !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3) !important;
        }}

        div[data-testid="stSidebar"] button:active {{
            transform: translateY(0) !important;
        }}

        /* Accessibility - Reduced Motion */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}

        /* Responsive Adjustments */
        @media (max-width: 768px) {{
            .block-container {{
                padding: 1.5rem;
            }}

            h1 {{
                font-size: 1.75rem;
            }}

            [data-testid="stMetric"] [data-testid="stMetricValue"] {{
                font-size: 2rem;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)
