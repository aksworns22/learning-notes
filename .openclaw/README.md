# OpenClaw Config Snapshot

This directory contains non-sensitive OpenClaw runtime config references.

Workspace behavior documents live at the repository root:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `memory/*.md`

## Included

- `workspace-state.json` - basic workspace setup timestamps
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
