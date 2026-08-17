# Business — Context

Your business or freelance practice — the work you sell, the money it earns, and the admin around them.

**Status: specified.** Replace the line above with a one-line description of your own practice.

> **This domain was specified by real use, and the shape below is what that use produced: a solo freelance practice, one recurring client, one line being actively sold.** It ships as a worked example, not as a schema you have earned. **Delete anything you have no instances of** — that rule is the first thing in this file for a reason, and it applies to this file itself.

## Governing principle

> **Two logs, and nothing that has no instance yet.**

Everything a business eventually needs — client notes, engagement notes, a pipeline — was considered and rejected here because it would have sat empty against one client. Add structure when the second and third instances arrive, not in anticipation of them.

See [`docs/agents/domain-authoring.md`](../../docs/agents/domain-authoring.md): *a stub is not an unfinished domain.* The same holds one level up — a small schema is not an incomplete one.

## Glossary

| Term | Means |
| --- | --- |
| **Service line** | A kind of work that can be sold. Recorded whether or not it is currently being sold |
| **The wedge** | The one line actively being marketed |
| **Contact** | One outreach attempt to one person |
| **Active relationship** | A client the income log shows recent work for. **Derived, never stored** |

Add the units your own work is actually sold in — per project, per hour, per retainer — as they get resolved in real work. **Don't invent vocabulary upfront.**

Deliberately absent here: **`lead`**, **`pipeline`** and **`engagement`**. A short turnaround leaves no gap between quoting and delivering for anything to live in — see [State](#state). If your sales cycle is long, that reasoning does not apply to you and a pipeline may be exactly what you need.

## Boundary

| Domain | Keeps | Test |
| --- | --- | --- |
| `learning/` | Capability — curricula, practice, logs | **Never holds a curriculum here**, however commercial the skill |
| `finances/` | Personal money | This domain records business income only, at the point it is earned |
| `initiatives/` | Coordination of the effort itself | An initiative note tracks *the work of building this*; this domain holds the business's own records |
| `pkm/` | Durable ideas | Still true if the business closed → PKM |

## Layout

```text
business/
  CONTEXT.md
  <practice>-plan.md              ← the operating plan: rates, weekly action, checkpoints
  income-log.md                   ← append-only; every payment received
  outreach-log.md                 ← append-only; every contact sent
```

**The plan lives here rather than in `.scratch/`** — on purpose. `.scratch/` holds the arguments; the answer you consult on a Tuesday belongs in the domain. A plan reachable only from a private effort directory is the failure this workspace calls *the last hop*.

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md).
- **No empty scaffolding.** Never create a file for a thing with one instance.
- Durable content belongs here, not in `memory/`.
- Notes here may freely wikilink into `pkm/notes/` — one graph.

### Invoicing rules

**Jurisdiction-specific, and yours will differ — replace this section rather than adapting it.** The structural point is that tax and invoicing constraints are *conventions*, not records: they govern how work gets written down, so they belong in this file rather than in a folder of their own.

The kind of thing that belongs here: whether your jurisdiction taxes services, digital goods, or both; whether bundling a taxable item into an un-itemized price makes the whole invoice taxable; and whether to quote tax-inclusive or tax-exclusive. Settle these with the relevant authority — it is usually free — **before the first invoice**, not after.

## Frontmatter

```yaml
type: plan | log
created: YYYY-MM-DD
```

Excluded on purpose: `status:` ([why](#state)), `updated:` (git knows), `tags:` (this workspace uses links).

## State

**Nothing in this domain has any, and that is an answer rather than an omission.**

Applying the gate in [`domain-authoring.md`](../../docs/agents/domain-authoring.md): the gate asks whether anything changes status. With two logs and no entity notes there is nothing to carry a field — **a log entry is a fact, and facts have no lifecycle.**

The pipeline that would normally hold state does not exist here, because a short turnaround means **nothing lives between "quoted" and "delivered" long enough to need a home.** The contact goes in the outreach log, the money goes in the income log, and there is no middle. A pipeline models a long sales cycle. **If yours is long, re-run the gate — the answer may genuinely differ for you.**

**One thing looks like state and must not become a field.** A practice is scored on **active client relationships**, but activity is **derived from the income log's most recent row for that client** — as `learning/` derives dormancy from its log. A `status: active` field would be a second record of a fact the log already holds, and it would be the losing copy: the log updates as a side effect of getting paid, a field only when someone remembers.

**Check the gate's own trap.** Per `systems/`: the gate asks whether anything changes status, not whether *absence* can carry that change. Here it can — a client with no recent rows is dormant, the rows stay either way, and nothing must remain listed after it stops being current.

## Authorship — the rule this domain lives or dies by

> **The user writes both logs. Claude transcribes payments and contacts the user reports, and never infers one.**

These are **records of fact**, nearer [`health/`](../health/CONTEXT.md)'s never-fabricate rule than a capture. One invented row and the logs stop being evidence — which matters more here than almost anywhere, because tax figures, rate evidence and the plan's own diagnostics are computed from them.

**Never backfill from an estimate.** Historical income may be reconstructed from bank statements or tax forms; it must never be generated from a remembered range, because dated rows read as a record whatever produced them.

**Never infer a status change from prose.** Same asymmetry as `learning/`: propose, don't mutate.

## The logs

Both are **tables, not prose** — a deliberate divergence from [`learning/`](../learning/CONTEXT.md)'s log. That one is prose because it is read as narrative and has to be pleasant to write after a session. These are **summed**, for baselines, rate evidence and tax figures, and a log that has to be totalled is a table.

One file each until size hurts, then split by year.

### `income-log.md`

| Column | Notes |
| --- | --- |
| `date` | |
| `client` | Plain text. Client notes start at roughly five clients, not before |
| `service` | Your own service lines |
| `amount` | Gross, before any platform commission |
| `net` | After commission; blank when there is none |
| **`hours`** | Time actually worked |

**`hours` is why this file matters more than it looks.** Any plan built on a per-unit price rests on an assumed cost per unit, and that assumption is usually made before the work has been done once. **Record hours from the first job, so the log tests the assumption rather than merely reporting income.**

### `outreach-log.md`

| Column | Notes |
| --- | --- |
| `date` | |
| `who` | Person or listing |
| `channel` | e.g. `marketplace` · `direct` · `warm` · `referral` |
| `outcome` | **Blank by default.** Written only when something happens |

**The metric is contacts sent, not clients won**, because only the first is yours to control. A zero-client month with twenty contacts logged and one with three are completely different problems with completely different fixes, and a client count cannot tell them apart.

**Reply rate is derived, never stored:** non-blank outcomes ÷ rows older than three weeks. *No reply* is never written — it is the absence, after enough time has passed. That keeps the single mutable column to one deliberate act.
