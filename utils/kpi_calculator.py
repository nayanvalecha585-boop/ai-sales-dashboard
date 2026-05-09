# =====================================================
# utils/kpi_calculator.py
# Computes all KPI values from the filtered dataframe
# =====================================================

import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Returns a dictionary of all dashboard KPIs.
    All calculations are isolated here — easy to extend.
    """
    total_sales   = df["Sales"].sum()
    total_profit  = df["Profit"].sum()
    total_orders  = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique() if "Customer ID" in df.columns else None
    avg_order_value = total_sales / total_orders if total_orders else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    avg_discount  = df["Discount"].mean() * 100 if "Discount" in df.columns else None

    # Sales by breakdowns (used in AI prompt)
    sales_by_category = (
        df.groupby("Category")["Sales"].sum().reset_index()
    )
    profit_by_region = (
        df.groupby("Region")["Profit"].sum().reset_index()
    )
    monthly_sales = (
        df.groupby("Month")["Sales"].sum().reset_index()
    )
    top_subcategories = (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    sales_by_segment = (
        df.groupby("Segment")["Sales"].sum().reset_index()
    )

    return {
        # Scalar KPIs
        "total_sales":       total_sales,
        "total_profit":      total_profit,
        "total_orders":      total_orders,
        "total_customers":   total_customers,
        "avg_order_value":   avg_order_value,
        "profit_margin":     profit_margin,
        "avg_discount":      avg_discount,

        # Grouped data (DataFrames)
        "sales_by_category":  sales_by_category,
        "profit_by_region":   profit_by_region,
        "monthly_sales":      monthly_sales,
        "top_subcategories":  top_subcategories,
        "sales_by_segment":   sales_by_segment,
    }
