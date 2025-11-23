"""
CVE (Common Vulnerabilities and Exposures) Intelligence Module
ML Task: Severity Prediction & Vulnerability Classification
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from modules.theme import get_chart_theme

def show(df):
    """Display CVE vulnerability intelligence and ML-ready visualizations"""

    st.title("🔐 CVE Intelligence Dashboard")
    st.markdown("""
    <div style="padding: 16px; background: linear-gradient(135deg, rgba(138, 43, 226, 0.1) 0%, rgba(75, 0, 130, 0.1) 100%);
                border-left: 4px solid #8A2BE2; border-radius: 8px; margin-bottom: 24px;">
        <p style="margin: 0; color: #A0A7B8; font-size: 0.95rem;">
            <strong style="color: #8A2BE2;">ML Task:</strong> Multi-class Classification (Severity Prediction) |
            <strong style="color: #8A2BE2;">Target:</strong> severity |
            <strong style="color: #8A2BE2;">Features:</strong> CVSS Scores + Metadata
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_cves = len(df)
    critical_count = len(df[df['severity'] == 'CRITICAL'])
    high_count = len(df[df['severity'] == 'HIGH'])
    avg_cvss = df['cvss_base_score'].mean()

    with col1:
        st.metric("Total CVEs", f"{total_cves:,}")
    with col2:
        st.metric("Critical Vulnerabilities", f"{critical_count:,}", delta=f"{(critical_count/total_cves)*100:.1f}%")
    with col3:
        st.metric("High Severity", f"{high_count:,}")
    with col4:
        st.metric("Avg CVSS Score", f"{avg_cvss:.1f}/10.0")

    st.markdown("---")

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview & Trends",
        "🎯 Severity Analysis",
        "🏢 Vendor & Product Analysis",
        "🤖 ML Preparation"
    ])

    with tab1:
        st.subheader("Vulnerability Overview")

        col1, col2 = st.columns(2)

        with col1:
            # Severity distribution
            severity_order = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            severity_colors = {
                'LOW': '#00D9FF',
                'MEDIUM': '#FFD700',
                'HIGH': '#FFA500',
                'CRITICAL': '#FF4B4B'
            }

            severity_dist = df['severity'].value_counts().reindex(severity_order).reset_index()
            severity_dist.columns = ['Severity', 'Count']

            fig_severity = px.pie(
                severity_dist,
                values='Count',
                names='Severity',
                title='Vulnerability Severity Distribution',
                color='Severity',
                color_discrete_map=severity_colors,
                hole=0.4
            )
            fig_severity.update_layout(**get_chart_theme())
            st.plotly_chart(fig_severity, use_container_width=True)

        with col2:
            # Vulnerability type distribution
            vuln_types = df['vulnerability_type'].value_counts().head(10).reset_index()
            vuln_types.columns = ['Vulnerability Type', 'Count']

            fig_types = px.bar(
                vuln_types,
                x='Count',
                y='Vulnerability Type',
                orientation='h',
                title='Top 10 Vulnerability Types',
                color='Count',
                color_continuous_scale='Purples'
            )
            fig_types.update_layout(**get_chart_theme())
            st.plotly_chart(fig_types, use_container_width=True)

        # Temporal trends
        st.subheader("Vulnerability Trends Over Time")

        # CVEs by year
        yearly_cves = df.groupby('year').size().reset_index(name='count')

        fig_yearly = px.line(
            yearly_cves,
            x='year',
            y='count',
            title='CVE Publications by Year',
            markers=True
        )
        fig_yearly.update_layout(**get_chart_theme())
        fig_yearly.update_traces(line_color='#8A2BE2', marker=dict(size=10))
        st.plotly_chart(fig_yearly, use_container_width=True)

        # Severity by year
        severity_by_year = df.groupby(['year', 'severity']).size().reset_index(name='count')

        fig_severity_year = px.bar(
            severity_by_year,
            x='year',
            y='count',
            color='severity',
            title='Vulnerability Severity Trends by Year',
            color_discrete_map=severity_colors,
            barmode='stack'
        )
        fig_severity_year.update_layout(**get_chart_theme())
        st.plotly_chart(fig_severity_year, use_container_width=True)

    with tab2:
        st.subheader("CVSS Score Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # CVSS score distribution
            fig_cvss_dist = px.histogram(
                df,
                x='cvss_base_score',
                nbins=30,
                title='CVSS Base Score Distribution',
                color_discrete_sequence=['#8A2BE2']
            )
            fig_cvss_dist.update_layout(**get_chart_theme())
            st.plotly_chart(fig_cvss_dist, use_container_width=True)

        with col2:
            # Exploitability vs Impact
            fig_scatter = px.scatter(
                df,
                x='exploitability_score',
                y='impact_score',
                color='severity',
                title='Exploitability vs Impact Score',
                color_discrete_map=severity_colors,
                opacity=0.6
            )
            fig_scatter.update_layout(**get_chart_theme())
            st.plotly_chart(fig_scatter, use_container_width=True)

        # CVSS by vulnerability type
        st.subheader("CVSS Scores by Vulnerability Type")

        top_vuln_types = df['vulnerability_type'].value_counts().head(8).index
        df_top_vulns = df[df['vulnerability_type'].isin(top_vuln_types)]

        fig_cvss_type = px.box(
            df_top_vulns,
            x='vulnerability_type',
            y='cvss_base_score',
            color='vulnerability_type',
            title='CVSS Score Distribution by Vulnerability Type'
        )
        fig_cvss_type.update_layout(**get_chart_theme(), showlegend=False)
        fig_cvss_type.update_xaxes(tickangle=45)
        st.plotly_chart(fig_cvss_type, use_container_width=True)

        # Exploit analysis
        st.subheader("Exploit Availability Analysis")

        col1, col2 = st.columns(2)

        with col1:
            exploit_data = df.groupby(['severity', 'has_exploit']).size().reset_index(name='count')
            exploit_data['Exploit'] = exploit_data['has_exploit'].map({True: 'Has Exploit', False: 'No Exploit'})

            fig_exploit = px.bar(
                exploit_data,
                x='severity',
                y='count',
                color='Exploit',
                title='Exploit Availability by Severity',
                barmode='group',
                color_discrete_map={'Has Exploit': '#FF4B4B', 'No Exploit': '#00D9FF'},
                category_orders={'severity': severity_order}
            )
            fig_exploit.update_layout(**get_chart_theme())
            st.plotly_chart(fig_exploit, use_container_width=True)

        with col2:
            public_exploit = df.groupby(['severity', 'exploit_public']).size().reset_index(name='count')
            public_exploit['Public'] = public_exploit['exploit_public'].map({True: 'Public Exploit', False: 'Not Public'})

            fig_public = px.bar(
                public_exploit,
                x='severity',
                y='count',
                color='Public',
                title='Public Exploit Availability',
                barmode='group',
                color_discrete_map={'Public Exploit': '#FF4B4B', 'Not Public': '#8A2BE2'},
                category_orders={'severity': severity_order}
            )
            fig_public.update_layout(**get_chart_theme())
            st.plotly_chart(fig_public, use_container_width=True)

        # Exploit percentage by severity
        exploit_pct = df.groupby('severity').agg({
            'has_exploit': lambda x: (x.sum() / len(x)) * 100,
            'exploit_public': lambda x: (x.sum() / len(x)) * 100
        }).reset_index()
        exploit_pct.columns = ['Severity', 'Has Exploit (%)', 'Public Exploit (%)']

        st.dataframe(
            exploit_pct.style.format({
                'Has Exploit (%)': '{:.1f}%',
                'Public Exploit (%)': '{:.1f}%'
            }).background_gradient(cmap='Reds', subset=['Has Exploit (%)', 'Public Exploit (%)']),
            use_container_width=True
        )

    with tab3:
        st.subheader("Vendor & Product Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Top vendors
            vendor_counts = df['vendor'].value_counts().head(10).reset_index()
            vendor_counts.columns = ['Vendor', 'CVE Count']

            fig_vendors = px.bar(
                vendor_counts,
                x='CVE Count',
                y='Vendor',
                orientation='h',
                title='Top 10 Vendors by CVE Count',
                color='CVE Count',
                color_continuous_scale='Purples'
            )
            fig_vendors.update_layout(**get_chart_theme())
            st.plotly_chart(fig_vendors, use_container_width=True)

        with col2:
            # Top products
            product_counts = df['product'].value_counts().head(10).reset_index()
            product_counts.columns = ['Product', 'CVE Count']

            fig_products = px.bar(
                product_counts,
                x='CVE Count',
                y='Product',
                orientation='h',
                title='Top 10 Products by CVE Count',
                color='CVE Count',
                color_continuous_scale='Blues'
            )
            fig_products.update_layout(**get_chart_theme())
            st.plotly_chart(fig_products, use_container_width=True)

        # Vendor severity heatmap
        st.subheader("Vendor Severity Heatmap")

        top_vendors = df['vendor'].value_counts().head(10).index
        vendor_severity = df[df['vendor'].isin(top_vendors)].groupby(['vendor', 'severity']).size().reset_index(name='count')
        vendor_severity_pivot = vendor_severity.pivot(index='vendor', columns='severity', values='count').fillna(0)
        vendor_severity_pivot = vendor_severity_pivot[severity_order]

        fig_heatmap = px.imshow(
            vendor_severity_pivot,
            title='Vulnerability Severity by Top Vendors',
            color_continuous_scale='Reds',
            aspect='auto',
            labels=dict(x="Severity", y="Vendor", color="Count")
        )
        fig_heatmap.update_layout(**get_chart_theme())
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Patch availability
        st.subheader("Patch Availability Analysis")

        col1, col2 = st.columns(2)

        with col1:
            patch_dist = df['patch_available'].value_counts().reset_index()
            patch_dist.columns = ['Status', 'Count']
            patch_dist['Status'] = patch_dist['Status'].map({True: 'Patch Available', False: 'No Patch'})

            fig_patch = px.pie(
                patch_dist,
                values='Count',
                names='Status',
                title='Patch Availability',
                color='Status',
                color_discrete_map={'Patch Available': '#00FFB3', 'No Patch': '#FF4B4B'},
                hole=0.4
            )
            fig_patch.update_layout(**get_chart_theme())
            st.plotly_chart(fig_patch, use_container_width=True)

        with col2:
            # Days to patch distribution
            df_patched = df[df['patch_available'] == True]

            fig_days = px.histogram(
                df_patched,
                x='days_to_patch',
                nbins=30,
                title='Days to Patch Distribution',
                color_discrete_sequence=['#8A2BE2']
            )
            fig_days.update_layout(**get_chart_theme())
            st.plotly_chart(fig_days, use_container_width=True)

        # Average days to patch by severity
        patch_time = df[df['patch_available'] == True].groupby('severity')['days_to_patch'].mean().reindex(severity_order).reset_index()
        patch_time.columns = ['Severity', 'Avg Days to Patch']

        fig_patch_time = px.bar(
            patch_time,
            x='Severity',
            y='Avg Days to Patch',
            title='Average Patch Time by Severity',
            color='Severity',
            color_discrete_map=severity_colors
        )
        fig_patch_time.update_layout(**get_chart_theme())
        st.plotly_chart(fig_patch_time, use_container_width=True)

    with tab4:
        st.subheader("🤖 Machine Learning Preparation")

        st.markdown("""
        <div style="padding: 16px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 255, 179, 0.1) 100%);
                    border-left: 4px solid #00D9FF; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #00D9FF;">Dataset Ready for ML Training</h4>
            <p style="margin-bottom: 0; color: #A0A7B8;">
                This dataset supports both classification (severity prediction) and regression (CVSS score prediction).
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Dataset statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Features", len(df.columns) - 1)  # Exclude cve_id
            st.caption("Available for training")

        with col2:
            st.metric("Classification Target", "severity")
            st.caption("4 classes: LOW/MEDIUM/HIGH/CRITICAL")

        with col3:
            st.metric("Regression Target", "cvss_base_score")
            st.caption("Range: 0.0 - 10.0")

        # Feature types breakdown
        st.markdown("#### Feature Types")

        feature_types = {
            'Numeric Features': ['year', 'affected_versions', 'cvss_base_score', 'exploitability_score',
                                'impact_score', 'days_to_patch', 'references_count'],
            'Boolean Features': ['has_exploit', 'exploit_public', 'patch_available'],
            'Categorical Features': ['vulnerability_type', 'vendor', 'product', 'severity', 'cwe_id'],
            'Date Features': ['published_date']
        }

        for feat_type, features in feature_types.items():
            with st.expander(f"{feat_type} ({len(features)} features)"):
                st.write(", ".join(features))

        # Class distribution
        st.markdown("#### Severity Class Distribution")

        class_dist = df['severity'].value_counts().reindex(severity_order)
        st.bar_chart(class_dist)

        # ML Pipeline recommendation
        st.markdown("#### Recommended ML Pipeline")

        pipeline_code = """
# Example ML Pipeline for CVE Severity Prediction

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Load data
df = pd.read_csv('data/cve_vulnerability_dataset.csv')

# Prepare features
features = ['cvss_base_score', 'exploitability_score', 'impact_score',
            'has_exploit', 'exploit_public', 'patch_available',
            'days_to_patch', 'references_count', 'affected_versions']

# Handle missing values (days_to_patch)
df['days_to_patch'].fillna(df['days_to_patch'].median(), inplace=True)

X = df[features]
y = df['severity']

# Encode target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Convert boolean to int
bool_cols = ['has_exploit', 'exploit_public', 'patch_available']
X[bool_cols] = X[bool_cols].astype(int)

# Split data (stratified for balanced classes)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Scale numeric features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest Classifier
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    class_weight='balanced'
)
clf.fit(X_train_scaled, y_train)

# Evaluate
y_pred = clf.predict(X_test_scaled)

print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': clf.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance)

# For CVSS Score Regression:
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

y_cvss = df['cvss_base_score']
# ... similar preprocessing
regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train_scaled, y_train_cvss)
predictions = regressor.predict(X_test_scaled)
print(f"RMSE: {np.sqrt(mean_squared_error(y_test_cvss, predictions)):.2f}")
print(f"R²: {r2_score(y_test_cvss, predictions):.3f}")
"""

        st.code(pipeline_code, language='python')

        # Download prepared data
        st.markdown("#### Download Dataset")

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CVE Dataset (CSV)",
            data=csv,
            file_name="cve_vulnerability_ml_ready.csv",
            mime="text/csv"
        )

        # Advanced ML techniques
        with st.expander("💡 Advanced ML Techniques for CVE Analysis"):
            st.markdown("""
            **Multi-Task Learning:**
            - Simultaneously predict severity AND CVSS score
            - Share representations between related tasks
            - Improve generalization

            **Feature Engineering:**
            - **Temporal features**: Days since publication, time to patch
            - **Vendor encoding**: One-hot or target encoding for vendors
            - **CWE grouping**: Group CWE IDs into categories
            - **Exploit features**: Combine has_exploit + exploit_public

            **Class Imbalance Handling:**
            - CRITICAL class is underrepresented (10%)
            - Use SMOTE or class weights
            - Consider cost-sensitive learning (higher cost for missing CRITICAL)

            **Model Ensembles:**
            - Combine Random Forest + Gradient Boosting + XGBoost
            - Voting or stacking for better performance

            **Real-world Applications:**
            - **Prioritization**: Help security teams prioritize patching
            - **Risk scoring**: Predict exploitation likelihood
            - **Alert systems**: Flag critical vulnerabilities automatically
            - **Trend analysis**: Predict future vulnerability patterns
            """)
