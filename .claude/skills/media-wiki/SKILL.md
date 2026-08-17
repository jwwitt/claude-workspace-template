---
name: media-wiki
description: Record an episode or chapter of a series into the media wiki — a chronology of what happened plus a graph of the characters, places, groups and things in it. Use when the user says they have watched or read a specific unit of a work ("watched Hunter x Hunter 46", "finished chapter 30"), naming both the work and the unit.
---

# Media wiki

Turn a consumed episode or chapter into two things: a section in the work's **chronology**, and whatever **entity notes** that section earns.

Read [`projects/music-media/CONTEXT.md`](../../../projects/music-media/CONTEXT.md) first — it holds the entity schema and the naming rule. The reasoning behind every decision here is [`.scratch/media-summarizer/spec.md`](../../../.scratch/media-summarizer/spec.md).

> **The whole design rests on one fact: there is exactly one reader, and notes are only ever written from what he has already consumed.** A note containing only what Jonah has seen cannot spoil Jonah. **So the artifact needs no spoiler machinery — the entire constraint is on what you are allowed to read.**

## When this fires

**Only when the message names both the work and the unit.** *"Hunter x Hunter episode 46"* is an input. *"Watched some anime"* is not — ask, do not guess.

**Guessing a position is prohibited.** `progress` is authoritative; inferring one writes a false consumption record into the field everything else trusts.

**Ranges are normal** — *"episodes 40 through 46"* is one invocation and one fetch.

## Steps

1. **Resolve the work to an adaptation.** *Hunter × Hunter* is two series; episode 45 is not the same episode in each. If the work has more than one adaptation and the user has not said which, **ask**. Getting this wrong produces a chronology that looks right and describes a different story.
2. **Read the vault first.** Open the chronology file and the universe folder. You need the existing appearance history to apply the second-appearance rule, and you need `progress` to know whether this unit is new, a correction, or a repeat.
3. **Fetch the source** — see *Sources* below.
4. **Write the chronology section**, in order, under `## Episode N — Title`.
5. **Create or grow entity notes** per the second-appearance rule.
6. **Update `progress`** on the chronology note to the furthest unit consumed.
7. **Report** the file, the unit, and every entity note created or grown. Nothing lands silently.

## Sources

> **A URL is a commitment to a scope. A query is a wish.**

**Fetch a constructed URL. Never search for plot.** Search is permitted only to identify a work or locate a season index.

**Television:** Wikipedia season pages carry 100–200-word per-episode summaries that name characters explicitly, on a constructible URL, and one page is exactly one chronology file.

**Ask the fetch for the bounded range, not the page.** Request *"episodes 1–26 only"* and let the fetch return only those. **This is the spoiler mechanism, not a convenience** — the summarising model reads the whole page, and your context receives only the slice you asked for. A raw fetch puts the entire season, including everything past the user's position, into your context.

**Prohibited:** whole-work character pages, plot-summary pages, fandom wikis, and **anything you already know about the work**. A model that has read the series needs no web page to spoil anyone. Answer questions from the notes, not from memory.

**Books mostly fail and fail silently.** Per-chapter sources are usually absent or blocked, and a per-chapter query returns a whole-work summary that arrives looking like success. **If the result describes events beyond the requested unit, it is not a source — discard it.**

**No-source branch.** Report the work, the unit, the addresses tried and why each failed. Then offer: **dictate it yourself · skip the unit · drop the work from the wiki.** Never fall back to search, and never to your own knowledge.

## The second-appearance rule

> **An entity earns a note the second time it appears. Never the first.**

The decision looks **backward**, which is what makes it cheap — you have already processed units 1…N−1, so *"has this appeared before?"* is a question about the vault.

**On creation, backfill the first appearance from the existing chronology section.** Never re-research it; the source that would answer it is prohibited.

**Four kinds only: `character`, `place`, `group`, `thing`.** Events and arcs are not entities — an event is what happened in a unit, which is the chronology's job, and an arc is a span of units, represented as a grouping heading.

> **Re-checked 2026-08-17, because Jonah's request named events explicitly** — *"characters, events, places, etc."* — and a vocabulary that excludes something the user asked for deserves re-argument rather than a second recital. **It holds, and it is now visibly true rather than merely asserted.** Every entity note's `## Appearances` list is a set of links to episode sections, and **an episode section is the event** — so *"what happened, and who was in it"* is already answered, from both directions, without an `event` kind. Adding one would create a second record of what the chronology already holds, and the two would drift. **The right response to "I want more about events" was more chronology, which is what the coverage gap turned out to be.**

**A note is a first-appearance line, a description, the chronology links, and an *appears alongside* list derived from co-occurrence.**

### Descriptions — the rule changed 2026-08-17

> ~~**No description** — the sources descriptions come from are prohibited. Thin early is correct, not a gap.~~ **Overruled by Jonah**, who asked for real descriptions after using the wiki: *"I would like for the media notes to have more information in them about the characters, events, places, etc."* Asked whether he wanted more detail inside the rule or full descriptions accepting spoiler risk, **he chose full descriptions and accepted the risk.**

**Write the description from the chronology files in this vault, and from nothing else.**

