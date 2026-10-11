# Threat model

Version 0, 2026-10-11. Describes the security and privacy design of slack-rewind.

## What slack-rewind does

slack-rewind runs on a user's local computer. Acting as the user via a read-only Slack user token, it fetches message history and metadata for channels and direct messages the user belongs to. It stores messages in a local SQLite database, deterministically selects conversations from an away window, anonymizes names and detected secrets through a local privacy layer, passes the anonymized payload to an LLM provider to synthesize a catch-up briefing, and renders the briefing in a desktop window with real names rehydrated locally on screen.

## What needs protecting

- **Workplace communications:** message text, attachments, links, and discussions from private channels and direct messages.
- **Identities and relationships:** real names, usernames, display names, and communication patterns of colleagues.
- **Slack credentials:** user token (`xoxp-`) with read access to the workspace.
- **LLM API keys:** credentials used to communicate with cloud model providers.
- **Local machine security:** the user's filesystem and processes.

## Trust boundaries

| Entity / Input | Trust level | Rationale |
|---|---|---|
| User command line / UI inputs | Trusted | The user initiates the run and selects parameters. |
| Slack API responses | Semi-trusted | Authentic Slack data, but message text contains arbitrary third-party and peer input. |
| Message text (untrusted content) | Untrusted | May contain malicious prompts (prompt injection), sensitive PII, or leaked secrets. |
| Cloud LLM providers | Untrusted with raw data | Must never receive real colleague names, real personal emails, or corporate secrets. |
| Local LLM (Ollama) | Local only | Data does not leave the host, but privacy layer still applies uniformly. |
| LLM generated output | Untrusted | Model output could hallucinate claims, omit context, or reflect injection attempts. |

## Threats and mitigations

| Threat | Mitigation |
|---|---|
| Colleague names or PII leak to cloud LLMs | The privacy layer builds an inventory of all workspace users and channels, replacing every name, handle, email, phone number, and IBAN with stable synthetic aliases (`Person_01`, `Channel_02`, `You`) before sending data over the network. |
| Hardcoded secrets or tokens in messages leak to LLM | Regex scanners identify high-entropy strings, token prefixes (`xoxp-`, `ghp_`, `AKIA`, `Bearer `), and credential patterns, masking them prior to model dispatch. |
| Prompt injection via Slack message content | Message content is isolated inside data containers and never interpreted as system or tool instructions. The model schema strictly enforces output structure (JSON briefing format). |
| Hallucinated claims in briefing | The briefing engine enforces "cite or drop": every factual summary bullet must include message citations (`channel_id`, `ts`, permalink) resolving to verified SQLite records. Unreferenced claims are discarded. |
| Slack token theft from local disk | Slack user tokens and LLM API keys are stored in the OS keyring (Windows Credential Manager / macOS Keychain), never in SQLite or plaintext configuration files. |
| Unintended modification of Slack workspace state | slack-rewind requests only read scopes (`:history`, `:read`) and never issues write API calls (`chat.postMessage`, `reactions.add`, `conversations.mark`). |
| Multi-user data leakage on shared machines | Single user identity per database instance. Disconnecting an account purges both the local SQLite store and the keyring entry. |
| Local loopback server exposure | If an internal HTTP/WS server is used for desktop UI IPC, it binds strictly to `127.0.0.1` on an ephemeral OS-assigned port. It never binds to `0.0.0.0`. |

## Supply chain security

- **Dependency vetting:** `poetry.toml` enforces `min-release-age = 14`. All dependencies must be at least 14 days old.
- **Vulnerability scanning:** OSV-Scanner audits `poetry.lock` in CI. Dependabot audits dependencies with a 14-day cooldown.
- **Secret leak prevention:** gitleaks runs on pre-commit hooks and full commit history in CI.
- **Action pinning:** GitHub Actions are pinned to full commit SHAs.

## Accepted risks for v1

- slack-rewind operates with the permissions of the logged-in desktop user.
- Local SQLite database on disk is unencrypted at rest; file security relies on OS user account isolation and NTFS permissions.

