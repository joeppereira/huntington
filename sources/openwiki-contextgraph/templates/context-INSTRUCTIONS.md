# OpenWiki brief: Q&A agent context graph (agent memory)

<!-- Copied by the backend to context-corpus/openwiki/INSTRUCTIONS.md every time the context corpus is
     (re)created. OpenWiki reads this for scope and priorities and never rewrites it. -->

## What this repository is

This repository is NOT a software codebase. It is the running log of a question-answering agent that
answers questions about a fictional bank (Crestline National Bank (CNB)). The agent answers using a
separate **semantic wiki** (the bank's documents) and writes one Markdown trace file per conversation turn:

- `sessions/<session-id>/session.md` - session metadata and a running list of turns.
- `sessions/<session-id>/turn-NNNN.md` - one file per turn. YAML front matter (session, turn number,
  timestamp, model, latency, confidence, tools used, semantic pages read) followed by sections:
  Question, Answer, Decision trace (ordered tool calls with inputs, results and timings), Sources cited,
  Reasoning summary (self-reported by the agent), Follow-up questions.

Ignore `AGENTS.md`, `CLAUDE.md`, `README.md` and this brief.

## Goal

Build a **context graph**: a linked wiki that records what the agent was asked, what it did, what it
decided, which knowledge it relied on, and how conversations connect over time. It must be detailed
enough to answer: "what has the user asked so far?", "why did the agent answer X?", "which sources
were used most?", "where was the agent unsure?", and "which earlier answer is this question following up?".

## Page types (use exactly these values in the front-matter `type` field)

| type | one page per | content |
|---|---|---|
| `Session` | session folder | start time, number of turns, topics covered, links to every Turn in order |
| `Turn` | turn file | the question, a short answer summary, confidence, latency, links to its Session, previous/next Turn, Decisions, Topics and SourceReferences |
| `Decision` | each meaningful choice in a decision trace | what was chosen (e.g. "searched semantic wiki for CECL scenario weights", "relied on Annual Report Note 6 over the Excel model", "declined to compute a new scenario"), why (from the reasoning summary and tool results), outcome |
| `ToolCall` | each distinct tool-call pattern | tool name, typical queries, how often used, which turns used it (aggregate repeated calls; do not create one page per individual call) |
| `SourceReference` | each semantic-wiki page the agent read | the semantic page path (e.g. `openwiki/models/cecl-allowance-model.md`), what it was used for, which Turns used it |
| `Topic` | each recurring subject the user asks about | e.g. CECL allowance, NII sensitivity, capital plan, API lineage; link to Turns and SourceReferences |
| `OpenQuestion` | each unresolved or low-confidence item | follow-ups the agent suggested, questions it could not answer, contradictions it noticed |
| `UserIntent` | each distinct goal the user appears to pursue across turns | e.g. "understand how models depend on APIs" |

Also maintain a `timeline` page listing all turns chronologically across sessions, and the reserved
`index.md`.

## Rules

- Every Turn page links to: its Session, the previous Turn (if any), each Decision it made, each Topic,
  and each SourceReference it read. Every Decision links back to its Turn.
- Copy exact facts from the trace files (timestamps, tool names, page paths, confidence values). Never
  invent tool calls or sources that are not in a trace file.
- Clearly label the "Reasoning summary" as the agent's self-report, not verified reasoning.
- Keep Turn pages short; put aggregate analysis (most-used sources, recurring uncertainty) on Topic,
  ToolCall and SourceReference pages.
- Add a Mermaid sequence diagram on each Session page showing user -> agent -> tools -> answer for its
  turns.
- Folder layout suggestion: `sessions/`, `turns/`, `decisions/`, `tools/`, `sources/`, `topics/`,
  `open-questions/`, `intents/`.
