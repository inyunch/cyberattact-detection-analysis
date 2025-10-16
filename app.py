import streamlit as st
import pandas as pd

# Handle query params for navigation (supports both new and legacy Streamlit APIs)
def _get_query_params():
    try:
        # Streamlit >= 1.30
        return dict(st.query_params)
    except Exception:
        try:
            return st.experimental_get_query_params()
        except Exception:
            return {}

_qp = _get_query_params()
if "page" in _qp:
    page_from_query = _qp.get("page")
    if isinstance(page_from_query, list):
        page_from_query = page_from_query[0]
    page_from_query = str(page_from_query).replace('_', ' ')
    allowed_pages = [
        "Dashboard Overview", "Global Threat Landscape", "Intrusion Detection",
        "Data Explorer", "IDA/EDA Analysis", "Comparative Insights", "Methodology"
    ]
    if page_from_query in allowed_pages:
        st.session_state.selected_page = page_from_query

# Page configuration
st.set_page_config(
    page_title="CyberGuard - Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "CyberGuard Threat Intelligence Dashboard - Powered by Streamlit & Python"
    }
)

# Apply centralized theme CSS
from modules.theme import apply_dashboard_css
apply_dashboard_css()

# Data loading with caching
@st.cache_data
def load_data():
    """Load both datasets with robust checks and clear guidance."""
    from pathlib import Path
    data_dir = Path('data')
    gt_path = data_dir / 'Global_Cybersecurity_Threats_2015-2024.csv'
    id_path = data_dir / 'cybersecurity_intrusion_data.csv'

    if not gt_path.exists() or not id_path.exists():
        missing = []
        if not gt_path.exists():
            missing.append(str(gt_path))
        if not id_path.exists():
            missing.append(str(id_path))
        st.error("Required dataset(s) missing: " + ", ".join(missing))
        st.info("Please place the datasets in the 'data/' directory with the exact filenames above, then rerun the app.")
        st.stop()

    try:
        global_threats = pd.read_csv(gt_path)
        intrusion_data = pd.read_csv(id_path)

        if 'Year' in global_threats.columns:
            global_threats['Year'] = pd.to_numeric(
                global_threats['Year'].astype(str).str.replace(',', ''),
                errors='coerce'
            ).astype('Int64')

        return global_threats, intrusion_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Load data
global_threats, intrusion_data = load_data()

# Import filter system
from modules.filters import global_filter_sidebar, init_filter_state

# Initialize filter state
init_filter_state()

# Sidebar Navigation
with st.sidebar:
    # Logo Header
    st.markdown("""
        <div style="padding: 8px 16px 12px 16px; border-bottom: 1px solid var(--border-color); margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 40px; filter: drop-shadow(0 0 12px rgba(0, 217, 255, 0.5));">🛡️</span>
                <div>
                    <h1 style="
                        margin: 0;
                        font-size: 22px;
                        font-weight: 800;
                        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        letter-spacing: -0.02em;
                        border: none;
                        padding: 0;
                        line-height: 1.2;
                    ">CyberGuard</h1>
                    <p style="
                        margin: 3px 0 0 0;
                        font-size: 11px;
                        color: var(--text-muted);
                        text-transform: uppercase;
                        letter-spacing: 0.08em;
                        font-weight: 600;
                        line-height: 1.2;
                    ">Threat Intelligence</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize selected page in session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Dashboard Overview"

    # --- Navigation Menu ---
    
    def nav_item(name, page_id, is_header=False, icon=""):
        if is_header:
            st.markdown(f"<h3 style='padding: 10px 10px 5px 10px; font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;'>{name}</h3>", unsafe_allow_html=True)
        else:
            is_selected = st.session_state.selected_page == name
            link_style = "color: #00FFB3; font-weight: 600; background-color: var(--bg-hover); border-radius: 8px;" if is_selected else "color: #A0A7B8; font-weight: 500;"
            st.markdown(f'''
            <a href="/?page={page_id}" target="_self" style="text-decoration: none; display: block; padding: 8px 10px 8px 20px; margin: 2px 10px; {link_style}">
                {icon} {name}
            </a>
            ''', unsafe_allow_html=True)

    nav_item("Dashboard", None, is_header=True)
    nav_item("Dashboard Overview", "Dashboard_Overview", icon="📊")
    nav_item("Global Threat Landscape", "Global_Threat_Landscape", icon="🌍")
    nav_item("Intrusion Detection", "Intrusion_Detection", icon="🛡️")

    nav_item("Analysis", None, is_header=True)
    nav_item("Data Explorer", "Data_Explorer", icon="🔍")
    nav_item("IDA/EDA Analysis", "IDA/EDA_Analysis", icon="📊")
    nav_item("Comparative Insights", "Comparative_Insights", icon="💡")

    nav_item("Documentation", None, is_header=True)
    nav_item("Methodology", "Methodology", icon="📖")

    selected = st.session_state.selected_page

    # --- Filters ---
    st.markdown("---")
    st.markdown("<h3 style='padding: 10px 10px 5px 10px; font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;'>Filters</h3>", unsafe_allow_html=True)

    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = {}

    if selected == "Global Threat Landscape":
        from modules.filters import page_filter_panel_global_threats, show_filter_stats, apply_page_filters_global_threats
        page_filters = page_filter_panel_global_threats(global_threats)
        st.session_state.page_filters['global_threats'] = page_filters
        
        filtered_df = apply_page_filters_global_threats(global_threats, page_filters)
        st.session_state.filtered_data['global_threats'] = filtered_df
        show_filter_stats(len(global_threats), len(filtered_df))

    elif selected == "Intrusion Detection":
        from modules.filters import page_filter_panel_intrusion, show_filter_stats, apply_page_filters_intrusion
        page_filters = page_filter_panel_intrusion(intrusion_data)
        st.session_state.page_filters['intrusion_detection'] = page_filters

        filtered_df = apply_page_filters_intrusion(intrusion_data, page_filters)
        st.session_state.filtered_data['intrusion_detection'] = filtered_df
        show_filter_stats(len(intrusion_data), len(filtered_df))

    else:
        st.info("No filters available for this page.")

# Page Routing
dash_pages = ["Dashboard Overview", "Global Threat Landscape", "Intrusion Detection"]
if selected in dash_pages:
    from modules import home
    home.show(global_threats, intrusion_data, page=selected)
elif selected == "Data Explorer":
    from modules import data_explorer
    data_explorer.show(intrusion_data)
elif selected == "IDA/EDA Analysis":
    from modules import data_analysis
    data_analysis.show(global_threats, intrusion_data)
elif selected == "Comparative Insights":
    from modules import comparative_insights
    comparative_insights.show(global_threats, intrusion_data)
elif selected == "Methodology":
    from modules import methodology
    methodology.show()