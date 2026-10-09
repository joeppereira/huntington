---
type: quickstart
title: "Quickstart: MHFC Agent Trace Log & Context Graph"
description: Entry point explaining that this repository is a Q&A agent's trace log (not application code) and routing readers to the trace-format, context-graph model, build workflow, refresh pipeline, and timeline pages.
tags: [quickstart, overview, trace-log, context-graph, openwiki, navigation]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T20:59:04.422Z
sources:
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-6f457e41d4f8c04f8264a562
    resource: repo://sessions/.gitkeep
generated: { by: "openwiki/0.7.0", at: "2026-10-09T20:59:04.422Z" }
---

## What this repository is

This repository is **not a software codebase**. There is no application to
build, run, or deploy here. It is the running trace log of a
question-answering agent that answers questions about a fictional bank,
Meridian Harbor Financial Corp. (MHFC), by consulting a separate semantic
wiki of the bank's documents. As the agent answers each question, it writes
one Markdown trace file per conversation turn to disk under `sessions/`:

- `sessions/<session-id>/session.md` - session metadata and a running list of
  turns.
- `sessions/<session-id>/turn-NNNN.md` - one file per turn, with YAML front
  matter (session, turn number, timestamp, model, latency, confidence, tools
  used, semantic pages read) followed by Question, Answer, Decision trace,
  Sources cited, Reasoning summary, and Follow-up questions sections.

See [Trace Log Format](concepts/trace-log-format.md) for the full schema.

`AGENTS.md`, `README.md`, and `openwiki/INSTRUCTIONS.md` describe this scope
and the generation brief; they are not themselves sources of trace content
and are out of scope as evidence for context-graph pages.

### Current state of the trace log

As of this writing, `sessions/` contains **no session or turn files yet** -
only a placeholder `sessions/.gitkeep`. No sessions, turns, decisions, tool
calls, or sources have been recorded. Every page in this wiki that discusses
the trace log's shape is describing the schema as specified in
`openwiki/INSTRUCTIONS.md`, not content observed in real files. Nothing here
should be read as an example of an actual recorded conversation; none exist
yet.

## What the context graph is for

On top of the raw trace log, this OpenWiki instance builds a **context
graph**: a linked wiki that re-organizes trace facts into typed pages so a
reader can answer questions that span many turns and sessions, such as:

- What has the user asked so far?
- Why did the agent answer a particular way?
- Which sources (semantic-wiki pages) were used most?
- Where was the agent unsure, or what did it leave unresolved?
- Which earlier answer is a given question following up on?

The graph has eight page types (`Session`, `Turn`, `Decision`, `ToolCall`,
`SourceReference`, `Topic`, `OpenQuestion`, `UserIntent`) plus a reserved
cross-session `timeline` page. See
[Context Graph Model](concepts/context-graph-model.md) for the full schema
and the mandatory link rules between page types.

Because no trace files exist yet, **no context-graph pages of these types
have been generated yet either**. The timeline page exists as a reserved,
currently-empty index (see below).

## How the graph gets built and kept up to date

- [Build Context Graph](workflows/build-context-graph.md) describes the
  end-to-end process for turning newly added `session.md` / `turn-NNNN.md`
  files into Decision, ToolCall, SourceReference, Topic, UserIntent, and
  OpenQuestion pages, linking them, and extending the timeline.
- [Wiki Refresh Pipeline](operations/wiki-refresh-pipeline.md) documents the
  scheduled GitHub Actions workflow
  (`.github/workflows/openwiki-update.yml`) that runs `openwiki code --update`
  daily, regenerates the graph from any new trace files, and opens a pull
  request with the result.
- [Timeline](timeline.md) is the single, reserved chronological index of
  every turn across all sessions. It is currently empty, pending the first
  recorded session and turn, and must be appended to in timestamp order as
  turns are ingested.

## Where to go next

| If you want to... | Go to |
|---|---|
| Understand the exact on-disk shape of `session.md` / `turn-NNNN.md` | [Trace Log Format](concepts/trace-log-format.md) |
| Understand the context-graph page types and required links | [Context Graph Model](concepts/context-graph-model.md) |
| Understand how trace files turn into context-graph pages | [Build Context Graph](workflows/build-context-graph.md) |
| Understand the automation that regenerates the graph | [Wiki Refresh Pipeline](operations/wiki-refresh-pipeline.md) |
| See every recorded turn in chronological order | [Timeline](timeline.md) |

## Ground rules for anyone extending this wiki

- Treat `sessions/<session-id>/session.md` and `turn-NNNN.md` files as the
  only source of truth for context-graph content. Never invent tool calls,
  sources, decisions, timestamps, or turns that are not present in an actual
  trace file.
- Ignore `AGENTS.md`, `CLAUDE.md`, `README.md`, and `openwiki/INSTRUCTIONS.md`
  as sources of wiki *content* - use them only to understand scope and the
  generation brief.
- Label any content drawn from a turn's "Reasoning summary" section as the
  agent's self-report, not verified reasoning, per
  [Trace Log Format](concepts/trace-log-format.md).
