# =====================================================
# components/ai_insights.py
# Renders the Gemini AI insights section
# =====================================================

import streamlit as st
from utils.gemini_client import generate_insight


def build_prompt(kpis: dict, chart_data: dict) -> str:
    """
    Builds a structured, token-efficient prompt from
    the computed KPIs and chart DataFrames.
    """
    monthly_tail = (
        kpis["monthly_sales"]
        .tail(12)
        .to_string(index=False)
    )

    prompt = f"""
You are a senior business analyst reviewing a retail sales dashboard.

Analyze the metrics below and provide a structured report covering:

1. **Executive Summary** — 2-3 sentence overview of the business health
2. **Key Trends** — what is growing, what is shrinking
3. **Risks & Concerns** — loss-making segments or regions, high discounts, etc.
4. **Top Opportunities** — where to invest or double down
5. **Actionable Recommendations** — 3 to 5 specific, prioritised actions

---
BUSINESS METRICS:

Total Sales:       ${kpis['total_sales']:,.2f}
Total Profit:      ${kpis['total_profit']:,.2f}
Total Orders:      {kpis['total_orders']:,}
Profit Margin:     {kpis['profit_margin']:.2f}%
Avg Order Value:   ${kpis['avg_order_value']:,.2f}
Avg Discount:      {f"{kpis['avg_discount']:.1f}%" if kpis['avg_discount'] is not None else "N/A"}

Sales by Category:
{kpis['sales_by_category'].to_string(index=False)}

Profit by Region:
{kpis['profit_by_region'].to_string(index=False)}

Last 12 Months of Sales:
{monthly_tail}

Top 10 Sub-Categories by Sales:
{kpis['top_subcategories'].to_string(index=False)}

Sales by Segment:
{kpis['sales_by_segment'].to_string(index=False)}
---
Be specific. Reference actual numbers where relevant. Format your output in clear markdown.
"""
    return prompt.strip()


def render_ai_insights(kpis: dict, chart_data: dict):
    """Renders the full AI insights section."""

    st.subheader("🤖 AI Business Insights")
    st.markdown(
        "Click the button below to let **Gemini AI** analyse "
        "the current filtered data and generate a business report."
    )

    # Session state so the insight persists after re-renders
    if "ai_insight" not in st.session_state:
        st.session_state.ai_insight = None
    if "ai_error" not in st.session_state:
        st.session_state.ai_error = None

    col1, col2 = st.columns([1, 5])

    with col1:
        generate_clicked = st.button("✨ Generate Insight", use_container_width=True)

    with col2:
        if st.session_state.ai_insight:
            if st.button("🗑️ Clear", use_container_width=False):
                st.session_state.ai_insight = None
                st.session_state.ai_error = None
                st.rerun()

    if generate_clicked:
        st.session_state.ai_insight = None
        st.session_state.ai_error = None

        with st.spinner("Gemini is analysing your data..."):
            try:
                prompt = build_prompt(kpis, chart_data)
                insight = generate_insight(prompt)
                st.session_state.ai_insight = insight

            except EnvironmentError as e:
                st.session_state.ai_error = str(e)

            except Exception as e:
                st.session_state.ai_error = (
                    f"Gemini API error: {e}\n\n"
                    "Check your API key and internet connection."
                )

    # Display result or error
    if st.session_state.ai_error:
        st.error(st.session_state.ai_error)

    if st.session_state.ai_insight:
        st.success("✅ Insight generated successfully!")
        st.markdown("---")
        st.markdown(st.session_state.ai_insight)
        st.markdown("---")

        # Download button for the report
        st.download_button(
            label="📥 Download Report as .txt",
            data=st.session_state.ai_insight,
            file_name="sales_insight_report.txt",
            mime="text/plain"
        )
