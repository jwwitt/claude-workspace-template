# Workspace Console

A live dashboard over this workspace: a kanban ticket board, planning (goals,
initiatives, backlogs), an Obsidian-style graph of the whole vault, a media
room, the PKM pipeline, learning progress, skills, agents, domains, and repo
activity — all read from the files themselves.

## Running it

```sh
python3 tools/dashboard/build.py --serve    # live at localhost:8787
python3 tools/dashboard/build.py --open     # build a portable snapshot and open it
python3 tools/dashboard/build.py --json     # dump the scan, for piping into something else
```

Python 3.9+, standard library only. No install, no dependencies, no network.

**`--serve` is the live mode, and live means seconds.** The page probes
`/api/version` every 2.5s — a cheap mtime walk, not a re-scan — and pulls a
full re-scan only when that fingerprint moves. Edit a ticket, save a note,
make a commit: the page updates itself a moment later, and the pill in the
sidebar says when it last synced. Plain `build` inlines a snapshot instead,
which is what makes `dist/index.html` a single file you can open from anywhere.

## The views

| View | What it shows |
| --- | --- |
| **Overview** | What needs a decision, ticket mix, commit activity, effort progress |
| **Board** | The live ticket tracker — Ready / Blocked / Resolved columns. *Blocked is derived*: a ticket sits there only while a ticket it names is still open |
| **Planning** | Goal notes (with their open questions), initiatives, both backlogs |
| **Questions** | Every open question in one place — goal notes' `## Open` bullets and unresolved tickets' `## Question` — each with an answer box, plus a quick-capture box and what's waiting in the inbox |
| **Graph** | The vault as Obsidian sees it — every `projects/` markdown file a node, every `[[wikilink]]` an edge, unresolved links as dashed ghosts. Drag, zoom, filter, hide groups from the legend, click a node to open it |
| **Notes** | The PKM pipeline stages and every note in the graph |
| **Media** | The reading room — sources laned by reading position (`progress`) and `sourceType`, from the source notes' own frontmatter |
| **Learning** | **Subjects and their dormancy**, from `logs/` — sessions counted and the last one dated. Curricula and assignments live in the LMS since [ADR-0005](../../docs/adr/0005-services-hold-the-record.md) and are deliberately *not* fetched: this scanner is offline by design, and reaching over HTTP would trade that for a unit list nobody disputes |
| **Efforts / Domains / Skills / Agents / System** | Wayfinder efforts and specs, domain maturity, the skill and agent rosters, ADRs, registry, git. *Efforts also lists **Documents** — work under `.scratch/` with no `map.md`, which every other view here is blind to* |

## What it reads

| Data | Source |
| --- | --- |
| Tickets, efforts | `.scratch/*/map.md` and `.scratch/*/issues/*.md` |
| Documents | `.scratch/*/` **without** a `map.md` — a plan, a runbook, a record. Kind is read from the filename; `research/`-only directories are excluded, since that is where a briefed agent is told to write |
| Goals | `projects/goals/*.md`, plus any vault note named `*-goal` |
| Backlogs | `.scratch/backlog.md`, `projects/initiatives/backlog.md` |
| Initiatives | `projects/initiatives/*.md` frontmatter, joined to their efforts by slug |
| Graph | every `*.md` under `projects/` (minus furniture: CONTEXT/INDEX/README) |
| Media | `projects/pkm/notes/source/*.md` frontmatter (`sourceType`, `progress`) |
| Knowledge | `projects/pkm/` — counted by stage directory |
| Learning | `projects/learning/logs/*-log.md` — session dates, fenced examples excluded |
| Skills | `.claude/skills/*/SKILL.md` frontmatter |
| Domains | `CONTEXT-MAP.md`, plus each domain's own `CONTEXT.md` and file count |
| System | `docs/adr/`, `registry/projects.md`, `git log` |

Everything above is **derived** — there is no state file to keep in sync, so the
dashboard cannot drift from the workspace. It can only be as old as its last
scan, and in serve mode that is a couple of seconds.

## The two writes

Both are serve-mode only, and both are disabled by `--read-only`.

**`POST /api/capture`** — submitting from the **Questions** view writes one file
into `projects/pkm/inbox/`, in the documented capture format, naming the question
and the file it came from so triage can fold the answer back where it belongs.
Answers are captured verbatim. This one only ever *adds* a file.

**`POST /api/frontmatter`** — the status controls in **Learning** and on an
initiative's detail panel set one frontmatter key on one existing note. This one
*edits*, so it is fenced considerably harder:

