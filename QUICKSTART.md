# ⚡ Quick Start Guide

## 🚀 Run the Dashboard (1 Command)

```bash
streamlit run app.py
```

That's it! The dashboard opens at `http://localhost:8501`

---

## 📊 What You'll Find

### In the Streamlit Dashboard:

1. **🏠 Home** - Overview and KPIs
2. **📊 IDA/EDA Analysis** - Statistical analysis with 20+ charts ⭐ NEW!
3. **🌍 Global Threats** - Attack trends and geographic patterns
4. **🔍 Intrusion Detection** - Network traffic analysis
5. **📈 Comparative Insights** - Key findings and recommendations
6. **📖 Methodology** - Complete documentation

### In the Jupyter Notebooks:

1. **01_Initial_Data_Analysis.ipynb** - Data quality and basic stats
2. **02_Exploratory_Data_Analysis.ipynb** - 50+ advanced visualizations

---

## 💻 Installation (First Time Only)

```bash
# Install all dependencies
pip install -r requirements.txt
```

---

## 📁 File Locations

- **Dashboard:** `app.py`
- **Notebooks:** `notebooks/`
- **Data:** `data/`
- **Docs:** `README_STREAMLIT.md`, `SETUP_GUIDE.md`, `MIDTERM_PLAN.md`

---

## 🎯 Key Features

✅ 60+ interactive visualizations
✅ Real-time filtering
✅ Download filtered data
✅ Statistical analysis (correlation, PCA)
✅ Geographic heat maps
✅ 3D scatter plots
✅ Attack behavior analysis

---

## 🆘 Troubleshooting

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Module not found?**
```bash
pip install --upgrade -r requirements.txt
```

**Data not loading?**
- Verify files in `data/` folder:
  - `Global_Cybersecurity_Threats_2015-2024.csv`
  - `cybersecurity_intrusion_data.csv`

---

## 📖 More Help

- **Detailed Setup:** See `SETUP_GUIDE.md`
- **Project Plan:** See `MIDTERM_PLAN.md`
- **Full README:** See `README_STREAMLIT.md`

---

**Ready to explore! 🛡️📊**
