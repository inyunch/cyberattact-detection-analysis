import streamlit as st
import pandas as pd

# Handle query params for navigation
if "page" in st.query_params:
    page_from_query = st.query_params.get("page").replace('_', ' ')
    allowed_pages = ["Dashboard Overview", "Global Threat Landscape", "Intrusion Detection", "Data Explorer", "IDA/EDA Analysis", "Comparative Insights", "Methodology"]
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

# Apply centralized base CSS/theme
from modules.ui_utils import apply_base_css
apply_base_css()

# Modern dark theme CSS - Following DESIGN_RULES.md
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* CSS Variables - from DESIGN_RULES.md */
    :root {
        --bg-primary: #141B2D;
        --bg-secondary: #1F2A40;
        --bg-tertiary: #0F1520;
        --bg-hover: #2A3650;
        --text-primary: #E8EAF0;
        --text-secondary: #A0A7B8;
        --text-muted: #6C7489;
        --accent-blue: #00D9FF;
        --accent-green: #00FFB3;
        --accent-purple: #7B61FF;
        --accent-orange: #FF9F43;
        --accent-red: #FF5370;
        --border-color: #2E3A52;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Main Content */
    .main {
        background: linear-gradient(180deg, var(--bg-primary) 0%, #0A0F1C 100%);
    }

    .block-container {
        padding: 3rem 2rem;
        max-width: 100%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-tertiary) 100%);
        padding-top: 0rem;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* Remove white background from navigation component containers */
    [data-testid="stSidebar"] .stElementContainer {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .element-container {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] iframe {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .stCustomComponentV1 {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Target all possible containers around the option menu */
    [data-testid="stSidebar"] [class*="st-emotion-cache"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] div[class*="e1mlolmg"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] div[class*="e196pkbe"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Streamlit's vertical block in sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Nuclear option - target ALL divs in sidebar */
    [data-testid="stSidebar"] > div > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Target the specific classes from your HTML */
    .st-emotion-cache-1vo6xi6 {
        background: transparent !important;
        background-color: transparent !important;
    }

    .st-emotion-cache-8atqhb {
        background: transparent !important;
        background-color: transparent !important;
    }

    .st-emotion-cache-1tvzk6f {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .e1mlolmg0 {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .e196pkbe0 {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .e1begtbc0 {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Hide entire sidebar header section */
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }

    [data-testid="stLogoSpacer"] {
        display: none !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    [data-testid="stBaseButton-headerNoPadding"] {
        display: none !important;
    }

    [data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }

    [data-testid="stSidebar"] button[kind="headerNoPadding"] {
        display: none !important;
    }

    /* Sidebar header button when collapsed */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border: none;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    h2 {
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.3;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    h3 {
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.4;
        color: var(--accent-blue);
    }

    p, li, span {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
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
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
        border-color: var(--accent-blue);
    }

    [data-testid="stMetric"] label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    [data-testid="stMetric"] > div {
        display: flex;
        flex-direction: column;
    }

    [data-testid="stMetric"] > div > div:last-child {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 2.0rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        flex-shrink: 0;
    }

    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Charts & DataFrames */
    .stPlotlyChart, [data-testid="stDataFrame"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 12px;
        box-shadow: var(--shadow-md);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        color: var(--text-primary);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
        color: var(--bg-primary);
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all var(--transition-fast);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 217, 255, 0.4);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        box-shadow: none;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-hover);
        border-color: var(--accent-blue);
        color: var(--accent-blue);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        transition: all var(--transition-fast);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-hover);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(0, 255, 179, 0.15) 100%);
        color: var(--text-primary);
        font-weight: 600;
        box-shadow: inset 0 0 20px rgba(0, 217, 255, 0.1);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }

    /* Slider */
    .stSlider > div > div > div > div {
        background: var(--accent-blue);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--bg-hover);
    }

    /* ULTIMATE NUCLEAR: Remove ALL visible containers around buttons in sidebar */
    /* Target EVERY possible Streamlit wrapper element */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > div,
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"],
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div,
    [data-testid="stSidebar"] [data-testid="column"],
    [data-testid="stSidebar"] [data-testid="column"] > div,
    [data-testid="stSidebar"] [data-testid="column"] > div > div,
    [data-testid="stSidebar"] [data-testid="column"] > div > div > div,
    [data-testid="stSidebar"] .element-container,
    [data-testid="stSidebar"] .stButton,
    [data-testid="stSidebar"] .stButton > div,
    [data-testid="stSidebar"] .row-widget,
    [data-testid="stSidebar"] .row-widget > div,
    section[data-testid="stSidebar"] > div > div > div,
    section[data-testid="stSidebar"] > div > div > div > div,
    section[data-testid="stSidebar"] [class*="css-"],
    section[data-testid="stSidebar"] div[class*="css-"][class*="e"],
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton,
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton > div,
    div[data-testid="stSidebar"] div[data-testid="column"] .element-container {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    /* Horizontal block should have only small gap */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        gap: 6px !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Columns should have absolutely no padding or margin */
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* NUCLEAR OVERRIDE - Force ALL sidebar buttons to blue (NO RED!) */
    /* This overrides Streamlit's default red primary button styling */
    /* Target every possible button selector in sidebar */
    div[data-testid="stSidebar"] .stButton > button,
    div[data-testid="stSidebar"] .stButton button,
    div[data-testid="stSidebar"] button,
    div[data-testid="stSidebar"] .stButton > button[kind="primary"],
    div[data-testid="stSidebar"] .stButton > button[kind="primaryFormSubmit"],
    div[data-testid="stSidebar"] div[data-testid="column"] button,
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton > button,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] [data-testid="baseButton-primary"],
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] .stButton button[data-testid*="baseButton"] {
        background: transparent !important;
        background-color: transparent !important;
        background-image: linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%) !important;
        color: #00D9FF !important;
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
    }

    /* Hover states for all sidebar buttons */
    div[data-testid="stSidebar"] .stButton > button:hover,
    div[data-testid="stSidebar"] .stButton button:hover,
    div[data-testid="stSidebar"] button:hover,
    div[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    div[data-testid="stSidebar"] div[data-testid="column"] button:hover,
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton > button:hover,
    section[data-testid="stSidebar"] button:hover,
    section[data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] [data-testid="baseButton-primary"]:hover,
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] .stButton button[data-testid*="baseButton"]:hover {
        background-image: linear-gradient(135deg, rgba(0, 217, 255, 0.25) 0%, rgba(0, 255, 179, 0.25) 100%) !important;
        border-color: #00D9FF !important;
        color: #00FFB3 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3) !important;
    }

    /* Active states for all sidebar buttons */
    div[data-testid="stSidebar"] .stButton > button:active,
    div[data-testid="stSidebar"] .stButton button:active,
    div[data-testid="stSidebar"] button:active,
    div[data-testid="stSidebar"] .stButton > button[kind="primary"]:active,
    div[data-testid="stSidebar"] div[data-testid="column"] button:active,
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton > button:active,
    section[data-testid="stSidebar"] button:active,
    section[data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] [data-testid="baseButton-primary"]:active,
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"]:active,
    [data-testid="stSidebar"] .stButton button[data-testid*="baseButton"]:active {
        transform: translateY(0) !important;
    }

    /* Focus states for all sidebar buttons */
    div[data-testid="stSidebar"] .stButton > button:focus,
    div[data-testid="stSidebar"] .stButton button:focus,
    div[data-testid="stSidebar"] button:focus,
    div[data-testid="stSidebar"] .stButton > button[kind="primary"]:focus,
    div[data-testid="stSidebar"] div[data-testid="column"] button:focus,
    div[data-testid="stSidebar"] div[data-testid="column"] .stButton > button:focus,
    section[data-testid="stSidebar"] button:focus,
    section[data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] [data-testid="baseButton-primary"]:focus,
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"]:focus,
    [data-testid="stSidebar"] .stButton button[data-testid*="baseButton"]:focus {
        border-color: #00D9FF !important;
        box-shadow: 0 0 0 2px rgba(0, 217, 255, 0.2) !important;
        outline: none !important;
    }

    /* Accessibility - Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    .tab-content-wrapper {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
    }

    /* Custom Tabs using st.radio */
div[role="radiogroup"] {
    display: flex;
    border-radius: 12px;
    background: var(--bg-secondary);
    padding: 8px;
    margin-bottom: 24px;
}

div[role="radiogroup"] > div {
    flex: 1;
}

div[role="radiogroup"] label {
    display: block;
    width: 100%;
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    transition: all var(--transition-fast);
    cursor: pointer;
}

div[role="radiogroup"] label:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

div[role="radiogroup"] input[type="radio"]:checked + label {
    background: linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(0, 255, 179, 0.15) 100%);
    color: var(--text-primary);
    font-weight: 600;
    box-shadow: inset 0 0 20px rgba(0, 217, 255, 0.1);
}

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem;
        }

        h1 {
            font-size: 1.75rem;
        }

        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

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