
from __future__ import annotations
import pandas as pd

def pick(df: pd.DataFrame, col: str) -> pd.Series:
    if df is None or df.empty:
        return pd.Series(dtype="float64")
    if col in df.columns:
        return df[col]
    cands = [c for c in df.columns if col.lower() in c.lower()]
    if cands:
        return df[cands[0]]
    return pd.Series(index=df.index, dtype="float64")

def compute_common_fields(income: pd.DataFrame, balance: pd.DataFrame) -> pd.DataFrame:
    idx = income.index if income is not None and not income.empty else balance.index
    df = pd.DataFrame(index=idx)
    df["NetIncome"] = pick(income, "Net Income").fillna(pick(income, "NetIncomeApplicableToCommonShares"))
    df["TotalRevenue"] = pick(income, "Total Revenue").fillna(pick(income, "TotalRevenue"))
    if df["TotalRevenue"].isna().all():
        df["TotalRevenue"] = pick(income, "Operating Revenue").fillna(0)
        nii = pick(income, "Net Interest Income").fillna(0)
        nonii = pick(income, "Total Non-Interest Income").fillna(0)
        df["TotalRevenue"] = df["TotalRevenue"].where(df["TotalRevenue"]!=0, nii+nonii)
    df["TotalAssets"] = pick(balance, "Total Assets").fillna(pick(balance, "TotalAssets"))
    df["TotalEquity"] = pick(balance, "Total Stockholder Equity").fillna(pick(balance, "TotalEquity"))
    return df
