import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Tuple, Dict, Any, Optional

# Base color palette and typography
_BASE_COLORS = {
    "primary": "#2563EB",      # Tailwind Blue-600
    "secondary": "#0EA5E9",    # Sky-500
    "background": "#F8FAFC",   # Slate-50
    "surface": "#FFFFFF",
    "text": "#0F172A",        # Slate-900
    "muted_text": "#475569",   # Slate-600
    "grid": "#E2E8F0",        # Slate-200
    "accent": "#F59E0B",      # Amber-500
    "danger": "#DC2626",      # Red-600
    "success": "#16A34A",     # Green-600
    "blue_palette": ["#2563EB", "#0EA5E9", "#8B5CF6", "#F59E0B", "#60A5FA"],
}

FONT_FAMILY = "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"


def _init_theme_state():
    if "theme_dark" not in st.session_state:
        st.session_state.theme_dark = False
    if "brand_colors" not in st.session_state:
        st.session_state.brand_colors = {"primary": _BASE_COLORS["primary"]}
    if "saved_views" not in st.session_state:
        st.session_state.saved_views = {}
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "year_range": None, "attack_types": [], "industries": [], "countries": []
        }


def get_colors() -> Dict[str, Any]:
    """Return effective color palette considering dark mode and brand overrides.
    Includes basic auto-contrast adjustment for text against surface/background.
    """
    _init_theme_state()
    primary = st.session_state.brand_colors.get("primary", _BASE_COLORS["primary"])
    dark = bool(st.session_state.theme_dark)
    if dark:
        palette = {
            **_BASE_COLORS,
            "primary": primary,
            "background": "#0E1117",
            "surface": "#111827",
            "text": "#E5E7EB",
            "muted_text": "#9CA3AF",
            "grid": "#374151",
        }
    else:
        palette = {**_BASE_COLORS, "primary": primary}

    # Auto-contrast adjustment for text if needed
    try:
        def cr(a, b):
            return (_contrast_ratio(a, b)) if '_contrast_ratio' in globals() else 10
        surf = palette.get("surface", "#FFFFFF")
        txt = palette.get("text", "#0F172A")
        if cr(txt, surf) < 4.5:
            # pick best of black or white
            best = max(["#000000", "#FFFFFF"], key=lambda c: cr(c, surf))
            palette["text"] = best
        # ensure muted still contrasts reasonably (AA for large text 3.0)
        mtxt = palette.get("muted_text", "#475569")
        if cr(mtxt, surf) < 3.0:
            options = ["#334155", "#64748B", "#CBD5E1"] if not dark else ["#9CA3AF", "#D1D5DB", "#F3F4F6"]
            best_m = max(options, key=lambda c: cr(c, surf))
            palette["muted_text"] = best_m
    except Exception:
        pass

    return palette


