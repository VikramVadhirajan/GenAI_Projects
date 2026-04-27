import pandas as pd
import streamlit as st


def load_file(uploaded_file):
    """Load CSV or Excel file into DataFrame"""
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type")
        return None

    return df


def file_uploader():
    """Streamlit file uploader UI"""
    uploaded_file = st.file_uploader(
        "Upload your dataset (CSV or Excel)", type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        df = load_file(uploaded_file)
        return df

    return None