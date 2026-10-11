# 3. Privacy layer with local pseudonymization and rehydration

Status: Accepted

Date: 2026-10-11

## Context

Sending raw workplace chat history to third-party language models poses substantial privacy risks: real employee names, discussion topics, emails, and accidentally pasted tokens could leak outside the enterprise boundary.

Simply asking a model to "ignore names" via prompt engineering is insufficient and easily circumvented by prompt injection or conversational context.

## Decision

All message content sent to any model must first pass through a deterministic privacy layer (`protect` module).

The privacy layer:
1. Compiles an inventory of workspace users, channels, and emails.
2. Identifies detected secrets and sensitive patterns (tokens, keys, phones, IBANs).
3. Replaces identifiers with consistent per-run aliases (`Person_01`, `Channel_02`, `Email_03`). The active user is aliased as `You`.
4. Dispatches only the pseudonymized payload to the model.
5. Rehydrates real names strictly on the client machine before presenting the briefing in the desktop window.

The mapping table is maintained strictly in local memory and is never transmitted to the model or recorded in persistent exports.

## Consequences

- Real employee names and detected secrets never leave the local computer during model synthesis.
- The model can still understand interactions and conversational flow using consistent alias markers.
- Unit tests must enforce zero leakage of fixture identities and tokens in outbound payloads.

