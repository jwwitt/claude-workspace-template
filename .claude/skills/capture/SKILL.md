---
name: capture
description: Drop raw material into the PKM inbox. Use when the user says to capture/save/note something, or when something durable-worthy surfaces in conversation and would otherwise be lost when the session ends.
---

# Capture

Write one file to `projects/pkm/inbox/`, then say you did it.

Capture is **cheap** — a capture costs nothing and can be discarded later, so the bar is "would this be a loss if the session ended now," not "is this worth a permanent note." Sorting happens in `/pkm-triage`; classifying here is wasted work.

## Steps

1. **Write** `projects/pkm/inbox/YYYY-MM-DD-<kebab-slug>.md`:

   ```markdown
   ---
   captured: YYYY-MM-DD
   source: <URL, "conversation", or where it came from>
   why: <one line — what made this worth keeping>
   ---

   <the material, in the user's words where you have them>
   ```

2. **Say so in your response** — one line naming the file. This is what keeps the inbox trustworthy: the user always knows what landed.

Done when the file exists and the response names it.

## Rules

- `why:` is the field that earns its keep. A capture with no stated reason is one that gets discarded at triage because nobody can reconstruct what was interesting about it. Write the reason even when it feels obvious.
- Preserve the user's own phrasing when the material is something they said. Their wording is the thing worth keeping; a summary loses the idea's edges.
- One capture per file. Two ideas in one file forces triage to split them.
- Capture the raw thing. Promotion into `notes/` needs the user's approval and belongs to `/pkm-triage` — writing there directly bypasses the gate that makes the graph trustworthy.
