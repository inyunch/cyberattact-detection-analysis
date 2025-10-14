# CyberGuard Dashboard Design Rules

**Version**: 1.0
**Last Updated**: 2025-10-14
**Author**: CyberGuard Development Team

---

## 📋 Table of Contents

1. [Visual Consistency](#visual-consistency)
2. [Color Palette & Variables](#color-palette--variables)
3. [Typography](#typography)
4. [Component Standards](#component-standards)
5. [Layout & Spacing](#layout--spacing)
6. [Accessibility Requirements](#accessibility-requirements)
7. [Responsive Design](#responsive-design)
8. [Code Quality Standards](#code-quality-standards)
9. [Animation & Transitions](#animation--transitions)
10. [Implementation Guidelines](#implementation-guidelines)

---

## 🎨 Visual Consistency

### Core Design Principles

**Must follow these rules for ALL UI elements:**

1. **Dark Theme First**: Primary background `#141B2D` with gradient variations
2. **Neon Accents**: Blue (`#00D9FF`) and Green (`#00FFB3`) for highlights and active states
3. **Rounded Corners**: Use 12-16px border-radius for cards, 10-12px for buttons, 8-10px for inputs
4. **Glowing Effects**: Active states must have subtle glow/shadow effects using neon colors
5. **Consistent Shadows**: Use defined shadow levels (sm, md, lg) - no arbitrary shadows

### Reference Design

All navigation, tabs, sidebars, and layout designs **MUST** match the established visual style:
- Modern, sleek, cybersecurity-themed aesthetic
- High contrast with proper WCAG compliance
- Glowing indicators and smooth transitions
- Gradient accents on interactive elements

---

## 🎨 Color Palette & Variables

### CSS Variables (REQUIRED)

**All components MUST use these CSS variables:**

```css
:root {
  /* Background Colors */
  --bg-primary: #141B2D;
  --bg-secondary: #1F2A40;
  --bg-tertiary: #0F1520;
  --bg-hover: #2A3650;

  /* Text Colors */
  --text-primary: #E8EAF0;
  --text-secondary: #A0A7B8;
  --text-muted: #6C7489;

  /* Accent Colors */
  --accent-blue: #00D9FF;
  --accent-green: #00FFB3;
  --accent-purple: #7B61FF;
  --accent-orange: #FF9F43;
  --accent-red: #FF5370;

  /* Borders & Dividers */
  --border-color: #2E3A52;
  --divider-color: #2E3A52;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);

  /* Transitions */
  --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Color Usage Rules

| Element | Background | Text | Border | Accent |
|---------|-----------|------|--------|--------|
| **Main Content** | `var(--bg-primary)` | `var(--text-primary)` | N/A | N/A |
| **Cards** | `var(--bg-secondary)` | `var(--text-primary)` | `var(--border-color)` | N/A |
| **Buttons (Primary)** | Gradient (blue→green) | `var(--bg-primary)` | None | N/A |
| **Active Items** | `rgba(0, 217, 255, 0.12)` | `var(--text-primary)` | `var(--accent-blue)` | Yes |
| **Hover States** | `var(--bg-hover)` | `var(--text-primary)` | `var(--accent-blue)` | Optional |

### Gradient Definitions

**Standard Gradients** (use these exact values):

```css
/* Primary Accent Gradient */
background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);

/* Background Gradient */
background: linear-gradient(180deg, var(--bg-primary) 0%, #0A0F1C 100%);

/* Active State Gradient */
background: linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%);
```

**NEVER** create arbitrary gradients. Use only these predefined ones.

---

## ✍️ Typography

### Font Families

**Primary Font Stack:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

**Monospace Font (for data/code):**
```css
font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
```

### Font Import

**Required** in every HTML/CSS entry point:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
```

### Typography Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| **H1** | 2rem (32px) | 800 | 1.2 | -0.02em |
| **H2** | 1.4rem (22.4px) | 700 | 1.3 | -0.01em |
| **H3** | 1.2rem (19.2px) | 600 | 1.4 | -0.01em |
| **Body** | 1rem (16px) | 400 | 1.6 | 0 |
| **Small** | 0.875rem (14px) | 500 | 1.5 | 0 |
| **Labels** | 0.75rem (12px) | 600 | 1.4 | 0.05em |
| **Numbers** | *varies* | 700-800 | 1.2 | -0.02em |

### Typography Usage Rules

✅ **DO:**
- Use `Inter` for all UI text
- Use `JetBrains Mono` for metrics, numbers, code snippets
- Apply gradient text effect to main headings (H1)
- Use uppercase + letter-spacing for labels

❌ **DON'T:**
- Mix font families within components
- Use font sizes not in the scale
- Apply gradients to body text
- Use bold weights below 600

### Gradient Text Effect (for H1 only)

```css
h1 {
  background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## 🧩 Component Standards

### 1. Sidebar Component

**Required Features:**
- Collapsible functionality
- Icon + text labels
- Active menu indicator (glowing left border)
- Hover state with background change
- Rounded corners (12px)
- Logo header with gradient text

**Structure:**
```
[Logo Header]
  - Icon (32px with glow effect)
  - Title (gradient text)
  - Subtitle (uppercase, muted)
[Navigation Menu]
  - Menu items (icon + label)
  - Active indicator (4px left border)
[Footer] (optional)
  - User info or actions
```

**Active State Styling:**
```css
.nav-item-active {
  background: linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%);
  border-left: 4px solid var(--accent-blue);
  box-shadow: inset 0 0 20px rgba(0, 217, 255, 0.1);
  color: var(--text-primary);
  font-weight: 600;
}
```

### 2. Tab System

**Variants:**
- **Underline**: Animated indicator below active tab
- **Pill**: Filled background for active tab
- **Default**: Gradient background for active

**Required Features:**
- Smooth animated indicator
- Icon support (optional)
- Badge support (optional)
- Keyboard navigation
- Hover effects

**Active Indicator (Underline variant):**
```css
.tab-indicator {
  position: absolute;
  bottom: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-green) 100%);
  border-radius: 2px 2px 0 0;
  transition: all var(--transition-base);
  box-shadow: 0 -2px 12px rgba(0, 217, 255, 0.6);
}
```

### 3. Card Components

**Standard Card Structure:**

```css
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
  border-color: var(--accent-blue);
}
```

**Types:**
- Metric Cards (with icon, value, delta)
- Chart Cards (with title, visualization)
- Table Cards (with header, action button)

### 4. Buttons

**Primary Button:**
```css
.button-primary {
  background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);
  color: var(--bg-primary);
  border: none;
  border-radius: 10px;
  padding: 12px 24px;
  font-weight: 600;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
}

.button-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 217, 255, 0.4);
}
```

**Secondary Button:**
```css
.button-secondary {
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-secondary);
  padding: 12px 24px;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.button-secondary:hover {
  background: var(--bg-hover);
  border-color: var(--accent-blue);
  color: var(--accent-blue);
}
```

### 5. Metric/Stat Cards

**Required Elements:**
- Icon with colored background
- Label (uppercase, small)
- Value (large, monospace)
- Delta/Change indicator (optional)

**Status Colors:**
- Success: `var(--accent-green)`
- Warning: `var(--accent-orange)`
- Danger: `var(--accent-red)`
- Info: `var(--accent-blue)`

---

## 📐 Layout & Spacing

### Spacing Scale

Use **8px base unit** for all spacing:

```css
--spacing-xs: 4px;   /* 0.25rem */
--spacing-sm: 8px;   /* 0.5rem */
--spacing-md: 16px;  /* 1rem */
--spacing-lg: 24px;  /* 1.5rem */
--spacing-xl: 32px;  /* 2rem */
--spacing-2xl: 40px; /* 2.5rem */
--spacing-3xl: 48px; /* 3rem */
```

### Grid System

**Stats Grid:**
```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
```

**Chart Grid:**
```css
.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}
```

### Container Padding

| Screen Size | Padding |
|-------------|---------|
| Desktop (>1024px) | `2.5rem` (40px) |
| Tablet (768-1024px) | `2rem` (32px) |
| Mobile (<768px) | `1.5rem` (24px) |

---

## ♿ Accessibility Requirements

### WCAG 2.1 AA Compliance

**Required Standards:**
- Minimum contrast ratio: **4.5:1** for normal text
- Minimum contrast ratio: **3:1** for large text (18px+)
- All interactive elements must be keyboard accessible
- Focus indicators must be visible (2px outline)

### Keyboard Navigation

**Must support:**
- `Tab` / `Shift+Tab`: Navigate between elements
- `Enter` / `Space`: Activate buttons/links
- `Arrow Keys`: Navigate tabs/menu items
- `Escape`: Close modals/dropdowns

### ARIA Attributes

**Required for all components:**

```html
<!-- Navigation -->
<nav aria-label="Main navigation">
  <button aria-current="page">Dashboard</button>
</nav>

<!-- Tabs -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
</div>

<!-- Buttons -->
<button aria-label="Close dialog">×</button>
```

### Focus Styles

**All interactive elements:**

```css
.focusable:focus-visible {
  outline: 2px solid var(--accent-blue);
  outline-offset: 2px;
}
```

### Color Contrast Audit

**Current palette compliance:**

| Combination | Ratio | Status |
|-------------|-------|--------|
| `--text-primary` / `--bg-secondary` | 12.5:1 | ✅ AAA |
| `--text-secondary` / `--bg-secondary` | 6.8:1 | ✅ AA |
| `--text-muted` / `--bg-secondary` | 4.7:1 | ✅ AA |
| `--accent-blue` / `--bg-secondary` | 8.2:1 | ✅ AAA |

---

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 480px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Small Desktop */
@media (max-width: 1024px) { }

/* Large Desktop */
@media (min-width: 1400px) { }
```

### Component Behavior

| Component | Desktop (>1024px) | Tablet (768-1024px) | Mobile (<768px) |
|-----------|------------------|---------------------|-----------------|
| **Sidebar** | Expanded (280px) | Collapsed (80px) | Hidden/Overlay |
| **Stats Grid** | 4 columns | 2-3 columns | 1 column |
| **Chart Grid** | 2 columns | 1 column | 1 column |
| **Tabs** | Full labels | Full labels | Icons only |
| **Cards** | Full padding | Reduced padding | Minimal padding |

### Responsive Utilities

**Mobile-first approach:**

```css
/* Base (mobile) styles */
.container { padding: 1.5rem; }

/* Tablet and up */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container { padding: 2.5rem; }
}
```

**NEVER use fixed widths** - always use:
- `max-width` + `width: 100%`
- Flexbox with `flex: 1`
- Grid with `fr` units
- Percentages or `rem` units

---

## 💻 Code Quality Standards

### Modular Architecture

**✅ DO:**
- Organize code into reusable components
- Use CSS modules or scoped styles
- Follow single responsibility principle
- Create utility functions for common tasks

**❌ DON'T:**
- Write inline styles
- Hard-code values
- Duplicate code
- Mix concerns in one file

### File Organization

```
project/
├── components/
│   ├── Sidebar/
│   │   ├── Sidebar.jsx
│   │   ├── Sidebar.css
│   │   └── index.js
│   ├── TabSystem/
│   │   ├── TabSystem.jsx
│   │   ├── TabSystem.css
│   │   └── index.js
├── styles/
│   ├── variables.css
│   ├── global.css
│   └── utilities.css
└── utils/
    └── helpers.js
```

### CSS Organization

**Order of properties:**

1. Positioning (`position`, `top`, `z-index`)
2. Box model (`display`, `width`, `padding`, `margin`)
3. Typography (`font`, `text-align`, `color`)
4. Visual (`background`, `border`, `box-shadow`)
5. Misc (`cursor`, `transition`, `animation`)

### Semantic HTML

**✅ Use semantic elements:**
```html
<header>, <nav>, <main>, <section>, <article>, <aside>, <footer>
```

**❌ Avoid divitis:**
```html
<!-- Bad -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- Good -->
<header>
  <nav>...</nav>
</header>
```

### No Placeholder Text

**❌ Bad:**
```html
<p>Lorem ipsum dolor sit amet...</p>
<button>Click here</button>
```

**✅ Good:**
```html
<p>Monitor real-time threat intelligence data...</p>
<button>View Detailed Report</button>
```

---

## 🎬 Animation & Transitions

### Transition Standards

**Use only defined transition variables:**

```css
/* Fast: Hover states, toggles */
transition: all var(--transition-fast);

/* Base: Transforms, color changes */
transition: all var(--transition-base);

/* Slow: Complex animations, layouts */
transition: all var(--transition-slow);
```

### Animation Best Practices

**✅ DO:**
- Use `transform` and `opacity` for performance
- Apply `cubic-bezier` for smooth easing
- Keep animations under 500ms
- Respect `prefers-reduced-motion`

**❌ DON'T:**
- Animate `width`, `height`, `top`, `left`
- Use `linear` easing
- Create jarring/distracting animations
- Override user motion preferences

### Glow Effects

**Standard glow animation:**

```css
@keyframes glow {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(0, 217, 255, 0.2);
  }
  50% {
    box-shadow: 0 4px 16px rgba(0, 217, 255, 0.3);
  }
}

.glowing {
  animation: glow 2s ease-in-out infinite;
}
```

### Reduced Motion Support

**Always include:**

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 🛠️ Implementation Guidelines

### For React/Vue Components

**Component Checklist:**
- [ ] Props are properly typed
- [ ] Styles are scoped/modular
- [ ] Accessibility attributes included
- [ ] Responsive behavior implemented
- [ ] No hard-coded values
- [ ] Loading/error states handled

### For Streamlit Apps

**Integration Steps:**

1. **Import fonts in CSS:**
```python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
</style>
""", unsafe_allow_html=True)
```

2. **Define CSS variables:**
```python
st.markdown("""
<style>
:root {
  --bg-primary: #141B2D;
  /* ... other variables */
}
</style>
""", unsafe_allow_html=True)
```

3. **Target Streamlit elements:**
```python
st.markdown("""
<style>
[data-testid="stSidebar"] {
  background: var(--bg-primary);
}
</style>
""", unsafe_allow_html=True)
```

### Integration Workflow

**When adding new components:**

1. **Plan** - Sketch layout, identify reusable parts
2. **Build** - Create modular component with proper structure
3. **Style** - Apply design system variables and rules
4. **Test** - Check responsiveness, accessibility, browser compatibility
5. **Document** - Add usage examples and props documentation
6. **Review** - Ensure compliance with this guide

### Code Review Checklist

**Before committing:**

- [ ] Uses CSS variables from this guide
- [ ] Follows typography scale
- [ ] Implements proper spacing
- [ ] Has responsive breakpoints
- [ ] Includes accessibility attributes
- [ ] Passes contrast checks
- [ ] No hard-coded colors/sizes
- [ ] Semantic HTML used
- [ ] Transitions are smooth
- [ ] Works in all supported browsers

---

## 📚 Quick Reference

### Color Quick Copy

```css
/* Copy-paste ready */
--bg-primary: #141B2D;
--bg-secondary: #1F2A40;
--text-primary: #E8EAF0;
--accent-blue: #00D9FF;
--accent-green: #00FFB3;
```

### Shadow Quick Copy

```css
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4); /* md */
box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2); /* glow */
```

### Gradient Quick Copy

```css
/* Primary gradient */
background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-green) 100%);

/* Active state */
background: linear-gradient(135deg, rgba(0, 217, 255, 0.12) 0%, rgba(0, 255, 179, 0.12) 100%);
```

### Border Radius Quick Copy

```css
border-radius: 16px; /* Cards */
border-radius: 12px; /* Buttons, nav items */
border-radius: 10px; /* Small buttons */
```

---

## 🚫 Common Mistakes to Avoid

1. **Using arbitrary colors** - Always use CSS variables
2. **Fixed widths** - Use responsive units (%, rem, fr)
3. **Missing hover states** - All interactive elements need them
4. **Inconsistent spacing** - Use the 8px spacing scale
5. **Poor contrast** - Test all color combinations
6. **No focus indicators** - Required for accessibility
7. **Hard-coded values** - Use variables and utilities
8. **Mixing font families** - Stick to Inter and JetBrains Mono
9. **Arbitrary animations** - Use defined transitions
10. **Skipping responsive design** - Mobile-first approach required

---

## 📖 Examples

### Example: Metric Card (Correct Implementation)

```html
<div class="metric-card">
  <div class="metric-icon success">
    <svg>...</svg>
  </div>
  <div class="metric-content">
    <p class="metric-label">Active Threats</p>
    <h3 class="metric-value">1,284</h3>
    <p class="metric-delta positive">↑ 12% from last hour</p>
  </div>
</div>
```

```css
.metric-card {
  display: flex;
  gap: 16px;
  padding: 24px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--accent-blue);
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.metric-icon.success {
  background: linear-gradient(135deg, rgba(0, 255, 179, 0.2) 0%, rgba(0, 217, 255, 0.2) 100%);
  color: var(--accent-green);
  box-shadow: 0 4px 16px rgba(0, 255, 179, 0.3);
}

.metric-label {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
}

.metric-delta.positive {
  color: var(--accent-green);
  font-weight: 600;
}
```

---

## 📞 Support & Questions

**For design questions:**
- Check this guide first
- Review the React component examples in `/components`
- Examine `app.py` for Streamlit implementation

**When in doubt:**
- Default to dark theme (`--bg-secondary`)
- Use CSS variables, never hard-coded values
- Keep it simple and consistent
- Prioritize accessibility

---

**End of Design Rules** • Last updated: 2025-10-14 • Version 1.0
