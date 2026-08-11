# Claude Workspace

Jonah's personal workspace: a knowledge pipeline, life-management domains, and an index of his other code repos. Claude Code and Obsidian both operate on these files.

**Read only what your task needs.** This file is an index, not a briefing — don't preload domains you aren't working in.

## Where things live

| Path | What it is |
| --- | --- |
| [CONTEXT-MAP.md](CONTEXT-MAP.md) | Points at one `CONTEXT.md` per domain — **start here** to find the right one |
| [projects/](projects/) | All durable content. Also the Obsidian vault root |
| [projects/pkm/](projects/pkm/) | The knowledge pipeline — see [its CONTEXT.md](projects/pkm/CONTEXT.md) |
| [registry/projects.md](registry/projects.md) | External code repos, by pointer. A routing table, not an inventory |
| [memory/](memory/) | How Claude should behave — **never** content |
| [docs/adr/](docs/adr/) | System-wide architecture decisions |
| [.scratch/](.scratch/) | Local issue tracker |

## Memory vs. content

A hard boundary, and the main defense against context bloat:

- **`memory/`** holds how Claude should behave and collaborate — preferences, working agreements, feedback.
- **`projects/`** holds everything durable — knowledge, domain data, plans.

If a fact would still be true if Claude didn't exist, it belongs in `projects/`, not `memory/`.

## Capturing knowledge

Capture is cheap; promotion is gated. You may drop a capture into `projects/pkm/inbox/` proactively when something durable-worthy surfaces — but **say so in your response**. Nothing lands silently.

Never write into `projects/pkm/notes/` without Jonah's approval. That approval is the trust boundary that makes the graph worth having. Full rules: [projects/pkm/CONTEXT.md](projects/pkm/CONTEXT.md).

## Subagents and usage limits

- Don't spawn a subagent for anything answerable directly in a few tool calls — delegation has overhead. Reserve it for genuinely large, independent work.
- Prefer **background** agents for research-shaped or long-running work, so this session isn't blocked and its context isn't consumed by intermediate output.
- Cap deliberate concurrent spawns at roughly **2–4 per turn**. Dispatch sequentially when tasks aren't independent of each other's findings.
- Default to the **standard model tier**. Drop lower only for trivial, well-defined work (lookups, formatting, simple fact-finding); escalate only for unusually hard tasks.
- Route open-ended research to the `research` skill, not ad hoc general-purpose agents — it keeps findings in a durable file instead of transient context.
- Never spawn an agent to duplicate work already delegated in the same turn.

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Multi-context — root `CONTEXT-MAP.md` + a `CONTEXT.md` per domain under `projects/<domain>/`, plus system-wide `docs/adr/` at the root. See `docs/agents/domain.md`.

## Architecture

The workspace's own design is specced at [.scratch/claude-workspace-architecture/spec.md](.scratch/claude-workspace-architecture/spec.md) (approved 2026-08-10). Its [map](.scratch/claude-workspace-architecture/map.md) is complete — all 10 tickets resolved.

Built: the directory tree, context docs, empty registry, the three PKM skills, Obsidian at `projects/.obsidian/`, this file, and the global `~/.claude/CLAUDE.md` repoint — so sessions started anywhere on the machine now route here for personal context. The per-repo backlink template is at [registry/backlink-template.md](registry/backlink-template.md), applied at the next repo creation. **The architecture build is complete** — what's left is content, and per-domain schemas when a domain earns one.
