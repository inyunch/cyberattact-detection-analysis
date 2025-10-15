import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import folium
from streamlit_folium import folium_static

# Power BI-style color palette
POWERBI_COLORS = {
    'primary': '#0078D4',      # Microsoft Blue
    'secondary': '#005a9e',    # Dark Blue
    'success': '#107C10',      # Green
    'warning': '#FFB900',      # Amber
    'danger': '#D13438',       # Red
    'info': '#00B7C3',         # Teal
    'purple': '#8764B8',       # Purple
    'orange': '#FF8C00',       # Orange
    'gradient': ['#0078D4', '#005a9e', '#003d66']
}

def create_kpi_card(label, value, delta=None, icon="📊", color="#0078D4"):
    """Create a professional KPI card with Power BI styling"""
    delta_html = ""
    if delta:
        delta_color = POWERBI_COLORS['success'] if isinstance(delta, str) and '+' in str(delta) else POWERBI_COLORS['danger']
        delta_html = f'<div style="color: {delta_color}; font-size: 14px; margin-top: 5px;">{delta}</div>'

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {color};
        height: 120px;
    ">
        <div style="color: #666; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
            {icon} {label}
        </div>
        <div style="color: #2c3e50; font-size: 32px; font-weight: 700;">
            {value}
        </div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def ensure_year_numeric(df):
    """Ensure Year column is numeric and properly formatted"""
    if 'Year' in df.columns:
        df = df.copy()
        df['Year'] = pd.to_numeric(df['Year'].astype(str).str.replace(',', ''), errors='coerce').astype(int)
    return df

def show(global_threats, intrusion_data):
    """Display IDA and EDA analysis with a tabbed interface."""

    st.title("📊 Data Science Investigation")
    st.markdown("A deep dive into the datasets, from initial understanding to exploratory analysis and key findings.")

    st.markdown("---")

    if global_threats is None or intrusion_data is None:
        st.error("Unable to load data for analysis.")
        return

    # Main tab navigation
    tab1, tab2, tab3 = st.tabs([
        "📖 Data Understanding (IDA)",
        "🔬 Exploratory Analysis (EDA)",
        "💡 Key Findings & Insights"
    ])

    # ==================== DATA UNDERSTANDING (IDA) TAB ====================
    with tab1:
        st.header("Initial Data Analysis (IDA)")

        # Nested tabs for dataset selection
        ida_tab1, ida_tab2, ida_tab3 = st.tabs([
            "🌍 Global Threats Dataset",
            "🔐 Intrusion Detection Dataset",
            "📋 Raw Data Explorer"
        ])

        with ida_tab1:
            show_ida_global(global_threats)
        with ida_tab2:
            show_ida_intrusion(intrusion_data)
        with ida_tab3:
            show_data_explorer(global_threats, intrusion_data)

    # ==================== EXPLORATORY ANALYSIS (EDA) TAB ====================
    with tab2:
        st.header("Exploratory Data Analysis (EDA)")
        st.markdown("""
        > *"Data exploration is detective work. We form hypotheses, test them with visualizations and statistics,
        > and build evidence for our conclusions."*
        """)

        with st.expander("🎯 How to Navigate This Analysis", expanded=True):
            st.markdown("""
            This EDA follows a **narrative arc**, with each section building on the previous to tell a comprehensive story.
            - **Temporal Analysis:** Are cyber threats growing over time?
            - **Geographic Analysis:** Where are threats and financial losses concentrated?
            - **Correlation Analysis:** What factors move together?
            - **Behavior Analysis:** How can we distinguish an attack from normal traffic?
            - **Advanced Analytics:** What hidden patterns exist in the data?
            """)
        st.markdown("---")

        # Display all EDA sections sequentially
        show_temporal_analysis(global_threats)
        st.markdown("---")
        show_geographic_analysis(global_threats)
        st.markdown("---")
        show_correlation_analysis(global_threats, intrusion_data)
        st.markdown("---")
        show_behavior_analysis(intrusion_data)
        st.markdown("---")
        show_advanced_analytics(global_threats, intrusion_data)

    # ==================== KEY FINDINGS TAB ====================
    with tab3:
        show_key_findings(global_threats, intrusion_data)


# ==================== IDA FUNCTIONS ====================

def show_ida_global(df):
    """IDA for Global Threats Dataset with narrative storytelling"""

    st.markdown("### 📋 Understanding the Global Threats Dataset")

    st.markdown("""
    **Dataset Context:** This dataset captures macro-level cybersecurity incidents reported globally from 2015-2024.
    Each record represents a significant security breach with documented financial impact and organizational response.

    **Critical Questions:**
    - Is the data quality sufficient for analysis?
    - What are the potential biases (reporting bias, geographic bias)?
    - What patterns can we trust vs. what might be artifacts?
    """)

    # Remove duplicates for analysis
    df = df.drop_duplicates()

    st.markdown("---")

    # KPI metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Records", f"{len(df):,}")
    with col2:
        st.metric("📝 Variables", df.shape[1])
    with col3:
        st.metric("📅 Years", f"{df['Year'].min()}-{df['Year'].max()}")
    with col4:
        st.metric("🌍 Countries", df['Country'].nunique())
    with col5:
        st.metric("🎯 Attack Types", df['Attack Type'].nunique())

    st.markdown("---")

    # Two-column layout for overview
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### 📊 Data Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True, height=300)

    with col2:
        st.markdown("#### 🏷️ Data Types")
        dtypes_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Type': df.dtypes.values.astype(str)
        })
        st.dataframe(dtypes_df, use_container_width=True, height=300)

    st.markdown("---")

    # Data Quality Section
    st.markdown("### 🔍 Data Quality Assessment")

    col1, col2, col3 = st.columns(3)

    # Missing Values
    with col1:
        st.markdown("#### 📉 Missing Values")
        missing_count = df.isnull().sum().sum()
        missing_pct = (missing_count / (len(df) * len(df.columns)) * 100)

        if missing_count == 0:
            st.success(f"✅ No missing values")
        else:
            st.warning(f"⚠️ {missing_count} missing values ({missing_pct:.2f}%)")

        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing': df.isnull().sum(),
            'Percent': (df.isnull().sum() / len(df) * 100).round(2)
        }).sort_values('Missing', ascending=False)

        st.dataframe(missing_data[missing_data['Missing'] > 0] if missing_count > 0 else
                    pd.DataFrame({'Info': ['No missing values']}),
                    use_container_width=True, height=200)

    # Duplicates
    with col2:
        st.markdown("#### 🔄 Duplicate Rows")
        duplicates = df.duplicated().sum()
        dup_pct = (duplicates / len(df) * 100)

        if duplicates == 0:
            st.success(f"✅ No duplicates")
        else:
            st.warning(f"⚠️ {duplicates} duplicates ({dup_pct:.2f}%)")

        st.metric("Total Duplicates", duplicates)
        st.metric("Percentage", f"{dup_pct:.2f}%")

    # Data Integrity
    with col3:
        st.markdown("#### ✔️ Data Integrity")

        # Check for negative values
        negative_loss = (df['Financial Loss (in Million $)'] < 0).sum()
        negative_users = (df['Number of Affected Users'] < 0).sum()

        if negative_loss == 0 and negative_users == 0:
            st.success("✅ No negative values")
        else:
            st.error("❌ Negative values found")

        st.metric("Negative Losses", negative_loss)
        st.metric("Negative Users", negative_users)

    st.markdown("---")

    # Statistical Summary
    st.markdown("### 📊 Statistical Summary")

    tab1, tab2 = st.tabs(["📈 Numeric Variables", "🏷️ Categorical Variables"])

    with tab1:
        st.markdown("#### Descriptive Statistics for Numeric Columns")
        numeric_stats = df[['Financial Loss (in Million $)', 'Number of Affected Users',
                           'Incident Resolution Time (in Hours)']].describe().round(2)

        # Add additional statistics
        numeric_stats.loc['skewness'] = df[['Financial Loss (in Million $)', 'Number of Affected Users',
                                            'Incident Resolution Time (in Hours)']].skew().round(2)
        numeric_stats.loc['kurtosis'] = df[['Financial Loss (in Million $)', 'Number of Affected Users',
                                            'Incident Resolution Time (in Hours)']].kurtosis().round(2)

        st.dataframe(numeric_stats, use_container_width=True)

        # Distribution visualizations
        st.markdown("#### 📊 Distribution Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            selected_num = st.selectbox("Select Numeric Variable",
                                       ['Financial Loss (in Million $)', 'Number of Affected Users',
                                        'Incident Resolution Time (in Hours)'],
                                       key='num_var_global')

            fig = px.histogram(df, x=selected_num, nbins=50,
                             title=f'Distribution of {selected_num}',
                             labels={selected_num: selected_num})
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.box(df, y=selected_num,
                        title=f'Box Plot of {selected_num}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("#### Categorical Variable Distributions")

        categorical_cols = ['Attack Type', 'Target Industry', 'Country', 'Attack Source',
                           'Security Vulnerability Type']

        col1, col2 = st.columns([2, 1])

        with col1:
            selected_cat = st.selectbox("Select Categorical Variable", categorical_cols,
                                       key='cat_var_global')

            value_counts = df[selected_cat].value_counts().head(15)

            fig = px.bar(x=value_counts.values, y=value_counts.index,
                        orientation='h',
                        title=f'Top 15 {selected_cat}',
                        labels={'x': 'Count', 'y': selected_cat},
                        color=value_counts.values,
                        color_continuous_scale='Blues')
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"**Statistics:**")
            st.metric("Total Unique", df[selected_cat].nunique())
            st.metric("Most Common", df[selected_cat].mode()[0] if len(df[selected_cat].mode()) > 0 else "N/A")
            st.metric("Frequency", df[selected_cat].value_counts().iloc[0] if len(df[selected_cat].value_counts()) > 0 else 0)

            st.markdown("**Top 10 Values:**")
            top_10 = df[selected_cat].value_counts().head(10).reset_index()
            top_10.columns = [selected_cat, 'Count']
            st.dataframe(top_10, use_container_width=True, height=300)


