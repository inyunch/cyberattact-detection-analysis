# Midterm Project Plan

## Project Goal

**Primary Goal:** Develop an interactive analytical platform that combines global cybersecurity threat trends with network-level intrusion detection to reveal patterns in cyber attacks across time, geography, and attack vectors. This will provide actionable insights for risk assessment and defense prioritization.

**Midterm Milestone:** Complete comprehensive exploratory data analysis and build a functional Streamlit dashboard that visualizes threat landscapes, attack distributions, and intrusion patterns from both datasets, with interactive filtering and drill-down capabilities.

---

## Datasets

### 1. Global Cybersecurity Threats Dataset (2015–2024)
- **Source:** [Kaggle - Global Cybersecurity Threats 2015-2024](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
- **Purpose:** Provides incident-level global records including attack types, targeted sectors/countries, financial losses, vulnerabilities, and resolutions
- **Use Case:** Macro-level trend analysis, geographic impact assessment, sector vulnerability analysis

### 2. Cybersecurity Intrusion Detection Dataset
- **Source:** [Kaggle - Cybersecurity Intrusion Detection Dataset](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset)
- **Purpose:** Network traffic and user behavior-based features for intrusion detection
- **Use Case:** Micro-level attack detection, behavior pattern analysis, ML-based classification

---

## Data Description and Encoding Strategy

### Global Cybersecurity Threats Dataset
**Expected Variables:**
- **Temporal:** Year, Date/Time of incident
- **Geographic:** Country, Region
- **Categorical:** Attack Type, Targeted Sector/Industry, Vulnerability Type, Resolution Status
- **Numeric:** Financial Losses, Duration, Affected Users

**Encoding Requirements:**
- **One-Hot Encoding:** Attack Type, Sector, Country (for ML models)
- **Label Encoding:** Ordinal variables like severity levels (if present)
- **Temporal Encoding:** Extract year, month, quarter from dates
- **Binary Encoding:** Resolution status (resolved/unresolved)

### Cybersecurity Intrusion Detection Dataset
**Variables:**
- **Network Features:** Packet size (64-1500 bytes), Protocol type (TCP/UDP/ICMP), Encryption type (AES/DES/None)
- **User Behavior:** Login attempts, Session duration, Failed login counts, Unusual time access, IP reputation score, Browser type
- **Target:** Binary classification (1=attack, 0=normal)

**Encoding Requirements:**
- **One-Hot Encoding:** Protocol type, Encryption type, Browser type
- **Normalization/Scaling:** Packet size, session duration, login attempts, IP reputation score
- **Binary Variables:** Already binary (unusual time access, target variable)

---

## Initial Data Analysis (IDA) Strategy

### Step 1: Data Collection and Importation
- Download both datasets from Kaggle
- Import using pandas
- Store raw data in `data/raw/` directory
- Create data loading functions for reproducibility

### Step 2: Data Cleaning and Preprocessing
- **Missing Values:**
  - Quantify missing data percentage per column
  - Visualize missing patterns using missingno library
  - For Global Threats: Check for missing financial losses, countries, dates
  - For Intrusion Detection: Check for missing user behavior metrics
- **Duplicates:**
  - Identify and remove exact duplicates
  - Check for semantic duplicates (same incident reported differently)
- **Data Types:**
  - Convert date columns to datetime
  - Ensure numeric columns (losses, packet size) are float/int
  - Convert categorical variables to appropriate dtypes (category)
- **Standardization:**
  - Standardize country names (USA vs United States vs US)
  - Normalize attack type naming conventions
  - Consistent datetime formats

### Step 3: Variable Identification and Classification
- **Global Threats Dataset:**
  - Dependent: Attack severity, Financial losses (if predicting)
  - Independent: Year, Country, Sector, Attack Type, Vulnerability
  - Categorical: Attack Type, Sector, Country, Resolution Status
  - Numeric: Financial Losses, Year, Duration
  - Temporal: Date/Year
- **Intrusion Detection Dataset:**
  - Dependent: Attack detected (1/0)
  - Independent: All network and user behavior features
  - Categorical: Protocol, Encryption, Browser
  - Numeric: Packet size, login attempts, session duration, IP reputation

### Step 4: Basic Descriptive Statistics
- Calculate central tendencies (mean, median, mode) for:
  - Financial losses per attack type
  - Session duration for normal vs attack traffic
  - Login attempts distribution
- Calculate dispersion (std, variance, range) for:
  - Packet sizes
  - IP reputation scores
  - Temporal distributions of attacks
- Summary statistics tables for each dataset

### Step 5: Data Quality Assessment
- **Inconsistencies:**
  - Check for negative values in numeric fields (losses, durations)
  - Validate date ranges (2015-2024 for global threats)
  - Check protocol types match expected values (TCP/UDP/ICMP)
- **Accuracy:**
  - Cross-reference attack types with known cybersecurity taxonomies
  - Validate packet size ranges (64-1500 bytes)
- **Completeness:**
  - Calculate completeness ratio per column
  - Identify critical columns that must be complete

### Step 6: Missing Data Analysis
- **Quantification:**
  - Create missing data matrix
  - Calculate percentage missing per variable
  - Identify columns with >30% missing (consider dropping)
- **Patterns:**
  - Are financial losses missing for specific attack types?
  - Are user behavior metrics missing together (MCAR vs MAR vs MNAR)?
  - Correlation between missing values across columns
- **Imputation Strategy:**
  - Numeric: Mean/median for continuous, mode for discrete
  - Categorical: Mode or "Unknown" category
  - Advanced: KNN imputation for related features
  - Time-series: Forward/backward fill for temporal data

### Step 7: Outlier Detection
- **Methods:**
  - Z-score method (>3 standard deviations)
  - IQR method (1.5 * IQR beyond Q1/Q3)
  - Visual inspection via box plots
- **Target Variables:**
  - Financial losses (extreme high-value breaches)
  - Packet sizes (unusually large/small)
  - Login attempts (potential brute force indicators)
  - Session durations (extremely long sessions)
- **Treatment:**
  - Document outliers (may represent significant attacks like Equifax, SolarWinds)
  - Cap extreme values using winsorization
  - Keep outliers for analysis but flag them
  - Consider separate analysis for outlier vs normal incidents

---

## Exploratory Data Analysis (EDA) Strategy

### Step 1: Univariate Analysis

#### Global Threats Dataset:
- **Histograms:**
  - Distribution of attacks per year (trend analysis)
  - Financial losses distribution (likely right-skewed)
  - Attack frequency by type
- **Box Plots:**
  - Financial losses by attack type
  - Incident duration distributions
- **Bar Charts:**
  - Top 10 affected countries
  - Top 10 targeted sectors
  - Attack type frequency counts
- **Summary Statistics:**
  - Total losses by year
  - Average incident duration
  - Most common attack types

#### Intrusion Detection Dataset:
- **Histograms:**
  - Packet size distribution
  - Session duration distribution
  - Login attempts distribution
  - IP reputation score distribution
- **Box Plots:**
  - Packet size by protocol type
  - Session duration for attack vs normal
- **Bar Charts:**
  - Protocol type distribution
  - Encryption type distribution
  - Browser type distribution
  - Attack vs normal activity ratio
- **Summary Statistics:**
  - Average packet size per protocol
  - Mean session duration by classification
  - Failed login attempt averages

### Step 2: Bivariate Analysis

#### Global Threats Dataset:
- **Scatter Plots:**
  - Financial losses vs year (trend)
  - Attack frequency vs GDP (if country GDP data added)
  - Duration vs financial impact
- **Cross-Tabulations:**
  - Attack type × Sector (heatmap)
  - Country × Attack type
  - Year × Sector (evolution of targeted sectors)
- **Correlations:**
  - Financial losses vs attack duration
  - Temporal correlations (seasonal patterns)

#### Intrusion Detection Dataset:
- **Scatter Plots:**
  - Packet size vs session duration (colored by attack/normal)
  - Login attempts vs failed logins
  - IP reputation vs attack classification
- **Cross-Tabulations:**
  - Protocol type × Attack classification
  - Encryption type × Attack classification
  - Unusual time access × Attack classification
- **Correlations:**
  - Session duration vs login attempts
  - Failed logins vs attack classification
  - Packet size vs protocol type

### Step 3: Multivariate Analysis

#### Global Threats Dataset:
- **Correlation Matrix:**
  - Heatmap of numeric variables (losses, duration, year)
- **Grouped Analysis:**
  - Average losses by (Year, Sector)
  - Attack frequency by (Country, Attack Type)
- **Faceted Visualizations:**
  - Small multiples: Losses over time per sector
  - Grid plots: Top attack types per region

#### Intrusion Detection Dataset:
- **Correlation Matrix:**
  - Heatmap of all numeric features
  - Identify multicollinearity issues
- **PCA (Principal Component Analysis):**
  - Reduce dimensionality of user behavior features
  - Visualize attack vs normal separation in 2D/3D
- **Pair Plots:**
  - Key features colored by attack/normal
  - Identify feature interactions

### Step 4: Correlation Analysis

#### Global Threats Dataset:
- Pearson correlation for numeric variables
- Cramér's V for categorical associations
- Identify strongest predictors of financial losses
- Temporal autocorrelation (attacks cluster in time?)

#### Intrusion Detection Dataset:
- Pearson/Spearman correlation matrix
- Feature correlation with target (attack/normal)
- Identify redundant features (correlation >0.9)
- Point-biserial correlation (continuous vs binary target)

### Step 5: Dimensionality Assessment

#### Global Threats Dataset:
- Features: ~8-10 (manageable, no reduction needed initially)
- Observations: Depends on dataset size (likely 1000s)
- Consider feature engineering:
  - Attack severity score (composite)
  - Country risk index
  - Temporal features (quarter, year_month)

#### Intrusion Detection Dataset:
- Features: ~10-12
- Observations: Unknown (check samples vs features ratio)
- **If p > 0.5*n:** Consider PCA or feature selection
- **Feature Selection:**
  - Chi-square test for categorical features
  - ANOVA F-test for numeric features
  - Recursive Feature Elimination (RFE)
- **Feature Engineering:**
  - Interaction terms (protocol × encryption)
  - Binning packet sizes (small/medium/large)

### Step 6: Pattern and Trend Identification

#### Global Threats Dataset:
- **Temporal Trends:**
  - Year-over-year attack growth rate
  - Emerging attack types over time
  - Seasonal patterns (monthly/quarterly analysis)
- **Geographic Patterns:**
  - Regional clustering of attacks
  - Country risk evolution over time
- **Sector Patterns:**
  - Which sectors are increasingly targeted?
  - Sector-specific attack type preferences

#### Intrusion Detection Dataset:
- **Behavioral Patterns:**
  - Typical attack signatures (high login attempts + unusual time)
  - Protocol preferences for attacks
  - Encryption correlation with attack types
- **Clustering:**
  - K-means clustering to identify attack subtypes
  - DBSCAN for anomaly detection
- **Time-based Patterns:**
  - Unusual time access patterns
  - Session duration anomalies

### Step 7: Hypothesis Generation

#### Global Threats Dataset:
1. **H1:** Financial losses have increased exponentially over time
2. **H2:** Certain sectors (finance, healthcare) have disproportionately higher losses
3. **H3:** Ransomware attacks show higher average losses than other attack types
4. **H4:** Developed nations report higher losses due to better reporting infrastructure
5. **H5:** Attack frequency correlates with global digitalization trends

#### Intrusion Detection Dataset:
1. **H1:** Attacks are characterized by higher login failure rates
2. **H2:** TCP protocol is more commonly used in attacks than UDP/ICMP
3. **H3:** Unusual time access is a strong predictor of attacks
4. **H4:** Lower IP reputation scores correlate with attack classification
5. **H5:** Encrypted traffic (AES/DES) may show different attack patterns than unencrypted

---

## Data Imbalance Handling

### Expected Imbalances

#### Global Threats Dataset:
- **Geographic:** Some countries over-represented (US, EU vs developing nations)
- **Sectoral:** Finance/tech sectors likely over-represented
- **Attack Types:** Common attacks (phishing, malware) vs rare (zero-days)
- **Temporal:** Recent years may have more data than earlier years

#### Intrusion Detection Dataset:
- **Class Imbalance:** Normal traffic likely >> Attack traffic (typical ratio 95:5 or worse)

### Handling Strategies

#### For Analysis and Visualization:
1. **Weighted Visualizations:**
   - Show both counts AND percentages
   - Use logarithmic scales for skewed distributions
   - Create normalized heatmaps
2. **Stratified Sampling:**
   - Sample proportionally for exploratory plots
   - Maintain class ratios in subsets
3. **Separate Analysis:**
   - Analyze minority classes separately
   - Create dedicated views for rare attack types

#### For Machine Learning (Final Project):
1. **Resampling:**
   - SMOTE (Synthetic Minority Over-sampling) for attack class
   - Random under-sampling of majority class
   - Combination approaches
2. **Algorithmic:**
   - Class weights in model training
   - Cost-sensitive learning
   - Ensemble methods (balanced random forest)
3. **Evaluation:**
   - Use precision, recall, F1-score (not just accuracy)
   - ROC-AUC, PR-AUC curves
   - Confusion matrix analysis

#### For Midterm Specifically:
- **Document imbalance ratios** in both datasets
- **Visualize class distributions** clearly
- **Acknowledge limitations** in conclusions
- **Show both raw and balanced views** in dashboard
- **Use stratified splits** if showing sample data

---

## Visualization Plan

### Visualization Strategy and Rationale

#### Principle: Every visualization must answer a specific question

### Global Threats Dataset Visualizations

#### 1. Time-Series Line Chart: Attack Frequency Over Time
- **Type:** Line chart with trend line
- **Variables:** Year (x-axis) vs Attack Count (y-axis), colored by Attack Type
- **Question:** How has the frequency of cyberattacks evolved from 2015-2024?
- **Rationale:**
  - Line charts best show temporal trends
  - Multiple lines reveal which attack types are growing/declining
  - Trend line shows overall trajectory
- **Interactivity:** Toggle attack types on/off, hover for exact counts

#### 2. Geographic Heatmap: Global Attack Distribution
- **Type:** Choropleth map
- **Variables:** Country (geography) vs Total Attacks or Total Losses (color intensity)
- **Question:** Which countries/regions are most affected by cyberattacks?
- **Rationale:**
  - Geographic data demands geographic visualization
  - Color intensity immediately shows high-risk regions
  - Reveals global patterns (concentrated in developed nations?)
- **Interactivity:** Tooltip with country details, filter by year/attack type

#### 3. Treemap: Financial Losses by Sector and Attack Type
- **Type:** Treemap (hierarchical)
- **Variables:** Sector (top level) → Attack Type (nested) → Size = Financial Losses
- **Question:** Which sectors and attack types cause the most financial damage?
- **Rationale:**
  - Treemap shows hierarchical part-to-whole relationships
  - Rectangle size immediately conveys magnitude
  - Nesting reveals sector + attack type interaction
  - More engaging than stacked bar chart
- **Interactivity:** Click to drill down, tooltip with exact losses

#### 4. Grouped Bar Chart: Top Attack Types by Frequency
- **Type:** Horizontal bar chart (sorted)
- **Variables:** Attack Type (y-axis) vs Count (x-axis)
- **Question:** What are the most common attack types?
- **Rationale:**
  - Bar charts best for categorical comparisons
  - Horizontal orientation better for long category names
  - Sorted by frequency for immediate insights
- **Interactivity:** Filter by year range, sector

#### 5. Box Plot: Loss Distribution by Attack Type
- **Type:** Box and whisker plot
- **Variables:** Attack Type (x-axis) vs Financial Losses (y-axis, log scale)
- **Question:** Which attack types have the highest and most variable losses?
- **Rationale:**
  - Box plots show distribution, not just averages
  - Reveals outliers (mega-breaches)
  - Log scale handles wide range of losses
  - Shows variability/risk
- **Interactivity:** Toggle outliers, hover for details

#### 6. Heatmap: Attack Type × Sector Frequency
- **Type:** 2D heatmap
- **Variables:** Attack Type (x-axis) × Sector (y-axis) → Color = Frequency
- **Question:** Which sectors are targeted by which attack types?
- **Rationale:**
  - Heatmap best shows relationships between two categorical variables
  - Color gradient reveals patterns (e.g., ransomware → healthcare)
  - Compact representation of many data points
- **Interactivity:** Filter by year, hover for counts

### Intrusion Detection Dataset Visualizations

#### 7. Stacked Bar Chart: Attack vs Normal by Protocol Type
- **Type:** Stacked or grouped bar chart
- **Variables:** Protocol Type (x-axis) vs Count (y-axis), stacked by Attack/Normal
- **Question:** Which network protocols are associated with attacks?
- **Rationale:**
  - Shows both total volume and attack proportion per protocol
  - Stacking reveals class imbalance
  - Easy comparison across protocols
- **Interactivity:** Toggle between counts and percentages

#### 8. Violin Plot: Session Duration Distribution by Classification
- **Type:** Violin plot (or box plot + KDE)
- **Variables:** Classification (Attack/Normal) vs Session Duration
- **Question:** Do attacks have different session duration patterns?
- **Rationale:**
  - Violin plot shows full distribution shape
  - Better than box plot for seeing bimodality
  - Direct visual comparison of attack vs normal
- **Interactivity:** Toggle between features (duration, packet size, login attempts)

#### 9. Scatter Plot: Login Attempts vs Failed Logins (colored by Classification)
- **Type:** 2D scatter plot with color encoding
- **Variables:** Login Attempts (x) vs Failed Logins (y), color = Attack/Normal
- **Question:** How do login behaviors differ between attacks and normal activity?
- **Rationale:**
  - Scatter plot reveals correlation and clustering
  - Color separation shows class separability
  - Brute force attacks should cluster (high attempts + failures)
- **Interactivity:** Brush selection, zoom, filter by other features

#### 10. Correlation Heatmap: Feature Correlations
- **Type:** Correlation matrix heatmap
- **Variables:** All numeric features
- **Question:** Which features are correlated and potentially redundant?
- **Rationale:**
  - Standard EDA practice
  - Identifies multicollinearity before modeling
  - Reveals feature relationships
- **Interactivity:** Hover for correlation values, hierarchical clustering

#### 11. Bar Chart: Feature Importance (if using simple model)
- **Type:** Horizontal bar chart
- **Variables:** Feature names (y) vs Importance score (x)
- **Question:** Which features are most predictive of attacks?
- **Rationale:**
  - Validates EDA findings
  - Guides future feature engineering
  - Communicates model insights
- **Interactivity:** Filter by model type (if comparing multiple)

### Dashboard Summary Visualizations

#### 12. KPI Cards: Summary Statistics
- **Type:** Metric cards / KPI indicators
- **Variables:**
  - Total attacks (2015-2024)
  - Total financial losses
  - Most targeted sector
  - Most common attack type
  - Average loss per attack
  - Detection accuracy (from intrusion dataset)
- **Question:** What are the key summary metrics?
- **Rationale:**
  - Executive summary for quick insights
  - Anchors the dashboard
  - Provides context for detailed visuals
- **Interactivity:** Update based on filters (year, region)

### Design Choices Rationale

#### Color Scheme:
- **Sequential:** Blue gradient for single-variable intensity (losses, counts)
- **Diverging:** Red-Yellow-Green for correlations (-1 to +1)
- **Categorical:** Distinct colors for attack types (max 10 colors, use colorblind-friendly palette like Set2 or Tab10)
- **Binary:** Red (attack) vs Blue (normal) for classification

#### Chart Selection Logic:
- **Comparison:** Bar charts (categorical), box plots (distributions)
- **Trends:** Line charts (time-series)
- **Relationships:** Scatter plots (2 numeric), heatmaps (2 categorical or correlation)
- **Part-to-whole:** Treemap (hierarchical), pie chart (avoid unless <5 categories)
- **Distribution:** Histograms, violin plots, box plots
- **Geographic:** Choropleth maps

#### Accessibility:
- Colorblind-friendly palettes
- Text labels on critical values
- High contrast for readability
- Alternative text for screen readers (in final app)

---

## Streamlit App Layout and Logic

### App Structure

#### Navigation: Sidebar + Multi-page Layout
- **Page 1:** 🏠 Home / Project Overview
- **Page 2:** 🌍 Global Threat Landscape
- **Page 3:** 🛡️ Intrusion Detection Analysis
- **Page 4:** 📊 Comparative Insights
- **Page 5:** 📖 Data Dictionary & Methodology

### Page-by-Page Layout

---

### Page 1: 🏠 Home / Project Overview

**Purpose:** Orient users, explain project goals, provide navigation guidance

**Layout:**
```
[Header: Project Title + Tagline]

[Row 1: KPI Cards - Summary Metrics]
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Total       │ Total       │ Detection   │ Years       │
│ Attacks     │ Losses      │ Accuracy    │ Covered     │
│ 12,543      │ $45.2B      │ 94.3%       │ 2015-2024   │
└─────────────┴─────────────┴─────────────┴─────────────┘

[Row 2: Two Columns]
┌────────────────────────────┬────────────────────────────┐
│ Project Goals & Questions  │ Quick Insights             │
│                            │                            │
│ • Temporal trends?         │ [Mini time-series preview] │
│ • Geographic patterns?     │ [Mini map preview]         │
│ • Attack signatures?       │ [Mini bar chart]           │
└────────────────────────────┴────────────────────────────┘

[Row 3: Navigation Guide]
"Explore the data using the sidebar navigation..."
```

**Interactive Elements:**
- None (static overview)

**Rationale:**
- Provides context before deep dive
- KPIs give immediate value
- Navigation guide reduces confusion

---

### Page 2: 🌍 Global Threat Landscape

**Purpose:** Explore macro-level cybersecurity trends from Global Threats Dataset

**Sidebar Filters (Persistent across all visualizations on this page):**
```
📅 Year Range: [2015] ━━━━●━━━━ [2024]
🌍 Regions: ☑ All / ☐ North America / ☐ Europe / ☐ Asia / ☐ Other
🏢 Sectors: ☑ All / ☐ Finance / ☐ Healthcare / ☐ Technology / ...
🎯 Attack Types: ☑ All / ☐ Ransomware / ☐ Phishing / ☐ DDoS / ...
```

**Main Panel Layout:**
```
[Tab 1: Temporal Trends]
┌──────────────────────────────────────────────────────────┐
│ Line Chart: Attack Frequency Over Time                   │
│ (Multiple lines for attack types)                        │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Box Plot: Loss Distribution by Attack Type               │
└──────────────────────────────────────────────────────────┘

[Tab 2: Geographic Analysis]
┌──────────────────────────────────────────────────────────┐
│ Choropleth Map: Global Attack Distribution               │
└──────────────────────────────────────────────────────────┘
┌───────────────────────┬──────────────────────────────────┐
│ Top 10 Countries      │ Regional Breakdown Pie Chart     │
│ (Bar Chart)           │                                  │
└───────────────────────┴──────────────────────────────────┘

[Tab 3: Sector & Attack Type Analysis]
┌──────────────────────────────────────────────────────────┐
│ Treemap: Financial Losses by Sector → Attack Type        │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Heatmap: Attack Type × Sector Frequency                  │
└──────────────────────────────────────────────────────────┘

[Tab 4: Data Explorer]
┌──────────────────────────────────────────────────────────┐
│ Filterable Data Table (top 100 rows)                     │
│ [Download CSV button]                                    │
└──────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
1. Sidebar filters (apply to all visualizations)
2. Tabs for organizing content
3. Hover tooltips on all charts
4. Clickable legend items (toggle visibility)
5. Zoom/pan on time-series and map
6. Downloadable data table

**Logic:**
- Filters update ALL visualizations reactively
- Tabs prevent overwhelming single-page scroll
- Data table allows power users to explore raw data

**Rationale:**
- Organized by analysis type (temporal, geographic, categorical)
- Filters enable drill-down (e.g., "Show only ransomware in healthcare 2020-2024")
- Tabs maintain focus while offering depth

---

### Page 3: 🛡️ Intrusion Detection Analysis

**Purpose:** Explore micro-level network intrusion patterns

**Sidebar Filters:**
```
🔍 Classification: ☑ All / ☐ Attack / ☐ Normal
📡 Protocol: ☑ All / ☐ TCP / ☐ UDP / ☐ ICMP
🔐 Encryption: ☑ All / ☐ AES / ☐ DES / ☐ None
🌐 Browser: ☑ All / ☐ Chrome / ☐ Firefox / ...
```

**Main Panel Layout:**
```
[Tab 1: Classification Overview]
┌───────────────────────┬──────────────────────────────────┐
│ KPI Cards             │ Pie Chart: Attack vs Normal      │
│ • Total Records       │                                  │
│ • Attack %            │                                  │
│ • Normal %            │                                  │
└───────────────────────┴──────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Stacked Bar: Attack vs Normal by Protocol                │
└──────────────────────────────────────────────────────────┘

[Tab 2: Feature Distributions]
┌──────────────────────────────────────────────────────────┐
│ Dropdown: Select Feature                                 │
│ [Packet Size ▼] [Session Duration] [Login Attempts] ...  │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Violin Plot: Selected Feature by Classification          │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Histogram: Distribution (with attack/normal overlay)     │
└──────────────────────────────────────────────────────────┘

[Tab 3: Behavioral Analysis]
┌──────────────────────────────────────────────────────────┐
│ Scatter Plot: Login Attempts vs Failed Logins            │
│ (Colored by Classification)                              │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ Correlation Heatmap: All Numeric Features                │
└──────────────────────────────────────────────────────────┘

[Tab 4: Data Explorer]
┌──────────────────────────────────────────────────────────┐
│ Filterable Data Table with Search                        │
│ [Download CSV button]                                    │
└──────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
1. Sidebar filters (protocol, encryption, etc.)
2. Dropdown for feature selection (Tab 2)
3. Searchable/sortable data table
4. Hover tooltips
5. Brushing on scatter plot (select points to see details)

**Logic:**
- Feature dropdown allows users to explore any variable without creating 10+ static plots
- Correlation heatmap clickable to generate corresponding scatter plot (stretch goal)
- Filters apply globally

**Rationale:**
- Reduces redundancy (one violin plot component, multiple features)
- Behavioral analysis tab focuses on attack signatures
- Data explorer empowers technical users

---

### Page 4: 📊 Comparative Insights

**Purpose:** Bridge both datasets, find connections

**Sidebar Filters:**
```
[Filters from both datasets combined, where applicable]
```

**Main Panel Layout:**
```
[Section 1: Key Findings]
┌──────────────────────────────────────────────────────────┐
│ "What we learned..."                                     │
│                                                          │
│ 💡 Insight 1: Attack frequency increased 340% from 2015  │
│ 💡 Insight 2: TCP protocol accounts for 78% of attacks   │
│ 💡 Insight 3: Healthcare sector shows highest growth     │
│ ...                                                      │
└──────────────────────────────────────────────────────────┘

[Section 2: Cross-Dataset Visualizations]
┌──────────────────────────────────────────────────────────┐
│ Side-by-Side Comparison:                                 │
│ [Global trends line chart] | [Intrusion detection rate]  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Attack Type Mapping (if possible):                       │
│ • Ransomware (global) ↔ Encryption patterns (intrusion)  │
│ • DDoS (global) ↔ Packet size anomalies (intrusion)      │
└──────────────────────────────────────────────────────────┘

[Section 3: Recommendations]
┌──────────────────────────────────────────────────────────┐
│ "Based on this analysis..."                              │
│                                                          │
│ 🎯 Prioritize monitoring TCP traffic in healthcare       │
│ 🎯 Invest in login attempt anomaly detection             │
│ 🎯 Focus defenses on top 5 attack types                  │
└──────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
- Expandable insight cards
- Toggle between different comparison views

**Logic:**
- Synthesizes findings from both datasets
- Provides actionable takeaways
- Demonstrates analytical thinking

**Rationale:**
- Shows you can integrate disparate data sources conceptually
- Provides value beyond raw visualizations
- Demonstrates storytelling (key for midterm)

---

### Page 5: 📖 Data Dictionary & Methodology

**Purpose:** Documentation, transparency, reproducibility

**Layout:**
```
[Tab 1: Data Sources]
• Dataset 1: Global Threats
  - Source, size, date range
  - Variables and descriptions
• Dataset 2: Intrusion Detection
  - Source, size, features

[Tab 2: Methodology]
• Data cleaning steps
• Imputation strategies
• Encoding methods
• Limitations and assumptions

[Tab 3: Code & Reproducibility]
• Link to GitHub repo
• How to run locally
• Dependencies
```

**Rationale:**
- Fulfills documentation requirement
- Builds credibility
- Helps graders understand your process

---

### Overall App Logic Flow

```
User Journey:

1. Land on Home → See KPIs and project goals → Orient
2. Click "Global Threats" → Filter by year/sector → Explore trends
3. Click "Intrusion Detection" → Select feature → Analyze distributions
4. Click "Insights" → Read findings → Understand conclusions
5. Click "Methodology" → See how it was done → Trust results
```

### Technical Implementation Plan

#### Streamlit Components:
- `st.sidebar` for filters
- `st.tabs()` for organizing content
- `st.columns()` for side-by-side layouts
- `st.metric()` for KPI cards
- `st.plotly_chart()` for interactive visualizations (Plotly Express/Graph Objects)
- `st.dataframe()` with filtering for data tables
- `st.download_button()` for CSV exports
- `st.selectbox()`, `st.multiselect()`, `st.slider()` for inputs

#### Libraries:
- **Data:** pandas, numpy
- **Visualization:** plotly express, plotly graph objects, seaborn (static), matplotlib
- **Maps:** plotly choropleth (built-in)
- **Missing data viz:** missingno
- **Stats:** scipy, statsmodels

#### State Management:
- Use `st.session_state` to persist filter selections across pages
- Cache data loading with `@st.cache_data`
- Cache expensive computations

#### Deployment:
- Streamlit Community Cloud (free, easy GitHub integration)
- Alternative: Heroku, AWS (if needed)

---

## Above and Beyond Elements (Target A Grade)

### 6. Advanced Data Techniques (5%)
- ✅ Multiple imputation methods (mean, median, KNN, iterative)
- ✅ Comparison of imputation effectiveness (visualize before/after)
- ✅ Advanced cleaning: regex for standardizing country names, attack type taxonomy mapping

### 7. Sophisticated Analysis and Visualization (5%)
- ✅ Interactive Plotly visualizations (zoom, filter, hover, drill-down)
- ✅ Animated time-series (if time permits): watch attacks spread geographically over time
- ✅ 3D scatter plot for multivariate analysis (if dimensionality reduction applied)
- ✅ Advanced heatmaps with hierarchical clustering

### 8. Advanced Data Processing (5%)
- ✅ Compare Simple Imputer vs KNN Imputer vs Iterative Imputer
- ✅ Document MCAR/MAR/MNAR patterns
- ✅ Sensitivity analysis: how do results change with different imputation strategies?

### 9. Enhanced App Features (5%)
- ✅ Polished UI: custom CSS, branded color scheme, professional layout
- ✅ Export functionality: download filtered data, download plots as PNG
- ✅ Advanced filters: date range slider, multi-select with search
- ✅ Tooltips and help icons explaining metrics
- ✅ Loading animations for data processing
- ✅ Responsive layout (works on mobile)

### 10. Project Complexity and Originality (5%)
- ✅ Dual-dataset integration (macro + micro perspectives)
- ✅ Creative linking of disparate data sources through narrative
- ✅ Original insights (not just reproducing Kaggle kernels)
- ✅ Domain expertise demonstrated (cybersecurity context)
- ✅ Clear storytelling arc throughout app

---

## Timeline and Milestones

### Week 1: Data Collection and IDA ✅ COMPLETED
- [x] Download and import datasets
- [x] Initial data profiling (shape, types, missing values)
- [x] Data cleaning (duplicates, types, standardization)
- [x] Missing data analysis and imputation
- [x] Outlier detection and treatment
- [x] Deliverable: Clean datasets saved to `data/processed/`
- [x] **BONUS:** Created comprehensive IDA Jupyter notebook

### Week 2: EDA and Visualization Development ✅ COMPLETED
- [x] Univariate analysis (histograms, box plots, bar charts)
- [x] Bivariate analysis (scatter, cross-tabs, correlations)
- [x] Multivariate analysis (correlation matrix, PCA if needed)
- [x] Create all 12 planned visualizations
- [x] Hypothesis generation and documentation
- [x] Deliverable: Jupyter notebook with full EDA
- [x] **BONUS:** Created comprehensive EDA Jupyter notebook with 20+ visualizations

### Week 3: Streamlit App Development ✅ COMPLETED
- [x] Set up Streamlit app structure (multi-page)
- [x] Implement Home page with KPIs
- [x] Implement Global Threats page with filters + visualizations
- [x] Implement Intrusion Detection page
- [x] Implement Comparative Insights page
- [x] Implement Methodology/Documentation page
- [x] Deliverable: Functional local Streamlit app
- [x] **BONUS:** Implemented 20+ interactive Plotly visualizations across all pages

### Week 4: Refinement and Deployment 🔄 IN PROGRESS
- [x] Polish UI/UX (CSS, layout, colors)
- [x] Add interactivity enhancements
- [x] Write in-app documentation
- [ ] Test on different screen sizes
- [ ] Deploy to Streamlit Cloud
- [ ] Update GitHub README with live link
- [ ] Final testing and bug fixes
- [ ] Deliverable: Deployed app + GitHub repo

---

## Success Criteria

### Base Requirements (80% - B grade):
- ✅ Two distinct datasets integrated
- ✅ Comprehensive data cleaning documented
- ✅ 3+ visualization types (we have 10+)
- ✅ Statistical summaries of key variables
- ✅ Missing data handling (imputation)
- ✅ Functional Streamlit app with 2+ interactive elements (we have 10+)
- ✅ Clear in-app documentation
- ✅ Deployed and accessible online
- ✅ GitHub repo with README

### Above and Beyond (20% - A grade):
- ✅ Advanced data cleaning (regex, taxonomy mapping)
- ✅ Multiple imputation method comparison
- ✅ Interactive, advanced visualizations (Plotly, animations)
- ✅ Polished, professional UI
- ✅ Original insights and creative approach
- ✅ Complex dual-dataset narrative

---

## Risk Mitigation

### Potential Challenges:

1. **Dataset integration complexity:**
   - Mitigation: Analyze datasets in parallel, link through narrative rather than direct joins
   - Backup: Focus on one dataset if integration proves infeasible

2. **Imbalanced intrusion detection data:**
   - Mitigation: Document imbalance, use stratified sampling for visualizations
   - Backup: Focus on EDA rather than ML for midterm (ML in final)

3. **Missing data exceeds 50% in critical columns:**
   - Mitigation: Drop those columns, document decision
   - Backup: Use proxy variables or aggregate to higher level

4. **Deployment issues on Streamlit Cloud:**
   - Mitigation: Test early, use requirements.txt, check resource limits
   - Backup: Deploy on alternative platform (Heroku) or submit video demo

5. **Time constraints:**
   - Mitigation: Prioritize base requirements first, add enhancements iteratively
   - Backup: Reduce number of visualizations, simplify app layout

---

## Deliverables Checklist

### GitHub Repository:
- [x] README.md with project overview, setup instructions, live app link
- [x] MIDTERM_PLAN.md (this document)
- [x] requirements.txt
- [x] /data/ folder with raw and processed data (or instructions to download)
- [x] /notebooks/ with EDA Jupyter notebooks (IDA + EDA)
- [x] /app.py or /pages/ for Streamlit app
- [x] .gitignore (exclude large files, API keys)

### Streamlit App:
- [x] Home page with project overview and KPIs
- [x] Global Threats analysis page
- [x] Intrusion Detection analysis page
- [x] Comparative Insights page
- [x] Methodology/Data Dictionary page
- [ ] Deployed and accessible via URL

### Documentation:
- [x] In-app documentation (tooltips, help text, methodology page)
- [x] Code comments in app.py
- [x] EDA notebook with markdown explanations
- [x] README with clear setup instructions

### Completed Files:
```
cyberattact-detection-analysis/
├── app.py ✅
├── pages/ ✅
│   ├── __init__.py
│   ├── home.py
│   ├── global_threats_page.py
│   ├── intrusion_detection_page.py
│   ├── comparative_insights.py
│   └── methodology.py
├── notebooks/ ✅
│   ├── 01_Initial_Data_Analysis.ipynb
│   └── 02_Exploratory_Data_Analysis.ipynb
├── data/ ✅
│   ├── Global_Cybersecurity_Threats_2015-2024.csv
│   └── cybersecurity_intrusion_data.csv
├── requirements.txt ✅
├── README_STREAMLIT.md ✅
├── MIDTERM_PLAN.md ✅ (updated)
└── .gitignore ✅
```

---

## Questions for Instructor (If Needed)

1. Are we expected to integrate the datasets through joins, or is parallel analysis with narrative linking acceptable?
2. For the intrusion detection dataset, should we focus on EDA or include basic ML classification for the midterm?
3. Is there a preferred deployment platform, or is Streamlit Cloud acceptable?
4. What is the expected depth of the "advanced imputation comparison"? (visual comparison vs. statistical tests?)
5. Should the app include any real-time data fetching, or are static datasets sufficient?

---

**End of Midterm Plan**
