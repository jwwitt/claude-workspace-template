# Health — Context

Health records, and habits that are themselves about health — sleep, movement, food, symptoms, measurements. Treat contents as sensitive; **never fabricate values**.

**This domain does not own habit tracking as a mechanism.** Habits are kept per-domain: a practice routine belongs to [learning](../learning/CONTEXT.md), not here. Routing every habit through this tree would dilute the sensitivity marking above and bury health records under content that doesn't need the handling.

**Status: scaffolded, not yet specified.** This domain's content schema is a deliberate later effort — the architecture defined the domain-plugin *pattern*, not per-domain schemas. This domain's schema stays unspecified until real use earns one.

## Glossary

_Empty. Add terms here as they get resolved in real work — don't invent vocabulary upfront._

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its own schema is unspecified.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
