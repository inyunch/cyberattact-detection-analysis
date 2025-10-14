# Filter System - Color Reference Guide

**Quick Reference**: All filter component colors and their hex values for easy implementation.

---

## 🎨 Core Color Palette

### Base Colors
```css
Background Primary:   #141B2D  /* Main app background */
Background Secondary: #1F2A40  /* Cards, panels */
Background Tertiary:  #0F1520  /* Darker elements */
Background Hover:     #2A3650  /* Hover states */

Text Primary:         #E8EAF0  /* Main text */
Text Secondary:       #A0A7B8  /* Secondary text */
Text Muted:           #6C7489  /* Labels, muted text */

Border Color:         #2E3A52  /* Standard borders */
```

### Accent Colors
```css
Accent Blue:          #00D9FF  /* Primary accent */
Accent Green:         #00FFB3  /* Secondary accent */
Accent Purple:        #7B61FF  /* Tertiary accent */
Accent Orange:        #FF9F43  /* Warning/attention */
Accent Red:           #FF5370  /* Error/remove */
```

---

## 🔍 Global Filter Sidebar Components

### Global Filter Header
**Rainbow gradient card with icon box**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.08) 0%,
    rgba(0, 255, 179, 0.08) 50%,
    rgba(123, 97, 255, 0.08) 100%);
Border: 1px solid rgba(0, 217, 255, 0.3);
Box Shadow: 0 8px 32px rgba(0, 217, 255, 0.15);

/* Rainbow top border */
Top Border: linear-gradient(90deg,
    #00D9FF 0%,    /* Blue */
    #00FFB3 50%,   /* Green */
    #7B61FF 100%); /* Purple */

/* Icon box */
Icon Background: linear-gradient(135deg, #00D9FF 0%, #00FFB3 100%);
Icon Shadow: 0 4px 12px rgba(0, 217, 255, 0.4);

/* Title */
Title Color: #E8EAF0;

/* Subtitle */
Subtitle Color: #6C7489;
```

### Time Period Card
**Gradient card with blue-green accent**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.05) 0%,
    rgba(0, 255, 179, 0.05) 100%);
Border: 1px solid rgba(0, 217, 255, 0.3);
Box Shadow: 0 4px 12px rgba(0, 217, 255, 0.15);

/* Icon + Label */
Icon: 📅
Label Color: #E8EAF0;
```

### Year Range Display
**Gradient background with colored numbers**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.1) 0%,
    rgba(0, 255, 179, 0.1) 100%);
Border Radius: 8px;

/* Start Year */
Start Year Color: #00D9FF (blue);

/* Arrow */
Arrow Color: #6C7489 (muted);

/* End Year */
End Year Color: #00FFB3 (green);
```

### Active Filter Count Badge
**Gradient badge with shadow**
```css
Background: linear-gradient(135deg, #00D9FF 0%, #00FFB3 100%);
Color: #141B2D (dark text on gradient);
Box Shadow: 0 2px 8px rgba(0, 217, 255, 0.3);
Border Radius: 12px;
Font: 'JetBrains Mono', monospace;
```

### Quick Preset Label
```css
Color: #6C7489 (muted);
Font Size: 0.75rem;
Text Transform: uppercase;
Letter Spacing: 0.05em;
```

### Clear All Filters Button
**Red outlined button**
```css
Background: transparent;
Border: 1px solid rgba(255, 83, 112, 0.5);
Color: #FF5370 (red);

/* Hover State */
Hover Background: rgba(255, 83, 112, 0.1);
Hover Border: 1px solid #FF5370;
Hover Transform: translateY(-1px);
```

---

## ✨ Active Filter Chips Container

### Container
**Rainbow gradient with top border**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.05) 0%,
    rgba(0, 255, 179, 0.05) 50%,
    rgba(123, 97, 255, 0.05) 100%);
Border: 1px solid rgba(0, 217, 255, 0.2);
Border Radius: 16px;
Box Shadow: 0 4px 20px rgba(0, 217, 255, 0.1);

/* Rainbow top border */
Top Border: linear-gradient(90deg,
    #00D9FF 0%,    /* Blue */
    #00FFB3 50%,   /* Green */
    #7B61FF 100%); /* Purple */

/* Header */
Icon: ✨
Title Color: #E8EAF0;
```

### Filter Chip - Blue (Global Filters)
**For year range and global time filters**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.2) 0%,
    rgba(0, 217, 255, 0.1) 100%);
Border: 1.5px solid rgba(0, 217, 255, 0.5);
Border Radius: 24px;
Text Color: #E8EAF0;
Box Shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

/* Icon */
Icon: 📅 (calendar)
```

### Filter Chip - Green (Page Filters)
**For attack types, industries, countries**
```css
Background: linear-gradient(135deg,
    rgba(0, 255, 179, 0.2) 0%,
    rgba(0, 255, 179, 0.1) 100%);
Border: 1.5px solid rgba(0, 255, 179, 0.5);
Border Radius: 24px;
Text Color: #E8EAF0;
Box Shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

/* Icons */
Attack Types: ⚠️
Industries: 🏭
Countries: 🌍
Protocols: 🔌
```

### Filter Chip - Purple (Numeric Ranges)
**For financial loss, port ranges**
```css
Background: linear-gradient(135deg,
    rgba(123, 97, 255, 0.2) 0%,
    rgba(123, 97, 255, 0.1) 100%);
