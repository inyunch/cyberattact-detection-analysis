# ML-Focused Cybersecurity Datasets Guide

## Overview

This guide describes the three new machine learning-focused cybersecurity datasets integrated into the CyberGuard dashboard.

## Datasets

### 1. Malware Detection Dataset
**File**: `data/malware_detection_dataset.csv`
**Samples**: 5,000 (2,998 malware, 2,002 benign)
**ML Task**: Binary Classification
**Target Variable**: `is_malware` (0 = Benign, 1 = Malware)

#### Features

**Static Analysis Features:**
- `file_size_kb`: File size in kilobytes
- `file_type`: File extension (.exe, .dll, .bat, etc.)
- `entropy`: File entropy score (higher = more random/packed)
- `is_packed`: Boolean - whether file is packed/compressed
- `code_sections`: Number of code sections in binary
- `imports_count`: Number of imported functions

**Behavioral Features:**
- `api_calls_count`: Number of API calls made
- `network_connections`: Number of network connections attempted
- `registry_changes`: Number of registry modifications
- `file_operations`: Number of file system operations
- `suspicious_strings`: Count of suspicious strings found

**Detection Features:**
- `obfuscated_code`: Boolean - code obfuscation detected
- `anti_debug_detected`: Boolean - anti-debugging techniques found
- `av_detection_rate`: Antivirus detection rate (0-1)
- `malware_type`: Type of malware (Trojan, Ransomware, etc.) or "Benign"

#### Recommended Algorithms
- Random Forest Classifier
- XGBoost
- Neural Networks
- Support Vector Machines

#### Key Use Cases
- Automated malware detection
- File reputation scoring
- Sandbox analysis augmentation
- Zero-day malware prediction

---

### 2. Phishing Detection Dataset
**File**: `data/phishing_detection_dataset.csv`
**Samples**: 4,000 (1,732 phishing, 2,268 legitimate)
**ML Task**: Binary Classification
**Target Variable**: `is_phishing` (0 = Legitimate, 1 = Phishing)

#### Features

**URL Features:**
- `domain`: Domain name
- `url_length`: Total URL character length
- `has_https`: Boolean - uses HTTPS protocol
- `ssl_valid`: Boolean - has valid SSL certificate
- `domain_age_days`: Age of domain in days
- `subdomain_count`: Number of subdomains
- `special_characters`: Count of special characters in URL
- `redirects_count`: Number of redirects

**Content Features:**
- `external_links`: Number of external links on page
- `forms_count`: Number of forms on page
- `popup_windows`: Boolean - uses popup windows
- `iframe_usage`: Boolean - uses iframes
- `suspicious_keywords`: Count of suspicious keywords

**Security Features:**
- `favicon_different_domain`: Boolean - favicon from different domain
- `dns_record_exists`: Boolean - DNS record exists
- `reported_phishing_count`: Number of phishing reports

#### Recommended Algorithms
- Gradient Boosting (XGBoost, LightGBM)
- Random Forest
- Logistic Regression
- Neural Networks

#### Key Use Cases
- Real-time URL filtering
- Email security gateways
- Browser extensions
- Security awareness training

---

### 3. CVE Vulnerability Dataset
**File**: `data/cve_vulnerability_dataset.csv`
**Samples**: 3,000 CVEs (2020-2024)
**ML Tasks**: Multi-class Classification OR Regression
**Target Variables**:
- Classification: `severity` (LOW, MEDIUM, HIGH, CRITICAL)
- Regression: `cvss_base_score` (0.0 - 10.0)

#### Features

**Metadata:**
- `cve_id`: CVE identifier (e.g., CVE-2023-00001)
- `published_date`: Publication date
- `year`: Publication year
- `vulnerability_type`: Type of vulnerability (SQL Injection, XSS, etc.)
- `vendor`: Affected vendor
- `product`: Affected product
- `affected_versions`: Number of affected versions

**CVSS Scores:**
- `cvss_base_score`: Base CVSS score (0-10)
- `severity`: Severity level (LOW/MEDIUM/HIGH/CRITICAL)
- `exploitability_score`: Exploitability sub-score (0-4)
- `impact_score`: Impact sub-score (0-6)

**Exploit Information:**
- `has_exploit`: Boolean - exploit code exists
- `exploit_public`: Boolean - exploit is publicly available

**Patch Information:**
- `patch_available`: Boolean - patch is available
- `days_to_patch`: Days from disclosure to patch

**Additional:**
- `cwe_id`: CWE identifier (e.g., CWE-79)
- `references_count`: Number of reference links

#### Recommended Algorithms

**For Severity Classification:**
- Random Forest
- Gradient Boosting
- Multi-class SVM
- Neural Networks

