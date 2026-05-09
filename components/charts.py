# =====================================================
# components/charts.py
# All Plotly chart rendering lives here
# =====================================================

import streamlit as st
import plotly.express as px
import pandas as pd


# Consistent colour palette
PALETTE = px.colors.qualitative.Set2


def render_all_charts(df: pd.DataFrame) -> dict:
    """
    Renders all dashboard charts.
    Returns the computed DataFrames so the AI insight
    component can reuse them without recalculating.
    """

    chart_data = {}

    # ---- Row 1: Category bar | Region pie ----
    col1, col2 = st.columns(2)

    with col1:
        sales_by_category = (
            df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )
        fig = px.bar(
            sales_by_category,
            x="Category",
            y="Sales",
            title="💼 Sales by Category",
            color="Category",
            color_discrete_sequence=PALETTE,
            text_auto=".2s"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        chart_data["sales_by_category"] = sales_by_category

    with col2:
        profit_by_region = (
            df.groupby("Region")["Profit"]
            .sum()
            .reset_index()
        )
        fig = px.pie(
            profit_by_region,
            names="Region",
            values="Profit",
            title="🌍 Profit by Region",
            color_discrete_sequence=PALETTE,
            hole=0.35
        )
        st.plotly_chart(fig, use_container_width=True)
        chart_data["profit_by_region"] = profit_by_region


    # ---- Row 2: Monthly trend (full width) ----
    monthly_sales = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )
    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        title="📅 Monthly Sales Trend",
        markers=True,
        color_discrete_sequence=["#4f46e5"]
    )
    fig.update_traces(line_width=2.5)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    chart_data["monthly_sales"] = monthly_sales


    # ---- Row 3: Segment bar | Sub-category bar ----
    col3, col4 = st.columns(2)

    with col3:
        sales_by_segment = (
            df.groupby("Segment")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )
        fig = px.bar(
            sales_by_segment,
            x="Segment",
            y="Sales",
            title="🧑‍💼 Sales by Segment",
            color="Segment",
            color_discrete_sequence=PALETTE,
            text_auto=".2s"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        chart_data["sales_by_segment"] = sales_by_segment

    with col4:
        top_subcategories = (
            df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
            top_subcategories,
            x="Sales",
            y="Sub-Category",
            title="🏆 Top 10 Sub-Categories by Sales",
            orientation="h",
            color="Sales",
            color_continuous_scale="Blues",
            text_auto=".2s"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
        chart_data["top_subcategories"] = top_subcategories


    # ---- Row 4: Profit vs Sales scatter ----
    if "Sub-Category" in df.columns:
        scatter_df = (
            df.groupby("Sub-Category")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
            .reset_index()
        )
        fig = px.scatter(
            scatter_df,
            x="Sales",
            y="Profit",
            size="Orders",
            color="Sub-Category",
            title="📌 Profit vs Sales by Sub-Category",
            hover_name="Sub-Category",
            size_max=40
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
        chart_data["scatter_df"] = scatter_df

    return chart_data
