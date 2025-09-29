# apps/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, pathlib, os

app = FastAPI(title="AxiomPath API", version="0.1.0")

# --- ścieżki do drzewek ---
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
TREES_DIR = REPO_ROOT / "trees"

@app.on_event("startup")
def validate_trees_on_boot():
    if not TREES_DIR.exists():
        print(f"[trees] directory not found: {TREES_DIR}")
        return
    strict = os.getenv("STRICT_TREES", "0") == "1"
    bad = []
    for p in TREES_DIR.glob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad.append(f"{p.name}: {e}")
    if bad:
        msg = "Invalid tree JSON files:\n- " + "\n- ".join(bad)
        if strict:
            # przerwij start serwisu, żeby od razu naprawić błąd
            raise RuntimeError(msg)
        else:
            # tylko wypisz w logach — serwis wstanie
            print(msg)
