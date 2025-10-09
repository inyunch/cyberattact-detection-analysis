import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def show(global_threats, intrusion_data):
    """Display IDA and EDA analysis with improved layout"""

    st.title("📊 Initial Data Analysis (IDA) & Exploratory Data Analysis (EDA)")
    st.markdown("### Comprehensive Statistical Analysis for Both Datasets")
    st.markdown("---")

    if global_threats is None or intrusion_data is None:
        st.error("Unable to load data for analysis.")
        return

    # Main navigation tabs
    main_tab1, main_tab2 = st.tabs(["🔍 Initial Data Analysis (IDA)", "📈 Exploratory Data Analysis (EDA)"])

    # ==================== IDA TAB ====================
    with main_tab1:
        st.markdown("## 🔍 Initial Data Analysis")
        st.info("📌 **Purpose:** Understand data structure, quality, and basic statistics for both datasets")

        # Create sub-tabs for both datasets
        ida_tab1, ida_tab2 = st.tabs(["🌍 Global Cybersecurity Threats", "🔐 Intrusion Detection"])

        with ida_tab1:
            show_ida_global(global_threats)

        with ida_tab2:
            show_ida_intrusion(intrusion_data)

    # ==================== EDA TAB ====================
    with main_tab2:
        st.markdown("## 📈 Exploratory Data Analysis")
        st.info("📌 **Purpose:** Deep dive into patterns, relationships, and insights from both datasets")

        # Create sub-tabs for different analysis types
        eda_tab1, eda_tab2, eda_tab3, eda_tab4, eda_tab5 = st.tabs([
            "📅 Temporal Analysis",
            "🗺️ Geographic Analysis",
            "🔗 Correlation Analysis",
            "⚔️ Attack Behavior",
            "🔬 Advanced Analytics"
        ])

        with eda_tab1:
            show_temporal_analysis(global_threats)

        with eda_tab2:
            show_geographic_analysis(global_threats)

        with eda_tab3:
            show_correlation_analysis(global_threats, intrusion_data)

        with eda_tab4:
            show_behavior_analysis(intrusion_data)

        with eda_tab5:
            show_advanced_analytics(global_threats, intrusion_data)


# ==================== IDA FUNCTIONS ====================

def show_ida_global(df):
    """IDA for Global Threats Dataset with improved layout"""

    st.markdown("### 📋 Dataset Overview")

    # Remove duplicates for analysis
    df = df.drop_duplicates()

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
    """Temporal Analysis for Global Threats"""

    st.markdown("### 📅 Temporal Trend Analysis")
    st.info("**Dataset:** Global Cybersecurity Threats (2015-2024)")

    # Remove duplicates
    df = df.drop_duplicates()

    # Attack frequency over time
    attacks_by_year = df.groupby('Year').size().reset_index(name='Count')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Attack Frequency Trend")

        fig = px.line(attacks_by_year, x='Year', y='Count',
                     title='Cyberattack Frequency (2015-2024)',
                     markers=True)

        # Add trend line
        z = np.polyfit(attacks_by_year['Year'], attacks_by_year['Count'], 1)
        p = np.poly1d(z)
        fig.add_scatter(x=attacks_by_year['Year'], y=p(attacks_by_year['Year']),
                       mode='lines', name='Trend', line=dict(dash='dash', color='red'))

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Year-over-Year Growth Rate")

        attacks_by_year['YoY_Growth'] = attacks_by_year['Count'].pct_change() * 100

        fig = px.bar(attacks_by_year[1:], x='Year', y='YoY_Growth',
                    title='YoY Growth Rate (%)',
                    labels={'YoY_Growth': 'Growth Rate (%)'},
                    color='YoY_Growth',
                    color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=0)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Statistics
    total_growth = ((attacks_by_year['Count'].iloc[-1] / attacks_by_year['Count'].iloc[0]) - 1) * 100
    slope, intercept, r_value, p_value, std_err = stats.linregress(attacks_by_year['Year'], attacks_by_year['Count'])

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

    st.markdown("---")

    # Financial losses over time
    st.markdown("#### 💰 Financial Impact Over Time")

    losses_by_year = df.groupby('Year').agg({
        'Financial Loss (in Million $)': ['sum', 'mean', 'median']
    }).round(2)
    losses_by_year.columns = ['Total_Loss', 'Avg_Loss', 'Median_Loss']
    losses_by_year = losses_by_year.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(losses_by_year, x='Year', y='Total_Loss',
                    title='Total Financial Losses by Year ($M)',
                    labels={'Total_Loss': 'Total Loss ($M)'},
                    color='Total_Loss',
                    color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=losses_by_year['Year'], y=losses_by_year['Avg_Loss'],
                                mode='lines+markers', name='Mean', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=losses_by_year['Year'], y=losses_by_year['Median_Loss'],
                                mode='lines+markers', name='Median', line=dict(color='green', width=3)))
        fig.update_layout(title='Average vs Median Loss Per Incident',
                         xaxis_title='Year',
                         yaxis_title='Loss ($M)',
                         height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Attack type evolution
    st.markdown("#### 🎯 Attack Type Evolution")

    attack_type_evolution = pd.crosstab(df['Year'], df['Attack Type'])

    fig = px.area(attack_type_evolution,
                 title='Attack Type Distribution Over Time',
                 labels={'value': 'Count', 'variable': 'Attack Type'})
    fig.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)


