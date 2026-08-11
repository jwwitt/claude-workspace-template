# Goals — Context

Goals and planning.

**Status: scaffolded, not yet specified.** This domain's content schema is a deliberate later effort — the architecture spec defined the domain-plugin *pattern*, not per-domain schemas. See [spec.md §10](../../.scratch/claude-workspace-architecture/spec.md).

## Glossary

_Empty. Add terms here as they get resolved in real work — don't invent vocabulary upfront._

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its own schema is unspecified.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
