def simplify_dtype(dtype):
    dtype = str(dtype)

    if "int" in dtype:
        return "int"
    elif "float" in dtype:
        return "float"
    elif "object" in dtype or "category" in dtype:
        return "cat"
    elif "datetime" in dtype:
        return "date"
    else:
        return dtype


def get_column_display_map(df):
    return {
        f"{col} ({simplify_dtype(df[col].dtype)})": col
        for col in df.columns
    }