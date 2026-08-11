# Claude Workspace

A personal workspace: a knowledge pipeline, life-management domains, and an index of external code repos. Claude Code and Obsidian both operate on these files.

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

**Read `memory/` at the start of a session** if it holds anything — one file per preference, kebab-case. It is small by design; if it grows past a quick read, that is a signal something in it belongs in `projects/`.

## Capturing knowledge

Capture is cheap; promotion is gated. You may drop a capture into `projects/pkm/inbox/` proactively when something durable-worthy surfaces — but **say so in your response**. Nothing lands silently.

Never write into `projects/pkm/notes/` without the user's approval. That approval is the trust boundary that makes the graph worth having. Full rules: [projects/pkm/CONTEXT.md](projects/pkm/CONTEXT.md).

## Subagents and usage limits

- Don't spawn a subagent for anything answerable directly in a few tool calls — delegation has overhead. Reserve it for genuinely large, independent work.
- Prefer **background** agents for research-shaped or long-running work, so this session isn't blocked and its context isn't consumed by intermediate output.
- Cap deliberate concurrent spawns at roughly **2–4 per turn**. Dispatch sequentially when tasks aren't independent of each other's findings.
- Default to the **standard model tier**. Drop lower only for trivial, well-defined work (lookups, formatting, simple fact-finding); escalate only for unusually hard tasks.
- Route open-ended research to a dedicated research skill where one is installed, or otherwise to a background agent briefed to write findings to a file under `.scratch/<effort>/research/` — not to ad hoc general-purpose agents. The point is that findings land somewhere durable instead of in transient context.
- Never spawn an agent to duplicate work already delegated in the same turn.

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Multi-context — root `CONTEXT-MAP.md` + a `CONTEXT.md` per domain under `projects/<domain>/`, plus system-wide `docs/adr/` at the root. See `docs/agents/domain.md`.

## Architecture

The design and its reasoning live in `.scratch/` as wayfinder efforts — one directory per effort, each with a map, numbered tickets, and a compiled spec. That is where to look for *why* a convention is the way it is; this file and the `CONTEXT.md` docs record only what it is.

Two pieces of setup live outside this repo and are **per-machine**, so a fresh checkout does not have them:

- **Global routing** — pointing `~/.claude/CLAUDE.md` at this workspace, so sessions started anywhere on the machine can find personal context.
- **Per-repo backlinks** — [registry/backlink-template.md](registry/backlink-template.md), pasted into a new project repo's own `CLAUDE.md` at creation time, alongside its row in [registry/projects.md](registry/projects.md).

The architecture itself is complete. What grows from here is content, and per-domain schemas as each domain earns one.
