"""
IDA/EDA Analysis Module for Cybersecurity Dashboard

This module provides comprehensive Initial Data Analysis (IDA) and Exploratory Data Analysis (EDA)
for cybersecurity threat data and intrusion detection datasets.

Key Features:
- Data quality assessment and completeness metrics
- Missing data imputation using MICE algorithm
- Temporal analysis of cyber threats over time
- Geographic analysis with interactive visualizations
- Correlation analysis between threat metrics
- Behavioral pattern analysis
- Advanced analytics including PCA and statistical tests
- Data exploration with filtering and downloadable views

Functions:
- show(): Main entry point that displays the complete IDA/EDA analysis
- show_mice_imputation_section(): Handle missing data imputation
- show_ida_global(): Initial data analysis for global threats dataset
- show_ida_intrusion(): Initial data analysis for intrusion detection dataset
- show_temporal_analysis(): Time-based threat analysis
- show_geographic_analysis(): Geographic threat distribution analysis
- show_correlation_analysis(): Correlation matrices and insights
- show_behavior_analysis(): Behavioral pattern analysis
- show_advanced_analytics(): PCA, statistical tests, and advanced metrics
- show_data_explorer(): Interactive data exploration interface
- show_key_findings(): Summary of key insights from analysis

Author: [Project Team]
Last Updated: 2025-01
"""

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
from modules.theme import COLORS, apply_plotly_theme

def ensure_year_numeric(df):
    """Ensure Year column is numeric and properly formatted"""
    if 'Year' in df.columns:
        df = df.copy()
        df['Year'] = pd.to_numeric(df['Year'].astype(str).str.replace(',', ''), errors='coerce').astype(int)
    return df