That is not a compromise, it is the strongest available version of what he asked for. **The chronology never contains anything past `progress`**, because the bounded fetch is what built it — so a description assembled from it **cannot exceed the user's position, structurally, with no promise required.** A character-page fetch bounded by an instruction is weaker: the instruction is a request to a summarising model, and the failure is silent and unrecoverable.

**A description is prose about who someone is, what they want, and what they have done** — several sentences for a principal, one for a doorman. Link other entities inline. **It does not restate plot beat by beat**; the chronology holds that and the appearance links reach it.

**The old rule's reasoning still stands where it was actually aimed**: whole-work character pages remain prohibited as *sources*. What changed is that the vault now contains enough to write from without them.

**If the chronology is too thin to describe an entity, the description is thin. Say so; do not go and find more.**

### The derived half is derived, not typed

**Appearances and *appears alongside* are facts about the chronology**, so they are computed from it rather than maintained by hand:

```sh
python3 .scratch/media-summarizer/rederive-entities.py --write
```

It preserves everything above `## Appearances` — descriptions are safe — and is idempotent, so running it twice changes nothing. **Run it after writing chronology sections; do not hand-edit the two derived sections.**

> **This exists because the accretion the design assumed never happened.** The old rule said notes *"accrete one line at a time from episode summaries."* Nothing accreted: after thirteen episodes [[hxh-killua|Killua]]'s note still said nothing about him, and every *appears alongside* list was a hand transcription that had silently gone incomplete — Zebro's was missing two entities it should have had. **A rule that requires an agent to remember to widen 40 files is a rule that will not be followed**, and the failure is invisible because the notes still look correct.

**Two thresholds live in that script**, both there for the same reason the second-appearance rule exists: an *appears alongside* edge needs **two** shared episodes, and the list caps at **12**. Unfiltered, Killua co-occurred with 34 of 40 entities — a list that names most of the universe is not a graph edge, it is the cast list.

### Four corrections from the first real run

Found running Hunter × Hunter (2011) season 1. Each is a way the rule fails quietly.

- **A first run is a backfill from unit 1, not from where the user is.** The rule needs history; starting mid-series produces wrong notes against an empty vault. **If the chronology does not exist and `progress` is well past the start, say so and offer to backfill from the beginning** — that is a bulk operation, not this skill's normal per-unit shape.
- **Skip recaps.** Clip shows and "previously on" episodes are re-narration, not appearance, and counting them promotes entities that appeared once. Wikipedia marks them plainly. **This rule was written and then not followed** — season 1 counted episodes 13 and 26 as appearances for Gon, Mito and Whale Island. It is now enforced in `rederive-entities.py`, which skips any section whose body opens `**Recap.**`, rather than left as an instruction. *Mark recaps that way in the chronology, or they will be counted.*
- **Resolve aliases before counting.** A disguised or renamed character is one entity, not two. Where a summary names both an alias and the real identity, record one note and mention the alias in it.
- **Normalise names before matching.** Sources spell inconsistently — the same place appeared as *Cucuroo* and *Kukuroo* in consecutive episodes. Exact-match counting silently misses a second appearance and filters out an entity that earned a note.

## Layout

```text
projects/pkm/notes/source/<work>-<season>.md     ← chronology, progress: lives here
projects/music-media/<universe>/<slug>-<name>.md ← entity notes
```

**Chronology is per work; the graph is per universe.** Several works can share one universe and one cast.

**Entity filenames carry the universe slug**, linked with an alias: `[[hxh-kurapika|Kurapika]]`. **Non-negotiable** — `projects/` is one vault-wide wikilink namespace, entity notes are the highest-collision content in it, and Obsidian resolves bare names vault-wide, so a collision silently resolves to the wrong note.

## Approval

**Writes both outputs without asking, and announces every one.** Justified from the promotion gate's stated purpose — *"the gate that matters is on atomics, ideas entering the graph"* — and neither a chronology section nor an entity note is an idea. Both are records of what a source says.

**Ask first for exactly three things:**

- **Creating a new universe folder** — a work entering the wiki at all.
- **Writing a unit with no usable source.**
- **Backfilling from unit 1** — it is bulk, and it is not what the user asked for.

**Refuse a unit earlier than `progress`** unless told it is a correction. Earlier is either a fix or a mistake, and they need different handling.

**Be idempotent.** Re-running a processed unit must not duplicate a section or re-count an appearance.

## The gap check

**Say when a chronology has gaps behind its own `progress`.** Both halves sit in one file: `progress` says the position, the sections say what was noted. `the-way-of-kings.md` has sections at 1, 3–8, 10–12 with `progress: chapter 12` — chapters 2 and 9 were read and never noted.

This is derived, not remembered, which is why it is better than a reminder. **Filling a gap is an ordinary invocation for an earlier unit**, which the refusal rule above requires be deliberate.

## One more sentence it owes

When writing into a universe where **another work's `progress` is mid-sequence**, say so once. Watching a sequel while part-way through its predecessor leaks into shared entity notes — accepted, because the sequel spoils it far more thoroughly than a note would, but worth naming at the moment it happens.
