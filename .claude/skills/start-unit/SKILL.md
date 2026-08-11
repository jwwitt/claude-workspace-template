---
name: start-unit
description: Begin the next unit of a curriculum — write its syllabus, materialize its assignments, verify every resource, and report what landed.
disable-model-invocation: true
---

# Start unit

Activate the next unit of a subject's curriculum. Activating a unit **is** writing its syllabus — you never write one in the abstract.

Read `projects/learning/CONTEXT.md` first, then the subject's `<subject>-curriculum.md`.

## Steps

1. **Identify the next unit** from the curriculum's ordered list — the first with no folder. Folder existence *is* activation.
2. **Source its resources** from the curriculum's origin material. Selection and ordering only; see the substitution rule below.
3. **Verify every resource**, and mark every one.
4. **Write** the unit folder: `<unit-slug>/<unit-slug>.md` (the syllabus) plus one file per assignment.
5. **Announce** what landed and what couldn't be verified.

Done when the folder exists, every resource carries a mark, and the announcement names anything unverified.

**There is no approval gate here** — it's inherited from the curriculum. That is exactly why step 5 is not optional: **the announcement is the review.**

## Verifying

| Resource | Check |
| --- | --- |
| Book | Open Library `search.json` on **title+author** — `numFound: 0` falsifies. Publisher's product page is the tiebreaker and the strongest single check |
| Video | YouTube **oEmbed** — `400` on a fabricated ID; returns title + channel to compare. **404s on playlists**, so verify the playlist page or a named member video |
| Paper | Crossref |
| Course, syllabus PDF | Fetch the URL and read what came back |
| **Human teacher** | **None exists.** Never `verified` |

**Do not verify a book by checking its ISBN resolves** — the placeholder `9781234567897` resolves to a real book. **Do not depend on the Google Books API** — quota-blocked without a key. **An author mismatch is not proof of fabrication** — Open Library currently attributes Leavitt's Vol. 1 to Victor Hugo. Escalate to the publisher page instead of concluding.

### Verification is asymmetric — the rule that prevents a worse failure

> **A positive result proves existence. A negative result proves nothing.**

`justinguitar.com` 403s every automated request; `berkleepress.com` has returned 500 on a *real* page; PMI's old syllabus URL is dead while the current one lives behind a `?rev=` token.

**Never delete, "correct," or substitute a resource on a failed check.** Mark it unverified with the reason. Deleting good resources on a 403 is a worse failure than the one you're defending against, because it's invisible.

### Marking

Inline, next to each resource — never frontmatter, which is per-file while the mark is per-resource.

```markdown
- **A Modern Method for Guitar, Vol. 1** — William Leavitt, Berklee Press.
  ✅ verified 2026-08-11 · openlibrary.org/isbn/9780876390139
- **"CAGED system" video series** — <channel>.
  ⚠️ UNVERIFIED — playlist URL not machine-checkable (oEmbed does not cover playlists)
```

**Every resource carries a mark. An unmarked resource is a bug.**

## Announcing

Attention measurably collapses at the **second** identical exposure, and the same class of warning ranges from 10% to 70% ignored on design alone. So:

1. **Don't use a fixed shape every run.** Vary the form with the content — free, because the content genuinely differs.
2. **Verified resources as a count; unverified named individually.** Nine verified and one unverified in a single list hides the one.
3. **All verified → one line, then stop.** The common case must be cheap or the rare case can't be expensive.
4. **Give the specific reason and the specific next action.** Not "could not verify X" but "no Open Library match on title+author, publisher site returned 403 — confirm before buying."
5. **Name the file**, so review and repair are the same action.
6. **More than ~2–3 unverified is one finding, not N warnings** — "5 of 7 resources couldn't be verified; this unit is probably sourced from something unreliable."
7. **Say *inconclusive*, never *fabricated*, when the check was inconclusive.** Overclaiming destroys the announcement's credibility, and with no gate the announcement is the only protection left.

## Rules

- **Substitution is prohibited**, same as `/curriculum`. Swapping in an easier resource creates a new one that inherits no verification. Selection, ordering and pacing are safe; substitution isn't.
- **Never write into `pkm/notes/`.** That tree is human-gated. `wiki-ingest` bypasses the inbox only because an explicit ingest is Jonah's own act — this skill's writes are not.
- **Never flip an assignment's status from log prose.** Propose it; don't do it.
- **Never rename or renumber anything.** Filenames carry no order and are stable link targets.
- **Scan for basename collisions before writing**; disambiguate with the subject when one exists.
- **No empty scaffolding** — if the unit has one assignment, it doesn't need a syllabus that only points at it.
- Assignments start `status: planned`; set `active` only for what enters the rotation now.
