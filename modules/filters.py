"""
Reusable filter components for the CyberGuard Dashboard
Follows DESIGN_RULES.md and filter architecture from .claudedesign
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
from modules.theme import COLORS


def init_filter_state():
    """Initialize filter state in session_state if not exists."""
    if 'global_filters' not in st.session_state:
        st.session_state['global_filters'] = {
            'year_range': None,
            'quick_preset': None,
            'attack_type': 'All'
        }

    if 'page_filters' not in st.session_state:
        st.session_state['page_filters'] = {
            'global_threats': {
                'attack_types': [],
                'industries': [],
                'countries': [],
                'loss_range': (0, 10000)
            },
            'intrusion_detection': {
                'protocols': [],
                'attack_detected': 'both',
                'port_range': (0, 65535)
            },
            'ida_eda': {
                'features': [],
                'method': 'All',
                'chart_type': 'Auto'
            },
            'comparative': {
                'mode': 'Year over Year',
                'metrics': []
            }
        }


def global_filter_inline(global_threats: pd.DataFrame) -> Dict[str, Any]:
    """
    Render global filters inline at the top of the page.

    Args:
        global_threats: DataFrame to extract year range from

    Returns:
        Dictionary of active global filters
    """
    init_filter_state()

    if 'Year' in global_threats.columns:
        min_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').min())
        max_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').max())

        if st.session_state['global_filters']['year_range'] is None:
            st.session_state['global_filters']['year_range'] = (min_year, max_year)

        # Year selection dropdowns
        year_options = list(range(min_year, max_year + 1))
        col1, col2 = st.columns(2)

        with col1:
            start_year = st.selectbox(
                "From Year",
                options=year_options,
                index=year_options.index(st.session_state['global_filters']['year_range'][0]),
                key='inline_start_year'
            )

        with col2:
            end_year = st.selectbox(
                "To Year",
                options=year_options,
                index=year_options.index(st.session_state['global_filters']['year_range'][1]),
                key='inline_end_year'
            )

        # Ensure start_year <= end_year
        if start_year > end_year:
            start_year, end_year = end_year, start_year

        st.session_state['global_filters']['year_range'] = (start_year, end_year)

    return st.session_state['global_filters']


def global_filter_sidebar(global_threats: pd.DataFrame) -> Dict[str, Any]:
    """
    Render global filters in sidebar that apply to all pages.
    Clean, unified design with all controls in one container.

    Args:
        global_threats: DataFrame to extract year range from

    Returns:
        Dictionary of active global filters
    """
    init_filter_state()

    st.sidebar.markdown("---")

    # CSS for slider and selectbox colors (Light theme)
    st.sidebar.markdown("""
        <style>
        .stSlider > div > div > div > div {
            background: #3182CE !important;
        }
        .stSlider > div > div > div > div > div {
            background: #3182CE !important;
            box-shadow: 0 0 8px rgba(49, 130, 206, 0.5) !important;
        }
        .stSlider > div > div > div {
            background: rgba(49, 130, 206, 0.15) !important;
        }

        /* Selectbox styling for Time Period */
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: transparent !important;
            border-color: #E2E8F0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'Year' in global_threats.columns:
        min_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').min())
        max_year = int(pd.to_numeric(global_threats['Year'], errors='coerce').max())

        if st.session_state['global_filters']['year_range'] is None:
            st.session_state['global_filters']['year_range'] = (min_year, max_year)

        # Time Period Container - header with top border (Light theme)
        with st.sidebar.container():
            st.markdown("""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-bottom: none; border-radius: 12px 12px 0 0; padding: 16px 18px 14px 18px; margin-bottom: 0px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 18px;">📅</span>
<span style="font-size: 0.95rem; font-weight: 700; color: #1A1A1A;">Time Period</span>
</div>
</div>""", unsafe_allow_html=True)

            # Dropdowns wrapper with side borders and background
            st.markdown("""<div style="background: #FFFFFF; border-left: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; padding: 0px 18px 8px 18px; margin-top: 0px; margin-bottom: 0px;">
</div>""", unsafe_allow_html=True)

            # Year selection dropdowns
            year_options = list(range(min_year, max_year + 1))
            col1, col2 = st.columns(2)

            with col1:
                start_year = st.selectbox(
                    "From",
                    options=year_options,
                    index=year_options.index(st.session_state['global_filters']['year_range'][0]),
                    key='start_year_select'
                )

            with col2:
                end_year = st.selectbox(
                    "To",
                    options=year_options,
                    index=year_options.index(st.session_state['global_filters']['year_range'][1]),
                    key='end_year_select'
                )

            # Bottom border closure (Light theme)
            st.markdown("""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: none; border-radius: 0 0 12px 12px; padding: 10px; margin-top: 0px; margin-bottom: 20px;">
</div>""", unsafe_allow_html=True)

        # Ensure start_year <= end_year
        if start_year > end_year:
            start_year, end_year = end_year, start_year

        st.session_state['global_filters']['year_range'] = (start_year, end_year)

        # Clear All button - separate from Time Period container
        if st.sidebar.button("🔄 Clear All Filters", key='clear_all', use_container_width=True, type="secondary"):
            st.session_state['global_filters']['year_range'] = (min_year, max_year)
            st.session_state['global_filters']['quick_preset'] = None
            for page in st.session_state['page_filters']:
                if page == 'global_threats':
                    st.session_state['page_filters'][page] = {
                        'attack_types': [],
                        'industries': [],
                        'countries': [],
                        'loss_range': (0, 10000)
                    }
            st.rerun()

    return st.session_state['global_filters']


