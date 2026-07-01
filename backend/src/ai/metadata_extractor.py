import pandas as pd


def extract_metadata(df: pd.DataFrame) -> dict:
    rows, cols = df.shape
    col_names = df.columns.to_list()
    
    column_datatypes = {col: str(df[col].dtype) for col in col_names}
    
    missing_values = {col: df[col].isnull().sum() for col in col_names}

    sample_values = {col: df[col].head(5).astype(str).to_list() for col in col_names}

    metadata_dict = {
        "rows": rows,
        "columns": cols,
        "column_names": col_names,
        "column_datatypes": column_datatypes,
        "missing_values": missing_values,
        "sample_values": sample_values
    }

    return metadata_dict