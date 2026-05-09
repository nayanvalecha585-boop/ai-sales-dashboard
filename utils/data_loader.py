# =====================================================
# utils/data_loader.py
# Handles loading CSV — either default or user-uploaded
# =====================================================

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Loading dataset...")
def load_default_csv(path: str) -> pd.DataFrame | None:
    """Load the default superstore CSV from disk."""
    try:
        df = pd.read_csv(path, encoding="latin1")
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
        df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
        df["Year"] = df["Order Date"].dt.year
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def load_uploaded_csv(file) -> pd.DataFrame | None:
    """Load a user-uploaded CSV file."""
    try:
        df = pd.read_csv(file, encoding="latin1")

        # Try to parse Order Date if it exists
        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
            df["Year"] = df["Order Date"].dt.year

        return df
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None


def load_data(uploaded_file=None) -> pd.DataFrame | None:
    """
    Master loader — prefers user-uploaded file,
    falls back to the default dataset.
    """
    if uploaded_file is not None:
        return load_uploaded_csv(uploaded_file)
    return load_default_csv("data/superstore.csv")