def filter_summary_chips(active_filters: Dict[str, Any], page_filters: Optional[Dict[str, Any]] = None):
    """
    Display active filters as removable chips with modern design.

    Args:
        active_filters: Global filters dict
        page_filters: Optional page-specific filters dict
    """
    chips = []

    # Global filters
    if active_filters.get('year_range'):
        year_range = active_filters['year_range']
        chips.append({
            'label': f"{year_range[0]}–{year_range[1]}",
            'icon': '📅',
            'type': 'global',
            'key': 'year_range',
            'color': 'blue'
        })

    # Page-specific filters
    if page_filters:
        for key, value in page_filters.items():
            if isinstance(value, list) and len(value) > 0:
                icon_map = {
                    'attack_types': '⚠️',
                    'industries': '🏭',
                    'countries': '🌍',
                    'protocols': '🔌'
                }
                for item in value:
                    chips.append({
                        'label': item,
                        'icon': icon_map.get(key, '🔖'),
                        'type': 'page',
                        'key': key,
                        'value': item,
                        'color': 'green'
                    })
            elif isinstance(value, tuple) and key.endswith('_range'):
                chips.append({
                    'label': f"{value[0]:,}–{value[1]:,}",
                    'icon': '💰' if 'loss' in key else '🔢',
                    'type': 'page',
                    'key': key,
                    'color': 'purple'
                })
            elif value and not isinstance(value, (list, tuple)) and value != 'both' and value != 'All' and value != 'Auto':
                chips.append({
                    'label': str(value),
                    'icon': '🎯',
                    'type': 'page',
                    'key': key,
                    'color': 'orange'
                })

    # Color schemes for different chip types - Light theme
    color_schemes = {
        'blue': {
            'bg': 'rgba(49, 130, 206, 0.1)',
            'border': '#3182CE',
            'text': '#3182CE'
        },
        'green': {
            'bg': 'rgba(56, 161, 105, 0.1)',
            'border': '#38A169',
            'text': '#38A169'
        },
        'purple': {
            'bg': 'rgba(128, 90, 213, 0.1)',
            'border': '#805AD5',
            'text': '#805AD5'
        },
        'orange': {
            'bg': 'rgba(221, 107, 32, 0.1)',
            'border': '#DD6B20',
            'text': '#DD6B20'
        }
    }

    # Build all chips HTML as a single string
    chips_html = ""
    if chips:
        for chip in chips:
            color_scheme = color_schemes.get(chip.get('color', 'blue'), color_schemes['blue'])
            chips_html += f'<div style="display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: {color_scheme["bg"]}; border: 1.5px solid {color_scheme["border"]}; border-radius: 24px; font-size: 0.85rem; font-weight: 600; color: {color_scheme["text"]}; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); transition: all 0.2s ease; cursor: default;"><span style="font-size: 14px; line-height: 1;">{chip["icon"]}</span><span style="letter-spacing: 0.02em;">{chip["label"]}</span></div>'
    else:
        chips_html = '<div style="flex: 1; display: flex; align-items: center; justify-content: center; color: #718096; font-size: 0.85rem;">No filters applied</div>'

    # Render complete HTML in one call with consistent height - Light theme
    html_content = f'''<div style="position: relative; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); min-height: 200px; display: flex; flex-direction: column;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
<span style="font-size: 18px;">✨</span>
<span style="font-size: 0.95rem; font-weight: 700; color: #1A1A1A;">Active Filters</span>
<div style="background: #3182CE; color: #FFFFFF; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); margin-left: auto;">{len(chips)}</div>
</div>
<div style="flex: 1; display: flex; flex-wrap: wrap; gap: 10px; align-items: flex-start; align-content: flex-start;">
{chips_html}
</div>
</div>'''

    st.markdown(html_content, unsafe_allow_html=True)


