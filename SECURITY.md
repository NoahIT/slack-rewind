# Security policy

## Reporting a vulnerability

Please report security problems privately through [GitHub's vulnerability reporting](https://github.com/NoahIT/slack-rewind/security/advisories/new), not in a public issue.

Include what you found, how to reproduce it and the version or commit you used. I'll reply as soon as I can and keep you updated until it's fixed.

## Supported versions

There are no releases yet. Fixes go into the latest code on the `develop` branch and merge to `main`.

## What counts

slack-rewind ingests workplace chat and communicates with language models, so these matter most:

- real colleague names, personal emails, or detected secrets escaping the machine in model payloads;
- Slack user tokens or model API keys being written to SQLite, logs, or unencrypted storage;
- prompt injection in message text altering application execution or bypassing grounding;
- any operation writing to Slack (the tool is strictly read-only).

