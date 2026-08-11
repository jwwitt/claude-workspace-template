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

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its notes are work, not evergreen knowledge.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
