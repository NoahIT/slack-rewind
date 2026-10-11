# 4. Deterministic selection and AI-generated narrative with grounding

Status: Accepted

Date: 2026-10-11

## Context

A user returning from leave may have thousands of missed messages across dozens of channels. Sending the entire corpus to an LLM is cost-prohibitive, exceeds context windows, and degrades synthesis quality.

Conversely, purely algorithmic heuristic summaries lack nuance, fail to synthesize cross-thread decisions, and read like disjointed message lists.

## Decision

slack-rewind separates input selection from synthesis:

1. **Deterministic selection:** Python code scores and filters candidate threads based on relevance to the user (@mentions, DMs, thread participation, questions, and activity density). The selection strictly respects a token budget.
2. **AI-generated narrative:** The model takes the anonymized selected threads and writes a cohesive briefing conforming to a strict JSON schema (sections: Needs you, Decisions, Announcements, By channel, Open threads, People).
3. **Grounding (cite or drop):** Every factual statement must cite source message identifiers (`channel_id`, `ts`, permalink). If a citation cannot be verified against the local database, the item is dropped.
4. **Graceful degradation:** If model calls fail or the provider is unreachable, slack-rewind renders the deterministically selected items with direct quotes, labelled clearly as unsummarized.

## Consequences

- The briefing provides coherent narrative summaries while remaining strictly grounded in real Slack messages.
- Hallucinations are actively discarded rather than surfaced to the user.
- If the user prefers not to use an LLM, the app still functions as a deterministic triage tool.

