import json
from collections import defaultdict
from pathlib import Path

import anthropic

from .scoring import chrf, judge


def load_tasks(path: str) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def run(models: list[str], tasks: list[dict]) -> dict:
    client = anthropic.Anthropic()
    rows = []
    for model in models:
        for t in tasks:
            out = client.messages.create(
                model=model, max_tokens=500,
                messages=[{"role": "user", "content": t["prompt"]}],
            ).content[0].text.strip()
            rows.append({
                "model": model, "id": t["id"], "task": t["task"], "lang": t["lang"],
                "output": out, "chrf": round(chrf(out, t["reference"]), 1),
                "judge": judge(t["prompt"], out, t["reference"]),
            })
    return {"rows": rows, "summary": summarize(rows)}


def summarize(rows: list[dict]) -> list[dict]:
    agg = defaultdict(lambda: {"chrf": [], "judge": []})
    for r in rows:
        k = (r["model"], r["lang"])
        agg[k]["chrf"].append(r["chrf"])
        agg[k]["judge"].append(r["judge"])
    return [
        {"model": m, "lang": l, "chrf": round(sum(v["chrf"]) / len(v["chrf"]), 1),
         "judge": round(sum(v["judge"]) / len(v["judge"]), 2), "n": len(v["chrf"])}
        for (m, l), v in sorted(agg.items())
    ]
