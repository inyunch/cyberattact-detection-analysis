"""
Data Encoding Module for Cybersecurity Dashboard

This module provides comprehensive data encoding capabilities for preparing
datasets for machine learning applications. It handles both label encoding
for ordinal variables and one-hot encoding for nominal categorical variables.

Features:
- Label Encoding for ordinal categorical variables
- One-Hot Encoding for nominal categorical variables
- Feature engineering utilities
- Encoded dataset visualization and export
- Encoding mapping documentation

Author: CyberGuard Team
Last Updated: 2025-01
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from modules.theme import COLORS, apply_plotly_theme


def show(global_threats, intrusion_data):
    """Main entry point for data encoding page."""

    st.title("🔢 Data Encoding & Feature Engineering")
    st.markdown("Transform categorical variables into numeric representations for machine learning")
    st.markdown("---")

    # Dataset selection
    dataset_choice = st.radio(
        "Select Dataset to Encode",
        ["Global Threats Dataset", "Intrusion Detection Dataset", "Both Datasets"],
        horizontal=True
    )

    st.markdown("---")

    if dataset_choice in ["Global Threats Dataset", "Both Datasets"]:
        st.subheader("🌍 Global Threats Dataset Encoding")
        encode_global_threats(global_threats)

        if dataset_choice == "Both Datasets":
            st.markdown("---")

    if dataset_choice in ["Intrusion Detection Dataset", "Both Datasets"]:
        st.subheader("🛡️ Intrusion Detection Dataset Encoding")
        encode_intrusion_detection(intrusion_data)


def encode_global_threats(df):
    """Encode categorical variables in Global Threats dataset."""

    st.markdown("#### 📋 Categorical Variables Identified")

    # Identify categorical columns
    categorical_cols = {
        'Country': 'nominal',
        'Attack Type': 'nominal',
        'Target Industry': 'nominal',
        'Attack Source': 'nominal',
        'Security Vulnerability Type': 'nominal'
    }

    # Display categorical columns info
    col1, col2 = st.columns(2)

    with col1:
        cat_info = []
        for col, enc_type in categorical_cols.items():
            if col in df.columns:
                unique_count = df[col].nunique()
                cat_info.append({
                    'Column': col,
                    'Unique Values': unique_count,
                    'Encoding Type': enc_type.title()
                })

        cat_df = pd.DataFrame(cat_info)
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

    with col2:
        st.info("""
        **Encoding Strategy:**
        - **Nominal** variables (no order) → One-Hot Encoding
        - Creates binary columns for each category
        - Suitable for: Country, Attack Type, Industry, etc.
        """)

    st.markdown("---")

    # Encoding options
    st.markdown("#### ⚙️ Encoding Configuration")

    encoding_method = st.radio(
        "Select Encoding Method",
        ["One-Hot Encoding (Recommended)", "Label Encoding", "Both Methods"],
        help="One-Hot creates binary columns; Label assigns integer codes"
    )

    selected_cols = st.multiselect(
        "Select Columns to Encode",
        options=[col for col in categorical_cols.keys() if col in df.columns],
        default=[col for col in categorical_cols.keys() if col in df.columns]
    )

    if not selected_cols:
        st.warning("Please select at least one column to encode.")
        return

    if st.button("🚀 Apply Encoding", type="primary"):
        with st.spinner("Encoding data..."):
            # Create copy of dataframe
            df_encoded = df.copy()
            encoding_info = {}

            if encoding_method in ["One-Hot Encoding (Recommended)", "Both Methods"]:
                st.markdown("---")
                st.markdown("#### 📊 One-Hot Encoded Dataset")

                # Apply one-hot encoding
                df_onehot = df.copy()
                for col in selected_cols:
                    if col in df_onehot.columns:
                        # Get dummies
                        dummies = pd.get_dummies(df_onehot[col], prefix=col, drop_first=False)
                        encoding_info[col] = {
                            'method': 'one-hot',
                            'original_categories': df[col].unique().tolist(),
                            'new_columns': dummies.columns.tolist()
                        }
                        # Drop original and concatenate dummies
                        df_onehot = df_onehot.drop(columns=[col])
                        df_onehot = pd.concat([df_onehot, dummies], axis=1)

                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Columns", len(df.columns))
                with col2:
                    st.metric("Encoded Columns", len(df_onehot.columns))
                with col3:
                    new_cols = len(df_onehot.columns) - len(df.columns) + len(selected_cols)
                    st.metric("New Feature Columns", f"+{new_cols}")

                # Preview
                st.markdown("**Preview (First 10 Rows):**")
                st.dataframe(df_onehot.head(10), use_container_width=True)

                # Show encoding mapping
                with st.expander("📖 View Encoding Mappings"):
                    for col, info in encoding_info.items():
                        st.markdown(f"**{col}**")
                        # Create one row per category showing which encoded column(s) it maps to
                        encoded_cols_list = []
                        for cat in info['original_categories']:
                            # Find columns that contain this category
                            matching_cols = [c for c in info['new_columns'] if str(cat) in c]
                            if len(matching_cols) > 3:
                                encoded_cols_list.append(', '.join(matching_cols[:3]) + '...')
                            else:
                                encoded_cols_list.append(', '.join(matching_cols) if matching_cols else 'N/A')

                        mapping_df = pd.DataFrame({
                            'Original Category': info['original_categories'],
                            'Encoded Columns': encoded_cols_list
                        })
                        st.dataframe(mapping_df, hide_index=True)
                        st.markdown("")

                # Download button
                csv = df_onehot.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download One-Hot Encoded Dataset (CSV)",
                    data=csv,
                    file_name='global_threats_onehot_encoded.csv',
                    mime='text/csv',
                    help="Download the dataset with one-hot encoded categorical variables"
                )

                # Visualization
                st.markdown("---")
                st.markdown("#### 📈 Feature Expansion Visualization")

                # Show before/after column counts by type
                fig = go.Figure()

                categories = ['Original Dataset', 'One-Hot Encoded']
                numeric_cols = [len(df.select_dtypes(include=[np.number]).columns),
                              len(df_onehot.select_dtypes(include=[np.number]).columns)]
                categorical_cols_count = [len(df.select_dtypes(include=['object']).columns),
                                         len(df_onehot.select_dtypes(include=['object']).columns)]

                fig.add_trace(go.Bar(
                    name='Numeric Features',
                    x=categories,
                    y=numeric_cols,
                    marker_color=COLORS['accent_blue']
                ))

                fig.add_trace(go.Bar(
                    name='Categorical Features',
                    x=categories,
                    y=categorical_cols_count,
                    marker_color=COLORS['accent_green']
                ))

                fig = apply_plotly_theme(fig, title='Feature Count: Before vs After Encoding')
                fig.update_layout(
                    barmode='stack',
                    xaxis_title='Dataset Version',
                    yaxis_title='Number of Features',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            if encoding_method in ["Label Encoding", "Both Methods"]:
                if encoding_method == "Both Methods":
                    st.markdown("---")

                st.markdown("#### 🔢 Label Encoded Dataset")

                # Apply label encoding
                df_label = df.copy()
                label_encoders = {}
                label_mappings = {}

                for col in selected_cols:
                    if col in df_label.columns:
                        le = LabelEncoder()
                        df_label[f'{col}_Encoded'] = le.fit_transform(df_label[col].astype(str))
                        label_encoders[col] = le
                        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

                # Show results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original Columns", len(df.columns))
                with col2:
                    st.metric("Total Columns (with encoded)", len(df_label.columns))

                # Preview
                st.markdown("**Preview (First 10 Rows):**")
                preview_cols = [col for col in df_label.columns if col in selected_cols or '_Encoded' in col][:10]
                st.dataframe(df_label[preview_cols].head(10), use_container_width=True)

                # Show encoding mapping
                with st.expander("📖 View Label Encoding Mappings"):
                    for col, mapping in label_mappings.items():
                        st.markdown(f"**{col}**")
                        mapping_df = pd.DataFrame(list(mapping.items()), columns=['Category', 'Encoded Value'])
                        st.dataframe(mapping_df, hide_index=True)
                        st.markdown("")

                # Download button
                csv = df_label.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Label Encoded Dataset (CSV)",
                    data=csv,
                    file_name='global_threats_label_encoded.csv',
                    mime='text/csv',
                    help="Download the dataset with label encoded categorical variables"
                )

                # Visualization - show distribution of encoded values
                st.markdown("---")
                st.markdown("#### 📊 Encoded Value Distributions")

                selected_viz_col = st.selectbox(
                    "Select column to visualize",
                    [col for col in selected_cols if col in df_label.columns]
                )

                if selected_viz_col:
                    col1, col2 = st.columns(2)

                    with col1:
                        # Original distribution
                        value_counts_df = df[selected_viz_col].value_counts().reset_index()
                        value_counts_df.columns = ['Category', 'Count']

                        fig = px.bar(
                            value_counts_df,
                            x='Category',
                            y='Count',
                            labels={'Category': selected_viz_col, 'Count': 'Count'},
                            color='Count',
                            color_continuous_scale='Blues'
                        )
                        fig = apply_plotly_theme(fig, title=f'Original: {selected_viz_col}')
                        fig.update_layout(height=400, showlegend=False)
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        # Encoded distribution
                        encoded_col = f'{selected_viz_col}_Encoded'
                        value_counts_df = df_label[encoded_col].value_counts().sort_index().reset_index()
                        value_counts_df.columns = ['Encoded_Value', 'Count']

                        fig = px.bar(
                            value_counts_df,
                            x='Encoded_Value',
                            y='Count',
                            labels={'Encoded_Value': 'Encoded Value', 'Count': 'Count'},
                            color='Count',
                            color_continuous_scale='Greens'
                        )
                        fig = apply_plotly_theme(fig, title=f'Encoded: {encoded_col}')
                        fig.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)


def encode_intrusion_detection(df):
    """Encode categorical variables in Intrusion Detection dataset."""

    st.markdown("#### 📋 Categorical Variables Identified")

    # Identify categorical columns
    categorical_cols = {
        'protocol_type': 'nominal',
        'encryption_used': 'nominal',
        'browser_type': 'nominal',
        'unusual_time_access': 'binary',
        'attack_detected': 'binary'
    }

    # Display categorical columns info
    col1, col2 = st.columns(2)

    with col1:
        cat_info = []
        for col, enc_type in categorical_cols.items():
            if col in df.columns:
                unique_count = df[col].nunique()
                cat_info.append({
                    'Column': col,
                    'Unique Values': unique_count,
                    'Encoding Type': enc_type.title()
                })

        cat_df = pd.DataFrame(cat_info)
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

    with col2:
        st.info("""
        **Encoding Strategy:**
        - **Binary** variables → Already numeric (0/1)
        - **Nominal** variables → One-Hot Encoding
        - Creates separate columns for each protocol, encryption, browser
        """)

    st.markdown("---")

    # Encoding options
    st.markdown("#### ⚙️ Encoding Configuration")

    # Filter out already binary columns
    non_binary_cols = [col for col, enc_type in categorical_cols.items()
                      if enc_type != 'binary' and col in df.columns]

    encoding_method = st.radio(
        "Select Encoding Method",
        ["One-Hot Encoding (Recommended)", "Label Encoding", "Both Methods"],
        help="One-Hot creates binary columns; Label assigns integer codes",
        key='intrusion_encoding_method'
    )

    selected_cols = st.multiselect(
        "Select Columns to Encode",
        options=non_binary_cols,
        default=non_binary_cols,
        key='intrusion_selected_cols'
    )

    # Feature scaling option
    apply_scaling = st.checkbox(
        "Apply StandardScaler to numeric features",
        value=False,
        help="Standardize numeric features to have mean=0 and std=1"
    )

    if not selected_cols:
        st.warning("Please select at least one column to encode.")
        return

    if st.button("🚀 Apply Encoding", type="primary", key='intrusion_encode_btn'):
        with st.spinner("Encoding data..."):
            # Create copy of dataframe
            df_encoded = df.copy()
            encoding_info = {}

            if encoding_method in ["One-Hot Encoding (Recommended)", "Both Methods"]:
                st.markdown("---")
                st.markdown("#### 📊 One-Hot Encoded Dataset")

                # Apply one-hot encoding
                df_onehot = df.copy()
                for col in selected_cols:
                    if col in df_onehot.columns:
                        # Get dummies
                        dummies = pd.get_dummies(df_onehot[col], prefix=col, drop_first=False)
                        encoding_info[col] = {
                            'method': 'one-hot',
                            'original_categories': df[col].unique().tolist(),
                            'new_columns': dummies.columns.tolist()
                        }
                        # Drop original and concatenate dummies
                        df_onehot = df_onehot.drop(columns=[col])
                        df_onehot = pd.concat([df_onehot, dummies], axis=1)

                # Apply scaling if requested
                if apply_scaling:
                    numeric_cols = df_onehot.select_dtypes(include=[np.number]).columns
                    scaler = StandardScaler()
                    # Pandas 2.0+ compatibility: convert numpy array back to DataFrame
                    scaled_data = scaler.fit_transform(df_onehot[numeric_cols])
                    df_onehot[numeric_cols] = pd.DataFrame(
                        scaled_data,
                        columns=numeric_cols,
                        index=df_onehot.index
                    )
                    st.success("✅ StandardScaler applied to numeric features")

                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Columns", len(df.columns))
                with col2:
                    st.metric("Encoded Columns", len(df_onehot.columns))
                with col3:
                    new_cols = len(df_onehot.columns) - len(df.columns) + len(selected_cols)
                    st.metric("New Feature Columns", f"+{new_cols}")

                # Preview
                st.markdown("**Preview (First 10 Rows):**")
                st.dataframe(df_onehot.head(10), use_container_width=True)

                # Show encoding mapping
                with st.expander("📖 View Encoding Mappings"):
                    for col, info in encoding_info.items():
                        st.markdown(f"**{col}**")
                        st.write(f"Original categories: {', '.join(map(str, info['original_categories']))}")
                        st.write(f"New columns: {', '.join(info['new_columns'])}")
                        st.markdown("")

                # Show feature importance for ML
                st.markdown("---")
                st.markdown("#### 🎯 ML-Ready Feature Summary")

                # Separate features and target
                if 'attack_detected' in df_onehot.columns:
                    feature_cols = [col for col in df_onehot.columns if col != 'attack_detected']
                    st.success(f"✅ **{len(feature_cols)} features** ready for ML training")
                    st.info(f"**Target variable:** attack_detected (binary classification)")

                    # Show feature types
                    col1, col2 = st.columns(2)
                    with col1:
                        numeric_features = len(df_onehot[feature_cols].select_dtypes(include=[np.number]).columns)
                        st.metric("Numeric Features", numeric_features)
                    with col2:
                        categorical_features = len(df_onehot[feature_cols].select_dtypes(include=['object']).columns)
                        st.metric("Categorical Features", categorical_features)

                # Download button
                csv = df_onehot.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download One-Hot Encoded Dataset (CSV)",
                    data=csv,
                    file_name='intrusion_detection_onehot_encoded.csv',
                    mime='text/csv',
                    help="Download the ML-ready dataset with encoded features"
                )

                # Visualization
                st.markdown("---")
                st.markdown("#### 📈 Feature Expansion Visualization")

                fig = go.Figure()

                categories = ['Original Dataset', 'One-Hot Encoded']
                numeric_cols_count = [len(df.select_dtypes(include=[np.number]).columns),
                                     len(df_onehot.select_dtypes(include=[np.number]).columns)]
                categorical_cols_count = [len(df.select_dtypes(include=['object']).columns),
                                         len(df_onehot.select_dtypes(include=['object']).columns)]

                fig.add_trace(go.Bar(
                    name='Numeric Features',
                    x=categories,
                    y=numeric_cols_count,
                    marker_color=COLORS['accent_blue']
                ))

                fig.add_trace(go.Bar(
                    name='Categorical Features',
                    x=categories,
                    y=categorical_cols_count,
                    marker_color=COLORS['accent_green']
                ))

                fig = apply_plotly_theme(fig, title='Feature Count: Before vs After Encoding')
                fig.update_layout(
                    barmode='stack',
                    xaxis_title='Dataset Version',
                    yaxis_title='Number of Features',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            if encoding_method in ["Label Encoding", "Both Methods"]:
                if encoding_method == "Both Methods":
                    st.markdown("---")

                st.markdown("#### 🔢 Label Encoded Dataset")

                # Apply label encoding
                df_label = df.copy()
                label_encoders = {}
                label_mappings = {}

                for col in selected_cols:
                    if col in df_label.columns:
                        le = LabelEncoder()
                        df_label[f'{col}_Encoded'] = le.fit_transform(df_label[col].astype(str))
                        label_encoders[col] = le
                        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

                # Apply scaling if requested
                if apply_scaling:
                    numeric_cols = df_label.select_dtypes(include=[np.number]).columns
                    scaler = StandardScaler()
                    # Pandas 2.0+ compatibility: convert numpy array back to DataFrame
                    scaled_data = scaler.fit_transform(df_label[numeric_cols])
                    df_label[numeric_cols] = pd.DataFrame(
                        scaled_data,
                        columns=numeric_cols,
                        index=df_label.index
                    )
                    st.success("✅ StandardScaler applied to numeric features")

                # Show results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original Columns", len(df.columns))
                with col2:
                    st.metric("Total Columns (with encoded)", len(df_label.columns))

                # Preview
                st.markdown("**Preview (First 10 Rows):**")
                preview_cols = list(df_label.columns)[:15]  # Show first 15 columns
                st.dataframe(df_label[preview_cols].head(10), use_container_width=True)

                # Show encoding mapping
                with st.expander("📖 View Label Encoding Mappings"):
                    for col, mapping in label_mappings.items():
                        st.markdown(f"**{col}**")
                        mapping_df = pd.DataFrame(list(mapping.items()), columns=['Category', 'Encoded Value'])
                        st.dataframe(mapping_df, hide_index=True)
                        st.markdown("")

                # Download button
                csv = df_label.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Label Encoded Dataset (CSV)",
                    data=csv,
                    file_name='intrusion_detection_label_encoded.csv',
                    mime='text/csv',
                    help="Download the dataset with label encoded categorical variables"
                )

                # Visualization - show encoding for protocol types
                st.markdown("---")
                st.markdown("#### 📊 Encoding Visualization")

                if 'protocol_type' in selected_cols and 'protocol_type' in df.columns:
                    col1, col2 = st.columns(2)

                    with col1:
                        # Protocol distribution
                        fig = px.pie(
                            df,
                            names='protocol_type',
                            title='Protocol Type Distribution',
                            color_discrete_sequence=[COLORS['accent_blue'], COLORS['accent_green'], COLORS['accent_purple']]
                        )
                        fig = apply_plotly_theme(fig)
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        # Attack rate by protocol
                        if 'attack_detected' in df.columns:
                            protocol_attack = df.groupby('protocol_type')['attack_detected'].mean() * 100
                            fig = px.bar(
                                protocol_attack.reset_index(),
                                x='protocol_type',
                                y='attack_detected',
                                labels={'attack_detected': 'Attack Rate (%)', 'protocol_type': 'Protocol'},
                                color='attack_detected',
                                color_continuous_scale='Reds'
                            )
                            fig = apply_plotly_theme(fig, title='Attack Rate by Protocol')
                            fig.update_layout(height=400, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)

    # Add ML Pipeline Guide
    st.markdown("---")
    st.markdown("#### 🤖 Next Steps: ML Pipeline")

    with st.expander("💡 How to Use Encoded Data for Machine Learning"):
        st.markdown("""
        **1. Load the encoded dataset:**
        ```python
        import pandas as pd
        df = pd.read_csv('intrusion_detection_onehot_encoded.csv')
        ```

        **2. Separate features and target:**
        ```python
        X = df.drop('attack_detected', axis=1)  # Features
        y = df['attack_detected']  # Target
        ```

        **3. Split into train/test sets:**
        ```python
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        ```

        **4. Train a model:**
        ```python
        from sklearn.ensemble import RandomForestClassifier

        model = RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',  # Handle class imbalance
            random_state=42
        )
        model.fit(X_train, y_train)
        ```

        **5. Evaluate:**
        ```python
        from sklearn.metrics import classification_report, roc_auc_score

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")
        ```

        **Important Notes:**
        - Use `class_weight='balanced'` to handle the 95:5 class imbalance
        - Consider SMOTE for oversampling the minority class
        - Use stratified splitting to maintain class proportions
        - Evaluate with Precision, Recall, F1-Score (not just accuracy)
        """)
