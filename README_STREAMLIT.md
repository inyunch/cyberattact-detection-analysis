# 🛡️ Cybersecurity Threat Analysis Dashboard

An interactive Streamlit dashboard that combines global cybersecurity threat trends with network-level intrusion detection to reveal patterns in cyber attacks across time, geography, and attack vectors.

## 🎯 Project Overview

This platform provides both **macro-level** (global threats) and **micro-level** (network intrusion) analysis of cybersecurity threats, offering actionable insights for risk assessment and defense prioritization.

### Key Features

- 📊 **Interactive visualizations** with 20+ charts and graphs
- 🌍 **Global threat landscape** analysis (2015-2024)
- 🔍 **Network intrusion detection** pattern analysis
- 🎯 **Comparative insights** bridging both datasets
- 📖 **Comprehensive documentation** and methodology

## 📁 Datasets

### 1. Global Cybersecurity Threats Dataset (2015-2024)
- **Source:** [Kaggle](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
- **Purpose:** Macro-level trend analysis, geographic impact, sector vulnerability
- **Features:** Attack types, countries, financial losses, affected users, vulnerabilities

### 2. Cybersecurity Intrusion Detection Dataset
- **Source:** [Kaggle](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset)
- **Purpose:** Micro-level attack detection, behavior patterns, ML classification
- **Features:** Network packets, protocols, login attempts, session data, attack labels

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cyberattact-detection-analysis.git
cd cyberattact-detection-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure datasets are in the `data/` folder:
```
data/
├── Global_Cybersecurity_Threats_2015-2024.csv
└── cybersecurity_intrusion_data.csv
```

### Running the Dashboard

Launch the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Dashboard Pages

### 🏠 Home
- Project overview and key metrics
- Summary KPIs (total attacks, losses, detection rates)
- Quick insights preview
- Navigation guide

### 🌍 Global Threat Landscape
- **Temporal Trends:** Attack frequency over time, financial losses, growth rates
- **Geographic Analysis:** Country rankings, choropleth maps, regional distribution
- **Sector & Attack Type:** Heatmaps, treemaps, top vulnerabilities
- **Data Explorer:** Filterable tables, downloadable data

**Filters:** Year range, countries, industries, attack types

### 🔍 Intrusion Detection Analysis
- **Overview:** Classification distribution, protocol analysis, encryption patterns
- **Feature Distributions:** Violin plots, histograms, box plots for all features
- **Behavioral Analysis:** Login patterns, correlation matrices, 3D visualizations
- **Data Explorer:** Searchable tables, protocol/encryption breakdowns

**Filters:** Classification type, protocols, encryption, browser types

### 📊 Comparative Insights
- Key findings from both datasets
- Cross-dataset visualizations
- Strategic recommendations prioritized by severity
- Conceptual mapping between global threats and network indicators

### 📖 Methodology
- Complete data dictionaries for both datasets
- Data cleaning and preprocessing steps
- Analysis methods and techniques
- Limitations and considerations

## 🎨 Visualizations

The dashboard includes **20+ interactive visualizations**:

- Line charts (temporal trends)
- Bar charts (comparisons, rankings)
- Box plots (distribution analysis)
- Violin plots (feature distributions)
- Scatter plots (relationships, correlations)
- Heatmaps (cross-tabulations, correlations)
- Treemaps (hierarchical data)
- Choropleth maps (geographic distribution)
- 3D scatter plots (multivariate analysis)
- Pie charts (proportions)

All visualizations feature:
- ✅ Hover tooltips with detailed information
- ✅ Interactive filtering and zoom
- ✅ Colorblind-friendly palettes
- ✅ Responsive design

## 📈 Key Insights

Some findings from the analysis:

1. **📈 Exponential Growth:** Cyber attacks increased significantly from 2015-2024
2. **🎯 Protocol Vulnerability:** TCP protocol shows highest attack rates
3. **🏥 Sector Targeting:** Certain industries face disproportionate risk
4. **💰 Financial Impact:** Billions in documented losses over 10 years
5. **🔐 Behavioral Patterns:** Failed logins and unusual time access correlate with attacks

## 🛠️ Technology Stack

- **Python 3.x** - Programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computing
- **Scipy** - Statistical analysis

## 📋 Project Structure

```
cyberattact-detection-analysis/
├── app.py                          # Main Streamlit application
├── pages/                          # Page modules
│   ├── __init__.py
│   ├── home.py                     # Home page
│   ├── global_threats_page.py      # Global threats analysis
│   ├── intrusion_detection_page.py # Intrusion detection analysis
│   ├── comparative_insights.py     # Comparative analysis
│   └── methodology.py              # Documentation
├── data/                           # Datasets
│   ├── Global_Cybersecurity_Threats_2015-2024.csv
│   └── cybersecurity_intrusion_data.csv
├── requirements.txt                # Python dependencies
├── MIDTERM_PLAN.md                # Detailed project plan
└── README.md                      # This file
```

## 🎓 Academic Context

This project was developed as part of a data analytics course, demonstrating:

- ✅ Comprehensive data cleaning and preprocessing
- ✅ Advanced exploratory data analysis (EDA)
- ✅ Multiple visualization techniques
- ✅ Statistical analysis and correlation studies
- ✅ Interactive dashboard development
- ✅ Professional documentation

## ⚠️ Limitations

- Reporting bias: Not all incidents are publicly disclosed
- Geographic bias: Developed nations may be overrepresented
- Temporal lag: Data reflects past incidents
- Synthetic elements: Intrusion dataset may include simulated data
- Class imbalance: Typical of real-world security data

See the **Methodology** page in the dashboard for detailed discussion of limitations.

## 🔮 Future Enhancements

- [ ] Machine learning models for attack prediction
- [ ] Real-time threat intelligence integration
- [ ] Automated response playbooks
- [ ] Additional datasets (CVE database, threat feeds)
- [ ] Time-series forecasting
- [ ] Anomaly detection algorithms

## 📝 License

This project is for educational purposes. Datasets are sourced from Kaggle under their respective licenses.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**⚠️ Disclaimer:** This analysis is for educational and research purposes. All interpretations and recommendations should be validated with current threat intelligence before implementation in production environments.
