import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Threat Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    h2 {
        color: #ff7f0e;
        padding-top: 1rem;
    }
    .css-1d391kg {
        padding-top: 3rem;
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

        # Basic preprocessing
        global_threats['Year'] = global_threats['Year'].astype(int)

        return global_threats, intrusion_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Load data
global_threats, intrusion_data = load_data()

# Sidebar navigation
st.sidebar.title("🛡️ Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📊 IDA/EDA Analysis", "🌍 Global Threat Landscape", "🔍 Intrusion Detection", "📈 Comparative Insights", "📖 Methodology"]
)

# Page routing
if page == "🏠 Home":
    from pages import home
    home.show(global_threats, intrusion_data)
elif page == "📊 IDA/EDA Analysis":
    from pages import data_analysis
    data_analysis.show(global_threats, intrusion_data)
elif page == "🌍 Global Threat Landscape":
    from pages import global_threats_page
    global_threats_page.show(global_threats)
elif page == "🔍 Intrusion Detection":
    from pages import intrusion_detection_page
    intrusion_detection_page.show(intrusion_data)
elif page == "📈 Comparative Insights":
    from pages import comparative_insights
    comparative_insights.show(global_threats, intrusion_data)
elif page == "📖 Methodology":
    from pages import methodology
    methodology.show()