**For CVSS Score Regression:**
- Gradient Boosting Regressor
- Random Forest Regressor
- Linear Regression (baseline)
- Neural Networks

#### Key Use Cases
- Vulnerability prioritization
- Patch management optimization
- Risk assessment automation
- Security investment planning
- Threat intelligence

---

## Dataset Generation

All datasets were generated using `scripts/generate_ml_datasets.py` with realistic distributions based on cybersecurity patterns.

To regenerate datasets:

```bash
cd /home/user/cyberattact-detection-analysis/scripts
python generate_ml_datasets.py
```

---

## Dashboard Integration

Each dataset has a dedicated dashboard page with:

1. **Overview Tab**: Class distribution, key metrics, temporal trends
2. **Feature Analysis Tab**: Feature distributions, correlations, patterns
3. **Specialized Analysis Tab**: Domain-specific insights
4. **ML Preparation Tab**:
   - Feature type breakdown
   - Sample ML pipeline code
   - Dataset download capability
   - Best practices and tips

### Accessing the Dashboards

1. **Malware Detection**: 🦠 ML Security → Malware Detection
2. **Phishing Detection**: 🎣 ML Security → Phishing Detection
3. **CVE Intelligence**: 🔐 ML Security → CVE Intelligence

---

## ML Pipeline Examples

### Quick Start - Malware Detection

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv('data/malware_detection_dataset.csv')

# Prepare features
features = ['file_size_kb', 'entropy', 'api_calls_count',
            'network_connections', 'is_packed', 'obfuscated_code']
X = df[features]
y = df['is_malware']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
```

### Quick Start - Phishing Detection

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

# Load and prepare data
df = pd.read_csv('data/phishing_detection_dataset.csv')

features = ['url_length', 'has_https', 'ssl_valid', 'domain_age_days',
            'subdomain_count', 'redirects_count', 'suspicious_keywords']
X = df[features]
y = df['is_phishing']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
clf = GradientBoostingClassifier(n_estimators=100)
# ... (continue with train-test-split and evaluation)
```

### Quick Start - CVE Severity Prediction

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv('data/cve_vulnerability_dataset.csv')

# Prepare features
features = ['cvss_base_score', 'exploitability_score', 'impact_score',
            'has_exploit', 'patch_available']
X = df[features]

# Encode target
le = LabelEncoder()
y = le.fit_transform(df['severity'])  # LOW/MEDIUM/HIGH/CRITICAL → 0/1/2/3

# Train model
clf = RandomForestClassifier(n_estimators=200, class_weight='balanced')
# ... (continue with train-test-split and evaluation)
```

---

## Best Practices

### 1. Data Splitting
- Always use **stratified sampling** for imbalanced classes
- Typical split: 80% train, 20% test
- Consider validation set for hyperparameter tuning

### 2. Evaluation Metrics
- **Don't rely on accuracy alone** for imbalanced datasets
- Use: Precision, Recall, F1-Score, ROC-AUC
- For malware: Prefer high recall (catch all malware)
- For phishing: Balance precision and recall

### 3. Class Imbalance
- Use `class_weight='balanced'` in sklearn models
- Consider SMOTE for oversampling minority class
- Adjust classification threshold based on business needs

### 4. Feature Engineering
- Normalize/standardize numeric features
- One-hot encode categorical variables
- Create interaction features (e.g., entropy × is_packed)

### 5. Model Selection
- Start with Random Forest (good baseline)
- Try Gradient Boosting for better performance
- Use cross-validation for robust evaluation

---

## Integration with Existing Datasets

These ML datasets complement the existing dashboard datasets:

- **Global Cybersecurity Threats**: Macro-level threat intelligence
- **Intrusion Detection**: Network-level attack patterns
- **Malware Detection**: File-level threat analysis *(NEW)*
- **Phishing Detection**: URL/email threat analysis *(NEW)*
- **CVE Intelligence**: Vulnerability management *(NEW)*

Together, they provide **end-to-end cybersecurity coverage** from strategic threats to tactical detection.

---

## Future Enhancements

Potential additions:
- [ ] DDoS attack detection dataset
- [ ] Ransomware behavior patterns
- [ ] IoT security dataset
- [ ] Cloud security logs
- [ ] Mobile app security features
- [ ] Advanced Persistent Threat (APT) indicators

---

## Support

For questions or issues with the ML datasets:
1. Check the dashboard's ML Preparation tab for code examples
2. Review the `scripts/generate_ml_datasets.py` file for generation logic
3. Refer to the main project documentation in `/docs`

---

**Last Updated**: 2024
**Dashboard Version**: CyberGuard 2.0 with ML Extensions
