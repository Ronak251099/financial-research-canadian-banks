
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import yaml

ROOT = Path(__file__).resolve().parents[1]

def ensure_dirs():
    (ROOT/"data"/"raw").mkdir(parents=True, exist_ok=True)
    (ROOT/"data"/"processed").mkdir(parents=True, exist_ok=True)
    (ROOT/"reports").mkdir(parents=True, exist_ok=True)

def load_config(path: str|Path = ROOT/"config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg

def safe_save(df, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=True)
