import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler



# ---------------- NULL HANDLING ---------------- #
def handle_nulls(df, method="drop"):
    if method == "drop":
        return df.dropna()

    elif method == "mean":
        return df.fillna(df.mean(numeric_only=True))

    elif method == "median":
        return df.fillna(df.median(numeric_only=True))

    elif method == "mode":
        return df.fillna(df.mode().iloc[0])

    return df


# ---------------- DUPLICATES ---------------- #
def remove_duplicates(df):
    return df.drop_duplicates()


# ---------------- STRING CLEANING ---------------- #
def clean_strings(df):
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()
    return df


# ---------------- OUTLIER (IQR) ---------------- #
def handle_outliers_iqr(df):
    df = df.copy()
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = np.where(df[col] < lower, lower, df[col])
        df[col] = np.where(df[col] > upper, upper, df[col])

    return df


# ---------------- ADVANCED IMPUTATION ---------------- #
def impute_missing_values(df, cat_cols, num_cols):
    df = df.copy()

    # ---- CATEGORICAL (Simple Imputer) ---- #
    if cat_cols:
        cat_imputer = SimpleImputer(strategy="most_frequent")
        df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])

    # ---- NUMERICAL (KNN Imputer) ---- #
    if num_cols:
        knn_imputer = KNNImputer(n_neighbors=5)
        df[num_cols] = knn_imputer.fit_transform(df[num_cols])

    return df


def drop_rows_by_missing_threshold(df, threshold_percent):
    df = df.copy()

    threshold = threshold_percent / 100

    row_missing_ratio = df.isnull().mean(axis=1)

    df = df[row_missing_ratio <= threshold]

    return df


# ---------------- OUTLIER SUMMARY ---------------- #
def get_outlier_summary(df):
    summary = {}

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        summary[col] = len(outliers)

    return summary


# ---------------- TREAT SELECTED OUTLIERS ---------------- #
def treat_outliers_selected(df, selected_cols):
    df = df.copy()

    for col in selected_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = np.clip(df[col], lower, upper)

    return df


# ---------------- REMOVE SYMBOLS ---------------- #
def remove_symbols_punctuation(df, cols):
    df = df.copy()
    affected_rows = set()

    for col in cols:

        def clean_value(x):
            if pd.isna(x):
                return x

            if not isinstance(x, str):
                return x  # leave numbers untouched

            # Step 1: temporarily protect numeric decimals
            x = re.sub(r'(\d)\.(\d)', r'\1__DOT__\2', x)

            # Step 2: remove all punctuation
            x = re.sub(r'[^\w\s]', '', x)

            # Step 3: restore decimal points
            x = x.replace("__DOT__", ".")

            return x

        original = df[col]
        cleaned = original.apply(clean_value)

        changed_idx = original != cleaned
        affected_rows.update(df[changed_idx].index.tolist())

        df[col] = cleaned

    return df, len(affected_rows)


# ---------------- SELECTIVE ENCODING ---------------- #
def encode_selected_columns(df, selected_cols, method):
    df = df.copy()

    if method == "label":
        for col in selected_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    elif method == "onehot":
        df = pd.get_dummies(df, columns=selected_cols)

    return df


# ---------------- SELECTIVE SCALING ---------------- #
def scale_features(df, target_col, method):
    df = df.copy()

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # remove target column
    if target_col in numeric_cols:
        numeric_cols.remove(target_col)

    if not numeric_cols:
        return df, []

    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    else:
        return df, []

    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df, numeric_cols


def get_outlier_bounds(df, cols):
    bounds = {}

    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        bounds[col] = {
            "lower": lower,
            "upper": upper
        }

    return bounds

def get_encoders(df, cols):
    encoders = {}

    for col in cols:
        le = LabelEncoder()
        df[col] = df[col].astype(str)
        le.fit(df[col])
        encoders[col] = le

    return encoders


def get_scaler(df, cols, method):
    if method == "standard":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()

    scaler.fit(df[cols])

    return scaler


def get_imputers(df, cat_cols, num_cols):
    imputers = {}

    if cat_cols:
        cat_imputer = SimpleImputer(strategy="most_frequent")
        cat_imputer.fit(df[cat_cols])
        imputers["categorical"] = cat_imputer

    if num_cols:
        num_imputer = KNNImputer()
        num_imputer.fit(df[num_cols])
        imputers["numerical"] = num_imputer

    return imputers


def get_symbol_cleaner(cols):
    return {
        "columns": cols,
        "pattern": r"[^\w\s]"
    }