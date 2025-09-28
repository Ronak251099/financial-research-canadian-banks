
from __future__ import annotations
import pandas as pd

def ratios_from_common(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["ROE"] = df["NetIncome"]/df["TotalEquity"]
    out["ROA"] = df["NetIncome"]/df["TotalAssets"]
    out["NetProfitMargin"] = df["NetIncome"]/df["TotalRevenue"]
    out["Leverage"] = df["TotalAssets"]/df["TotalEquity"]
    out["RevenueYoY"] = df["TotalRevenue"].pct_change()
    out["NetIncomeYoY"] = df["NetIncome"].pct_change()
    return out
