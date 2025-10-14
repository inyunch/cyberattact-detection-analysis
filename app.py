import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="CyberGuard - Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/cyberattack-detection-analysis',
        'Report a bug': 'https://github.com/yourusername/cyberattack-detection-analysis/issues',
        'About': "CyberGuard Threat Intelligence Dashboard - Powered by Streamlit & Python"
    }
)

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
        padding: 1rem 2rem;
        max-width: 100%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-tertiary) 100%);
    }

    /* Sidebar collapse icon (top right) */
    [data-testid="stSidebar"] button[kind="header"] {
        color: #E8EAF0 !important;
    }

    [data-testid="stSidebar"] button[kind="header"] svg {
        fill: #E8EAF0 !important;
        color: #E8EAF0 !important;
    }

    /* Sidebar header button */
    [data-testid="collapsedControl"] button {
        color: #E8EAF0 !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: #E8EAF0 !important;
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
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
        border-color: var(--accent-blue);
    }

    [data-testid="stMetric"] label {
        font-size: 0.75rem;
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
        justify-content: space-between;
        gap: 12px;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        flex-shrink: 0;
    }

    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
        text-align: right;
        margin-left: auto;
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
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 10px 16px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin: 0 !important;
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
    """Load both datasets"""
    try:
        global_threats = pd.read_csv('data/Global_Cybersecurity_Threats_2015-2024.csv')
        intrusion_data = pd.read_csv('data/cybersecurity_intrusion_data.csv')

        if 'Year' in global_threats.columns:
            global_threats['Year'] = pd.to_numeric(
                global_threats['Year'].astype(str).str.replace(',', ''),
                errors='coerce'
            ).astype('Int64')

        return global_threats, intrusion_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

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
        <div style="padding: 14px 16px; border-bottom: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 28px; filter: drop-shadow(0 0 12px rgba(0, 217, 255, 0.5));">🛡️</span>
                <div>
                    <h1 style="
                        margin: 0;
                        font-size: 18px;
                        font-weight: 800;
                        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        letter-spacing: -0.02em;
                        border: none;
                        padding: 0;
                    ">CyberGuard</h1>
                    <p style="
                        margin: 2px 0 0 0;
                        font-size: 10px;
                        color: var(--text-muted);
                        text-transform: uppercase;
                        letter-spacing: 0.08em;
                        font-weight: 600;
                    ">Threat Intelligence</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "IDA/EDA Analysis",
            "Global Threat Landscape",
            "Intrusion Detection",
            "Comparative Insights",
            "Methodology"
        ],
        icons=[
            "house-door-fill",
            "bar-chart-line-fill",
            "globe-americas",
            "shield-shaded",
            "lightbulb-fill",
            "book-half"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "10px 10px !important",
                "background-color": "transparent"
            },
            "icon": {
                "color": "var(--accent-blue)",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "14px",
                "font-weight": "500",
                "text-align": "left",
                "margin": "0 0 4px 0",
                "padding": "11px 14px",
                "border-radius": "10px",
                "color": "var(--text-secondary)",
                "transition": "all 0.15s cubic-bezier(0.4, 0, 0.2, 1)",
                "--hover-color": "var(--bg-hover)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%)",
                "color": "var(--text-primary)",
                "font-weight": "600",
                "box-shadow": "inset 0 0 20px rgba(0, 217, 255, 0.1)",
                "border-left": "4px solid var(--accent-blue)"
            }
        }
    )

    # Filters, Time Period, and Data Stats
    if global_threats is not None:
        st.markdown("<div style='margin-top: 4px; margin-bottom: 6px; border-top: 1px solid var(--border-color);'></div>", unsafe_allow_html=True)

        # CSS for selectbox styling
        st.markdown("""
            <style>
            /* Selectbox styling for Time Period */
            [data-testid="stSidebar"] [data-baseweb="select"] > div {
                background: linear-gradient(135deg, rgba(0, 217, 255, 0.08) 0%, rgba(0, 255, 179, 0.08) 100%) !important;
                border-color: rgba(0, 217, 255, 0.3) !important;
                color: #E8EAF0 !important;
            }

            /* Selectbox text color */
            [data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
                color: #E8EAF0 !important;
            }

            /* Selectbox label color */
            [data-testid="stSidebar"] label {
                color: #E8EAF0 !important;
            }

            /* Selectbox dropdown menu items */
            [data-baseweb="menu"] [role="option"] {
                color: #E8EAF0 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Get year range from data
        min_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').min())
        max_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').max())

        if st.session_state['global_filters']['year_range'] is None:
            st.session_state['global_filters']['year_range'] = (min_year, max_year)

        # 1. Year selection dropdowns (no container)
        year_options = list(range(min_year, max_year + 1))
        col1, col2 = st.columns(2)

        with col1:
            start_year = st.selectbox(
                "From",
                options=year_options,
                index=year_options.index(st.session_state['global_filters']['year_range'][0]),
                key='sidebar_start_year'
            )

        with col2:
            end_year = st.selectbox(
                "To",
                options=year_options,
                index=year_options.index(st.session_state['global_filters']['year_range'][1]),
                key='sidebar_end_year'
            )

        # Ensure start_year <= end_year
        if start_year > end_year:
            start_year, end_year = end_year, start_year

        st.session_state['global_filters']['year_range'] = (start_year, end_year)

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        # 2. TIME PERIOD SECTION - Visual display of selected range
        current_range = st.session_state['global_filters']['year_range']
        st.markdown(f"""<div style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.08) 0%, rgba(0, 255, 179, 0.08) 100%); border: 1px solid rgba(0, 217, 255, 0.3); border-radius: 12px 12px 0 0; padding: 12px 14px; margin: 0px; box-shadow: 0 4px 16px rgba(0, 217, 255, 0.1);">
