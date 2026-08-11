# Context Map

This workspace is multi-context. Each domain below owns its own `CONTEXT.md`; read the ones relevant to your task, not all of them.

System-wide architecture decisions live in [docs/adr/](docs/adr/). A domain that accumulates its own decisions gets `projects/<domain>/docs/adr/`.

| Context | Doc | What it covers |
| --- | --- | --- |
| PKM | [projects/pkm/CONTEXT.md](projects/pkm/CONTEXT.md) | The 3-stage Zettelkasten: inbox → source/atomic/synthesis → outputs |
| Goals | [projects/goals/CONTEXT.md](projects/goals/CONTEXT.md) | Goals and planning |
| Health | [projects/health/CONTEXT.md](projects/health/CONTEXT.md) | Health and habit tracking |
| Business | [projects/business/CONTEXT.md](projects/business/CONTEXT.md) | Creative freelance business — session guitar, mixing, production, content |
| Music & media | [projects/music-media/CONTEXT.md](projects/music-media/CONTEXT.md) | Music and media consumption, library, references |
| Finances | [projects/finances/CONTEXT.md](projects/finances/CONTEXT.md) | Personal finances |
| Journaling | [projects/journaling/CONTEXT.md](projects/journaling/CONTEXT.md) | Journals and reflection |
| Initiatives | [projects/initiatives/CONTEXT.md](projects/initiatives/CONTEXT.md) | Life-style / big-picture project tracking |
| Learning | [projects/learning/CONTEXT.md](projects/learning/CONTEXT.md) | Instructional structure — curricula, syllabi, assignments, practice logs |

## Scope note

`registry/` is deliberately **not** a context. It indexes external code repos — a routing concern, not workspace content. See [registry/projects.md](registry/projects.md).

`projects/` is also the **Obsidian vault root**. Everything under it is human-facing content; repo machinery (`.scratch/`, `docs/`, `registry/`, `memory/`, root `CLAUDE.md`) sits outside the vault on purpose.
