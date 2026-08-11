---
name: curriculum
description: Build a curriculum for a subject the user wants to learn — find real existing structure, propose the arc, write it on approval.
disable-model-invocation: true
---

# Curriculum

Create `projects/learning/<subject>/<subject>-curriculum.md`: a proficiency target and an ordered list of units. **Nothing else** — units materialize later via `/start-unit`.

Read `projects/learning/CONTEXT.md` first. It holds the glossary, layout, frontmatter, and the resource rules this skill writes to, and is the single source of truth for them.

## Steps

1. **Find, don't invent.** Dispatch a **background research agent** to locate existing curricula by tier (below). This is the expensive step and it happens once per subject.
2. **Propose** the proficiency and the ordered unit list, naming the source you're adapting and what you changed. Say which tier it came from.
3. **Wait.** This is a months-long plan; the user approves the arc before it lands.
4. **Write** `<subject>-curriculum.md` and report.

Done when the curriculum file exists, its unit list is `[[wikilinks]]`, and no unit folder has been created.

## Find before generate

**A graded-exam board is structurally the same thing as a certification body.** Search by tier, not by keyword:

| Tier | What | Examples |
| --- | --- | --- |
| **A** | The awarding/certifying body publishes the syllabus free | Trinity, RSL/Rockschool, PMI, CompTIA, AWS, ACM/IEEE |
| **B** | A university publishes a real course with readings | MIT OCW (richest), Open Yale |
| **C** | Community roadmap — **a route into A/B, never terminal authority** | OSSU, roadmap.sh |
| **D** | The established method book — a book *is* a curriculum | Leavitt, *A Modern Method for Guitar* |
| **E** | A free structured online course | JustinGuitar |

A source qualifies if it has a **named owner with a stake**, a **stability commitment**, a URL that **returns the document** (not a page about it), **states its own targets**, and **says what it doesn't cover**.

**Stop at the first tier that yields a qualifying source.** One Tier A source is sufficient — comparing it against three blog roadmaps adds noise, not confidence. Below Tier A, use at least two independent sources and build the arc from what they **agree** on. There is no evidence for a magic comparison count; don't invent one.

## Adaptation — the line you must not cross

> **Permitted adaptation is any operation whose output resources are a subset of the input resources.**

Select, drop, reorder, split, merge, re-pace, re-scope, rewrite objectives as observable capability — all safe, because none can produce a resource that doesn't exist.

**Substitution is prohibited.** "That book is too advanced, here's a gentler one" is the most natural move when adapting to a learner's level, and it converts a verified curriculum into an unverified one. A substituted resource is a **new** resource: it inherits nothing and re-enters verification from scratch.

The best defence against "real book, wrong level" is never having substituted the book — when resources come from a found curriculum, the level judgement was made by Trinity or Berklee, not by you.

## Rules

- **Delegating to a research agent is not verification.** Retrieval-grounded tools still fabricate at 17–33%. Web search does not discharge the duty.
- **Fabrication concentrates on obscure topics** — roughly 6% on common subjects against 28–29% on niche ones — which is exactly the long tail that makes a curriculum valuable. Be most careful where you're least sure.
- **Proficiency is observable capability, never a level.** "Can sight-read a chart and track a usable rhythm part in one take," not "intermediate." A level is unfalsifiable; a capability tells you when to stop.
- **Materialize nothing below the curriculum.** No unit folders, no syllabus, no assignments — a unit's files appear when `/start-unit` activates it, so that unit 5 is written knowing how units 1–4 went.
- **Scan the vault for basename collisions before writing.** Filenames are wikilink targets and must be unique vault-wide.
- **Never write to `goals/`**, and never write evergreen notes into `learning/` — durable ideas leave via `/capture`.
- **No initiative note by default.** One exists only if the pursuit needs coordination beyond studying — money, gear, people, deadlines, revenue.
