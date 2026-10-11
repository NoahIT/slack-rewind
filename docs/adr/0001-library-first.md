# 1. Library first, single process

Status: Accepted

Date: 2026-10-11

## Context

slack-rewind could be built as a multi-tenant web application, a hosted SaaS with OAuth callbacks, or a local service with multiple background worker daemons.

A hosted architecture introduces significant data privacy and security burdens: storing company chat history and tokens on external infrastructure, managing multi-tenant isolation, and handling compliance risks. A multi-process setup introduces IPC overhead and process supervision issues on desktop machines.

## Decision

slack-rewind is structured as a typed Python library running in a single process on the user's machine. The library exposes clear interfaces for ingestion, storage, thread selection, privacy protection, and briefing synthesis.

The desktop window and developer CLI are thin frontends over this core library. Data is persisted in a local single-file SQLite database.

## Consequences

- All ingestion, processing, and persistence happen locally without an intermediate slack-rewind server.
- The core library remains testable offline using deterministic mock data and recorded fixtures.
- If a hidden loopback HTTP server is needed for desktop IPC, it binds strictly to 127.0.0.1 on an ephemeral port.