def show_geographic_analysis(df):
    """Geographic Analysis for Global Threats"""

    st.markdown("### 🗺️ Geographic Distribution Analysis")
    st.info("**Dataset:** Global Cybersecurity Threats")

    # Remove duplicates
    df = df.drop_duplicates()

    # Country statistics
    country_stats = df.groupby('Country').agg({
        'Financial Loss (in Million $)': ['sum', 'mean', 'count'],
        'Number of Affected Users': 'sum'
    }).round(2)
    country_stats.columns = ['Total_Loss', 'Avg_Loss', 'Attack_Count', 'Total_Users']
    country_stats = country_stats.sort_values('Total_Loss', ascending=False).reset_index()

    top_countries = country_stats.head(15)

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💰 Top 15 Countries by Financial Loss")
        fig = px.bar(top_countries, y='Country', x='Total_Loss',
                    orientation='h',
                    title='Total Financial Loss by Country ($M)',
                    labels={'Total_Loss': 'Total Loss ($M)'},
                    color='Total_Loss',
                    color_continuous_scale='Reds')
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Top 15 Countries by Attack Frequency")
        fig = px.bar(top_countries, y='Country', x='Attack_Count',
                    orientation='h',
                    title='Number of Attacks by Country',
                    labels={'Attack_Count': 'Number of Attacks'},
                    color='Attack_Count',
                    color_continuous_scale='Blues')
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Choropleth map
    st.markdown("#### 🌍 Global Heat Map")

    map_metric = st.radio("Select Metric for Map",
                         ["Total Financial Loss", "Attack Count", "Average Loss Per Attack"],
                         horizontal=True)

    if map_metric == "Total Financial Loss":
        color_col = 'Total_Loss'
        color_label = 'Total Loss ($M)'
        color_scale = 'Reds'
    elif map_metric == "Attack Count":
        color_col = 'Attack_Count'
        color_label = 'Number of Attacks'
        color_scale = 'Blues'
    else:
        color_col = 'Avg_Loss'
        color_label = 'Avg Loss ($M)'
        color_scale = 'Oranges'

    fig = px.choropleth(country_stats,
                       locations='Country',
                       locationmode='country names',
                       color=color_col,
                       hover_name='Country',
                       hover_data=['Attack_Count', 'Total_Loss', 'Avg_Loss', 'Total_Users'],
                       title=f'Global {map_metric} Distribution',
                       color_continuous_scale=color_scale,
                       labels={color_col: color_label})
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Top statistics table
    st.markdown("#### 📊 Top 20 Countries - Detailed Statistics")
    st.dataframe(country_stats.head(20), use_container_width=True, height=400)


def show_correlation_analysis(global_df, intrusion_df):
    """Correlation Analysis for Both Datasets"""

    st.markdown("### 🔗 Correlation Analysis")

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

        corr_matrix = global_df[numeric_cols].corr()

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
        st.info("**Analyzing:** Intrusion Detection Dataset")

        numeric_features = ['network_packet_size', 'login_attempts', 'session_duration',
                           'ip_reputation_score', 'failed_logins', 'unusual_time_access', 'attack_detected']

        corr_matrix = intrusion_df[numeric_features].corr()

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

        sample_df = df.sample(min(5000, len(df)))

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

        X = intrusion_df[features_for_pca].values
        y = intrusion_df['attack_detected'].values

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

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Financial Loss Distribution**")
                st.metric("Mean", f"${global_df['Financial Loss (in Million $)'].mean():.2f}M")
                st.metric("Median", f"${global_df['Financial Loss (in Million $)'].median():.2f}M")
                st.metric("Skewness", f"{global_df['Financial Loss (in Million $)'].skew():.2f}")
                st.metric("Kurtosis", f"{global_df['Financial Loss (in Million $)'].kurtosis():.2f}")

                if global_df['Financial Loss (in Million $)'].skew() > 1:
                    st.warning("⚠️ Highly right-skewed distribution (mean >> median)")
                else:
                    st.success("✅ Moderately skewed distribution")

            with col2:
                fig = px.histogram(global_df, x='Financial Loss (in Million $)',
                                  nbins=50, title='Financial Loss Distribution',
                                  marginal='box')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

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