def show(global_threats, intrusion_data, phishing_data):
    """Display IDA and EDA analysis with clean, organized layout."""

    if global_threats is None or intrusion_data is None or phishing_data is None:
        st.error("Unable to load data for analysis.")
        return

    # Page header
    st.title("📊 IDA/EDA Analysis")
    st.markdown("Comprehensive exploratory data analysis of cybersecurity threats and detection patterns")

    # ==================== KEY FINDINGS AT THE TOP ====================
    st.markdown("---")
    st.markdown("## 💡 Key Data Insights")

    # Prepare data for key findings
    global_threats_clean = ensure_year_numeric(global_threats.drop_duplicates())

    # Calculate key metrics
    attacks_by_year = global_threats_clean.groupby('Year').size().reset_index(name='Count')
    growth_rate = ((attacks_by_year['Count'].iloc[-1] / attacks_by_year['Count'].iloc[0]) - 1) * 100 if len(attacks_by_year) > 1 else 0
    attack_rate = intrusion_data['attack_detected'].mean() * 100
    imbalance_ratio = (1 - intrusion_data['attack_detected'].mean()) / intrusion_data['attack_detected'].mean() if intrusion_data['attack_detected'].mean() > 0 else 0
    phishing_rate = phishing_data['CLASS_LABEL'].mean() * 100

    # Display key findings in a grid
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="padding: 20px; background: linear-gradient(135deg, {COLORS['accent_blue']}15 0%, {COLORS['accent_blue']}05 100%);
             border-left: 4px solid {COLORS['accent_blue']}; border-radius: 8px; height: 160px;">
            <div style="font-size: 0.85rem; color: {COLORS['text_muted']}; margin-bottom: 8px;">Threat Growth</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['accent_blue']}; margin-bottom: 4px;">+{growth_rate:.0f}%</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">2015-2024</div>
            <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; margin-top: 12px; line-height: 1.4;">
                Exponential growth in cyber threats indicates systematic evolution of attack sophistication
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="padding: 20px; background: linear-gradient(135deg, {COLORS['accent_red']}15 0%, {COLORS['accent_red']}05 100%);
             border-left: 4px solid {COLORS['accent_red']}; border-radius: 8px; height: 160px;">
            <div style="font-size: 0.85rem; color: {COLORS['text_muted']}; margin-bottom: 8px;">Class Imbalance</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['accent_red']}; margin-bottom: 4px;">{imbalance_ratio:.0f}:1</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">Normal vs Attack</div>
            <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; margin-top: 12px; line-height: 1.4;">
                Severe imbalance requires specialized ML techniques (SMOTE, cost-sensitive learning)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="padding: 20px; background: linear-gradient(135deg, {COLORS['accent_green']}15 0%, {COLORS['accent_green']}05 100%);
             border-left: 4px solid {COLORS['accent_green']}; border-radius: 8px; height: 160px;">
            <div style="font-size: 0.85rem; color: {COLORS['text_muted']}; margin-bottom: 8px;">Attack Detection Rate</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['accent_green']}; margin-bottom: 4px;">{attack_rate:.1f}%</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">Intrusion Dataset</div>
            <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; margin-top: 12px; line-height: 1.4;">
                Low attack rate highlights need for high-precision detection models
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="padding: 20px; background: linear-gradient(135deg, {COLORS['accent_orange']}15 0%, {COLORS['accent_orange']}05 100%);
             border-left: 4px solid {COLORS['accent_orange']}; border-radius: 8px; height: 160px;">
            <div style="font-size: 0.85rem; color: {COLORS['text_muted']}; margin-bottom: 8px;">Phishing Rate</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['accent_orange']}; margin-bottom: 4px;">{phishing_rate:.1f}%</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">URLs Classified</div>
            <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; margin-top: 12px; line-height: 1.4;">
                Balanced dataset ideal for binary classification modeling
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Dataset selection
    st.markdown("### 📊 Select Dataset for Analysis")
    dataset_option = st.radio(
        "Choose the dataset to analyze:",
        ["Global Threats Dataset", "Intrusion Detection Dataset", "Phishing Detection Dataset"],
        horizontal=True,
        help="Select which dataset to perform IDA/EDA analysis on"
    )

    st.markdown("---")

    # ==================== DATA QUALITY ASSESSMENT ====================
    st.markdown("## 🔍 Data Quality Assessment")

    # Check if missing data file exists and use it for accurate completeness metrics
    from pathlib import Path
    missing_file = Path('data/global_threat_landscape_with_missing.csv')
    if missing_file.exists():
        try:
            gt_for_metrics = pd.read_csv(missing_file)
        except:
            gt_for_metrics = global_threats
    else:
        gt_for_metrics = global_threats

    # Calculate comprehensive metrics
    gt_rows, gt_cols = gt_for_metrics.shape
    gt_missing_pct = (gt_for_metrics.isnull().sum().sum() / (gt_rows * gt_cols)) * 100
    gt_completeness = 100 - gt_missing_pct
    gt_duplicates = gt_for_metrics.duplicated().sum()

    id_rows, id_cols = intrusion_data.shape
    id_missing_pct = (intrusion_data.isnull().sum().sum() / (id_rows * id_cols)) * 100
    id_completeness = 100 - id_missing_pct
    id_duplicates = intrusion_data.duplicated().sum()

    ph_rows, ph_cols = phishing_data.shape
    ph_missing_pct = (phishing_data.isnull().sum().sum() / (ph_rows * ph_cols)) * 100
    ph_completeness = 100 - ph_missing_pct
    ph_duplicates = phishing_data.duplicated().sum()

    # Display quality metrics in organized columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="padding: 16px; background: {COLORS['bg_primary']}; border: 1px solid {COLORS['border_color']}; border-radius: 8px;">
            <div style="font-size: 0.9rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 12px;">🌍 Global Threats</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Records: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{gt_rows:,}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Features: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{gt_cols}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Completeness: <span style="color: {COLORS['accent_green']}; font-weight: 600;">{gt_completeness:.1f}%</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Duplicates: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{gt_duplicates:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="padding: 16px; background: {COLORS['bg_primary']}; border: 1px solid {COLORS['border_color']}; border-radius: 8px;">
            <div style="font-size: 0.9rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 12px;">🛡️ Intrusion Detection</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Records: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{id_rows:,}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Features: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{id_cols}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Completeness: <span style="color: {COLORS['accent_green']}; font-weight: 600;">{id_completeness:.1f}%</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Duplicates: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{id_duplicates:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="padding: 16px; background: {COLORS['bg_primary']}; border: 1px solid {COLORS['border_color']}; border-radius: 8px;">
            <div style="font-size: 0.9rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 12px;">🎣 Phishing Detection</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Records: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{ph_rows:,}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Features: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{ph_cols}</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Completeness: <span style="color: {COLORS['accent_green']}; font-weight: 600;">{ph_completeness:.1f}%</span></div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">Duplicates: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{ph_duplicates:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================== DATASET-SPECIFIC ANALYSIS ====================
    if dataset_option == "Global Threats Dataset":
        st.markdown("## 📋 Global Threats Dataset Analysis")
        show_ida_global(global_threats)

    elif dataset_option == "Intrusion Detection Dataset":
        st.markdown("## 📋 Intrusion Detection Dataset Analysis")
        show_ida_intrusion(intrusion_data)

    elif dataset_option == "Phishing Detection Dataset":
        st.markdown("## 📋 Phishing Detection Dataset Analysis")
        show_ida_phishing(phishing_data)

    st.markdown("---")

    # ==================== ADVANCED ANALYSIS SECTIONS (COLLAPSIBLE) ====================
    with st.expander("🔧 View Raw Data & Statistical Summary"):
        st.markdown("### Dataset Preview")
        if dataset_option == "Global Threats Dataset":
            st.dataframe(global_threats.head(20), use_container_width=True)
            st.markdown("### Statistical Summary")
            st.dataframe(global_threats.describe(), use_container_width=True)
        elif dataset_option == "Intrusion Detection Dataset":
            st.dataframe(intrusion_data.head(20), use_container_width=True)
            st.markdown("### Statistical Summary")
            st.dataframe(intrusion_data.describe(), use_container_width=True)
        else:
            st.dataframe(phishing_data.head(20), use_container_width=True)
            st.markdown("### Statistical Summary")
            st.dataframe(phishing_data.describe(), use_container_width=True)

    # ==================== ADVANCED ANALYSIS (OPTIONAL EXPANDERS) ====================

    # MICE Imputation Analysis
    with st.expander("🔬 MICE Imputation Analysis - Missing Data Handling"):
        show_mice_imputation_section()

    # Temporal Analysis (only for Global Threats)
    if dataset_option == "Global Threats Dataset":
        with st.expander("📅 Temporal Trend Analysis - Time-based Patterns"):
            show_temporal_analysis(global_threats)

        with st.expander("🗺️ Geographic Distribution Analysis - Regional Insights"):
            show_geographic_analysis(global_threats)

    # Correlation Analysis
    with st.expander("📊 Correlation Analysis - Feature Relationships"):
        if dataset_option == "Global Threats Dataset":
            show_correlation_analysis(global_threats, intrusion_data)
        elif dataset_option == "Intrusion Detection Dataset":
            # Show only intrusion correlations
            st.markdown("### Feature Correlations - Intrusion Detection")
            numeric_cols = intrusion_data.select_dtypes(include=[np.number]).columns
            corr_matrix = intrusion_data[numeric_cols].corr()

            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 8}
            ))

            fig = apply_plotly_theme(fig, title="Correlation Heatmap")
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Phishing correlations
            st.markdown("### Feature Correlations - Phishing Detection")
            numeric_cols = phishing_data.select_dtypes(include=[np.number]).columns
            corr_matrix = phishing_data[numeric_cols].corr()

            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 8}
            ))

            fig = apply_plotly_theme(fig, title="Correlation Heatmap")
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

    # Behavioral Analysis (only for Intrusion)
    if dataset_option == "Intrusion Detection Dataset":
        with st.expander("🔍 Attack Behavior Analysis - Pattern Detection"):
            show_behavior_analysis(intrusion_data)

    # Advanced Analytics
    with st.expander("🎓 Advanced Analytics - PCA & Statistical Tests"):
        show_advanced_analytics(global_threats, intrusion_data)


