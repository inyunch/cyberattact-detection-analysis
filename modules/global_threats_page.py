import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show(global_threats):
    """Display global threat landscape analysis"""

    st.title("🌍 Global Threat Landscape Analysis")
    st.markdown("### Macro-level cybersecurity trends from 2015-2024")
    st.markdown("---")

    if global_threats is None:
        st.error("Unable to load global threats data.")
        return

    # Year range filter card
    with st.sidebar.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
            padding: 15px 16px 12px 16px;
            border-radius: 10px;
            margin-bottom: 18px;
            border: 1px solid rgba(0,120,212,0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <p style="color: #ffffff; font-weight: 600; font-size: 13px; margin: 0 0 12px 0; letter-spacing: 0.5px;">
                📅 YEAR RANGE
            </p>
        """, unsafe_allow_html=True)

        min_year, max_year = int(global_threats['Year'].min()), int(global_threats['Year'].max())
        year_range = st.slider(
            "Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Country filter card
    with st.sidebar.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
            padding: 15px 16px 12px 16px;
            border-radius: 10px;
            margin: 20px 0 18px 0;
            border: 1px solid rgba(0,120,212,0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <p style="color: #ffffff; font-weight: 600; font-size: 13px; margin: 0 0 12px 0; letter-spacing: 0.5px;">
                🌍 COUNTRIES
            </p>
        """, unsafe_allow_html=True)

        countries = ['All'] + sorted(global_threats['Country'].unique().tolist())
        selected_countries = st.multiselect(
            "Countries",
            options=countries,
            default=['All'],
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Sector filter card
    with st.sidebar.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
            padding: 15px 16px 12px 16px;
            border-radius: 10px;
            margin: 20px 0 18px 0;
            border: 1px solid rgba(0,120,212,0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <p style="color: #ffffff; font-weight: 600; font-size: 13px; margin: 0 0 12px 0; letter-spacing: 0.5px;">
                🏢 INDUSTRIES
            </p>
        """, unsafe_allow_html=True)

        sectors = ['All'] + sorted(global_threats['Target Industry'].unique().tolist())
        selected_sectors = st.multiselect(
            "Industries",
            options=sectors,
            default=['All'],
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Attack type filter card
    with st.sidebar.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
            padding: 15px 16px 12px 16px;
            border-radius: 10px;
            margin: 20px 0 18px 0;
            border: 1px solid rgba(0,120,212,0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <p style="color: #ffffff; font-weight: 600; font-size: 13px; margin: 0 0 12px 0; letter-spacing: 0.5px;">
                🎯 ATTACK TYPES
            </p>
        """, unsafe_allow_html=True)

        attack_types = ['All'] + sorted(global_threats['Attack Type'].unique().tolist())
        selected_attack_types = st.multiselect(
            "Attack Types",
            options=attack_types,
            default=['All'],
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Apply filters
    filtered_data = global_threats.copy()
    filtered_data = filtered_data[
        (filtered_data['Year'] >= year_range[0]) &
        (filtered_data['Year'] <= year_range[1])
    ]

    if 'All' not in selected_countries:
        filtered_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

    if 'All' not in selected_sectors:
        filtered_data = filtered_data[filtered_data['Target Industry'].isin(selected_sectors)]

    if 'All' not in selected_attack_types:
        filtered_data = filtered_data[filtered_data['Attack Type'].isin(selected_attack_types)]

    # Display filter results
    st.info(f"📊 Showing **{len(filtered_data):,}** incidents (filtered from {len(global_threats):,} total)")

    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs([
        "📈 Temporal Trends",
        "🗺️ Geographic Analysis",
        "🎯 Sector & Attack Type"
    ])

    # TAB 1: Temporal Trends
    with tab1:
        st.markdown("## 📈 Temporal Analysis")

        # Attacks over time by type
        attacks_by_year_type = filtered_data.groupby(['Year', 'Attack Type']).size().reset_index(name='Count')

        # Ensure Year is numeric
        attacks_by_year_type['Year'] = attacks_by_year_type['Year'].astype(int)

        fig1 = go.Figure()
        for attack_type in attacks_by_year_type['Attack Type'].unique():
            type_data = attacks_by_year_type[attacks_by_year_type['Attack Type'] == attack_type]
            fig1.add_trace(go.Scatter(
                x=[int(y) for y in type_data['Year']],
                y=[int(c) for c in type_data['Count']],
                mode='lines+markers',
                name=attack_type,
                marker=dict(size=6)
            ))

        fig1.update_layout(
            title='Attack Frequency Over Time by Type',
            xaxis_title='Year',
            yaxis_title='Number of Attacks',
            height=500,
            hovermode='x unified',
            xaxis=dict(range=[2014.5, 2024.5], dtick=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Financial losses over time
        col1, col2 = st.columns(2)

        with col1:
            losses_by_year = filtered_data.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index()

            # Convert to lists
            loss_years = [int(y) for y in losses_by_year['Year']]
            total_losses = [float(l) for l in losses_by_year['Financial Loss (in Million $)']]

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=loss_years,
                y=total_losses,
                marker=dict(color='#ff6b6b')
            ))
            fig2.update_layout(
                title='Total Financial Losses by Year',
                xaxis_title='Year',
                yaxis_title='Loss ($M)',
                height=400,
                xaxis=dict(range=[2014.5, 2024.5], dtick=1)
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            avg_losses_by_year = filtered_data.groupby('Year')['Financial Loss (in Million $)'].mean().reset_index()

            # Convert to lists
            avg_years = [int(y) for y in avg_losses_by_year['Year']]
            avg_losses = [float(l) for l in avg_losses_by_year['Financial Loss (in Million $)']]

            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=avg_years,
                y=avg_losses,
                mode='lines+markers',
                line=dict(color='#4ecdc4', width=3),
                marker=dict(size=8)
            ))
            fig3.update_layout(
                title='Average Loss Per Incident Over Time',
                xaxis_title='Year',
                yaxis_title='Avg Loss ($M)',
                height=400,
                xaxis=dict(range=[2014.5, 2024.5], dtick=1)
            )
            st.plotly_chart(fig3, use_container_width=True)

        # Box plot: Loss distribution by attack type
        fig4 = px.box(filtered_data, x='Attack Type', y='Financial Loss (in Million $)',
                     title='Financial Loss Distribution by Attack Type',
                     labels={'Financial Loss (in Million $)': 'Loss ($M)'})
        fig4.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig4, use_container_width=True)

    # TAB 2: Geographic Analysis
    with tab2:
        st.markdown("## 🗺️ Geographic Distribution")

        # Top countries by attack count
        col1, col2 = st.columns([2, 1])

        with col1:
            country_counts = filtered_data['Country'].value_counts().head(15).reset_index()
            country_counts.columns = ['Country', 'Count']

            fig5 = px.bar(country_counts, x='Count', y='Country',
                         title='Top 15 Most Targeted Countries',
                         orientation='h',
                         labels={'Count': 'Number of Attacks'})
            fig5.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig5, use_container_width=True)

        with col2:
            # Top countries by financial loss
            country_losses = filtered_data.groupby('Country')['Financial Loss (in Million $)'].sum().sort_values(ascending=False).head(10).reset_index()

            fig6 = px.pie(country_losses, values='Financial Loss (in Million $)', names='Country',
                         title='Loss Distribution (Top 10 Countries)')
            fig6.update_layout(height=500)
            st.plotly_chart(fig6, use_container_width=True)

        # Geographic heatmap (choropleth)
        country_summary = filtered_data.groupby('Country').agg({
            'Financial Loss (in Million $)': 'sum',
            'Number of Affected Users': 'sum'
        }).reset_index()

        fig7 = px.choropleth(country_summary,
                            locations='Country',
                            locationmode='country names',
                            color='Financial Loss (in Million $)',
                            hover_name='Country',
                            hover_data=['Number of Affected Users'],
                            title='Global Attack Distribution by Financial Impact',
                            color_continuous_scale='Reds')
        fig7.update_layout(height=600)
        st.plotly_chart(fig7, use_container_width=True)

    # TAB 3: Sector & Attack Type Analysis
    with tab3:
        st.markdown("## 🎯 Sector & Attack Type Analysis")

        # Heatmap: Attack Type × Sector
        heatmap_data = pd.crosstab(filtered_data['Attack Type'], filtered_data['Target Industry'])

        fig8 = px.imshow(heatmap_data,
                        labels=dict(x="Industry", y="Attack Type", color="Frequency"),
                        title='Attack Type × Industry Heatmap',
                        aspect='auto',
                        color_continuous_scale='Blues')
        fig8.update_layout(height=600)
        st.plotly_chart(fig8, use_container_width=True)

        # Top attack types
        col1, col2 = st.columns(2)

        with col1:
            attack_type_counts = filtered_data['Attack Type'].value_counts().reset_index()
            attack_type_counts.columns = ['Attack Type', 'Count']

            fig9 = px.bar(attack_type_counts, x='Count', y='Attack Type',
                         title='Attack Type Frequency',
                         orientation='h',
                         labels={'Count': 'Number of Incidents'})
            fig9.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig9, use_container_width=True)

        with col2:
            sector_counts = filtered_data['Target Industry'].value_counts().head(10).reset_index()
            sector_counts.columns = ['Industry', 'Count']

            fig10 = px.bar(sector_counts, x='Count', y='Industry',
                          title='Top 10 Targeted Industries',
                          orientation='h',
                          labels={'Count': 'Number of Attacks'})
            fig10.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig10, use_container_width=True)

        # Treemap: Losses by sector and attack type
        treemap_data = filtered_data.groupby(['Target Industry', 'Attack Type'])['Financial Loss (in Million $)'].sum().reset_index()
        treemap_data = treemap_data.sort_values('Financial Loss (in Million $)', ascending=False).head(50)

        fig11 = px.treemap(treemap_data,
                          path=['Target Industry', 'Attack Type'],
                          values='Financial Loss (in Million $)',
                          title='Financial Losses by Industry and Attack Type (Top 50)',
                          color='Financial Loss (in Million $)',
                          color_continuous_scale='RdYlGn_r')
        fig11.update_layout(height=600)
        st.plotly_chart(fig11, use_container_width=True)

        # Attack source analysis
        st.markdown("### 🕵️ Attack Source Analysis")

        col1, col2 = st.columns(2)

        with col1:
            source_counts = filtered_data['Attack Source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']

            fig12 = px.pie(source_counts, values='Count', names='Source',
                          title='Attack Sources Distribution')
            fig12.update_layout(height=400)
            st.plotly_chart(fig12, use_container_width=True)

        with col2:
            vuln_counts = filtered_data['Security Vulnerability Type'].value_counts().head(10).reset_index()
            vuln_counts.columns = ['Vulnerability', 'Count']

            fig13 = px.bar(vuln_counts, x='Count', y='Vulnerability',
                          title='Top 10 Security Vulnerabilities',
                          orientation='h')
            fig13.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig13, use_container_width=True)
