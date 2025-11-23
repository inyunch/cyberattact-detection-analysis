"""
Phishing Detection Analysis Module
ML Task: Binary Classification (Phishing vs Legitimate)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from modules.theme import get_chart_theme

def show(df):
    """Display phishing detection analysis and ML-ready visualizations"""

    st.title("🎣 Phishing Detection Analysis")
    st.markdown("""
    <div style="padding: 16px; background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(255, 215, 0, 0.1) 100%);
                border-left: 4px solid #FFA500; border-radius: 8px; margin-bottom: 24px;">
        <p style="margin: 0; color: #A0A7B8; font-size: 0.95rem;">
            <strong style="color: #FFA500;">ML Task:</strong> Binary Classification |
            <strong style="color: #FFA500;">Target:</strong> is_phishing |
            <strong style="color: #FFA500;">Features:</strong> URL + Content + Security Indicators
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_urls = len(df)
    phishing_count = df['is_phishing'].sum()
    legitimate_count = total_urls - phishing_count
    phishing_rate = (phishing_count / total_urls) * 100

    with col1:
        st.metric("Total URLs Analyzed", f"{total_urls:,}")
    with col2:
        st.metric("Phishing URLs", f"{phishing_count:,}", delta=f"{phishing_rate:.1f}%", delta_color="inverse")
    with col3:
        st.metric("Legitimate URLs", f"{legitimate_count:,}")
    with col4:
        avg_reports = df[df['is_phishing'] == 1]['reported_phishing_count'].mean()
        st.metric("Avg Reports/Phishing", f"{avg_reports:.0f}")

    st.markdown("---")

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview & Distribution",
        "🔗 URL Features",
        "🔒 Security Analysis",
        "🤖 ML Preparation"
    ])

    with tab1:
        st.subheader("Dataset Overview")

        col1, col2 = st.columns(2)

        with col1:
            # Class distribution
            class_dist = df['is_phishing'].value_counts().reset_index()
            class_dist.columns = ['Class', 'Count']
            class_dist['Class'] = class_dist['Class'].map({1: 'Phishing', 0: 'Legitimate'})

            fig_class = px.pie(
                class_dist,
                values='Count',
                names='Class',
                title='URL Classification Distribution',
                color='Class',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'},
                hole=0.4
            )
            fig_class.update_layout(**get_chart_theme())
            st.plotly_chart(fig_class, use_container_width=True)

        with col2:
            # HTTPS usage
            https_dist = df.groupby(['has_https', 'is_phishing']).size().reset_index(name='count')
            https_dist['HTTPS'] = https_dist['has_https'].map({True: 'HTTPS', False: 'HTTP'})
            https_dist['Class'] = https_dist['is_phishing'].map({1: 'Phishing', 0: 'Legitimate'})

            fig_https = px.bar(
                https_dist,
                x='HTTPS',
                y='count',
                color='Class',
                title='HTTPS Usage by Class',
                barmode='group',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_https.update_layout(**get_chart_theme())
            st.plotly_chart(fig_https, use_container_width=True)

        # Top suspicious domains
        st.subheader("Most Reported Domains")

        top_reported = df[df['is_phishing'] == 1].nlargest(10, 'reported_phishing_count')[
            ['domain', 'reported_phishing_count', 'url_length']
        ]
        top_reported.columns = ['Domain', 'Reports', 'URL Length']

        fig_reported = px.bar(
            top_reported,
            x='Reports',
            y='Domain',
            orientation='h',
            title='Top 10 Most Reported Phishing Domains',
            color='Reports',
            color_continuous_scale='Oranges'
        )
        fig_reported.update_layout(**get_chart_theme())
        st.plotly_chart(fig_reported, use_container_width=True)

    with tab2:
        st.subheader("URL Feature Analysis")

        # URL length distribution
        df_plot = df.copy()
        df_plot['Class'] = df_plot['is_phishing'].map({1: 'Phishing', 0: 'Legitimate'})

        col1, col2 = st.columns(2)

        with col1:
            fig_url_len = px.histogram(
                df_plot,
                x='url_length',
                color='Class',
                title='URL Length Distribution',
                nbins=50,
                barmode='overlay',
                opacity=0.7,
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_url_len.update_layout(**get_chart_theme())
            st.plotly_chart(fig_url_len, use_container_width=True)

        with col2:
            fig_special = px.box(
                df_plot,
                x='Class',
                y='special_characters',
                color='Class',
                title='Special Characters Count',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_special.update_layout(**get_chart_theme())
            st.plotly_chart(fig_special, use_container_width=True)

        # Domain age vs URL length
        st.subheader("Domain Age Analysis")

        fig_scatter = px.scatter(
            df_plot,
            x='domain_age_days',
            y='url_length',
            color='Class',
            title='Domain Age vs URL Length',
            opacity=0.6,
            color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'},
            hover_data=['domain']
        )
        fig_scatter.update_layout(**get_chart_theme())
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Subdomain analysis
        col1, col2 = st.columns(2)

        with col1:
            fig_subdomain = px.violin(
                df_plot,
                x='Class',
                y='subdomain_count',
                color='Class',
                title='Subdomain Count Distribution',
                box=True,
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_subdomain.update_layout(**get_chart_theme())
            st.plotly_chart(fig_subdomain, use_container_width=True)

        with col2:
            fig_redirects = px.violin(
                df_plot,
                x='Class',
                y='redirects_count',
                color='Class',
                title='Redirects Count Distribution',
                box=True,
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_redirects.update_layout(**get_chart_theme())
            st.plotly_chart(fig_redirects, use_container_width=True)

    with tab3:
        st.subheader("Security Indicators Analysis")

        # SSL validation
        col1, col2 = st.columns(2)

        with col1:
            ssl_dist = df.groupby(['ssl_valid', 'is_phishing']).size().reset_index(name='count')
            ssl_dist['SSL Status'] = ssl_dist['ssl_valid'].map({True: 'Valid SSL', False: 'Invalid/No SSL'})
            ssl_dist['Class'] = ssl_dist['is_phishing'].map({1: 'Phishing', 0: 'Legitimate'})

            fig_ssl = px.bar(
                ssl_dist,
                x='SSL Status',
                y='count',
                color='Class',
                title='SSL Certificate Status',
                barmode='group',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_ssl.update_layout(**get_chart_theme())
            st.plotly_chart(fig_ssl, use_container_width=True)

        with col2:
            dns_dist = df.groupby(['dns_record_exists', 'is_phishing']).size().reset_index(name='count')
            dns_dist['DNS Status'] = dns_dist['dns_record_exists'].map({True: 'DNS Exists', False: 'No DNS'})
            dns_dist['Class'] = dns_dist['is_phishing'].map({1: 'Phishing', 0: 'Legitimate'})

            fig_dns = px.bar(
                dns_dist,
                x='DNS Status',
                y='count',
                color='Class',
                title='DNS Record Status',
                barmode='group',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_dns.update_layout(**get_chart_theme())
            st.plotly_chart(fig_dns, use_container_width=True)

        # Security indicator prevalence
        st.subheader("Suspicious Indicators Prevalence")

        bool_features = ['popup_windows', 'iframe_usage', 'favicon_different_domain']

        phishing_df = df[df['is_phishing'] == 1]
        legit_df = df[df['is_phishing'] == 0]

        indicator_data = []
        for feature in bool_features:
            phishing_pct = (phishing_df[feature].sum() / len(phishing_df)) * 100
            legit_pct = (legit_df[feature].sum() / len(legit_df)) * 100

            indicator_data.append({
                'Indicator': feature.replace('_', ' ').title(),
                'Phishing': phishing_pct,
                'Legitimate': legit_pct
            })

        indicator_df = pd.DataFrame(indicator_data)

        fig_indicators = go.Figure()
        fig_indicators.add_trace(go.Bar(
            name='Phishing',
            x=indicator_df['Indicator'],
            y=indicator_df['Phishing'],
            marker_color='#FFA500'
        ))
        fig_indicators.add_trace(go.Bar(
            name='Legitimate',
            x=indicator_df['Indicator'],
            y=indicator_df['Legitimate'],
            marker_color='#00D9FF'
        ))

        fig_indicators.update_layout(
            **get_chart_theme(),
            barmode='group',
            title='Suspicious Indicator Prevalence (%)',
            yaxis_title='Percentage'
        )
        st.plotly_chart(fig_indicators, use_container_width=True)

        # Content features analysis
        st.subheader("Content Features")

        col1, col2 = st.columns(2)

        with col1:
            fig_forms = px.box(
                df_plot,
                x='Class',
                y='forms_count',
                color='Class',
                title='Forms Count Distribution',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_forms.update_layout(**get_chart_theme())
            st.plotly_chart(fig_forms, use_container_width=True)

        with col2:
            fig_links = px.box(
                df_plot,
                x='Class',
                y='external_links',
                color='Class',
                title='External Links Distribution',
                color_discrete_map={'Phishing': '#FFA500', 'Legitimate': '#00D9FF'}
            )
            fig_links.update_layout(**get_chart_theme())
            st.plotly_chart(fig_links, use_container_width=True)

        # Feature correlation
        st.subheader("Feature Correlation Matrix")

        correlation_features = ['url_length', 'domain_age_days', 'subdomain_count',
                               'special_characters', 'external_links', 'redirects_count',
                               'suspicious_keywords', 'reported_phishing_count', 'is_phishing']

        corr_matrix = df[correlation_features].corr()

        fig_corr = px.imshow(
            corr_matrix,
            title='Feature Correlation Heatmap',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            aspect='auto'
        )
        fig_corr.update_layout(**get_chart_theme())
        st.plotly_chart(fig_corr, use_container_width=True)

    with tab4:
        st.subheader("🤖 Machine Learning Preparation")

        st.markdown("""
        <div style="padding: 16px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 255, 179, 0.1) 100%);
                    border-left: 4px solid #00D9FF; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #00D9FF;">Dataset Ready for ML Training</h4>
            <p style="margin-bottom: 0; color: #A0A7B8;">
                This dataset is optimized for phishing detection with comprehensive URL and content features.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Dataset statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Features", len(df.columns) - 2)  # Exclude url_id, is_phishing
            st.caption("Available for training")

        with col2:
            st.metric("Target Variable", "is_phishing")
            st.caption("Binary: 0 (Legitimate) / 1 (Phishing)")

        with col3:
            class_ratio = phishing_count / legitimate_count
            st.metric("Class Ratio", f"{class_ratio:.2f}:1")
            st.caption("Phishing:Legitimate")

        # Feature types breakdown
        st.markdown("#### Feature Types")

        feature_types = {
            'Numeric Features': ['url_length', 'domain_age_days', 'subdomain_count',
                                'special_characters', 'external_links', 'forms_count',
                                'redirects_count', 'suspicious_keywords', 'reported_phishing_count'],
            'Boolean Features': ['has_https', 'ssl_valid', 'popup_windows', 'iframe_usage',
                                'favicon_different_domain', 'dns_record_exists'],
            'Categorical Features': ['domain']
        }

        for feat_type, features in feature_types.items():
            with st.expander(f"{feat_type} ({len(features)} features)"):
                st.write(", ".join(features))

        # ML Pipeline recommendation
        st.markdown("#### Recommended ML Pipeline")

        pipeline_code = """
# Example ML Pipeline for Phishing Detection

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# Load data
df = pd.read_csv('data/phishing_detection_dataset.csv')

# Prepare features (exclude url_id and domain for simplicity)
features = ['url_length', 'has_https', 'ssl_valid', 'domain_age_days',
            'subdomain_count', 'special_characters', 'external_links',
            'forms_count', 'popup_windows', 'iframe_usage', 'redirects_count',
            'suspicious_keywords', 'favicon_different_domain',
            'dns_record_exists', 'reported_phishing_count']

X = df[features]
y = df['is_phishing']

# Convert boolean to int
bool_cols = ['has_https', 'ssl_valid', 'popup_windows', 'iframe_usage',
             'favicon_different_domain', 'dns_record_exists']
X[bool_cols] = X[bool_cols].astype(int)

# Split data (stratified for balanced classes)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Scale numeric features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Gradient Boosting Classifier
clf = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
clf.fit(X_train_scaled, y_train)

# Evaluate
y_pred = clf.predict(X_test_scaled)
y_pred_proba = clf.predict_proba(X_test_scaled)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': clf.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance.head(10))
"""

        st.code(pipeline_code, language='python')

        # Download prepared data
        st.markdown("#### Download Dataset")

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Phishing Detection Dataset (CSV)",
            data=csv,
            file_name="phishing_detection_ml_ready.csv",
            mime="text/csv"
        )

        # Best practices
        with st.expander("💡 Best Practices for Phishing Detection"):
            st.markdown("""
            **Key Considerations:**

            1. **Feature Engineering**:
               - Domain reputation scores (if available)
               - Lexical features (character frequency, word count)
               - URL obfuscation indicators

            2. **Model Selection**:
               - **Gradient Boosting** (XGBoost, LightGBM) - Generally best performance
               - **Random Forest** - Good baseline, handles non-linear relationships
               - **Neural Networks** - For deep feature learning

            3. **Evaluation Metrics**:
               - **Precision**: Minimize false positives (legitimate sites blocked)
               - **Recall**: Maximize true positives (catch phishing attempts)
               - **F1-Score**: Balance between precision and recall

            4. **Real-world Deployment**:
               - Regular model retraining (phishing techniques evolve)
               - Whitelist/blacklist integration
               - User feedback loop for continuous improvement
               - Low-latency requirements for real-time detection

            5. **Additional Data Sources**:
               - URL reputation databases
               - Certificate transparency logs
               - Domain registration (WHOIS) data
            """)
