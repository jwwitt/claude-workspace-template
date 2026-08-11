# Learning — Context

**Instructional structure**: the plan for acquiring a skill or body of knowledge, plus the record of working it. Full design in `.scratch/learning-domain/spec.md`.

## Governing principle

> **Placement is decided by artifact class, never by motive or subject.**

Why you're learning something must never move a file. Motive is unstable — hobbies become revenue lines — and unknowable when a file is created.

## Glossary

| Term | Means |
| --- | --- |
| **Subject** | The thing being learned. The unit a folder here is named for |
| **Curriculum** | The whole arc for a subject. Declares the proficiency, orders the units. One per subject |
| **Proficiency** | The curriculum-level target, written as **observable capability**, never as a level |
| **Syllabus** | The **document** for one unit — objectives, resources, sequence |
| **Objectives** | The syllabus-level targets. What one unit makes you able to do |
| **Assignment** | One piece of work, its own file. Covers repeated drills and one-off deliverables alike |
| **Resource** | Anything external you learn from — book, video series, online course, human teacher |
| **Session** | One bounded stretch of studying or practising. Produces one log entry |

Deliberately absent: **`course`** (an external course is a resource, or an imported syllabus — provenance records which) and any **drill/task** split (`status:` accommodates both).

## Boundary

| Domain | Keeps | Test |
| --- | --- | --- |
| `pkm/` | Durable ideas produced while learning | Still true after you abandon the subject → PKM |
| `business/` | Records of commerce | Never holds a curriculum, however commercial the skill |
| `goals/` | Outcomes and targets | Optional, one-directional. **Skills never write there** |
| `health/` | Health records only | Habits are per-domain; that tree's sensitivity marking stays undiluted |
| `initiatives/` | Pursuits needing coordination beyond studying — money, gear, people, deadlines | Opt-in and rare. Default is **no** initiative note |

**This domain holds zero evergreen notes.** Durable output leaves via `/capture` → `pkm/inbox/` → normal triage.

## Layout

```text
learning/
  archive/
    piano/                          ← abandoned subjects, moved here deliberately
  guitar/
    guitar-curriculum.md            ← landing page; ordered unit list, no state
    guitar-log.md                   ← append-only session history
    fretboard-fluency/              ← a unit; exists only because it was activated
      fretboard-fluency.md          ← the unit's syllabus document
      caged-shapes.md               ← assignments
```

## Conventions

- **Filenames carry no order.** No `01-` prefixes anywhere — the curriculum and syllabus already hold the ordering, and prefixes would encode it twice. Filenames are **stable identifiers**; a mid-curriculum insertion must never rename anything.
- **Filenames are unique vault-wide.** Name naturally; prepend the subject only where a collision exists. Scan before writing. This is what forces `<subject>-curriculum.md` and `<subject>-log.md`, and why a unit's syllabus is named after its unit rather than `syllabus.md`.
- **Assignments are files, not list items** — the workspace uses links, not tags, so anything worth referencing must be a file.
- **No empty scaffolding.** Instantiate only the levels that carry content. Never create a file whose only content points at one child; a single-unit subject goes curriculum → assignments.
- **No up-links.** The curriculum links down; Obsidian supplies the backlink.
- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- Notes here may freely wikilink into `pkm/notes/` — one graph.

## Frontmatter

```yaml
type: curriculum | syllabus | assignment
created: YYYY-MM-DD
provenance: generated | imported | co
source: <URL or citation>     # required when imported
status: planned | active | retired    # assignments
status: active | complete             # syllabus
```

Excluded on purpose: **`status:` on curricula** (see below), `updated:` (git knows), `tags:` (this workspace uses links).

`provenance:` rather than PKM's `author:` — an imported syllabus was written by a stranger that field can't name.

## State

Two records making **non-overlapping claims**. The log is immutable history; `status:` is current state with no memory. They cannot contradict each other.

**`done` is deliberately not a status value.** A drill never finishes, so any vocabulary containing `done` would leave every drill permanently mislabelled. `active` means "in my current rotation"; `retired` is honest for both a completed task and a dropped drill.

**A unit folder exists only because the unit was activated** — existence is the status, so a planned unit is just a line in the curriculum.

### Abandonment

- **Dormancy** is derived from the log's last entry date. No field; it cannot go stale.
- **Abandonment** is a **move to `learning/archive/<subject>/`**. Location carries the status. Jonah's act, never a skill's.

### Authorship — the rule this lives or dies by

> **Jonah writes the log by default. Claude transcribes sessions Jonah reports and never infers one. Status changes are always explicit.**

A session log is a **record of fact**, nearer `health/`'s never-fabricate rule than a capture. One invented line and the whole log stops being evidence.

Logging "finished the CAGED drills" must never flip an assignment to `retired`. That inference fails asymmetrically — it silently removes a drill from rotation, with no signal for weeks. **Propose; never mutate from prose.**

### Log entries

Date, prose, wikilinks. Nothing structured — the binding constraint is that it be pleasant to hand-write after a session. Duration and self-ratings were rejected: tedious, usually guessed, and a guessed number looks like data.

```markdown
## 2026-08-11
Forty minutes on [[caged-shapes]]. B-shape still collapses above the 7th fret.
```

One file per subject until size hurts, then split by year.

### "Where am I"

**Derived on demand, never stored.** Active unit = the folder whose syllabus says `active`; current work = its `active` assignments; recent history = the log's tail. **No skill maintains a status file** — a stale "where am I" is worse than none.

`<subject>-curriculum.md` is the landing page. Its unit list is `[[wikilinks]]`, and unmaterialized units have no file, so Obsidian renders the frontier for free.

## Resources

> **`verified` means: confirmed to exist, with matching title and author/creator, against a named source, on a named date.**

It claims **nothing** about fit, level, availability, edition, or quality.

**The mark is inline, never frontmatter** — it's per-resource and frontmatter is per-file, and Obsidian doesn't support nested properties.

```markdown
- **A Modern Method for Guitar, Vol. 1** — William Leavitt, Berklee Press.
  ✅ verified 2026-08-11 · openlibrary.org/isbn/9780876390139
- **"CAGED system" video series** — <channel>.
  ⚠️ UNVERIFIED — playlist URL not machine-checkable (oEmbed does not cover playlists)
```

**Every resource carries a mark. An unmarked resource is a bug** — if unmarked could mean "fine" or "unchecked," the mark stops carrying information within a month.

**Human teachers are never `verified`.** No check exists. Never name a teacher you found; record only teachers Jonah supplies.

Full sourcing and verification procedure: `.scratch/learning-domain/spec.md` §7.

## Finishing a resource

When Jonah **finishes** a resource, that's a `wiki-ingest` trigger — it writes the source note into `pkm/notes/source/` and gates the atomics, which is exactly the right handling.

**Never wire this into `/start-unit`.** Verification asks whether a thing exists; `wiki-ingest` reads what it says. And `/start-unit` must never write into `pkm/notes/` — that tree is human-gated, and `wiki-ingest` bypasses the inbox only because an explicit ingest is Jonah's explicit act.
