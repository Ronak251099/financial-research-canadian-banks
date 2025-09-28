
from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd

def write_markdown(report_path: Path, bank_name: str, meta: Dict[str, str],
                   common: pd.DataFrame, ratios: pd.DataFrame):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n## {bank_name}\n")
        if meta.get("ticker"):
            f.write(f"**Ticker:** {meta['ticker']}\n\n")
        latest_c = common.dropna(how='all').iloc[-1]
        latest_r = ratios.dropna(how='all').iloc[-1]
        f.write("**Latest Snapshot (annual):**\n\n")
        f.write("- Total Revenue: {:,.0f}\n".format(latest_c.get("TotalRevenue", float('nan'))))
        f.write("- Net Income: {:,.0f}\n".format(latest_c.get("NetIncome", float('nan'))))
        f.write("- Total Assets: {:,.0f}\n".format(latest_c.get("TotalAssets", float('nan'))))
        f.write("- Total Equity: {:,.0f}\n\n".format(latest_c.get("TotalEquity", float('nan'))))
        f.write("**Key Ratios:**\n\n")
        f.write("- ROE: {:.2%}\n".format(latest_r.get("ROE", float('nan'))))
        f.write("- ROA: {:.2%}\n".format(latest_r.get("ROA", float('nan'))))
        f.write("- Net Profit Margin: {:.2%}\n".format(latest_r.get("NetProfitMargin", float('nan'))))
        f.write("- Leverage (Assets/Equity): {:.2f}x\n".format(latest_r.get("Leverage", float('nan'))))
        f.write("- Revenue YoY: {:.2%}\n".format(latest_r.get("RevenueYoY", float('nan'))))
        f.write("- Net Income YoY: {:.2%}\n".format(latest_r.get("NetIncomeYoY", float('nan'))))
