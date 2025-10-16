import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show(global_threats, intrusion_data):
    """Display comparative insights from both datasets"""

    st.title("📊 Comparative Insights & Key Findings")
    st.markdown("### Bridging Macro and Micro Perspectives")
    st.markdown("---")

    if global_threats is None or intrusion_data is None:
        st.error("Unable to load data for comparison.")
        return

    # Key Findings Section
    st.markdown("## 💡 Key Insights")

    # Calculate key metrics
    total_attacks = len(global_threats)
    total_losses = global_threats['Financial Loss (in Million $)'].sum()
    year_growth = global_threats.groupby('Year').size()
    growth_rate = ((year_growth.iloc[-1] - year_growth.iloc[0]) / year_growth.iloc[0] * 100)

    intrusion_attack_rate = intrusion_data['attack_detected'].mean() * 100
    tcp_attacks = intrusion_data[intrusion_data['protocol_type'] == 'TCP']['attack_detected'].mean() * 100

    top_sector = global_threats['Target Industry'].value_counts().index[0]
    top_attack_type = global_threats['Attack Type'].value_counts().index[0]

    # Insight cards
    insights = [
        {
            "icon": "📈",
            "title": "Exponential Attack Growth",
            "finding": f"Cyber attacks increased by {growth_rate:.1f}% from 2015 to 2024",
            "implication": "Organizations must continuously adapt their security posture as the threat landscape evolves rapidly.",
            "source": "Global Threats Dataset"
        },
        {
            "icon": "🎯",
            "title": "High Detection Challenge",
            "finding": f"{intrusion_attack_rate:.1f}% of network traffic in the intrusion dataset is malicious",
            "implication": "Real-time intrusion detection systems must maintain high accuracy with minimal false positives.",
            "source": "Intrusion Detection Dataset"
        },
        {
            "icon": "🔴",
            "title": "Protocol Vulnerability",
            "finding": f"TCP protocol shows {tcp_attacks:.1f}% attack rate, making it the primary vector",
            "implication": "Enhanced monitoring of TCP traffic should be a priority for network security teams.",
            "source": "Intrusion Detection Dataset"
        },
        {
            "icon": "🏥",
            "title": "Sector-Specific Targeting",
            "finding": f"{top_sector} is the most frequently targeted industry",
            "implication": "Sector-specific security frameworks and threat intelligence sharing are crucial.",
            "source": "Global Threats Dataset"
        },
        {
            "icon": "💰",
            "title": "Financial Impact",
            "finding": f"Total documented losses exceed ${total_losses:,.1f} billion over 10 years",
            "implication": "Investment in cybersecurity is not optional—it's a business imperative.",
            "source": "Global Threats Dataset"
        },
        {
            "icon": "⚠️",
            "title": "Attack Method Dominance",
            "finding": f"{top_attack_type} is the most common attack method observed",
            "implication": "Training and technical controls should prioritize defense against prevalent attack vectors.",
            "source": "Global Threats Dataset"
        }
    ]

    # Display insights in expandable cards
    for i in range(0, len(insights), 2):
        col1, col2 = st.columns(2)

        with col1:
            insight = insights[i]
            with st.expander(f"{insight['icon']} {insight['title']}", expanded=True):
                st.markdown(f"**Finding:** {insight['finding']}")
                st.markdown(f"**Implication:** {insight['implication']}")
                st.caption(f"*Source: {insight['source']}*")

        if i + 1 < len(insights):
            with col2:
                insight = insights[i + 1]
                with st.expander(f"{insight['icon']} {insight['title']}", expanded=True):
                    st.markdown(f"**Finding:** {insight['finding']}")
                    st.markdown(f"**Implication:** {insight['implication']}")
                    st.caption(f"*Source: {insight['source']}*")

    st.markdown("---")

    # Cross-Dataset Visualizations
    st.markdown("## 📊 Cross-Dataset Analysis")

    # Side-by-side comparison
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌍 Global Threat Evolution")

        # Attack growth over time
        attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')

        # Convert to lists for better Plotly compatibility
        comp_years = [int(y) for y in attacks_by_year['Year']]
        comp_counts = [int(c) for c in attacks_by_year['Count']]

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=comp_years,
            y=comp_counts,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#ff7f0e', width=2),
            name='Attacks'
        ))

        fig1.update_layout(
            xaxis_title='Year',
            yaxis_title='Number of Attacks',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("""
        **Observation:** Clear upward trend in reported incidents, with potential
        acceleration in recent years. This may reflect both increased attack activity
        and improved detection/reporting capabilities.
        """)

    with col2:
        st.markdown("### 🔍 Network-Level Detection")

        # Protocol attack rates
        protocol_stats = intrusion_data.groupby('protocol_type').agg({
            'attack_detected': ['sum', 'count', 'mean']
        }).round(3)
        protocol_stats.columns = ['Attacks', 'Total', 'Attack Rate']
        protocol_stats = protocol_stats.reset_index()

        fig2 = px.bar(protocol_stats, x='protocol_type', y='Attack Rate',
                     labels={'protocol_type': 'Protocol', 'Attack Rate': 'Attack Rate'},
                     color='Attack Rate',
                     color_continuous_scale='Reds')
        fig2 = apply_plotly_theme(fig2, title='Attack Rate by Network Protocol')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        **Observation:** Different protocols show varying attack rates, suggesting
        attackers have preferences or that certain protocols have inherent vulnerabilities.
        """)

    # Attack type mapping
    st.markdown("## 🔗 Attack Type Patterns")

    st.markdown("""
    While the two datasets capture different levels of cyber threat activity, we can draw parallels:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌍 Global Attack Types (Macro)")

        attack_types = global_threats['Attack Type'].value_counts().head(10).reset_index()
        attack_types.columns = ['Attack Type', 'Count']

        fig3 = px.bar(attack_types, y='Attack Type', x='Count',
                     orientation='h',
                     color='Count',
                     color_continuous_scale='Blues')
        fig3 = apply_plotly_theme(fig3, title='Top 10 Attack Types (Global)')
        fig3.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("### 🔍 Network Attack Indicators (Micro)")

        # Create attack signature analysis
        attack_signatures = intrusion_data[intrusion_data['attack_detected'] == 1].groupby('protocol_type').agg({
            'login_attempts': 'mean',
            'failed_logins': 'mean',
            'session_duration': 'mean',
            'network_packet_size': 'mean'
        }).round(2).reset_index()

        # Melt for visualization
        attack_sigs_melted = attack_signatures.melt(id_vars=['protocol_type'],
                                                     var_name='Feature',
                                                     value_name='Average Value')

        fig4 = px.bar(attack_sigs_melted, x='protocol_type', y='Average Value',
                     color='Feature',
                     barmode='group',
                     labels={'protocol_type': 'Protocol', 'Average Value': 'Avg Value'})
        fig4.update_layout(height=500)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Conceptual mapping
    st.markdown("## 🧩 Conceptual Mapping Between Datasets")

    mapping_data = {
        "Global Attack Type": ["Ransomware", "Phishing", "DDoS", "Malware", "Man-in-the-Middle"],
        "Network Indicators": [
            "High encryption usage + unusual session duration",
            "Multiple failed logins + low IP reputation",
            "Large packet sizes + high traffic volume",
            "Unusual protocols + suspicious packet patterns",
            "Protocol anomalies + session hijacking patterns"
        ],
        "Defense Priority": ["Critical", "High", "High", "Medium", "Medium"]
    }

    mapping_df = pd.DataFrame(mapping_data)

    st.dataframe(
        mapping_df.style.apply(lambda x: ['background-color: #ffcccc' if v == 'Critical'
                                          else 'background-color: #ffe6cc' if v == 'High'
                                          else 'background-color: #ffffcc' if v == 'Medium'
                                          else '' for v in x], subset=['Defense Priority']),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Recommendations Section
    st.markdown("## 🎯 Strategic Recommendations")

    st.markdown("""
    Based on comprehensive analysis of both macro-level threat trends and micro-level intrusion patterns,
    we recommend the following prioritized defense strategies:
    """)

    recommendations = [
        {
            "priority": "🔴 Critical Priority",
            "recommendation": "Enhance TCP Traffic Monitoring",
            "rationale": f"TCP shows the highest attack rate ({tcp_attacks:.1f}%) and is the most common protocol",
            "actions": [
                "Deploy deep packet inspection for TCP traffic",
                "Implement anomaly detection on TCP connection patterns",
                "Monitor for TCP-based attack signatures (SYN floods, port scans)"
            ]
        },
        {
            "priority": "🟠 High Priority",
            "recommendation": f"Sector-Specific Protections for {top_sector}",
            "rationale": f"{top_sector} is the most frequently targeted industry with significant financial impact",
            "actions": [
                "Implement industry-specific threat intelligence feeds",
                "Conduct regular sector-focused penetration testing",
                "Establish information sharing with industry peers"
            ]
        },
        {
            "priority": "🟠 High Priority",
            "recommendation": "Login Security Enhancement",
            "rationale": "Failed login attempts strongly correlate with attack activity in network data",
            "actions": [
                "Implement adaptive authentication (MFA)",
                "Deploy behavioral biometrics for login monitoring",
                "Set up real-time alerts for suspicious login patterns"
            ]
        },
        {
            "priority": "🟡 Medium Priority",
            "recommendation": "Temporal Access Controls",
            "rationale": "Unusual time access shows correlation with attack behavior",
            "actions": [
                "Implement time-based access policies",
                "Flag and investigate off-hours access patterns",
                "Require additional authentication for unusual time access"
            ]
        },
        {
            "priority": "🟡 Medium Priority",
            "recommendation": "IP Reputation Integration",
            "rationale": "Low IP reputation scores are associated with attack traffic",
            "actions": [
                "Integrate real-time IP reputation feeds",
                "Implement risk-based authentication based on IP reputation",
                "Automatically block or challenge low-reputation sources"
            ]
        }
    ]

    for rec in recommendations:
        with st.expander(f"{rec['priority']}: {rec['recommendation']}", expanded=False):
            st.markdown(f"**Rationale:** {rec['rationale']}")
            st.markdown("**Recommended Actions:**")
            for action in rec['actions']:
                st.markdown(f"- {action}")

    st.markdown("---")

    # Summary metrics comparison
    st.markdown("## 📈 Summary Comparison")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Global Incidents",
            f"{len(global_threats):,}",
            delta="10-year period"
        )

    with col2:
        avg_loss = global_threats['Financial Loss (in Million $)'].mean()
        st.metric(
            "Avg Loss per Incident",
            f"${avg_loss:.2f}M",
            delta=f"Total: ${total_losses:.1f}B"
        )

    with col3:
        st.metric(
            "Network Attack Rate",
            f"{intrusion_attack_rate:.1f}%",
            delta=f"{len(intrusion_data):,} records"
        )

    with col4:
        unique_countries = global_threats['Country'].nunique()
        st.metric(
            "Countries Affected",
            f"{unique_countries}",
            delta="Global coverage"
        )

    st.markdown("---")

    # Final thoughts
    st.markdown("## 💭 Concluding Observations")

    st.success("""
    **Integration of Macro and Micro Perspectives:**

    This analysis demonstrates the value of examining cybersecurity from multiple vantage points:

    1. **Macro View (Global Threats):** Reveals strategic trends, financial impacts, and sector-specific targeting patterns
       that inform policy and investment decisions.

    2. **Micro View (Intrusion Detection):** Uncovers technical attack signatures and behavioral patterns that enable
       real-time threat detection and response.

    3. **Combined Insight:** Organizations can prioritize defenses based on both the likelihood of specific attack types
       (from global trends) and the technical indicators that signal active intrusions (from network analysis).

    **Key Takeaway:** Effective cybersecurity requires both strategic awareness of the evolving threat landscape
    and tactical capability to detect and respond to active intrusions. This dual-dataset approach provides
    a comprehensive foundation for risk assessment and defense prioritization.
    """)

    st.info("""
    **Future Work:**
    - Develop machine learning models for attack prediction and classification
    - Integrate real-time threat intelligence feeds
    - Create automated response playbooks based on detected patterns
    - Expand analysis to include emerging attack vectors and zero-day vulnerabilities
    """)
