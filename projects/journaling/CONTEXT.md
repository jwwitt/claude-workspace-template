# Journaling — Context

Journals and reflection. Treat contents as sensitive.

> **Storage.** These files live in the workspace's git repository and go wherever it goes — see [health/CONTEXT.md](../health/CONTEXT.md) for the full reasoning. **This workspace's rule: private remote, never made public.** Journals name other people who never agreed to be written about; that is the exposure worth weighing here, more than anything about the author.

**Status: scaffolded, not yet specified.** This domain's content schema is a deliberate later effort — the architecture defined the domain-plugin *pattern*, not per-domain schemas. This domain's schema stays unspecified until real use earns one — when it does, see [docs/agents/domain-authoring.md](../../docs/agents/domain-authoring.md).

## Glossary

_Empty. Add terms here as they get resolved in real work — don't invent vocabulary upfront._

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md). Its own schema is unspecified.
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
