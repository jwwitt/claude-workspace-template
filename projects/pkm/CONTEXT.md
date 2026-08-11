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
```

Excluded on purpose: `updated` (git knows), `status` (existing here *is* the status), `id`, `tags`.

This schema is **PKM-only** — other domains are a different artifact class and get their own.
