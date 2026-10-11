# Golden evaluation set — CNB payments-estate semantic wiki

`golden_cnb.json` contains 70 evaluation questions for agents answering over the
CNB (Crestline National Bank) semantic corpus at
`sources/openwiki-contextgraph/semantic-corpus-cnb/openwiki/`.

All expected answers and entity IDs were verified against
`sources/demo-docs/Wire_Tracking_Demo_Kit/estate_ground_truth.json` (the scoring
ground truth, as_of 2026-10-05 — never ingest it into the graph) and
cross-checked against the actual wiki pages and, where needed, the raw source
documents under `semantic-corpus-cnb/sources/estate/`.

## Item schema

```json
{
  "id": "G-001",
  "question": "natural-language question",
  "class": "one of eleven classes below",
  "expected_answer": "concise ground-truth answer the response is scored against",
  "expected_refs": ["openwiki/<folder>/<page>.md", "..."],
  "expected_entity_ids": ["EP-SPS-01", "..."],
  "hazard": "optional — why this item is hard or what known defect it probes",
  "source": "ground_truth | demo_pack | diagnosed_failure | authored"
}
```

- `expected_refs` are paths relative to `semantic-corpus-cnb/` — the wiki pages
  that should ground a correct answer. Empty for unanswerable items.
- `expected_entity_ids` come from **ground truth, not page frontmatter**. At
  authoring time several wiki pages carried corrupted `entity_id` frontmatter
  (see "Known corpus gaps" below); a concurrent repair pass is fixing them.
  Score entity-ID recall against this field, never against stale frontmatter.
- `source` provenance:
  - `ground_truth` — authored directly from facts in `estate_ground_truth.json`.
  - `demo_pack` — the scripted questions from the PM demo
    (`PROJECT_CONTEXT_Semantic_Graph_PM_Demo.md` §8 / the Demo Pack PDF); the
    question text is the demo's user wording, the expected answer is the demo's
    target answer. Included: Q1 (G-020), Q2 (G-037), Q3 (G-021), Q4 (G-042),
    Q5 (G-022), Q8 (G-026), Q9 (G-035), plus demo-derived items G-025, G-040, G-059.
  - `diagnosed_failure` — regression items reproducing previously observed wrong
    answers (G-008, G-009, G-015, G-032).
  - `authored` — written for this set to probe collisions, vocabulary gaps,
    Jira-only entities, and unanswerables.

## Question classes

| Class | Tests | Items |
|---|---|---|
| `entity_lookup` | Direct retrieval of one entity's facts (what/limits/values) | 8 |
| `ownership` | Who owns a system/epic/policy, including temporal ownership changes | 7 |
| `deprecation_supersession` | Deprecated/replacement pairs, sunsets, superseded proposals | 5 |
| `dependency_impact` | Multi-page traversal: dependencies, blockers, conflicts, feasibility | 8 |
| `inventory_coverage` | Exhaustive enumeration (endpoints, event types, gaps) | 5 |
| `incident_history` | Incidents, PIRs, complaints and the decisions they produced | 5 |
| `policy_constraint` | What POL-FCC-014 / DUS-07 / MRM-POL-02 / ADRs permit or forbid | 8 |
| `hard_vocab_gap` | Paraphrased questions sharing no words with page titles | 5 |
| `collision_disambiguation` | Near-identical names across types (system vs team, policy vs document) | 4 |
| `negative_unanswerable` | Facts deliberately absent — correct behavior is to say so | 5 |
| `typo_id` | Corrupted-identifier questions probing the deterministic fuzzy ID tiers | 10 |

### `typo_id` class (G-061–G-070)

Each `typo_id` item is a variant of a clean-ID twin (named in its `hazard`) whose
only change is a corrupted identifier in the question; `expected_refs` /
`expected_entity_ids` are copied from the twin. The corruptions map one-to-one to
the retriever's fuzzy ID tiers (`backend/app/retrieval/retriever.py`):

