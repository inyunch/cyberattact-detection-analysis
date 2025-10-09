import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show(intrusion_data):
    """Display intrusion detection analysis"""

    st.title("🔍 Intrusion Detection Analysis")
    st.markdown("### Network-level patterns and behavioral analysis")
    st.markdown("---")

    if intrusion_data is None:
        st.error("Unable to load intrusion detection data.")
        return

    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters")

    # Classification filter
    classification_options = ['All', 'Attack', 'Normal']
    selected_classification = st.sidebar.selectbox(
        "🎯 Classification",
        options=classification_options
    )

    # Protocol filter
    protocols = ['All'] + sorted(intrusion_data['protocol_type'].unique().tolist())
    selected_protocols = st.sidebar.multiselect(
        "📡 Protocol Type",
        options=protocols,
        default=['All']
    )

    # Encryption filter
    encryption_types = ['All'] + sorted(intrusion_data['encryption_used'].unique().tolist())
    selected_encryption = st.sidebar.multiselect(
        "🔐 Encryption Type",
        options=encryption_types,
        default=['All']
    )

    # Browser filter
    browsers = ['All'] + sorted(intrusion_data['browser_type'].unique().tolist())
    selected_browsers = st.sidebar.multiselect(
        "🌐 Browser Type",
        options=browsers,
        default=['All']
    )

    # Apply filters
    filtered_data = intrusion_data.copy()

    if selected_classification != 'All':
        filtered_data = filtered_data[
            filtered_data['attack_detected'] == (1 if selected_classification == 'Attack' else 0)
        ]

    if 'All' not in selected_protocols:
        filtered_data = filtered_data[filtered_data['protocol_type'].isin(selected_protocols)]

    if 'All' not in selected_encryption:
        filtered_data = filtered_data[filtered_data['encryption_used'].isin(selected_encryption)]

    if 'All' not in selected_browsers:
        filtered_data = filtered_data[filtered_data['browser_type'].isin(selected_browsers)]

    # Display filter results
    attack_count = filtered_data['attack_detected'].sum()
    normal_count = len(filtered_data) - attack_count
    attack_rate = (attack_count / len(filtered_data) * 100) if len(filtered_data) > 0 else 0

    st.info(f"📊 Showing **{len(filtered_data):,}** records | Attacks: **{attack_count:,}** ({attack_rate:.1f}%) | Normal: **{normal_count:,}**")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Feature Distributions",
        "🔬 Behavioral Analysis",
        "📋 Data Explorer"
    ])

    # TAB 1: Overview
    with tab1:
        st.markdown("## 📊 Classification Overview")

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", f"{len(filtered_data):,}")
        with col2:
            st.metric("Attack Records", f"{attack_count:,}", delta=f"{attack_rate:.1f}%")
        with col3:
            st.metric("Normal Records", f"{normal_count:,}", delta=f"{100-attack_rate:.1f}%")
        with col4:
            avg_ip_score = filtered_data['ip_reputation_score'].mean()
            st.metric("Avg IP Reputation", f"{avg_ip_score:.2f}")

        # Attack vs Normal distribution
        col1, col2 = st.columns(2)

        with col1:
            class_dist = filtered_data['attack_detected'].value_counts().reset_index()
            class_dist.columns = ['Classification', 'Count']
            class_dist['Classification'] = class_dist['Classification'].map({0: 'Normal', 1: 'Attack'})

            fig1 = px.pie(class_dist, values='Count', names='Classification',
                         title='Attack vs Normal Distribution',
                         color='Classification',
                         color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Protocol distribution by classification
            protocol_class = filtered_data.groupby(['protocol_type', 'attack_detected']).size().reset_index(name='Count')
            protocol_class['Classification'] = protocol_class['attack_detected'].map({0: 'Normal', 1: 'Attack'})

            fig2 = px.bar(protocol_class, x='protocol_type', y='Count', color='Classification',
                         title='Traffic Volume by Protocol and Classification',
                         barmode='group',
                         color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'},
                         labels={'protocol_type': 'Protocol', 'Count': 'Number of Records'})
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

        # Stacked bar: Protocol breakdown
        protocol_pct = filtered_data.groupby(['protocol_type', 'attack_detected']).size().unstack(fill_value=0)
        protocol_pct.columns = ['Normal', 'Attack']

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Normal', x=protocol_pct.index, y=protocol_pct['Normal'],
                             marker_color='#4444ff'))
        fig3.add_trace(go.Bar(name='Attack', x=protocol_pct.index, y=protocol_pct['Attack'],
                             marker_color='#ff4444'))

        fig3.update_layout(
            barmode='stack',
            title='Protocol Distribution: Attack vs Normal (Stacked)',
            xaxis_title='Protocol Type',
            yaxis_title='Count',
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Encryption analysis
        col1, col2 = st.columns(2)

        with col1:
            encryption_dist = filtered_data['encryption_used'].value_counts().reset_index()
            encryption_dist.columns = ['Encryption', 'Count']

            fig4 = px.bar(encryption_dist, x='Encryption', y='Count',
                         title='Encryption Type Distribution',
                         color='Count',
                         color_continuous_scale='Blues')
            fig4.update_layout(height=400)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            browser_dist = filtered_data['browser_type'].value_counts().head(10).reset_index()
            browser_dist.columns = ['Browser', 'Count']

            fig5 = px.bar(browser_dist, x='Count', y='Browser',
                         title='Top 10 Browser Types',
                         orientation='h',
                         color='Count',
                         color_continuous_scale='Greens')
            fig5.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig5, use_container_width=True)

    # TAB 2: Feature Distributions
    with tab2:
        st.markdown("## 📈 Feature Distribution Analysis")

        # Feature selector
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

        # Create label for classification
        filtered_data['Classification'] = filtered_data['attack_detected'].map({0: 'Normal', 1: 'Attack'})

        # Violin plot
        fig6 = px.violin(filtered_data, x='Classification', y=selected_feature,
                        title=f'{selected_feature.replace("_", " ").title()} Distribution by Classification',
                        color='Classification',
                        box=True,
                        points='outliers',
                        color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
        fig6.update_layout(height=500)
        st.plotly_chart(fig6, use_container_width=True)

        # Histogram with overlay
        col1, col2 = st.columns(2)

        with col1:
            fig7 = px.histogram(filtered_data, x=selected_feature, color='Classification',
                               title=f'{selected_feature.replace("_", " ").title()} Distribution',
                               nbins=50,
                               barmode='overlay',
                               opacity=0.7,
                               color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
            fig7.update_layout(height=400)
            st.plotly_chart(fig7, use_container_width=True)

        with col2:
            fig8 = px.box(filtered_data, x='Classification', y=selected_feature,
                         title=f'{selected_feature.replace("_", " ").title()} Box Plot',
                         color='Classification',
                         color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
            fig8.update_layout(height=400)
            st.plotly_chart(fig8, use_container_width=True)

        # All numeric features comparison
        st.markdown("### 📊 All Features Overview")

        col1, col2 = st.columns(2)

        attack_data = filtered_data[filtered_data['attack_detected'] == 1][numeric_features]
        normal_data = filtered_data[filtered_data['attack_detected'] == 0][numeric_features]

        with col1:
            st.markdown("**Attack Traffic Statistics**")
            st.dataframe(attack_data.describe().round(2), use_container_width=True)

        with col2:
            st.markdown("**Normal Traffic Statistics**")
            st.dataframe(normal_data.describe().round(2), use_container_width=True)

    # TAB 3: Behavioral Analysis
    with tab3:
        st.markdown("## 🔬 Behavioral Pattern Analysis")

        # Scatter plot: Login attempts vs failed logins
        fig9 = px.scatter(filtered_data.sample(min(5000, len(filtered_data))),
                         x='login_attempts',
                         y='failed_logins',
                         color='Classification',
                         title='Login Attempts vs Failed Logins',
                         opacity=0.6,
                         color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'},
                         hover_data=['session_duration', 'ip_reputation_score'])
        fig9.update_layout(height=500)
        st.plotly_chart(fig9, use_container_width=True)

        # Correlation heatmap
        st.markdown("### 🔥 Feature Correlation Matrix")

        corr_data = filtered_data[numeric_features + ['attack_detected']].corr()

        fig10 = px.imshow(corr_data,
                         labels=dict(color="Correlation"),
                         title='Feature Correlation Heatmap',
                         color_continuous_scale='RdBu_r',
                         aspect='auto',
                         zmin=-1,
                         zmax=1)
        fig10.update_layout(height=600)
        st.plotly_chart(fig10, use_container_width=True)

        # Unusual time access analysis
        col1, col2 = st.columns(2)

        with col1:
            unusual_time_data = filtered_data.groupby(['unusual_time_access', 'attack_detected']).size().reset_index(name='Count')
            unusual_time_data['Unusual Time'] = unusual_time_data['unusual_time_access'].map({0: 'Normal Hours', 1: 'Unusual Hours'})
            unusual_time_data['Classification'] = unusual_time_data['attack_detected'].map({0: 'Normal', 1: 'Attack'})

            fig11 = px.bar(unusual_time_data, x='Unusual Time', y='Count', color='Classification',
                          title='Attack Distribution by Access Time',
                          barmode='group',
                          color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
            fig11.update_layout(height=400)
            st.plotly_chart(fig11, use_container_width=True)

        with col2:
            # IP reputation vs attack
            fig12 = px.histogram(filtered_data, x='ip_reputation_score', color='Classification',
                                title='IP Reputation Score Distribution',
                                nbins=50,
                                barmode='overlay',
                                opacity=0.7,
                                color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
            fig12.update_layout(height=400)
            st.plotly_chart(fig12, use_container_width=True)

        # Advanced: 3D scatter plot
        st.markdown("### 🌐 3D Feature Space Visualization")

        sample_data = filtered_data.sample(min(3000, len(filtered_data)))

        fig13 = px.scatter_3d(sample_data,
                             x='login_attempts',
                             y='session_duration',
                             z='ip_reputation_score',
                             color='Classification',
                             title='3D Feature Space: Login Attempts × Session Duration × IP Reputation',
                             opacity=0.6,
                             color_discrete_map={'Attack': '#ff4444', 'Normal': '#4444ff'})
        fig13.update_layout(height=700)
        st.plotly_chart(fig13, use_container_width=True)

        # Protocol × Encryption analysis
        st.markdown("### 🔐 Protocol and Encryption Patterns")

        protocol_encryption = pd.crosstab(filtered_data['protocol_type'],
                                         filtered_data['encryption_used'],
                                         values=filtered_data['attack_detected'],
                                         aggfunc='mean')

        fig14 = px.imshow(protocol_encryption,
                         labels=dict(x="Encryption Type", y="Protocol Type", color="Attack Rate"),
                         title='Attack Rate by Protocol × Encryption',
                         color_continuous_scale='Reds',
                         aspect='auto')
        fig14.update_layout(height=400)
        st.plotly_chart(fig14, use_container_width=True)

    # TAB 4: Data Explorer
    with tab4:
        st.markdown("## 📋 Data Explorer")

        # Search functionality
        st.markdown("### 🔍 Search and Filter")

        search_col1, search_col2 = st.columns(2)

        with search_col1:
            session_search = st.text_input("Search by Session ID", "")

        with search_col2:
            min_packet_size = st.number_input("Min Packet Size", min_value=0, value=0)

        # Apply search filters
        display_data = filtered_data.copy()

        if session_search:
            display_data = display_data[display_data['session_id'].str.contains(session_search, case=False, na=False)]

        if min_packet_size > 0:
            display_data = display_data[display_data['network_packet_size'] >= min_packet_size]

        st.markdown(f"### Filtered Dataset ({len(display_data)} records)")

        # Display data with color coding
        st.dataframe(
            display_data.head(100),
            use_container_width=True,
            height=400
        )

        # Download button
        csv = display_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name='filtered_intrusion_data.csv',
            mime='text/csv'
        )

        # Summary statistics
        st.markdown("### 📊 Summary Statistics by Protocol")

        stats_by_protocol = filtered_data.groupby('protocol_type').agg({
            'attack_detected': ['count', 'sum', 'mean'],
            'network_packet_size': ['mean', 'median'],
            'session_duration': ['mean', 'median'],
            'login_attempts': ['mean', 'median'],
            'ip_reputation_score': ['mean']
        }).round(3)

        stats_by_protocol.columns = ['Count', 'Attacks', 'Attack Rate',
                                     'Avg Packet Size', 'Median Packet Size',
                                     'Avg Session Duration', 'Median Session Duration',
                                     'Avg Login Attempts', 'Median Login Attempts',
                                     'Avg IP Reputation']

        st.dataframe(stats_by_protocol, use_container_width=True)

        # Classification metrics
        st.markdown("### 🎯 Classification Breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**By Protocol**")
            protocol_attack_rate = filtered_data.groupby('protocol_type')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
            protocol_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
            st.dataframe(protocol_attack_rate)

        with col2:
            st.markdown("**By Encryption**")
            encryption_attack_rate = filtered_data.groupby('encryption_used')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
            encryption_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
            st.dataframe(encryption_attack_rate)

        with col3:
            st.markdown("**By Unusual Time Access**")
            time_attack_rate = filtered_data.groupby('unusual_time_access')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
            time_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
            time_attack_rate.index = ['Normal Hours', 'Unusual Hours']
            st.dataframe(time_attack_rate)
