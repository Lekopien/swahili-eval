import argparse

from .report import write_report
from .runner import load_tasks, run


def main() -> None:
    p = argparse.ArgumentParser(prog="sweval")
    p.add_argument("--model", action="append", default=None, help="Model to evaluate (repeatable)")
    p.add_argument("--tasks", default="data/tasks.jsonl")
    p.add_argument("--out", default="docs/index.html")
    args = p.parse_args()
    results = run(args.model or ["claude-sonnet-5-5"], load_tasks(args.tasks))
    write_report(results, args.out)
    print(f"Report written to {args.out}")


if __name__ == "__main__":
    main()
