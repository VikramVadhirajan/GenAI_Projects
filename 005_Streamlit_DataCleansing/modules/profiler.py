import pandas as pd


def generate_profile(df: pd.DataFrame) -> dict:
    """Generate lightweight dataset summary for LLM"""

    profile = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

    numerical_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    profile["numerical_summary"] = {
        col: {
            "mean": df[col].mean(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max(),
        }
        for col in numerical_cols
    }

    profile["categorical_summary"] = {
        col: {
            "unique_values": df[col].nunique(),
            "top_values": df[col].value_counts().head(5).to_dict(),
        }
        for col in categorical_cols
    }

    return profile




def profile_to_text(profile: dict) -> str:
    text = []

    text.append(
        f"The dataset contains {profile['rows']} rows and {profile['columns']} columns."
    )

    # Missing values summary
    missing = {k: v for k, v in profile["missing_values"].items() if v > 0}
    if missing:
        cols = ", ".join(missing.keys())
        text.append(f"Missing values are present in columns such as {cols}.")
    else:
        text.append("There are no missing values in the dataset.")

    # Numerical insight
    if profile["numerical_summary"]:
        num_cols = list(profile["numerical_summary"].keys())
        text.append(
            f"Numerical columns include {', '.join(num_cols)} with varying distributions."
        )

    # Categorical insight
    if profile["categorical_summary"]:
        cat_cols = list(profile["categorical_summary"].keys())
        text.append(
            f"Categorical columns include {', '.join(cat_cols)} with multiple unique values."
        )

    return " ".join(text)