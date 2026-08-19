# Learning — Context

**Instructional structure**: the plan for acquiring a skill, plus the record of working it. Since [ADR-0005](../../docs/adr/0005-services-hold-the-record.md) those two halves live in different places, and knowing which is which is most of what this document is for.

## Where the two halves live

| Half | Lives in | Holds |
| --- | --- | --- |
| **Structure** | the **LMS** — a self-hosted Tutor LMS, written to by a publisher tool (private, named `tools/lms-publish/` in this workspace) | Curricula, units, assignments, the proficiency target, and per-assignment status |
| **Sessions** | this directory, [`logs/`](logs/) | What was actually worked, when, in prose |

**The LMS is the record for structure, not a copy of one.** There is no markdown behind it. `/curriculum` and `/start-unit` author into it directly; nothing here is generated from it and nothing there is generated from here.

**Logs stayed as files deliberately, and it is not an exception to ADR-0005.** That ADR says the service is the record *where a service holds the content* — and no service holds these. Tutor has no practice-log concept. A log is prose written after a session, and the thing that keeps one alive is that it is pleasant to write in; a web form is not that.

> **The dormancy signal is real and it is the console's whole reading of this domain now.** Dormancy is the age of a log's last entry, and the [Canvas decline](../initiatives/backlog.md) scored that as a strength over a stored percentage that goes stale silently.
>
> **It is working for one subject of three.** `guitar` carries two substantial entries (2026-08-15 and 08-16) and reads as current; the other two subjects hold only the format example `/curriculum` ships and correctly read as never started. **That asymmetry is the signal doing its job**, not a defect — a subject with a curriculum and no sessions is exactly what it exists to surface.
>
> **The fenced example does not count as an entry.** [`scan_learning`](../../tools/dashboard/scan.py) strips fenced blocks before counting dates, because a log that ships with a sample would otherwise report one session on the day it was created and never read as dormant again.

**Log entries link to things that are no longer vault notes.** `[[repertoire-maintenance]]`, `[[guitar-curriculum]]` and four others render as unresolved ghosts in Obsidian since 2026-08-18. **They are correct and should be left alone** — the targets exist, as lessons and courses in the LMS, and `[[ ]]` cannot address a URL. Rewriting them to links would hardcode a tailnet address into the vault and break the day it changes. A ghost here means *"in the LMS"*, not *"worth writing"*.

## Glossary

| Term | Means |
| --- | --- |
| **Subject** | The thing being learned. One **course** in the LMS |
| **Curriculum** | The whole arc for a subject — declares the proficiency, orders the units. The course itself |
| **Proficiency** | The curriculum-level target, written as **observable capability**, never as a level |
| **Unit** | One stage of the arc. A **topic** in the LMS |
| **Syllabus** | The topic's own body — objectives, resources, sequence |
| **Assignment** | One piece of work. A **lesson** in the LMS. Covers repeated drills and one-off deliverables alike |
| **Resource** | Anything external you learn from — book, video series, course, human teacher |
| **Session** | One bounded stretch of practice. Produces one entry in `logs/` |

Deliberately absent: **`course`** as a vault term — an external course is a *resource*, and the word now means the LMS object. Any drill/task split, as before: status covers both.

## What the vault still carries

- **`logs/<subject>-log.md`** — append-only, newest at the bottom, one entry per session. Prose and `[[wikilinks]]`, nothing structured.
- **`archive/`** — abandoned subjects. Empty; a retired *subject* is now a retired course, and what lands here is only a log with nowhere left to point.

**Imported vault frontmatter survives in the LMS as `_vault_*` post meta** — `type`, `created`, `provenance`, `status`, and the **source citation**. That last one is the least reconstructible field a curriculum has, and it existed nowhere else.

## Boundary

| Domain | Keeps | Test |
| --- | --- | --- |
| `pkm/` | Durable ideas produced while learning | Still true after you abandon the subject → PKM |
| `music-media/` | A title consumed and rated | A game being *practised* is a subject; the same game *played* is a catalogue row. [ADR-0004](../../docs/adr/0004-split-shared-objects-by-aspect.md)'s fifth case |
| `business/` | Records of commerce | Never holds a curriculum, however commercial the skill |
| `goals/` | Outcomes and targets | Optional, one-directional. **Skills never write there** |
| `health/` | Health records only | Habits are per-domain |
| `initiatives/` | Pursuits needing coordination beyond studying | Opt-in and rare. Default is **no** initiative note |

**This domain holds zero evergreen notes.** Durable output leaves via `/capture` → `pkm/inbox/` → normal triage.

## Sensitivity

A subject may be **health-grade** and still move to the LMS with the rest — authorized on the property that the destination is the user's alone: tailnet-only, their account, no public interface, and inside the same encrypted backup repository the vault reached. The governing rule lives in this workspace's private `memory/`. **Egress is still the whole test**, and the LMS is a second authorized channel rather than a general widening.

## Conventions

- **Filenames carry no order.** No `01-` prefixes. Ordering lives in the LMS's own `menu_order`.
- **Log filenames are `<subject>-log.md`** and unique vault-wide, as everything under `projects/` is.
- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- Notes here may freely wikilink into `pkm/notes/` — one graph.

## Frontmatter

Only logs have any, and it is minimal:

```yaml
type: log
created: YYYY-MM-DD
```

Everything the old schema carried — `provenance`, `source`, `status` — now lives on the LMS post as `_vault_*` meta, because that is where the object it describes lives.
