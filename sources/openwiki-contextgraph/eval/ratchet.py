#!/usr/bin/env python3
"""Metric ratchet: floors only move up.

  python eval/ratchet.py check  [--results eval/results/enriched.json]
  python eval/ratchet.py update [--results eval/results/enriched.json]

`check` exits 1 if any metric in the results is below its floor in eval/ratchet.json.
`update` raises floors to current values (never lowers them) and records provenance.
"""

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATCHET = ROOT / "eval" / "ratchet.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["check", "update"])
    ap.add_argument("--results", default=str(ROOT / "eval" / "results" / "enriched.json"))
    args = ap.parse_args()

    results = json.loads(Path(args.results).read_text())
    metrics = results["metrics"]
    state = json.loads(RATCHET.read_text()) if RATCHET.exists() else {"floors": {}, "history": []}
    floors = state["floors"]

    if args.mode == "check":
        failures = [
            f"{k}: {metrics[k]:.4f} < floor {floors[k]:.4f}"
            for k in floors
            if k in metrics and metrics[k] < floors[k]
        ]
        for f in failures:
            print("RATCHET FAIL", f)
        if not failures:
            print(f"ratchet ok ({len(floors)} floors, arm={results.get('arm')})")
        return 1 if failures else 0

    raised = {k: v for k, v in metrics.items() if v > floors.get(k, -1)}
    floors.update(raised)
    state["history"].append(
        {"date": date.today().isoformat(), "arm": results.get("arm"), "raised": raised}
    )
    RATCHET.write_text(json.dumps(state, indent=2))
    print(f"floors now: {json.dumps(floors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
