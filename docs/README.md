# CyberGuard Dashboard Documentation

Complete documentation for the CyberGuard Threat Intelligence Dashboard - a modern cybersecurity analytics platform with light theme design.

---

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Project Structure
```
cyberattack-detection-analysis/
├── app.py                      # Main application entry point
├── modules/
│   ├── theme.py               # Centralized color system and styling
│   ├── filters.py             # Reusable filter components
│   ├── home.py                # Dashboard overview pages
│   ├── data_analysis.py       # IDA/EDA analysis
│   ├── comparative_insights.py # Cross-dataset insights
│   ├── data_encoding.py       # Data encoding guide
│   ├── data_explorer.py       # Data exploration tools
│   └── methodology.py         # Methodology documentation
├── data/                      # CSV datasets (not in repo)
└── docs/                      # Documentation (this file)
```

---

## 🎨 Design System

### Color Palette (Light Theme)
All colors are defined in `modules/theme.py` via the `COLORS` dictionary:

```python
COLORS = {
    "bg_primary": "#F8F9FA",        # Main background
    "bg_secondary": "#FFFFFF",      # Cards, panels
    "bg_tertiary": "#E9ECEF",       # Slightly darker
    "bg_hover": "#DEE2E6",          # Hover states

    "text_primary": "#1A1A1A",      # Main text
    "text_secondary": "#4A5568",    # Secondary text
    "text_muted": "#718096",        # Labels, muted

    "accent_blue": "#3182CE",       # Primary accent
    "accent_green": "#38A169",      # Secondary accent
    "accent_purple": "#805AD5",     # Tertiary accent
    "accent_orange": "#DD6B20",     # Warning/attention
    "accent_red": "#E53E3E",        # Error/destructive

    "border_color": "#E2E8F0",      # Borders
}
```

### Typography
- **Body**: Inter (sans-serif)
- **Code/Data**: JetBrains Mono (monospace)

### Key Principles
✅ **Always use COLORS constants** - Never hardcode hex values
✅ **Light theme** - Professional, clean appearance
✅ **Accessibility** - WCAG 2.1 AA compliant
✅ **Mobile-first** - Responsive design
✅ **Semantic HTML** - Proper ARIA attributes

---

## 🔧 Filter System

### Global Filters (Sidebar)
Applied to all pages, controlled in `modules/filters.py`:
- **Year Range**: Time period selection with dropdowns
- **Quick Presets**: 3Y, 5Y, All buttons
- **Clear All**: Reset all filters

### Page-Specific Filters

**Global Threat Landscape:**
- Attack Type (multiselect)
- Target Industry (multiselect)
- Country (multiselect)
- Financial Loss Range (slider)

**Intrusion Detection:**
- Protocol Type (multiselect)
- Attack Detected (toggle: Yes/No/Both)

### Implementation Pattern
```python
from modules.filters import (
    global_filter_sidebar,
    page_filter_panel_global_threats,
    apply_global_filters,
    apply_page_filters_global_threats,
    show_filter_stats
)

# Apply global filters
global_filters = global_filter_sidebar(global_threats)
filtered_data = apply_global_filters(df, global_filters)

# Apply page filters
page_filters = page_filter_panel_global_threats(filtered_data)
final_data = apply_page_filters_global_threats(filtered_data, page_filters)

# Show stats
show_filter_stats(len(df), len(final_data))
```

---

## 📊 Data Analysis

### Datasets

**1. Global Cybersecurity Threats (2015-2024)**
- 500 global cyber attack records
- Fields: Year, Attack Type, Country, Industry, Financial Loss
- Source: `data/Global_Cybersecurity_Threats_2015-2024.csv`

**2. Intrusion Detection Network Traffic**
- 12,000+ network traffic records
- Fields: protocol_type, service, flag, src_bytes, dst_bytes, attack_detected
- Source: `data/cybersecurity_intrusion_data.csv`

### Analysis Types

**Initial Data Analysis (IDA)**
- Data structure and types
- Missing value analysis (MICE imputation)
- Data quality assessment

**Exploratory Data Analysis (EDA)**
- Distribution analysis
- Correlation analysis
- Outlier detection
- Time series trends

**Comparative Insights**
- Cross-dataset comparisons
- Year-over-year analysis
- Industry benchmarking

---

## 🛠️ Development Guidelines

### Adding New Features

1. **Use the centralized color system:**
```python
from modules.theme import COLORS, SHADOWS

# Good
st.markdown(f'<div style="color: {COLORS["text_primary"]};">Text</div>')

# Bad - Never do this!
st.markdown('<div style="color: #1A1A1A;">Text</div>')
```

2. **Follow component patterns:**
```python
from modules.theme import apply_plotly_theme, st_observation_box

# Apply theme to charts
fig = apply_plotly_theme(fig, title="My Chart")

# Use observation boxes for insights
st_observation_box("Key Finding:", "Description here")
```

3. **Handle data loading:**
```python
@st.cache_data
def load_data():
    # Use caching for performance
    return pd.read_csv('data/file.csv')
```

### Code Quality Checklist
- [ ] Use `COLORS` constants (no hardcoded hex values)
- [ ] Apply `apply_plotly_theme()` to all charts
- [ ] Add ARIA labels for accessibility
- [ ] Test responsive behavior
- [ ] Cache data loading functions
- [ ] Follow existing component patterns

---

## 📈 Performance Optimization

### Caching Strategy
- `@st.cache_data` for data loading
- `@st.cache_resource` for model/connection objects
- Session state for filters and user selections

### Best Practices
- Minimize recomputation with caching
- Use efficient data structures (pandas)
- Lazy load large datasets
- Optimize Plotly chart rendering

---

## 🔐 Security Considerations

- No hard-coded credentials
- Input validation on all user inputs
- Safe HTML rendering (avoid XSS)
- Data sanitization before display
- HTTPS enforced in production

---

## 🐛 Troubleshooting

### Common Issues

**Colors not updating?**
- Clear Streamlit cache: `streamlit cache clear`
- Check `.streamlit/config.toml` theme settings
- Verify `COLORS` import in module

**Filters not working?**
- Check `st.session_state['global_filters']` initialization
- Verify filter functions are imported correctly
- Ensure data has required columns

**Charts not themed?**
- Confirm `apply_plotly_theme()` is called
- Check for hardcoded colors in chart config
- Verify theme.py is up to date

---

## 📝 Version History

### Latest (2025-01-25)
- Unified light theme color system
- Removed all hardcoded colors
- Centralized styling in `modules/theme.py`
- Simplified filter components
- Improved documentation structure

---

## 🤝 Contributing

1. Use consistent coding style (PEP 8)
2. Always reference `COLORS` dictionary
3. Test changes across all pages
4. Update documentation when adding features
5. Follow existing component patterns

---

**Need Help?** Check the inline code documentation in `modules/theme.py` and `modules/filters.py` for detailed implementation examples.
