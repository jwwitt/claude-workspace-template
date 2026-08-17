# Music & Media — Context

Music and media — listening, library, references, consumption.

**Status: partly specified.** The **media wiki** half has a schema, compiled 2026-08-13 by [the media-summarizer effort](../../.scratch/media-summarizer/spec.md) — ~~specified but not yet built~~ **built, and extended 2026-08-17 to 40 entities across 45 episodes of Hunter × Hunter (2011).** The **music** half is untouched and remains a stub: nothing in that effort addressed listening, and per [docs/agents/domain-authoring.md](../../docs/agents/domain-authoring.md) it stays unspecified until real use earns a shape.

## What lives here

| Artifact | Answers |
| --- | --- |
| [`media-library.md`](media-library.md) · [`book-inventory.md`](book-inventory.md) — the catalogue | *What exists, and do I care?* |
| **`<universe>/`** — one folder per universe, holding entity notes | *What is this, and what does it connect to?* |

> **The catalogue is thin, and this doc previously oversold it.** The effort that designed this domain called the library *"the thing built twice, unprompted"* and treated it as the half that already had content. On promotion it turned out to be **14 works and 63 book titles**, whose only state columns held one value each — `consumed: false` on every row, `status: unknown` on every row — so both were dropped. What arrived is a real list of titles and a set of Jonah's own ratings; it is **evidence of a want more than a working artifact**, and the wiki half is not the speculative one by comparison.

**A third artifact answers a third question and lives in another domain**, which is the most important thing on this page:

> **The chronology — what happened in a work, and how far through it you are — is a source note and lives in [`pkm/notes/source/`](../pkm/CONTEXT.md), not here.**

**A work is claimed by two domains and split by aspect, with neither owning it.** `pkm/` holds what the work *says*, in the order it says it; `music-media/` holds what the things in it *are*. They link to each other. See [ADR-0004](../../docs/adr/0004-split-shared-objects-by-aspect.md).

**Precedence, where the catalogue and the chronology touch one fact:** `consumed` in the catalogue answers *have I started this*; `progress` on the chronology answers *where am I*. **Where both exist, the chronology wins.** The catalogue links out to universe folders; nothing links back, because a catalogue that must be updated whenever a wiki grows is a second record of the same fact.

## The wiki — schema

**Organised by universe, not by work.** A character belongs to the continuity, not to the volume they first appeared in — and a long-running series may be three or four *works* sharing one continuous cast. The catalogue lists works; this half is grouped by universe.

**Entity notes:**

```yaml
---
type: entity-note
kind: character | place | group | thing
universe: <universe-slug>
created: 2026-08-13
---
```

Body: a description, then **appearances recorded as links to chronology sections — never restatements of them**, then an *appears alongside* list. Plot lives in exactly one place.

> **The description rule changed 2026-08-17.** This schema always said *"a short description accreted a line at a time"* while [the skill](../../.claude/skills/media-wiki/SKILL.md) said *"no description"* — **a contradiction that resolved in practice as no descriptions at all**, and neither document noticed for four days. Jonah overruled the skill after using the wiki. **Descriptions are now written from the chronology in this vault and from nothing else**, which bounds them to `progress` structurally rather than by instruction.
>
> **The two sections below the description are derived**, not hand-maintained — `.scratch/media-summarizer/rederive-entities.py` computes both from the chronology files. The accretion this schema assumed would happen by hand never happened once.

**Four kinds only.** Events and arcs are **not** entities: an event is what happened in a unit, which the chronology already holds, and an arc is a *span* of units — structure rather than a noun, represented as a grouping heading in the chronology.

**An entity earns a note the second time it appears**, never the first. The first appearance is backfilled from the existing chronology section rather than re-researched.

**Filenames carry the universe slug** — `<universe>-<entity>.md`, linked with an alias so the display name stays readable: `[[<universe>-<entity>|Entity Name]]`. **Non-negotiable**, and the reason is not tidiness: `projects/` is one vault-wide wikilink namespace, entity notes are the highest-collision content this vault will ever hold — two universes with a *Council*, a *Capital*, a character sharing a common first name — and a folder alone does not help, because Obsidian resolves bare names vault-wide and a collision would silently resolve to the wrong note.

## State

**None.** Entity notes have no lifecycle; a universe folder has no lifecycle. The one piece of moving state in the design — `progress` — sits on the chronology note in `pkm/`, placed there by the aspect split.

Worth recording, because it is the part that would be expensive to rediscover: **splitting the object by aspect split the state with it.** Asking whether a domain has state *before* knowing which aspects it owns produces the wrong answer. See [ADR-0004](../../docs/adr/0004-split-shared-objects-by-aspect.md).

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Entity notes use the schema above; the catalogue is a table.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph. The wiki depends on it.

## Glossary

| Term | Means |
| --- | --- |
| **Work** | One book, season, or film. The unit the catalogue lists and the chronology covers |
| **Universe** | The continuity a work belongs to. One universe may span many works |
| **Chronology** | The per-work record of what happened, in `pkm/notes/source/`. The spine the wiki hangs off |
| **Entity** | A character, place, group or thing. The nodes of the wiki |

## Not specified

- **Music.** Listening, library and references, all named in the scope line, all untouched. A stub until real use earns a shape.
- **Games.** Deliberately excluded — a game has no chronology unit, so the spine the wiki hangs off does not exist.
- **Books, in practice.** The schema covers them; the tooling will not, because per-chapter sources are blocked or absent and the failure mode is silent — a per-chapter query returns a whole-work summary that arrives looking like success. Existing hand-written chapter notes stay hand-written and are not a target for automation.
