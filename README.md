# Cybersecurity Threat Analysis Dashboard

A Streamlit-powered dashboard for analyzing global cybersecurity threats alongside network intrusion patterns. This README has been streamlined to reflect the actual repository contents and provide precise setup instructions.

## Features
- Dashboard pages: Dashboard Overview, Global Threat Landscape, Intrusion Detection, Data Explorer, IDA/EDA Analysis, Comparative Insights, Methodology
- Consistent theming via centralized theme system (modules/theme.py)
- Robust data loading with clear guidance when datasets are missing
- Interactive filtering and downloadable data views

## Requirements
- Python 3.8+
- pip

## Installation
```
pip install -r requirements.txt
```

## Datasets
Place the following CSV files in the `data/` directory with exact filenames:
- `data/Global_Cybersecurity_Threats_2015-2024.csv`
- `data/cybersecurity_intrusion_data.csv`

If files are missing, the app will show an error and stop with instructions.

## Run locally
```
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

## Deploy to Streamlit Cloud
- Repo: point to this repository
- Main file: `app.py`
- Python version: 3.10 or 3.11
- Dependencies: `requirements.txt`
- Pre-run scripts: none
- Secrets: not required

If you encounter a theming or import error, make sure the app uses Streamlit >= 1.32 (we set this in requirements.txt) and redeploy.

## Project Structure
```
.
├── app.py
├── modules/
│   ├── home.py
│   ├── data_explorer.py
│   ├── data_analysis.py
│   ├── comparative_insights.py
│   ├── methodology.py
│   ├── filters.py
│   └── theme.py
├── data/
│   ├── Global_Cybersecurity_Threats_2015-2024.csv (you provide)
│   └── cybersecurity_intrusion_data.csv (you provide)
├── notebooks/
├── docs/
├── requirements.txt
└── LICENSE
```

## Documentation
For comprehensive documentation, see **[docs/CyberGuard_Dashboard_Documentation.md](docs/CyberGuard_Dashboard_Documentation.md)** which includes:
- 📖 Complete implementation guide
- 🎨 Design system and component documentation
- 🎛️ Filter system implementation guides
- 🧬 Data analysis methodology and reports
- 🎯 Quick reference guides by use case

## Notes
- All UI styling is centralized in `modules/theme.py` via `apply_dashboard_css()` to maintain consistency and avoid code duplication
- The theme system provides consistent colors, typography, and styling across all dashboard pages
- Redundant code and unused modules have been removed to reduce maintenance burden
- `data_analysis.py` includes comprehensive documentation for all analysis functions
- For advanced EDA and methodology details, see the docs/ folder and notebooks/

## License
MIT — see `LICENSE`.
