# Typed-relation frontmatter schema (gap-fix round, 2026-10-10)

Contract between the corpus build (tools/augment_frontmatter.py) and the retrieval layer
(backend/app/retrieval). Derived deterministically from estate_ground_truth.json + page
sources — no LLM. Motivated by the 26 golden-set misses (docs/plan-retrieval-ratchets.md).

All relation values are **page refs** (`openwiki/<folder>/<slug>.md`); the validator
rejects refs that don't exist and type-pairs outside this table.

| field | on types | target type | source of truth |
|---|---|---|---|
| `owned_by` | System, Interface, Dataset | Team | GT systems.owner_team_current, interfaces.system→system owner |
| `owner` | Project | Person | GT jira.owner |
| `part_of` | Interface | System | GT interfaces.system |
| `status` | all entities | enum: `live \| deprecated \| proposed \| closed \| absent` | GT interfaces.status, jira.status (normalized; free text goes in `status_note`) |
| `supersedes` / `superseded_by` | Interface, Decision, Project | same | GT notes + ADR/PNG links (v1→EP-SPS-01 via ADR-PAY-019; PNG-1544→GTSI-0107) |
| `governed_by` | Concept, Interface, Dataset, Project | Policy | curated map (predictions/stats→MRM-POL-02+DUS-07; client disclosure→POL-FCC-014) |
| `relates_to` | Incident, Project, Document | any | GT jira.links phrases ("is caused by", "documented in") |
| `described_by` | System, Interface, Policy | Document | page `sources:` resources ↔ documents/ pages |
| `depends_on` | System, Interface | System, Interface | derived from source "Integration inventory" tables (consumer component → system; each consumed interface id → its owning system via `part_of`) + corroborated prose dependency statements for the payment-network systems |
| `aliases` | any | strings | GT names + curated vocab-gap table (see below) |

Alias table targets the measured vocab-gap failures: UETR ← "tracking number",
"parcel tracking"; gpi tracker pages ← "banks passed through", "route", "intermediary
banks", "freshness", "how fresh"; status APIs ← "where is my money", "payment location";
refresh/batch pages ← "up to date", "latest data".

`depends_on` derivation (tools/augment_frontmatter.py, deterministic + idempotent): the
source "Integration inventory"-style tables name a consumer component and the interface id
(EP-/EV-/BT- in parentheses) it consumes. The consumer component resolves to its system page
(via the interface page whose slug is that component, taking its `part_of`); each consumed
interface id resolves to its owning system via ground-truth `interfaces[].system`. A
`depends_on` ref to the owning system is written on the consumer's system page (deduped,
self-edges skipped). Additionally, plainly stated "<System> routes to / feeds / consumes /
funds-control against <System>" sentences for the payment-network systems are encoded from a
curated map, each corroborated against the depending page's own prose before it is written.
This closes the gap where the typed graph had no system→system edge (owned_by/part_of only),
so "which systems does X depend on" could not be assembled from the graph. Q1/Q5 regressions.

Retrieval consumes these as: typed graph edges (WikiGraph), alias-aware exact tier and
indexing, status facets for typed queries, Document-demotion via `described_by`, and the
gated second pass (entity-anchored re-query). Golden regression targets: G-001..003,
G-010, G-014, G-017, G-020, G-027, G-029, G-031, G-035, G-040..045, G-058.

## ID-closure requirement (ENFORCED, added 2026-10-10)

**Every identifier-grammar token appearing in the raw source documents MUST resolve to a
page's `entity_id` or alias** — exactly, by zero-padding normalization, as a prefix
fragment of a claimed id, or via a `SYS-`/`DOC-` prefixed form. Codes about the topic
(systems, endpoints, teams, people, controls, templates, model-registry ids…) are
**index keys, not prose**: an unresolved code is a page or frontmatter field the build
failed to emit. Exclusions: external regulator citations (`FIL-`, `FFIEC-`, `FTC-`,
`ISO-`, `RFC-`), tokens with ≥6-digit numeric segments (instance data: wire refs,
serials), and tokens inside code blocks/spans (example payloads).

- **Enforcement:** `tools/validate_corpus.py` `check_id_closure` — build fails on any
  unresolved token. This is the static twin of the eval's `id_coverage` metric; the
  meta-rule is *for every eval metric, enforce its build-time invariant in the validator*.
- **Producer side:** `tools/assign_canonical_ids.py` derives canonical ids from ground
  truth (teams TEAM-*, people P-*, HRC codes, doc_ids, model-register/control/template
  families) and creates registry pages for id families with no page of their own
  (Jira backlog, proposed-but-nonexistent interfaces). Pages with more than 6 ids are
  registries: in retrieval, only their PRIMARY id pins to rank 1.
