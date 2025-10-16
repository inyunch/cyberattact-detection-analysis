import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from modules.theme import COLORS, apply_plotly_theme

def show(global_threats_original, intrusion_data_original, page="Dashboard Overview"):
    """Display the main dashboard page with conditional content based on the selected page."""

    if global_threats_original is None or intrusion_data_original is None:
        st.error("Data not loaded. Please check the data sources.")
        return

    # Add top margin to align with navigation
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    if page == "Dashboard Overview":
        # Use unfiltered data for overview
        global_threats = global_threats_original.copy()
        intrusion_data = intrusion_data_original.copy()

        # METRICS ROW
        total_incidents = len(global_threats)
        total_loss = global_threats['Financial Loss (in Million $)'].sum()
        avg_resolution_time = global_threats['Incident Resolution Time (in Hours)'].mean()

        # Intrusion detection metrics
        attack_count = intrusion_data['attack_detected'].sum()
        total_intrusion_records = len(intrusion_data)
        network_attack_rate = (attack_count / total_intrusion_records * 100) if total_intrusion_records > 0 else 0

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

        # --- Row 1 ---
        r1_col1, r1_col2, r1_col3, r1_col4 = st.columns(4)

        with r1_col1:
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
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig1, use_container_width=True)

        with r1_col2:
            st.subheader("Top 5 Countries by Attack")
            top_countries = global_threats['Country'].value_counts().nlargest(5)
            fig2 = go.Figure(go.Bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                marker_color=COLORS["accent_green"]
            ))
            fig2 = apply_plotly_theme(fig2)
            fig2.update_layout(
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

        with r1_col3:
            st.subheader("Top 5 Attack Types")
            attack_types = global_threats['Attack Type'].value_counts().nlargest(5)
            fig3 = go.Figure(go.Bar(
                x=attack_types.values,
                y=attack_types.index,
                orientation='h',
                marker_color=COLORS["accent_orange"]
            ))
            fig3 = apply_plotly_theme(fig3)
            fig3.update_layout(
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig3, use_container_width=True)

        with r1_col4:
            st.subheader("Intrusion Overview")
            class_dist = intrusion_data['attack_detected'].value_counts().reset_index()
            class_dist.columns = ['Classification', 'Count']
            class_dist['Classification'] = class_dist['Classification'].map({0: 'Normal', 1: 'Attack'})
            fig4 = px.pie(class_dist, values='Count', names='Classification',
                            title='',
                            color='Classification',
                            color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
            fig4 = apply_plotly_theme(fig4)
            fig4.update_layout(
                height=250,
                margin=dict(l=10, r=10, t=30, b=10),
                legend=dict(orientation="h", yanchor="bottom", y= -0.4, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        # --- Row 2 ---
        r2_col1, r2_col2 = st.columns(2)

        with r2_col1:
            st.subheader("Attack Frequency Over Time")
            attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(
                x=attacks_by_year['Year'],
                y=attacks_by_year['Count'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color=COLORS["accent_blue"], width=3),
                marker=dict(size=8, color=COLORS["accent_green"]),
                fillcolor=f'rgba(0, 217, 255, 0.1)'
            ))
            fig5 = apply_plotly_theme(fig5)
            fig5.update_layout(
                xaxis_title="Year",
                yaxis_title="Number of Incidents",
                height=300
            )
            st.plotly_chart(fig5, use_container_width=True)

        with r2_col2:
            st.subheader("Financial Loss by Country")
            country_loss = global_threats.groupby('Country')['Financial Loss (in Million $)'].sum().reset_index()
            fig6 = px.choropleth(
                country_loss,
                locations="Country",
                locationmode="country names",
                color="Financial Loss (in Million $)",
                hover_name="Country",
                color_continuous_scale=[[0, COLORS["bg_secondary"]], [0.5, COLORS["accent_blue"]], [1, COLORS["accent_green"]]],
                projection="natural earth"
            )
            fig6 = apply_plotly_theme(fig6)
            fig6.update_layout(
                height=300,
                geo=dict(
                    bgcolor=COLORS["bg_secondary"],
                    lakecolor=COLORS["bg_primary"],
                    landcolor=COLORS["bg_hover"],
                    subunitcolor=COLORS["border_color"]
                )
            )
            st.plotly_chart(fig6, use_container_width=True)

    elif page == "Global Threat Landscape":
        global_threats_tab2 = st.session_state.filtered_data.get('global_threats', global_threats_original)

        st.markdown("### Macro-level cybersecurity trends from 2015-2024")
        st.markdown("---")

        # Row 1: High-Level Trends
        st.markdown("## High-Level Trends")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Attack Frequency Over Time by Type")
            attacks_by_year_type = global_threats_tab2.groupby(['Year', 'Attack Type']).size().reset_index(name='Count')
            attacks_by_year_type['Year'] = attacks_by_year_type['Year'].astype(int)
            fig1 = go.Figure()
            for attack_type in attacks_by_year_type['Attack Type'].unique():
                type_data = attacks_by_year_type[attacks_by_year_type['Attack Type'] == attack_type]
                fig1.add_trace(go.Scatter(x=[int(y) for y in type_data['Year']], y=[int(c) for c in type_data['Count']], mode='lines+markers', name=attack_type, marker=dict(size=6)))
            fig1 = apply_plotly_theme(fig1)
            fig1.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.markdown("#### Attack Distribution by Industry and Type")
            bar_data = global_threats_tab2.groupby(['Target Industry', 'Attack Type']).size().reset_index(name='Count')
            fig2 = px.bar(bar_data, x='Target Industry', y='Count', color='Attack Type', barmode='group')
            fig2 = apply_plotly_theme(fig2)
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

        # Row 2: Financial Impact
        st.markdown("## Financial Impact")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### Total Financial Losses by Year")
            losses_by_year = global_threats_tab2.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index()
            loss_years = [int(y) for y in losses_by_year['Year']]
            total_losses = [float(l) for l in losses_by_year['Financial Loss (in Million $)']]
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=loss_years, y=total_losses, marker=dict(color=COLORS["accent_red"])))
            fig3 = apply_plotly_theme(fig3)
            fig3.update_layout(height=300)
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            st.markdown("##### Average Loss Per Incident")
            avg_losses_by_year = global_threats_tab2.groupby('Year')['Financial Loss (in Million $)'].mean().reset_index()
            avg_years = [int(y) for y in avg_losses_by_year['Year']]
            avg_losses = [float(l) for l in avg_losses_by_year['Financial Loss (in Million $)']]
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=avg_years, y=avg_losses, mode='lines+markers', line=dict(color=COLORS["accent_green"], width=3), marker=dict(size=8)))
            fig4 = apply_plotly_theme(fig4)
            fig4.update_layout(height=300)
            st.plotly_chart(fig4, use_container_width=True)
        with col3:
            st.markdown("##### Loss Distribution by Attack Type")
            fig5 = px.box(global_threats_tab2, x='Attack Type', y='Financial Loss (in Million $)')
            fig5 = apply_plotly_theme(fig5)
            fig5.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)

        # Row 3: Top Targets
        st.markdown("## Top Targets")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### Top 15 Most Targeted Countries")
            country_counts = global_threats_tab2['Country'].value_counts().head(15).reset_index()
            country_counts.columns = ['Country', 'Count']
            fig6 = px.bar(country_counts, x='Count', y='Country', orientation='h')
            fig6 = apply_plotly_theme(fig6)
            fig6.update_layout(height=300, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig6, use_container_width=True)
        with col2:
            st.markdown("##### Top 10 Targeted Industries")
            sector_counts = global_threats_tab2['Target Industry'].value_counts().head(10).reset_index()
            sector_counts.columns = ['Industry', 'Count']
            fig7 = px.bar(sector_counts, x='Count', y='Industry', orientation='h')
            fig7 = apply_plotly_theme(fig7)
            fig7.update_layout(height=300, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig7, use_container_width=True)
        with col3:
            st.markdown("##### Loss Distribution (Top 10 Countries)")
            country_losses = global_threats_tab2.groupby('Country')['Financial Loss (in Million $)'].sum().sort_values(ascending=False).head(10).reset_index()
            fig8 = px.pie(country_losses, values='Financial Loss (in Million $)', names='Country')
            fig8 = apply_plotly_theme(fig8)
            fig8.update_layout(height=300)
            st.plotly_chart(fig8, use_container_width=True)

        # Row 4: Attack & Vulnerability Analysis
        st.markdown("## Attack & Vulnerability Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Attack Type × Industry Heatmap")
            heatmap_data = pd.crosstab(global_threats_tab2['Attack Type'], global_threats_tab2['Target Industry'])
            fig9 = px.imshow(heatmap_data, labels=dict(x="Industry", y="Attack Type", color="Frequency"), aspect='auto', color_continuous_scale='Blues')
            fig9 = apply_plotly_theme(fig9)
            fig9.update_layout(height=400)
            st.plotly_chart(fig9, use_container_width=True)
        with col2:
            st.markdown("#### Financial Losses by Industry and Attack Type")
            treemap_data = global_threats_tab2.groupby(['Target Industry', 'Attack Type'])['Financial Loss (in Million $)'].sum().reset_index()
            treemap_data = treemap_data.sort_values('Financial Loss (in Million $)', ascending=False).head(50)
            fig10 = px.treemap(treemap_data, path=['Target Industry', 'Attack Type'], values='Financial Loss (in Million $)', color='Financial Loss (in Million $)', color_continuous_scale='RdYlGn_r')
            fig10 = apply_plotly_theme(fig10)
            fig10.update_layout(height=400)
            st.plotly_chart(fig10, use_container_width=True)

        # Row 5: Attack & Vulnerability Details
        st.markdown("## Attack & Vulnerability Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### Attack Type Frequency")
            attack_type_counts = global_threats_tab2['Attack Type'].value_counts().reset_index()
            attack_type_counts.columns = ['Attack Type', 'Count']
            fig11 = px.bar(attack_type_counts, x='Count', y='Attack Type', orientation='h')
            fig11 = apply_plotly_theme(fig11)
            fig11.update_layout(height=300, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig11, use_container_width=True)
        with col2:
            st.markdown("##### Top 10 Security Vulnerabilities")
            vuln_counts = global_threats_tab2['Security Vulnerability Type'].value_counts().head(10).reset_index()
            vuln_counts.columns = ['Vulnerability', 'Count']
            fig12 = px.bar(vuln_counts, x='Count', y='Vulnerability', orientation='h')
            fig12 = apply_plotly_theme(fig12)
            fig12.update_layout(height=300, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig12, use_container_width=True)
        with col3:
            st.markdown("##### Attack Sources Distribution")
            source_counts = global_threats_tab2['Attack Source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']
            fig13 = px.pie(source_counts, values='Count', names='Source')
            fig13 = apply_plotly_theme(fig13)
            fig13.update_layout(height=300)
            st.plotly_chart(fig13, use_container_width=True)

    elif page == "Intrusion Detection":
        intrusion_data = st.session_state.filtered_data.get('intrusion_detection', intrusion_data_original)

        attack_count = intrusion_data['attack_detected'].sum()
        normal_count = len(intrusion_data) - attack_count
        attack_rate = (attack_count / len(intrusion_data) * 100) if len(intrusion_data) > 0 else 0

        st.markdown("### Network-level patterns and behavioral analysis")
        st.markdown("---")

        # Create sub-tabs for intrusion detection
        subtab1, subtab2, subtab3 = st.tabs([
            "📊 Overview",
            "📈 Feature Distributions",
            "🔬 Behavioral Analysis"
        ])

        with subtab1:
            st.markdown("## 📊 Classification Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Records", f"{len(intrusion_data):,}")
            with col2:
                st.metric("Attack Records", f"{attack_count:,}", delta=f"{attack_rate:.1f}%")
            with col3:
                st.metric("Normal Records", f"{normal_count:,}", delta=f"{100-attack_rate:.1f}%")
            with col4:
                avg_ip_score = intrusion_data['ip_reputation_score'].mean()
                st.metric("Avg IP Reputation", f"{avg_ip_score:.2f}")

            col1, col2 = st.columns(2)

            with col1:
                class_dist = intrusion_data['attack_detected'].value_counts().reset_index()
                class_dist.columns = ['Classification', 'Count']
                class_dist['Classification'] = class_dist['Classification'].map({0: 'Normal', 1: 'Attack'})

                fig = px.pie(class_dist, values='Count', names='Classification',
                             title='Attack vs Normal Distribution',
                             color='Classification',
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                protocol_class = intrusion_data.groupby(['protocol_type', 'attack_detected']).size().reset_index(name='Count')
                protocol_class['Classification'] = protocol_class['attack_detected'].map({0: 'Normal', 1: 'Attack'})

                fig = px.bar(protocol_class, x='protocol_type', y='Count', color='Classification',
                             title='Traffic Volume by Protocol and Classification',
                             barmode='group',
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]},
                             labels={'protocol_type': 'Protocol', 'Count': 'Number of Records'})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            protocol_pct = intrusion_data.groupby(['protocol_type', 'attack_detected']).size().unstack(fill_value=0)
            protocol_pct.columns = ['Normal', 'Attack']

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Normal', x=protocol_pct.index, y=protocol_pct['Normal'],
                                 marker_color=COLORS["accent_blue"]))
            fig.add_trace(go.Bar(name='Attack', x=protocol_pct.index, y=protocol_pct['Attack'],
                                 marker_color=COLORS["accent_red"]))

            fig = apply_plotly_theme(fig)
            fig.update_layout(
                barmode='stack',
                title='Protocol Distribution: Attack vs Normal (Stacked)',
                xaxis_title='Protocol Type',
                yaxis_title='Count',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                encryption_dist = intrusion_data['encryption_used'].value_counts().reset_index()
                encryption_dist.columns = ['Encryption', 'Count']

                fig = px.bar(encryption_dist, x='Encryption', y='Count',
                             title='Encryption Type Distribution',
                             color='Count',
                             color_continuous_scale='Blues')
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                browser_dist = intrusion_data['browser_type'].value_counts().head(10).reset_index()
                browser_dist.columns = ['Browser', 'Count']

                fig = px.bar(browser_dist, x='Count', y='Browser',
                             title='Top 10 Browser Types',
                             orientation='h',
                             color='Count',
                             color_continuous_scale='Greens')
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

        with subtab2:
            st.markdown("## 📈 Feature Distribution Analysis")

            numeric_features = [
                'network_packet_size',
                'login_attempts',
                'session_duration',
                'ip_reputation_score',
                'failed_logins'
            ]

            selected_feature = st.selectbox(
                "Select Feature to Analyze",
                options=numeric_features,
                format_func=lambda x: x.replace('_', ' ').title()
            )

            intrusion_data['Classification'] = intrusion_data['attack_detected'].map({0: 'Normal', 1: 'Attack'})

            fig = px.violin(intrusion_data, x='Classification', y=selected_feature,
                            title=f'{selected_feature.replace("_", " ").title()} Distribution by Classification',
                            color='Classification',
                            box=True,
                            points='outliers',
                            color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(intrusion_data, x=selected_feature, color='Classification',
                                   title=f'{selected_feature.replace("_", " ").title()} Distribution',
                                   nbins=50,
                                   barmode='overlay',
                                   opacity=0.7,
                                   color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.box(intrusion_data, x='Classification', y=selected_feature,
                             title=f'{selected_feature.replace("_", " ").title()} Box Plot',
                             color='Classification',
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 📊 All Features Overview")

            col1, col2 = st.columns(2)

            attack_data = intrusion_data[intrusion_data['attack_detected'] == 1][numeric_features]
            normal_data = intrusion_data[intrusion_data['attack_detected'] == 0][numeric_features]

            with col1:
                st.markdown("**Attack Traffic Statistics**")
                st.dataframe(attack_data.describe().round(2), use_container_width=True)

            with col2:
                st.markdown("**Normal Traffic Statistics**")
                st.dataframe(normal_data.describe().round(2), use_container_width=True)

        with subtab3:
            st.markdown("## 🔬 Behavioral Pattern Analysis")

            fig = px.scatter(intrusion_data.sample(min(5000, len(intrusion_data))),
                             x='login_attempts',
                             y='failed_logins',
                             color='Classification',
                             title='Login Attempts vs Failed Logins',
                             opacity=0.6,
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]},
                             hover_data=['session_duration', 'ip_reputation_score'])
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🔥 Feature Correlation Matrix")

            corr_data = intrusion_data[numeric_features + ['attack_detected']].corr()

            fig = px.imshow(corr_data,
                             labels=dict(color="Correlation"),
                             title='Feature Correlation Heatmap',
                             color_continuous_scale='RdBu_r',
                             aspect='auto',
                             zmin=-1,
                             zmax=1)
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                unusual_time_data = intrusion_data.groupby(['unusual_time_access', 'attack_detected']).size().reset_index(name='Count')
                unusual_time_data['Unusual Time'] = unusual_time_data['unusual_time_access'].map({0: 'Normal Hours', 1: 'Unusual Hours'})
                unusual_time_data['Classification'] = unusual_time_data['attack_detected'].map({0: 'Normal', 1: 'Attack'})

                fig = px.bar(unusual_time_data, x='Unusual Time', y='Count', color='Classification',
                              title='Attack Distribution by Access Time',
                              barmode='group',
                              color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.histogram(intrusion_data, x='ip_reputation_score', color='Classification',
                                    title='IP Reputation Score Distribution',
                                    nbins=50,
                                    barmode='overlay',
                                    opacity=0.7,
                                    color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🌐 3D Feature Space Visualization")

            sample_data = intrusion_data.sample(min(3000, len(intrusion_data)))

            fig = px.scatter_3d(sample_data,
                                 x='login_attempts',
                                 y='session_duration',
                                 z='ip_reputation_score',
                                 color='Classification',
                                 title='3D Feature Space: Login Attempts × Session Duration × IP Reputation',
                                 opacity=0.6,
                                 color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=700)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🔐 Protocol and Encryption Patterns")

            protocol_encryption = pd.crosstab(intrusion_data['protocol_type'],
                                             intrusion_data['encryption_used'],
                                             values=intrusion_data['attack_detected'],
                                             aggfunc='mean')

            fig = px.imshow(protocol_encryption,
                             labels=dict(x="Encryption Type", y="Protocol Type", color="Attack Rate"),
                             title='Attack Rate by Protocol × Encryption',
                             color_continuous_scale='Reds',
                             aspect='auto')
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
