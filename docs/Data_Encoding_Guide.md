# Data Encoding Guide

## Overview

The Data Encoding module provides comprehensive data encoding capabilities to prepare cybersecurity datasets for machine learning applications. It transforms categorical variables into numeric representations that ML algorithms can process.

## Accessing the Data Encoding Page

Navigate to **Analysis → Data Encoding** in the dashboard sidebar.

## Features

### 1. **Categorical Variable Identification**

The module automatically identifies categorical variables in both datasets:

#### Global Threats Dataset
- `Country` - Nominal (195+ unique values)
- `Attack Type` - Nominal (Ransomware, Phishing, DDoS, etc.)
- `Target Industry` - Nominal (Healthcare, Finance, Government, etc.)
- `Attack Source` - Nominal (Cybercriminal, Nation-State, Hacktivist, etc.)
- `Security Vulnerability Type` - Nominal

#### Intrusion Detection Dataset
- `protocol_type` - Nominal (TCP, UDP, ICMP)
- `encryption_used` - Nominal (AES, DES, None)
- `browser_type` - Nominal
- `unusual_time_access` - Binary (already encoded as 0/1)
- `attack_detected` - Binary (already encoded as 0/1)

### 2. **Encoding Methods**

#### One-Hot Encoding (Recommended)
**What it does:**
- Creates separate binary columns for each category
- Each category becomes a feature with values 0 or 1
- Preserves no implicit ordering

**Example:**
```
Original:
protocol_type
-------------
TCP
UDP
TCP

One-Hot Encoded:
protocol_type_TCP | protocol_type_UDP | protocol_type_ICMP
-----------------|--------------------|--------------------
        1        |         0          |         0
        0        |         1          |         0
        1        |         0          |         0
```

**Best for:**
- Nominal variables (no inherent order)
- When you want to avoid imposing false ordering
- Most machine learning algorithms

**Advantages:**
- ✅ No false relationships between categories
- ✅ Works well with linear models
- ✅ Easy to interpret

**Disadvantages:**
- ❌ Increases feature dimensionality
- ❌ Can cause memory issues with high-cardinality features (e.g., Country with 195 values)

#### Label Encoding
**What it does:**
- Assigns each category a unique integer
- Simple numeric mapping: Category1=0, Category2=1, Category3=2, etc.

**Example:**
```
Original:          Label Encoded:
protocol_type  →   protocol_type_Encoded
-------------      ---------------------
TCP            →          0
UDP            →          1
ICMP           →          2
TCP            →          0
```

**Best for:**
- Tree-based models (Random Forest, XGBoost)
- When you want to minimize feature count
- Ordinal variables (though we use it for nominal here)

**Advantages:**
- ✅ Minimal memory footprint
- ✅ Works well with tree-based algorithms

**Disadvantages:**
- ❌ Introduces false ordering (TCP=0, UDP=1 implies TCP < UDP)
- ❌ Not suitable for linear models

### 3. **Feature Scaling (Optional)**

When encoding the Intrusion Detection dataset, you can optionally apply StandardScaler to numeric features:

**What it does:**
```python
scaled_value = (value - mean) / std_deviation
```

**Result:**
- All features have mean = 0
- All features have standard deviation = 1

**When to use:**
- For distance-based algorithms (KNN, SVM, Neural Networks)
- When features have different scales (e.g., packet_size: 64-1500, ip_reputation: 0-1)

**When NOT to use:**
- For tree-based algorithms (Random Forest, XGBoost) - they don't require scaling

## Step-by-Step Usage

### For Global Threats Dataset

1. **Select Dataset**: Choose "Global Threats Dataset"

2. **Review Categorical Variables**: Check the table showing:
   - Column names
   - Number of unique values
   - Recommended encoding type

3. **Configure Encoding**:
   - Select encoding method (One-Hot, Label, or Both)
   - Choose which columns to encode (can select subset)

4. **Apply Encoding**: Click "Apply Encoding" button

5. **Review Results**:
   - Check the before/after column counts
   - Preview the encoded data (first 10 rows)
   - Review encoding mappings in the expander

6. **Download**: Click the download button to save the encoded dataset

### For Intrusion Detection Dataset

1. **Select Dataset**: Choose "Intrusion Detection Dataset"

2. **Configure Encoding**:
   - Select encoding method
   - Choose columns to encode (protocol_type, encryption_used, browser_type)
   - Optionally enable StandardScaler for numeric features

3. **Apply Encoding**: Click "Apply Encoding" button

4. **Review ML-Ready Summary**:
   - Total features available for training
   - Confirmation that target variable (attack_detected) is identified
   - Feature type breakdown

5. **Download**: Save the ML-ready dataset

## Encoding Recommendations by Use Case

### Use Case 1: Logistic Regression / Linear Models
**Recommendation:** One-Hot Encoding
```
Reason: Linear models assume numeric features have meaningful
relationships. One-Hot encoding prevents false ordinal relationships.
```

**Configuration:**
- Encoding Method: One-Hot Encoding
- Feature Scaling: ✅ Yes (StandardScaler)

### Use Case 2: Random Forest / XGBoost / Decision Trees
**Recommendation:** Label Encoding
```
Reason: Tree-based models can handle label-encoded categories well
and benefit from reduced dimensionality.
```

