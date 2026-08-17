# Goals — Context

A goal is a **stated intention with no delivery mechanism yet** — something Jonah wants to be true, written down before it has become study, a project, or a routine.

**Status: partly specified.** Placement, discovery, state and boundaries are settled below — they were earned by two notes and by the console already depending on them. **The note's internal shape is deliberately not specified**, and no frontmatter schema exists: two goals is not enough use to justify a template, and the absence of fields here is a decision rather than a gap. See [domain-authoring.md](../../docs/agents/domain-authoring.md).

## Glossary

| Term | Means |
| --- | --- |
| **Goal** | A stated intention. Prose, no fields, no lifecycle |
| **Open thread** | A bullet under `## Open` — a question or an undecided matter. Struck through when it closes, with the answer written beside it |

## Where a goal lives

> **Placement follows the subject, not the word "goal".** A goal about health is a health record and lives in `health/`; this domain holds the ones whose subject has no domain of its own.

A body-composition goal sits in `health/`; a goal about a recreational sport sits here. That asymmetry is correct rather than untidy — it is [ADR-0004](../../docs/adr/0004-split-shared-objects-by-aspect.md)'s split-by-aspect applied to intentions. The first is subject to `health/`'s sensitivity handling and the second is subject to nothing, and that difference is exactly what placement is carrying.

**So this domain is a fallback location, and it will stay small on purpose.** If a subject earns a domain later, its goal moves there and this one keeps only the homeless.

### Being found matters, because placement is scattered

**A goal is discovered by being either in `goals/` or named `<subject>-goal.md`.** The [Workspace Console](../../tools/dashboard/README.md)'s Planning and Questions views glob exactly that, so the naming convention is load-bearing rather than cosmetic:

| Written as | Found? |
| --- | --- |
| `projects/goals/<subject>.md` | Yes — in the domain |
| `projects/<domain>/<subject>-goal.md` | Yes — the `*-goal` suffix |
| `projects/<domain>/goals.md` | **No.** Plural, no suffix match |
| `projects/<domain>/<intention>.md` | **No.** Names the subject and not the artifact |

**A goal that is not found does not announce itself** — it simply never appears in Planning, and nothing reports the absence. That is the whole reason this section exists.

## Structure

No template. Two notes is not enough use to justify one, and both got where they are by being written rather than filled in. What has repeated across both, and is worth keeping:

- **A bolded opening statement of the goal**, with who stated it and when. Both notes record where it was written down, too, and that provenance has already earned its place — it is what makes a figure attributable later, and it is the line that stops a number nobody can source becoming a fact.
- **`## Open`** — the open threads, as top-level bullets.
- **`Related:`** — links to goals that share a mechanism.

### The `## Open` convention, exactly

**A thread closes by being struck through, with its answer written beside it, in the same bullet.** Nothing is deleted, because the reasoning that produced the answer is most of the value.

```markdown
- ~~**"Better" is unspecified.**~~ **Answered by Jonah 2026-08-13**, and the
  answer changes the goal's shape more than its content.
```

Two consequences, both learned by the console getting them wrong:

- **A struck bullet is closed and must not be counted as open.** Reading it as open puts a settled question in front of the user with an answer box attached.
- **Bullets inside a `###` subsection of `## Open` are not open threads.** They argue that subsection's point. One note here has seven such bullets, all of them standing decisions rather than questions, and counting them reported eight open questions where the true number was zero.

## No state, deliberately

Per [domain-authoring.md](../../docs/agents/domain-authoring.md)'s direction test: **nothing here changes status.** A goal is stated and then it is true, abandoned, or superseded by a real mechanism — and none of those is a status a note should carry, because each of them is better expressed by what the goal turned into.

- **Achieved** is a fact for the subject's own record, not a field. The weight series is the evidence; a `status: done` beside it would be a second, weaker record of the same thing.
- **Abandoned** has no reader. An abandoned goal is a note nobody links to, and the graph already shows that.
- **Became real work** is a *move*, not a state — see the boundaries below.

**Do not add `status:`.** The expensive mistake domain-authoring names is inventing a state model for a domain that never needed one, and this is that domain.

## Boundaries

Both were argued out in a real goal note against real candidates, and both defaulted to *no*. The bar is high in each direction:

| It becomes | When |
| --- | --- |
| **A curriculum** in [`learning/`](../learning/CONTEXT.md) | It turns into actual study with units and assignments. *A named deficit and a good source are not use* — declined once already on exactly that ground, because nothing had been done yet |
| **An initiative** in [`initiatives/`](../initiatives/CONTEXT.md) | It needs coordination — money, gear, people, deadlines. Declined once already; the standing precedent is an initiative that met the criteria on paper and was closed anyway |
| **A standing assignment** in `learning/` | The work runs but never finishes, so it never becomes a unit — *nothing introduces it and nothing completes it*. A maintenance drill is the existing example |

> **The default in all three directions is no.** A goal that has produced no activity is a goal, and moving it early creates the structure before the work — the failure this workspace keeps catching.

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). It has no frontmatter schema of its own either, per the status line above.
- A goal placed in another domain is subject to **that domain's** handling rules, including sensitivity. A goal filed under `health/` is a health record first and a goal second, and inherits that domain's egress rules whole.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
