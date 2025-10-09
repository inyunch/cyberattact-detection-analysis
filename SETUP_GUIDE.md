# 🚀 Setup Guide - Cybersecurity Threat Analysis Dashboard

## Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Data Files

Ensure the following files are in the `data/` folder:
- `Global_Cybersecurity_Threats_2015-2024.csv`
- `cybersecurity_intrusion_data.csv`

### Step 3: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## Detailed Setup Instructions

### Prerequisites

- **Python:** 3.8 or higher
- **pip:** Latest version recommended
- **Git:** For cloning the repository

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cyberattact-detection-analysis.git
cd cyberattact-detection-analysis
```

#### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit >= 1.28.0
- pandas >= 2.0.0
- plotly >= 5.17.0
- numpy >= 1.24.0
- scipy >= 1.11.0

#### 4. Download Datasets (if not included)

If datasets are not in the `data/` folder:

1. Download from Kaggle:
   - [Global Cybersecurity Threats 2015-2024](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
   - [Cybersecurity Intrusion Detection Dataset](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset)

2. Place CSV files in the `data/` directory

#### 5. Run the Application

```bash
streamlit run app.py
```

---

## Exploring the Jupyter Notebooks

### Running IDA Notebook

```bash
jupyter notebook notebooks/01_Initial_Data_Analysis.ipynb
```

This notebook contains:
- Data loading and inspection
- Missing value analysis
- Duplicate detection
- Data quality checks
- Basic visualizations

### Running EDA Notebook

```bash
jupyter notebook notebooks/02_Exploratory_Data_Analysis.ipynb
```

This notebook contains:
- Temporal trend analysis
- Geographic patterns
- Correlation analysis
- Attack behavior analysis
- PCA dimensionality reduction
- 20+ comprehensive visualizations

---

## Dashboard Navigation

### 🏠 Home Page
- Project overview
- Key performance indicators (KPIs)
- Quick insights preview
- Navigation guide

### 🌍 Global Threat Landscape
- **Temporal Trends:** Attack frequency over time
- **Geographic Analysis:** Country and regional patterns
- **Sector Analysis:** Industry targeting patterns
- **Interactive Filters:** Year, country, sector, attack type

### 🔍 Intrusion Detection Analysis
- **Overview:** Classification distribution
- **Feature Analysis:** Distribution comparisons
- **Behavioral Patterns:** Login and session analysis
- **Interactive Filters:** Protocol, encryption, browser

### 📊 Comparative Insights
- Key findings from both datasets
- Cross-dataset visualizations
- Strategic recommendations
- Actionable insights

### 📖 Methodology
- Complete data dictionaries
- Data cleaning procedures
- Analysis methods
- Limitations and considerations

---

## Troubleshooting

### Issue: Module not found

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Check if port 8501 is in use
streamlit run app.py --server.port 8502
```

### Issue: Data files not loading

**Solution:**
1. Verify files are in `data/` folder
2. Check file names match exactly:
   - `Global_Cybersecurity_Threats_2015-2024.csv`
   - `cybersecurity_intrusion_data.csv`
3. Ensure CSV files are not corrupted

### Issue: Visualizations not displaying

**Solution:**
```bash
pip install --upgrade plotly
streamlit cache clear
```

---

## Development Mode

### Editing the Code

1. Make changes to files in `pages/` directory
2. Streamlit will automatically reload
3. Refresh browser to see changes

### Adding New Visualizations

Edit relevant page files:
- `pages/home.py`
- `pages/global_threats_page.py`
- `pages/intrusion_detection_page.py`
- `pages/comparative_insights.py`
- `pages/methodology.py`

### Custom Styling

CSS customization is in `app.py` under the `st.markdown()` section.

---

## Performance Tips

### For Large Datasets

1. **Use data caching:**
```python
@st.cache_data
def load_data():
    # Your data loading code
```

2. **Sample data for visualizations:**
```python
sample_data = data.sample(n=10000)
```

3. **Clear cache if needed:**
```bash
streamlit cache clear
```

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Deploy!

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## Project Structure

```
cyberattact-detection-analysis/
├── app.py                          # Main application entry point
├── pages/                          # Page modules
│   ├── home.py                     # Home page
│   ├── global_threats_page.py      # Global threats analysis
│   ├── intrusion_detection_page.py # Intrusion detection analysis
│   ├── comparative_insights.py     # Comparative analysis
│   └── methodology.py              # Documentation
├── notebooks/                      # Jupyter notebooks
│   ├── 01_Initial_Data_Analysis.ipynb
│   └── 02_Exploratory_Data_Analysis.ipynb
├── data/                           # Datasets
│   ├── Global_Cybersecurity_Threats_2015-2024.csv
│   └── cybersecurity_intrusion_data.csv
├── requirements.txt                # Dependencies
├── README_STREAMLIT.md            # Project README
├── MIDTERM_PLAN.md                # Detailed project plan
├── SETUP_GUIDE.md                 # This file
└── .gitignore                     # Git ignore rules
```

---

## FAQ

**Q: Can I use my own datasets?**

A: Yes! Replace the CSV files in the `data/` folder. You may need to adjust column names in the code.

**Q: How do I export visualizations?**

A: Use the download buttons in the dashboard or the camera icon in Plotly charts.

**Q: Can I customize the color scheme?**

A: Yes! Edit the CSS in `app.py` and color parameters in visualization functions.

**Q: How do I add more pages?**

A: Create a new file in `pages/` directory and add routing in `app.py`.

**Q: Is the data real or synthetic?**

A: The datasets are from Kaggle. Check the Methodology page for details on data sources and limitations.

---

## Support

For issues or questions:
1. Check this setup guide
2. Review the Methodology page in the dashboard
3. Open an issue on GitHub

---

## Next Steps

After setup:
1. ✅ Run the dashboard and explore
2. ✅ Review Jupyter notebooks for detailed analysis
3. ✅ Check MIDTERM_PLAN.md for project details
4. ✅ Read Methodology page for data insights
5. ✅ Customize for your needs!

**Happy analyzing! 🛡️📊**
