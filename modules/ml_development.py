"""
ML Model Development and Evaluation Module
Implements multiple ML models for intrusion detection with comprehensive evaluation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc, roc_auc_score
)
from modules.theme import COLORS, apply_plotly_theme, st_observation_box, st_dark_box
import warnings
warnings.filterwarnings('ignore')


def show(global_threats, intrusion_data):
    """Display ML model development and evaluation"""

    st.title("🤖 ML Model Development and Evaluation")

    st.markdown(f"""
    <div style="background: {COLORS['accent_blue']}0D; border-left: 4px solid {COLORS['accent_blue']}; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
        <p style="margin: 0; color: {COLORS['text_primary']}; line-height: 1.6;">
            <strong>Purpose:</strong> Develop and evaluate machine learning models for network intrusion detection.
            This module implements multiple supervised learning algorithms, performs model comparison, and demonstrates
            proper validation techniques.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # SECTION 1: FEATURE ENGINEERING
    # ============================================
    st.header("1️⃣ Feature Engineering & Selection")

    st.markdown("""
    Understanding and preparing features is crucial for model performance.
    Let's analyze the most important features for intrusion detection.
    """)

    # Feature importance from Random Forest
    @st.cache_data
    def analyze_features(df):
        """Analyze and rank features by importance"""
        # Select numerical features
        feature_cols = ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
                       'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
                       'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
                       'num_shells', 'num_access_files', 'count', 'srv_count',
                       'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
                       'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate']

        available_features = [col for col in feature_cols if col in df.columns]

        if len(available_features) < 5:
            return None, None, None

        X = df[available_features].copy()
        y = df['attack_detected'] if 'attack_detected' in df.columns else df.iloc[:, -1]

        # Handle missing values
        X = X.fillna(X.mean())

        # Train quick Random Forest to get feature importance
        rf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
        rf.fit(X, y)

        # Get feature importance
        importance_df = pd.DataFrame({
            'Feature': available_features,
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=False)

        return importance_df, X, y

    importance_df, X_features, y_target = analyze_features(intrusion_data)

    if importance_df is not None:
        # Feature importance chart
        fig = go.Figure(go.Bar(
            x=importance_df.head(15)['Importance'],
            y=importance_df.head(15)['Feature'],
            orientation='h',
            marker=dict(
                color=importance_df.head(15)['Importance'],
                colorscale=[[0, COLORS['accent_blue']], [1, COLORS['accent_green']]],
                showscale=False
            ),
            text=importance_df.head(15)['Importance'].apply(lambda x: f'{x:.4f}'),
            textposition='auto'
        ))

        fig.update_layout(
            xaxis_title='Importance Score',
            yaxis_title='Feature',
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )

        fig = apply_plotly_theme(fig, title='Top 15 Features by Importance (Random Forest)')
        st.plotly_chart(fig, use_container_width=True)

        st_observation_box(
            "💡 Feature Importance Insights",
            f"The top 3 most predictive features are **{importance_df.iloc[0]['Feature']}**, "
            f"**{importance_df.iloc[1]['Feature']}**, and **{importance_df.iloc[2]['Feature']}**. "
            f"These features have the highest impact on intrusion detection accuracy."
        )

        # Feature correlation heatmap
        with st.expander("📊 Feature Correlation Analysis", expanded=False):
            top_features = importance_df.head(10)['Feature'].tolist()
            corr_matrix = intrusion_data[top_features].corr()

            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))

            fig.update_layout(
                xaxis={'side': 'bottom'},
                height=600
            )

            fig = apply_plotly_theme(fig, title='Feature Correlation Matrix (Top 10 Features)')
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ============================================
    # SECTION 2: MODEL DEVELOPMENT
    # ============================================
    st.header("2️⃣ Model Development & Training")

    st.markdown("""
    We implement multiple machine learning algorithms to find the best approach for intrusion detection.
    Each model has different strengths and assumptions.
    """)

    # Data preparation
    @st.cache_data
    def prepare_ml_data(df):
        """Prepare data for ML training"""
        feature_columns = ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
                          'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
                          'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
                          'num_shells', 'num_access_files', 'count', 'srv_count',
                          'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
                          'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate']

        available_features = [col for col in feature_columns if col in df.columns]

        X = df[available_features].copy()
        y = df['attack_detected'] if 'attack_detected' in df.columns else df.iloc[:, -1]

        # Handle missing values
        X = X.fillna(X.mean())

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.3, random_state=42, stratify=y
        )

        return X_train, X_test, y_train, y_test, available_features

    try:
        X_train, X_test, y_train, y_test, feature_names = prepare_ml_data(intrusion_data)

        # Display data split
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Samples", f"{len(X_train) + len(X_test):,}")
        with col2:
            st.metric("Training (70%)", f"{len(X_train):,}")
        with col3:
            st.metric("Testing (30%)", f"{len(X_test):,}")
        with col4:
            st.metric("Features", len(feature_names))

        # Model training interface
        st.subheader("📚 Select Models to Train")

        col1, col2 = st.columns(2)
        with col1:
            use_rf = st.checkbox("Random Forest", value=True, help="Ensemble of decision trees")
            use_lr = st.checkbox("Logistic Regression", value=True, help="Linear probabilistic model")
        with col2:
            use_gb = st.checkbox("Gradient Boosting", value=True, help="Boosted decision trees")
            use_dt = st.checkbox("Decision Tree", value=False, help="Single decision tree")

        if st.button("🚀 Train Selected Models", type="primary"):
            results = {}
            progress_bar = st.progress(0)
            status_text = st.empty()

            models_to_train = []
            if use_rf:
                models_to_train.append(("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)))
            if use_gb:
                models_to_train.append(("Gradient Boosting", GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)))
            if use_lr:
                models_to_train.append(("Logistic Regression", LogisticRegression(max_iter=1000, random_state=42)))
            if use_dt:
                models_to_train.append(("Decision Tree", DecisionTreeClassifier(random_state=42, max_depth=10)))

            for idx, (model_name, model) in enumerate(models_to_train):
                status_text.text(f"Training {model_name}...")

                # Train model
                model.fit(X_train, y_train)

                # Predictions
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred

                # Metrics
                results[model_name] = {
                    'model': model,
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, zero_division=0),
                    'recall': recall_score(y_test, y_pred, zero_division=0),
                    'f1': f1_score(y_test, y_pred, zero_division=0),
                    'roc_auc': roc_auc_score(y_test, y_pred_proba),
                    'confusion_matrix': confusion_matrix(y_test, y_pred),
                    'y_pred': y_pred,
                    'y_pred_proba': y_pred_proba
                }

                progress_bar.progress((idx + 1) / len(models_to_train))

            status_text.success("✅ Training complete!")
            st.session_state.ml_results = results
            st.session_state.y_test = y_test

        # Display results
        if 'ml_results' in st.session_state and st.session_state.ml_results:
            st.markdown("---")
            st.header("3️⃣ Model Evaluation & Comparison")

            results = st.session_state.ml_results

            # Performance metrics table
            metrics_df = pd.DataFrame({
                'Model': list(results.keys()),
                'Accuracy': [r['accuracy'] for r in results.values()],
                'Precision': [r['precision'] for r in results.values()],
                'Recall': [r['recall'] for r in results.values()],
                'F1-Score': [r['f1'] for r in results.values()],
                'ROC-AUC': [r['roc_auc'] for r in results.values()]
            }).sort_values('F1-Score', ascending=False)

            st.subheader("📊 Performance Metrics Comparison")
            st.dataframe(
                metrics_df.style.format({
                    'Accuracy': '{:.4f}',
                    'Precision': '{:.4f}',
                    'Recall': '{:.4f}',
                    'F1-Score': '{:.4f}',
                    'ROC-AUC': '{:.4f}'
                }).background_gradient(cmap='RdYlGn', subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']),
                use_container_width=True,
                hide_index=True
            )

            # Bar chart comparison
            fig = go.Figure()
            metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']

            for metric in metrics:
                fig.add_trace(go.Bar(
                    name=metric,
                    x=metrics_df['Model'],
                    y=metrics_df[metric],
                    text=metrics_df[metric].apply(lambda x: f'{x:.3f}'),
                    textposition='auto'
                ))

            fig.update_layout(
                barmode='group',
                xaxis_title='Model',
                yaxis_title='Score',
                yaxis=dict(range=[0, 1.05]),
                height=500
            )

            fig = apply_plotly_theme(fig, title='Model Performance Comparison')
            st.plotly_chart(fig, use_container_width=True)

            # Best model
            best_model = metrics_df.iloc[0]['Model']
            best_f1 = metrics_df.iloc[0]['F1-Score']

            st_observation_box(
                "🏆 Best Performing Model",
                f"**{best_model}** achieved the highest F1-Score of **{best_f1:.4f}**. "
                f"This model provides the best balance between precision (minimizing false alarms) "
                f"and recall (catching actual attacks)."
            )

            # ROC Curves
            st.subheader("📈 ROC Curve Analysis")

            fig = go.Figure()

            y_test_data = st.session_state.y_test

            for model_name, model_results in results.items():
                if len(np.unique(y_test_data)) > 1:
                    fpr, tpr, _ = roc_curve(y_test_data, model_results['y_pred_proba'])
                    auc_score = model_results['roc_auc']

                    fig.add_trace(go.Scatter(
                        x=fpr,
                        y=tpr,
                        mode='lines',
                        name=f'{model_name} (AUC = {auc_score:.3f})',
                        line=dict(width=3)
                    ))

            # Diagonal reference
            fig.add_trace(go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode='lines',
                name='Random Classifier',
                line=dict(color=COLORS['text_muted'], width=2, dash='dash')
            ))

            fig.update_layout(
                xaxis_title='False Positive Rate',
                yaxis_title='True Positive Rate',
                xaxis=dict(range=[0, 1]),
                yaxis=dict(range=[0, 1]),
                height=500
            )

            fig = apply_plotly_theme(fig, title='ROC Curves - Model Comparison')
            st.plotly_chart(fig, use_container_width=True)

            # Confusion Matrices
            st.subheader("🎯 Confusion Matrices")

            cols = st.columns(min(2, len(results)))
            for idx, (model_name, model_results) in enumerate(results.items()):
                with cols[idx % 2]:
                    cm = model_results['confusion_matrix']

                    fig = go.Figure(data=go.Heatmap(
                        z=cm,
                        x=['Predicted Normal', 'Predicted Attack'],
                        y=['Actual Normal', 'Actual Attack'],
                        colorscale='Blues',
                        text=cm,
                        texttemplate='<b>%{text}</b>',
                        textfont={"size": 16},
                        showscale=True
                    ))

                    fig.update_layout(height=350)
                    fig = apply_plotly_theme(fig, title=f'{model_name}')
                    st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Model validation
            st.header("4️⃣ Model Validation")

            st.markdown("""
            Cross-validation provides a robust estimate of model performance by training on multiple data splits.
            """)

            if st.button("🔄 Run 5-Fold Cross-Validation on Best Model"):
                with st.spinner(f"Performing cross-validation on {best_model}..."):
                    best_model_obj = results[best_model]['model']

                    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
                    cv_scores = cross_val_score(best_model_obj, X_train, y_train, cv=cv, scoring='f1', n_jobs=-1)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean F1-Score", f"{cv_scores.mean():.4f}")
                    with col2:
                        st.metric("Std Deviation", f"{cv_scores.std():.4f}")
                    with col3:
                        st.metric("95% Confidence", f"±{1.96 * cv_scores.std():.4f}")

                    fig = go.Figure(go.Bar(
                        x=[f'Fold {i+1}' for i in range(len(cv_scores))],
                        y=cv_scores,
                        marker_color=COLORS['accent_purple'],
                        text=cv_scores.round(4),
                        textposition='auto'
                    ))

                    fig.add_hline(
                        y=cv_scores.mean(),
                        line_dash="dash",
                        line_color=COLORS['accent_orange'],
                        annotation_text=f"Mean: {cv_scores.mean():.4f}"
                    )

                    fig.update_layout(
                        xaxis_title='Fold',
                        yaxis_title='F1-Score',
                        height=400,
                        yaxis=dict(range=[0, 1])
                    )

                    fig = apply_plotly_theme(fig, title='Cross-Validation Results')
                    st.plotly_chart(fig, use_container_width=True)

                    st_observation_box(
                        "✅ Cross-Validation Assessment",
                        f"The model shows **{'consistent' if cv_scores.std() < 0.05 else 'variable'}** "
                        f"performance across folds (std: {cv_scores.std():.4f}). "
                        f"Mean F1-Score of {cv_scores.mean():.4f} indicates strong generalization."
                    )

    except Exception as e:
        st.error(f"Error in ML model development: {e}")
        st.info("Please ensure the intrusion dataset has required features for model training.")
