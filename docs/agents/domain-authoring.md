# Adding a domain

How to write a domain's `CONTEXT.md`. For how skills should *consume* domain docs once they exist, see [domain.md](domain.md).

A domain is a top-level directory under the context root (`projects/` here) with its own `CONTEXT.md`, listed in `CONTEXT-MAP.md`. Adding one is mostly copying an existing stub. This document covers the parts that aren't obvious.

## What every domain doc carries

The invariant core. All of it fits on a page:

| Part | What it does |
| --- | --- |
| **Title and a one-line scope** | What belongs here, in a sentence. The line that stops the next domain from overlapping this one |
| **Status line** | Whether the schema is specified yet. A stub says so plainly rather than pretending |
| **Glossary** | Terms as they get resolved in real work. Empty is a valid and common state — **don't invent vocabulary upfront** |
| **Conventions** | Vault membership, link style, what schema it does and doesn't inherit, where durable content goes |

## What varies, and is supposed to

Copying a neighbouring stub is the normal way to make a new one, so it's worth knowing which differences between existing domains are deliberate:

- **Sensitivity handling.** `health/`, `finances/` and `journaling/` carry a storage-policy paragraph the other stubs don't. That is deliberate — a domain holding records that could harm someone if disclosed states where its files may live, because "treat as sensitive" with no egress rule is decoration.
- **Boundary rules.** A domain that is easily confused with another says so explicitly. `health/` disclaims habit tracking; `learning/` disclaims commerce. Most domains need nothing.
- **Depth.** Most domains are stubs. Two are fully specified. **A stub is not an unfinished domain** — it routes correctly and holds nothing, and it stays that way until real use earns a shape. Filling one in speculatively is the failure mode, not the goal.

## State

**Most domains have no lifecycle state.** A place where notes live doesn't need any of this. If nothing in your domain changes status over time — if a file is just filed somewhere and stays there — you are done. Skip the rest of this section.

Six of this workspace's nine domains are in exactly that position.

### The test

If your domain does have things that change status, one question decides the mechanism:

> **Does the state ever move backward?**

| | Mechanism | Why |
| --- | --- | --- |
| **One-way** — a thing advances and never returns | **Location.** The folder *is* the state | A move is a real event and the filesystem records it. Nothing can be in two stages at once, and there's no field to go stale |
| **Reversible or recurring** — active, paused, active again; stops without finishing | **A field** in frontmatter | Expressing this by location means moving files on every change, and every move breaks the `[[wikilinks]]` pointing at them |

**This is a classification, not a fallback chain.** Don't try location and retreat to a field when it gets awkward — that's how you end up moving files on every status change. Answer the direction question first; the mechanism follows from it.

**One qualifier.** `learning/archive/` uses location for abandonment even though abandonment is reversible in principle. That works because abandonment is **rare and deliberate enough that the move is itself the meaningful act** — and in exchange, abandoned subjects drop out of every query automatically instead of every reader having to remember to filter them. So: location for one-way transitions, and for reversible ones rare enough that moving is the point.

### How the two existing examples land

**`pkm/` has an obvious lifecycle and no `status:` field anywhere.** That's correct, not an oversight. Promotion is one-way — a capture becomes a note and never returns to the inbox — so the folder carries the stage. And once an atomic lands it has no lifecycle at all: fold-in sharpens it in place rather than re-staging it. If you're tempted to add a status field, check first whether you're actually in this situation.

**`learning/` uses both mechanisms, and isn't inconsistent for doing so.** Unit activation is one-way — you can't un-start a unit — so a unit folder existing *is* its activation. Assignment rotation is reversible, since a drill leaves and returns, so assignments carry `status: planned | active | retired`. One domain, two mechanisms, each matching its direction of travel.

