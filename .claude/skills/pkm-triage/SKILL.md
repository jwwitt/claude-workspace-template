---
name: pkm-triage
description: Clear the PKM inbox — propose a verdict per capture, write notes on approval.
disable-model-invocation: true
---

# PKM triage

Clear `projects/pkm/inbox/` to zero. Every capture leaves with one of four verdicts, and every write into `notes/` happens after the user approves it.

Read `projects/pkm/CONTEXT.md` first — it holds the note format (frontmatter, filenames, links) this skill writes to, and it is the single source of truth for it.

## Steps

1. **Read the inbox and `notes/INDEX.md`.** Reading the index first is what makes fold-in visible; propose without it and you will create near-duplicates you cannot see.
2. **Propose a verdict for every capture, in one batch.** State the verdict, the reasoning, and for a promote, the note type and the exact filename you'd write. Batch them — the user reads all of them at once and answers once.
3. **Wait.** The user's approval is the trust boundary that makes the graph worth having.
4. **Apply the approved verdicts**, then report what changed.

Done when the inbox holds zero files and every one is accounted for by an applied verdict.

## The four verdicts

| Verdict | Means | Applying it |
| --- | --- | --- |
| **Promote** | A new idea the graph doesn't hold | Write a source, atomic, or synthesis note per `CONTEXT.md`; add its `INDEX.md` line; delete the inbox file |
| **Fold in** | An existing note already covers this — sharpen it | Edit that note; update its `INDEX.md` line if its claim changed; delete the inbox file |
| **Route** | This is **work**, not knowledge — something to build or do | Append one line to the right backlog (below); delete the inbox file |
| **Discard** | Not worth keeping | Delete the inbox file |

**Reach for fold-in aggressively.** It is the verdict that decides whether the atomic layer stays evergreen or silts up with near-duplicates saying almost the same thing. When a capture is close to an existing atomic, folding in is the better outcome — a sharper existing note beats a second, weaker one.

Discard means delete. Git history is the audit trail, so nothing is truly lost, and an inbox that can't reach zero stops being read.

## Routing work

An idea to **build or do** something is not an evergreen note — forcing it into `notes/` produces an atomic nobody rereads and loses the fact that it was actionable. Route it instead, by what it's about:

| The idea is about | Goes to |
| --- | --- |
| This workspace — a skill, schema, convention, or fix | `.scratch/backlog.md` |
| The user's life — a project, business move, or pursuit | `projects/initiatives/backlog.md` |

The split follows the vault boundary: `.scratch/` is repo machinery, `projects/` is content the user browses in Obsidian.

Append one line, dated, in the file's existing format. Routing is a **handoff, not a plan** — capture the idea and its `why:`, and leave scoping to whoever picks it up.


## Applying a promote

- **Consult `INDEX.md` for the filename** — it must be unique across the whole notes tree, not just its stage folder.
- **Link the new note into the graph.** An atomic with no `[[wikilinks]]` is invisible: links are the retrieval mechanism, so connect it to what it relates to as you write it.
- **Update `INDEX.md` incrementally** — one line, title plus the note's single claim. You already know what you added; a full rebuild is expensive enough that it must stay a deliberate, on-demand act.
- **Record where it came from.** A source note carries `source:` and `sourceType:`; a note promoted from a conversation capture says so.

## Writing atomics

An atomic note holds **one** idea, stated so it still makes sense years from now with no memory of the capture it came from. If a proposed atomic needs "as discussed above" or names a context it doesn't contain, it is either a source note or two atomics.

Set `author:` honestly — `claude` when you drafted it, `co` when the user reshaped it in the approval round, `user` when the words are theirs.
