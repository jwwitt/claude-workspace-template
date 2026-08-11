# ADR-0001: When to write an ADR

**Status:** Accepted · 2026-08-11

## Context

`docs/adr/` has been referenced since the workspace was built — by `CLAUDE.md`, `CONTEXT-MAP.md`, and `docs/agents/domain.md`, which instructs skills to read ADRs before working and to flag conflicts with them. It has been empty the whole time. Nothing said what belonged in it, so nothing was ever put there.

Meanwhile the reasoning behind every decision this workspace has made lives in `.scratch/<effort>/` — maps, tickets and compiled specs, which are detailed and genuinely good. Two problems follow:

1. **`.scratch/` is excluded from the published template.** A cloner receives the conventions and none of the arguments that produced them. `CLAUDE.md` says so directly: "a workspace created from it carries the decisions but not the arguments."
2. **Efforts are indexed by effort, not by subject.** Someone who wants to know why domains work the way they do must first know that an effort called `claude-workspace-architecture` exists and that ticket 04 is the relevant one.

The risk in the other direction is real and is why this sat unanswered. An ADR per decision would duplicate the effort specs, and two records of one decision drift — which is the failure this workspace rules against everywhere else, from `learning/`'s non-overlapping-claims state model to the registry's refusal to hand-maintain what a command produces.

## Decision

**An architecture decision earns an ADR only when all three hold:**

1. **It constrains work beyond the effort that produced it** — someone will collide with it later without having read that effort.
2. **Its reasoning is not recoverable from the artifact it produced.** If the convention explains itself where it lives, that is already the record.
3. **Reversing it is expensive, or reversing it accidentally breaks something quietly.**

**An ADR states the decision and why. It never restates the effort's exploration.** The effort holds the alternatives, the arguments and the dead ends; the ADR holds what was chosen and what it costs, and links back for the rest. Where both exist, the effort is the authority on *how it was decided* and the ADR is the authority on *what stands*.

**Corollary — the publication asymmetry is the strongest single reason to write one.** A decision that shapes the *template* has no other channel to its readers, because `.scratch/` never reaches them. A decision that only affects Jonah's private content has a weaker case, since the effort is right there.

### What this excludes

- Decisions recorded in a document that already carries its own reasoning — `learning/CONTEXT.md`'s state model, `domain-authoring.md`'s location-vs-field rule, `CLAUDE.md`'s memory/content boundary. All three explain themselves at the point of use, which is better than an ADR because it is unmissable.
- Anything still being decided. That is a ticket.
- Per-domain decisions, which go in `projects/<domain>/docs/adr/` per [`domain-authoring.md`](../agents/domain-authoring.md).

## Consequences

- `docs/adr/` stays small on purpose. A directory with three entries that are all load-bearing is more useful than thirty that must be skimmed.
- Applying this test to the existing decisions yields exactly two backfills, written alongside this one: [ADR-0002](0002-multi-context-layout.md) and [ADR-0003](0003-publish-by-allowlist.md). Everything else either explains itself or is effort-local.
- ADRs publish. They are generic by construction — an ADR that could not be published is describing content, not architecture, and is probably the wrong artifact.
- Each new ADR needs a `public` row in [`publish/manifest.md`](../../publish/manifest.md). The manifest forbids globs on the public side, so this is one row per file, deliberately.