**Configuration:**
- Encoding Method: Label Encoding
- Feature Scaling: ❌ No (not needed)

### Use Case 3: Neural Networks
**Recommendation:** One-Hot Encoding + Scaling
```
Reason: Neural networks work best with normalized inputs and
one-hot encoded categoricals prevent false relationships.
```

**Configuration:**
- Encoding Method: One-Hot Encoding
- Feature Scaling: ✅ Yes (StandardScaler)

### Use Case 4: Exploratory Analysis
**Recommendation:** Both Methods
```
Reason: Compare model performance with different encoding strategies
to find what works best for your specific data.
```

**Configuration:**
- Encoding Method: Both Methods
- Feature Scaling: Test with and without

## Machine Learning Pipeline

After encoding, follow these steps:

### 1. Load Encoded Data
```python
import pandas as pd

# Load the one-hot encoded dataset
df = pd.read_csv('intrusion_detection_onehot_encoded.csv')
```

### 2. Separate Features and Target
```python
# Intrusion Detection
X = df.drop('attack_detected', axis=1)  # Features
y = df['attack_detected']  # Target (0=Normal, 1=Attack)

# Global Threats (for supervised learning, you'd need to define a target)
# Example: Predict if loss will be high
# df['high_loss'] = (df['Financial Loss (in Million $)'] > df['Financial Loss (in Million $)'].median()).astype(int)
```

### 3. Train/Test Split
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Important for imbalanced data
)
```

### 4. Handle Class Imbalance
```python
# Option 1: Use class weights
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',  # Automatically adjust weights
    random_state=42
)

# Option 2: Use SMOTE
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy=0.5, random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

### 5. Train Model
```python
model.fit(X_train, y_train)
```

### 6. Evaluate
```python
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Classification report
print(classification_report(y_test, y_pred))

# ROC-AUC Score
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Confusion Matrix
print(confusion_matrix(y_test, y_pred))
```

## Important Considerations

### High Cardinality Features

**Problem:** Features like `Country` (195 unique values) create 195 binary columns when one-hot encoded.

**Solutions:**

1. **Target Encoding:**
   ```python
   # Encode based on target mean
   country_means = df.groupby('Country')['target'].mean()
   df['Country_Encoded'] = df['Country'].map(country_means)
   ```

2. **Frequency Encoding:**
   ```python
   # Encode based on frequency
   country_freq = df['Country'].value_counts(normalize=True)
   df['Country_Encoded'] = df['Country'].map(country_freq)
   ```

3. **Group Rare Categories:**
   ```python
   # Group countries with < 1% frequency as "Other"
   freq = df['Country'].value_counts(normalize=True)
   rare_countries = freq[freq < 0.01].index
   df['Country'] = df['Country'].replace(rare_countries, 'Other')
   ```

### Class Imbalance (Intrusion Detection)

**Problem:** Dataset has 95% normal traffic, 5% attacks

**Impact:**
- Model will bias toward predicting "Normal"
- 95% accuracy can be achieved by always predicting "Normal"

**Solutions:**

1. **Use appropriate metrics:** Precision, Recall, F1-Score, ROC-AUC (not accuracy)

2. **Apply class weights:** `class_weight='balanced'`

3. **Use SMOTE/ADASYN:** Oversample minority class

4. **Use ensemble methods:** Random Forest, XGBoost handle imbalance better

5. **Threshold adjustment:** Adjust prediction threshold from 0.5 to optimize for recall

## Visualizations

The encoding page provides:

1. **Feature Count Comparison:**
   - Stacked bar chart showing numeric vs categorical features
   - Before and after encoding

2. **Value Distribution:**
   - Original category distribution
   - Encoded value distribution
   - Side-by-side comparison

3. **Attack Rate Analysis:**
   - Attack rates by protocol type
   - Helps understand which categories are more predictive

## Export Formats

All encoded datasets are exported as CSV files:

- `global_threats_onehot_encoded.csv` - One-hot encoded global threats
- `global_threats_label_encoded.csv` - Label encoded global threats
- `intrusion_detection_onehot_encoded.csv` - One-hot encoded intrusion detection
- `intrusion_detection_label_encoded.csv` - Label encoded intrusion detection

Files include:
- ✅ All original numeric features
- ✅ All encoded categorical features
- ✅ Original categorical columns (for reference in label encoding)
- ✅ Proper column names with prefixes

## Troubleshooting

### Issue: "Memory Error" when encoding
**Solution:** Reduce the number of columns to encode or use label encoding for high-cardinality features

### Issue: Model performs poorly with one-hot encoding
**Solution:** Try label encoding or feature selection to reduce dimensionality

### Issue: Encoded values don't make sense
**Solution:** Check the encoding mappings in the expander to verify correct mapping

### Issue: Can't load encoded CSV
**Solution:** Ensure you're using pandas with `pd.read_csv()` and the file path is correct

## Additional Resources

- **Scikit-learn Preprocessing:** https://scikit-learn.org/stable/modules/preprocessing.html
- **Handling Categorical Data:** https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
- **Class Imbalance:** https://imbalanced-learn.org/stable/

## Support

For questions or issues with data encoding:
1. Check the encoding mappings in the expander
2. Verify your feature selection matches your ML algorithm choice
3. Review the ML Pipeline guide in the expander on the encoding page
