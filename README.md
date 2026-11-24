# sweval: Swahili + English LLM eval kit

Benchmark language models on Swahili and English tasks (translation, summarization, local-context Q&A) and publish a comparison report to GitHub Pages.

## Why this exists
Most eval tooling is English-first, so teams building for East Africa have little evidence of how models actually perform in Swahili. This kit makes that measurable and repeatable.

## Quick start
```bash
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
sweval --model claude-sonnet-5-5 --model claude-haiku-5-5
open docs/index.html
```

## Scoring
- **chrF**: character n-gram F-score against a reference. Works better than BLEU for morphologically rich languages.
- **LLM judge**: 1-5 rating for correctness and fluency.

## Add your own tasks
Append lines to `data/tasks.jsonl`: `{"id","task","lang","prompt","reference"}`. The starter set is tiny on purpose. **Grow it to 50+ items per task type before drawing conclusions**, and have native speakers validate references.

## Publish
Repo Settings > Pages > deploy from `main` / `docs`.

## Roadmap
- [ ] Larger human-verified dataset (community contributions welcome)
- [ ] Sheng and code-switching tasks
- [ ] Multi-provider adapters
- [ ] Human-rating mode

## License
MIT
