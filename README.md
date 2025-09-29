# Cyberattack Detection and Global Impact Analysis

## Project Overview

The goal of this project is to investigate cyberattacks from both granular technical (network/packet-level) and broader global perspectives. The narrative centers around understanding how attack behaviors observed in IoT network packet captures align with real-world cybersecurity incidents, trends, and organizational impacts. By bridging these layers, the project aims to deliver actionable insights into detection, risk management, and mitigation strategies.

## Why this matters

Cybersecurity is not just a technical challenge—it's a strategic risk. Organizations must understand both how attacks manifest on their networks and what large-scale impacts these incidents create across regions, industries, and timescales. By connecting the technical evidence with global trends, this project helps answer: Can early detection and behavior analysis prevent or contextualize serious breaches and losses?

## Datasets Used

1. **Kitsune Network Attack Dataset** (https://archive.ics.uci.edu/dataset/516/kitsune+network+attack+dataset)
    - Packet-level records for key IoT network attacks (e.g., OS scan, man-in-the-middle, DoS, botnet malware).
    - 115 engineered features per packet, with categorical labels (malicious/benign).
    - Used for behavioral analysis, anomaly detection, and attack classification.
2. **Global Cybersecurity Threats Dataset (2015–2024)** (https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
    - Incident-level global records: attack types, targeted sectors/countries, financial losses, vulnerabilities, resolutions.
    - Used for trend analysis and mapping technical detections to broader impacts.

## Project Narrative

Before diving into analysis or visualization, this project establishes a clear message:

- **What is the story?**
    - Technical detection helps organizations prevent major incidents. Insights at the network level may provide early warning for broader impacts.
    - Understanding connections between attack behavior and global incident patterns drives better mitigation strategies.
- **What are we trying to prove?**
    - Can specific packet behaviors provide leading indicators for global attack trends?
    - Do certain network violation types (confidentiality, integrity, authenticity) correlate with high-impact incidents globally?
    - What risk management recommendations emerge from linking fine-grained data to global impacts?

All visualizations will start by specifying the point or insight being communicated. Random or unhelpful charts will be avoided; every visual must relate to the core narrative.

## Features and Deliverables

- **Basic Requirements**
    - At least two distinct data sources, basic cleaning/imputation
    - Three or more visualization types driven by narrative/story
    - Exploratory analysis and statistical summaries of key variables
    - Handling missing data, encoding features appropriately
    - Streamlit app with at least two interactive elements (sidebars, tabs, dropdowns, filterable tables, etc.)
    - Basic documentation and usage instructions within the app
    - GitHub repository with README and setup instructions
- **Advanced Features**
    - Advanced cleaning, feature engineering (e.g., feature selection for ML models)
    - Enhanced interactive visualizations (e.g., confusion matrices, ROC/AUC, sector/region heatmaps)
    - Multiple machine learning models (attack detection/classification, trend prediction, clustering)
    - In-depth model comparison and evaluation
    - Model outputs for risk forecasting or real-time detection
    - Polished user interface and documentation in Streamlit

## App Structure

- Tabs/pages: "Packet-level Detection," "Global Incident Analysis," "Comparative Insights"
- Sidebars/dropdowns: Data source selection, variable selection, time filters
- Visualizations: Time-series, interactive dashboards, heatmaps, bar/treemaps, model performance charts
- Tables: Summary statistics, top attacks/impacts, feature importances
- Documentation: Embedded user help, project purpose, instructions, definitions

## Risk Mitigation

- If dataset integration proves too complex, results will be analyzed in parallel but contextualized through narrative links.
- Any data limitations or modeling constraints will be clearly documented in both the README and app.

## Getting Started

1. Clone this repository
2. Install requirements using `pip install -r requirements.txt`
3. Run the Streamlit app: `streamlit run app.py`
4. Explore source code and documentation for variable definitions and modeling walkthroughs

## Repository Structure

```
├── app.py                   # Main Streamlit app
├── data/                    # Data files and sources
├── notebooks/               # Exploratory analysis and prototyping
├── models/                  # ML scripts and serialized models
├── docs/                    # Documentation and data dictionary
├── README.md                # This file
└── requirements.txt         # Project dependencies
```

## Contact

Questions? Reach out via Teams or email as instructed in the syllabus.

---

Feel free to update as your workflow and insights develop!