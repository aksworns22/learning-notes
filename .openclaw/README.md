# OpenClaw Workspace Snapshot

This directory contains a non-sensitive snapshot of the OpenClaw setup used with this learning log repository.

## Included

- `workspace-state.json` - basic workspace setup timestamps
- `workspace/*.md` - agent/workspace behavior notes
- `openclaw.example.json` - redacted OpenClaw config shape

## Excluded

The following local OpenClaw files are intentionally not committed:

- `credentials/`
- `state/*.sqlite*`
- `memory/*.sqlite*`
- `logs/`
- `identity/device.json`
- real API tokens, Slack tokens, auth profiles, and owner identifiers

Use `openclaw.example.json` as a reference only. Do not put live secrets in this repository.