def apply_global_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply global filters to a dataframe.

    Args:
        df: DataFrame to filter
        filters: Global filters dictionary

    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()

    # Apply year range filter
    if filters.get('year_range') and 'Year' in filtered_df.columns:
        year_range = filters['year_range']
        filtered_df = filtered_df[
            (filtered_df['Year'] >= year_range[0]) &
            (filtered_df['Year'] <= year_range[1])
        ]

    # Apply attack type filter
    if filters.get('attack_type') and filters['attack_type'] != 'All' and 'Attack Type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Attack Type'] == filters['attack_type']]

    return filtered_df


def page_filter_panel_global_threats(global_threats: pd.DataFrame, page_name: str = 'global_threats') -> Dict[str, Any]:
    """
    Render page-specific filters for Global Threat Landscape page with modern design.

    Args:
        global_threats: DataFrame for extracting unique values
        page_name: Key for session state

    Returns:
        Dictionary of active page filters
    """
    init_filter_state()

    st.markdown('<div style="padding: 12px 16px; background: rgba(49, 130, 206, 0.05); border: 1px solid #E2E8F0; border-radius: 12px; margin-bottom: 16px;"><p style="margin: 0; font-size: 0.85rem; color: #4A5568; text-align: center;"><span style="color: #3182CE; font-weight: 600;">Customize</span> this page\'s visualization by applying specific filters below</p></div>', unsafe_allow_html=True)

    # Attack Type filter
    attack_types_options = ["All"] + sorted(global_threats['Attack Type'].dropna().unique()) if 'Attack Type' in global_threats.columns else ["All"]
    selected_attacks = st.multiselect(
        "⚠️ Attack Type",
        options=attack_types_options,
        default="All",
        key=f'{page_name}_attack_types'
    )
    if "All" in selected_attacks and len(selected_attacks) > 1:
        selected_attacks.remove("All")
    if not selected_attacks:
        selected_attacks = ["All"]
    st.session_state['page_filters'][page_name]['attack_types'] = selected_attacks

    # Target Industry filter
    industries_options = ["All"] + sorted(global_threats['Target Industry'].dropna().unique()) if 'Target Industry' in global_threats.columns else ["All"]
    selected_industries = st.multiselect(
        "🏭 Target Industry",
        options=industries_options,
        default="All",
        key=f'{page_name}_industries'
    )
    if "All" in selected_industries and len(selected_industries) > 1:
        selected_industries.remove("All")
    if not selected_industries:
        selected_industries = ["All"]
    st.session_state['page_filters'][page_name]['industries'] = selected_industries

    # Country filter
    countries_options = ["All"] + sorted(global_threats['Country'].dropna().unique()) if 'Country' in global_threats.columns else ["All"]
    selected_countries = st.multiselect(
        "🌍 Country",
        options=countries_options,
        default="All",
        key=f'{page_name}_countries'
    )
    if "All" in selected_countries and len(selected_countries) > 1:
        selected_countries.remove("All")
    if not selected_countries:
        selected_countries = ["All"]
    st.session_state['page_filters'][page_name]['countries'] = selected_countries

    # Financial Loss Range
    if 'Financial Loss (in Million $)' in global_threats.columns:
        max_loss = int(global_threats['Financial Loss (in Million $)'].max())
        loss_range = st.slider(
            "💰 Financial Loss Range (Million $)",
            min_value=0,
            max_value=max_loss,
            value=st.session_state['page_filters'][page_name]['loss_range'],
            key=f'{page_name}_loss_range'
        )
        st.session_state['page_filters'][page_name]['loss_range'] = loss_range

    return st.session_state['page_filters'][page_name]


def apply_page_filters_global_threats(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply page-specific filters for Global Threats page.

    Args:
        df: DataFrame to filter
        filters: Page filters dictionary

    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()

    # Attack Type filter
    if "All" not in filters['attack_types'] and filters['attack_types'] and 'Attack Type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Attack Type'].isin(filters['attack_types'])]

    # Industry filter
    if "All" not in filters['industries'] and filters['industries'] and 'Target Industry' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Target Industry'].isin(filters['industries'])]

    # Country filter
    if "All" not in filters['countries'] and filters['countries'] and 'Country' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Country'].isin(filters['countries'])]

    # Financial Loss range filter
    if filters['loss_range'] and 'Financial Loss (in Million $)' in filtered_df.columns:
        loss_range = filters['loss_range']
        filtered_df = filtered_df[
            (filtered_df['Financial Loss (in Million $)'] >= loss_range[0]) &
            (filtered_df['Financial Loss (in Million $)'] <= loss_range[1])
        ]

    return filtered_df