def apply_base_css():
    """Inject base CSS honoring dark mode and brand color with upgraded visual polish."""
    COLORS = get_colors()
    st.markdown(
        f"""
        <style>
        .main {{ background-color: {COLORS['background']}; }}
        .block-container {{ padding-top: 1.2rem; }}
        h1, h2, h3, h4, h5, h6 {{ color: {COLORS['text']}; font-family: {FONT_FAMILY}; }}
        h1 {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }}
        h2 {{ font-size: 1.4rem; font-weight: 700; margin-top: 1.2rem; }}
        p, li, span {{ color: {COLORS['muted_text']}; font-size: 0.98rem; }}

        /* Cards and surfaces */
        .rovocard {{
            background: {COLORS['surface']};
            border: 1px solid {COLORS['grid']};
            border-radius: 14px;
            box-shadow: 0 8px 30px rgba(2, 6, 23, 0.05);
            padding: 16px 18px;
        }}

        /* Buttons */
        .stButton>button {{ background-color: {COLORS['primary']}; color: white; border: none; border-radius: 10px; padding: 10px 18px; font-weight: 600; }}
        .stButton>button:hover {{ filter: brightness(0.95); transform: translateY(-1px); }}

        /* Plot containers */
        .stPlotlyChart, .stDataFrame {{ background-color: {COLORS['surface']}; border-radius: 14px; padding: 10px; border: 1px solid {COLORS['grid']}; }}
        .streamlit-expanderHeader {{ font-weight: 700; }}
        .chip {{ display:inline-block; padding:4px 10px; border-radius:999px; background: rgba(15, 23, 42, 0.05); margin:2px 6px 0 0; font-size:0.85rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme_controls_in_sidebar(show_appearance: bool = True, show_saved_views: bool = True):
    """Render optional appearance controls (dark mode, brand color) and optional Saved Views in the sidebar."""
    _init_theme_state()

    if show_appearance:
        st.sidebar.markdown("### Appearance")
        st.session_state.theme_dark = st.sidebar.toggle("Dark mode", value=st.session_state.theme_dark)
        st.session_state.brand_colors["primary"] = st.sidebar.color_picker(
            "Brand primary color", value=st.session_state.brand_colors.get("primary", _BASE_COLORS["primary"]) 
        )

    if show_saved_views:
        st.sidebar.markdown("### Saved views")
        view_names = sorted(list(st.session_state.saved_views.keys()))
        selected_view = st.sidebar.selectbox("Load view", options=["-"] + view_names, index=0)
        cols = st.sidebar.columns([1,1,1])
        with cols[0]:
            if st.button("Load", use_container_width=True):
                if selected_view != "-":
                    load_view(selected_view)
                    st.rerun()
        with cols[1]:
            if st.button("Save", use_container_width=True):
                name = st.sidebar.text_input("View name", key="_view_name_input")
                if name:
                    save_current_view(name)
                    st.toast(f"Saved view '{name}'")
        with cols[2]:
            if st.button("Delete", use_container_width=True):
                if selected_view != "-" and selected_view in st.session_state.saved_views:
                    del st.session_state.saved_views[selected_view]
                    st.rerun()


def save_current_view(name: str):
    """Save filters and theme under a name in session_state."""
    _init_theme_state()
    st.session_state.saved_views[name] = {
        "filters": st.session_state.filters,
        "theme_dark": st.session_state.theme_dark,
        "brand_colors": st.session_state.brand_colors,
    }


def load_view(name: str):
    """Load filters and theme from a saved view into session_state."""
    _init_theme_state()
    data = st.session_state.saved_views.get(name)
    if not data:
        return
    st.session_state.filters = data.get("filters", st.session_state.filters)
    st.session_state.theme_dark = data.get("theme_dark", st.session_state.theme_dark)
    st.session_state.brand_colors = data.get("brand_colors", st.session_state.brand_colors)


def apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply a consistent Plotly theme to a figure using current colors."""
    COLORS = get_colors()
    fig.update_layout(
        title=dict(text=title, x=0, xanchor="left", font=dict(size=18, color=COLORS["text"], family=FONT_FAMILY)),
        font=dict(family=FONT_FAMILY, size=12, color=COLORS["text"]),
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        margin=dict(t=40, b=30, l=30, r=30),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            zeroline=False,
            title_font=dict(size=12, color=COLORS["muted_text"]),
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            zeroline=False,
            title_font=dict(size=12, color=COLORS["muted_text"]),
            tickfont=dict(size=11),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11)
        ),
        colorway=get_colors()["blue_palette"],
    )
    return fig


