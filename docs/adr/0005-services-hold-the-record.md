# ADR-0005: Where a service holds the content, the service is the record

**Status:** Accepted · 2026-08-18
**Amends:** [ADR-0004](0004-split-shared-objects-by-aspect.md) — its corollary only

## Context

This workspace was built on markdown files as the record, with everything else derived from them. Two conditions enforced it: **`derive, never store`**, and [ADR-0004](0004-split-shared-objects-by-aspect.md)'s corollary that *the aspect split determines where state lives* — which is why `music-media/` has no state model at all, and why the [Reminders projection](../../tools/reminders-sync/) and the [Workspace Console](../../tools/dashboard/README.md) both read files and never own them.

**On 2026-08-18 two services were stood up and the rule was reversed deliberately.** A course platform ([Tutor LMS](../../tools/lms-publish/README.md)) and a media tracker (Ryot) were self-hosted, each initially as a presentation layer over the vault. Asked where the content should actually live, Jonah ruled:

> **"Store both in Ryot as the source. Same with the learning module. The service should always be the source of truth."**

**This is recorded as a decision, not re-argued.** The case against it is already written down in two places — the [Canvas decline](../../projects/initiatives/backlog.md) and the media-tracker entry beside it — and both were overruled knowingly. What follows is what the ruling *costs* and what it therefore *requires*, because those are not obvious and are expensive to rediscover.

## Decision

> **Where a service holds the content, the service is the record. The vault does not keep a second copy.**

- **No coexistence.** A retired file is deleted, not left in place. Two stores of one fact disagree, and the stale one is the one that answers first.
- **The service's database is now irreplaceable content**, not a cache that can be rebuilt.
- **ADR-0004's decision stands. Only its corollary is amended.** Splitting a shared object by aspect and linking, with no owner, is unchanged and still governs domain docs. What changes is the corollary's claim that the split determines where *state* lives: state now lives in whichever service holds it.

### What the ruling requires, and none of it is optional

1. **A real database dump, before anything stops being authoritative.** A file-level copy of a running database is not a backup — Postgres often survives one by crash recovery and MariaDB sometimes does, which is worse than never working, because it fails at restore time on the one night it matters. Done 2026-08-18 in [`backup.sh`](../../projects/systems/homelab-config/opt/restic/backup.sh); both live data directories are excluded so nothing can mistake them for a usable copy, and a failed dump is a failed run with its own status field.

2. **Everything the file held must reach the service first.** The LMS publisher stripped frontmatter for months and nobody noticed, because the vault still had it. Retiring the markdown would have destroyed `provenance`, `created`, `status` and the **source citations** — the least reconstructible field a curriculum has. Carried as `_vault_*` post meta on 2026-08-18, 215 rows.

3. **Every writer into the retired tree must be rewired in the same change.** `/curriculum`, `/start-unit` and `/media-wiki` write markdown into trees that would no longer be read. A skill writing into a dead directory fails silently and looks like it worked.

4. **A migration that cannot complete does not license a retirement.** Ryot resolves media through metadata providers; TMDB and IGDB need credentials that did not exist on 2026-08-18, so films, games and music could not be imported. **The media catalogues were therefore kept**, and the ruling is applied to the learning half only until the rest can actually land.

## Consequences

**What this costs:**

- **The console's derived views go dark** for any domain that moves. They read files, and there are no longer files to read.
- **Authoring moves into a web UI.** Markdown in an editor is replaced by whatever form the service provides. That is an ergonomic change, not a neutral one.
- **Git stops being the history.** A file's record of who changed what and when is replaced by whatever the service keeps, which for both of these is less.
- **The blast radius of losing a database is now total for that domain**, which is what requirement 1 exists to bound.

**What it buys:**

- One place to look, and one place to write, per domain.
- The service's own features — progress, scrobbling, ratings history — become usable rather than decorative, which is what they were as a presentation layer.

**What is deliberately unresolved.** The vault still holds *chronology* positions in [`pkm/notes/source/`](../../projects/pkm/CONTEXT.md) frontmatter. When the media migration completes, that becomes the last collision: ADR-0004 ruled the chronology wins over a catalogue flag, and a tracker that stores progress is exactly the field that rule was written to exclude. **That decision is owed and is not made here.**
