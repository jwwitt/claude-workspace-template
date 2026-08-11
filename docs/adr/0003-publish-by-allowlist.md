# ADR-0003: Publish by allowlist, with no catch-all

**Status:** Accepted · 2026-08-11

Decided in `.scratch/two-repo-split/`. That effort is itself private — it inventories where sensitive content lives — so this ADR is the only published account of the decision, which is precisely the case [ADR-0001](0001-when-to-write-an-adr.md) exists to catch.

## Context

This workspace mixes structure that is true for anyone with content that is true only for its owner. Sharing the structure means separating the two, and the separation has to survive the workspace growing — a rule written once against a snapshot silently stops covering files added later.

Two directions of failure, and they are not symmetric. Publishing something private is **irreversible**: it is fetched, cached and indexed, and deleting it afterwards does not retract it. Failing to publish something public is merely an incomplete template, fixed whenever anyone notices.

## Decision

**Every file is classified in [`publish/manifest.md`](../../publish/manifest.md), and the export script has no judgement of its own.**

- Four classes: `public` (copied verbatim), `template` (taken from `publish/overlay/` instead, for files mixing structural shape with accumulating content), `public-only` (exists solely in the overlay), `private` (never copied).
- **No catch-all.** A file matching no rule aborts the export. This is what keeps "everything is classified" true rather than merely believed — and it is why adding a new effort directory or a new ADR requires a manifest row.
- **Globs are forbidden on the public side, permitted on the private side.** The asymmetry is the whole design: an over-matching public rule leaks, while an over-matching private rule only makes the template incomplete. Failures are pushed toward the recoverable direction.
- **The script never commits and never pushes.** Publishing stays a separate deliberate act, with a human reading the diff.

The governing test for classification: **a file publishes if it would be equally true in someone else's workspace.**

## Consequences

- **The manifest is the security control**, not the script. All the judgement lives in a table a person can read in one sitting; a script with no discretion can be trusted once rather than re-audited every run.
- **Structural changes carry a standing obligation**: re-run `publish/export.sh` and review the diff. Skipping it means the template quietly describes a workspace that no longer exists.
- **Identity-concession and template-correctness are different axes**, and conflating them caused the one real misclassification found in testing. Jonah's name publishing is fine; a file handing a cloner *his* business as *their* domain context is not, even though both are "about him." That file became `template`.
- **The backstop is narrower than it looks.** The overlap check catches private content copy-pasted into a structurally-public file. It cannot catch a misclassified manifest entry, because the export is built only from public-classified files — a file wrongly marked public leaves the private corpus and the check goes quiet. Only the manifest and the diff review catch that.
