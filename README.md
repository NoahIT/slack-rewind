# slack-rewind

A local-first catch-up tool for people returning from leave. Acting as you, it ingests missed Slack messages, strips real names and secrets in a local privacy layer, generates a cited briefing through a model, and rehydrates real names strictly on screen in a desktop window.

## Status

Early development. The tooling skeleton, architecture decisions, and threat model are in place. Slack ingestion and SQLite storage are underway.

## How it works

1. **Ingest as you:** connect via an internal user token. Reads only channels and direct messages you already belong to.
2. **Deterministic selection:** score and filter relevant threads (@mentions, DMs, discussions you took part in, and team questions) within a token budget.
3. **Local privacy layer:** replace user names, handles, emails, channels, and detected secrets with stable aliases (`Person_01`, `Channel_02`, `You`). The alias map never leaves process memory.
4. **Model synthesis with grounding:** the model writes a structured catch-up briefing. Every claim must cite verified Slack message timestamps ("cite or drop").
5. **Desktop window:** a native window (React in a Python-managed host) displays the briefing with real names rehydrated locally on screen.

## What it won't do

- **Never write to Slack:** strictly read-only. No posting messages, no reactions, no marking channels read.
- **Never expose names to cloud models:** real identities are stripped before requests leave your machine and restored only in your local window.
- **Not a loopback browser URL:** no opening `http://localhost:8000` or managing local servers.
- **Not a workspace bot or compliance tool:** designed for personal return-from-leave catch-up on Free and Pro tiers, not workplace monitoring.

## Development

Requires Python 3.12 or newer, [Poetry](https://python-poetry.org/) 2.x, and GNU Make.

```
make install    # install dependencies and git hooks
make lint       # format check, ruff lint and mypy strict
make test       # pytest with branch coverage
```

## License

[Apache License 2.0](LICENSE).
