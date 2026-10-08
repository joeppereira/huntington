---
name: audit-indicators
description: Compute leading and lagging indicators for the current run, or roll them up across prior huntington pipeline runs. Use at the end of a run, periodically for trend review, or when asked how the pipeline is performing.
---

Read `specs/07-indicators.md` first.

1. Delegate to the `indicator-reporter` subagent.
2. For a single-run report: compute leading indicators from Requirement/Spec/Validation
   Memory, and lagging indicators from Run/Episodic Memory once human review has
   happened.
3. For a roll-up request: aggregate across all Run/Episodic records, but **never**
   collapse a severity-1 security finding into an averaged trend line — report it
   separately regardless of how the request was phrased.
4. Always present leading and lagging indicators as two distinct sections, never one
   blended score.