def show_ida_intrusion(df):
    """IDA for Intrusion Detection Dataset with improved layout"""

    st.markdown("### 📋 Dataset Overview")

    attack_rate = df['attack_detected'].mean() * 100

    # KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Records", f"{len(df):,}")
    with col2:
        st.metric("📝 Variables", df.shape[1])
    with col3:
        st.metric("🎯 Attack Rate", f"{attack_rate:.2f}%")
    with col4:
        st.metric("📡 Protocols", df['protocol_type'].nunique())
    with col5:
        st.metric("🔐 Encryption Types", df['encryption_used'].nunique())

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### 📊 Data Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True, height=300)

    with col2:
        st.markdown("#### ⚖️ Class Balance")

        attack_counts = df['attack_detected'].value_counts()
        attack_pct = df['attack_detected'].value_counts(normalize=True) * 100

        balance_df = pd.DataFrame({
            'Class': ['Normal (0)', 'Attack (1)'],
            'Count': [attack_counts[0], attack_counts[1]],
            'Percentage': [attack_pct[0], attack_pct[1]]
        }).round(2)

        st.dataframe(balance_df, use_container_width=True, height=150)

        st.metric("Imbalance Ratio", f"{attack_counts[0]/attack_counts[1]:.2f}:1")

    st.markdown("---")

    # Class Distribution Visualization
    st.markdown("### 📊 Class Distribution Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(values=attack_counts.values,
                    names=['Normal', 'Attack'],
                    title='Attack vs Normal Distribution',
                    color_discrete_sequence=['#4444ff', '#ff4444'],
                    hole=0.4)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(x=['Normal', 'Attack'], y=attack_counts.values,
                    title='Attack vs Normal Count',
                    labels={'x': 'Classification', 'y': 'Count'},
                    color=['Normal', 'Attack'],
                    color_discrete_map={'Normal': '#4444ff', 'Attack': '#ff4444'})
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Data Quality
    st.markdown("### 🔍 Data Quality Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📉 Missing Values")
        missing_count = df.isnull().sum().sum()

        if missing_count == 0:
            st.success("✅ No missing values in this dataset!")
        else:
            st.warning(f"⚠️ {missing_count} missing values found")
            missing_data = pd.DataFrame({
                'Column': df.columns,
                'Missing': df.isnull().sum(),
                'Percent': (df.isnull().sum() / len(df) * 100).round(2)
            }).sort_values('Missing', ascending=False)
            st.dataframe(missing_data[missing_data['Missing'] > 0], use_container_width=True)

    with col2:
        st.markdown("#### ✔️ Data Integrity")

        numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins']

        integrity_issues = 0
        for col in numeric_features:
            if (df[col] < 0).sum() > 0:
                integrity_issues += 1

        if integrity_issues == 0:
            st.success("✅ No negative values")
        else:
            st.error(f"❌ {integrity_issues} columns with negative values")

        # IP reputation range check
        ip_out_of_range = ((df['ip_reputation_score'] < 0) | (df['ip_reputation_score'] > 1)).sum()
        if ip_out_of_range == 0:
            st.success("✅ IP reputation in valid range (0-1)")
        else:
            st.warning(f"⚠️ {ip_out_of_range} IP scores out of range")

    st.markdown("---")

    # Statistical Summary
    st.markdown("### 📊 Statistical Summary")

    tab1, tab2, tab3 = st.tabs(["📈 Numeric Features", "🏷️ Categorical Features", "⚔️ Attack vs Normal"])

    with tab1:
        st.markdown("#### Descriptive Statistics for Numeric Features")

        numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins']

        stats_df = df[numeric_features].describe().round(2)
        stats_df.loc['skewness'] = df[numeric_features].skew().round(2)
        stats_df.loc['kurtosis'] = df[numeric_features].kurtosis().round(2)

        st.dataframe(stats_df, use_container_width=True)

        # Distribution visualization
        st.markdown("#### 📊 Feature Distribution")

        col1, col2 = st.columns(2)

        with col1:
            selected_feature = st.selectbox("Select Feature", numeric_features, key='num_feat_intrusion')

            fig = px.histogram(df, x=selected_feature, nbins=50,
                             title=f'Distribution of {selected_feature.replace("_", " ").title()}',
                             color_discrete_sequence=['steelblue'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.box(df, y=selected_feature,
                        title=f'Box Plot of {selected_feature.replace("_", " ").title()}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("#### Categorical Feature Distributions")

        cat_features = ['protocol_type', 'encryption_used', 'browser_type']

        col1, col2 = st.columns([2, 1])

        with col1:
            selected_cat = st.selectbox("Select Categorical Feature", cat_features, key='cat_feat_intrusion')

            value_counts = df[selected_cat].value_counts().head(15)

            fig = px.bar(x=value_counts.values, y=value_counts.index,
                        orientation='h',
                        title=f'{selected_cat.replace("_", " ").title()} Distribution',
                        labels={'x': 'Count', 'y': selected_cat.replace('_', ' ').title()},
                        color=value_counts.values,
                        color_continuous_scale='Viridis')
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Statistics:**")
            st.metric("Unique Values", df[selected_cat].nunique())
            st.metric("Most Common", df[selected_cat].mode()[0] if len(df[selected_cat].mode()) > 0 else "N/A")

            st.markdown("**Value Counts:**")
            vc_df = value_counts.reset_index()
            vc_df.columns = ['Value', 'Count']
            st.dataframe(vc_df, use_container_width=True, height=250)

    with tab3:
        st.markdown("#### Attack vs Normal Comparison")

        attack_data = df[df['attack_detected'] == 1]
        normal_data = df[df['attack_detected'] == 0]

        numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins']

        comparison_df = pd.DataFrame({
            'Feature': [f.replace('_', ' ').title() for f in numeric_features],
            'Normal Mean': [normal_data[f].mean() for f in numeric_features],
            'Attack Mean': [attack_data[f].mean() for f in numeric_features],
        }).round(2)

        comparison_df['Difference'] = (comparison_df['Attack Mean'] - comparison_df['Normal Mean']).round(2)
        comparison_df['% Difference'] = ((comparison_df['Attack Mean'] - comparison_df['Normal Mean']) /
                                        comparison_df['Normal Mean'] * 100).round(1)

        st.dataframe(comparison_df, use_container_width=True)

        # Visualization
        selected_comp = st.selectbox("Select Feature for Comparison", numeric_features, key='comp_feat')

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=normal_data[selected_comp], name='Normal',
                                  opacity=0.6, marker_color='blue', nbinsx=50))
        fig.add_trace(go.Histogram(x=attack_data[selected_comp], name='Attack',
                                  opacity=0.6, marker_color='red', nbinsx=50))
        fig.update_layout(
            title=f'{selected_comp.replace("_", " ").title()} Distribution: Attack vs Normal',
            xaxis_title=selected_comp.replace('_', ' ').title(),
            yaxis_title='Frequency',
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


# ==================== EDA FUNCTIONS ====================

def show_temporal_analysis(df):
    """Temporal Analysis for Global Threats with Narrative Storytelling"""

    st.markdown("### 📅 Temporal Trend Analysis: The Evolution of Cyber Threats Over Time")

    st.markdown("""
    > **The Research Question:** *Are cyberattacks becoming more frequent and costly over time,
    > or is this merely increased reporting? Let's follow the data trail...*
    """)

    with st.expander("📖 What This Analysis Reveals", expanded=True):
        st.markdown("""
        **Why temporal analysis matters:**
        - Identifies **emerging trends** and cyclical patterns
        - Reveals whether threats are **accelerating or stabilizing**
        - Helps security teams **anticipate future attack volumes**
        - Informs **budget planning** for cybersecurity investments

        **What to look for:**
        - 📈 **Upward trends** = growing threat landscape
        - 📉 **Spikes** = major incident periods or reporting changes
        - 🔄 **Seasonality** = predictable attack patterns
        - 💰 **Cost trends** = economic impact evolution
        """)

    st.markdown("---")

    # Remove duplicates and ensure Year is numeric
    df = ensure_year_numeric(df.drop_duplicates())

    # Attack frequency over time
    attacks_by_year = df.groupby('Year').size().reset_index(name='Count')

    # Convert to lists for better Plotly compatibility
    years = [int(y) for y in attacks_by_year['Year']]
    counts = [int(c) for c in attacks_by_year['Count']]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Attack Frequency Trend")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=counts,
            mode='lines+markers',
            name='Attacks',
            line=dict(color=POWERBI_COLORS['primary'], width=4),
            marker=dict(size=10, color=POWERBI_COLORS['primary'],
                       line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor=f'rgba(0, 120, 212, 0.1)'
        ))

        # Add trend line
        z = np.polyfit(years, counts, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=years, y=p(years),
            mode='lines',
            name='Trend',
            line=dict(dash='dash', color=POWERBI_COLORS['danger'], width=3)
        ))

        fig.update_layout(
            title={
                'text': 'Cyberattack Frequency (2015-2024)',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Segoe UI'}
            },
            xaxis_title='Year',
            yaxis_title='Attack Count',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1, showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=12, color='#2c3e50'),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255,255,255,0.8)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Year-over-Year Growth Rate")

        attacks_by_year['YoY_Growth'] = attacks_by_year['Count'].pct_change() * 100

        # Prepare data (skip first year which has NaN growth)
        growth_years = [int(y) for y in attacks_by_year['Year'][1:]]
        growth_values = [float(g) for g in attacks_by_year['YoY_Growth'][1:]]

        # Color bars based on positive/negative growth
        colors = [POWERBI_COLORS['success'] if v >= 0 else POWERBI_COLORS['danger'] for v in growth_values]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=growth_years,
            y=growth_values,
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            text=[f"{v:+.1f}%" for v in growth_values],
            textposition='outside',
            textfont=dict(size=11, color='#2c3e50', family='Segoe UI')
        ))

        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="#666", line_width=1)

        fig.update_layout(
            title={
                'text': 'YoY Growth Rate (%)',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Segoe UI'}
            },
            xaxis_title='Year',
            yaxis_title='Growth Rate (%)',
            height=400,
            xaxis=dict(range=[2015.5, 2024.5], dtick=1, showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0', zeroline=True),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI', size=12, color='#2c3e50'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Statistics
    total_growth = ((attacks_by_year['Count'].iloc[-1] / attacks_by_year['Count'].iloc[0]) - 1) * 100
    slope, intercept, r_value, p_value, std_err = stats.linregress(attacks_by_year['Year'], attacks_by_year['Count'])

    st.markdown("#### 📊 Statistical Insights")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Growth", f"{total_growth:.1f}%", delta="2015-2024")
    with col2:
        st.metric("Trend Slope", f"{slope:.2f}", delta="attacks/year")
    with col3:
        st.metric("R-squared", f"{r_value**2:.4f}")
    with col4:
        avg_growth = attacks_by_year['YoY_Growth'].mean()
        st.metric("Avg YoY Growth", f"{avg_growth:.1f}%")

    # Add interpretation
    st.markdown("#### 💡 Key Findings")

    if total_growth > 10:
        interpretation = f"📈 **Significant Growth:** The data shows a {total_growth:.1f}% increase in cyberattacks over the decade. "
        if slope > 0:
            interpretation += f"The positive trend (slope: {slope:.2f}) indicates a **consistent upward trajectory**. "
    elif total_growth < -10:
        interpretation = f"📉 **Declining Trend:** Attacks decreased by {abs(total_growth):.1f}% over the period. "
    else:
        interpretation = f"➡️ **Stable Pattern:** Attack frequency remained relatively stable ({total_growth:.1f}% change). "

    if r_value**2 > 0.7:
        interpretation += f"The high R² value ({r_value**2:.3f}) suggests this trend is **statistically robust**."
    elif r_value**2 > 0.4:
        interpretation += f"The moderate R² value ({r_value**2:.3f}) indicates a **discernible trend** with some variation."
    else:
        interpretation += f"The low R² value ({r_value**2:.3f}) suggests **high volatility** or non-linear patterns."

    st.info(interpretation)

    # Actionable insight
    if slope > 0:
        st.warning(f"⚠️ **Security Implication:** At the current rate ({slope:.2f} additional attacks/year), "
                   f"organizations should expect attack volumes to continue rising. This demands **increased vigilance and investment**.")
    else:
        st.success("✅ **Positive Signal:** The stable or declining trend may indicate improving security postures or changes in attack targeting.")

    st.markdown("---")

    # Financial losses over time
    st.markdown("#### 💰 Financial Impact Over Time")

    losses_by_year = df.groupby('Year').agg({
        'Financial Loss (in Million $)': ['sum', 'mean', 'median']
    }).round(2)
    losses_by_year.columns = ['Total_Loss', 'Avg_Loss', 'Median_Loss']
    losses_by_year = losses_by_year.reset_index()

    # Convert to lists
    loss_years = [int(y) for y in losses_by_year['Year']]
    total_losses = [float(l) for l in losses_by_year['Total_Loss']]
    avg_losses = [float(l) for l in losses_by_year['Avg_Loss']]
    median_losses = [float(l) for l in losses_by_year['Median_Loss']]

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=loss_years,
            y=total_losses,
            marker=dict(
                color=total_losses,
                colorscale='Reds',
                colorbar=dict(title="Loss ($M)")
            )
        ))
        fig.update_layout(
            title='Total Financial Losses by Year ($M)',
            xaxis_title='Year',
            yaxis_title='Total Loss ($M)',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=loss_years, y=avg_losses,
                                mode='lines+markers', name='Mean',
                                line=dict(color='blue', width=3),
                                marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=loss_years, y=median_losses,
                                mode='lines+markers', name='Median',
                                line=dict(color='green', width=3),
                                marker=dict(size=8)))
        fig.update_layout(
            title='Average vs Median Loss Per Incident',
            xaxis_title='Year',
            yaxis_title='Loss ($M)',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Attack type evolution
    st.markdown("#### 🎯 Attack Type Evolution")

    attack_type_evolution = pd.crosstab(df['Year'], df['Attack Type']).reset_index()

    # Convert Year to list
    evo_years = [int(y) for y in attack_type_evolution['Year']]

    fig = go.Figure()
    for col in attack_type_evolution.columns[1:]:
        fig.add_trace(go.Scatter(
            x=evo_years,
            y=attack_type_evolution[col].tolist(),
            mode='lines',
            name=col,
            stackgroup='one',
            groupnorm=''
        ))

    fig.update_layout(
        title='Attack Type Distribution Over Time',
        xaxis_title='Year',
        yaxis_title='Count',
        height=500,
        hovermode='x unified',
        xaxis=dict(range=[2014.5, 2024.5], dtick=1)
    )
    st.plotly_chart(fig, use_container_width=True)


def show_geographic_analysis(df):
    """Geographic Analysis for Global Threats with Storytelling"""

    st.markdown("### 🗺️ Geographic Distribution Analysis: Global Threat Landscape")

    st.markdown("""
    > **The Research Question:** *Is cybercrime evenly distributed globally, or are certain nations bearing
    > a disproportionate burden? What makes a country an attractive target?*
    """)

    with st.expander("📖 What This Geographic Analysis Reveals", expanded=True):
        st.markdown("""
        **Why geography matters in cybersecurity:**
        - **Economic targets:** Wealthier nations often face higher attack rates
        - **Digital infrastructure:** Countries with advanced tech are both safer AND more targeted
        - **Regulatory environments:** Data protection laws influence breach reporting
        - **Attack attribution:** Geographic patterns may reveal state-sponsored activity

        **Key questions we're answering:**
        - 🌍 Which countries are **most targeted**?
        - 💰 Where are the **costliest breaches** occurring?
        - 🎯 Do attack **types vary by region**?
        - 📊 Is there a correlation between attack frequency and financial impact?
        """)

    st.markdown("---")

    # Remove duplicates
    df = df.drop_duplicates()

    # ========== FILTERS SECTION ==========
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%);
        padding: 20px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,120,212,0.3);
        margin-bottom: 25px;
    ">
        <h3 style="color: white; margin: 0 0 8px 0; font-size: 20px; font-weight: 700;">
            🔍 FILTER DATA
        </h3>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 14px; font-weight: 500;">
            Refine your analysis by selecting specific parameters below
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter controls with white background panel
    st.markdown("""
    <div style="
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    ">
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Year filter
        st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">📅 Year Range</p>', unsafe_allow_html=True)
        available_years = sorted(df['Year'].dropna().unique().tolist())
        selected_years = st.multiselect(
            "Year Range",
            options=available_years,
            default=available_years,
            key='geo_year_filter',
            help="Select one or more years to analyze",
            label_visibility="collapsed"
        )

    with col2:
        # Attack Type filter
        st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🎯 Attack Type</p>', unsafe_allow_html=True)
        attack_types = ['All'] + sorted(df['Attack Type'].dropna().unique().tolist())
        selected_attack_type = st.selectbox(
            "Attack Type",
            options=attack_types,
            key='geo_attack_filter',
            help="Filter by specific attack category",
            label_visibility="collapsed"
        )

    with col3:
        # Industry filter
        st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🏢 Target Industry</p>', unsafe_allow_html=True)
        industries = ['All'] + sorted(df['Target Industry'].dropna().unique().tolist())
        selected_industry = st.selectbox(
            "Target Industry",
            options=industries,
            key='geo_industry_filter',
            help="Filter by industry sector",
            label_visibility="collapsed"
        )

    # Show active filters summary
    active_filters = []
    if selected_years and len(selected_years) < len(available_years):
        active_filters.append(f"**Years:** {len(selected_years)} selected")
    if selected_attack_type != 'All':
        active_filters.append(f"**Attack Type:** {selected_attack_type}")
    if selected_industry != 'All':
        active_filters.append(f"**Industry:** {selected_industry}")

    if active_filters:
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd;
            padding: 12px 20px;
            border-radius: 6px;
            border-left: 4px solid #0078D4;
            margin: 15px 0;
        ">
            <strong style="color: #2c3e50;">🎯 Active Filters:</strong>
            <span style="color: #555;">{' | '.join(active_filters)}</span>
        </div>
        """, unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
    if selected_attack_type != 'All':
        filtered_df = filtered_df[filtered_df['Attack Type'] == selected_attack_type]
    if selected_industry != 'All':
        filtered_df = filtered_df[filtered_df['Target Industry'] == selected_industry]

    # Country statistics
    country_stats = filtered_df.groupby('Country').agg({
        'Financial Loss (in Million $)': ['sum', 'mean', 'count'],
        'Number of Affected Users': 'sum'
    }).round(2)
    country_stats.columns = ['Total_Loss', 'Avg_Loss', 'Attack_Count', 'Total_Users']
    country_stats = country_stats.sort_values('Total_Loss', ascending=False).reset_index()

    # Add loss per attack metric
    country_stats['Loss_Per_Attack'] = (country_stats['Total_Loss'] / country_stats['Attack_Count']).round(2)

    st.markdown("---")

    # ========== KEY METRICS DASHBOARD ==========
    st.markdown("#### 📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌍 Countries Affected",
            f"{len(country_stats)}"
        )

    with col2:
        total_loss = country_stats['Total_Loss'].sum()
        st.metric(
            "💰 Total Loss",
            f"${total_loss:,.0f}M"
        )

    with col3:
        top_country = country_stats.iloc[0] if len(country_stats) > 0 else None
        if top_country is not None:
            st.metric(
            "🔝 Top Country",
            top_country['Country'],
            delta=f"${top_country['Total_Loss']:,.0f}M"
        )

    with col4:
        total_attacks = country_stats['Attack_Count'].sum()
        st.metric(
            "🎯 Total Attacks",
            f"{int(total_attacks):,}"
        )

    st.markdown("---")

    # ========== TOP COUNTRIES VISUALIZATION ==========
    st.markdown("#### 🏆 Top Countries Analysis")

    # Top N selector
    top_n = st.slider("Select number of top countries to display", min_value=5, max_value=15, value=10, step=1, key='top_n_slider')

    top_countries = country_stats.head(top_n)

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Financial Impact", "🎯 Attack Frequency", "⚖️ Loss Efficiency"])

    with tab1:
        col1, col2 = st.columns([3, 2])

        with col1:
            # Beautiful bar chart with gradient
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=top_countries['Country'],
                x=top_countries['Total_Loss'],
                orientation='h',
                marker=dict(
                    color=top_countries['Total_Loss'],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Loss ($M)", x=1.15)
                ),
                text=top_countries['Total_Loss'].apply(lambda x: f'${x:,.1f}M'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Total Loss: $%{x:,.1f}M<extra></extra>'
            ))

            fig.update_layout(
                title=f'Top {top_n} Countries by Total Financial Loss',
                xaxis_title='Total Loss ($M)',
                yaxis_title='Country',
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Pie chart showing concentration
            st.markdown("##### 🥧 Loss Concentration")

            top_5_loss = top_countries.head(5)['Total_Loss'].sum()
            other_loss = country_stats['Total_Loss'].sum() - top_5_loss

            fig = go.Figure(data=[go.Pie(
                labels=['Top 5 Countries', 'Other Countries'],
                values=[top_5_loss, other_loss],
                hole=.4,
                marker=dict(colors=['#ff4444', '#4444ff']),
                textinfo='label+percent',
                textposition='inside'
            )])

            fig.update_layout(
                title='Geographic Loss Concentration',
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # Statistics
            concentration_pct = (top_5_loss / country_stats['Total_Loss'].sum()) * 100
            st.metric("Top 5 Concentration", f"{concentration_pct:.1f}%")

    with tab2:
        col1, col2 = st.columns([3, 2])

        with col1:
            # Attack frequency bar chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=top_countries['Country'],
                x=top_countries['Attack_Count'],
                orientation='h',
                marker=dict(
                    color=top_countries['Attack_Count'],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="Attacks", x=1.15)
                ),
                text=top_countries['Attack_Count'].apply(lambda x: f'{int(x):,}'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Attacks: %{x:,}<extra></extra>'
            ))

            fig.update_layout(
                title=f'Top {top_n} Countries by Attack Frequency',
                xaxis_title='Number of Attacks',
                yaxis_title='Country',
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Sunburst chart
            st.markdown("##### ☀️ Attack Distribution")

            sunburst_data = top_countries.head(8).copy()
            sunburst_data['label'] = sunburst_data['Country'] + '<br>' + sunburst_data['Attack_Count'].apply(lambda x: f'{int(x):,}')

            fig = go.Figure(go.Sunburst(
                labels=['All Countries'] + sunburst_data['Country'].tolist(),
                parents=[''] + ['All Countries'] * len(sunburst_data),
                values=[sunburst_data['Attack_Count'].sum()] + sunburst_data['Attack_Count'].tolist(),
                marker=dict(colorscale='Blues')
            ))

            fig.update_layout(
                title='Top 8 Attack Distribution',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Loss per attack analysis
        st.markdown("##### 💡 Loss Efficiency Analysis")
        st.caption("*Higher loss per attack indicates more damaging attacks or higher-value targets*")

        fig = go.Figure()

        # Scatter plot
        fig.add_trace(go.Scatter(
            x=top_countries['Attack_Count'],
            y=top_countries['Total_Loss'],
            mode='markers+text',
            marker=dict(
                size=top_countries['Avg_Loss'] * 2,
                color=top_countries['Loss_Per_Attack'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Loss/Attack ($M)", x=1.15),
                line=dict(width=2, color='white')
            ),
            text=top_countries['Country'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                         'Attacks: %{x:,}<br>' +
                         'Total Loss: $%{y:,.1f}M<br>' +
                         '<extra></extra>'
        ))

        fig.update_layout(
            title='Attack Frequency vs Total Loss (bubble size = Avg Loss)',
            xaxis_title='Number of Attacks',
            yaxis_title='Total Loss ($M)',
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(240,240,240,0.5)'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ========== GEOGRAPHIC COMPARISON VISUALIZATIONS ==========
    st.markdown("#### 🌍 Global Geographic Comparison")

    # Create 3 powerful alternative visualizations
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📊 Ranking & Distribution", "🎯 Attack Patterns", "💰 Financial Analysis"])

    with viz_tab1:
        st.markdown("##### Country Rankings and Size Comparison")

        col1, col2 = st.columns([3, 2])

        with col1:
            # Bubble chart showing size relationship
            fig = px.scatter(
                country_stats.head(15),
                x='Attack_Count',
                y='Total_Loss',
                size='Total_Users',
                color='Country',
                hover_name='Country',
                size_max=60,
                title='Attack Volume vs Financial Impact (bubble size = affected users)',
                labels={
                    'Attack_Count': 'Number of Attacks',
                    'Total_Loss': 'Total Loss ($M)',
                    'Total_Users': 'Affected Users'
                }
            )
            fig.update_layout(
                height=450,
                showlegend=False,
                plot_bgcolor='rgba(240,240,240,0.3)',
                xaxis=dict(gridcolor='white'),
                yaxis=dict(gridcolor='white')
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Funnel chart showing concentration
            funnel_data = country_stats.head(10).copy()
            funnel_data = funnel_data.sort_values('Total_Loss', ascending=True)

            fig = go.Figure(go.Funnel(
                y=funnel_data['Country'],
                x=funnel_data['Total_Loss'],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=funnel_data['Total_Loss'],
                    colorscale='Reds'
                )
            ))
            fig.update_layout(
                title='Top 10 Loss Funnel',
                height=450,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

    with viz_tab2:
        st.markdown("##### Attack Type Distribution by Country")

        # Get attack type breakdown by country
        attack_breakdown = filtered_df.groupby(['Country', 'Attack Type']).size().reset_index(name='Count')
        top_5_countries = country_stats.head(5)['Country'].tolist()
        attack_breakdown_top = attack_breakdown[attack_breakdown['Country'].isin(top_5_countries)]

        col1, col2 = st.columns(2)

        with col1:
            # Stacked bar chart
            fig = px.bar(
                attack_breakdown_top,
                x='Country',
                y='Count',
                color='Attack Type',
                title='Attack Type Breakdown (Top 5 Countries)',
                labels={'Count': 'Number of Attacks'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                height=400,
                xaxis_tickangle=-45,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Sunburst chart
            fig = px.sunburst(
                attack_breakdown_top,
                path=['Country', 'Attack Type'],
                values='Count',
                title='Hierarchical Attack Distribution',
                color='Count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap
        pivot_data = attack_breakdown_top.pivot(index='Attack Type', columns='Country', values='Count').fillna(0)

        fig = px.imshow(
            pivot_data,
            labels=dict(x="Country", y="Attack Type", color="Attacks"),
            title='Attack Type × Country Heatmap (Top 5)',
            color_continuous_scale='YlOrRd',
            aspect='auto',
            text_auto=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with viz_tab3:
        st.markdown("##### Financial Loss Deep Dive")

        col1, col2 = st.columns(2)

        with col1:
            # Waterfall chart showing cumulative loss
            waterfall_data = country_stats.head(8).copy()

            fig = go.Figure(go.Waterfall(
                name="Loss Breakdown",
                orientation="v",
                measure=["relative"] * len(waterfall_data),
                x=waterfall_data['Country'],
                y=waterfall_data['Total_Loss'],
                text=[f"${x:,.0f}M" for x in waterfall_data['Total_Loss']],
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#ff6b6b"}},
            ))
            fig.update_layout(
                title="Cumulative Loss Waterfall (Top 8)",
                height=400,
                showlegend=False,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Box plot comparing loss distributions
            box_data = filtered_df[filtered_df['Country'].isin(country_stats.head(6)['Country'])]

            fig = px.box(
                box_data,
                x='Country',
                y='Financial Loss (in Million $)',
                title='Loss Distribution Comparison (Top 6)',
                labels={'Financial Loss (in Million $)': 'Loss ($M)'},
                color='Country',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)

        # Parallel coordinates for multi-dimensional comparison
        parallel_data = country_stats.head(10).copy()

        # Normalize for better visualization
        for col in ['Total_Loss', 'Attack_Count', 'Avg_Loss', 'Total_Users']:
            if parallel_data[col].max() > 0:
                parallel_data[f'{col}_norm'] = (parallel_data[col] / parallel_data[col].max() * 100).round(2)

        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=parallel_data['Total_Loss'],
                    colorscale='Reds',
                    showscale=True,
                    cmin=parallel_data['Total_Loss'].min(),
                    cmax=parallel_data['Total_Loss'].max()
                ),
                dimensions=[
                    dict(range=[0, 100], label='Total Loss', values=parallel_data['Total_Loss_norm']),
                    dict(range=[0, 100], label='Attack Count', values=parallel_data['Attack_Count_norm']),
                    dict(range=[0, 100], label='Avg Loss', values=parallel_data['Avg_Loss_norm']),
                    dict(range=[0, 100], label='Users Affected', values=parallel_data['Total_Users_norm'])
                ]
            )
        )
        fig.update_layout(
            title='Multi-Dimensional Country Comparison (Top 10, Normalized)',
            height=350,
            margin=dict(l=100, r=100, t=50, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption("💡 Use the parallel coordinates plot to filter and compare countries across multiple dimensions")

    # Overall summary with insights
    st.markdown("---")
    st.markdown("#### 📊 Global Summary & Key Insights")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Countries Analyzed", len(country_stats))
    with col2:
        st.metric("🔝 Highest Loss", f"{country_stats.iloc[0]['Country']}", f"${country_stats.iloc[0]['Total_Loss']:,.0f}M")
    with col3:
        most_attacked_country = country_stats.sort_values('Attack_Count', ascending=False).iloc[0]
        st.metric("🎯 Most Attacks", f"{most_attacked_country['Country']}",
                  f"{int(most_attacked_country['Attack_Count']):,}")
    with col4:
        st.metric("💰 Global Total", f"${country_stats['Total_Loss'].sum():,.0f}M")

    # Calculate concentration
    top_5_loss = country_stats.head(5)['Total_Loss'].sum()
    total_loss = country_stats['Total_Loss'].sum()
    concentration = (top_5_loss / total_loss) * 100

    # Generate insights
    st.markdown("#### 💡 Geographic Threat Intelligence")

    insights = []

    # Concentration insight
    if concentration > 70:
        insights.append(f"🎯 **High Concentration:** The top 5 countries account for **{concentration:.1f}%** of global losses, "
                       "indicating that cyber threats are **highly concentrated** in economically significant nations.")
    elif concentration > 50:
        insights.append(f"📊 **Moderate Concentration:** Top 5 countries represent {concentration:.1f}% of losses, "
                       "showing a **balanced but notable concentration**.")
    else:
        insights.append(f"🌍 **Distributed Threats:** With only {concentration:.1f}% of losses in top 5 countries, "
                       "cyber threats are **widely distributed globally**.")

    # Leader analysis
    leader = country_stats.iloc[0]
    leader_dominance = (leader['Total_Loss'] / total_loss) * 100
    insights.append(f"🥇 **Top Target:** {leader['Country']} leads with ${leader['Total_Loss']:,.0f}M in losses "
                   f"({leader_dominance:.1f}% of global total), experiencing {int(leader['Attack_Count'])} recorded attacks.")

    # Attack efficiency insight
    if len(country_stats) >= 2:
        high_efficiency = country_stats.nlargest(3, 'Loss_Per_Attack')
        insights.append(f"⚡ **Most Damaging Attacks:** {high_efficiency.iloc[0]['Country']} faces the highest loss-per-attack "
                       f"(${high_efficiency.iloc[0]['Loss_Per_Attack']:.2f}M), suggesting either **high-value targets** or "
                       f"**sophisticated attack methods**.")

    for insight in insights:
        st.info(insight)

    # Actionable recommendations
    st.warning("""
    **🛡️ Security Recommendations:**
    - **For high-loss countries:** Invest in advanced threat detection and incident response
    - **For high-attack countries:** Focus on preventive measures and security awareness training
    - **For all regions:** Share threat intelligence across borders to combat organized cybercrime
    """)

    st.markdown("---")

    # ========== DETAILED DATA TABLE ==========
    st.markdown("#### 📊 Detailed Country Statistics")

    # Format the dataframe for display
    display_df = country_stats.copy()
    display_df.columns = ['Country', 'Total Loss ($M)', 'Avg Loss ($M)', 'Attack Count', 'Total Users Affected', 'Loss per Attack ($M)']
    display_df = display_df.round(2)

    # Color code the table
    st.dataframe(
        display_df.head(25).style.background_gradient(subset=['Total Loss ($M)'], cmap='Reds')
                                  .background_gradient(subset=['Attack Count'], cmap='Blues')
                                  .background_gradient(subset=['Avg Loss ($M)'], cmap='Oranges')
                                  .format({
                                      'Total Loss ($M)': '${:,.1f}',
                                      'Avg Loss ($M)': '${:,.2f}',
                                      'Attack Count': '{:,.0f}',
                                      'Total Users Affected': '{:,.0f}',
                                      'Loss per Attack ($M)': '${:,.2f}'
                                  }),
        use_container_width=True,
        height=600
    )

    # Download button
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Geographic Analysis Data (CSV)",
        data=csv,
        file_name='geographic_threat_analysis.csv',
        mime='text/csv',
        help="Download the complete geographic analysis data"
    )


def show_correlation_analysis(global_df, intrusion_df):
    """Correlation Analysis with Storytelling"""

    st.markdown("### 🔗 Correlation Analysis: Uncovering Hidden Relationships")

    st.markdown("""
    > **The Research Question:** *Which cybersecurity metrics move together? Can understanding these relationships
    > help us predict attack severity or response effectiveness?*
    """)

    with st.expander("📖 Why Correlation Analysis Matters", expanded=True):
        st.markdown("""
        **Correlation reveals causal candidates:**
        - **Strong positive correlation (> 0.7):** Variables tend to increase together
        - **Strong negative correlation (< -0.7):** As one increases, the other decreases
        - **Weak correlation (near 0):** Variables are independent

        **Security applications:**
        - 💰 Does **financial loss correlate with affected users**?
        - ⏱️ Do **longer resolution times lead to higher costs**?
        - 📅 Is there a **temporal pattern** in attack severity?
        - 🎯 Can we **predict attack impact** from early indicators?

        **⚠️ Remember:** Correlation ≠ Causation! We identify relationships for further investigation.
        """)

    st.markdown("---")

    # Dataset selector
    dataset_choice = st.radio("Select Dataset",
                             ["🌍 Global Cybersecurity Threats", "🔐 Intrusion Detection"],
                             horizontal=True)

    if "Global" in dataset_choice:
        st.info("**Analyzing:** Global Cybersecurity Threats Dataset")

        # Remove duplicates
        global_df = global_df.drop_duplicates()

        numeric_cols = ['Year', 'Financial Loss (in Million $)',
                       'Number of Affected Users', 'Incident Resolution Time (in Hours)']

        # Check if we have enough data
        if len(global_df) > 1:
            # Ensure all columns are numeric and handle any non-numeric values
            for col in numeric_cols:
                global_df[col] = pd.to_numeric(global_df[col], errors='coerce')

            # Drop rows with NaN in numeric columns
            global_df_clean = global_df[numeric_cols].dropna()

            if len(global_df_clean) > 1:
                corr_matrix = global_df_clean.corr()

                col1, col2 = st.columns([3, 2])

                with col1:
                    st.markdown("#### 🔥 Correlation Heatmap")
                    fig = px.imshow(corr_matrix,
                                   labels=dict(color="Correlation"),
                                   title='Correlation Matrix - Global Threats',
                                   color_continuous_scale='RdBu_r',
                                   zmin=-1, zmax=1,
                                   text_auto='.3f',
                                   aspect='auto')
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("#### 📊 Correlation Values")
                    st.dataframe(corr_matrix.round(3), use_container_width=True, height=400)

                    st.markdown("#### 🔍 Key Correlations")
                    # Find strong correlations
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            if abs(corr_matrix.iloc[i, j]) > 0.3:
                                corr_pairs.append({
                                    'Variable 1': corr_matrix.columns[i],
                                    'Variable 2': corr_matrix.columns[j],
                                    'Correlation': corr_matrix.iloc[i, j]
                                })

                    if corr_pairs:
                        corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Correlation',
                                                                             key=abs, ascending=False)
                        st.dataframe(corr_pairs_df.round(3), use_container_width=True)
                    else:
                        st.info("No strong correlations (|r| > 0.3) found")
            else:
                st.warning("Not enough valid data to calculate correlations.")
        else:
            st.warning("Insufficient data for correlation analysis.")

    else:
        st.info("**Analyzing:** Intrusion Detection Dataset")

        numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins', 'unusual_time_access', 'attack_detected']

        # Ensure all columns are numeric
        for col in numeric_features:
            if col in intrusion_df.columns:
                intrusion_df[col] = pd.to_numeric(intrusion_df[col], errors='coerce')

        # Drop rows with NaN
        intrusion_df_clean = intrusion_df[numeric_features].dropna()

        if len(intrusion_df_clean) > 1:
            corr_matrix = intrusion_df_clean.corr()

            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("#### 🔥 Correlation Heatmap")
                fig = px.imshow(corr_matrix,
                               labels=dict(color="Correlation"),
                               title='Correlation Matrix - Intrusion Detection',
                               color_continuous_scale='RdBu_r',
                               zmin=-1, zmax=1,
                               text_auto='.3f',
                               aspect='auto')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### 🎯 Correlation with Attack Detection")

                target_corr = corr_matrix['attack_detected'].sort_values(ascending=False)[:-1]

                target_corr_df = pd.DataFrame({
                    'Feature': target_corr.index,
                    'Correlation': target_corr.values
                })

                st.dataframe(target_corr_df.round(3), use_container_width=True, height=300)

                st.markdown("#### 📊 Feature Importance")
                fig = px.bar(target_corr_df, y='Feature', x='Correlation',
                            orientation='h',
                            title='Feature Correlation with Attack',
                            color='Correlation',
                            color_continuous_scale='RdYlGn',
                            color_continuous_midpoint=0)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for correlation analysis.")


def show_behavior_analysis(df):
    """Attack Behavior Analysis for Intrusion Detection"""

    st.markdown("### ⚔️ Attack Behavior Analysis")
    st.info("**Dataset:** Intrusion Detection Dataset")

    attack_data = df[df['attack_detected'] == 1]
    normal_data = df[df['attack_detected'] == 0]

    # Comparison statistics
    st.markdown("#### 📊 Statistical Comparison: Attack vs Normal")

    numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                       'ip_reputation_score', 'failed_logins']

    comparison_df = pd.DataFrame({
        'Feature': [f.replace('_', ' ').title() for f in numeric_features],
        'Normal Mean': [normal_data[f].mean() for f in numeric_features],
        'Normal Median': [normal_data[f].median() for f in numeric_features],
        'Attack Mean': [attack_data[f].mean() for f in numeric_features],
        'Attack Median': [attack_data[f].median() for f in numeric_features],
    }).round(2)

    comparison_df['Mean Diff'] = (comparison_df['Attack Mean'] - comparison_df['Normal Mean']).round(2)
    comparison_df['% Diff'] = ((comparison_df['Attack Mean'] - comparison_df['Normal Mean']) /
                              comparison_df['Normal Mean'] * 100).round(1)

    st.dataframe(comparison_df, use_container_width=True)

    st.markdown("---")

    # Behavioral Pattern Visualizations
    st.markdown("#### 🔍 Behavioral Pattern Visualizations")

    viz_choice = st.selectbox("Select Visualization",
                             ["Login Behavior", "Session & IP Analysis",
                              "Protocol Distribution", "Feature Distribution Comparison"])

    if viz_choice == "Login Behavior":
        st.markdown("##### 🔐 Login Attempts vs Failed Logins")

        # Ensure columns are numeric
        df_plot = df.copy()
        df_plot['login_attempts'] = pd.to_numeric(df_plot['login_attempts'], errors='coerce')
        df_plot['failed_logins'] = pd.to_numeric(df_plot['failed_logins'], errors='coerce')
        df_plot['attack_detected'] = pd.to_numeric(df_plot['attack_detected'], errors='coerce')

        # Drop NaN values
        df_plot = df_plot[['login_attempts', 'failed_logins', 'attack_detected']].dropna()

        if len(df_plot) > 0:
            sample_df = df_plot.sample(min(5000, len(df_plot)))

            fig = px.scatter(sample_df,
                            x='login_attempts',
                            y='failed_logins',
                            color='attack_detected',
                            title='Login Behavior Pattern',
                            labels={'attack_detected': 'Classification',
                                   'login_attempts': 'Login Attempts',
                                   'failed_logins': 'Failed Logins'},
                            color_discrete_map={0: 'blue', 1: 'red'},
                            opacity=0.6)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No valid data available for this visualization.")

    elif viz_choice == "Session & IP Analysis":
        st.markdown("##### 🌐 Session Duration vs IP Reputation")

        sample_df = df.sample(min(5000, len(df)))

        fig = px.scatter(sample_df,
                        x='session_duration',
                        y='ip_reputation_score',
                        color='attack_detected',
                        title='Session Duration vs IP Reputation Score',
                        labels={'attack_detected': 'Classification',
                               'session_duration': 'Session Duration (s)',
                               'ip_reputation_score': 'IP Reputation (0-1)'},
                        color_discrete_map={0: 'blue', 1: 'red'},
                        opacity=0.6)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif viz_choice == "Protocol Distribution":
        st.markdown("##### 📡 Attack Rate by Protocol and Encryption")

        protocol_attack = df.groupby('protocol_type')['attack_detected'].agg(['sum', 'count', 'mean'])
        protocol_attack.columns = ['Attacks', 'Total', 'Attack_Rate']
        protocol_attack['Attack_Rate'] = (protocol_attack['Attack_Rate'] * 100).round(2)
        protocol_attack = protocol_attack.reset_index()

        encryption_attack = df.groupby('encryption_used')['attack_detected'].agg(['sum', 'count', 'mean'])
        encryption_attack.columns = ['Attacks', 'Total', 'Attack_Rate']
        encryption_attack['Attack_Rate'] = (encryption_attack['Attack_Rate'] * 100).round(2)
        encryption_attack = encryption_attack.reset_index()

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(protocol_attack, x='protocol_type', y='Attack_Rate',
                        title='Attack Rate by Protocol (%)',
                        labels={'Attack_Rate': 'Attack Rate (%)', 'protocol_type': 'Protocol'},
                        color='Attack_Rate',
                        color_continuous_scale='Reds')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(encryption_attack, x='encryption_used', y='Attack_Rate',
                        title='Attack Rate by Encryption (%)',
                        labels={'Attack_Rate': 'Attack Rate (%)', 'encryption_used': 'Encryption'},
                        color='Attack_Rate',
                        color_continuous_scale='Oranges')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    else:  # Feature Distribution Comparison
        st.markdown("##### 📊 Feature Distribution: Attack vs Normal")

        selected_feature = st.selectbox("Select Feature to Compare", numeric_features,
                                       key='feature_dist_comp')

        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=normal_data[selected_feature], name='Normal',
                                      opacity=0.6, marker_color='blue', nbinsx=50))
            fig.add_trace(go.Histogram(x=attack_data[selected_feature], name='Attack',
                                      opacity=0.6, marker_color='red', nbinsx=50))
            fig.update_layout(
                title=f'{selected_feature.replace("_", " ").title()} Distribution',
                xaxis_title=selected_feature.replace('_', ' ').title(),
                yaxis_title='Frequency',
                barmode='overlay',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.box(df, x='attack_detected', y=selected_feature,
                        title=f'{selected_feature.replace("_", " ").title()} Box Plot',
                        labels={'attack_detected': 'Classification'},
                        color='attack_detected',
                        color_discrete_map={0: 'blue', 1: 'red'})
            fig.update_xaxes(ticktext=['Normal', 'Attack'], tickvals=[0, 1])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def show_advanced_analytics(global_df, intrusion_df):
    """Advanced Analytics: PCA and Other Advanced Techniques"""

    st.markdown("### 🔬 Advanced Analytics")

    analysis_type = st.radio("Select Analysis",
                             ["🔬 PCA (Intrusion Detection)", "📊 Advanced Statistics (Both Datasets)"],
                             horizontal=True)

    if "PCA" in analysis_type:
        st.info("**Dataset:** Intrusion Detection | **Technique:** Principal Component Analysis")

        st.markdown("#### 🎯 Principal Component Analysis (PCA)")
        st.markdown("PCA reduces dimensionality while preserving variance in the data")

        # Prepare data
        features_for_pca = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins']

        # Ensure all features are numeric and drop NaN
        intrusion_df_pca = intrusion_df.copy()
        for col in features_for_pca:
            intrusion_df_pca[col] = pd.to_numeric(intrusion_df_pca[col], errors='coerce')

        intrusion_df_pca['attack_detected'] = pd.to_numeric(intrusion_df_pca['attack_detected'], errors='coerce')

        # Drop rows with NaN in required columns
        intrusion_df_pca = intrusion_df_pca[features_for_pca + ['attack_detected']].dropna()

        if len(intrusion_df_pca) < 10:
            st.warning("Not enough valid data for PCA analysis. Please check your data quality.")
            return

        X = intrusion_df_pca[features_for_pca].values
        y = intrusion_df_pca['attack_detected'].values

        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply PCA
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)

        explained_var = pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📊 Explained Variance")

            fig = go.Figure()
            fig.add_trace(go.Bar(x=list(range(1, len(explained_var)+1)),
                                y=explained_var,
                                name='Individual',
                                marker_color='steelblue'))
            fig.add_trace(go.Scatter(x=list(range(1, len(cumulative_var)+1)),
                                    y=cumulative_var,
                                    mode='lines+markers',
                                    name='Cumulative',
                                    marker_color='red',
                                    line=dict(width=3)))
            fig.update_layout(title='PCA Scree Plot',
                             xaxis_title='Principal Component',
                             yaxis_title='Explained Variance Ratio',
                             height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("##### 📈 PCA Statistics")

            pca_stats = pd.DataFrame({
                'Component': [f'PC{i+1}' for i in range(len(explained_var))],
                'Variance (%)': (explained_var * 100).round(2),
                'Cumulative (%)': (cumulative_var * 100).round(2)
            })

            st.dataframe(pca_stats, use_container_width=True, height=300)

            st.metric("PC1 Variance", f"{explained_var[0]*100:.2f}%")
            st.metric("PC1+PC2 Total", f"{cumulative_var[1]*100:.2f}%")
            st.metric("Components for 95%", f"{np.argmax(cumulative_var >= 0.95) + 1}")

        st.markdown("---")

        # 2D Projection
        st.markdown("##### 📍 2D PCA Projection")

        pca_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'Classification': ['Attack' if x == 1 else 'Normal' for x in y]
        })

        # Sample for performance
        sample_pca = pca_df.sample(min(10000, len(pca_df)))

        fig = px.scatter(sample_pca, x='PC1', y='PC2', color='Classification',
                        title=f'PCA Projection (PC1: {explained_var[0]*100:.1f}%, PC2: {explained_var[1]*100:.1f}%)',
                        color_discrete_map={'Normal': 'blue', 'Attack': 'red'},
                        opacity=0.5)
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Component loadings
        st.markdown("##### 🔍 Feature Loadings on Principal Components")

        loadings = pd.DataFrame(
            pca.components_[:3].T,
            columns=['PC1', 'PC2', 'PC3'],
            index=[f.replace('_', ' ').title() for f in features_for_pca]
        ).round(3)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(loadings, use_container_width=True)

        with col2:
            fig = px.imshow(loadings.T,
                           labels=dict(x="Feature", y="Component", color="Loading"),
                           title='Feature Loadings Heatmap',
                           color_continuous_scale='RdBu_r',
                           aspect='auto')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    else:  # Advanced Statistics
        st.info("**Datasets:** Both Global Threats and Intrusion Detection")

        st.markdown("#### 📊 Advanced Statistical Analysis")

        dataset_choice = st.selectbox("Select Dataset for Analysis",
                                     ["Global Cybersecurity Threats", "Intrusion Detection"])

        if dataset_choice == "Global Cybersecurity Threats":
            # Remove duplicates
            global_df = global_df.drop_duplicates()

            st.markdown("##### 📈 Distribution Analysis")

            # Ensure Financial Loss column is numeric
            global_df['Financial Loss (in Million $)'] = pd.to_numeric(
                global_df['Financial Loss (in Million $)'], errors='coerce'
            )

            # Drop NaN values
            loss_data = global_df['Financial Loss (in Million $)'].dropna()

            if len(loss_data) > 0:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Financial Loss Distribution**")
                    st.metric("Mean", f"${loss_data.mean():.2f}M")
                    st.metric("Median", f"${loss_data.median():.2f}M")
                    st.metric("Skewness", f"{loss_data.skew():.2f}")
                    st.metric("Kurtosis", f"{loss_data.kurtosis():.2f}")

                    if loss_data.skew() > 1:
                        st.warning("⚠️ Highly right-skewed distribution (mean >> median)")
                    else:
                        st.success("✅ Moderately skewed distribution")

                with col2:
                    # Create dataframe for plotting
                    plot_df = pd.DataFrame({'Financial Loss (in Million $)': loss_data})

                    fig = px.histogram(plot_df, x='Financial Loss (in Million $)',
                                      nbins=50, title='Financial Loss Distribution',
                                      marginal='box')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No valid financial loss data available for analysis.")

        else:  # Intrusion Detection
            st.markdown("##### 🎯 Class Imbalance Analysis")

            attack_rate = intrusion_df['attack_detected'].mean() * 100
            imbalance_ratio = (1 - intrusion_df['attack_detected'].mean()) / intrusion_df['attack_detected'].mean()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Attack Rate", f"{attack_rate:.2f}%")
            with col2:
                st.metric("Imbalance Ratio", f"{imbalance_ratio:.2f}:1")
            with col3:
                if imbalance_ratio > 10:
                    st.error("❌ Severe imbalance")
                elif imbalance_ratio > 5:
                    st.warning("⚠️ Moderate imbalance")
                else:
                    st.success("✅ Balanced dataset")

            st.markdown("##### 📊 Statistical Tests")
            st.markdown("**T-test: Failed Logins (Attack vs Normal)**")

            attack_failed = intrusion_df[intrusion_df['attack_detected'] == 1]['failed_logins']
            normal_failed = intrusion_df[intrusion_df['attack_detected'] == 0]['failed_logins']

            t_stat, p_value = stats.ttest_ind(attack_failed, normal_failed)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Attack Mean", f"{attack_failed.mean():.2f}")
            with col2:
                st.metric("Normal Mean", f"{normal_failed.mean():.2f}")
            with col3:
                st.metric("p-value", f"{p_value:.2e}")

            if p_value < 0.05:
                st.success("✅ Statistically significant difference (p < 0.05)")
            else:
                st.info("ℹ️ No significant difference (p >= 0.05)")


def show_data_explorer(global_threats, intrusion_data):
    """Data Explorer with Filters for Both Datasets"""

    st.markdown("### 📋 Data Explorer")
    st.info("**Purpose:** Browse and filter raw data from both datasets")

    # Dataset selector
    dataset_choice = st.radio("Select Dataset to Explore",
                             ["🌍 Global Cybersecurity Threats", "🔐 Intrusion Detection"],
                             horizontal=True)

    if "Global" in dataset_choice:
        st.markdown("#### 🌍 Global Cybersecurity Threats Dataset")

        # Remove duplicates
        df = global_threats.drop_duplicates().copy()

        # Filters in columns
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%);
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,120,212,0.3);
            margin: 20px 0;
        ">
            <h4 style="color: white; margin: 0; font-size: 18px; font-weight: 700;">
                🔍 FILTER DATA
            </h4>
            <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 13px;">
                Apply filters to refine the dataset view
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Filter controls with white background panel
        st.markdown("""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        ">
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Year filter
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">📅 Year</p>', unsafe_allow_html=True)
            year_options = ['All'] + sorted(df['Year'].unique().tolist())
            selected_years = st.multiselect("Year", year_options, default=['All'], key='explorer_year', label_visibility="collapsed")

        with col2:
            # Country filter
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🌍 Country</p>', unsafe_allow_html=True)
            country_options = ['All'] + sorted(df['Country'].unique().tolist())
            selected_countries = st.multiselect("Country", country_options, default=['All'], key='explorer_country', label_visibility="collapsed")

        with col3:
            # Attack Type filter
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🎯 Attack Type</p>', unsafe_allow_html=True)
            attack_type_options = ['All'] + sorted(df['Attack Type'].unique().tolist())
            selected_attack_types = st.multiselect("Attack Type", attack_type_options, default=['All'], key='explorer_attack', label_visibility="collapsed")

        with col4:
            # Industry filter
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🏢 Industry</p>', unsafe_allow_html=True)
            industry_options = ['All'] + sorted(df['Target Industry'].unique().tolist())
            selected_industries = st.multiselect("Industry", industry_options, default=['All'], key='explorer_industry', label_visibility="collapsed")

        # Apply filters
        filtered_df = df.copy()

        if 'All' not in selected_years:
            filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

        if 'All' not in selected_countries:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]

        if 'All' not in selected_attack_types:
            filtered_df = filtered_df[filtered_df['Attack Type'].isin(selected_attack_types)]

        if 'All' not in selected_industries:
            filtered_df = filtered_df[filtered_df['Target Industry'].isin(selected_industries)]

        # Display filtered count
        st.success(f"📊 Showing **{len(filtered_df):,}** records (filtered from {len(df):,} total)")

        st.markdown("---")

        # Display data with highlighting
        st.markdown("##### 📊 Filtered Dataset (First 100 Rows)")
        st.dataframe(
            filtered_df.head(100).style.highlight_max(axis=0, subset=['Financial Loss (in Million $)', 'Number of Affected Users']),
            use_container_width=True,
            height=400
        )

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name='filtered_global_threats.csv',
            mime='text/csv'
        )

        st.markdown("---")

        # Summary statistics
        st.markdown("##### 📈 Summary Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Incidents", f"{len(filtered_df):,}")
            st.metric("Unique Countries", filtered_df['Country'].nunique())

        with col2:
            st.metric("Total Loss", f"${filtered_df['Financial Loss (in Million $)'].sum():,.1f}M")
            st.metric("Avg Loss", f"${filtered_df['Financial Loss (in Million $)'].mean():,.2f}M")

        with col3:
            st.metric("Total Users Affected", f"{filtered_df['Number of Affected Users'].sum():,.0f}")
            st.metric("Avg Resolution Time", f"{filtered_df['Incident Resolution Time (in Hours)'].mean():.1f}h")

        # Detailed statistics table
        st.markdown("##### 📊 Detailed Statistics by Attack Type")
        if len(filtered_df) > 0:
            stats_by_type = filtered_df.groupby('Attack Type').agg({
                'Financial Loss (in Million $)': ['count', 'sum', 'mean', 'median'],
                'Number of Affected Users': ['sum', 'mean'],
                'Incident Resolution Time (in Hours)': ['mean', 'median']
            }).round(2)

            stats_by_type.columns = ['Count', 'Total Loss ($M)', 'Avg Loss ($M)', 'Median Loss ($M)',
                                     'Total Users', 'Avg Users', 'Avg Resolution (h)', 'Median Resolution (h)']
            st.dataframe(stats_by_type.sort_values('Total Loss ($M)', ascending=False), use_container_width=True)
        else:
            st.warning("No data available with current filters.")

    else:
        st.markdown("#### 🔐 Intrusion Detection Dataset")

        df = intrusion_data.copy()

        # Filters in columns
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%);
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,120,212,0.3);
            margin: 20px 0;
        ">
            <h4 style="color: white; margin: 0; font-size: 18px; font-weight: 700;">
                🔍 FILTER DATA
            </h4>
            <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 13px;">
                Apply filters to refine the dataset view
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Filter controls with white background panel
        st.markdown("""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        ">
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Attack detected filter
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🚨 Attack Status</p>', unsafe_allow_html=True)
            attack_filter = st.selectbox("Attack Status", ['All', 'Attack (1)', 'Normal (0)'], key='explorer_attack_status', label_visibility="collapsed")

        with col2:
            # Protocol filter - handle mixed types and NaN values
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🌐 Protocol</p>', unsafe_allow_html=True)
            protocol_values = df['protocol_type'].dropna().astype(str).unique().tolist()
            protocol_options = ['All'] + sorted(protocol_values)
            selected_protocols = st.multiselect("Protocol", protocol_options, default=['All'], key='explorer_protocol', label_visibility="collapsed")

        with col3:
            # Encryption filter - handle mixed types and NaN values
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🔐 Encryption</p>', unsafe_allow_html=True)
            encryption_values = df['encryption_used'].dropna().astype(str).unique().tolist()
            encryption_options = ['All'] + sorted(encryption_values)
            selected_encryptions = st.multiselect("Encryption", encryption_options, default=['All'], key='explorer_encryption', label_visibility="collapsed")

        with col4:
            # Browser filter - handle mixed types and NaN values
            st.markdown('<p style="color: #2c3e50; font-weight: 600; font-size: 14px; margin-bottom: 8px;">🌐 Browser</p>', unsafe_allow_html=True)
            browser_values = df['browser_type'].dropna().astype(str).unique().tolist()
            browser_options = ['All'] + sorted(browser_values)
            selected_browsers = st.multiselect("Browser", browser_options, default=['All'], key='explorer_browser', label_visibility="collapsed")

        # Apply filters
        filtered_df = df.copy()

        if attack_filter == 'Attack (1)':
            filtered_df = filtered_df[filtered_df['attack_detected'] == 1]
        elif attack_filter == 'Normal (0)':
            filtered_df = filtered_df[filtered_df['attack_detected'] == 0]

        if 'All' not in selected_protocols:
            filtered_df = filtered_df[filtered_df['protocol_type'].isin(selected_protocols)]

        if 'All' not in selected_encryptions:
            filtered_df = filtered_df[filtered_df['encryption_used'].isin(selected_encryptions)]

        if 'All' not in selected_browsers:
            filtered_df = filtered_df[filtered_df['browser_type'].isin(selected_browsers)]

        # Display filtered count
        st.success(f"📊 Showing **{len(filtered_df):,}** records (filtered from {len(df):,} total)")

        st.markdown("---")

        # Display data
        st.markdown("##### 📊 Filtered Dataset (First 100 Rows)")
        st.dataframe(filtered_df.head(100), use_container_width=True, height=400)

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name='filtered_intrusion_data.csv',
            mime='text/csv'
        )

        st.markdown("---")

        # Summary statistics
        st.markdown("##### 📈 Summary Statistics")

        attack_rate = (filtered_df['attack_detected'].mean() * 100) if len(filtered_df) > 0 else 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", f"{len(filtered_df):,}")
            st.metric("Attack Rate", f"{attack_rate:.2f}%")

        with col2:
            st.metric("Avg Packet Size", f"{filtered_df['network_packet_size'].mean():.1f}")
            st.metric("Avg Login Attempts", f"{filtered_df['login_attempts'].mean():.2f}")

        with col3:
            st.metric("Avg Session Duration", f"{filtered_df['session_duration'].mean():.1f}s")
            st.metric("Avg Failed Logins", f"{filtered_df['failed_logins'].mean():.2f}")

        with col4:
            st.metric("Avg IP Reputation", f"{filtered_df['ip_reputation_score'].mean():.3f}")
            st.metric("Unusual Time Access %", f"{(filtered_df['unusual_time_access'].mean() * 100):.1f}%")

        # Protocol breakdown
        st.markdown("##### 📊 Breakdown by Protocol")
        if len(filtered_df) > 0:
            protocol_stats = filtered_df.groupby('protocol_type').agg({
                'attack_detected': ['count', 'sum', 'mean'],
                'network_packet_size': 'mean',
                'session_duration': 'mean'
            }).round(2)

            protocol_stats.columns = ['Total Records', 'Attacks', 'Attack Rate', 'Avg Packet Size', 'Avg Session Duration']
            protocol_stats['Attack Rate'] = (protocol_stats['Attack Rate'] * 100).round(2)
            st.dataframe(protocol_stats, use_container_width=True)
        else:
            st.warning("No data available with current filters.")


def show_key_findings(global_threats, intrusion_data):
    """Display key findings and insights with data science storytelling"""

    st.markdown("## 💡 Key Findings & Data Science Insights")

    st.markdown("""
    > *"The goal of data science is not just to find patterns, but to translate them into actionable intelligence.
    > What have we learned, and what should we do about it?"*
    """)

    # Remove duplicates and ensure Year is numeric
    global_threats = ensure_year_numeric(global_threats.drop_duplicates())

    st.markdown("---")

    # Finding 1: Temporal Evolution
    st.markdown("### 🔍 Finding 1: The Threat Landscape is Evolving Exponentially")

    col1, col2 = st.columns([2, 1])

    with col1:
        attacks_by_year = global_threats.groupby('Year').size().reset_index(name='Count')
        growth_rate = ((attacks_by_year['Count'].iloc[-1] / attacks_by_year['Count'].iloc[0]) - 1) * 100

        # Convert to lists for better Plotly compatibility
        find_years = [int(y) for y in attacks_by_year['Year']]
        find_counts = [int(c) for c in attacks_by_year['Count']]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=find_years, y=find_counts,
                                mode='lines+markers',
                                name='Attacks',
                                line=dict(color='#1f77b4', width=3),
                                marker=dict(size=8)))

        # Add trend line
        z = np.polyfit(find_years, find_counts, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=find_years, y=p(find_years),
                                mode='lines',
                                name='Trend',
                                line=dict(dash='dash', color='red', width=3)))

        fig.update_layout(
            title='Attack Frequency Growth (2015-2024)',
            xaxis_title='Year',
            yaxis_title='Count',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Statistical Evidence")
        st.metric("Total Growth", f"{growth_rate:.1f}%", delta="2015-2024")
        st.metric("CAGR", f"{(np.power(attacks_by_year['Count'].iloc[-1]/attacks_by_year['Count'].iloc[0], 1/9) - 1)*100:.1f}%", delta="Compound Annual")

        st.markdown("**🎓 Data Science Insight:**")
        st.info("""
        The near-linear trend suggests systematic growth, not random variation.
        This indicates structural changes in the threat landscape (more connected devices,
        sophisticated attackers) rather than periodic spikes.
        """)

    st.markdown("---")

    # Finding 2: Class Imbalance Challenge
    st.markdown("### 🔍 Finding 2: Severe Class Imbalance in Intrusion Detection")

    col1, col2 = st.columns([1, 2])

    with col1:
        attack_rate = intrusion_data['attack_detected'].mean() * 100
        imbalance_ratio = (1 - intrusion_data['attack_detected'].mean()) / intrusion_data['attack_detected'].mean()

        st.metric("Attack Rate", f"{attack_rate:.2f}%")
        st.metric("Imbalance Ratio", f"{imbalance_ratio:.1f}:1")

        st.markdown("**🎓 ML Implication:**")
        st.warning("""
        With this severe imbalance, standard accuracy is misleading.
        We must use:
        - Precision-Recall curves
        - F1-score
        - SMOTE or class weighting
        - Cost-sensitive learning
        """)

    with col2:
        attack_counts = intrusion_data['attack_detected'].value_counts()

        fig = px.pie(values=attack_counts.values,
                    names=['Normal Traffic', 'Attack Traffic'],
                    title='Class Distribution in Intrusion Dataset',
                    color_discrete_sequence=['#4444ff', '#ff4444'],
                    hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Finding 3: Geographic Concentration
    st.markdown("### 🔍 Finding 3: Attack Impact is Highly Concentrated")

    country_stats = global_threats.groupby('Country').agg({
        'Financial Loss (in Million $)': 'sum'
    }).sort_values('Financial Loss (in Million $)', ascending=False).reset_index()

    top_10_loss = country_stats.head(10)['Financial Loss (in Million $)'].sum()
    total_loss = country_stats['Financial Loss (in Million $)'].sum()
    concentration = (top_10_loss / total_loss) * 100

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(country_stats.head(10), y='Country', x='Financial Loss (in Million $)',
                    orientation='h',
                    title='Top 10 Countries by Financial Loss',
                    color='Financial Loss (in Million $)',
                    color_continuous_scale='Reds')
        fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Concentration Metrics")
        st.metric("Top 10 Share", f"{concentration:.1f}%", delta="of total losses")
        st.metric("Countries Affected", country_stats.shape[0])

        st.markdown("**🎓 Risk Management Insight:**")
        st.info("""
        Pareto principle in action: ~80% of losses come from ~20% of locations.
        Risk mitigation should prioritize high-value targets in concentrated regions.
        """)

    st.markdown("---")

    # Finding 4: Protocol Vulnerabilities
    st.markdown("### 🔍 Finding 4: TCP Shows Significantly Higher Attack Rates")

    protocol_stats = intrusion_data.groupby('protocol_type').agg({
        'attack_detected': ['sum', 'count', 'mean']
    })
    protocol_stats.columns = ['Attacks', 'Total', 'Attack_Rate']
    protocol_stats['Attack_Rate'] = (protocol_stats['Attack_Rate'] * 100).round(2)
    protocol_stats = protocol_stats.reset_index()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(protocol_stats, x='protocol_type', y='Attack_Rate',
                    title='Attack Rate by Protocol Type (%)',
                    color='Attack_Rate',
                    color_continuous_scale='Reds',
                    text='Attack_Rate')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Statistical Test")

        tcp_attacks = intrusion_data[intrusion_data['protocol_type'] == 'TCP']['attack_detected']
        udp_attacks = intrusion_data[intrusion_data['protocol_type'] == 'UDP']['attack_detected']

        if len(tcp_attacks) > 0 and len(udp_attacks) > 0:
            from scipy.stats import chi2_contingency

            contingency = pd.crosstab(intrusion_data['protocol_type'], intrusion_data['attack_detected'])
            chi2, p_value, dof, expected = chi2_contingency(contingency)

            st.metric("Chi-square", f"{chi2:.2f}")
            st.metric("p-value", f"{p_value:.2e}")

            if p_value < 0.05:
                st.success("✅ Statistically significant (p < 0.05)")
            else:
                st.warning("⚠️ Not statistically significant")

        st.markdown("**🎓 Security Insight:**")
        st.info("""
        TCP's connection-oriented nature creates more attack surface.
        Recommendation: Enhanced monitoring and anomaly detection for TCP traffic.
        """)

    st.markdown("---")

    # Finding 5: Feature Correlation for ML
    st.markdown("### 🔍 Finding 5: Failed Logins Strongly Predict Attacks")

    numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                       'ip_reputation_score', 'failed_logins', 'unusual_time_access']

    corr_matrix = intrusion_data[numeric_features + ['attack_detected']].corr()
    target_corr = corr_matrix['attack_detected'].drop('attack_detected').sort_values(ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        target_corr_df = pd.DataFrame({
            'Feature': [f.replace('_', ' ').title() for f in target_corr.index],
            'Correlation': target_corr.values
        })

        fig = px.bar(target_corr_df, y='Feature', x='Correlation',
                    orientation='h',
                    title='Feature Correlation with Attack Detection',
                    color='Correlation',
                    color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=0)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 ML Feature Importance")

        top_feature = target_corr.idxmax()
        top_corr = target_corr.max()

        st.metric("Strongest Predictor", top_feature.replace('_', ' ').title())
        st.metric("Correlation", f"{top_corr:.3f}")

        st.markdown("**🎓 ML Engineering Insight:**")
        st.info("""
        Feature engineering opportunity:
        - Create ratio features (failed/total logins)
        - Time-window aggregations
        - Interaction terms between correlated features
        """)

    st.markdown("---")

    # Executive Summary
    st.markdown("### 🎯 Executive Summary: What Should We Do?")

    recommendations = [
        {
            "priority": "🔴 Critical",
            "finding": "Exponential growth in attacks",
            "action": "Increase security budget proportionally; invest in automated detection systems",
            "stakeholder": "C-Suite, Security Leadership"
        },
        {
            "priority": "🟠 High",
            "finding": "Severe class imbalance in detection data",
            "action": "Implement specialized ML techniques (SMOTE, ensemble methods) for rare event detection",
            "stakeholder": "Data Science Team, ML Engineers"
        },
        {
            "priority": "🟠 High",
            "finding": "Geographic concentration of losses",
            "action": "Deploy enhanced security controls in top 10 high-risk countries",
            "stakeholder": "Global Security Operations"
        },
        {
            "priority": "🟡 Medium",
            "finding": "TCP protocol vulnerability",
            "action": "Implement deep packet inspection and behavioral analysis for TCP traffic",
            "stakeholder": "Network Security Team"
        },
        {
            "priority": "🟡 Medium",
            "finding": "Failed logins as strong predictor",
            "action": "Deploy real-time alerting on anomalous login patterns; implement MFA",
            "stakeholder": "Identity & Access Management"
        }
    ]

    st.markdown("#### 📋 Actionable Recommendations")

    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"{i}. {rec['priority']}: {rec['finding']}", expanded=(i <= 2)):
            st.markdown(f"**📌 Recommended Action:**")
            st.write(rec['action'])
            st.markdown(f"**👥 Key Stakeholder:** {rec['stakeholder']}")

    st.markdown("---")

    st.success("""
    **🎓 Data Science Conclusion:**

    This analysis demonstrates the power of combining macro-level threat intelligence with micro-level
    network data. By bridging these perspectives, we've identified:

    1. **Quantifiable trends** - Not just "attacks are increasing" but *by how much* and *at what rate*
    2. **Statistically validated insights** - Used hypothesis testing to validate observations
    3. **ML-ready findings** - Identified class imbalance, feature importance, and engineering opportunities
    4. **Actionable intelligence** - Translated technical findings into business recommendations

    **Next Steps for Your Organization:**
    - Deploy ML models for real-time intrusion detection
    - Implement recommended security controls
    - Establish KPIs to track improvement
    - Continue data collection for longitudinal analysis
    """)
