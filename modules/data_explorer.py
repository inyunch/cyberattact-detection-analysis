import streamlit as st
import pandas as pd

def show(intrusion_data_original):
    """
    Display the Data Explorer page.
    """
    st.markdown("## 📋 Data Explorer")

    st.markdown("### 🔍 Search and Filter")

    search_col1, search_col2 = st.columns(2)

    with search_col1:
        session_search = st.text_input("Search by Session ID", "")

    with search_col2:
        min_packet_size = st.number_input("Min Packet Size", min_value=0, value=0)

    display_data = intrusion_data_original.copy()

    if session_search:
        display_data = display_data[display_data['session_id'].str.contains(session_search, case=False, na=False)]

    if min_packet_size > 0:
        display_data = display_data[display_data['network_packet_size'] >= min_packet_size]

    st.markdown(f"### Filtered Dataset ({len(display_data)} records)")

    st.dataframe(
        display_data.head(100),
        use_container_width=True,
        height=400
    )

    csv = display_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name='filtered_intrusion_data.csv',
        mime='text/csv'
    )

    st.markdown("### 📊 Summary Statistics by Protocol")

    stats_by_protocol = display_data.groupby('protocol_type').agg({
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

    st.markdown("### 🎯 Classification Breakdown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**By Protocol**")
        protocol_attack_rate = display_data.groupby('protocol_type')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
        protocol_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
        st.dataframe(protocol_attack_rate)

    with col2:
        st.markdown("**By Encryption**")
        encryption_attack_rate = display_data.groupby('encryption_used')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
        encryption_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
        st.dataframe(encryption_attack_rate)

    with col3:
        st.markdown("**By Unusual Time Access**")
        time_attack_rate = display_data.groupby('unusual_time_access')['attack_detected'].agg(['sum', 'count', 'mean']).round(3)
        time_attack_rate.columns = ['Attacks', 'Total', 'Attack Rate']
        time_attack_rate.index = ['Normal Hours', 'Unusual Hours']
        st.dataframe(time_attack_rate)
