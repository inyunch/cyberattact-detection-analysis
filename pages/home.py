import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show(global_threats, intrusion_data):
    """Display the home page with project overview and KPIs"""

    # Header
    st.title("🛡️ Global Cybersecurity Threat Analysis Platform")
    st.markdown("### *Revealing Patterns in Cyber Attacks Across Time, Geography, and Attack Vectors*")
    st.markdown("---")

    # Calculate KPIs
    if global_threats is not None and intrusion_data is not None:
        total_attacks = len(global_threats)
        total_losses = global_threats['Financial Loss (in Million $)'].sum()
        years_covered = f"{global_threats['Year'].min()}-{global_threats['Year'].max()}"
        detection_rate = (intrusion_data['attack_detected'].sum() / len(intrusion_data) * 100)

        # KPI Cards
        st.markdown("## 📊 Key Metrics at a Glance")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="📈 Total Incidents",
                value=f"{total_attacks:,}",
                delta="Global Threats Dataset"
            )

        with col2:
            st.metric(
                label="💰 Total Financial Losses",
                value=f"${total_losses:,.1f}B",
                delta="2015-2024"
            )

        with col3:
            st.metric(
                label="🎯 Attack Detection Rate",
                value=f"{detection_rate:.1f}%",
                delta="Intrusion Dataset"
            )

        with col4:
            st.metric(
                label="📅 Years Covered",
                value=years_covered,
                delta="10 years"
            )

        st.markdown("---")

        # Project Goals Section
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## 🎯 Project Goals")
            st.markdown("""
            This interactive analytical platform combines:

            **🌍 Macro-Level Analysis**
            - Global cybersecurity threat trends (2015-2024)
            - Geographic and sectoral impact assessment
            - Financial loss patterns and attack type evolution

            **🔍 Micro-Level Analysis**
            - Network-level intrusion detection patterns
            - User behavior and attack signatures
            - Protocol and encryption analysis

            **Key Research Questions:**
            1. How have cyber attacks evolved over the past decade?
            2. Which sectors and countries face the highest risk?
            3. What behavioral patterns distinguish attacks from normal traffic?
            4. How can we prioritize defense strategies based on data?
            """)

        with col2:
            st.markdown("## 📊 Quick Insights Preview")

            # Mini visualization: Attacks over time
            attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')
            fig = px.line(attacks_by_year, x='Year', y='Count',
                         title='Attack Frequency Trend (2015-2024)',
                         markers=True)
            fig.update_layout(height=250, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Top attack types
            top_attacks = global_threats['Attack Type'].value_counts().head(5)
            fig2 = px.bar(x=top_attacks.values, y=top_attacks.index,
                         orientation='h',
                         title='Top 5 Attack Types',
                         labels={'x': 'Count', 'y': 'Attack Type'})
            fig2.update_layout(height=250, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # Navigation Guide
        st.markdown("## 🧭 Navigation Guide")

        nav_col1, nav_col2, nav_col3 = st.columns(3)

        with nav_col1:
            st.markdown("""
            ### 📊 IDA/EDA Analysis
            Statistical analysis & visualizations:
            - Initial Data Analysis (IDA)
            - Exploratory Data Analysis (EDA)
            - Correlation matrices
            - PCA dimensionality reduction
            - 20+ comprehensive charts
            """)

            st.markdown("""
            ### 🌍 Global Threats
            Explore macro-level cybersecurity trends:
            - Temporal analysis
            - Geographic patterns
            - Sector vulnerabilities
            - Financial impact
            """)

        with nav_col2:
            st.markdown("""
            ### 🔍 Intrusion Detection
            Analyze network-level patterns:
            - Attack vs. normal traffic
            - Protocol analysis
            - Behavioral signatures
            - Feature distributions
            """)

            st.markdown("""
            ### 📈 Comparative Insights
            Cross-dataset analysis:
            - Key findings
            - Strategic recommendations
            - Defense priorities
            - Actionable insights
            """)

        with nav_col3:
            st.markdown("""
            ### 📖 Methodology
            Project documentation:
            - Data sources
            - Cleaning process
            - Analysis methods
            - Limitations
            """)

        st.markdown("---")

        # Dataset Overview
        st.markdown("## 📁 Dataset Overview")

        ds_col1, ds_col2 = st.columns(2)

        with ds_col1:
            st.markdown("### 🌍 Global Cybersecurity Threats Dataset")
            st.info(f"""
            **Records:** {len(global_threats):,}
            **Time Range:** {global_threats['Year'].min()}-{global_threats['Year'].max()}
            **Variables:** {global_threats.shape[1]}
            **Source:** Kaggle

            Provides incident-level global records including attack types,
            targeted sectors/countries, financial losses, and resolutions.
            """)

        with ds_col2:
            st.markdown("### 🔍 Intrusion Detection Dataset")
            st.info(f"""
            **Records:** {len(intrusion_data):,}
            **Attack Rate:** {detection_rate:.1f}%
            **Variables:** {intrusion_data.shape[1]}
            **Source:** Kaggle

            Network traffic and user behavior-based features for intrusion
            detection, including protocol types, encryption, and session data.
            """)

        st.markdown("---")
        st.markdown("*Use the sidebar to navigate to different analysis sections* 👈")

    else:
        st.error("Unable to load datasets. Please check data files.")
