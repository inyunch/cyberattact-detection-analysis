import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.theme import COLORS, apply_plotly_theme
from modules.filters import apply_global_filters, filter_summary_chips, show_filter_stats, global_filter_inline

def show(global_threats, intrusion_data):
    """Display the main dashboard page."""

    if global_threats is None or intrusion_data is None:
        st.error("Data not loaded. Please check the data sources.")
        return

    # Apply global filters
    global_filters = st.session_state.get('global_filters', {})
    global_threats = apply_global_filters(global_threats, global_filters)

    # Add top margin to align with navigation
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

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
        st.metric("Total Incidents", f"{total_incidents:,}", incident_delta_str)
    with col2:
        st.metric("Total Financial Loss", f"${total_loss/1000:.2f}B", "Over 10 years")
    with col3:
        st.metric("Avg. Resolution Time", f"{avg_resolution_time:.1f} hrs", "Lower is better")
    with col4:
        st.metric("Network Attack Rate", f"{network_attack_rate:.2f}%", "From intrusion dataset")

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # --- Main Dashboard Grid ---
    col1, col2 = st.columns([2, 3])

    with col1:
        # --- Top Targeted Industries (Bar Chart) ---
        st.subheader("Top 5 Targeted Industries")
        target_industry = global_threats['Target Industry'].value_counts().nlargest(5)
        fig1 = go.Figure(go.Bar(
            x=target_industry.values,
            y=target_industry.index,
            orientation='h',
            marker_color=COLORS["accent_blue"]
        ))
        fig1 = apply_plotly_theme(fig1)
        fig1.update_layout(
            xaxis_title="Number of Incidents",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            height=300
        )
        st.plotly_chart(fig1, use_container_width=True)

        # --- Top Countries by Attack Frequency (Bar Chart) ---
        st.subheader("Top 5 Countries by Attack Frequency")
        top_countries = global_threats['Country'].value_counts().nlargest(5)
        fig2 = go.Figure(go.Bar(
            x=top_countries.values,
            y=top_countries.index,
            orientation='h',
            marker_color=COLORS["accent_green"]
        ))
        fig2 = apply_plotly_theme(fig2)
        fig2.update_layout(
            xaxis_title="Number of Incidents",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # --- Attack Frequency Over Time (Line Chart) ---
        attack_type_filter = st.session_state.get('global_filters', {}).get('attack_type', 'All')
        if attack_type_filter == 'All':
            st.subheader("Attack Frequency Over Time")
        else:
            st.subheader(f"Attack Frequency Over Time: {attack_type_filter}")

        attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=attacks_by_year['Year'],
            y=attacks_by_year['Count'],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color=COLORS["accent_blue"], width=3),
            marker=dict(size=8, color=COLORS["accent_green"]),
            fillcolor=f'rgba(0, 217, 255, 0.1)'
        ))
        fig3 = apply_plotly_theme(fig3)
        fig3.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Incidents",
            height=300
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
            color_continuous_scale=[[0, COLORS["bg_secondary"]], [0.5, COLORS["accent_blue"]], [1, COLORS["accent_green"]]],
            projection="natural earth"
        )
        fig4 = apply_plotly_theme(fig4)
        fig4.update_layout(
            height=300,
            geo=dict(
                bgcolor=COLORS["bg_secondary"],
                lakecolor=COLORS["bg_primary"],
                landcolor=COLORS["bg_hover"],
                subunitcolor=COLORS["border_color"]
            )
        )
        st.plotly_chart(fig4, use_container_width=True)