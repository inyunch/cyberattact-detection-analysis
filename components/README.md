# Modern Dashboard Components

A collection of modern, accessible React components for building cybersecurity dashboards with a dark theme and neon accents.

## Components

### 🎨 Design Features

- **Dark Theme**: Primary background `#141B2D` with gradient accents
- **Neon Accents**: Blue (`#00D9FF`) and Green (`#00FFB3`) gradients for highlights
- **Typography**: Inter for UI text, JetBrains Mono for data/numbers
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation support
- **Responsive**: Optimized for desktop, tablet, and mobile devices

---

## 📁 Sidebar Component

A collapsible navigation sidebar with icon/text menu items and active state indicators.

### Features
- Collapsible with smooth animations
- Active menu indicator with glowing effect
- Rounded corners and modern styling
- User profile section in footer
- Keyboard navigation support

### Usage

```jsx
import Sidebar from './Sidebar';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
  { id: 'analytics', label: 'Analytics', icon: '📊' },
  { id: 'threats', label: 'Threats', icon: '⚠️' },
];

function App() {
  const [activeItem, setActiveItem] = useState('dashboard');
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Sidebar
      menuItems={menuItems}
      activeItem={activeItem}
      onMenuClick={setActiveItem}
      isCollapsed={collapsed}
      onToggle={() => setCollapsed(!collapsed)}
    />
  );
}
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `menuItems` | `Array<{id, label, icon}>` | Menu items to display |
| `activeItem` | `string` | ID of the currently active menu item |
| `onMenuClick` | `(id: string) => void` | Callback when menu item is clicked |
| `isCollapsed` | `boolean` | Whether sidebar is collapsed |
| `onToggle` | `() => void` | Callback when toggle button is clicked |

---

## 🎯 TabSystem Component

A modern tab system with animated indicators and multiple style variants.

### Features
- Three variants: `underline`, `pill`, and default
- Glowing active state with animations
- Badge support for notifications
- Icon support
- Smooth indicator transitions
- Keyboard navigation (arrow keys)

### Usage

```jsx
import TabSystem from './TabSystem';

const tabs = [
  { id: 'overview', label: 'Overview', icon: '📈' },
  { id: 'threats', label: 'Threats', icon: '⚠️', badge: 5 },
  { id: 'network', label: 'Network', icon: '🔗' },
];

function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <TabSystem
      tabs={tabs}
      activeTab={activeTab}
      onTabChange={setActiveTab}
      variant="underline" // or "pill"
    />
  );
}
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `tabs` | `Array<{id, label, icon?, badge?, disabled?}>` | Tab items to display |
| `activeTab` | `string` | ID of the currently active tab |
| `onTabChange` | `(id: string) => void` | Callback when tab is clicked |
| `variant` | `'underline' \| 'pill'` | Visual style variant (default: underline) |

---

## 🎛️ Dashboard Component

A complete dashboard layout showcasing the sidebar and tab system together with demo content.

### Features
- Responsive layout
- Stats cards with icons and trends
- Chart placeholders for data visualization
- Table card for data display
- Header with actions and notifications

### Usage

```jsx
import Dashboard from './Dashboard';

function App() {
  return <Dashboard />;
}
```

---

## 🎨 Customization

### CSS Variables

All components use CSS custom properties for easy theming:

```css
:root {
  --bg-primary: #141B2D;
  --bg-secondary: #1F2A40;
  --bg-hover: #2A3650;
  --text-primary: #E8EAF0;
  --text-secondary: #A0A7B8;
  --text-muted: #6C7489;
  --accent-blue: #00D9FF;
  --accent-green: #00FFB3;
  --accent-purple: #7B61FF;
  --accent-orange: #FF9F43;
  --accent-red: #FF5370;
  --border-color: #2E3A52;
}
```

### Changing Colors

Override the CSS variables in your own stylesheet:

```css
:root {
  --accent-blue: #YOUR_COLOR;
  --accent-green: #YOUR_COLOR;
  /* ... other variables */
}
```

---

## ♿ Accessibility Features

- **Keyboard Navigation**: Full support for Tab, Enter, Arrow keys
- **ARIA Attributes**: Proper roles, states, and labels
- **Focus Indicators**: Visible focus outlines for keyboard users
- **Color Contrast**: WCAG AA compliant contrast ratios
- **Reduced Motion**: Respects `prefers-reduced-motion` setting
- **Screen Reader**: Semantic HTML and descriptive labels

### Keyboard Shortcuts

- **Tab/Shift+Tab**: Navigate between interactive elements
- **Enter/Space**: Activate buttons and links
- **Escape**: Close modals/dropdowns (if implemented)

---

## 📱 Responsive Breakpoints

- **Desktop**: > 1024px - Full sidebar with text labels
- **Tablet**: 768px - 1024px - Collapsed sidebar by default
- **Mobile**: < 768px - Hidden sidebar with toggle overlay

---

## 🚀 Integration with Existing Dashboard

Since your current dashboard uses **Streamlit (Python)**, here are integration options:

### Option 1: Replace with React

1. Set up a React app with Create React App or Vite
2. Install dependencies: `npm install react react-dom`
3. Import and use the components as shown above
4. Integrate your Plotly charts into the placeholder areas

### Option 2: Embed React in Streamlit

Use `streamlit-component-template` to create a custom Streamlit component:

```python
import streamlit as st
from streamlit.components.v1 import html

# Read your compiled React bundle
with open('build/static/js/main.js') as f:
    react_js = f.read()

html(f"""
    <div id="root"></div>
    <script>{react_js}</script>
""", height=800)
```

### Option 3: Keep Streamlit, Style to Match

Adapt the CSS styling to your Streamlit app:

```python
st.markdown("""
<style>
    /* Copy relevant CSS from Sidebar.css and TabSystem.css */
    /* Adapt selectors to match Streamlit's generated classes */
</style>
""", unsafe_allow_html=True)
```

---

## 📦 File Structure

```
components/
├── Sidebar.jsx          # Sidebar component
├── Sidebar.css          # Sidebar styles
├── TabSystem.jsx        # Tab system component
├── TabSystem.css        # Tab system styles
├── Dashboard.jsx        # Demo dashboard layout
├── Dashboard.css        # Dashboard layout styles
└── README.md           # This file
```

---

## 🔧 Dependencies

- React 16.8+ (for hooks)
- No external UI library dependencies
- Pure CSS (no CSS-in-JS required)

---

## 🎯 Next Steps

1. **Install React** if you haven't already
2. **Copy the component files** to your project
3. **Import and customize** the components
4. **Replace placeholders** with your actual data visualizations
5. **Test accessibility** with keyboard navigation and screen readers

---

## 💡 Tips

- Use the Dashboard component as a starting template
- Customize colors via CSS variables for brand consistency
- Add your Plotly charts in the `.chart-placeholder` divs
- Connect to your data APIs in the Dashboard component
- Extend with additional components as needed (modals, dropdowns, etc.)

---

## 🐛 Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari 12+, Chrome Android

---

## 📄 License

Free to use and modify for your cybersecurity dashboard project.

---

**Created with Claude Code** 🛡️
