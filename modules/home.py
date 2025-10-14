import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color palette inspired by the target design
COLORS = {
    "primary": "#4A90E2",
    "secondary": "#7ED321",
    "background": "#F0F2F6",
    "text": "#2A3F54",
    "light_text": "#5E6C79",
    "grid": "#EAEAEA",
    "accent": "#F5A623",
    "danger": "#D0021B",
    "blue_palette": ["#4A90E2", "#50E3C2", "#BD10E0", "#F5A623", "#F8E71C"]
}

def kpi_card(icon, title, value, delta, delta_color="normal"):
    """Custom KPI card styled like the target image."""
    st.markdown(f"""
    <div class="stMetric" style="border-left-color: {COLORS['primary']};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['light_text']};">{title}</div>
            <div style="font-size: 2rem; color: {COLORS['primary']};">{icon}</div>
        </div>
        <div style="font-size: 2.5rem; font-weight: 700; color: {COLORS['text']}; margin-top: 8px;">{value}</div>
        <div style="font-size: 0.9rem; color: {'#D0021B' if delta_color == 'inverse' else '#2E8B57'}; margin-top: 8px;">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

def show(global_threats, intrusion_data):
    """Display the main dashboard page."""

    st.title("🛡️ Cybersecurity Command Center")
    st.markdown("An overview of the global threat landscape and network security posture.")

    if global_threats is None or intrusion_data is None:
        st.error("Data not loaded. Please check the data sources.")
        return

    # --- KPI Row ---
    st.markdown("##") # Vertical space
    total_incidents = len(global_threats)
    total_loss = global_threats['Financial Loss (in Million $)'].sum()
    avg_resolution_time = global_threats['Incident Resolution Time (in Hours)'].mean()
    network_attack_rate = intrusion_data['attack_detected'].mean() * 100

    # Calculate deltas (YoY change for incidents)
    try:
        incidents_this_year = len(global_threats[global_threats['Year'] == global_threats['Year'].max()])
        incidents_last_year = len(global_threats[global_threats['Year'] == global_threats['Year'].max() - 1])
        incident_delta = ((incidents_this_year - incidents_last_year) / incidents_last_year) * 100
        incident_delta_str = f"{'+' if incident_delta >= 0 else ''}{incident_delta:.1f}% vs Last Year"
    except Exception:
        incident_delta_str = "No YoY data"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("🚨", "Total Incidents", f"{total_incidents:,}", incident_delta_str)
    with col2:
        kpi_card("💰", "Total Financial Loss", f"${total_loss/1000:.2f}B", "Over 10 years")
    with col3:
        kpi_card("⏱️", "Avg. Resolution Time", f"{avg_resolution_time:.1f} hrs", "Lower is better", delta_color="inverse")
    with col4:
        kpi_card("📡", "Network Attack Rate", f"{network_attack_rate:.2f}%", "From intrusion dataset")

    st.markdown("##") # Vertical space

    # --- Main Dashboard Grid ---
    col1, col2 = st.columns([2, 3])

    with col1:
        # --- Top Attack Types (Donut Chart) ---
        st.subheader("Top 5 Attack Types")
        attack_types = global_threats['Attack Type'].value_counts().nlargest(5)
        fig = go.Figure(data=[go.Pie(
            labels=attack_types.index,
            values=attack_types.values,
            hole=.6,
            marker_colors=COLORS["blue_palette"],
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        fig.update_layout(
            showlegend=False,
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Top Targeted Industries (Bar Chart) ---
        st.subheader("Top 5 Targeted Industries")
        target_industry = global_threats['Target Industry'].value_counts().nlargest(5)
        fig2 = go.Figure(go.Bar(
            x=target_industry.values,
            y=target_industry.index,
            orientation='h',
            marker_color=COLORS["primary"]
        ))
        fig2.update_layout(
            title_text="",
            xaxis_title="Number of Incidents",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            height=350,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # --- Attack Frequency Over Time (Line Chart) ---
        st.subheader("Attack Frequency Over Time")
        attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=attacks_by_year['Year'],
            y=attacks_by_year['Count'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color=COLORS["primary"], width=3),
            marker=dict(size=8)
        ))
        fig3.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Incidents",
            height=350,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis=dict(gridcolor=COLORS["grid"]),
            yaxis=dict(gridcolor=COLORS["grid"])
        )
        st.plotly_chart(fig3, use_container_width=True)

        # --- Financial Loss by Country (Map) ---
        st.subheader("Financial Loss by Country")
        country_loss = global_threats.groupby('Country')['Financial Loss (in Million $)'].sum().reset_index()
        fig4 = px.choropleth(
            country_loss,
            locations="Country",
            locationmode="country names",
            color="Financial Loss (in Million $)",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Blues,
            projection="natural earth"
        )
        fig4.update_layout(
            height=350,
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                lakecolor=COLORS["background"],
                landcolor="#EAEAEA",
                subunitcolor="#FFFFFF"
            ),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # --- Project Summary ---
    st.markdown("##")
    st.subheader("About This Platform")
    st.markdown("""
    This interactive dashboard provides a dual perspective on cybersecurity:

    - **🌍 Macro View:** Analyzing over 10 years of global cyber attack data to identify strategic trends, financial impacts, and high-risk sectors.
    - **🔍 Micro View:** Inspecting network-level data to uncover tactical intrusion patterns and behavioral signatures.

    Use the navigation panel on the left to dive deeper into specific analyses, explore the raw data, and understand the project's methodology.
    """)