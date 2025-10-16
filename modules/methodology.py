import streamlit as st


def _card(content: str):
    """Render a simple themed card using the global CSS variables from theme.py."""
    st.markdown(
        f"""
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px; margin: 8px 0;">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _pill(label: str):
    st.markdown(
        f"""
        <span style="display:inline-block; padding:6px 10px; border-radius:999px; border:1px solid var(--border-color); background: var(--bg-tertiary); color: var(--text-secondary); font-size:12px; margin-right:6px; margin-bottom:6px;">{label}</span>
        """,
        unsafe_allow_html=True,
    )


def show():
    """Simple, user-friendly methodology and data dictionary."""

    st.title("📖 Data Dictionary & Methodology")
    st.markdown("Easy-to-understand reference for the datasets used and how the insights are produced.")
    st.markdown("---")

    # Overview / How to use
    _card(
        """
        <b>How to use this dashboard</b>
        <ul style="margin: 6px 0 0 18px;">
          <li>Select a page from the sidebar.</li>
          <li>Apply filters to focus on specific years, countries, sectors, or attributes.</li>
          <li>Hover, zoom, and click legends on charts to explore details.</li>
        </ul>
        """
    )

    # Data sources section removed per request to keep the page concise.

    st.markdown("---")

    st.subheader("🧹 Data Preparation (Brief)")

    _card(
        """
        <ul style="margin: 0 0 0 18px;">
          <li><b>Quality checks:</b> inspected data types, missingness, duplicates.</li>
          <li><b>Standardization:</b> consistent naming for countries, attack types, and dates.</li>
          <li><b>Missing values:</b> simple imputation for small gaps; flagged large gaps.</li>
          <li><b>Outliers:</b> kept and highlighted where helpful for insight.</li>
        </ul>
        """
    )

    st.markdown("---")

    st.subheader("📊 Methods (At a glance)")

    _card(
        """
        <b>What we look at</b>
        <ul style="margin: 6px 0 0 18px;">
          <li><b>Univariate</b> — single-variable distributions and counts.</li>
          <li><b>Bivariate</b> — relationships like Year × Attack Type, Sector × Loss.</li>
          <li><b>Multivariate</b> — combined patterns and feature interactions.</li>
          <li><b>Time Trends</b> — year-over-year changes and sustained movement.</li>
          <li><b>Geographic</b> — country/regional comparisons and hotspots.</li>
        </ul>
        """
    )

    _card(
        """
        <b>How it’s visualized</b>
        <ul style="margin: 6px 0 0 18px;">
          <li><b>Bars & Lines</b> — comparisons and trends over time.</li>
          <li><b>Scatter</b> — relationships among numeric variables.</li>
          <li><b>Heatmaps</b> — frequency and correlation matrices.</li>
          <li><b>Maps</b> — geographic distribution (choropleth/bubbles).</li>
          <li><b>Tables</b> — sortable, filterable breakdowns.</li>
        </ul>
        """
    )

    _card(
        """
        <b>How to read the outputs</b>
        <ul style="margin: 6px 0 0 18px;">
          <li>Use filters to focus your view; hover for tooltips and details.</li>
          <li>Compare across sectors or countries before drawing conclusions.</li>
          <li>Look for <b>consistent</b> movement across multiple periods, not only spikes.</li>
        </ul>
        """
    )

    st.markdown("---")

    st.subheader("⚠️ Notes & Limitations")

    _card(
        """
        <ul style="margin: 0 0 0 18px;">
          <li><b>Reported data:</b> may not capture all incidents; focus on patterns.</li>
          <li><b>Different levels:</b> global macro trends vs. session micro features are complementary.</li>
          <li><b>Context matters:</b> compare within region/sector before drawing conclusions.</li>
        </ul>
        """
    )

    st.markdown("---")

    st.subheader("✅ Concluding Observations")

    _card(
        """
        <ul style="margin: 0 0 0 18px;">
          <li><b>Trends</b> show meaningful year-over-year variation—look for sustained changes.</li>
          <li><b>Sectors & geographies</b> have distinct risk profiles—interpret within context.</li>
          <li><b>Intrusion indicators</b> help surface suspicious sessions—use to guide investigation.</li>
          <li><b>Designed for usability:</b> select a page, filter, and explore interactively.</li>
        </ul>
        """
    )

    st.caption("This page is intentionally concise and aligned with the dashboard's design for clarity and ease of use.")
