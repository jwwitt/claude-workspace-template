# Project Registry

External git repos that are **not** this workspace. Each stays fully independent — own git history, own remote. This is a pointer index, never a monorepo consolidation.

## What earns a row

A **routing table, not an inventory.** A repo earns a row only if a session in this workspace might need to be routed to it.

- Don't add repos you'd never open again. `gh repo list` produces the exhaustive list on demand — there's nothing to hand-maintain here.
- Don't accumulate archived rows. Delete the row when a project dies.
- Code repos only. Non-code context — this workspace itself, and anything else that isn't a git repo — is routed by `~/.claude/CLAUDE.md`, not from here — see [global-pointer-template.md](global-pointer-template.md) for that snippet.

`remote` is the required key — it's stable identity that survives machine changes and is directly actionable via `gh`. `localPath` is filled in only when a checkout actually exists.

## Registered projects

| Name | Remote | Local path | Purpose | Status | Tags |
| --- | --- | --- | --- | --- | --- |
| _(none yet)_ | | | | | |

## Registering a project

Two steps, both at repo creation:

1. Add its row above.
2. Paste the backlink into the new repo's own `CLAUDE.md` — copy-paste snippet and rationale in [backlink-template.md](backlink-template.md).
