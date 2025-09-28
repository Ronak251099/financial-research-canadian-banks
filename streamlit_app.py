
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Canadian Banks — Research Dashboard", layout="wide")

DATA_DIR = Path("data/processed")

st.title("Canadian Banks — Research Dashboard")

league_path = DATA_DIR / "league_table.csv"
if not league_path.exists():
    st.warning("Run `python main.py` first to generate `data/processed/league_table.csv`.")
else:
    league = pd.read_csv(league_path)
    st.subheader("League Table (Latest Annual Snapshot)")
    st.dataframe(league, use_container_width=True)

    kpi = st.selectbox("Pick a KPI to compare", ["ROE", "ROA", "NetProfitMargin", "Leverage"])
    if kpi in league.columns:
        st.bar_chart(league.set_index("Name")[kpi])

    st.subheader("Per-bank Time Series (Computed)")
    tick = st.selectbox("Select bank", league["Ticker"].tolist()) if "Ticker" in league.columns else None
    if tick:
        ratios_path = DATA_DIR / f"{tick}_ratios.csv"
        common_path = DATA_DIR / f"{tick}_common.csv"
        if ratios_path.exists():
            ratios = pd.read_csv(ratios_path, index_col=0, parse_dates=True)
            st.write(f"**{tick} — Ratios**")
            st.line_chart(ratios[["ROE","ROA","NetProfitMargin","Leverage"]])
        else:
            st.info(f"Ratios file not found for {tick}: {ratios_path}")

        if common_path.exists():
            common = pd.read_csv(common_path, index_col=0, parse_dates=True)
            st.write(f"**{tick} — Financials (Common Fields)**")
            st.area_chart(common[["TotalRevenue","NetIncome","TotalAssets","TotalEquity"]])
        else:
            st.info(f"Common file not found for {tick}: {common_path}")