def page_filter_panel_intrusion(intrusion_data: pd.DataFrame, page_name: str = 'intrusion_detection') -> Dict[str, Any]:
    """
    Render page-specific filters for Intrusion Detection page.

    Args:
        intrusion_data: DataFrame for extracting unique values
        page_name: Key for session state

    Returns:
        Dictionary of active page filters
    """
    init_filter_state()

    # Protocol Type filter
    protocols_options = ["All"] + sorted(intrusion_data['protocol_type'].dropna().unique()) if 'protocol_type' in intrusion_data.columns else ["All"]
    selected_protocols = st.multiselect(
        "🔌 Protocol Type",
        options=protocols_options,
        default="All",
        key=f'{page_name}_protocols'
    )
    if "All" in selected_protocols and len(selected_protocols) > 1:
        selected_protocols.remove("All")
    if not selected_protocols:
        selected_protocols = ["All"]
    st.session_state['page_filters'][page_name]['protocols'] = selected_protocols

    # Attack Detected toggle
    attack_filter = st.selectbox(
        "🚨 Attack Detected",
        options=['both', 'yes', 'no'],
        index=['both', 'yes', 'no'].index(st.session_state['page_filters'][page_name]['attack_detected']),
        key=f'{page_name}_attack_detected'
    )
    st.session_state['page_filters'][page_name]['attack_detected'] = attack_filter
    return st.session_state['page_filters'][page_name]


def apply_page_filters_intrusion(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply page-specific filters for Intrusion Detection page.

    Args:
        df: DataFrame to filter
        filters: Page filters dictionary

    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()

    # Protocol filter
    if "All" not in filters['protocols'] and filters['protocols'] and 'protocol_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['protocol_type'].isin(filters['protocols'])]

    # Attack detected filter
    if filters['attack_detected'] != 'both' and 'attack_detected' in filtered_df.columns:
        if filters['attack_detected'] == 'yes':
            filtered_df = filtered_df[filtered_df['attack_detected'] == 1]
        else:
            filtered_df = filtered_df[filtered_df['attack_detected'] == 0]

    return filtered_df


def show_filter_stats(original_count: int, filtered_count: int):
    """
    Display data count before/after filtering with modern design.

    Args:
        original_count: Original number of rows
        filtered_count: Filtered number of rows
    """
    reduction = original_count - filtered_count
    percentage = (reduction / original_count * 100) if original_count > 0 else 0

    # Determine color based on filter intensity (Light theme)
    if percentage < 25:
        bar_color = '#38A169'
        glow_color = 'rgba(56, 161, 105, 0.3)'
    elif percentage < 50:
        bar_color = '#3182CE'
        glow_color = 'rgba(49, 130, 206, 0.3)'
    elif percentage < 75:
        bar_color = '#DD6B20'
        glow_color = 'rgba(221, 107, 32, 0.3)'
    else:
        bar_color = '#805AD5'
        glow_color = 'rgba(128, 90, 213, 0.3)'

    stats_html = f'''<div style="position: relative; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); overflow: hidden;">
<div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, #3182CE 0%, #38A169 100%); box-shadow: 0 0 8px {glow_color};"></div>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
<div style="display: flex; align-items: baseline; gap: 8px;">
<span style="font-size: 2rem; font-weight: 800; color: #1A1A1A; font-family: 'JetBrains Mono', monospace; letter-spacing: -0.02em;">{filtered_count:,}</span>
<span style="font-size: 0.9rem; color: #4A5568;">/ {original_count:,}</span>
</div>
<span style="font-size: 0.8rem; color: #718096; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Showing</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(0, 0, 0, 0.05); border-radius: 3px; overflow: hidden;">
<div style="width: {100 - percentage}%; height: 100%; background: linear-gradient(90deg, #3182CE 0%, #38A169 100%); border-radius: 3px; box-shadow: 0 0 6px {glow_color}; transition: width 0.3s ease;"></div>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
<div style="font-size: 0.75rem; color: #718096;">{reduction:,} records filtered out</div>
<div style="padding: 4px 12px; background: {bar_color}; border-radius: 12px; font-size: 0.8rem; color: #FFFFFF; font-weight: 700; font-family: 'JetBrains Mono', monospace; box-shadow: 0 2px 4px {glow_color};">{percentage:.1f}%</div>
</div>
</div>'''

    st.sidebar.markdown(stats_html, unsafe_allow_html=True)
