# Claude Workspace — structure

The scaffolding of a personal [Claude Code](https://claude.com/claude-code) workspace: a knowledge pipeline and a set of life-management domains, with all of the actual content removed.

This is the **structure only**. Every note, journal entry, goal, plan and log lives in a separate private repo. What's here is the part that would be equally true in anyone else's workspace — the conventions, the skills, the context docs, and the empty shape they operate on.

> ## ⚠️ Make your copy private before you put anything in it
>
> This repo is public because it's empty. **Yours won't be.** The moment you start capturing, this tree holds notes, journals, and whatever `projects/health/` and `projects/finances/` are named for — and those domains' own docs tell agents to treat their contents as sensitive.
>
> **Use "Use this template" and choose Private**, or clone and repoint the remote at a private repo of your own. Do **not** fork: a fork of a public repo is public, and GitHub will happily let you push your journal into it.
>
> Nothing here excludes content from git — deliberately, since you almost certainly *do* want your notes version-controlled. Just not here.

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

Five steps. The first two are required; skipping the first is the one mistake with consequences you can't take back.

1. **Make your copy private.** "Use this template" → Private, or clone and repoint `origin` at your own private repo:

   ```bash
   git remote set-url origin git@github.com:<you>/<your-private-repo>.git
   git remote -v          # confirm before you commit anything
   ```

   Or drop the remote entirely and stay local: `git remote remove origin`.

2. **Run Claude Code with this directory as the working directory.** Every skill uses repo-relative paths (`projects/pkm/inbox/`, `projects/learning/`), so they only resolve from the repo root. Nothing works until this is true.

3. **Point Obsidian at `projects/`** as the vault root, if you want the files navigable by hand. The `.obsidian/` config is tracked, so plugins come pre-enabled — but nothing is *configured*: no daily-notes folder, no template folder, and Obsidian Sync is switched on and is a paid service you may want off. Everything outside `projects/` — `docs/`, `registry/`, `.scratch/`, `CLAUDE.md` — deliberately sits outside the vault; it's machinery, not content.

4. **Optional — global routing.** Adding a pointer to this workspace in your own `~/.claude/CLAUDE.md` lets sessions started in *other* directories find it. Without it everything still works; you just have to start sessions here. `registry/backlink-template.md` covers the reverse direction — a pointer *from* another repo back to this one.

5. **Optional — external skills.** `docs/agents/` describes conventions for a local markdown issue tracker and triage labels that some third-party skill packs expect. Nothing in this repo requires them: the five skills in `.claude/skills/` are self-contained and have no external dependencies.

## Using it

Read `CLAUDE.md` (the root index and agent guardrails) and `CONTEXT-MAP.md` (which domain owns what), then start capturing — **once step 1 is done.** Delete the domains you don't want; they're independent.

The conventions are opinionated on purpose, and most are written down with their reasoning attached — if a rule looks arbitrary, the `CONTEXT.md` that states it usually says why. `projects/learning/CONTEXT.md` and `projects/pkm/CONTEXT.md` are the two fully worked-out ones; the other six domains are deliberate stubs waiting for real use to give them a shape.

Where a document defers to "the reasoning behind it," that reasoning lived in design efforts under `.scratch/` which aren't published — the decisions themselves are all here, only the arguments that produced them are missing.

## Provenance

Built by [Jonah Witt](https://github.com/jwwitt) with Claude Code, for personal use. Shared because the structure is reusable even though the contents aren't. No support promised.
