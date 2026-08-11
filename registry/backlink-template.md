# Backlink template

The pointer that goes into a **new** project repo's own `CLAUDE.md`, so a session working in that repo knows this workspace exists.

This is the **reverse** direction. [global-pointer-template.md](global-pointer-template.md) is the forward one — a pointer in `~/.claude/CLAUDE.md` that makes this workspace reachable from anywhere on the machine.

Added **at repo creation**, alongside the repo's registry row. Retrofitting it into repos that predate this workspace is out of scope — the registry starts empty by design.

## The snippet

Paste into the new repo's `CLAUDE.md`:

```markdown
## Workspace

This project is registered in the personal workspace at
`<absolute-path-to-workspace>` — it holds `registry/projects.md` (an index of
the other repos) and any cross-project context. Read it when a task reaches
beyond this repo.
```

Replace `<absolute-path-to-workspace>` with the real path on this machine. It has to be absolute: a session running in the other repo has no relative route back here.

That's the whole thing. Then add the repo's row to [projects.md](projects.md).

## Why it's this short

The backlink answers exactly one question — *what else exists and where* — and a coding session rarely needs even that. Every line costs context on every turn in that repo, so it routes and stops.

It deliberately carries **no pointer to personal or life context**. A session debugging a build has no use for health or finance data, and the global `~/.claude/CLAUDE.md` already routes anyone who does need it. Keeping the two layers separate is what stops every coding session from loading a life-management briefing.

Adjust the wording per repo where it helps; keep the path, the registry mention, and the reach-beyond-this-repo condition.

## When not to paste it

**A repo derived from this workspace never gets a backlink.** The snippet carries an absolute path to the workspace, so pasting it into a repo that is published — or into any file that gets copied out of here — writes a local filesystem path somewhere it doesn't belong. It would also be overwritten the moment that repo is regenerated.

The backlink is for **independent** repos: separate projects with their own history that occasionally need to reach back here. A derived repo already has the relationship recorded in the other direction, in [projects.md](projects.md), which is the correct place for it.
