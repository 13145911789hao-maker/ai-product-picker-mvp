from fastapi import FastAPI
import json
from collections import defaultdict

app = FastAPI()

DATA_PATH = "output.json"


def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


@app.get("/top-products")
def top_products(limit: int = 20):
    data = load_data()
    return data[:limit]


@app.get("/trend-summary")
def trend_summary():
    data = load_data()
    trend = defaultdict(float)
    count = defaultdict(int)

    for item in data:
        style = item.get("style_group", "unknown")
        score = item.get("total_score", 0)
        trend[style] += score
        count[style] += 1

    result = {}
    for k in trend:
        result[k] = trend[k] / max(count[k], 1)

    return {
        "trend_score_by_style": result
    }


@app.get("/health")
def health():
    return {"status": "ok"}