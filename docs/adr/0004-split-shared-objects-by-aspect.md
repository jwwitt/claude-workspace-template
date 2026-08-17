# ADR-0004: When two domains claim the same object, split by aspect

**Status:** Accepted · 2026-08-13

## Context

A multi-context layout ([ADR-0002](0002-multi-context-layout.md)) gives each domain its own `CONTEXT.md` and its own patch of `projects/`. It says nothing about objects that belong to more than one domain, and those turn up constantly once a workspace holds real content.

**Four independent cases have now arrived, from three unrelated efforts:**

| Object | Claimed by | Arrived in |
| --- | --- | --- |
| **Studio hardware** | the business (what it cost) · systems (what it is plugged into) | [personal-systems-map 05](../../.scratch/personal-systems-map/issues/05-devices.md) |
| **Online accounts** | the vault (enumeration) · systems (what a service is *for*) | [personal-systems-map 04](../../.scratch/personal-systems-map/issues/04-accounts-and-storage-policy.md) |
| **Subscriptions** | systems · finances · business | [personal-systems-map 06](../../.scratch/personal-systems-map/issues/06-software.md) |
| **A consumed work** | PKM (what it *says*) · music-media (what the things in it *are*) | [media-summarizer 02](../../.scratch/media-summarizer/issues/02-the-boundary-against-source-notes.md) |
| **A game being practised** | music-media (a title consumed and rated) · learning (a skill being trained) | [the Rocket League entry](../../projects/initiatives/backlog.md), 2026-08-17 |

**All four resolved the same way, none of them by consulting the others.** The first three arrived in one sitting and were held pending a fourth, on the grounds that three arrivals from a single effort might be one author's habit rather than a finding. The fourth came from an unrelated effort two days later and landed identically — and it is stronger evidence than a fourth of the same kind would have been, because the first three are all *a cost aspect plus an infrastructure aspect*, and this one is neither.

> **A fifth case arrived 2026-08-17, after this ADR was accepted, and it is recorded because it is a new axis rather than a repeat.** Rocket League is simultaneously a row in [`media-library.md`](../../projects/music-media/media-library.md) — a title consumed and rated — and the subject of a [`learning/` curriculum](../../projects/learning/rocket-league/rocket-league-curriculum.md). The first four pairs were *cost + infrastructure* three times and *source + universe* once; **this is the first *consumed versus practised* pair**, and it resolved identically without anyone consulting the rule.
>
> **It also exercises the corollary in the direction that bites.** Rank and practice history are **training** state, so they belong to `learning/`, whose log derives dormancy from its own last entry — and appending them to the catalogue row would have put a second, unmaintained copy of the same fact in the domain that has no state model *because of this ADR*. The catalogue's job stays *what exists, and do I care*.

**The obvious alternative is to pick an owner**, and it fails in a specific way. Ownership forces a lossy choice: whichever domain does not win either loses the fact or keeps a copy. A copy is two records of one fact, which this workspace rules against everywhere — and the losing domain's `CONTEXT.md` then has to describe an object it does not hold, which is how a reader ends up in the wrong file.

**Why this needs an ADR**, against [ADR-0001](0001-when-to-write-an-adr.md)'s three tests:

1. **It constrains work beyond its effort** — four efforts have already collided with it, and any workspace with more than two domains will.
2. **The reasoning is not recoverable from the artifact.** What the split produces is two documents that link to each other, which looks like ordinary cross-referencing. Nothing at the site says *why* neither one owns the object, so the next person to meet the problem re-derives it.
3. **Reversing it is expensive and quiet.** Consolidating under an owner later means moving content and breaking every `[[wikilink]]` into it — and getting it wrong is silent, because a domain doc that overclaims reads perfectly well.

## Decision

> **When two domains claim the same object, split it by aspect and link. Do not assign an owner.**

Concretely:

- **Each domain records the aspect it can answer**, and says which question that is. `systems/` records what a device is connected to; `business/` records what it cost. Neither records the other.
- **They link across.** One graph, two entry points.
- **Neither domain's doc claims the object.** It claims an aspect, in those words, so a reader who arrives with the other question is routed rather than misled.
- **Nothing is duplicated for convenience.** If both domains would state a fact, exactly one states it and the other links.

### The corollary, which is the expensive part to rediscover

> **The aspect split determines where the *state* lives — so do the split before asking whether a domain needs a state model.**

`music-media/` looked like it needed one: works are consumed over time and progress moves. It has none. The split sent the chronology — and with it `progress` — to `pkm/`, leaving `music-media/` holding entity notes and a catalogue, neither of which has a lifecycle.

**Asked in the wrong order, the question gets the wrong answer**, and [`docs/agents/domain-authoring.md`](../agents/domain-authoring.md)'s state gate is exactly the kind of thing that gets asked early. Split first, then run the gate against what each domain actually holds.

## Consequences

**What this costs:**

- **Two files to read instead of one**, for anyone who wants the whole object. Accepted: reading three files per query is cheap at this scale, and the alternative is a cache that goes stale.
- **The split has to be *stated*, not just performed.** A domain doc that silently holds one aspect looks like a domain doc that holds the object badly.
- **It does not tell you where an aspect boundary falls.** That is still judgement, per object. The ADR fixes the *shape* of the answer, not the answer.

**What it buys:**

- No duplicated facts, so no disagreement between records.
- Domains stay small and honest — each says what it answers, which is also what stops the next domain overlapping it.
- New domains get a rule instead of an argument.

**Where the reasoning lives.** [personal-systems-map](../../.scratch/personal-systems-map/map.md) tickets 04–06 and [media-summarizer](../../.scratch/media-summarizer/map.md) tickets 02 and 08 hold the alternatives and the dead ends. Per [ADR-0001](0001-when-to-write-an-adr.md), those efforts are the authority on *how it was decided*; this ADR is the authority on *what stands*. **Both are excluded from the published template**, which is why this file exists.
