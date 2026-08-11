# Claude Workspace — structure

The scaffolding of a personal [Claude Code](https://claude.com/claude-code) workspace: a knowledge pipeline and a set of life-management domains, with all of the actual content removed.

This is the **structure only**. Every note, journal entry, goal, plan and log lives in a separate private repo. What's here is the part that would be equally true in anyone else's workspace — the conventions, the skills, the context docs, and the empty shape they operate on.

## What's in it

- **A 3-stage Zettelkasten** — `projects/pkm/`, running `inbox/` → `notes/{source,atomic,synthesis}/` → `outputs/`, with capture cheap and promotion human-gated.
- **Skills** — `/capture`, `/pkm-triage`, `wiki-ingest` for the knowledge pipeline; `/curriculum` and `/start-unit` for building and working through a learning plan.
- **Domain context docs** — one `CONTEXT.md` per domain, routed from `CONTEXT-MAP.md`, so a session loads only the context its task needs.
- **Agent conventions** — a local markdown issue tracker, triage labels, and how the engineering skills should read domain docs.
- **An Obsidian vault config**, rooted at `projects/`, so the same files are navigable by hand.

`projects/learning/CONTEXT.md` is the most fully worked-out domain and the best single file to read if you want to see how one is meant to be specified.

## What's deliberately absent

Notes, journals, health records, finances, business specifics, the project registry's rows, and the design efforts under `.scratch/`. The directory structure they live in is here; the contents are not.

## Setup

Four steps, none of them long. Only the first is required.

1. **Run Claude Code with this directory as the working directory.** Every skill uses repo-relative paths (`projects/pkm/inbox/`, `projects/learning/`), so they only resolve from the repo root. Nothing else works until this is true.

2. **Point Obsidian at `projects/`** as the vault root, if you want the files navigable by hand. The `.obsidian/` config ships with the repo, so the vault opens configured. Everything outside `projects/` — `docs/`, `registry/`, `.scratch/`, `CLAUDE.md` — deliberately sits outside the vault; it's machinery, not content.

3. **Optional — global routing.** Adding a pointer to this workspace in your own `~/.claude/CLAUDE.md` lets sessions started in *other* directories find it. Without it everything still works; you just have to start sessions here. `registry/backlink-template.md` covers the reverse direction — a pointer *from* another repo back to this one.

4. **Optional — external skills.** `docs/agents/` describes conventions for a local markdown issue tracker and triage labels that some third-party skill packs expect. Nothing in this repo requires them: the five skills in `.claude/skills/` are self-contained and have no external dependencies.

## Using it

Read `CLAUDE.md` (the root index and agent guardrails) and `CONTEXT-MAP.md` (which domain owns what), then start capturing. Delete the domains you don't want — they're independent.

The conventions are opinionated on purpose, and most are written down with their reasoning attached — if a rule looks arbitrary, the `CONTEXT.md` that states it usually says why. `projects/learning/CONTEXT.md` and `projects/pkm/CONTEXT.md` are the two fully worked-out ones; the other six domains are deliberate stubs waiting for real use to give them a shape.

Where a document defers to "the reasoning behind it," that reasoning lived in design efforts under `.scratch/` which aren't published — the decisions themselves are all here, only the arguments that produced them are missing.

## Provenance

Built by [Jonah Witt](https://github.com/jwwitt) with Claude Code, for his own use. Shared because the structure is reusable even though the contents aren't. No support promised.
