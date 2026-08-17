---
type: dashboard
created: 2026-08-16
cssclasses:
  - command-center
---

# Command Center

**[[pkm/CONTEXT|PKM]]** · **[[initiatives/CONTEXT|Initiatives]]** · **[[learning/CONTEXT|Learning]]** · **[[systems/CONTEXT|Systems]]** · **[[goals/CONTEXT|Goals]]** · **[[business/CONTEXT|Business]]** · **[[finances/CONTEXT|Finances]]** · **[[health/CONTEXT|Health]]** · **[[journaling/CONTEXT|Journaling]]** · **[[music-media/CONTEXT|Music & Media]]**

## Triage queue

Captures waiting in the inbox. Nothing clears these on its own — run `/pkm-triage`.

![[dashboard.base#Triage]]

## Active initiatives

![[dashboard.base#In flight]]

## Job scans

Dated evidence of what the market held. Postings close — an old scan is old, not wrong. Refresh with `/job-scan`.

![[dashboard.base#Job scans]]

## Learning

Syllabi in play, ordered as the curriculum sequences them.

![[dashboard.base#Syllabi]]

Assignments currently open. `unknown` means imported without a recorded completion state, not stalled.

![[dashboard.base#Open assignments]]

## Knowledge graph

Atomics are the gated layer — nothing lands here without approval.

![[dashboard.base#Notes by stage]]

## Recently touched

![[dashboard.base#Recent]]

## Run

Bases cannot execute anything, so this page does not try to list skills — a hand-written list goes stale the moment one is added or removed.

**The Command Center plugin** reads `.claude/skills/` directly and gives each skill a button and a command-palette entry. Open it from the terminal icon in the ribbon, or ⌘P → *Open Command Center*.

**The Workspace Console** (`python3 tools/dashboard/build.py --serve`) carries the rest — the ticket board, the vault graph, planning, and editable status on learning and initiatives.

---

Other views live in [[dashboard.base]] and aren't embedded here — *All initiatives*, *Assignments by status*, *Atomics*, *Sources*. Open the file to browse or edit any of them in the Bases UI.
