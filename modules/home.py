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
            target_industry = global_threats['Target Industry'].value_counts().nlargest(5)
            fig1 = go.Figure(go.Bar(
                x=target_industry.values,
                y=target_industry.index,
                orientation='h',
                marker_color=COLORS["accent_blue"]
            ))
            fig1 = apply_plotly_theme(fig1, title='Top 5 Targeted Industries')
            fig1.update_layout(
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig1, use_container_width=True)

        with r1_col2:
            top_countries = global_threats['Country'].value_counts().nlargest(5)
            fig2 = go.Figure(go.Bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                marker_color=COLORS["accent_green"]
            ))
            fig2 = apply_plotly_theme(fig2, title='Top 5 Countries by Attack')
            fig2.update_layout(
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

        with r1_col3:
            attack_types = global_threats['Attack Type'].value_counts().nlargest(5)
            fig3 = go.Figure(go.Bar(
                x=attack_types.values,
                y=attack_types.index,
                orientation='h',
                marker_color=COLORS["accent_orange"]
            ))
            fig3 = apply_plotly_theme(fig3, title='Top 5 Attack Types')
            fig3.update_layout(
                xaxis_title="Incidents",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                height=250,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig3, use_container_width=True)

        with r1_col4:
            class_dist = intrusion_data['attack_detected'].value_counts().reset_index()
            class_dist.columns = ['Classification', 'Count']
            class_dist['Classification'] = class_dist['Classification'].map({0: 'Normal', 1: 'Attack'})
            fig4 = px.pie(class_dist, values='Count', names='Classification',
                            title='Intrusion Overview',
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
            fig5 = apply_plotly_theme(fig5, title='Attack Frequency Over Time')
            fig5.update_layout(
                xaxis_title="Year",
                yaxis_title="Number of Incidents",
                height=300
            )
            st.plotly_chart(fig5, use_container_width=True)

        with r2_col2:
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
            fig6 = apply_plotly_theme(fig6, title='Financial Loss by Country')
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

        st.markdown("### The evolving story of cyber threats: From emergence to impact")
        st.markdown("---")

        # Section 1: Temporal Evolution - How threats have evolved over time
        col1, col2 = st.columns(2)
        with col1:
            attacks_by_year_type = global_threats_tab2.groupby(['Year', 'Attack Type']).size().reset_index(name='Count')
            attacks_by_year_type['Year'] = attacks_by_year_type['Year'].astype(int)
            fig1 = go.Figure()
            for attack_type in attacks_by_year_type['Attack Type'].unique():
                type_data = attacks_by_year_type[attacks_by_year_type['Attack Type'] == attack_type]
                fig1.add_trace(go.Scatter(x=[int(y) for y in type_data['Year']], y=[int(c) for c in type_data['Count']], mode='lines+markers', name=attack_type, marker=dict(size=6)))
            fig1 = apply_plotly_theme(fig1, title='Attack Frequency Over Time by Type')
            fig1.update_layout(
                height=400,
                hovermode='x unified',
                margin=dict(l=60, r=150, t=60, b=50),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1.0,
                    xanchor="left",
                    x=1.02,
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor=COLORS["border_color"],
                    borderwidth=1
                )
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            losses_by_year = global_threats_tab2.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index()
            loss_years = [int(y) for y in losses_by_year['Year']]
            total_losses = [float(l) for l in losses_by_year['Financial Loss (in Million $)']]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=loss_years, y=total_losses, marker=dict(color=COLORS["accent_red"])))
            fig2 = apply_plotly_theme(fig2, title='Total Financial Losses by Year')
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Section 2: Attack Anatomy - Understanding what attackers do
        st.subheader("Attack Anatomy")
        col1, col2, col3 = st.columns(3)
        with col1:
            attack_type_counts = global_threats_tab2['Attack Type'].value_counts().reset_index()
            attack_type_counts.columns = ['Attack Type', 'Count']
            fig3 = px.bar(attack_type_counts, x='Count', y='Attack Type', orientation='h')
            fig3 = apply_plotly_theme(fig3, title='Attack Type Frequency')
            fig3.update_layout(
                height=350,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=150, r=50, t=60, b=50),
                yaxis_tickfont=dict(size=10)
            )
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            vuln_counts = global_threats_tab2['Security Vulnerability Type'].value_counts().head(10).reset_index()
            vuln_counts.columns = ['Vulnerability', 'Count']
            fig4 = px.bar(vuln_counts, x='Count', y='Vulnerability', orientation='h')
            fig4 = apply_plotly_theme(fig4, title='Top 10 Security Vulnerabilities')
            fig4.update_layout(
                height=350,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=180, r=50, t=60, b=50),
                yaxis_tickfont=dict(size=9)
            )
            st.plotly_chart(fig4, use_container_width=True)
        with col3:
            source_counts = global_threats_tab2['Attack Source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']
            fig5 = px.pie(source_counts, values='Count', names='Source')
            fig5 = apply_plotly_theme(fig5, title='Attack Sources Distribution')
            fig5.update_layout(
                height=350,
                margin=dict(l=50, r=50, t=60, b=50)
            )
            st.plotly_chart(fig5, use_container_width=True)



        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Section 4: Industry Impact Analysis - Cross-dimensional relationships
        st.subheader("Industry Impact Analysis")
        col1, col2 = st.columns(2)
        with col1:
            heatmap_data = pd.crosstab(global_threats_tab2['Attack Type'], global_threats_tab2['Target Industry'])
            fig8 = px.imshow(heatmap_data, labels=dict(x="Industry", y="Attack Type", color="Frequency"), aspect='auto', color_continuous_scale='Blues')
            fig8 = apply_plotly_theme(fig8, title='Attack Type × Industry Heatmap')
            fig8.update_layout(
                height=450,
                margin=dict(l=120, r=50, t=60, b=120),
                xaxis_tickangle=-45,
                xaxis_tickfont=dict(size=9),
                yaxis_tickfont=dict(size=9)
            )
            st.plotly_chart(fig8, use_container_width=True)
        with col2:
            treemap_data = global_threats_tab2.groupby(['Target Industry', 'Attack Type'])['Financial Loss (in Million $)'].sum().reset_index()
            treemap_data = treemap_data.sort_values('Financial Loss (in Million $)', ascending=False).head(50)
            fig9 = px.treemap(treemap_data, path=['Target Industry', 'Attack Type'], values='Financial Loss (in Million $)', color='Financial Loss (in Million $)', color_continuous_scale='RdYlGn_r')
            fig9 = apply_plotly_theme(fig9, title='Financial Losses by Industry and Attack Type')
            fig9.update_layout(
                height=450,
                margin=dict(l=50, r=50, t=60, b=50)
            )
            st.plotly_chart(fig9, use_container_width=True)

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Section 5: Industry Distribution - How attacks vary across industries
        st.subheader("Industry Distribution")
        bar_data = global_threats_tab2.groupby(['Target Industry', 'Attack Type']).size().reset_index(name='Count')
        fig10 = px.bar(bar_data, x='Target Industry', y='Count', color='Attack Type', barmode='group')
        fig10 = apply_plotly_theme(fig10, title='Attack Distribution by Industry and Type')
        fig10.update_layout(
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=60, r=150, t=60, b=120),
            xaxis_tickfont=dict(size=10),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.0,
                xanchor="left",
                x=1.02,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor=COLORS["border_color"],
                borderwidth=1
            )
        )
        st.plotly_chart(fig10, use_container_width=True)

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
                             barmode='group',
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]},
                             labels={'protocol_type': 'Protocol', 'Count': 'Number of Records'})
                fig = apply_plotly_theme(fig, title='Traffic Volume by Protocol and Classification')
                fig.update_layout(
                    height=400,
                    xaxis_tickangle=-30,
                    margin=dict(l=60, r=150, t=60, b=80),
                    xaxis_tickfont=dict(size=10),
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=1.0,
                        xanchor="left",
                        x=1.02,
                        bgcolor="rgba(255, 255, 255, 0.9)",
                        bordercolor=COLORS["border_color"],
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

            protocol_pct = intrusion_data.groupby(['protocol_type', 'attack_detected']).size().unstack(fill_value=0)
            protocol_pct.columns = ['Normal', 'Attack']

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Normal', x=protocol_pct.index, y=protocol_pct['Normal'],
                                 marker_color=COLORS["accent_blue"]))
            fig.add_trace(go.Bar(name='Attack', x=protocol_pct.index, y=protocol_pct['Attack'],
                                 marker_color=COLORS["accent_red"]))

            fig = apply_plotly_theme(fig, title='Protocol Distribution: Attack vs Normal (Stacked)')
            fig.update_layout(
                barmode='stack',
                xaxis_title='Protocol Type',
                yaxis_title='Count',
                height=400,
                xaxis_tickangle=-30,
                margin=dict(l=60, r=50, t=60, b=80),
                xaxis_tickfont=dict(size=10),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor=COLORS["border_color"],
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                encryption_dist = intrusion_data['encryption_used'].value_counts().reset_index()
                encryption_dist.columns = ['Encryption', 'Count']

                fig = px.bar(encryption_dist, x='Encryption', y='Count',
                             color='Count',
                             color_continuous_scale='Blues')
                fig = apply_plotly_theme(fig, title='Encryption Type Distribution')
                fig.update_layout(
                    height=400,
                    xaxis_tickangle=-45,
                    margin=dict(l=60, r=50, t=60, b=100),
                    xaxis_tickfont=dict(size=10)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                browser_dist = intrusion_data['browser_type'].value_counts().head(10).reset_index()
                browser_dist.columns = ['Browser', 'Count']

                fig = px.bar(browser_dist, x='Count', y='Browser',
                             orientation='h',
                             color='Count',
                             color_continuous_scale='Greens')
                fig = apply_plotly_theme(fig, title='Top 10 Browser Types')
                fig.update_layout(
                    height=400,
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(l=120, r=50, t=60, b=50),
                    yaxis_tickfont=dict(size=10)
                )
                st.plotly_chart(fig, use_container_width=True)

        with subtab2:
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
                            color='Classification',
                            box=True,
                            points='outliers',
                            color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
            fig = apply_plotly_theme(fig, title=f'{selected_feature.replace("_", " ").title()} Distribution by Classification')
            fig.update_layout(
                height=500,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor=COLORS["border_color"],
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(intrusion_data, x=selected_feature, color='Classification',
                                   nbins=50,
                                   barmode='overlay',
                                   opacity=0.7,
                                   color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig, title=f'{selected_feature.replace("_", " ").title()} Distribution')
                fig.update_layout(
                    height=400,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99,
                        bgcolor="rgba(255, 255, 255, 0.9)",
                        bordercolor=COLORS["border_color"],
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.box(intrusion_data, x='Classification', y=selected_feature,
                             color='Classification',
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig, title=f'{selected_feature.replace("_", " ").title()} Box Plot')
                fig.update_layout(
                    height=400,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99,
                        bgcolor="rgba(255, 255, 255, 0.9)",
                        bordercolor=COLORS["border_color"],
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

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
            fig = px.scatter(intrusion_data.sample(min(5000, len(intrusion_data))),
                             x='login_attempts',
                             y='failed_logins',
                             color='Classification',
                             opacity=0.6,
                             color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]},
                             hover_data=['session_duration', 'ip_reputation_score'])
            fig = apply_plotly_theme(fig, title='Login Attempts vs Failed Logins')
            fig.update_layout(
                height=500,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor=COLORS["border_color"],
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            corr_data = intrusion_data[numeric_features + ['attack_detected']].corr()

            fig = px.imshow(corr_data,
                             labels=dict(color="Correlation"),
                             color_continuous_scale='RdBu_r',
                             aspect='auto',
                             zmin=-1,
                             zmax=1)
            fig = apply_plotly_theme(fig, title='Feature Correlation Heatmap')
            fig.update_layout(
                height=600,
                xaxis_tickangle=-45,
                margin=dict(l=120, r=50, t=60, b=120),
                xaxis_tickfont=dict(size=9),
                yaxis_tickfont=dict(size=9)
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                unusual_time_data = intrusion_data.groupby(['unusual_time_access', 'attack_detected']).size().reset_index(name='Count')
                unusual_time_data['Unusual Time'] = unusual_time_data['unusual_time_access'].map({0: 'Normal Hours', 1: 'Unusual Hours'})
                unusual_time_data['Classification'] = unusual_time_data['attack_detected'].map({0: 'Normal', 1: 'Attack'})

                fig = px.bar(unusual_time_data, x='Unusual Time', y='Count', color='Classification',
                              barmode='group',
                              color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig, title='Attack Distribution by Access Time')
                fig.update_layout(
                    height=400,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99,
                        bgcolor="rgba(255, 255, 255, 0.9)",
                        bordercolor=COLORS["border_color"],
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.histogram(intrusion_data, x='ip_reputation_score', color='Classification',
                                    nbins=50,
                                    barmode='overlay',
                                    opacity=0.7,
                                    color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
                fig = apply_plotly_theme(fig, title='IP Reputation Score Distribution')
                fig.update_layout(
                    height=400,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99,
                        bgcolor="rgba(255, 255, 255, 0.9)",
                        bordercolor=COLORS["border_color"],
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

            sample_data = intrusion_data.sample(min(3000, len(intrusion_data)))

            fig = px.scatter_3d(sample_data,
                                 x='login_attempts',
                                 y='session_duration',
                                 z='ip_reputation_score',
                                 color='Classification',
                                 opacity=0.6,
                                 color_discrete_map={'Attack': COLORS["accent_red"], 'Normal': COLORS["accent_blue"]})
            fig = apply_plotly_theme(fig, title='3D Feature Space: Login Attempts × Session Duration × IP Reputation')
            fig.update_layout(
                height=700,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor=COLORS["border_color"],
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            protocol_encryption = pd.crosstab(intrusion_data['protocol_type'],
                                             intrusion_data['encryption_used'],
                                             values=intrusion_data['attack_detected'],
                                             aggfunc='mean')

            fig = px.imshow(protocol_encryption,
                             labels=dict(x="Encryption Type", y="Protocol Type", color="Attack Rate"),
                             color_continuous_scale='Reds',
                             aspect='auto')
            fig = apply_plotly_theme(fig, title='Attack Rate by Protocol × Encryption')
            fig.update_layout(
                height=400,
                xaxis_tickangle=-45,
                margin=dict(l=100, r=50, t=60, b=100),
                xaxis_tickfont=dict(size=10),
                yaxis_tickfont=dict(size=10)
            )
            st.plotly_chart(fig, use_container_width=True)