- G-061 zero-padding drop (`EP-PPH-1`) and G-068 four-digit-segment padding drop
  (`GTSI-107`) — `_norm_id` normalization;
- G-062 adjacent transposition (`CBO-3970`), G-063 substitution (`PIR-2924-07`),
  G-067 head transposition (`MCP-2026-1189`), G-066 two-error long id
  (`CNB-MEM0-2026-9`) — whole-token Damerau-Levenshtein with length-scaled budget
  (1/<8 chars, 2/<14, 3/≥14), transposition = 1 error;
- G-064 separator-broken (`EP PPH 01`) and G-065 missing-hyphen (`EPSPS01`) —
  moving-pattern scan over the separator-normalized stream (fires only when
  tokenization yields no ID token);
- G-069 deliberate ambiguity (`GTSI-0117`, distance 1 from GTSI-0107/0112/0115 on
  three different pages) — unique-minimum-distance rule: ties → NO pin; and
  G-070 registry guard (`CBO-4412`, both nearest ids live only on the 20-id Jira
  backlog registry page) — registry pages (>6 ids) are never pinned by secondary
  ids. For these two, rank-1 pinning is NOT expected — only top-10 via BM25.

## Known corpus gaps and defects this set deliberately probes

1. **Interface-page collapse (31 → 11).** Ground truth defines 31 interface
   entries (EP-/EV-/BT- ids, including 5 marked DOES NOT EXIST); the wiki
   collapses them into 11 `interfaces/` pages (multi-endpoint pages such as
   `EP-PPH-04..07` and `EP-ENS-01..03`; no dedicated pages for `EP-CBO-01..03`
   or the five nonexistent proposals). Items G-028–G-031 are expected to FAIL
   on exhaustive recall today — they are in the set to measure this gap
   (`hazard: coverage_gap`).
2. **Corrupted `entity_id` frontmatter** (under concurrent repair; score against
   ground truth):
   - `interfaces/sps-read-model-api.md` → `EP-PPH-01` (should be `EP-SPS-01`) — G-002, G-015;
   - `incidents/cmp-2026-1189.md` → `PIR-2024-07` (should be `CMP-2026-1189`) — G-032, G-034;
   - `projects/gtsi-0107-gpi-real-time-service.md` → `CBO-3790` (should be `GTSI-0107`) — G-017;
   - `projects/gtsi-0112-gpi-knowledge-transfer.md` → `CBO-4480` (should be `GTSI-0112`) — G-009.
3. **Jira-only entities.** Jason Park (owner of CBO-4388, CBO-4402, and others)
   and Mei Tanaka (QA lead, CBO-4522) have no `people/` pages; they exist only
   in the Jira export document/source. Items G-013, G-014
   (`hazard: jira_only_entity`).
4. **Deliberately excluded documents.** Sarah Whitfield's Wire Tracking concept
   / market research and the Demo Pack are never ingested; questions about her
   (G-053) must be answered "not in the wiki."
5. **Title/type collisions.** System vs team (`cbo-wire-center` vs
   `cbo-wire-center-squad`; ENS system vs Enterprise Notification Platform
   team) and policy vs document vs incident pages sharing an ID
   (POL-FCC-014, PIR-2024-07). Items G-049–G-052.
6. **Temporal ownership.** The gpi connector moved PNE → GTSI effective
   2026-10-01 (CNB-MEMO-2026-09); older documents (PNG-TDD-6.0, spike CBO-4480)
   still name the old owner. Latest `valid_from` must win. Items G-009, G-012, G-020.

## Scoring guidance

- **expected_answer**: grade on factual agreement with the stated facts
  (ids, dates, owners, numbers), not wording.
- **expected_refs**: at least one listed page should be cited/grounded for
  answerable items; for `negative_unanswerable`, any confident fabricated
  answer scores zero regardless of citations.
- **expected_entity_ids**: recall over the listed ids; for inventory items,
  report recall fraction rather than pass/fail.