def kpi_card(title: str, value: str, delta: str = None, icon: str = "", delta_status: str = "neutral"):
    """Reusable KPI card with semantic delta colors (success/warn/danger/neutral)."""
    COLORS = get_colors()
    delta_color = {
        "success": COLORS["success"],
        "warn": COLORS["accent"],
        "danger": COLORS["danger"],
        "neutral": COLORS["muted_text"],
    }.get(delta_status, COLORS["muted_text"])

    st.markdown(f"""
    <div style=\"background:{COLORS['surface']}; border:1px solid #E5E7EB; border-left:6px solid {COLORS['primary']};
                border-radius:12px; padding:16px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);\">
      <div style=\"display:flex; justify-content:space-between; align-items:center;\">
        <div style=\"font-size:0.95rem; font-weight:600; color:{COLORS['muted_text']};\">{title}</div>
        <div style=\"font-size:1.6rem;\">{icon}</div>
      </div>
      <div style=\"font-size:2rem; font-weight:700; color:{COLORS['text']}; margin-top:6px;\">{value}</div>
      {f'<div style=\"font-size:0.9rem; color:{delta_color}; margin-top:6px;\">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)


def filter_controls(global_threats: pd.DataFrame, intrusion_data: pd.DataFrame, show_active_summary: bool = True, enable_quick_presets: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Render a compact filter bar and return filtered datasets.
    Syncs with st.session_state.filters so clicks and saved views can update it.
    Returns: filtered_global_threats, filtered_intrusion_data, filters_dict
    """
    _init_theme_state()
    COLORS = get_colors()
    with st.container():
        st.markdown("""
        <div class='rovocard' style='padding: 14px 16px;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:8px;'>
                <span style='font-size:18px;'>🔎</span>
                <h2 style='margin:0; font-size:1.1rem;'>Filters</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Grouped filter layout: When / What / Where
        when_col, what_col, where_col = st.columns([2, 3, 3])

        # Year range
        min_year = int(pd.to_numeric(global_threats.get("Year"), errors="coerce").dropna().min()) if "Year" in global_threats.columns else None
        max_year = int(pd.to_numeric(global_threats.get("Year"), errors="coerce").dropna().max()) if "Year" in global_threats.columns else None
        year_range = st.session_state.filters.get("year_range")
        with when_col:
            if min_year and max_year and min_year <= max_year:
                if not year_range:
                    year_range = (min_year, max_year)
                st.write("When")
                c_when1, c_when2 = st.columns([3, 2])
                with c_when1:
                    year_range = st.slider("Year", min_value=min_year, max_value=max_year, value=tuple(year_range), label_visibility="collapsed")
                if enable_quick_presets:
                    with c_when2:
                        if st.button("Last 3y"):
                            preset_min = max(min_year, max_year - 2)
                            year_range = (preset_min, max_year)
                        if st.button("Last 5y"):
                            preset_min = max(min_year, max_year - 4)
                            year_range = (preset_min, max_year)

        # Attack Type
        with what_col:
            st.write("What")
            attack_types = sorted(global_threats["Attack Type"].dropna().unique()) if "Attack Type" in global_threats.columns else []
            sel_attack_types = st.multiselect("Attack Type", options=attack_types, default=st.session_state.filters.get("attack_types", []))
            if enable_quick_presets and attack_types:
                c_q1, c_q2 = st.columns(2)
                with c_q1:
                    if st.button("Top 5 Attack Types"):
                        # compute contextual top5 based on selected year_range
                        df_ctx = global_threats.copy()
                        if year_range and "Year" in df_ctx.columns:
                            df_ctx = df_ctx[(df_ctx["Year"] >= year_range[0]) & (df_ctx["Year"] <= year_range[1])]
                        top5 = df_ctx["Attack Type"].value_counts().head(5).index.tolist() if "Attack Type" in df_ctx.columns else []
                        st.session_state.filters["attack_types"] = top5
                        st.rerun()
                with c_q2:
                    if st.button("Clear Attacks"):
                        st.session_state.filters["attack_types"] = []
                        st.rerun()

        # Target Industry + Country
        with where_col:
            st.write("Where")
            industries = sorted(global_threats["Target Industry"].dropna().unique()) if "Target Industry" in global_threats.columns else []
            sel_industries = st.multiselect("Target Industry", options=industries, default=st.session_state.filters.get("industries", []))
            if enable_quick_presets and industries:
                c_i1, c_i2 = st.columns(2)
                with c_i1:
                    if st.button("Top 5 Industries"):
                        df_ctx = global_threats.copy()
                        if year_range and "Year" in df_ctx.columns:
                            df_ctx = df_ctx[(df_ctx["Year"] >= year_range[0]) & (df_ctx["Year"] <= year_range[1])]
                        top5i = df_ctx["Target Industry"].value_counts().head(5).index.tolist() if "Target Industry" in df_ctx.columns else []
                        st.session_state.filters["industries"] = top5i
                        st.rerun()
                with c_i2:
                    if st.button("Clear Industries"):
                        st.session_state.filters["industries"] = []
                        st.rerun()
            countries = sorted(global_threats["Country"].dropna().unique()) if "Country" in global_threats.columns else []
            sel_countries = st.multiselect("Country", options=countries, default=st.session_state.filters.get("countries", []))

    # Apply filters to global_threats
    gt = global_threats.copy()
    if year_range and "Year" in gt.columns:
        gt = gt[(gt["Year"] >= year_range[0]) & (gt["Year"] <= year_range[1])]
    if sel_attack_types:
        gt = gt[gt["Attack Type"].isin(sel_attack_types)]
    if sel_industries:
        gt = gt[gt["Target Industry"].isin(sel_industries)]
    if sel_countries:
        gt = gt[gt["Country"].isin(sel_countries)]

    # For intrusion data we can map by year if present
    idf = intrusion_data.copy()
    if year_range and "timestamp" in idf.columns:
        ts = pd.to_datetime(idf["timestamp"], errors="coerce")
        idf = idf[(ts.dt.year >= year_range[0]) & (ts.dt.year <= year_range[1])]

    filters = {
        "year_range": year_range,
        "attack_types": sel_attack_types,
        "industries": sel_industries,
        "countries": sel_countries,
    }
    st.session_state.filters = filters

    # Active filter summary and clear
    if show_active_summary:
        chips = []
        if year_range:
            chips.append(f"<span class='chip'>Year: {year_range[0]}–{year_range[1]}</span>")
        for v in sel_attack_types:
            chips.append(f"<span class='chip'>Attack: {v}</span>")
        for v in sel_industries:
            chips.append(f"<span class='chip'>Industry: {v}</span>")
        for v in sel_countries:
            chips.append(f"<span class='chip'>Country: {v}</span>")
        if chips:
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='rovocard' style='padding:10px 12px;'>" + " ".join(chips) + "</div>", unsafe_allow_html=True)
            if st.button("Clear all filters", type="secondary"):
                # Reset back to defaults
                st.session_state.filters = {"year_range": (int(pd.to_numeric(global_threats.get("Year"), errors="coerce").dropna().min()) if "Year" in global_threats.columns else None,
                                                            int(pd.to_numeric(global_threats.get("Year"), errors="coerce").dropna().max()) if "Year" in global_threats.columns else None),
                                            "attack_types": [], "industries": [], "countries": []}
                st.rerun()

    return gt, idf, filters


def download_buttons(df: pd.DataFrame, filename: str, label: str = "Download CSV"):
    """Render a convenient CSV download button for the current filtered dataset."""
    if df is None or df.empty:
        return
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def page_hero(title: str, subtitle: str = "", emoji: str = ""):
    """Render a hero header card consistent across pages."""
    lead = f"<div style='font-size:28px;'>{emoji}</div>" if emoji else ""
    st.markdown(
        f"""
        <div class="rovocard" style="padding:20px 22px;">
            <div style="display:flex; align-items:center; gap:14px;">
                {lead}
                <div>
                    <h1 style="margin:0;">{title}</h1>
                    {f'<p style="margin:2px 0 0 0;">{subtitle}</p>' if subtitle else ''}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(f"<h2 style='margin-bottom:0.2rem;'>{text}</h2>", unsafe_allow_html=True)


# Simple WCAG contrast audit to check palette pairs
# Returns a dataframe and also renders a small report
import math

def _rel_luminance(hex_color: str) -> float:
    c = hex_color.lstrip('#')
    r, g, b = [int(c[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    def lin(v):
        return v/12.92 if v <= 0.03928 else ((v + 0.055)/1.055)**2.4
    R, G, B = lin(r), lin(g), lin(b)
    return 0.2126*R + 0.7152*G + 0.0722*B

def _contrast_ratio(c1: str, c2: str) -> float:
    L1 = _rel_luminance(c1)
    L2 = _rel_luminance(c2)
    lighter, darker = (L1, L2) if L1 >= L2 else (L2, L1)
    return (lighter + 0.05) / (darker + 0.05)


def contrast_audit_report():
    COLORS = get_colors()
    pairs = [
        ("text/surface", COLORS["text"], COLORS["surface"]),
        ("muted_text/surface", COLORS["muted_text"], COLORS["surface"]),
        ("text/background", COLORS["text"], COLORS["background"]),
        ("primary/surface", COLORS["primary"], COLORS["surface"]),
        ("accent/surface", COLORS["accent"], COLORS["surface"]),
        ("danger/surface", COLORS["danger"], COLORS["surface"]),
        ("success/surface", COLORS["success"], COLORS["surface"]),
    ]
    rows = []
    for name, fg, bg in pairs:
        rows.append({
            "pair": name,
            "fg": fg,
            "bg": bg,
            "ratio": round(_contrast_ratio(fg, bg), 2)
        })
    df = pd.DataFrame(rows)
    st.markdown("#### Contrast audit (WCAG-AA target: 4.5:1 for normal text)")
    st.dataframe(df)
    return df
