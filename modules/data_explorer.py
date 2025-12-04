import streamlit as st
import pandas as pd

def show(intrusion_data_original, phishing_data_original):
    """
    Display the Data Explorer page with support for multiple datasets.
    """
    st.markdown("## 📋 Data Explorer")

    # Dataset selection
    st.markdown("### 📊 Select Dataset")
    dataset_option = st.radio(
        "Choose the dataset to explore:",
        ["Intrusion Detection Dataset", "Phishing Detection Dataset"],
        horizontal=True,
        help="Select which dataset to explore and analyze"
    )

    if dataset_option == "Intrusion Detection Dataset":
        display_data = intrusion_data_original.copy()
        dataset_type = "intrusion"
        st.info("🛡️ **Intrusion Detection Dataset** selected - Network traffic analysis")
    else:
        display_data = phishing_data_original.copy()
        dataset_type = "phishing"
        st.info("🎣 **Phishing Detection Dataset** selected - URL feature analysis")

    st.markdown("---")
    st.markdown("### 🔍 Search and Filter")

    if dataset_type == "intrusion":
        # Intrusion dataset filters
        search_col1, search_col2 = st.columns(2)

        with search_col1:
            session_search = st.text_input("Search by Session ID", "")

        with search_col2:
            min_packet_size = st.number_input("Min Packet Size", min_value=0, value=0)

        if session_search:
            display_data = display_data[display_data['session_id'].str.contains(session_search, case=False, na=False)]

        if min_packet_size > 0:
            display_data = display_data[display_data['network_packet_size'] >= min_packet_size]

    else:
        # Phishing dataset filters
        search_col1, search_col2 = st.columns(2)

        with search_col1:
            min_url_length = st.number_input("Min URL Length", min_value=0, value=0)

        with search_col2:
            https_filter = st.selectbox("HTTPS Filter", ["All", "HTTPS Only", "No HTTPS"])

        if min_url_length > 0:
            display_data = display_data[display_data['UrlLength'] >= min_url_length]

        if https_filter == "HTTPS Only":
            display_data = display_data[display_data['NoHttps'] == 0]
        elif https_filter == "No HTTPS":
            display_data = display_data[display_data['NoHttps'] == 1]

    st.markdown(f"### Filtered Dataset ({len(display_data)} records)")

    st.dataframe(
        display_data.head(100),
        use_container_width=True,
        height=400
    )

    csv = display_data.to_csv(index=False).encode('utf-8')
    filename = 'filtered_intrusion_data.csv' if dataset_type == "intrusion" else 'filtered_phishing_data.csv'
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name=filename,
        mime='text/csv'
    )

    st.markdown("### 📊 Summary Statistics")

    if dataset_type == "intrusion":
        # Intrusion dataset statistics
        st.markdown("#### By Protocol")
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

    else:
        # Phishing dataset statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total URLs", len(display_data))
            st.metric("Avg URL Length", f"{display_data['UrlLength'].mean():.1f}")

        with col2:
            phishing_count = display_data['CLASS_LABEL'].sum()
            st.metric("Phishing URLs", phishing_count)
            st.metric("Phishing Rate", f"{(phishing_count/len(display_data)*100):.1f}%")

        with col3:
            st.metric("Legitimate URLs", len(display_data) - phishing_count)
            st.metric("HTTPS Usage", f"{((display_data['NoHttps'] == 0).sum()/len(display_data)*100):.1f}%")

        st.markdown("### 🎯 Classification Breakdown")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**By HTTPS Usage**")
            https_stats = display_data.groupby('NoHttps')['CLASS_LABEL'].agg(['sum', 'count', 'mean']).round(3)
            https_stats.columns = ['Phishing', 'Total', 'Phishing Rate']
            https_stats.index = ['Uses HTTPS', 'No HTTPS']
            st.dataframe(https_stats)

        with col2:
            st.markdown("**By IP Address in URL**")
            ip_stats = display_data.groupby('IpAddress')['CLASS_LABEL'].agg(['sum', 'count', 'mean']).round(3)
            ip_stats.columns = ['Phishing', 'Total', 'Phishing Rate']
            ip_stats.index = ['No IP', 'Contains IP']
            st.dataframe(ip_stats)