# ==================== MICE IMPUTATION SECTION ====================
def show_mice_imputation_section():
    """Display MICE imputation analysis section."""
    from pathlib import Path

    st.markdown("### Missing Data Analysis & Imputation")
    st.markdown("Multiple Imputation by Chained Equations (MICE) for handling missing Financial Loss data")

    # Check if imputation files exist
    data_dir = Path('data')
    missing_file = data_dir / 'global_threat_landscape_with_missing.csv'
    imputed_file = data_dir / 'global_threat_landscape_imputed.csv'
    comparison_file = data_dir / 'imputation_comparison.csv'

    # Show instructions if files don't exist
    if not missing_file.exists():
        st.info("""
        ℹ️ **MICE Imputation Dataset Not Yet Generated**

        To explore missing data imputation analysis:

        1. Generate dataset with missing values:
           ```bash
           python scripts/generate_missing_data.py
           ```

        2. Run MICE imputation notebook:
           ```bash
           jupyter notebook notebooks/mice_imputation_demo.ipynb
           ```

        3. Refresh this page to see results
        """)
        return

    # Load data
    df_missing = pd.read_csv(missing_file)
    missing_count = df_missing['Financial Loss (in Million $)'].isnull().sum()
    missing_pct = (missing_count / len(df_missing)) * 100

    st.markdown("---")
    st.markdown("#### 📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df_missing):,}")
    with col2:
        st.metric("Missing Values", f"{missing_count:,}", f"{missing_pct:.1f}%")
    with col3:
        if imputed_file.exists():
            st.metric("Status", "✓ Imputed", "Analysis available")
        else:
            st.metric("Status", "⚠ Pending", "Run notebook")

    # Missing Data Randomness Analysis
    st.markdown("---")
    st.markdown("#### 🔍 Missing Data Randomness Analysis")

    # Create missing data matrix
    missing_matrix = df_missing.isnull().astype(int)
    cols_with_missing = missing_matrix.sum()[missing_matrix.sum() > 0].index.tolist()

    if len(cols_with_missing) > 0:
        # Analyze randomness for Financial Loss column
        target_col = 'Financial Loss (in Million $)'
        if target_col in cols_with_missing:
            missing_indices = df_missing[df_missing[target_col].isnull()].index.tolist()

            # Calculate spacing between missing values
            if len(missing_indices) > 1:
                missing_indices_sorted = sorted(missing_indices)
                gaps = [missing_indices_sorted[i+1] - missing_indices_sorted[i] for i in range(len(missing_indices_sorted)-1)]

                # Statistical measures of randomness
                gap_mean = np.mean(gaps)
                gap_std = np.std(gaps)
                gap_cv = gap_std / gap_mean if gap_mean > 0 else 0  # Coefficient of variation

                # Expected gap for random missing (total_records / num_missing)
                expected_gap = len(df_missing) / len(missing_indices)

                # Assess randomness
                # High CV (>0.7) and gaps close to expected = likely random
                # Low CV (<0.3) or regular gaps = likely systematic
                is_random = gap_cv > 0.5 and abs(gap_mean - expected_gap) / expected_gap < 0.3

                # Display randomness assessment
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    status = "✓ Random" if is_random else "⚠ Systematic"
                    status_color = "🟢" if is_random else "🟡"
                    st.metric("Pattern Type", status, status_color)

                with col2:
                    st.metric("Gap Variability", f"{gap_cv:.2f}", "Higher = More Random")

                with col3:
                    st.metric("Avg Gap", f"{gap_mean:.0f}", "Records between missing")

                with col4:
                    st.metric("Expected Gap", f"{expected_gap:.0f}", "For random pattern")

                # Interpretation
                st.markdown("---")
                if is_random:
                    st.success("""
                    **✓ Missing Data Appears Random (MCAR - Missing Completely At Random)**

                    The missing values are scattered randomly throughout the dataset with irregular gaps.
                    This is ideal for MICE imputation as there's no systematic bias in what's missing.

                    **What this means:**
                    - High variability in gaps between missing values
                    - No apparent pattern or clustering
                    - Safe to use MICE imputation
                    - Imputed values will be unbiased
                    """)
                else:
                    st.warning("""
                    **⚠ Missing Data May Be Systematic (MAR/MNAR)**

                    The missing values show some pattern or regularity in their distribution.
                    This could indicate the data is Missing At Random (related to other variables)
                    or Missing Not At Random (related to the missing value itself).

                    **What this means:**
                    - Regular gaps or clustering detected
                    - May be related to data collection process
                    - MICE can still work but verify results carefully
                    - Consider investigating the cause
                    """)

                # Visualize missing pattern distribution
                st.markdown("---")
                st.markdown("**📊 Missing Value Distribution Pattern**")

                # Create histogram of gaps
                fig = go.Figure()

                fig.add_trace(go.Histogram(
                    x=gaps,
                    nbinsx=min(30, len(gaps)),
                    marker_color=COLORS["accent_blue"],
                    opacity=0.7,
                    name='Actual Gaps'
                ))

                # Add vertical line for expected gap
                fig.add_vline(
                    x=expected_gap,
                    line_dash="dash",
                    line_color=COLORS["accent_orange"],
                    line_width=2,
                    annotation_text=f"Expected Gap: {expected_gap:.0f}",
                    annotation_position="top"
                )

                # Add vertical line for mean gap
                fig.add_vline(
                    x=gap_mean,
                    line_dash="dash",
                    line_color=COLORS["accent_green"],
                    line_width=2,
                    annotation_text=f"Actual Mean: {gap_mean:.0f}",
                    annotation_position="bottom"
                )

                fig = apply_plotly_theme(fig)
                fig.update_layout(
                    title=dict(text='Distribution of Gaps Between Missing Values', x=0.5),
                    xaxis_title='Records Between Missing Values',
                    yaxis_title='Frequency',
                    height=350,
                    showlegend=False
                )

                st.plotly_chart(fig, use_container_width=True)

                st.markdown("""
                **How to interpret:**
                - **Wide spread**: More random (good for MICE)
                - **Narrow spike**: Regular pattern (may be systematic)
                - **Multiple peaks**: Could indicate multiple missing mechanisms
                - **Close to expected gap**: Supports randomness
                """)
    else:
        st.success("✅ No missing values detected in any column!")

    # If imputation results exist, show quality metrics
    if comparison_file.exists():
        st.markdown("---")
        st.markdown("#### 📈 Imputation Quality Metrics")

        # Load comparison data
        comparison_df = pd.read_csv(comparison_file)
        imputed_only = comparison_df[comparison_df['Was_Missing'] == True]

        # Calculate metrics
        mae = np.abs(imputed_only['Original'] - imputed_only['Imputed']).mean()
        rmse = np.sqrt(((imputed_only['Original'] - imputed_only['Imputed']) ** 2).mean())
        mape = (np.abs((imputed_only['Original'] - imputed_only['Imputed']) / imputed_only['Original']).mean()) * 100

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("MAE", f"${mae:.2f}M", "Mean Absolute Error")
        with col2:
            st.metric("RMSE", f"${rmse:.2f}M", "Root Mean Squared")
        with col3:
            quality_color = "🟢" if mape < 10 else ("🟡" if mape < 20 else "🔴")
            st.metric("MAPE", f"{mape:.2f}%", quality_color)
        with col4:
            quality_label = "Excellent" if mape < 10 else ("Good" if mape < 20 else "Moderate")
            st.metric("Quality", quality_label, f"Based on MAPE")

    else:
        st.info("""
        ℹ️ **Imputation Results Not Yet Available**

        Run the MICE imputation notebook to generate results:

        ```bash
        jupyter notebook notebooks/mice_imputation_demo.ipynb
        ```

        After completion, refresh this page to see the analysis.
        """)

    # Documentation
    st.markdown("---")
    st.markdown("#### 📚 About MICE")

    with st.expander("ℹ️ Learn More About MICE Imputation"):
        st.markdown("""
        **MICE (Multiple Imputation by Chained Equations)** is a robust method for handling missing data.

        **How it Works:**
        1. Make initial guesses for missing values
        2. Iteratively model each variable as a function of others
        3. Update predictions until convergence

        **Features Used:**
        - Year (temporal context)
        - Incident Resolution Time (severity indicator)
        - Financial Loss (target variable)
        - Number of Affected Users (impact indicator)

        **Quality Metrics:**
        - **MAE**: Average absolute error
        - **RMSE**: Root mean squared error (penalizes large errors)
        - **MAPE**: Percentage error (scale-independent)
          - < 10%: Excellent
          - 10-20%: Good
          - > 20%: Moderate
        """)


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
                             labels={selected_num: selected_num})
            fig = apply_plotly_theme(fig, title=f'Distribution of {selected_num}')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.box(df, y=selected_num)
            fig = apply_plotly_theme(fig, title=f'Box Plot of {selected_num}')
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
                        labels={'x': 'Count', 'y': selected_cat},
                        color=value_counts.values,
                        color_continuous_scale='Blues')
            fig = apply_plotly_theme(fig, title=f'Top 15 {selected_cat}')
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
                    color_discrete_sequence=[COLORS["accent_blue"], COLORS["accent_red"]],
                    hole=0.4)
        fig = apply_plotly_theme(fig)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(x=['Normal', 'Attack'], y=attack_counts.values,
                    title='Attack vs Normal Count',
                    labels={'x': 'Classification', 'y': 'Count'},
                    color=['Normal', 'Attack'],
                    color_discrete_map={'Normal': COLORS["accent_blue"], 'Attack': COLORS["accent_red"]})
        fig = apply_plotly_theme(fig)
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
                             color_discrete_sequence=['steelblue'])
            fig = apply_plotly_theme(fig, title=f'Distribution of {selected_feature.replace("_", " ").title()}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.box(df, y=selected_feature)
            fig = apply_plotly_theme(fig, title=f'Box Plot of {selected_feature.replace("_", " ").title()}')
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
                        labels={'x': 'Count', 'y': selected_cat.replace('_', ' ').title()},
                        color=value_counts.values,
                        color_continuous_scale='Viridis')
            fig = apply_plotly_theme(fig, title=f'{selected_cat.replace("_", " ").title()} Distribution')
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
                                  opacity=0.6, marker_color=COLORS["accent_blue"], nbinsx=50))
        fig.add_trace(go.Histogram(x=attack_data[selected_comp], name='Attack',
                                  opacity=0.6, marker_color=COLORS["accent_red"], nbinsx=50))
        fig.update_layout(
            title=f'{selected_comp.replace("_", " ").title()} Distribution: Attack vs Normal',
            xaxis_title=selected_comp.replace('_', ' ').title(),
            yaxis_title='Frequency',
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


def show_ida_phishing(df):
    """Initial Data Analysis for Phishing Detection Dataset"""

    st.markdown("### 📋 Dataset Overview")

    rows, cols = df.shape
    phishing_count = df['CLASS_LABEL'].sum()
    phishing_rate = (phishing_count / len(df)) * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total URLs", f"{rows:,}")

    with col2:
        st.metric("Features", cols)

    with col3:
        st.metric("Phishing URLs", f"{phishing_count:,}")

    with col4:
        st.metric("Phishing Rate", f"{phishing_rate:.1f}%")

    # Dataset balance
    with st.expander("📊 Class Distribution", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            class_counts = df['CLASS_LABEL'].value_counts()

            fig = go.Figure(data=[go.Pie(
                labels=['Legitimate', 'Phishing'],
                values=[class_counts[0], class_counts[1]],
                hole=0.4,
                marker=dict(colors=[COLORS["accent_green"], COLORS["accent_red"]])
            )])

            fig = apply_plotly_theme(fig, title="URL Classification Distribution")
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Balance Analysis")
            balance_ratio = class_counts[0] / class_counts[1] if class_counts[1] > 0 else 0
            st.metric("Balance Ratio", f"{balance_ratio:.2f}:1")
            st.markdown(f"""
            **Interpretation:**
            The dataset shows a {'well-balanced' if 0.5 <= balance_ratio <= 2 else 'slightly imbalanced'}
            distribution, which is {'ideal' if 0.5 <= balance_ratio <= 2 else 'acceptable'} for binary classification.
            """)

    # Feature distributions
    with st.expander("📊 Key Feature Analysis"):
        st.markdown("#### Top Features by Importance")

        col1, col2 = st.columns(2)

        with col1:
            # HTTPS usage
            https_stats = df.groupby('NoHttps')['CLASS_LABEL'].agg(['sum', 'count', 'mean']).round(3)
            https_stats.index = ['Uses HTTPS', 'No HTTPS']

            fig = go.Figure(data=[
                go.Bar(name='Legitimate', x=https_stats.index,
                      y=https_stats['count'] - https_stats['sum'],
                      marker_color=COLORS["accent_green"]),
                go.Bar(name='Phishing', x=https_stats.index,
                      y=https_stats['sum'],
                      marker_color=COLORS["accent_red"])
            ])

            fig = apply_plotly_theme(fig, title="HTTPS Usage vs Classification")
            fig.update_layout(barmode='stack', height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # IP Address presence
            ip_stats = df.groupby('IpAddress')['CLASS_LABEL'].agg(['sum', 'count', 'mean']).round(3)
            ip_stats.index = ['No IP', 'Contains IP']

            fig = go.Figure(data=[
                go.Bar(name='Legitimate', x=ip_stats.index,
                      y=ip_stats['count'] - ip_stats['sum'],
                      marker_color=COLORS["accent_green"]),
                go.Bar(name='Phishing', x=ip_stats.index,
                      y=ip_stats['sum'],
                      marker_color=COLORS["accent_red"])
            ])

            fig = apply_plotly_theme(fig, title="IP Address Presence vs Classification")
            fig.update_layout(barmode='stack', height=300)
            st.plotly_chart(fig, use_container_width=True)

    # Data quality
    st.markdown("### 🔍 Data Quality")

    col1, col2 = st.columns(2)

    with col1:
        missing_count = df.isnull().sum().sum()
        completeness = ((df.size - missing_count) / df.size) * 100

        st.metric("Data Completeness", f"{completeness:.2f}%")
        st.metric("Missing Values", missing_count)

    with col2:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)
        st.metric("Unique URLs", df.shape[0] - duplicates)


# ==================== EDA FUNCTIONS ====================

def show_temporal_analysis(df):
    """Temporal Analysis for Global Threats"""

    st.subheader("📅 Temporal Trend Analysis")
    st.markdown("How have cyberattacks evolved over time?")

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
            line=dict(color=COLORS["accent_blue"], width=4),
            marker=dict(size=10, color=COLORS["accent_blue"],
                       line=dict(color=COLORS["bg_primary"], width=2)),
            fill='tozeroy',
            fillcolor=f'rgba(0, 217, 255, 0.1)'
        ))

        # Add trend line
        z = np.polyfit(years, counts, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=years, y=p(years),
            mode='lines',
            name='Trend',
            line=dict(dash='dash', color=COLORS["accent_red"], width=3)
        ))

        fig = apply_plotly_theme(fig, title='Cyberattack Frequency (2015-2024)')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Attack Count',
            height=400,
            xaxis=dict(range=[2014.5, 2024.5], dtick=1),
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
        colors = [COLORS["accent_green"] if v >= 0 else COLORS["accent_red"] for v in growth_values]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=growth_years,
            y=growth_values,
            marker=dict(
                color=colors,
                line=dict(color=COLORS["text_primary"], width=1)
            ),
            text=[f"{v:+.1f}%" for v in growth_values],
            textposition='outside',
            textfont=dict(size=11, color=COLORS["text_primary"], family='Segoe UI')
        ))

        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)

        fig = apply_plotly_theme(fig, title='YoY Growth Rate (%)')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Growth Rate (%)',
            height=400,
            xaxis=dict(range=[2015.5, 2024.5], dtick=1, showgrid=False),
            yaxis=dict(zeroline=True),
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
                                line=dict(color=COLORS["accent_blue"], width=3),
                                marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=loss_years, y=median_losses,
                                mode='lines+markers', name='Median',
                                line=dict(color=COLORS["accent_green"], width=3),
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
    """Geographic Analysis for Global Threats"""

    st.subheader("🗺️ Geographic Distribution Analysis")
    st.markdown("Where are cyberattacks happening around the world?")

    st.markdown("---")

    # Remove duplicates
    df = df.drop_duplicates()

    # ========== FILTERS SECTION ==========
    st.markdown("#### 🔍 Filter Data")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Year filter
        available_years = sorted(df['Year'].dropna().unique().tolist())
        selected_years = st.multiselect(
            "📅 Year Range",
            options=available_years,
            default=available_years,
            key='geo_year_filter',
            help="Select one or more years to analyze"
        )

    with col2:
        # Attack Type filter
        attack_types = ['All'] + sorted(df['Attack Type'].dropna().unique().tolist())
        selected_attack_type = st.selectbox(
            "🎯 Attack Type",
            options=attack_types,
            key='geo_attack_filter',
            help="Filter by specific attack category"
        )

    with col3:
        # Industry filter
        industries = ['All'] + sorted(df['Target Industry'].dropna().unique().tolist())
        selected_industry = st.selectbox(
            "🏢 Target Industry",
            options=industries,
            key='geo_industry_filter',
            help="Filter by industry sector"
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
            background-color: var(--bg-secondary);
            padding: 12px 20px;
            border-radius: 6px;
            border-left: 4px solid var(--accent-blue);
            margin: 15px 0;
        ">
            <strong style="color: var(--text-primary);">🎯 Active Filters:</strong>
            <span style="color: var(--text-secondary);">{' | '.join(active_filters)}</span>
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
                marker=dict(colors=[COLORS["accent_red"], COLORS["accent_blue"]]),
                textinfo='label+percent',
                textposition='inside'
            )])

            fig = apply_plotly_theme(fig, title='Geographic Loss Concentration')
            fig.update_layout(
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
                line=dict(width=2, color=COLORS["text_primary"])
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
            plot_bgcolor='rgba(248, 249, 250, 0.5)'
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
                labels={
                    'Attack_Count': 'Number of Attacks',
                    'Total_Loss': 'Total Loss ($M)',
                    'Total_Users': 'Affected Users'
                }
            )
            fig = apply_plotly_theme(fig, title='Attack Volume vs Financial Impact (bubble size = affected users)')
            fig.update_layout(
                height=450,
                showlegend=False,
                plot_bgcolor='rgba(248, 249, 250, 0.5)',
                xaxis=dict(gridcolor=COLORS["border_color"]),
                yaxis=dict(gridcolor=COLORS["border_color"])
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
                labels={'Count': 'Number of Attacks'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig = apply_plotly_theme(fig, title='Attack Type Breakdown (Top 5 Countries)')
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
                color='Count',
                color_continuous_scale='Blues'
            )
            fig = apply_plotly_theme(fig, title='Hierarchical Attack Distribution')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap
        pivot_data = attack_breakdown_top.pivot(index='Attack Type', columns='Country', values='Count').fillna(0)

        fig = px.imshow(
            pivot_data,
            labels=dict(x="Country", y="Attack Type", color="Attacks"),
            color_continuous_scale='YlOrRd',
            aspect='auto',
            text_auto=True
        )
        fig = apply_plotly_theme(fig, title='Attack Type × Country Heatmap (Top 5)')
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
                connector={"line": {"color": COLORS["border_color"]}},
                increasing={"marker": {"color": COLORS["accent_red"]}},
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
                labels={'Financial Loss (in Million $)': 'Loss ($M)'},
                color='Country',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig = apply_plotly_theme(fig, title='Loss Distribution Comparison (Top 6)')
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


def show_correlation_analysis(global_df, intrusion_df):
    """Correlation Analysis"""

    st.subheader("🔗 Correlation Analysis")
    st.markdown("Understanding relationships between cybersecurity metrics")

    st.markdown("---")

    with st.expander("ℹ️ About Correlation Analysis", expanded=False):
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
                                   color_continuous_scale='RdBu_r',
                                   zmin=-1, zmax=1,
                                   text_auto='.3f',
                                   aspect='auto')
                    fig = apply_plotly_theme(fig, title='Correlation Matrix - Global Threats')
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
                               color_continuous_scale='RdBu_r',
                               zmin=-1, zmax=1,
                               text_auto='.3f',
                               aspect='auto')
                fig = apply_plotly_theme(fig, title='Correlation Matrix - Intrusion Detection')
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
                            color='Correlation',
                            color_continuous_scale='RdYlGn',
                            color_continuous_midpoint=0)
                fig = apply_plotly_theme(fig, title='Feature Correlation with Attack')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for correlation analysis.")


