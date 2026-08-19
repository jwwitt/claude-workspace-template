# Initiatives — Context

Life-style and big-picture project tracking. Named `initiatives/` rather than `projects/` to avoid colliding with the top-level `projects/` folder that contains it.

**Status: partially specified.** The backlog shape below was defined when `/pkm-triage` gained its route verdict and needed somewhere to send life-shaped ideas. What an *active* initiative note contains beyond its frontmatter is still open — leave it to real use rather than inventing it now.

## Glossary

| Term | Means |
| --- | --- |
| **Idea** | An unscoped line in [backlog.md](backlog.md). Costs nothing, commits to nothing |
| **Initiative** | An idea you've actually picked up. Gets its own note, `<slug>.md` |

## Flow

```text
backlog.md ──(you pick it up)──▶ <slug>.md
     ▲
  /pkm-triage route verdict
```

An idea earns a note when you start on it, not when you like it. A backlog of one-liners stays scannable; a backlog of stubs does not.

## Initiative notes

`projects/initiatives/<slug>.md`, kebab-case, with:

```yaml
---
type: initiative
status: active | paused | done
started: YYYY-MM-DD
---
```

Beyond that, write what the initiative actually needs. Link it from `backlog.md`'s Active section, and `[[wikilink]]` it to the notes and domains it touches.

### `## Next actions` — **retired 2026-08-18. Tasks live in Vikunja.**

> **The convention below is history.** Actionable tasks moved to
> a self-hosted Vikunja instance on 2026-08-18: 31 open items into five
> projects, 26 completed ones carried across as done, and the sections stripped
> from seven files in the same change that rewired every reader.
>
> **Initiative notes no longer carry a task list.** They carry what they always
> carried and what a task manager is bad at — the reasoning, the constraints,
> the argument for doing this rather than that. The task-triage flow's
> **Attach** verdict now writes a Vikunja task instead of a `- [ ]` line, and
> the approval gate is unchanged: Claude proposes, the user approves.
>
> **Two places still hold checkboxes and both are deliberate.** The example
> below, because a retired convention still has to be legible to whoever finds
> a stray checkbox; and one dated prep artifact for an event that already
> happened — its boxes record what was prepared rather than work outstanding,
> and a retirement does not oblige rewriting history that used the convention.
>
> **What the retirement cost, stated because [ADR-0005](../../docs/adr/0005-services-hold-the-record.md) says to state it:** the console's task
> counts go dark, because it reads files and there are no longer files to read.
> Obsidian no longer renders the state where the note is read. Both were known
> and accepted, and neither is a bug to be fixed by reaching over HTTP.

The shape it had, kept for readers of older commits:

Added 2026-08-17, and **this is the "leave it to real use" clause above being exercised rather than overridden**: the shape was not invented in advance, it was earned when Jonah asked for captured tasks to sit under their parent initiative and there was nowhere for them to go.

```markdown
## Next actions

- [ ] Buy the powered USB hub and re-run the dd reproducer
- [x] Order the Thunderbolt adapter
```

**Checkboxes, and this is the only place in the workspace that uses them.** Everywhere else a thing is closed by striking its lead clause — a convention that carries reasoning well, and which the console needed a dedicated check for because a verdict written mid-body still reads as open. **A task has no reasoning to carry and no lead clause to strike.** It is done or it is not. `- [x]` cannot be written ambiguously, cannot be buried four paragraphs down, and renders as a real checkbox in Obsidian, so the state is visible in the app the note is actually read in.

**The section is earned, not scaffolded.** Absent is the normal case and parses as zero actions; add the heading when there is a first action to put under it. An initiative note carrying an empty `## Next actions` is [[scaffolding-substitutes-for-the-work-it-holds]] in the file that documents the work.

**Open items projected into Apple Reminders**, into the list belonging to that initiative — that is the whole reason the shape is fixed rather than free. Ticked items were never emitted, because re-emitting one resurrects finished work. Writing here was gated: a triage skill proposed and the user approved, the same boundary `/pkm-triage` holds over `notes/`.

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its notes are work, not evergreen knowledge.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
