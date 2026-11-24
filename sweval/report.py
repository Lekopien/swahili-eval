import html
import json
from pathlib import Path

TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Swahili vs English LLM eval</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--card:#f5f5f4;--line:#ddd}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161616;--fg:#eee;--card:#222;--line:#333}}}}
body{{font:16px/1.5 system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:900px;margin:0 auto;padding:24px 16px}}
.wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;margin:12px 0 32px}}
th,td{{border-bottom:1px solid var(--line);padding:8px;text-align:left;font-size:14px;vertical-align:top}}
th{{background:var(--card)}}
</style></head><body>
<h1>Swahili vs English LLM eval</h1>
<h2>Summary</h2><div class="wrap"><table><tr><th>Model</th><th>Lang</th><th>chrF</th><th>Judge (1-5)</th><th>n</th></tr>{summary}</table></div>
<h2>All results</h2><div class="wrap"><table><tr><th>Model</th><th>Task</th><th>Lang</th><th>Output</th><th>chrF</th><th>Judge</th></tr>{rows}</table></div>
</body></html>"""


def write_report(results: dict, out: str = "docs/index.html") -> None:
    s = "".join(
        f"<tr><td>{html.escape(r['model'])}</td><td>{r['lang']}</td><td>{r['chrf']}</td><td>{r['judge']}</td><td>{r['n']}</td></tr>"
        for r in results["summary"]
    )
    rows = "".join(
        f"<tr><td>{html.escape(r['model'])}</td><td>{r['task']}</td><td>{r['lang']}</td>"
        f"<td>{html.escape(r['output'])}</td><td>{r['chrf']}</td><td>{r['judge']}</td></tr>"
        for r in results["rows"]
    )
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(TEMPLATE.format(summary=s, rows=rows))
    Path(out).with_name("results.json").write_text(json.dumps(results, indent=2))
