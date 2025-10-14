import streamlit as st
from typing import List, Optional, Dict, Any
import plotly.graph_objects as go
from .ui_utils import apply_theme, get_colors


def chart_card(fig: Optional[go.Figure] = None, title: Optional[str] = None, caption: Optional[str] = None, height: Optional[int] = 350, use_container_width: bool = True, *args, **kwargs):
    """Render a Plotly figure within a styled card, with optional title and caption.
    Accepts arbitrary extra args/kwargs for compatibility with st.plotly_chart replacements.
    """
    COLORS = get_colors()
    # Backward compatibility: if called as chart_card(fig, use_container_width=True)
    if fig is None and args:
        fig = args[0]
    if 'use_container_width' in kwargs:
        use_container_width = kwargs.get('use_container_width', use_container_width)
    if 'height' in kwargs and height is None:
        height = kwargs.get('height')
    with st.container():
        st.markdown("<div class='rovocard'>", unsafe_allow_html=True)
        if title:
            st.markdown(f"<h3 style='margin:0 0 0.4rem 0;'>{title}</h3>", unsafe_allow_html=True)
        if height and hasattr(fig, 'update_layout'):
            fig.update_layout(height=height)
        if fig is not None:
            fig = apply_theme(fig)
            st.plotly_chart(fig, use_container_width=use_container_width)
        if caption:
            st.markdown(f"<p style='margin:6px 0 0 0; font-size:0.95rem;'>{caption}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def kpi_group(items: List[Dict[str, Any]], columns: Optional[int] = 4):
    """Render KPI items in a single rovocard as a row of columns.
    Each item: {title, value, delta, icon, delta_status}
    """
    st.markdown("<div class='rovocard'>", unsafe_allow_html=True)
    cols = st.columns(columns)
    for i, it in enumerate(items):
        with cols[i % columns]:
            from .ui_utils import kpi_card
            kpi_card(
                title=it.get("title", "KPI"),
                value=it.get("value", "-"),
                delta=it.get("delta"),
                icon=it.get("icon", ""),
                delta_status=it.get("delta_status", "neutral"),
            )
    st.markdown("</div>", unsafe_allow_html=True)


def two_col(left_ratio: int = 2, right_ratio: int = 3):
    """A semantic helper to create a two-column layout with default ratios."""
    return st.columns([left_ratio, right_ratio])
