# Context Map

This workspace is multi-context. Each domain below owns its own `CONTEXT.md`; read the ones relevant to your task, not all of them.

Adding a domain? See [docs/agents/domain-authoring.md](docs/agents/domain-authoring.md).

System-wide architecture decisions live in [docs/adr/](docs/adr/). A domain that accumulates its own decisions gets `projects/<domain>/docs/adr/`.

| Context | Doc | What it covers |
| --- | --- | --- |
| PKM | [projects/pkm/CONTEXT.md](projects/pkm/CONTEXT.md) | The 3-stage Zettelkasten: inbox → source/atomic/synthesis → outputs |
| Goals | [projects/goals/CONTEXT.md](projects/goals/CONTEXT.md) | Goals and planning |
| Health | [projects/health/CONTEXT.md](projects/health/CONTEXT.md) | Health records and health habits — sensitive; habits generally live with their own domain |
| Business | [projects/business/CONTEXT.md](projects/business/CONTEXT.md) | Business or freelance practice — clients, engagements, pipeline, admin |
| Music & media | [projects/music-media/CONTEXT.md](projects/music-media/CONTEXT.md) | Music and media consumption, library, references |
| Finances | [projects/finances/CONTEXT.md](projects/finances/CONTEXT.md) | Personal finances |
| Journaling | [projects/journaling/CONTEXT.md](projects/journaling/CONTEXT.md) | Journals and reflection |
| Initiatives | [projects/initiatives/CONTEXT.md](projects/initiatives/CONTEXT.md) | Life-style / big-picture project tracking |
| Learning | [projects/learning/CONTEXT.md](projects/learning/CONTEXT.md) | **Practice logs, and where the structure went.** Curricula, units and assignments moved to the self-hosted LMS on 2026-08-18 per [ADR-0005](docs/adr/0005-services-hold-the-record.md); the vault keeps the session history |
| Systems | [projects/systems/CONTEXT.md](projects/systems/CONTEXT.md) | Personal infrastructure — devices, what connects to what, and what breaks if it stops |

## Scope note

`registry/` is deliberately **not** a context. It indexes external code repos — a routing concern, not workspace content. See [registry/projects.md](registry/projects.md).

`projects/` is also the **Obsidian vault root**. Everything under it is human-facing content; repo machinery (`.scratch/`, `docs/`, `registry/`, `memory/`, root `CLAUDE.md`) sits outside the vault on purpose.
