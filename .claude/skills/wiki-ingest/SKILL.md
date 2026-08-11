---
name: wiki-ingest
description: Turn an external source into PKM notes. Use when the user shares a URL, article, paper, PDF, video link, or pasted text and wants it read, ingested, or turned into notes.
---

# Wiki ingest

Turn one external source into a source note, then propose the atomics worth extracting from it.

Read `projects/pkm/CONTEXT.md` first — it holds the note format (frontmatter, filenames, links) this skill writes to, and it is the single source of truth for it.

An explicit ingest has a known source and a known type, so it already **is** a literature note — write the source note straight into `projects/pkm/notes/source/`, bypassing the inbox. The gate this skill respects is the one on **atomics**: those need the user's approval, same as any promotion.

## Steps

1. **Get the content.** URLs via `WebFetch`; local files and PDFs via `Read`; pasted text as given. For video and audio, see *Sources without a transcript* below.
2. **Write the source note** into `notes/source/`, with `source:` and `sourceType:` set. Capture what the source actually says — its claims, its evidence, its structure — not your reaction to it.
3. **Add its `INDEX.md` line**, then report the file.
4. **Propose the atomics** worth extracting, in one batch: for each, the claim in one sentence and the filename you'd write. Check `notes/INDEX.md` first — where the graph already holds an idea, propose folding into that note instead of a new one.
5. **Wait for approval**, then write the approved atomics, link them into the graph, and update `INDEX.md`.

Done when the source note exists, the atomics are proposed, and every approved atomic is written and indexed.

## What earns an atomic

A source yields far fewer atomics than it has paragraphs. Extract the ideas that would still be worth holding if the source vanished — a claim you'd want to reason with later, connected to what you already know.

Restating the source's outline produces notes nobody rereads. If a candidate atomic only makes sense while holding the source in mind, it belongs in the source note.

Link every atomic back to its source note with a `[[wikilink]]`, and to the existing atomics it bears on. Links are the retrieval mechanism.

## Sources without a transcript

There's no reliable transcript tool for video or audio. Write a **stub source note**: the link, `sourceType: video`, and whatever the user gives you — their timestamps, their summary, what they found interesting. Mark it clearly as a stub.

A stub is a real note that enriches later, and it hangs atomics from the user's own observations immediately. Where much of the input arrives as video, this path carries weight — treat it as a first-class outcome.

## Provenance

Set `author:` honestly — `claude` when you drafted it, `co` when the user reshaped it in the approval round, `user` when the words are theirs. A source note you wrote from a fetched article is `claude`, and that is fine; it exists in `notes/` because the user accepted the ingest.
