"""
Phishing Detection Dashboard Module

This module provides comprehensive visualization and analysis of phishing detection data,
including URL characteristics, security indicators, and threat patterns.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from modules.theme import COLORS, apply_plotly_theme


def show(phishing_data_original):
    """Display the phishing detection dashboard page."""

    if phishing_data_original is None:
        st.error("Phishing data not loaded. Please check the data sources.")
        return

    # Add top margin to align with navigation
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Use filtered data if available, otherwise use original
    if 'filtered_data' in st.session_state and 'phishing_detection' in st.session_state.filtered_data:
        phishing_data = st.session_state.filtered_data['phishing_detection'].copy()
    else:
        phishing_data = phishing_data_original.copy()

    # ==================== METRICS ROW ====================
    total_urls = len(phishing_data)
    phishing_count = phishing_data['CLASS_LABEL'].sum()
    legitimate_count = total_urls - phishing_count
    phishing_rate = (phishing_count / total_urls * 100) if total_urls > 0 else 0

    # Calculate HTTPS usage
    https_usage = ((phishing_data['NoHttps'] == 0).sum() / total_urls * 100) if total_urls > 0 else 0

    # Calculate IP address usage
    ip_usage = (phishing_data['IpAddress'].sum() / total_urls * 100) if total_urls > 0 else 0

    # Average URL length
    avg_url_length = phishing_data['UrlLength'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total URLs Analyzed", f"{total_urls:,}")
    with col2:
        st.metric("Phishing URLs", f"{phishing_count:,}", f"{phishing_rate:.1f}%")
    with col3:
        st.metric("Legitimate URLs", f"{legitimate_count:,}", f"{100-phishing_rate:.1f}%")
    with col4:
        st.metric("HTTPS Usage", f"{https_usage:.1f}%", "Security indicator")

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # ==================== ROW 1: Key Security Indicators ====================
    r1_col1, r1_col2, r1_col3 = st.columns(3)

    with r1_col1:
        # HTTPS vs No HTTPS breakdown
        https_data = phishing_data.groupby('NoHttps')['CLASS_LABEL'].agg(['sum', 'count']).reset_index()
        https_data['percentage'] = (https_data['sum'] / https_data['count'] * 100)
        https_data['label'] = https_data['NoHttps'].map({0: 'Uses HTTPS', 1: 'No HTTPS'})

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name='Phishing',
            x=https_data['label'],
            y=https_data['sum'],
            marker_color=COLORS["accent_red"],
            text=https_data['sum'],
            textposition='auto'
        ))
        fig1.add_trace(go.Bar(
            name='Legitimate',
            x=https_data['label'],
            y=https_data['count'] - https_data['sum'],
            marker_color=COLORS["accent_green"],
            text=https_data['count'] - https_data['sum'],
            textposition='auto'
        ))

        fig1 = apply_plotly_theme(fig1, title='HTTPS Usage Analysis')
        fig1.update_layout(
            barmode='stack',
            xaxis_title="",
            yaxis_title="Number of URLs",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with r1_col2:
        # IP Address in URL
        ip_data = phishing_data.groupby('IpAddress')['CLASS_LABEL'].agg(['sum', 'count']).reset_index()
        ip_data['label'] = ip_data['IpAddress'].map({0: 'Domain Name', 1: 'IP Address'})

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name='Phishing',
            x=ip_data['label'],
            y=ip_data['sum'],
            marker_color=COLORS["accent_red"],
            text=ip_data['sum'],
            textposition='auto'
        ))
        fig2.add_trace(go.Bar(
            name='Legitimate',
            x=ip_data['label'],
            y=ip_data['count'] - ip_data['sum'],
            marker_color=COLORS["accent_green"],
            text=ip_data['count'] - ip_data['sum'],
            textposition='auto'
        ))

        fig2 = apply_plotly_theme(fig2, title='IP Address vs Domain Name')
        fig2.update_layout(
            barmode='stack',
            xaxis_title="",
            yaxis_title="Number of URLs",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with r1_col3:
        # Embedded Brand Name
        brand_data = phishing_data.groupby('EmbeddedBrandName')['CLASS_LABEL'].agg(['sum', 'count']).reset_index()
        brand_data['label'] = brand_data['EmbeddedBrandName'].map({0: 'No Brand', 1: 'Has Brand'})

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Phishing',
            x=brand_data['label'],
            y=brand_data['sum'],
            marker_color=COLORS["accent_red"],
            text=brand_data['sum'],
            textposition='auto'
        ))
        fig3.add_trace(go.Bar(
            name='Legitimate',
            x=brand_data['label'],
            y=brand_data['count'] - brand_data['sum'],
            marker_color=COLORS["accent_green"],
            text=brand_data['count'] - brand_data['sum'],
            textposition='auto'
        ))

        fig3 = apply_plotly_theme(fig3, title='Embedded Brand Names')
        fig3.update_layout(
            barmode='stack',
            xaxis_title="",
            yaxis_title="Number of URLs",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # ==================== ROW 2: URL Characteristics ====================
    r2_col1, r2_col2 = st.columns(2)

    with r2_col1:
        # URL Length Distribution
        fig4 = go.Figure()

        phishing_urls = phishing_data[phishing_data['CLASS_LABEL'] == 1]['UrlLength']
        legitimate_urls = phishing_data[phishing_data['CLASS_LABEL'] == 0]['UrlLength']

        fig4.add_trace(go.Histogram(
            x=phishing_urls,
            name='Phishing',
            marker_color=COLORS["accent_red"],
            opacity=0.7,
            nbinsx=30
        ))
        fig4.add_trace(go.Histogram(
            x=legitimate_urls,
            name='Legitimate',
            marker_color=COLORS["accent_green"],
            opacity=0.7,
            nbinsx=30
        ))

        fig4 = apply_plotly_theme(fig4, title='URL Length Distribution')
        fig4.update_layout(
            barmode='overlay',
            xaxis_title="URL Length (characters)",
            yaxis_title="Count",
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig4, use_container_width=True)

    with r2_col2:
        # Subdomain Level Distribution
        subdomain_stats = phishing_data.groupby(['SubdomainLevel', 'CLASS_LABEL']).size().unstack(fill_value=0)

        fig5 = go.Figure()

        if 1 in subdomain_stats.columns:
            fig5.add_trace(go.Bar(
                name='Phishing',
                x=subdomain_stats.index,
                y=subdomain_stats[1],
                marker_color=COLORS["accent_red"]
            ))

        if 0 in subdomain_stats.columns:
            fig5.add_trace(go.Bar(
                name='Legitimate',
                x=subdomain_stats.index,
                y=subdomain_stats[0],
                marker_color=COLORS["accent_green"]
            ))

        fig5 = apply_plotly_theme(fig5, title='Subdomain Level Analysis')
        fig5.update_layout(
            barmode='group',
            xaxis_title="Subdomain Level",
            yaxis_title="Count",
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # ==================== ROW 3: Behavioral Indicators ====================
    st.markdown("### 🎯 Behavioral & Content Indicators")

    r3_col1, r3_col2, r3_col3 = st.columns(3)

    with r3_col1:
        # PopUp Window
        popup_stats = phishing_data.groupby('PopUpWindow')['CLASS_LABEL'].mean() * 100

        fig6 = go.Figure(go.Bar(
            x=['No PopUp', 'Has PopUp'],
            y=[popup_stats.get(0, 0), popup_stats.get(1, 0)],
            marker_color=[COLORS["accent_green"], COLORS["accent_red"]],
            text=[f"{popup_stats.get(0, 0):.1f}%", f"{popup_stats.get(1, 0):.1f}%"],
            textposition='auto'
        ))

        fig6 = apply_plotly_theme(fig6, title='PopUp Window Phishing Rate')
        fig6.update_layout(
            xaxis_title="",
            yaxis_title="Phishing Rate (%)",
            height=260,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig6, use_container_width=True)

    with r3_col2:
        # Right Click Disabled
        rightclick_stats = phishing_data.groupby('RightClickDisabled')['CLASS_LABEL'].mean() * 100

        fig7 = go.Figure(go.Bar(
            x=['Right Click Enabled', 'Right Click Disabled'],
            y=[rightclick_stats.get(0, 0), rightclick_stats.get(1, 0)],
            marker_color=[COLORS["accent_green"], COLORS["accent_red"]],
            text=[f"{rightclick_stats.get(0, 0):.1f}%", f"{rightclick_stats.get(1, 0):.1f}%"],
            textposition='auto'
        ))

        fig7 = apply_plotly_theme(fig7, title='Right Click Disabled Phishing Rate')
        fig7.update_layout(
            xaxis_title="",
            yaxis_title="Phishing Rate (%)",
            height=260,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig7, use_container_width=True)

    with r3_col3:
        # Submit Info to Email
        email_stats = phishing_data.groupby('SubmitInfoToEmail')['CLASS_LABEL'].mean() * 100

        fig8 = go.Figure(go.Bar(
            x=['No Email Submit', 'Submits to Email'],
            y=[email_stats.get(0, 0), email_stats.get(1, 0)],
            marker_color=[COLORS["accent_green"], COLORS["accent_red"]],
            text=[f"{email_stats.get(0, 0):.1f}%", f"{email_stats.get(1, 0):.1f}%"],
            textposition='auto'
        ))

        fig8 = apply_plotly_theme(fig8, title='Submit to Email Phishing Rate')
        fig8.update_layout(
            xaxis_title="",
            yaxis_title="Phishing Rate (%)",
            height=260,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig8, use_container_width=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # ==================== ROW 4: Advanced Analysis ====================
    st.markdown("### 📊 Advanced Feature Analysis")

    r4_col1, r4_col2 = st.columns(2)

    with r4_col1:
        # External Hyperlinks Percentage
        fig9 = go.Figure()

        phishing_ext_links = phishing_data[phishing_data['CLASS_LABEL'] == 1]['PctExtHyperlinks']
        legitimate_ext_links = phishing_data[phishing_data['CLASS_LABEL'] == 0]['PctExtHyperlinks']

        fig9.add_trace(go.Box(
            y=phishing_ext_links,
            name='Phishing',
            marker_color=COLORS["accent_red"],
            boxmean='sd'
        ))
        fig9.add_trace(go.Box(
            y=legitimate_ext_links,
            name='Legitimate',
            marker_color=COLORS["accent_green"],
            boxmean='sd'
        ))

        fig9 = apply_plotly_theme(fig9, title='External Hyperlinks Percentage')
        fig9.update_layout(
            yaxis_title="Percentage",
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig9, use_container_width=True)

    with r4_col2:
        # Insecure Forms
        forms_data = phishing_data.groupby('InsecureForms')['CLASS_LABEL'].agg(['sum', 'count']).reset_index()
        forms_data['label'] = forms_data['InsecureForms'].map({0: 'Secure Forms', 1: 'Insecure Forms'})
        forms_data['phishing_rate'] = (forms_data['sum'] / forms_data['count'] * 100)

        fig10 = go.Figure()

        fig10.add_trace(go.Bar(
            x=forms_data['label'],
            y=forms_data['phishing_rate'],
            marker_color=[COLORS["accent_green"], COLORS["accent_red"]],
            text=forms_data['phishing_rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='auto'
        ))

        fig10 = apply_plotly_theme(fig10, title='Insecure Forms Phishing Rate')
        fig10.update_layout(
            xaxis_title="",
            yaxis_title="Phishing Rate (%)",
            height=300
        )
        st.plotly_chart(fig10, use_container_width=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # ==================== KEY INSIGHTS ====================
    st.markdown("### 💡 Key Insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.markdown(f"""
        <div style="background: {COLORS['accent_blue']}0D; border-left: 4px solid {COLORS['accent_blue']};
        border-radius: 8px; padding: 16px; height: 180px;">
            <h4 style="margin-top: 0; color: {COLORS['accent_blue']};">🔒 HTTPS Usage</h4>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.6; margin: 0;">
                <strong>{https_usage:.1f}%</strong> of analyzed URLs use HTTPS.
                However, HTTPS presence doesn't guarantee legitimacy - phishing sites increasingly use SSL certificates.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        ip_phishing_rate = (phishing_data[phishing_data['IpAddress'] == 1]['CLASS_LABEL'].mean() * 100) if (phishing_data['IpAddress'] == 1).any() else 0
        st.markdown(f"""
        <div style="background: {COLORS['accent_red']}0D; border-left: 4px solid {COLORS['accent_red']};
        border-radius: 8px; padding: 16px; height: 180px;">
            <h4 style="margin-top: 0; color: {COLORS['accent_red']};">⚠️ IP Address URLs</h4>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.6; margin: 0;">
                URLs containing IP addresses have a <strong>{ip_phishing_rate:.1f}%</strong> phishing rate.
                Using IP addresses instead of domain names is a strong phishing indicator.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col3:
        avg_phishing_length = phishing_data[phishing_data['CLASS_LABEL'] == 1]['UrlLength'].mean()
        avg_legitimate_length = phishing_data[phishing_data['CLASS_LABEL'] == 0]['UrlLength'].mean()
        st.markdown(f"""
        <div style="background: {COLORS['accent_green']}0D; border-left: 4px solid {COLORS['accent_green']};
        border-radius: 8px; padding: 16px; height: 180px;">
            <h4 style="margin-top: 0; color: {COLORS['accent_green']};">📏 URL Length</h4>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.6; margin: 0;">
                Average phishing URL length: <strong>{avg_phishing_length:.0f}</strong> characters<br>
                Average legitimate URL length: <strong>{avg_legitimate_length:.0f}</strong> characters<br>
                Longer URLs may indicate obfuscation attempts.
            </p>
        </div>
        """, unsafe_allow_html=True)
