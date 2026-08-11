# Health — Context

Health records, and habits that are themselves about health — sleep, movement, food, symptoms, measurements. Treat contents as sensitive; **never fabricate values**.

> **Storage — decide this before writing anything real here.** This domain has no storage of its own. Its files live in the workspace's git repository and go wherever that repository goes; if it has a remote, these records are on it, and git history makes that permanent. A "sensitive" marking with no egress rule is decoration. **This workspace's rule: everything here lives in a private remote, and that remote is never made public.** A private host is access-controlled, not encrypted — adequate for records at this sensitivity, and the wrong answer for anything you would not want read under a subpoena or after an account compromise. The cheap moment to choose differently is while this domain is still empty.

**This domain does not own habit tracking as a mechanism.** Habits are kept per-domain: a practice routine belongs to [learning](../learning/CONTEXT.md), not here. Routing every habit through this tree would dilute the sensitivity marking above and bury health records under content that doesn't need the handling.

**Status: scaffolded, not yet specified.** This domain's content schema is a deliberate later effort — the architecture defined the domain-plugin *pattern*, not per-domain schemas. This domain's schema stays unspecified until real use earns one — when it does, see [docs/agents/domain-authoring.md](../../docs/agents/domain-authoring.md).

## Glossary

_Empty. Add terms here as they get resolved in real work — don't invent vocabulary upfront._

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its own schema is unspecified.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
