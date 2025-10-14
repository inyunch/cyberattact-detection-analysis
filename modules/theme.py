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


def apply_plotly_theme(fig, title=""):
    """
    Apply consistent theme to a Plotly figure.

    Args:
        fig: Plotly figure object
        title: Optional chart title

    Returns:
        Modified figure with theme applied
    """
    theme = get_plotly_theme()

    if title:
        theme["title"] = {
            "text": title,
            "x": 0,
            "xanchor": "left",
            "font": {"size": 18, "color": COLORS["text_primary"], "family": FONTS["primary"]}
        }

    fig.update_layout(**theme)
    return fig
