# 7. Workflow, branching model, and clean commit style

Status: Accepted

Date: 2026-10-11

## Context

The repository aims for high engineering quality and clear portfolio depth. The git history should reflect human-sized, logical changes that can be reviewed and understood individually.

Squashing large branches or generating generic machine-attributed commits obscures the thought process and craft behind each decision.

## Decision

slack-rewind adopts the workflow established in allymend:
1. Day-to-day development occurs on a long-lived `develop` branch.
2. Milestone pull requests merge `develop` into `main` using merge commits (no squashing or rebasing on PRs to preserve commit history and GPG/SSH signatures).
3. Changes follow a one-logical-step loop: make the change, run verification, inspect results, and hand over a concise commit subject line.
4. Commit subjects are plain, capitalized, imperative statements without type prefixes (e.g. `Add threat model and data flow documentation`), under 72 characters, with no body except `Signed-off-by`.
5. Zero AI metadata is permitted in repository files, commit messages, or pull requests.

## Consequences

- The git log is clean, consistent, and readable.
- Every commit on `develop` and `main` is signed and verifiable.
- Progress is trackable commit-by-commit against documented roadmap milestones.

