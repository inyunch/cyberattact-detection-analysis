# Cybersecurity Threat Analysis Dashboard

A Streamlit-powered dashboard for analyzing global cybersecurity threats alongside network intrusion patterns. This README has been streamlined to reflect the actual repository contents and provide precise setup instructions.

## Features
- Dashboard pages: Dashboard Overview, Global Threat Landscape, Intrusion Detection, Data Explorer, IDA/EDA Analysis, Comparative Insights, Methodology
- Consistent theming via centralized utilities (modules/ui_utils.py)
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

## Run
```
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

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
│   ├── ui_utils.py
│   └── components.py
├── data/
│   ├── Global_Cybersecurity_Threats_2015-2024.csv (you provide)
│   └── cybersecurity_intrusion_data.csv (you provide)
├── notebooks/
├── docs/
├── requirements.txt
└── LICENSE
```

## Notes
- All UI styling is applied via `modules/ui_utils.apply_base_css()` to avoid large inline CSS in `app.py`.
- Unused page modules were removed from `modules/` to reduce maintenance burden.
- For advanced EDA and methodology details, see the docs/ folder and notebooks/.

## License
MIT — see `LICENSE`.
