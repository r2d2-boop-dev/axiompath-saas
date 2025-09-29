from fastapi import FastAPI
from pydantic import BaseModel
import json, pathlib

app = FastAPI(title="AxiomPath API", version="0.1.0")

class ClassifyIn(BaseModel):
    product_text: str
    declared_use: str | None = None
    market: str = "EU"
    language: str = "en"

@app.get("/health")
def health(): 
    return {"ok": True}

@app.get("/trees/{tree_id}")
def get_tree(tree_id: str):
    path = pathlib.Path(__file__).parents[2] / "trees" / f"{tree_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))

@app.post("/classify")
def classify(payload: ClassifyIn):
    # v0 demo: zawsze pytamy o główną funkcję produktu
    return {
      "status": "NEED_INFO",
      "questions": [{
        "attr":"function_primary",
        "question":"What is the product's primary function?",
        "options":["data_telecom","audio_video","measurement","power_conversion","other"]
      }],
      "candidates": [],
      "trace_id": "TRC-DEMO-001"
    }