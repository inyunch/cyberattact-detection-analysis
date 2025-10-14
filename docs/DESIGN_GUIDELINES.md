# Design Guidelines

This document summarizes the visual system used in the Streamlit dashboard: color palette, components, and patterns.

Principles
- Clarity: communicate hierarchy with typography, spacing, and color usage.
- Consistency: shared card surfaces (rovocard), consistent section headers.
- Accessibility: WCAG-AA contrast targets (4.5:1 for normal text).

Palette (Light)
- primary: #2563EB
- secondary: #0EA5E9
- background: #F8FAFC
- surface: #FFFFFF
- text: #0F172A
- muted_text: #475569
- grid: #E2E8F0
- accent: #F59E0B
- danger: #DC2626
- success: #16A34A
- blue_palette: [#2563EB, #0EA5E9, #8B5CF6, #F59E0B, #60A5FA]

Components
- Hero header (page_hero): Title + optional emoji, optional subtitle inside a rovocard.
- Section header (section_header): Smaller h2 headline to guide narrative.
- KPI Cards (kpi_card): Keep metric/delta semantics; use apply_base_css for base style.
- Charts: Use apply_theme for consistent colors and spacing. Avoid excessive gridlines.

Drill-down pattern
- Click events refine global filters (attack type, industry, country, year) and rerun the app.

Contrast audit
- Use contrast_audit_report() to inspect color pairs and ratios. Aim for >= 4.5:1.

Notes
- Appearance and Saved Views UI are disabled by default per product request.
- Keep content and logic the same; these guidelines only affect presentation.
