import streamlit as st
st.markdown("""
<style>

/* Container spacing */
div[data-baseweb="tab-list"] {
    gap: 10px;
}

/* All tabs = pill style */
button[data-baseweb="tab"] {
    background-color: #1f2937 !important;
    border-radius: 999px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border: 1px solid #374151 !important;
    color: #cbd5e1 !important;
}

/* Active tab */
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #00ffcc !important;
    color: black !important;
    border: none !important;
}

/* Hover effect */
button[data-baseweb="tab"]:hover {
    background-color: #374151 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)





import pandas as pd
from modules.llm import generate_llm_summary
import pickle
import io
import matplotlib.pyplot as plt
import seaborn as sns

from modules.uploader import file_uploader
from modules.profiler import generate_profile, profile_to_text
from modules.preprocessing import (
    impute_missing_values,
    get_outlier_summary,
    treat_outliers_selected,
    remove_symbols_punctuation,
    encode_selected_columns,
    scale_features,
    get_outlier_bounds,
    get_imputers,
    get_symbol_cleaner,
    get_encoders,
    get_scaler
)
from modules.visualization import (
    univariate_analysis,
    bivariate_analysis,
    multivariate_analysis
)
from modules.missing_analysis import show_missing_summary, show_missing_matrix
from modules.utils import get_column_display_map


import pickle
import io

def create_download(data, filename, label):
    buffer = io.BytesIO()
    pickle.dump(data, buffer)
    buffer.seek(0)

    st.download_button(
        label,
        data=buffer,
        file_name=filename,
        mime="application/octet-stream"
    )


st.set_page_config(page_title="AI Data Processing App", layout="wide")
st.title("📊 AI-Powered Data Processing App")

if st.sidebar.button("🧹 Reset App"):
    st.session_state.clear()
    st.rerun()

# ---------------- FILE UPLOAD ---------------- #
df = file_uploader()

if df is not None:
    st.session_state["df"] = df

# ---------------- MAIN APP ---------------- #
if "df" in st.session_state:
    df = st.session_state["df"]

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Data",
        "🤖 LLM Summary",
        "📊 Profiling",
        "📈 EDA",
        "⚙️ Processing",
        "⬇️ Output"
    ])

    # ================= DATA ================= #
    with tab1:
        st.subheader("📄 Data Preview")
        st.dataframe(df)
        st.write(f"Shape: {df.shape}")

    # ================= LLM ================= #
    with tab2:
        st.subheader("🤖 AI Data Summary")

        df_current = st.session_state.get("df_processed", df)

        api_key = st.text_input(
            "Enter Groq API Key",
            type="password",
            key="groq_key"
        )

        if st.button("🚀 Generate AI Summary", key="llm_btn"):
            if not api_key:
                st.warning("Please enter your Groq API key")
            else:
                with st.spinner("Analyzing dataset..."):
                    profile = generate_profile(df_current)
                    profile_text = profile_to_text(profile)

                    summary = generate_llm_summary(profile_text, api_key)

                    st.session_state["llm_summary"] = summary

        # -------- DISPLAY -------- #
        if st.session_state.get("llm_summary"):
            st.markdown("### 📊 Insights")

            st.markdown(
                f"""
                <div style="
                    background-color:#0E1117;
                    padding:15px;
                    border-radius:10px;
                    border:1px solid #333;
                    ">
                    {st.session_state["llm_summary"]}
                </div>
                """,
                unsafe_allow_html=True
            )
    # ================= PROFILING ================= #
    with tab3:
        st.subheader("📊 Dataset Summary")
        profile = generate_profile(df)
        st.write(profile_to_text(profile))

    # ================= EDA ================= #
    with tab4:
        st.subheader("📈 Exploratory Data Analysis")

        df_eda = st.session_state.get("df_processed", df)
        col_map = get_column_display_map(df_eda)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            analysis_type = st.selectbox("Analysis Type", ["Univariate", "Bivariate", "Multivariate"])

        with col2:
            selected_x = st.selectbox("X Axis", list(col_map.keys()))
            col_x = col_map[selected_x]

        with col3:
            selected_y = st.selectbox("Y Axis", list(col_map.keys()))
            col_y = col_map[selected_y]

        with col4:
            chart_type = st.selectbox("Chart Type", ["Auto", "Histogram", "Boxplot", "Bar", "Scatter", "Violin"])

        if analysis_type == "Univariate":
            univariate_analysis(df_eda, col_x, chart_type)

        elif analysis_type == "Bivariate":
            if col_x != col_y:
                bivariate_analysis(df_eda, col_x, col_y, chart_type)
            else:
                st.warning("Select two different columns")

        elif analysis_type == "Multivariate":
            multivariate_analysis(df_eda)

    # ================= PROCESSING ================= #
    with tab5:

        df_current = st.session_state.get("df_processed", df)

        # -------- SYMBOL REMOVAL -------- #
        st.markdown("## ✂️ Remove Symbols & Punctuation")

        col_map = get_column_display_map(df_current)
        text_cols = df_current.select_dtypes(include="object").columns.tolist()
        text_display = [k for k, v in col_map.items() if v in text_cols]

        selected_text_display = st.multiselect("Select Columns", text_display)
        selected_text_cols = [col_map[c] for c in selected_text_display]

        if st.button("✂️ Remove Symbols"):
            if selected_text_cols:
                df_current, affected = remove_symbols_punctuation(df_current, selected_text_cols)
                st.session_state["df_processed"] = df_current
                st.session_state["symbol_msg"] = (
                    f"Symbols removed from {len(selected_text_cols)} column(s). "
                    f"{affected} rows affected."
                )
                symbol_cleaner = get_symbol_cleaner(selected_text_cols)
                st.session_state["symbol_artifact"] = symbol_cleaner
                st.rerun()
            else:
                st.warning("No columns selected")

        if st.session_state.get("symbol_msg"):
            st.success(st.session_state["symbol_msg"])
            del st.session_state["symbol_msg"]

        st.markdown("---")

        # -------- COLUMN DROP -------- #
        st.markdown("## 🗑️ Column Removal")

        col_map = get_column_display_map(df_current)
        drop_display = st.multiselect("Select Columns to Drop", list(col_map.keys()))
        drop_cols = [col_map[c] for c in drop_display]

        if st.button("🗑️ Drop Columns"):
            if drop_cols:
                df_current = df_current.drop(columns=drop_cols)
                st.session_state["df_processed"] = df_current
                st.session_state["drop_msg"] = (
                    f"{len(drop_cols)} column(s) removed: {', '.join(drop_cols)}"
                )
                st.rerun()

        if st.session_state.get("drop_msg"):
            st.success(st.session_state["drop_msg"])
            del st.session_state["drop_msg"]

        st.markdown("---")

        # -------- MISSING ANALYSIS -------- #
        st.markdown("## 🔍 Missing Value Analysis")

        col1, col2 = st.columns([1,1])
        with col1:
            show_missing_summary(df_current)
        with col2:
            show_missing_matrix(df_current)

        st.markdown("---")

        # -------- ROW REMOVAL -------- #
        st.markdown("## 🧹 Row-Level Missing Handling")

        threshold = st.slider("Remove rows if missing % >", 0, 100, 30)
        row_missing_ratio = df_current.isnull().mean(axis=1)
        rows_to_drop = (row_missing_ratio > threshold / 100).sum()

        st.info(f"{rows_to_drop} rows will be removed")

        if st.button("🗑️ Remove Rows"):
            df_current = df_current[row_missing_ratio <= threshold / 100]
            st.session_state["df_processed"] = df_current
            st.session_state["row_msg"] = f"{rows_to_drop} rows removed"
            st.rerun()

        if st.session_state.get("row_msg"):
            st.success(st.session_state["row_msg"])
            del st.session_state["row_msg"]

        st.markdown("---")

        # -------- IMPUTATION -------- #
        st.markdown("## 🧠 Missing Value Treatment")

        missing_cols = df_current.columns[df_current.isnull().any()].tolist()

        if missing_cols:
            col1, col2 = st.columns([1, 1])
            with col1:
                cat_cols = df_current[missing_cols].select_dtypes(include="object").columns.tolist()
                selected_cat = st.multiselect("Categorical Columns", cat_cols)
            with col2:
                num_cols = df_current[missing_cols].select_dtypes(include=["int64", "float64"]).columns.tolist()          
                selected_num = st.multiselect("Numerical Columns", num_cols)

            if st.button("🧠 Apply Imputation"):
                df_current = impute_missing_values(df_current, selected_cat, selected_num)
                st.session_state["df_processed"] = df_current

                total_cols = len(selected_cat) + len(selected_num)

                st.session_state["impute_msg"] = (
                    f"Missing values treated for {total_cols} column(s). "
                    f"Categorical: {len(selected_cat)}, Numerical: {len(selected_num)}"
                )
                imputers = get_imputers(df_current, selected_cat, selected_num)
                st.session_state["imputer_artifact"] = imputers
                st.rerun()

        if st.session_state.get("impute_msg"):
            st.success(st.session_state["impute_msg"])
            del st.session_state["impute_msg"]

        st.markdown("---")

        # -------- OUTLIERS -------- #
        st.markdown("## 📊 Outlier Analysis")

        outlier_summary = get_outlier_summary(df_current)
        outlier_df = pd.DataFrame.from_dict(
            outlier_summary, orient="index", columns=["Outliers"]
        )

        col1, col2 = st.columns([1, 1])

        # -------- LEFT -------- #
        with col1:
            st.markdown("### 📦 Table View")
            st.dataframe(outlier_df)

        selected_outliers = st.multiselect(
            "Select Columns",
            outlier_df.index.tolist(),
            key="outlier_cols"
        )

        # -------- BUTTON 1: SHOW PLOT -------- #
        if st.button("📦 Show Box Plot", key="show_boxplot_btn"):
            if selected_outliers:
                st.session_state["plot_cols"] = selected_outliers
            else:
                st.warning("Select at least one column")

        # -------- BUTTON 2: TREAT OUTLIERS -------- #
        if st.button("📉 Treat Outliers", key="outlier_treat_btn"):
            if selected_outliers:
                df_current = treat_outliers_selected(df_current, selected_outliers)
                st.session_state["df_processed"] = df_current

                # store bounds for pickle
                bounds = get_outlier_bounds(df_current, selected_outliers)
                st.session_state["outlier_artifact"] = bounds

                st.session_state["outlier_msg"] = (
                    f"Outliers treated in {len(selected_outliers)} column(s): "
                    f"{', '.join(selected_outliers)}"
                )
                st.rerun()
            else:
                st.warning("Select at least one column")

        # -------- RIGHT -------- #
        with col2:
            st.markdown("### 📦 Box Plot")

            plot_cols = st.session_state.get("plot_cols")

            if plot_cols:

                # ensure numeric only
                numeric_cols = df_current[plot_cols].select_dtypes(include=["int64", "float64"]).columns.tolist()

                if not numeric_cols:
                    st.warning("Selected columns are not numeric")
                else:
                    fig, ax = plt.subplots(figsize=(8, 5))

                    sns.boxplot(data=df_current[numeric_cols], ax=ax,showmeans=True, palette="Set2")

                    ax.set_title("Multi-Column Distribution")
                    ax.set_xticklabels(numeric_cols, rotation=30)

                    st.pyplot(fig)

            else:
                st.info("Click 'Show Box Plot' to visualize")
                st.markdown("---")

        # -------- ENCODING -------- #
        st.markdown("## 🔤 Encoding")

        cat_cols = df_current.select_dtypes(include="object").columns.tolist()

        selected_enc_cols = st.multiselect(
                                "Select Columns",
                                cat_cols,
                                key="encoding_cols"
                            )
        encoding_method = st.selectbox("Method", ["label", "onehot"])

        if st.button("🔤 Apply Encoding"):
            df_current = encode_selected_columns(df_current, selected_enc_cols, encoding_method)
            st.session_state["df_processed"] = df_current

            st.session_state["encoding_msg"] = (
                f"{encoding_method.capitalize()} encoding applied to "
                f"{len(selected_enc_cols)} column(s): {', '.join(selected_enc_cols)}"
            )
            st.session_state["encoder_config"] = {
                                                    "columns": selected_enc_cols,
                                                    "method": encoding_method
                                                }
            encoders = get_encoders(df_current, selected_enc_cols)
            st.session_state["encoder_artifact"] = encoders
            st.rerun()

        if st.session_state.get("encoding_msg"):
            st.success(st.session_state["encoding_msg"])
            del st.session_state["encoding_msg"]

        st.markdown("---")

        # -------- SCALING -------- #
        st.markdown("## 📏 Scaling")

        numeric_cols = df_current.select_dtypes(include=["int64", "float64"]).columns.tolist()

        target = st.selectbox("Target (not scaled)", ["None"] + numeric_cols)
        scaling_method = st.selectbox("Scaling Method", ["standard", "minmax"])

        if st.button("📏 Apply Scaling"):
            df_current, scaled_cols = scale_features(
                df_current,
                None if target == "None" else target,
                scaling_method
            )

            st.session_state["df_processed"] = df_current

            st.session_state["scaling_msg"] = (
                f"{scaling_method.capitalize()} scaling applied to "
                f"{len(scaled_cols)} column(s). Target excluded: {target}"
            )
            st.session_state["scaler_config"] = {
                                                "method": scaling_method,
                                                "target": target,
                                                "scaled_columns": scaled_cols
                                            }
            scaler = get_scaler(df_current, scaled_cols, scaling_method)
            st.session_state["scaler_artifact"] = scaler
            st.rerun()

        if st.session_state.get("scaling_msg"):
            st.success(st.session_state["scaling_msg"])
            del st.session_state["scaling_msg"]

        # -------- OUTPUT PREVIEW -------- #
        if "df_processed" in st.session_state:
            st.subheader("✅ Processed Data")
            st.dataframe(st.session_state["df_processed"])

    # ================= DOWNLOAD ================= #
    with tab6:
        st.subheader("⬇️ Download Processed Data")

        if "df_processed" in st.session_state:
            csv = st.session_state["df_processed"].to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv, file_name="processed.csv")

    # ================= PIPELINE ================= #
        st.markdown("### 📦 Saved Components")

        if st.button("Generate Outlier Pickle File"):
            data = st.session_state.get("outlier_artifact")

            if data:
                create_download(data, "outlier.pkl", "Download outlier.pkl")
            else:
                st.warning("Outliers not applied yet")


        if st.button("Generate Encoder Pickle File"):
            data = st.session_state.get("encoder_artifact")

            if data:
                create_download(data, "encoder.pkl", "Download encoder.pkl")
            else:
                st.warning("Encoding not applied yet")

                
        if st.button("Generate Scaler Pickle File"):
            data = st.session_state.get("scaler_artifact")

            if data:
                create_download(data, "scaler.pkl", "Download scaler.pkl")
            else:
                st.warning("Scaling not applied yet")


        if st.button("Generate Imputer Pickle File"):
            data = st.session_state.get("imputer_artifact")

            if data:
                create_download(data, "imputer.pkl", "Download imputer.pkl")
            else:
                st.warning("Imputation not applied yet")


        if st.button("Generate Symbol Cleaner Pickle File"):
            data = st.session_state.get("symbol_artifact")

            if data:
                create_download(data, "symbol_cleaner.pkl", "Download symbol_cleaner.pkl")
            else:
                st.warning("Symbol cleaning not applied yet")
            
else:
    st.info("Upload a dataset to begin")