<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 10px;">
<span style="font-size: 16px;">📅</span>
<span style="font-size: 0.9rem; font-weight: 700; color: #E8EAF0;">Time Period</span>
</div>
<div style="display: flex; justify-content: center; gap: 6px;">
<div style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.2) 0%, rgba(0, 217, 255, 0.1) 100%); border: 1.5px solid rgba(0, 217, 255, 0.5); border-radius: 24px; font-size: 0.8rem; font-weight: 600; color: #E8EAF0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">
<span style="font-size: 13px;">📅</span>
<span>{current_range[0]} – {current_range[1]}</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

        # 3. DATA STATS SECTION - Results of filtering
        from modules.filters import apply_global_filters
        filtered_data = apply_global_filters(global_threats, st.session_state['global_filters'])
        original_count = len(global_threats)
        filtered_count = len(filtered_data)
        reduction = original_count - filtered_count
        percentage = (reduction / original_count * 100) if original_count > 0 else 0

        # Determine color based on filter intensity
        if percentage < 25:
            bar_color = '#00FFB3'
            glow_color = 'rgba(0, 255, 179, 0.3)'
        elif percentage < 50:
            bar_color = '#00D9FF'
            glow_color = 'rgba(0, 217, 255, 0.3)'
        elif percentage < 75:
            bar_color = '#FF9F43'
            glow_color = 'rgba(255, 159, 67, 0.3)'
        else:
            bar_color = '#7B61FF'
            glow_color = 'rgba(123, 97, 255, 0.3)'

        stats_html = f'''<div style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.08) 0%, rgba(0, 255, 179, 0.08) 100%); border: 1px solid rgba(0, 217, 255, 0.3); border-top: none; border-radius: 0 0 12px 12px; padding: 12px 14px; box-shadow: 0 4px 16px rgba(0, 217, 255, 0.1); margin-bottom: 12px;">
<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 10px;">
<span style="font-size: 16px;">📊</span>
<span style="font-size: 0.9rem; font-weight: 700; color: #E8EAF0;">Data Stats</span>
</div>
<div style="display: flex; align-items: baseline; gap: 6px; margin-bottom: 10px;">
<span style="font-size: 1.6rem; font-weight: 800; color: #E8EAF0; font-family: 'JetBrains Mono', monospace; letter-spacing: -0.02em; text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);">{filtered_count:,}</span>
<span style="font-size: 0.8rem; color: #A0A7B8;">/ {original_count:,}</span>
</div>
<div style="width: 100%; height: 5px; background: rgba(255, 255, 255, 0.05); border-radius: 3px; overflow: hidden; margin-bottom: 6px;">
<div style="width: {100 - percentage}%; height: 100%; background: linear-gradient(90deg, #00D9FF 0%, #00FFB3 100%); border-radius: 3px; box-shadow: 0 0 10px {glow_color}; transition: width 0.3s ease;"></div>
</div>
<div style="font-size: 0.7rem; color: #6C7489; text-align: center;">{reduction:,} records filtered</div>
</div>'''

        st.markdown(stats_html, unsafe_allow_html=True)

# Page Routing
if selected == "Dashboard":
    from modules import home
    home.show(global_threats, intrusion_data)
elif selected == "IDA/EDA Analysis":
    from modules import data_analysis
    data_analysis.show(global_threats, intrusion_data)
elif selected == "Global Threat Landscape":
    from modules import global_threats_page
    global_threats_page.show(global_threats)
elif selected == "Intrusion Detection":
    from modules import intrusion_detection_page
    intrusion_detection_page.show(intrusion_data)
elif selected == "Comparative Insights":
    from modules import comparative_insights
    comparative_insights.show(global_threats, intrusion_data)
elif selected == "Methodology":
    from modules import methodology
    methodology.show()