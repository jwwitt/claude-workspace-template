# ADR-0002: Multi-context layout, one CONTEXT.md per domain

**Status:** Accepted · 2026-08-10 · recorded 2026-08-11

Decided in `.scratch/claude-workspace-architecture/`, ticket 04. That effort holds the alternatives and the argument; this records what stands.

## Context

The repo was initially scaffolded **single-context** — one `CONTEXT.md` and `docs/adr/` at the root — because it was empty when the engineering-skill setup ran. It then turned out to house nine distinct domains: PKM, goals, health, business, music-media, finances, journaling, initiatives, and later learning.

A single root context document covering all of them would be read in full by every session regardless of the task, which is the specific failure this workspace was built to avoid: loading context nobody needed.

## Decision

**Multi-context.** The root holds [`CONTEXT-MAP.md`](../../CONTEXT-MAP.md), a routing table; each domain owns `projects/<domain>/CONTEXT.md`.

- **Read only the domain your task needs.** `CLAUDE.md` and `CONTEXT-MAP.md` are indexes, not briefings.
- **System-wide architecture decisions** go in root `docs/adr/`. A domain that accumulates its own gets `projects/<domain>/docs/adr/`.
- **A domain is a plugin.** The architecture defines the *pattern*; each domain's content schema is its own later decision, and stays an unfilled stub until real use earns it one — see [`domain-authoring.md`](../agents/domain-authoring.md).

## Consequences

- **The cost is the extra hop**, and it is the workspace's characteristic failure mode. The two-repo-split functional test found that routing failed most often at the *last* hop — domain doc to the skill that operates on it — not at the map. Any new domain doc must point onward to whatever acts on it, or it is unreachable in practice.
- Adding a domain means adding a row to `CONTEXT-MAP.md` as well as the directory. A domain absent from the map does not exist.
- Six of the nine domains are deliberately empty stubs. That is the pattern working, not incompleteness — filling them speculatively is argued against in the learning-domain spec and in `domain-authoring.md`.
- This shape is what makes the public template coherent: a cloner deletes the domains they don't want and adds their own, without touching anything structural.
