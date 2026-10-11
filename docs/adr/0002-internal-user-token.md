# 2. Internal user-token Slack app with read-only access

Status: Accepted

Date: 2026-10-11

## Context

Catching up after an absence requires fetching history as the individual user to view their accessible channels and personal direct messages. Bot tokens cannot see DMs or private channels unless explicitly invited, making them unsuitable for catching up as an individual.

Furthermore, on 29 May 2025, Slack restricted newly created commercially distributed / unlisted apps to 1 request per minute (max 15 messages) on `conversations.history` and `conversations.replies`. Internal custom apps retain Tier 3 rate limits (50+ requests per minute). Distributing a public OAuth client would hit severe rate limiting for multi-day catch-ups.

## Decision

v1 requires the user (or their workspace admin) to create an internal custom Slack app and paste a user token (`xoxp-`) into the setup wizard.

slack-rewind requests only read scopes (`channels:history`, `channels:read`, `groups:history`, `groups:read`, `im:history`, `im:read`, `mpim:history`, `mpim:read`, `users:read`, `users.profile:read`). No write permissions are requested or used.

The token is stored in the OS keyring (Windows Credential Manager / macOS Keychain).

## Consequences

- Ingestion retains Tier 3 throughput, allowing rapid backfill of multi-day absences.
- Setup requires a one-time step where the user creates an internal app. The app must provide clear visual onboarding steps in the wizard.
- Read-only guarantees that slack-rewind will never post messages, modify reactions, or alter channel read states.

