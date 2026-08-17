# PKM — Context

The knowledge pipeline: a 3-stage Zettelkasten. This document is the operating spec; the reasoning behind it lives with the architecture effort under `.scratch/` — **which is not published in the template**, so if that directory holds only `backlog.md`, nothing is missing.

## Governing principle

> **Capture is cheap and agent-driven. Promotion into `notes/` is human-gated.**

The user's approval at promotion *is* the trust boundary — a note existing in `notes/` means they accepted it.

## Glossary

| Term | Means |
| --- | --- |
| **Capture** | Raw, unprocessed material dropped in `inbox/`. Any conforming markdown file counts, including hand-written ones — see the inbox format below. |
| **Source note** | A literature note — one per external source, in `notes/source/`. What the source says. |
| **Atomic note** | One idea, evergreen, densely linked, in `notes/atomic/`. The durable core. |
| **Synthesis note** | Combined insight across atomics, in `notes/synthesis/`. |
| **Output** | An artifact **written to leave the building** — video script, post, newsletter, client-facing material. Lives in `outputs/`. Internal work products belong to their own domain, not here. **Its format is unspecified** — no skill writes there, and no schema has been earned yet; the first real output defines the shape. |
| **Promotion** | Moving a capture into `notes/` via `/pkm-triage`. Requires approval. |
| **Fold-in** | A triage verdict: sharpen an existing atomic rather than create a near-duplicate. |

## Flow

```text
                    ┌──▶ notes/source/ ──▶ notes/atomic/ ──▶ notes/synthesis/ ──▶ outputs/
                    │         ▲
inbox/ ──/pkm-triage┤         └─ wiki-ingest (writes source notes directly, bypassing inbox)
                    │
                    └──▶ .scratch/backlog.md  ·  projects/initiatives/backlog.md
                              (route — the idea is work to do, not knowledge to keep)
```

- The **inbox is transient**. On promotion the inbox file is deleted; git history is the audit trail. No archive folder — an inbox that can't be cleared to zero stops being read.
- `/pkm-triage` has four verdicts: promote · fold into an existing note · route to a backlog · discard.
- `wiki-ingest` bypasses the inbox because an explicit ingest of a known source already *is* a literature note. Atomics it proposes still need approval.

## Conventions

- **Filenames**: descriptive kebab-case (`spaced-repetition.md`), unique **across the whole vault**, not just the notes tree. `projects/` is the vault root, so a PKM note and a learning assignment share one wikilink namespace — and `INDEX.md` lists only PKM notes, so it cannot detect a collision outside them. Scan the vault, not just the index.
- **Links**: `[[wikilinks]]`. Obsidian resolves them — `projects/` is the vault root.
- **No tags.** Links are the retrieval mechanism. To group, write a synthesis or map-of-content note; to associate with a domain, wikilink to that domain's note.
- **`INDEX.md`** is agent-facing: one line per note, title + its single claim. `/pkm-triage` updates it incrementally on each promotion. The user browses via Obsidian instead.

### Inbox format — what "conforming" means

A capture is `inbox/YYYY-MM-DD-<kebab-slug>.md` with three fields. Written here, not only in `/capture`, because hand-written captures are explicitly allowed and nobody opens a `SKILL.md` to write one by hand:

```yaml
---
captured: YYYY-MM-DD
source: <URL, "conversation", or where it came from>
why: <one line — what made this worth keeping>
---
```

`why:` is the field that earns its keep. A capture with no stated reason gets discarded at triage, because by then nobody can reconstruct what was interesting about it.

### Frontmatter

```yaml
# all notes
type: source-note | atomic-note | synthesis-note
created: 2026-08-10
author: claude | user | co

# source notes additionally
source: <URL or citation>
sourceType: article | video | book | paper | conversation

# source notes for works consumed over time
progress: <a position — "chapter 12", "s4e12", "finished", "not started">

# any note imported rather than written here
provenance: <where it came from, and when>
```

Excluded on purpose: `updated` (git knows), `id`, `tags`.

**`status` is excluded too, but the reason is narrower than it used to say here.** This section previously read *"`status` — existing here **is** the status,"* which is true of **promotion** and false of **consumption**. A note existing in `notes/` does mean it was promoted; it says nothing about how far through the work Jonah has got. Those are two different lifecycles and only the first is carried by location.

**`progress` holds a position, not a status**, and it exists because the alternative was falsified in this corpus: [`the-way-of-kings.md`](notes/source/the-way-of-kings.md) has sections at Prelude, Prologue, 1, 3–8, 10–12, and **chapters 2 and 9 were certainly read.** Absence records what was *noted*, not what was *consumed*, so the two can never be derived from one another. It is authoritative over the sections; the sections are a record of note-taking.

**Only source notes for works consumed over time carry it.** An article has no position. Reasoning: [media-summarizer 05](../../.scratch/media-summarizer/issues/05-the-spoiler-horizon.md).

**Never store a reading *lane* beside it.** The console's Media panel shows queued / in-progress / completed, and those are **derived from the position**, not recorded. A stored lane and a stored position are two records of one fact, and the field this replaced is the proof: `readingStatus: queued` sat on a note holding twelve chapters of reading.

**Vocabulary.** Anything that names a position is valid — `chapter 12`, `s4e12`, `part two`. Two reserved values sit at the ends: **`not started`** and **`finished`**.

> **`in progress` is a degraded value and is not a target to write.** Six notes carry it, inherited from the 2026-08-12 migration's `readingStatus: in-progress`, and it is kept only because inventing a chapter number Jonah never gave would be worse. **Replace it with a real position the next time that book is picked up.** It is honest about being imprecise, which is the most that can be said for it.

**`progress` replaced `readingStatus` across all 16 source notes on 2026-08-13**, and `provenance` was documented at the same time. Both were already in the corpus, added by the migration and never recorded here — so this section began as a repair rather than an extension.

This schema is **PKM-only** — other domains are a different artifact class and get their own.