**`systems/` is the case where "no state at all" looked right and wasn't.** A device is acquired, used, retired — and the obvious move is to skip the state model entirely, because an unlisted device is a retired one. That reasoning fails on one case: a retired drive in a drawer may still hold the only copy of something, which is the most valuable fact the domain records. Retired devices therefore have to stay listed, so absence cannot encode retirement, so the state needs somewhere to live. Retirement is reversible — hardware gets pressed back into service — so it is a **field**, `status: active | retired`.

Worth noticing what nearly went wrong there. The gate below is designed to send most domains away, and this domain would have walked through it for a plausible reason. **The gate asks whether anything changes status; it does not ask whether absence can carry that change.** When you are tempted to skip the state model, check what else the record has to hold — if a thing must stay listed after it stops being current, absence is not available to you.

### If you have state, four more things hold

- **Two mechanisms are only safe together if neither can answer the other's question.** An append-only log plus a status field is fine: the log is immutable history, the status is current state with no memory, and neither can contradict the other. Checkboxes plus a log is not fine — both try to encode completion, and they will disagree.
- **Say which question each mechanism answers.** In `learning/`, curriculum ordering answers *how far have I got* and `status:` answers *what is still in my rotation*. Asking one of them the other's question is what makes derived state go quietly wrong.
- **Derive on demand; never store a "where am I".** A maintained status file is a cache, and a stale cache is confidently wrong about the one thing it exists to answer. Reading three files per query is cheap at this scale.
- **Never infer a status change from prose.** "Finished the CAGED drills" in a log must not flip an assignment to `retired`. That inference fails asymmetrically — it silently removes something from rotation with no signal for weeks. Propose the change; don't make it.

### How much to trust this

Originally two domains, one author, written within a fortnight — so some of the agreement may be house style rather than a finding. What makes the direction test worth stating anyway is that it explains cases it wasn't derived from: `pkm/` having no status field, `learning/` needing two mechanisms, and `archive/` looking like an exception when it isn't.

**Re-checked against a third domain.** `systems/` was designed after this document and tested against it rather than the reverse. The direction test handled it correctly and produced a **non-obvious** answer — "just leave retired devices out" looks sufficient until the sole-copy case makes it dangerous — which is the useful kind of confirmation, since a rule that only agrees with what you already thought is not being tested.

Two things the third domain did **not** exercise, so they remain on a two-domain base: whether two mechanisms are safe together, and the never-infer-from-prose rule. `systems/` has one mechanism and no log.

One rule generalised beyond where it was written. *Derive on demand; never store a "where am I"* was stated about **status**; `systems/` applied the same move to a **relationship**, recording each dependency once on the depending side and deriving the reverse direction rather than storing it as a second field. The underlying invariant is broader than status: **two records of one fact can disagree, and the derived one is the one that updates itself.**

And the cost of getting it wrong is low. Pick the wrong mechanism and you'll find out the first time state moves in a direction you didn't expect, then add or drop a field. That is an afternoon. The expensive mistake is the other one — inventing a state model for a domain that never needed one.

## Frontmatter

Frontmatter schemas are **per-domain**. `pkm/`'s applies to PKM notes only; `learning/` has its own. A new domain inherits neither by default, and should say so in its Conventions.

Two exclusions have held everywhere so far and are worth copying:

- **No `updated:`** — git knows.
- **No `tags:`** — this workspace retrieves by links. To group, write a note that links the group.

The underlying principle is worth more than either instance: **don't create a field that will be systematically wrong.** `learning/` excludes `done` from its status vocabulary for the same reason — a drill never finishes, so any vocabulary containing `done` would leave every drill permanently mislabelled.

## Registering it

1. Create `projects/<domain>/CONTEXT.md`.
2. Add a row to [CONTEXT-MAP.md](../../CONTEXT-MAP.md) — name, path, one-line scope.
3. If this workspace is published from, classify the new files in `publish/manifest.md`. A domain stub is normally `public`; anything holding real content is `private`.

Domain-specific decisions that need their reasoning recorded go in `projects/<domain>/docs/adr/`, not the system-wide `docs/adr/`.
