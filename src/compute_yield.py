import pandas as pd

def compute_yield(df: pd.DataFrame) -> pd.DataFrame:
    df["rental_yield"] = (df["annual_rent"] / df["property_value"]) * 100
    return df
