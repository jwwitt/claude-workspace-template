# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check `<context-root>/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. Where a domain-modeling skill is installed, it creates them lazily as terms and decisions actually get resolved; otherwise they accrete by hand.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root). **This workspace is one** — its context root is `projects/`, not `src/`:

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── projects/                          ← the context root; `src/` in a code repo
    ├── pkm/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions, if any
    └── learning/
        ├── CONTEXT.md
        └── docs/adr/
```

The context root is whatever directory holds the contexts — `src/` in a typical code repo, `projects/` here. `CONTEXT-MAP.md` names every context and where it lives, so read that rather than assuming a layout.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap worth raising before you build on it.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
