# Backlink template

The pointer that goes into a **new** project repo's own `CLAUDE.md`, so a session working in that repo knows this workspace exists.

Added **at repo creation**, alongside the repo's registry row. Retrofitting it into repos that predate this workspace is out of scope — the registry starts empty by design.

## The snippet

Paste into the new repo's `CLAUDE.md`:

```markdown
## Workspace

This project is registered in Jonah's workspace at
`/Users/jonahwitt/Documents/Claude Workspace` — it holds `registry/projects.md`
(where his other repos live) and any cross-project context. Read it when a task
reaches beyond this repo.
```

That's the whole thing. Then add the repo's row to [projects.md](projects.md).

## Why it's this short

The backlink answers exactly one question — *what else exists and where* — and a coding session rarely needs even that. Every line costs context on every turn in that repo, so it routes and stops.

It deliberately carries **no pointer to personal or life context**. A session debugging a build has no use for health or finance data, and the global `~/.claude/CLAUDE.md` already routes anyone who does need it. Keeping the two layers separate is what stops every coding session from loading a life-management briefing.

Adjust the wording per repo where it helps; keep the path, the registry mention, and the reach-beyond-this-repo condition.
