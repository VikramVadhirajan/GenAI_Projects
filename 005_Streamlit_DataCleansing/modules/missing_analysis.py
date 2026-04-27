import streamlit as st
import missingno as msno
import matplotlib.pyplot as plt
import pandas as pd


def show_missing_summary(df):
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    summary_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percent.round(2)
    })
    summary_df["Missing %"] = summary_df["Missing %"].astype(str) + " %"
    # sort by highest missing %
    summary_df = summary_df.sort_values(by="Missing %", ascending=False)

    st.dataframe(summary_df)

def show_missing_matrix(df):
    # Bigger figure
    fig, ax = plt.subplots(figsize=(10, 5))

    msno.matrix(
        df,
        ax=ax,
        sparkline=False,
        fontsize=8    # smaller labels
    )

    # Rotate labels for better fit
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    fig.tight_layout()

    st.pyplot(fig) 