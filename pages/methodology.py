import streamlit as st

def show():
    """Display methodology and data dictionary"""

    st.title("📖 Data Dictionary & Methodology")
    st.markdown("### Documentation, Sources, and Reproducibility")
    st.markdown("---")

    # Create tabs for organization
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Data Sources",
        "🧹 Data Cleaning",
        "📊 Analysis Methods",
        "⚠️ Limitations"
    ])

    # TAB 1: Data Sources
    with tab1:
        st.markdown("## 📁 Data Sources and Variables")

        # Global Threats Dataset
        st.markdown("### 🌍 Global Cybersecurity Threats Dataset (2015-2024)")

        st.info("""
        **Source:** [Kaggle - Global Cybersecurity Threats 2015-2024](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)

        **Description:** This dataset provides incident-level global records of cybersecurity threats,
        including attack types, targeted sectors and countries, financial losses, vulnerabilities, and resolutions.

        **Time Period:** 2015-2024 (10 years)

        **Purpose:** Macro-level trend analysis, geographic impact assessment, sector vulnerability analysis
        """)

        st.markdown("#### Variable Dictionary")

        global_vars = {
            "Variable": [
                "Country",
                "Year",
                "Attack Type",
                "Target Industry",
                "Financial Loss (in Million $)",
                "Number of Affected Users",
                "Attack Source",
                "Security Vulnerability Type",
                "Defense Mechanism Used",
                "Incident Resolution Time (in Hours)"
            ],
            "Type": [
                "Categorical",
                "Temporal",
                "Categorical",
                "Categorical",
                "Numeric (Continuous)",
                "Numeric (Discrete)",
                "Categorical",
                "Categorical",
                "Categorical",
                "Numeric (Continuous)"
            ],
            "Description": [
                "Country where the attack occurred",
                "Year of the incident (2015-2024)",
                "Type of cyber attack (e.g., Ransomware, Phishing, DDoS)",
                "Industry sector targeted (e.g., Finance, Healthcare, Retail)",
                "Financial losses in millions of USD",
                "Number of users/accounts affected",
                "Origin of attack (e.g., Hacker Group, Nation-state, Insider)",
                "Type of security vulnerability exploited",
                "Security defense mechanism that was in place",
                "Time taken to resolve the incident in hours"
            ]
        }

        st.table(global_vars)

        st.markdown("---")

        # Intrusion Detection Dataset
        st.markdown("### 🔍 Cybersecurity Intrusion Detection Dataset")

        st.info("""
        **Source:** [Kaggle - Cybersecurity Intrusion Detection Dataset](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset)

        **Description:** Network traffic and user behavior-based features designed for intrusion detection.
        Contains both normal traffic and attack patterns with labeled classifications.

        **Purpose:** Micro-level attack detection, behavior pattern analysis, ML-based classification
        """)

        st.markdown("#### Variable Dictionary")

        intrusion_vars = {
            "Variable": [
                "session_id",
                "network_packet_size",
                "protocol_type",
                "login_attempts",
                "session_duration",
                "encryption_used",
                "ip_reputation_score",
                "failed_logins",
                "browser_type",
                "unusual_time_access",
                "attack_detected"
            ],
            "Type": [
                "Identifier",
                "Numeric (Discrete)",
                "Categorical",
                "Numeric (Discrete)",
                "Numeric (Continuous)",
                "Categorical",
                "Numeric (Continuous)",
                "Numeric (Discrete)",
                "Categorical",
                "Binary",
                "Binary (Target)"
            ],
            "Description": [
                "Unique session identifier",
                "Size of network packet in bytes (typically 64-1500)",
                "Network protocol used (TCP, UDP, ICMP)",
                "Number of login attempts in session",
                "Duration of session in seconds",
                "Type of encryption used (AES, DES, None)",
                "Reputation score of source IP (0-1 scale)",
                "Number of failed login attempts",
                "Web browser type used",
                "Whether access occurred during unusual hours (0=normal, 1=unusual)",
                "Target variable: attack detected (0=normal, 1=attack)"
            ]
        }

        st.table(intrusion_vars)

    # TAB 2: Data Cleaning
    with tab2:
        st.markdown("## 🧹 Data Cleaning and Preprocessing")

        st.markdown("### Data Quality Assessment")

        st.markdown("""
        The following data cleaning steps were performed to ensure data quality and consistency:
        """)

        st.markdown("#### 1. Initial Data Inspection")
        st.code("""
# Load and inspect datasets
global_threats = pd.read_csv('Global_Cybersecurity_Threats_2015-2024.csv')
intrusion_data = pd.read_csv('cybersecurity_intrusion_data.csv')

# Check shape, dtypes, missing values
print(global_threats.info())
print(intrusion_data.info())
        """, language='python')

        st.markdown("#### 2. Missing Data Analysis")

        st.warning("""
        **Missing Data Strategy:**

        - **Quantification:** Calculate percentage of missing values per column
        - **Pattern Analysis:** Identify if data is Missing Completely at Random (MCAR), Missing at Random (MAR),
          or Missing Not at Random (MNAR)
        - **Treatment:**
            - Numeric variables: Mean/median imputation for minor missingness (<10%)
            - Categorical variables: Mode imputation or "Unknown" category
            - Columns with >30% missing: Consider dropping or flagging
        """)

        st.markdown("#### 3. Data Type Conversion")

        st.code("""
# Ensure correct data types
global_threats['Year'] = global_threats['Year'].astype(int)
global_threats['Financial Loss (in Million $)'] = pd.to_numeric(
    global_threats['Financial Loss (in Million $)']
)

# Convert categorical variables for efficiency
categorical_cols = ['Country', 'Attack Type', 'Target Industry']
for col in categorical_cols:
    global_threats[col] = global_threats[col].astype('category')
        """, language='python')

        st.markdown("#### 4. Outlier Detection and Treatment")

        st.info("""
        **Outlier Detection Methods:**

        1. **Z-score method:** Identify values >3 standard deviations from mean
        2. **IQR method:** Flag values beyond 1.5 × IQR from Q1/Q3
        3. **Domain knowledge:** Validate extreme values (e.g., major breaches like Equifax)

        **Treatment Approach:**
        - Document outliers (may represent significant real events)
        - Keep outliers but flag them for analysis
        - Consider separate analysis for outlier vs. normal incidents
        - Use robust statistics (median, IQR) alongside mean/std
        """)

        st.markdown("#### 5. Data Standardization")

        st.markdown("""
        - **Country names:** Standardized variations (USA → United States)
        - **Attack type naming:** Consistent capitalization and terminology
        - **Datetime formats:** Uniform date representations
        """)

        st.markdown("#### 6. Duplicate Removal")

        st.code("""
# Check for and remove exact duplicates
duplicates = global_threats.duplicated().sum()
global_threats = global_threats.drop_duplicates()

# Check for semantic duplicates (manual inspection required)
        """, language='python')

    # TAB 3: Analysis Methods
    with tab3:
        st.markdown("## 📊 Analysis Methods and Techniques")

        st.markdown("### Exploratory Data Analysis (EDA) Approach")

        st.markdown("#### 1. Univariate Analysis")

        st.success("""
        **For Numeric Variables:**
        - Histograms for distribution visualization
        - Box plots to identify outliers and quartiles
        - Summary statistics (mean, median, std, min, max)

        **For Categorical Variables:**
        - Bar charts for frequency counts
        - Pie charts for proportion visualization (when <5 categories)
        - Value counts and percentage distributions
        """)

        st.markdown("#### 2. Bivariate Analysis")

        st.success("""
        **Numeric × Numeric:**
        - Scatter plots to visualize relationships
        - Correlation coefficients (Pearson, Spearman)

        **Categorical × Numeric:**
        - Box plots grouped by category
        - Violin plots for distribution comparison
        - Group statistics and comparisons

        **Categorical × Categorical:**
        - Cross-tabulation (contingency tables)
        - Heatmaps for frequency visualization
        - Chi-square tests for independence
        """)

        st.markdown("#### 3. Multivariate Analysis")

        st.success("""
        **Techniques Applied:**
        - Correlation matrices for all numeric features
        - Heatmaps with hierarchical clustering
        - Faceted visualizations (small multiples)
        - 3D scatter plots for three-variable relationships
        - Principal Component Analysis (PCA) for dimensionality assessment
        """)

        st.markdown("#### 4. Time Series Analysis")

        st.code("""
# Temporal trend analysis
attacks_by_year = global_threats.groupby('Year').size()

# Calculate year-over-year growth
yoy_growth = attacks_by_year.pct_change() * 100

# Identify trends using linear regression
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(
    attacks_by_year.index, attacks_by_year.values
)
        """, language='python')

        st.markdown("#### 5. Geographic Analysis")

        st.markdown("""
        - Choropleth maps for global distribution
        - Country-level aggregations
        - Regional comparisons and clustering
        """)

        st.markdown("### Visualization Strategy")

        st.info("""
        **Chart Selection Principles:**

        - **Comparison:** Bar charts (categorical), box plots (distributions)
        - **Trends:** Line charts (time-series), area charts
        - **Relationships:** Scatter plots (2 numeric), heatmaps (2 categorical)
        - **Part-to-whole:** Treemaps (hierarchical), pie charts (<5 categories)
        - **Distribution:** Histograms, violin plots, density plots
        - **Geographic:** Choropleth maps, bubble maps

        **Design Guidelines:**
        - Colorblind-friendly palettes (avoid red-green combinations)
        - High contrast for readability
        - Interactive elements for exploration (hover, zoom, filter)
        - Clear axis labels and titles
        - Consistent color schemes across related visualizations
        """)

        st.markdown("### Statistical Techniques")

        st.markdown("""
        **Descriptive Statistics:**
        - Central tendency: mean, median, mode
        - Dispersion: standard deviation, variance, IQR
        - Distribution: skewness, kurtosis

        **Inferential Statistics:**
        - Correlation analysis (Pearson, Spearman, Point-biserial)
        - Hypothesis testing (when applicable)
        - Confidence intervals for key metrics

        **Feature Analysis (Intrusion Detection):**
        - Feature correlation with target variable
        - Feature importance (using simple models)
        - Multicollinearity detection
        """)

    # TAB 4: Limitations
    with tab4:
        st.markdown("## ⚠️ Limitations and Considerations")

        st.markdown("### Data Limitations")

        limitations = [
            {
                "area": "Reporting Bias",
                "description": "Not all cyber incidents are reported or publicly disclosed. Actual attack volumes "
                              "may be significantly higher than recorded.",
                "impact": "High",
                "mitigation": "Acknowledge in conclusions; focus on trends rather than absolute numbers"
            },
            {
                "area": "Geographic Bias",
                "description": "Developed nations with better reporting infrastructure may be overrepresented "
                              "compared to developing countries.",
                "impact": "Medium",
                "mitigation": "Analyze per-capita or normalize by digitalization metrics when possible"
            },
            {
                "area": "Temporal Bias",
                "description": "Recent years may have more complete data due to improved detection and "
                              "reporting requirements.",
                "impact": "Medium",
                "mitigation": "Note trend interpretations; consider percentage changes rather than absolute growth"
            },
            {
                "area": "Attribution Challenges",
                "description": "Attack source attribution is difficult and may be inaccurate, especially for "
                              "sophisticated nation-state actors.",
                "impact": "Medium",
                "mitigation": "Treat attack source data as indicative rather than definitive"
            },
            {
                "area": "Financial Loss Estimation",
                "description": "Financial losses are estimates and may not include indirect costs, reputational "
                              "damage, or long-term impacts.",
                "impact": "High",
                "mitigation": "Present as lower bounds; acknowledge true costs likely higher"
            },
            {
                "area": "Synthetic/Simulated Data",
                "description": "The intrusion detection dataset may be partially synthetic or simulated for "
                              "research purposes.",
                "impact": "Medium",
                "mitigation": "Validate patterns against known attack signatures; use for conceptual insights"
            },
            {
                "area": "Class Imbalance",
                "description": "Intrusion detection data shows imbalance between attack and normal traffic, "
                              "typical of real-world scenarios but challenging for analysis.",
                "impact": "Medium",
                "mitigation": "Use stratified sampling, weighted metrics, and acknowledge in visualizations"
            },
            {
                "area": "Lack of Direct Integration",
                "description": "The two datasets operate at different levels (macro vs. micro) and cannot be "
                              "directly joined or merged.",
                "impact": "Low",
                "mitigation": "Use comparative narrative approach; find conceptual rather than statistical links"
            }
        ]

        for lim in limitations:
            impact_color = "🔴" if lim['impact'] == "High" else "🟡" if lim['impact'] == "Medium" else "🟢"

            with st.expander(f"{impact_color} {lim['area']} [{lim['impact']} Impact]"):
                st.markdown(f"**Description:** {lim['description']}")
                st.markdown(f"**Mitigation:** {lim['mitigation']}")

        st.markdown("---")

        st.markdown("### Methodological Considerations")

        st.warning("""
        **Important Considerations:**

        1. **Causation vs. Correlation:** All analyses present correlations and associations. Causal relationships
           cannot be definitively established without controlled experiments.

        2. **External Validity:** Findings may not generalize to all organizations or contexts. Each organization
           has unique risk profiles.

        3. **Temporal Lag:** Data reflects past incidents. Current threat landscape may have evolved since data
           collection.

        4. **Missing Variables:** Many relevant factors (organization size, security maturity, budget) are not
           captured in the datasets.

        5. **Sampling Bias:** The datasets represent observed and reported incidents, not the entire population
           of cyber threats.
        """)

        st.markdown("---")

        st.markdown("### Assumptions")

        st.info("""
        **Key Assumptions Made in This Analysis:**

        - Reported incidents are representative of broader trends
        - Data collection methods were consistent across time periods
        - Missing data patterns do not systematically bias results
        - Attack classifications are accurate and standardized
        - Financial loss estimates follow consistent methodologies
        - Network intrusion patterns in dataset reflect real-world attack behaviors
        """)

        st.markdown("---")

        st.markdown("### Recommended Next Steps")

        st.success("""
        **To Address Limitations and Extend Analysis:**

        1. **Data Enrichment:** Integrate additional data sources (threat intelligence feeds, CVE databases)
        2. **Machine Learning:** Develop predictive models for attack classification and risk scoring
        3. **Real-time Integration:** Connect to live threat feeds for up-to-date analysis
        4. **Longitudinal Studies:** Continue tracking trends as new data becomes available
        5. **Cross-validation:** Validate findings against independent datasets or expert assessments
        6. **Sector-specific Deep Dives:** Conduct focused analyses on high-risk industries
        7. **Cost-benefit Analysis:** Model ROI of security investments based on threat data
        """)

    # Footer
    st.markdown("---")

    st.markdown("## 📚 References and Additional Resources")

    st.markdown("""
    **Datasets:**
    - [Global Cybersecurity Threats 2015-2024 - Kaggle](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
    - [Cybersecurity Intrusion Detection Dataset - Kaggle](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset)

    **Technologies Used:**
    - **Python 3.x** - Programming language
    - **Streamlit** - Web application framework
    - **Pandas** - Data manipulation and analysis
    - **Plotly** - Interactive visualizations
    - **NumPy** - Numerical computing

    **Frameworks and Standards:**
    - MITRE ATT&CK Framework
    - NIST Cybersecurity Framework
    - ISO 27001 Information Security Standards
    """)

    st.markdown("---")

    st.caption("*This project was developed as part of a data analysis course. All interpretations and recommendations "
              "should be validated with current threat intelligence before implementation.*")
