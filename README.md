# Cybersecurity Threat Analysis Dashboard

Interactive dashboard for analyzing global cybersecurity threats and network intrusion patterns.

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Required Datasets
Place these files in the `data/` directory:
- `Global_Cybersecurity_Threats_2015-2024.csv`
- `cybersecurity_intrusion_data.csv`

### Run
```bash
streamlit run app.py
```
Open http://localhost:8501

## Features
- **Pages**: Dashboard Overview, Global Threat Landscape, Intrusion Detection, Data Explorer, IDA/EDA Analysis, Comparative Insights, Methodology
- **Theme**: Dark mode with neon accents (centralized in `modules/theme.py`)
- **Filters**: Interactive global and page-specific filters
- **Analysis**: Complete IDA/EDA with MICE imputation

## Project Structure
```
├── app.py                      # Main entry point
├── modules/
│   ├── theme.py               # Colors and styles
│   ├── filters.py             # Filter components
│   └── *.py                   # Page modules
├── data/                      # CSV datasets
└── docs/                      # Documentation
```

## Documentation
See **[docs/CyberGuard_Dashboard_Documentation.md](docs/CyberGuard_Dashboard_Documentation.md)** for:
- Complete implementation guide
- Design system and components
- Filter system guide
- Data analysis methodology

## Deploy to Streamlit Cloud
- Main file: `app.py`
- Python version: 3.10+
- Dependencies: `requirements.txt`

## License
MIT — see `LICENSE`
