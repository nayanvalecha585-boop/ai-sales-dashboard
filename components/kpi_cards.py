# =====================================================
# components/kpi_cards.py
# Renders the KPI metric row at the top of the dashboard
# =====================================================

import streamlit as st


def render_kpi_cards(kpis: dict):
    """Render 4 primary KPI cards + 2 secondary ones."""

    # --- Primary KPIs (row 1) ---
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="💰 Total Sales",
        value=f"${kpis['total_sales']:,.2f}"
    )
    col2.metric(
        label="📈 Total Profit",
        value=f"${kpis['total_profit']:,.2f}",
        delta=f"{kpis['profit_margin']:.1f}% margin"
    )
    col3.metric(
        label="🛒 Total Orders",
        value=f"{kpis['total_orders']:,}"
    )
    col4.metric(
        label="🧾 Avg Order Value",
        value=f"${kpis['avg_order_value']:,.2f}"
    )

    # --- Secondary KPIs (row 2) ---
    col5, col6, col7 = st.columns(3)

    col5.metric(
        label="📊 Profit Margin",
        value=f"{kpis['profit_margin']:.2f}%"
    )

    if kpis["total_customers"] is not None:
        col6.metric(
            label="👥 Unique Customers",
            value=f"{kpis['total_customers']:,}"
        )

    if kpis["avg_discount"] is not None:
        col7.metric(
            label="🏷️ Avg Discount",
            value=f"{kpis['avg_discount']:.1f}%"
        )
