# Global pointer template

The pointer that goes into your own `~/.claude/CLAUDE.md`, so a Claude Code session started **anywhere on the machine** can find this workspace.

This is the **forward** direction. [backlink-template.md](backlink-template.md) is the reverse — a pointer from an individual project repo back to here. The two are separate on purpose: a coding session should be able to reach the registry without loading a life-management briefing.

## The snippet

Paste into `~/.claude/CLAUDE.md`, replacing the path:

```markdown
# Personal Workspace

Personal context — knowledge pipeline, life-management domains, and an index of
other code repos — lives at:

`<absolute-path-to-workspace>`

**When it's relevant, read `<workspace>/CLAUDE.md` first** — it's that workspace's
own index and is authoritative on how to navigate and edit it. It routes on to
`CONTEXT-MAP.md` and one `CONTEXT.md` per domain, so read only the domain the
task needs.

## When to pull from it

- The user asks about personal goals, health, finances, journaling, ongoing
  projects, or anything captured in their notes
- A request needs context about the user that isn't in the current project
- You need to find one of their other repos — the workspace holds
  `registry/projects.md`, a routing table

## When not to

- Working in an unrelated software project, where the request doesn't connect
- The current project has its own CLAUDE.md that already answers the question
```

The path must be **absolute** — a session in another directory has no relative route here.

## Why it's shaped this way

It routes and stops. The **when not to** half matters as much as the rest: without it, every session everywhere starts loading personal context it has no use for, and the token cost lands on every turn.

It also names no domains beyond a short list, so adding or removing a domain never requires editing a file outside this repo.
