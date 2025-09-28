
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Tuple
import pandas as pd
import yfinance as yf

STAT_KEYS = {
    "income": "financials",
    "balance": "balance_sheet",
    "cashflow": "cashflow",
}

def fetch_statements(ticker: str, cache_dir: Path) -> Dict[str, pd.DataFrame]:
    tk = yf.Ticker(ticker)
    out = {}
    for label, attr in STAT_KEYS.items():
        try:
            df = getattr(tk, attr)
            if df is None or df.empty:
                out[label] = pd.DataFrame()
                continue
            df_t = df.T
            df_t.index = pd.to_datetime(df_t.index)
            df_t.sort_index(inplace=True)
            out[label] = df_t
        except Exception:
            out[label] = pd.DataFrame()
    raw_path = cache_dir / f"{ticker}_raw.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        serializable = {k: v.reset_index().to_dict(orient="list") for k, v in out.items()}
        raw_path.write_text(json.dumps(serializable, default=str))
    except Exception:
        pass
    return out

def latest_price_and_shares(ticker: str) -> Tuple[float|None, float|None]:
    try:
        tk = yf.Ticker(ticker)
        info = tk.fast_info
        price = float(info.last_price) if getattr(info, "last_price", None) is not None else None
        shares = None
        try:
            shares = float(tk.get_shares_full(start="2010-01-01").iloc[-1]["SharesOutstanding"])
        except Exception:
            shares = float(getattr(info, "shares", None)) if getattr(info, "shares", None) else None
        return price, shares
    except Exception:
        return None, None