| Guard | Rule |
| --- | --- |
| **Gated tree** | Never writes inside `projects/pkm/notes/`. A note being there means Jonah approved it, and a dashboard toggle is not approval |
| **Key** | `status` only. Not a general file editor reachable over HTTP |
| **Value** | Must be one the domains already define — `active`, `completed`, `planned`, `paused`, `done`, `not started`, `unknown` |
| **Location** | Must resolve inside the workspace, be markdown, and already have frontmatter — writing frontmatter into a file that had none would invent a schema for a domain that has not earned one |

Everything outside the single edited line is carried across untouched, body
included. Where a record has no file behind it — an unmaterialized unit — the
control degrades to the read-only chip rather than offering a write that would
fail.

**Promotion is still `/pkm-triage`'s**, and tickets, goals and backlog entries
are still read-only here. Goals in particular: that domain's schema is
deliberately unspecified, and a management UI would have to invent one.

**One exception:** `agents.json`. Agent types come from the Claude Code harness
rather than this repo, so they cannot be read off disk. That file is the only
hand-maintained input, and the Agents panel labels it as declared. Update it when
the harness roster changes.

## Serving it from a always-on box

If a server already holds a synced copy of the workspace, it can serve the
console to every device you own without the laptop being awake:

```sh
docker run -d --name workspace-console --restart unless-stopped \
  -v /path/to/synced/workspace:/claude-workspace:ro \
  -p <private-mesh-ip>:8787:8787 \
  python:3.12-alpine \
  python3 /claude-workspace/tools/dashboard/build.py \
    --serve --host 0.0.0.0 --port 8787 --read-only --no-open
```

Four things make that command the shape it is:

- **`--read-only` when the copy is a one-way mirror.** A file-sync engine that
  pulls in one direction will fight or revert anything written on the receiving
  side, so the capture endpoint is disabled there and the Questions view says
  so rather than offering a box that silently fails. Writes belong to whatever
  already owns writing — an editor on the phone, or the console running where
  the authoritative copy lives.
- **Bind a private-mesh address, never `0.0.0.0` on the host.** The container
  binds `0.0.0.0` *inside* itself; the published port is pinned to one
  interface. This console renders whatever the vault holds, including anything
  sensitive, so the mesh is the boundary — never port-forward it or expose it
  to the public internet.
- **The template is re-read per request**, so UI edits reach the server through
  the sync itself, with no redeploy. Changes to `build.py` or `scan.py` need a
  container restart.
- **Git panels go quiet** if the sync excludes `.git`, which is the correct way
  to sync a repository. Nothing else changes.

## Watching a backup

Set `WORKSPACE_BACKUP_STATUS` to a file a backup job writes, and the console
reports how stale the last success is — silently when it is recent, as a warning
past 26 hours, and as a critical past 48. The file is `key=value` lines:

```
last_run=2026-08-13T03:38:46-04:00
last_exit=1
last_result=failed
last_success=2026-08-12T15:52:15-04:00
```

Only `last_success` is required. Unset the variable and the feature disappears
entirely — no panel, no assumptions.

**It measures age-of-last-success rather than the last exit code**, and that is
the whole point: a job that never ran cannot report that it never ran, so
freshness has to be judged by the reader. A failed run is also reported
immediately even when the previous success is recent, because one failure after
a good night is not an emergency but it is the first sign of one.

## Reading the panels

- **Needs a decision** ranks what is actually waiting on you — blocked backlog
  entries first, then risks, then parked efforts and uncompiled specs. An empty
  panel is the correct steady state.
- **Effort state** is inferred from ticket resolution, then overridden by the
  initiative note where one exists — that note is where *parked* is recorded, and
  ticket counts alone can't tell parked from stalled.
- **Spec state** distinguishes *compiled*, *compiled elsewhere* (High Regard
  Studios compiled into `projects/business/`), *none by design* (Guitar Program,
  where closing the initiative was the result), and *not yet compiled*. Only the
  last one is a gap.
- **Graph ghosts** (dashed rings) are wikilinks whose target note doesn't exist
  yet. Each one marks a note worth writing, not an error.

## Getting around

`⌘K` searches everything — tickets, notes, goals, media, skills, agents,
efforts, initiatives, domains, vault files, backlog entries — and jumps to it.
`Esc` closes. Clicking any card, row, or graph node opens its detail panel.
Charts carry a **Table** toggle for the numbers behind them.

## Extending it

Add a panel by calling `defineView(id, label, icon, section, count, render)` in
`template.html`; it registers itself in the sidebar under its section. Add data
by writing a `scan_*` function in `scan.py` and wiring it into `scan()`.

Chart colors come from the validated palette in the `dataviz` skill — light and
dark are separately stepped, not flipped. The graph is an all-pairs color case,
so its groups use the blue/yellow/magenta/green subset (the only 4-slot subset
that passes the all-pairs floors in both modes), with "life" folded to neutral
and phantoms carried by shape. If you change any series, re-run that skill's
`validate_palette.js` rather than eyeballing the result.
