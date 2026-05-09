# =====================================================
# AI SALES INSIGHTS DASHBOARD
# Entry point — run with: streamlit run app.py
# =====================================================

import streamlit as st
from utils.data_loader import load_data
from utils.kpi_calculator import calculate_kpis
from components.kpi_cards import render_kpi_cards
from components.charts import render_all_charts
from components.ai_insights import render_ai_insights


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Sales Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .metric-card { background-color: #f0f2f6; border-radius: 10px; padding: 1rem; }
        h1 { color: #1f2d3d; }
        .stButton > button {
            background-color: #4f46e5;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-size: 1rem;
            border: none;
        }
        .stButton > button:hover { background-color: #4338ca; }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/combo-chart--v1.png", width=80)
    st.title("Dashboard Controls")
    st.markdown("---")

    # File uploader (optional override)
    uploaded_file = st.file_uploader(
        "Upload your own CSV",
        type=["csv"],
        help="Upload a Superstore-style CSV to override the default dataset."
    )

    st.markdown("---")
    st.caption("Built with Streamlit + Gemini AI")


# =====================================================
# HEADER
# =====================================================

st.title("📊 AI Sales Insights Dashboard")
st.markdown("Analyze sales performance with **AI-powered** business insights.")
st.markdown("---")


# =====================================================
# LOAD DATA
# =====================================================

df = load_data(uploaded_file)

if df is None:
    st.error("❌ Could not load data. Please check that `data/superstore.csv` exists.")
    st.stop()


# =====================================================
# DATA PREVIEW (collapsible)
# =====================================================

with st.expander("📁 Preview Raw Dataset", expanded=False):
    st.dataframe(df.head(20), use_container_width=True)
    st.caption(f"Dataset has **{len(df):,} rows** and **{len(df.columns)} columns**.")


# =====================================================
# SIDEBAR FILTERS
# =====================================================

with st.sidebar:
    st.subheader("🔍 Filters")

    # Region filter
    all_regions = sorted(df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions
    )

    # Category filter
    all_categories = sorted(df["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories
    )

    # Segment filter
    all_segments = sorted(df["Segment"].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Segment",
        options=all_segments,
        default=all_segments
    )

# Apply filters
filtered_df = df[
    df["Region"].isin(selected_regions) &
    df["Category"].isin(selected_categories) &
    df["Segment"].isin(selected_segments)
]

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selections.")
    st.stop()


# =====================================================
# KPI CALCULATIONS
# =====================================================

kpis = calculate_kpis(filtered_df)


# =====================================================
# KPI CARDS
# =====================================================

st.subheader("📌 Key Performance Indicators")
render_kpi_cards(kpis)


st.markdown("---")


# =====================================================
# CHARTS
# =====================================================

st.subheader("📈 Sales & Profit Analysis")
chart_data = render_all_charts(filtered_df)


st.markdown("---")


# =====================================================
# AI INSIGHTS
# =====================================================

render_ai_insights(kpis, chart_data)
