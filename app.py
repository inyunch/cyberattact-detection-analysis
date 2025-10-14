import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Threat Analysis Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/cyberattack-detection-analysis',
        'Report a bug': 'https://github.com/yourusername/cyberattack-detection-analysis/issues',
        'About': """
        # Cybersecurity Threat Analysis Dashboard
        Powered by Streamlit, Plotly, and Python.
        This dashboard provides a comprehensive analysis of global cybersecurity threats
        and network intrusion detection patterns.
        """
    }
)

# Custom CSS for the new design
st.markdown("""
    <style>
    /* Core layout and background */
    .main {
        background-color: #F0F2F6; /* Light grey background */
    }

    .block-container {
        padding: 2rem 2rem 2rem 2rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0E1117; /* Dark sidebar */
        border-right: 1px solid #262730;
    }

    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 1.5rem;
    }

    /* Sidebar option menu styling */
    .st-emotion-cache-16txtl3 {
        padding: 0 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2A3F54;
    }

    h1 {
        font-size: 2.2rem;
        font-weight: 700;
        border-bottom: 2px solid #4A90E2;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    h2 {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
    }

    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4A90E2;
    }

    /* Metric cards */
    .stMetric {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease-in-out;
        border-left: 6px solid #4A90E2;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    .stMetric > label {
        font-size: 1rem;
        font-weight: 600;
        color: #5E6C79;
    }

    .stMetric > div {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2A3F54;
    }

    .stMetric .st-emotion-cache-1xarl3l {
        font-size: 0.875rem;
        color: #5E6C79;
    }

    /* Chart and container styling */
    .stPlotlyChart, .stDataFrame {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        font-weight: 600;
        color: #2A3F54;
    }

    /* Button styling */
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
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

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: white; font-size: 24px; font-weight: 700; border: none;">
                🛡️ CyberGuard
            </h1>
            <p style="color: #A0AEC0; font-size: 14px;">Threat Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

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
            "container": {"padding": "0!important", "background-color": "#0E1117"},
            "icon": {"color": "#4A90E2", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "15px 20px",
                "--hover-color": "#262730"
            },
            "nav-link-selected": {"background-color": "#262730"},
        }
    )

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