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

## Using it

Clone it, delete what you don't want, and start capturing. The two files worth reading first are `CLAUDE.md` (the root index and agent guardrails) and `CONTEXT-MAP.md` (which domain owns what).

The conventions are opinionated on purpose, and most of them are written down with their reasoning attached — if a rule looks arbitrary, the `CONTEXT.md` that states it usually says why.

## Provenance

Built by [Jonah Witt](https://github.com/jwwitt) with Claude Code, for his own use. Shared because the structure is reusable even though the contents aren't. No support promised.
