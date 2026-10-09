---
type: Timeline
title: "Timeline: All Turns in Chronological Order"
description: Cross-session chronological index of every recorded conversation turn; currently empty because no sessions or turns have been ingested yet.
tags: [timeline, index, sessions, turns, chronology]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T20:59:04.422Z
sources:
  - id: openwiki-source-6f457e41d4f8c04f8264a562
    resource: repo://sessions/.gitkeep
generated: { by: "openwiki/0.7.0", at: "2026-10-09T20:59:04.422Z" }
---

## Purpose

This page is the single, reserved cross-session index of every turn answered by the
Q&A agent, ordered strictly by timestamp regardless of which session they belong to.
It exists to answer "what has the user asked so far?" across the whole history of the
agent, as required by the context-graph brief (see
[Context Graph Model](concepts/context-graph-model.md) and
[Build Context Graph](workflows/build-context-graph.md)).

## Status

No turns have been recorded yet. The `sessions/` source directory contains no
session folders or turn files (only a placeholder `.gitkeep`), so there is nothing to
list. This page states that plainly rather than fabricating entries.

## How this page will be maintained

Once session folders and `turn-NNNN.md` files appear under `sessions/`, each turn will
be appended here in strict chronological order using the exact `timestamp` value from
that turn's YAML front matter (as described in
<!-- openwiki: broken internal link [../INSTRUCTIONS.md] file "../INSTRUCTIONS.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[../INSTRUCTIONS.md](../INSTRUCTIONS.md)). Each entry will include:

- The timestamp, copied verbatim from the turn's front matter.
- The session identifier and turn number.
- A short summary of the question asked.
- A link to the corresponding Turn page.

Entries must never be reordered to group by session; the ordering key is always the
timestamp, so turns from different sessions will interleave here if their timestamps
interleave. No turn, timestamp, question, or answer should be invented — only facts
copied directly from `sessions/<session-id>/turn-NNNN.md` files are eligible for
inclusion.

## Turns

_(none yet — pending the first recorded session/turn)_