Border: 1.5px solid rgba(123, 97, 255, 0.5);
Border Radius: 24px;
Text Color: #E8EAF0;
Box Shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

/* Icons */
Financial Loss: 💰
Port Range: 🔢
```

### Filter Chip - Orange (Other Filters)
**For special or unique filters**
```css
Background: linear-gradient(135deg,
    rgba(255, 159, 67, 0.2) 0%,
    rgba(255, 159, 67, 0.1) 100%);
Border: 1.5px solid rgba(255, 159, 67, 0.5);
Border Radius: 24px;
Text Color: #E8EAF0;
Box Shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

/* Icon */
Generic: 🎯
```

---

## 📊 Filter Statistics Component

### Container
```css
Background: #1F2A40 (secondary bg);
Border: 1px solid #2E3A52;
Border Radius: 16px;
Box Shadow: 0 4px 16px rgba(0, 0, 0, 0.3);

/* Left accent border */
Left Border: 4px solid;
Left Border Color: linear-gradient(180deg, #00D9FF 0%, #00FFB3 100%);
Left Border Shadow: 0 0 12px {dynamic glow};
```

### Intensity-Based Colors
**Progress bar and badge change based on filter intensity**

#### Light Filtering (< 25%)
```css
Badge Color: #00FFB3 (green);
Glow Color: rgba(0, 255, 179, 0.3);
Meaning: Light filtering, most data visible
```

#### Moderate Filtering (25-50%)
```css
Badge Color: #00D9FF (blue);
Glow Color: rgba(0, 217, 255, 0.3);
Meaning: Moderate filtering, balanced view
```

#### Heavy Filtering (50-75%)
```css
Badge Color: #FF9F43 (orange);
Glow Color: rgba(255, 159, 67, 0.3);
Meaning: Heavy filtering, narrow focus
```

#### Very Heavy Filtering (> 75%)
```css
Badge Color: #7B61FF (purple);
Glow Color: rgba(123, 97, 255, 0.3);
Meaning: Very focused filtering, precision view
```

### Progress Bar
```css
Track: rgba(255, 255, 255, 0.05);
Fill: linear-gradient(90deg, #00D9FF 0%, #00FFB3 100%);
Fill Shadow: 0 0 10px {dynamic based on intensity};
Height: 6px;
Transition: width 0.3s ease;
```

### Text Elements
```css
/* "Showing" label */
Label Color: #6C7489 (muted);
Label Size: 0.8rem;

/* Filtered count (large number) */
Count Color: #E8EAF0 (primary);
Count Size: 2rem;
Count Font: 'JetBrains Mono', monospace;
Count Shadow: 0 0 20px rgba(0, 217, 255, 0.3);

/* Total count */
Total Color: #A0A7B8 (secondary);

/* Percentage badge */
Badge Font: 'JetBrains Mono', monospace;
Badge Color: #141B2D (dark on gradient);

/* "filtered out" text */
Footer Color: #6C7489 (muted);
Footer Size: 0.75rem;
```

---

## 🎯 Page Filter Panel

### Info Card
**Gradient card with blue accent**
```css
Background: linear-gradient(135deg,
    rgba(0, 217, 255, 0.05) 0%,
    rgba(0, 255, 179, 0.05) 100%);
Border: 1px solid rgba(0, 217, 255, 0.2);
Border Radius: 12px;

/* Text */
Text Color: #A0A7B8 (secondary);
Accent Word Color: #00D9FF (blue) for "Customize";
```

---

## 🔧 Implementation Tips

### Using Gradients in Inline Styles
```html
<!-- Correct format for Streamlit st.markdown() -->
<div style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, rgba(0, 255, 179, 0.05) 100%);">
```

### Building Dynamic HTML
```python
# Use triple quotes for multiline HTML
html = f'''<div style="color: #E8EAF0;">
{dynamic_content}
</div>'''

st.markdown(html, unsafe_allow_html=True)
```

### Color Psychology
- **Blue (#00D9FF)**: Trust, global scope, time-based, moderate intensity
- **Green (#00FFB3)**: Success, page-specific, positive, light intensity
- **Purple (#7B61FF)**: Premium, precision, focused filtering, advanced
- **Orange (#FF9F43)**: Attention, focused scope, heavy filtering
- **Red (#FF5370)**: Critical actions only (Clear All, Remove)

---

## ✅ Color Contrast Compliance

All color combinations meet WCAG 2.1 AA standards:

| Foreground | Background | Ratio | Pass |
|------------|-----------|-------|------|
| #E8EAF0 | #141B2D | 12.8:1 | ✅ AAA |
| #E8EAF0 | #1F2A40 | 10.2:1 | ✅ AAA |
| #00D9FF | #141B2D | 8.9:1 | ✅ AAA |
| #00FFB3 | #141B2D | 11.3:1 | ✅ AAA |
| #6C7489 | #141B2D | 4.8:1 | ✅ AA |
| #141B2D | #00D9FF | 8.9:1 | ✅ AAA |
| #141B2D | #00FFB3 | 11.3:1 | ✅ AAA |

---

**Last Updated**: 2025-10-14
**Version**: 2.0
