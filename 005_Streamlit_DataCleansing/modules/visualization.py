import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# Styling
sns.set_style("whitegrid")
plt.rcParams.update({"font.size": 8})


# ---------------- CENTERED PLOT ---------------- #
def centered_plot(fig):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)


# ---------------- DOWNLOAD BUTTON ---------------- #
def get_download_button(fig, filename="plot.png"):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="⬇️ Download Chart",
            data=buf,
            file_name=filename,
            mime="image/png"
        )


# ---------------- AUTO INSIGHTS ---------------- #
def generate_auto_insights(df, col):
    insights = []

    if df[col].dtype in ["int64", "float64"]:
        skew = df[col].skew()

        if skew > 1:
            insights.append("Highly positively skewed distribution")
        elif skew < -1:
            insights.append("Highly negatively skewed distribution")
        else:
            insights.append("Fairly symmetric distribution")

        # Outlier detection (IQR)
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        outliers = df[
            (df[col] < Q1 - 1.5 * IQR) |
            (df[col] > Q3 + 1.5 * IQR)
        ]

        if len(outliers) > 0:
            insights.append(f"Contains {len(outliers)} potential outliers")

    else:
        counts = df[col].value_counts(normalize=True)

        if len(counts) > 0 and counts.iloc[0] > 0.7:
            insights.append("Highly imbalanced categorical variable")
        else:
            insights.append("Relatively balanced categories")

    return insights


# ---------------- UNIVARIATE ---------------- #
def univariate_analysis(df, col, chart_type="Auto"):
    st.subheader(f"Univariate Analysis: {col}")

    fig, ax = plt.subplots(figsize=(5, 3))
    is_numeric = df[col].dtype in ["int64", "float64"]

    try:
        if chart_type == "Histogram" or (chart_type == "Auto" and is_numeric):
            sns.histplot(df[col], kde=True, ax=ax)

        elif chart_type == "Boxplot":
            sns.boxplot(x=df[col], ax=ax)

        elif chart_type == "Bar" or (not is_numeric):
            df[col].value_counts().head(10).plot(kind="bar", ax=ax)

        else:
            st.warning("Selected chart type may not suit the data")

        fig.tight_layout()
        centered_plot(fig)
        get_download_button(fig, f"{col}_univariate.png")

        # Stats
        if is_numeric:
            st.write(df[col].describe())

        # Insights
        st.subheader("🔍 Auto Insights")
        insights = generate_auto_insights(df, col)
        for ins in insights:
            st.success(ins)

    except Exception as e:
        st.error(f"Error generating plot: {e}")


# ---------------- BIVARIATE ---------------- #
def bivariate_analysis(df, col1, col2, chart_type="Auto"):
    st.subheader(f"Bivariate Analysis: {col1} vs {col2}")

    fig, ax = plt.subplots(figsize=(5, 3))
    num_types = ["int64", "float64"]

    is_num1 = df[col1].dtype in num_types
    is_num2 = df[col2].dtype in num_types

    try:
        if chart_type == "Scatter" or (chart_type == "Auto" and is_num1 and is_num2):
            sns.scatterplot(x=df[col1], y=df[col2], ax=ax)

            corr = df[[col1, col2]].corr().iloc[0, 1]
            st.write(f"Correlation: {round(corr, 3)}")

        elif chart_type == "Boxplot":
            sns.boxplot(x=df[col1], y=df[col2], ax=ax)

        elif chart_type == "Violin":
            sns.violinplot(x=df[col1], y=df[col2], ax=ax)

        else:
            st.warning("Selected chart type may not suit the data")

        fig.tight_layout()
        centered_plot(fig)
        get_download_button(fig, f"{col1}_{col2}_bivariate.png")

    except Exception as e:
        st.error(f"Error generating plot: {e}")


# ---------------- MULTIVARIATE ---------------- #
def multivariate_analysis(df):
    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] > 1:
        fig, ax = plt.subplots(figsize=(6, 4))

        try:
            sns.heatmap(
                numeric_df.corr(),
                annot=True,
                cmap="coolwarm",
                ax=ax
            )

            fig.tight_layout()
            centered_plot(fig)
            get_download_button(fig, "correlation_heatmap.png")

        except Exception as e:
            st.error(f"Error generating heatmap: {e}")

    else:
        st.warning("Not enough numerical columns for correlation analysis")