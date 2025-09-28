
# Canadian Banks Research Analyst Project (Python)

A practical, mini‑project to analyze the **Big 6 Canadian banks** using Python. It fetches statements, computes bank‑specific KPIs, and generates tidy CSVs and a markdown report you can share.

```
## Quick Start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate

pip install -r requirements.txt

python main.py
# or a subset:
python main.py --tickers RY.TO TD.TO
```
Outputs:
- `data/processed/league_table.csv`
- per‑bank `*_common.csv` and `*_ratios.csv`
- `reports/summary.md`
