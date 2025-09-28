
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from rich import print as rprint

from src.utils import ensure_dirs, load_config, safe_save
from src.data_fetch import fetch_statements, latest_price_and_shares
from src.clean_transform import compute_common_fields
from src.bank_ratios import ratios_from_common
from src.make_report import write_markdown

def run():
    parser = argparse.ArgumentParser(description="Analyze Canadian banks")
    parser.add_argument("--tickers", nargs="*", default=None, help="Override tickers")
    args = parser.parse_args()

    ensure_dirs()
    cfg = load_config()
    universe = cfg["universe"] if args.tickers is None else {t: t for t in args.tickers}

    cache_dir = Path(cfg["settings"]["cache_dir"]) 
    processed_dir = Path(cfg["settings"]["processed_dir"]) 
    report_path = Path(cfg["settings"]["report_path"]) 

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("# Canadian Banks — Summary Report\n")

    rows = []
    for tk, name in universe.items():
        rprint(f"\n[bold cyan]Fetching[/] {name} ({tk}) …")
        bundles = fetch_statements(tk, cache_dir)
        income, balance = bundles.get("income"), bundles.get("balance")
        if income is None or income.empty or balance is None or balance.empty:
            rprint(f"[yellow]Warning:[/] missing statements for {tk}; skipping ratios.")
            continue

        common = compute_common_fields(income, balance)
        ratios = ratios_from_common(common)

        safe_save(common, processed_dir / f"{tk}_common.csv")
        safe_save(ratios, processed_dir / f"{tk}_ratios.csv")

        price, shares = latest_price_and_shares(tk)
        mcap = price * shares if (price and shares) else None

        write_markdown(report_path, name, {"ticker": tk}, common, ratios)

        last_c = common.dropna(how='all').iloc[-1]
        last_r = ratios.dropna(how='all').iloc[-1]
        rows.append({
            "Ticker": tk,
            "Name": name,
            "Price": price,
            "Shares": shares,
            "MarketCap": mcap,
            "TotalRevenue": last_c.get("TotalRevenue"),
            "NetIncome": last_c.get("NetIncome"),
            "TotalAssets": last_c.get("TotalAssets"),
            "TotalEquity": last_c.get("TotalEquity"),
            "ROE": last_r.get("ROE"),
            "ROA": last_r.get("ROA"),
            "NetProfitMargin": last_r.get("NetProfitMargin"),
            "Leverage": last_r.get("Leverage"),
        })

    if rows:
        league = pd.DataFrame(rows)
        league.sort_values(by=["ROE"], ascending=False, inplace=True)
        safe_save(league, processed_dir / "league_table.csv")
        rprint("\n[green]Saved league table:[/] data/processed/league_table.csv")
        rprint("[green]Report:[/] reports/summary.md")
    else:
        rprint("[red]No data pulled. Check tickers or connectivity.")

if __name__ == "__main__":
    run()