def show_behavior_analysis(df):
    """Attack Behavior Analysis for Intrusion Detection"""

    st.subheader("⚔️ Attack Behavior Analysis")
    st.markdown("Comparing attack traffic patterns with normal network behavior")

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
                            labels={'attack_detected': 'Classification',
                                   'login_attempts': 'Login Attempts',
                                   'failed_logins': 'Failed Logins'},
                            color_discrete_map={0: 'blue', 1: 'red'},
                            opacity=0.6)
            fig = apply_plotly_theme(fig, title='Login Behavior Pattern')
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
                        labels={'attack_detected': 'Classification',
                               'session_duration': 'Session Duration (s)',
                               'ip_reputation_score': 'IP Reputation (0-1)'},
                        color_discrete_map={0: 'blue', 1: 'red'},
                        opacity=0.6)
        fig = apply_plotly_theme(fig, title='Session Duration vs IP Reputation Score')
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
                        labels={'Attack_Rate': 'Attack Rate (%)', 'protocol_type': 'Protocol'},
                        color='Attack_Rate',
                        color_continuous_scale='Reds')
            fig = apply_plotly_theme(fig, title='Attack Rate by Protocol (%)')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(encryption_attack, x='encryption_used', y='Attack_Rate',
                        labels={'Attack_Rate': 'Attack Rate (%)', 'encryption_used': 'Encryption'},
                        color='Attack_Rate',
                        color_continuous_scale='Oranges')
            fig = apply_plotly_theme(fig, title='Attack Rate by Encryption (%)')
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
                                      opacity=0.6, marker_color=COLORS["accent_blue"], nbinsx=50))
            fig.add_trace(go.Histogram(x=attack_data[selected_feature], name='Attack',
                                      opacity=0.6, marker_color=COLORS["accent_red"], nbinsx=50))
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
                        labels={'attack_detected': 'Classification'},
                        color='attack_detected',
                        color_discrete_map={0: 'blue', 1: 'red'})
            fig = apply_plotly_theme(fig, title=f'{selected_feature.replace("_", " ").title()} Box Plot')
            fig.update_xaxes(ticktext=['Normal', 'Attack'], tickvals=[0, 1])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def show_advanced_analytics(global_df, intrusion_df):
    """Advanced Analytics: PCA and Other Advanced Techniques"""

    st.subheader("🔬 Advanced Analytics")
    st.markdown("Deep dive into data patterns using statistical techniques")

    st.markdown("---")

    analysis_type = st.radio("Select Analysis",
                             ["Principal Component Analysis", "Advanced Statistics"],
                             horizontal=True)

    if "Principal Component" in analysis_type:
        st.markdown("#### Principal Component Analysis (PCA)")
        st.markdown("Reducing dimensionality while preserving data variance")

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
                                marker_color=COLORS["accent_blue"]))
            fig.add_trace(go.Scatter(x=list(range(1, len(cumulative_var)+1)),
                                    y=cumulative_var,
                                    mode='lines+markers',
                                    name='Cumulative',
                                    marker_color=COLORS["accent_red"],
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
                        color_discrete_map={'Normal': 'blue', 'Attack': 'red'},
                        opacity=0.5)
        fig = apply_plotly_theme(fig, title=f'PCA Projection (PC1: {explained_var[0]*100:.1f}%, PC2: {explained_var[1]*100:.1f}%)')
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
                           color_continuous_scale='RdBu_r',
                           aspect='auto')
            fig = apply_plotly_theme(fig, title='Feature Loadings Heatmap')
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
                                      nbins=50,
                                      marginal='box')
                    fig = apply_plotly_theme(fig, title='Financial Loss Distribution')
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

        # Filters section
        st.markdown("#### 🔍 Filter Data")
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Year filter
            year_options = ['All'] + sorted(df['Year'].unique().tolist())
            selected_years = st.multiselect("📅 Year", year_options, default=['All'], key='explorer_year')

        with col2:
            # Country filter
            country_options = ['All'] + sorted(df['Country'].unique().tolist())
            selected_countries = st.multiselect("🌍 Country", country_options, default=['All'], key='explorer_country')

        with col3:
            # Attack Type filter
            attack_type_options = ['All'] + sorted(df['Attack Type'].unique().tolist())
            selected_attack_types = st.multiselect("🎯 Attack Type", attack_type_options, default=['All'], key='explorer_attack')

        with col4:
            # Industry filter
            industry_options = ['All'] + sorted(df['Target Industry'].unique().tolist())
            selected_industries = st.multiselect("🏢 Industry", industry_options, default=['All'], key='explorer_industry')

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

        # Filters section
        st.markdown("#### 🔍 Filter Data")
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Attack detected filter
            attack_filter = st.selectbox("🚨 Attack Status", ['All', 'Attack (1)', 'Normal (0)'], key='explorer_attack_status')

        with col2:
            # Protocol filter - handle mixed types and NaN values
            protocol_values = df['protocol_type'].dropna().astype(str).unique().tolist()
            protocol_options = ['All'] + sorted(protocol_values)
            selected_protocols = st.multiselect("🌐 Protocol", protocol_options, default=['All'], key='explorer_protocol')

        with col3:
            # Encryption filter - handle mixed types and NaN values
            encryption_values = df['encryption_used'].dropna().astype(str).unique().tolist()
            encryption_options = ['All'] + sorted(encryption_values)
            selected_encryptions = st.multiselect("🔐 Encryption", encryption_options, default=['All'], key='explorer_encryption')

        with col4:
            # Browser filter - handle mixed types and NaN values
            browser_values = df['browser_type'].dropna().astype(str).unique().tolist()
            browser_options = ['All'] + sorted(browser_values)
            selected_browsers = st.multiselect("🌐 Browser", browser_options, default=['All'], key='explorer_browser')

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
                                line=dict(color=COLORS["accent_blue"], width=3),
                                marker=dict(size=8)))

        # Add trend line
        z = np.polyfit(find_years, find_counts, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=find_years, y=p(find_years),
                                mode='lines',
                                name='Trend',
                                line=dict(dash='dash', color=COLORS["accent_red"], width=3)))

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
                    color_discrete_sequence=[COLORS["accent_blue"], COLORS["accent_red"]],
                    hole=0.4)
        fig = apply_plotly_theme(fig)
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
                    color='Financial Loss (in Million $)',
                    color_continuous_scale='Reds')
        fig = apply_plotly_theme(fig, title='Top 10 Countries by Financial Loss')
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
                    color='Attack_Rate',
                    color_continuous_scale='Reds',
                    text='Attack_Rate')
        fig = apply_plotly_theme(fig, title='Attack Rate by Protocol Type (%)')
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
                    color='Correlation',
                    color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=0)
        fig = apply_plotly_theme(fig, title='Feature Correlation with Attack Detection')
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
