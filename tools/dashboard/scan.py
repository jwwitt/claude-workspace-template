"""Read the workspace and return everything the dashboard renders.

Every number the dashboard shows is derived here from files on disk. Nothing is
hand-maintained, so a stale dashboard is impossible — it can only be out of date
by however long ago it was scanned.

The one exception is the agent roster, which has no filesystem source: agent
types are supplied by the harness, not the repo. It is read from agents.json and
labelled as declared rather than derived.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# --- frontmatter and markdown helpers ---------------------------------------

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def frontmatter(text: str) -> dict[str, str]:
    """Parse the flat `key: value` frontmatter this workspace uses."""
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def body(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def title(text: str, fallback: str) -> str:
    for line in body(text).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def first_paragraph(text: str, after: str | None = None) -> str:
    """The first real prose paragraph, optionally after a given heading."""
    lines = body(text).splitlines()
    if after is not None:
        for i, line in enumerate(lines):
            if line.strip().lower() == after.strip().lower():
                lines = lines[i + 1 :]
                break
        else:
            return ""
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if collected:
                break
            continue
        if stripped.startswith(("#", ">", "|", "```", "---")):
            if collected:
                break
            continue
        collected.append(stripped)
    return " ".join(collected)


def strip_markdown(text: str) -> str:
    """Flatten inline markdown to plain text for display in the UI."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = WIKILINK.sub(r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"~~([^~]*)~~", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


# --- wayfinder efforts ------------------------------------------------------

TICKET_FIELD = re.compile(
    r"^(Type|Status|Blocked by):\s*(.+)$", re.MULTILINE | re.IGNORECASE
)
# Map status shows up as a bold sentence; the wording varies by effort.
MAP_STATUS = re.compile(
    r"\*\*((?:Status:|Complete|Closed|Parked)[^*]{0,220})\*\*", re.IGNORECASE
)


# A `Status:` line is hand-written prose about as often as it is a value. Five
# tickets in one effort read `**resolved 2026-08-14**`, one of them with a
# whole clause appended after an em dash. The decoration is annotation and the
# leading word is the state — so without this the Board counts finished work as
# open, which is the single thing a board must never do.
STATUS_WORDS = (
    "resolved", "claimed", "blocked", "parked", "wontfix",
    "needs-triage", "needs-info", "ready-for-agent", "ready-for-human",
    "active", "open",
)


def normalize_status(value: str, default: str = "open") -> str:
    """Reduce a hand-written Status: line to the state word it starts with."""
    cleaned = re.sub(r"[*_`]", "", value or "").strip().lower()
    # Split only on separators that carry surrounding space, so the hyphens
    # inside `ready-for-agent` survive.
    cleaned = re.split(r"\s+[—–]\s+|\s+-\s+|,|\(", cleaned, maxsplit=1)[0].strip()
    for word in STATUS_WORDS:
        if cleaned == word or cleaned.startswith(word + " "):
            return word
    return cleaned or default


def ticket_fields(text: str) -> dict[str, str]:
    """Read the header block only.

    Tickets quote frontmatter samples further down — ticket 08 of
    personal-systems-map carries a `Status: active` inside one — so a whole-file
    scan reads the sample as the ticket's own status.
    """
    header = re.split(r"^## ", body(text), maxsplit=1, flags=re.MULTILINE)[0]
    fields: dict[str, str] = {}
    for key, value in TICKET_FIELD.findall(header):
        fields.setdefault(key.lower(), value.strip())
    return fields


def scan_efforts(root: Path) -> list[dict]:
    efforts = []
    scratch = root / ".scratch"
    if not scratch.is_dir():
        return efforts

    for directory in sorted(p for p in scratch.iterdir() if p.is_dir()):
        map_path = directory / "map.md"
        if not map_path.is_file():
            continue
        map_text = read(map_path)

        tickets = []
        for ticket_path in sorted(directory.glob("issues/*.md")):
            ticket_text = read(ticket_path)
            fields = ticket_fields(ticket_text)
            number = re.match(r"(\d+)", ticket_path.stem)
            tickets.append(
                {
                    "id": f"{directory.name}/{ticket_path.stem}",
                    "number": number.group(1) if number else "",
                    "title": title(ticket_text, ticket_path.stem),
                    "type": fields.get("type", "unspecified").lower(),
                    "status": normalize_status(fields.get("status", "open")),
                    # The line as written, kept so the drawer can show the
                    # annotation the normalisation drops (a resolution date is
                    # worth reading even though it is not a state).
                    "status_raw": fields.get("status", "").strip(),
                    "blocked_by": fields.get("blocked by", ""),
                    "effort": directory.name,
                    "updated": datetime.fromtimestamp(ticket_path.stat().st_mtime)
                    .date()
                    .isoformat(),
                    "path": str(ticket_path.relative_to(root)),
                    "question": truncate(
                        strip_markdown(first_paragraph(ticket_text, "## Question")), 260
                    ),
                }
            )

        # A ticket is blocked only while one of the tickets it names is itself
        # unresolved — a stale "Blocked by: 01" on a ticket whose blocker has
        # since resolved is not a live blockage, and the board must not show it
        # as one.
        resolved_numbers = {t["number"] for t in tickets if t["status"] == "resolved"}
        for ticket in tickets:
            blockers = [b.strip() for b in ticket["blocked_by"].split(",") if b.strip()]
            open_blockers = [b for b in blockers if b not in resolved_numbers]
            ticket["open_blockers"] = open_blockers
            ticket["blocked"] = ticket["status"] != "resolved" and bool(open_blockers)

        resolved = sum(1 for t in tickets if t["status"] == "resolved")
        status_match = MAP_STATUS.search(map_text)
        blurb = strip_markdown(status_match.group(1)) if status_match else ""

        if tickets and resolved == len(tickets):
            state = "complete"
        # Struck text dropped for the same reason it is everywhere else here:
        # a map that says `~~parked~~ — restarted` is not parked. No map says
        # that today; this keeps the rule uniform rather than waiting for one.
        elif (re.search(r"\bparked\b", STRIKETHROUGH.sub(" ", map_text), re.IGNORECASE)
              and resolved == 0):
            state = "parked"
        elif resolved:
            state = "in-progress"
        else:
            state = "open"

        efforts.append(
            {
                "slug": directory.name,
                "title": title(map_text, directory.name),
                "destination": truncate(
                    strip_markdown(first_paragraph(map_text, "## Destination")), 400
                ),
                "status_note": truncate(blurb, 220),
                "state": state,
                "tickets": tickets,
                "resolved": resolved,
                "total": len(tickets),
                "spec": spec_state(
                    directory, map_text, finished=bool(tickets) and resolved == len(tickets)
                ),
                "path": str(map_path.relative_to(root)),
                "updated": last_touched(directory),
            }
        )
    return efforts


def spec_state(directory: Path, map_text: str, finished: bool = False) -> dict:
    """Where an effort's spec ended up.

    Not every effort compiles one into its own directory: High Regard Studios
    compiled to `projects/business/`, and Guitar Program deliberately compiled
    none because closing the initiative *was* the result. Treating either as a
    missing spec would raise an alarm about work that is finished.

    `by-design` used to be detected by looking for the words "no spec" in the
    map, which **no map in this repo has ever said** — Guitar Program words it
    as *"fold this back into `learning/` and close the initiative, which is a
    complete result"*, and prose is not going to converge on a keyword. So the
    branch was unreachable and its effort was reported as a gap for as long as
    it had been finished.

    Derived instead: an effort whose every ticket is resolved, with no spec in
    its directory and none named elsewhere, did not *fail* to compile one. It
    finished without needing one, which is the distinction `by-design` exists
    to draw. An unfinished effort with no spec is still genuinely pending.
    """
    if (directory / "spec.md").is_file():
        return {"state": "compiled", "target": f"{directory.name}/spec.md"}

    elsewhere = re.search(r"spec is compiled to \[`?([^`\]]+)", map_text)
    if elsewhere:
        return {"state": "elsewhere", "target": elsewhere.group(1)}

    # Kept as an explicit override: if a map ever does say it outright, that
    # beats inference.
    if re.search(r"\bno spec\b", map_text, re.IGNORECASE) or finished:
        return {"state": "by-design", "target": ""}

    return {"state": "pending", "target": ""}


def last_touched(directory: Path) -> str:
    stamps = [p.stat().st_mtime for p in directory.rglob("*.md") if p.is_file()]
    if not stamps:
        return ""
    return datetime.fromtimestamp(max(stamps)).date().isoformat()


# --- initiatives ------------------------------------------------------------


def scan_initiatives(root: Path) -> list[dict]:
    directory = root / "projects" / "initiatives"
    if not directory.is_dir():
        return []

    initiatives = []
    for path in sorted(directory.glob("*.md")):
        if path.stem in {"CONTEXT", "backlog"}:
            continue
        text = read(path)
        fields = frontmatter(text)
        initiatives.append(
            {
                "slug": path.stem,
                "title": title(text, path.stem),
                "status": fields.get("status", "unknown").lower(),
                "started": fields.get("started", ""),
                "summary": truncate(strip_markdown(first_paragraph(text)), 300),
                "standing": truncate(
                    strip_markdown(first_paragraph(text, "## Where it stands")), 400
                ),
                "path": str(path.relative_to(root)),
                "effort": path.stem if (root / ".scratch" / path.stem).is_dir() else "",
                "links": sorted(set(WIKILINK.findall(text)))[:12],
            }
        )
    return initiatives


# --- backlogs ---------------------------------------------------------------

BACKLOG_ENTRY = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.*)$")


# Clauses that report an entry's *state* rather than name its subject. A
# headline made of these says nothing: "IN PROGRESS, part-built. DONE, same day
# it was found." was a real one, and it named neither the idea nor the outcome.
STATUS_STAMP = re.compile(
    r"^\s*(?:→\s*)?(?:IN PROGRESS|DONE|COMPLETED?|RESOLVED|DECIDED|GRADUATED"
    r"|UNBLOCKED|SUPERSEDED|WITHDRAWN|ANSWERED|FIXED)\b",
    re.IGNORECASE,
)


def entry_headline(raw: str, plain: str) -> str:
    """The clause that names an entry, whether or not it is still live.

    Strike markers are removed rather than their contents, because a closed
    entry's struck lead *is* its name — `~~Adopt a password manager~~ →
    **DECIDED AND DONE**` is called "adopt a password manager", and dropping
    the struck half leaves a headline that begins with an arrow.
    """
    text = raw.replace("~~", "")

    # `idea → outcome` is how a closed entry is written, so whatever precedes
    # the first arrow is the name — and it is not always bold. Two entries name
    # themselves in plain text, and a bold-only scan walks straight past them
    # into the outcome clause.
    if "→" in text:
        lead = strip_markdown(text.split("→", 1)[0]).strip()
        if len(lead) >= 25 and not STATUS_STAMP.match(lead):
            return lead

    for clause in re.findall(r"\*\*(.+?)\*\*", text, re.DOTALL):
        candidate = strip_markdown(clause).strip()
        if len(candidate) >= 25 and not STATUS_STAMP.match(candidate):
            return candidate
    return strip_markdown(text).strip() or plain


def scan_backlog(root: Path, relative: str, label: str) -> dict:
    path = root / relative
    if not path.is_file():
        return {"label": label, "path": relative, "sections": {}, "entries": []}

    entries: list[dict] = []
    sections: Counter[str] = Counter()
    section = "Open"
    for line in read(path).splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            sections.setdefault(section, 0)
        match = BACKLOG_ENTRY.match(line.strip())
        if not match:
            continue
        raw = match.group(2)
        sections[section] += 1
        plain = strip_markdown(raw)
        headline = entry_headline(raw, plain)
        entries.append(
            {
                "date": match.group(1),
                "board": label,
                "section": section,
                "headline": truncate(headline, 150),
                "detail": truncate(plain, 700),
                "flags": entry_flags(raw),
            }
        )
    return {
        "label": label,
        "path": relative,
        "sections": dict(sections),
        "entries": entries,
    }


# A backlog entry is an argument that gets amended in place: claims are struck
# through when they stop holding, and the correction is written beside them
# rather than replacing them. So the text carries its own history, and a
# substring scan reads that history as the present.
STRIKETHROUGH = re.compile(r"~~.+?~~", re.DOTALL)

# How this backlog closes an entry: strike the lead clause and write the
# outcome beside it — `~~**Adopt a password manager**~~ → **DECIDED AND DONE**`.
# The entry stays in `## Open` because its reasoning is still worth reading,
# so the section heading cannot be trusted for state and the struck lead can.
# Checked against all 12 open entries: it separates the 5 live ones from the 7
# closed ones exactly, where matching on words like DONE or RESOLVED does not —
# those appear mid-entry in entries that are still live.
CLOSED_LEAD = re.compile(r"\s*~~")


def entry_flags(raw: str) -> list[str]:
    """Flags describing an entry's *current* state.

    Two things have to be dropped before matching, and both were producing
    false criticals on the Overview:

    - **Struck text.** `~~blocked on a Let's Encrypt certificate~~ — UNBLOCKED
      and live` is a resolved blocker. Reading it as blocked is reading the
      retraction as the claim.
    - **Substrings.** `"blocked" in "unblocked"` is true, so the very word that
      announces a blocker is *cleared* was what kept flagging it.
    """
    live = STRIKETHROUGH.sub(" ", raw).lower()
    flags = []
    if re.search(r"\bin progress\b|\bpart-built\b", live):
        flags.append("in-progress")
    if re.search(r"\bblocked\b", live) and not re.search(r"\bunblocked\b", live):
        flags.append("blocked")
    if re.search(r"\brisks?\b", live):
        flags.append("risk")
    if CLOSED_LEAD.match(raw):
        flags.append("closed")
    return flags


# --- skills and agents ------------------------------------------------------


def scan_skills(root: Path) -> list[dict]:
    directory = root / ".claude" / "skills"
    if not directory.is_dir():
        return []

    skills = []
    for skill_path in sorted(directory.glob("*/SKILL.md")):
        text = read(skill_path)
        fields = frontmatter(text)
        user_only = fields.get("disable-model-invocation", "").lower() == "true"
        skills.append(
            {
                "name": fields.get("name", skill_path.parent.name),
                "description": fields.get("description", ""),
                "invocation": "user-invoked" if user_only else "auto",
                "summary": truncate(strip_markdown(first_paragraph(text)), 320),
                "steps": [
                    strip_markdown(line[2:])
                    for line in body(text).splitlines()
                    if re.match(r"^\d+\.\s", line.strip())
                ][:8],
                "writes": writes_to(text),
                "path": str(skill_path.relative_to(root)),
                "lines": len(text.splitlines()),
            }
        )
    return skills


def writes_to(text: str) -> list[str]:
    """Directories a skill writes into, as named in its own instructions."""
    found = re.findall(r"`(projects/[^`]*?/)`", text)
    return sorted(set(found))[:4]


def scan_agents(root: Path) -> list[dict]:
    """Agent types come from the harness, so they are declared, not derived."""
    config = Path(__file__).parent / "agents.json"
    if not config.is_file():
        return []
    try:
        return json.loads(read(config)).get("agents", [])
    except json.JSONDecodeError:
        return []


def scan_guardrails(root: Path) -> list[str]:
    """The subagent rules from CLAUDE.md — the policy the agents run under."""
    text = read(root / "CLAUDE.md")
    match = re.search(
        r"^## Subagents and usage limits\s*\n(.*?)(?=^## )", text, re.DOTALL | re.MULTILINE
    )
    if not match:
        return []
    return [
        truncate(strip_markdown(line.strip()[2:]), 240)
        for line in match.group(1).splitlines()
        if line.strip().startswith("- ")
    ]


# --- domains ----------------------------------------------------------------

CONTEXT_MAP_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|")


def scan_domains(root: Path) -> list[dict]:
    text = read(root / "CONTEXT-MAP.md")
    domains = []
    for line in text.splitlines():
        match = CONTEXT_MAP_ROW.match(line.strip())
        if not match:
            continue
        name, _, doc_path, covers = match.groups()
        if name.lower() in {"context", "---"}:
            continue
        context_file = root / doc_path
        directory = context_file.parent
        context_text = read(context_file)

        files = [
            p
            for p in directory.rglob("*.md")
            if p.is_file() and p.name != "CONTEXT.md"
        ]
        domains.append(
            {
                "name": name.strip(),
                "slug": directory.name,
                "covers": covers.strip(),
                "path": doc_path,
                "maturity": domain_maturity(context_text),
                "status_note": truncate(strip_markdown(domain_status(context_text)), 200),
                "file_count": len(files),
                "files": sorted(str(p.relative_to(root)) for p in files)[:24],
                "has_glossary": "## Glossary" in context_text,
                "sensitive": "sensitive" in covers.lower(),
            }
        )
    return domains


def domain_status(text: str) -> str:
    match = re.search(r"\*\*Status:([^*]{0,200})\*\*", text)
    return match.group(1).strip() if match else ""


def domain_maturity(text: str) -> str:
    """A domain is a stub, partly specified, or specified — read from its own words."""
    status = domain_status(text).lower()
    if "stub" in status or "not yet" in status:
        return "stub"
    # "partly" and "partially" are both in use — initiatives says one,
    # music-media the other — and matching only "partial" reported a domain
    # that calls itself half-finished as fully specified. Its own doc says the
    # music half "is untouched and remains a stub".
    if re.search(r"\bpart(ly|ial(ly)?)\b", status):
        return "partial"
    if status:
        return "specified"
    return "specified" if "## Glossary" in text and len(text) > 1500 else "stub"


# --- pkm --------------------------------------------------------------------


def scan_pkm(root: Path) -> dict:
    base = root / "projects" / "pkm"

    # Documentation that lives inside a stage folder is furniture, not content.
    # The inbox's README.md is deliberate and permanent: an empty directory does
    # not sync, so without it the inbox disappears from every other device the
    # moment triage empties it. Counting it would report a capture that is not
    # there — and the one number on this dashboard that must never cry wolf is
    # the inbox, because nothing clears it automatically.
    FURNITURE = {"INDEX.md", "README.md"}

    def count(*parts: str) -> int:
        directory = base.joinpath(*parts)
        if not directory.is_dir():
            return 0
        return sum(
            1
            for p in directory.rglob("*.md")
            if p.is_file() and p.name not in FURNITURE
        )

    notes = []
    for stage in ("source", "atomic", "synthesis"):
        for path in sorted((base / "notes" / stage).glob("*.md")):
            text = read(path)
            fields = frontmatter(text)
            notes.append(
                {
                    "slug": path.stem,
                    "title": title(text, path.stem),
                    "stage": stage,
                    "created": fields.get("created", ""),
                    "summary": truncate(strip_markdown(first_paragraph(text)), 260),
                    "path": str(path.relative_to(root)),
                    "links": sorted(set(WIKILINK.findall(text)))[:10],
                }
            )

    return {
        "stages": [
            {"name": "Inbox", "key": "inbox", "count": count("inbox")},
            {"name": "Source", "key": "source", "count": count("notes", "source")},
            {"name": "Atomic", "key": "atomic", "count": count("notes", "atomic")},
            {"name": "Synthesis", "key": "synthesis", "count": count("notes", "synthesis")},
            {"name": "Outputs", "key": "outputs", "count": count("outputs")},
        ],
        "notes": notes,
    }


# --- learning ---------------------------------------------------------------

# A curriculum lists its units either as a numbered list or as a table with a
# leading number column. Both are in use and neither is wrong — a subject whose
# units gate each other reads as a sequence, one whose units do not reads as a
# table with a "why here in the order" column. Matching only the list form made
# `sexuality` — five units and 98 built assignments — report as an empty subject.
CURRICULUM_UNIT = re.compile(r"^(?:\d+\.|\|\s*\d+\s*\|)\s*\[\[([^\]|]+)")


def scan_learning(root: Path) -> list[dict]:
    base = root / "projects" / "learning"
    if not base.is_dir():
        return []

    subjects = []
    for directory in sorted(p for p in base.iterdir() if p.is_dir() and p.name != "archive"):
        curriculum_path = directory / f"{directory.name}-curriculum.md"
        if not curriculum_path.is_file():
            continue
        curriculum_text = read(curriculum_path)

        units = []
        in_units = False
        for line in body(curriculum_text).splitlines():
            if line.startswith("## "):
                in_units = line.strip() == "## Units"
                continue
            if not in_units:
                continue
            match = CURRICULUM_UNIT.match(line.strip())
            if not match:
                continue
            slug = match.group(1)
            unit_dir = directory / slug
            syllabus = unit_dir / f"{slug}.md"
            status = "not started"
            assignments = []
            if syllabus.is_file():
                status = frontmatter(read(syllabus)).get("status", "active")
                for path in sorted(unit_dir.glob("*.md")):
                    if path.stem == slug:
                        continue
                    fields = frontmatter(read(path))
                    assignments.append(
                        {
                            "slug": path.stem,
                            "title": title(read(path), path.stem),
                            "status": fields.get("status", "planned"),
                            # Addressable so the console can write status back.
                            "path": str(path.relative_to(root)),
                        }
                    )
            units.append(
                {
                    "slug": slug,
                    "label": strip_markdown(line.strip()),
                    "status": status,
                    "materialized": syllabus.is_file(),
                    "assignments": assignments,
                    "path": str(syllabus.relative_to(root)) if syllabus.is_file() else None,
                }
            )

        standing = []
        for path in sorted(directory.glob("*.md")):
            fields = frontmatter(read(path))
            if fields.get("type") == "assignment":
                standing.append(
                    {
                        "slug": path.stem,
                        "title": title(read(path), path.stem),
                        "status": fields.get("status", "active"),
                        "path": str(path.relative_to(root)),
                    }
                )

        proficiency = ""
        match = re.search(r"^>\s*\*\*(.+?)\*\*", body(curriculum_text), re.MULTILINE | re.DOTALL)
        if match:
            proficiency = truncate(strip_markdown(match.group(1)), 420)

        log_path = directory / f"{directory.name}-log.md"
        log_entries = 0
        if log_path.is_file():
            log_entries = sum(
                1
                for line in read(log_path).splitlines()
                if re.match(r"^\|\s*\d{4}-\d{2}-\d{2}", line.strip())
            )

        subjects.append(
            {
                "subject": directory.name,
                "proficiency": proficiency,
                "units": units,
                "standing": standing,
                "log_entries": log_entries,
                "path": str(curriculum_path.relative_to(root)),
            }
        )
    return subjects


# --- registry, adrs, git ----------------------------------------------------

REGISTRY_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*<?([^|>]*?)>?\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def scan_registry(root: Path) -> list[dict]:
    text = read(root / "registry" / "projects.md")
    rows = []
    for line in text.splitlines():
        match = REGISTRY_ROW.match(line.strip())
        if not match:
            continue
        name, remote, local, purpose, status = match.groups()
        if not remote.startswith("http"):
            continue
        rows.append(
            {
                "name": name.strip(),
                "remote": remote.strip(),
                "local": local.strip().strip("`"),
                "purpose": purpose.strip(),
                "status": status.strip(),
            }
        )
    return rows


def scan_adrs(root: Path) -> list[dict]:
    directory = root / "docs" / "adr"
    if not directory.is_dir():
        return []
    adrs = []
    for path in sorted(directory.glob("*.md")):
        text = read(path)
        adrs.append(
            {
                "id": path.stem.split("-")[0],
                "title": title(text, path.stem),
                "summary": truncate(strip_markdown(first_paragraph(text)), 220),
                "path": str(path.relative_to(root)),
            }
        )
    return adrs


def scan_publish(root: Path) -> dict:
    """Whether the manifest still covers every file, asked of `export.sh` itself.

    Deliberately shells out rather than re-parsing `publish/manifest.md` here.
    The classification rules are subtle — directory rules, globs, and a
    public-before-private precedence — and a second implementation of them
    would eventually disagree with the first. The copy that drifts unnoticed
    would be this one, which is the safety check, so it is the worse of the
    two to have wrong.

    The failure this surfaces is specifically a *silent* one: an unclassified
    file aborts the export, which is correct and protects nothing if nobody
    runs the export. A mechanism cannot tell you it is unused.
    """
    script = root / "publish" / "export.sh"
    if not script.is_file():
        return {"available": False, "ok": True, "unclassified": []}

    try:
        result = subprocess.run(
            [str(script), "--check"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {"available": False, "ok": True, "unclassified": []}

    if result.returncode == 0:
        return {"available": True, "ok": True, "unclassified": []}

    unclassified = [
        line.strip()
        for line in result.stderr.splitlines()
        if line.startswith("  ") and line.strip()
    ]
    return {"available": True, "ok": False, "unclassified": unclassified}


def scan_index_coverage(root: Path) -> dict:
    """Whether CLAUDE.md's index names every tracked top-level directory.

    A mention is not an index entry. `tools/` existed, was described in passing
    in two files that were read, and was absent from the one table anyone
    consults to learn what this workspace contains — and a whole session went
    into rebuilding the console that lives there. The symptom of a missing row
    is not an error; it is a successful build of something redundant, which
    nothing else here can detect.

    Deliberately exemption-free. An allowlist of directories that "do not need
    a row" would rebuild the exact trap this check exists to close: the next
    directory added to it stops being reported, silently, by the mechanism
    meant to report it. If something tracked genuinely does not belong in the
    index, the honest fixes are to give it a row saying so or to stop tracking
    it — not to teach the check to skip it.
    """
    text = read(root / "CLAUDE.md")
    section = re.search(
        r"^## Where things live\s*\n(.*?)(?=^## )", text, re.DOTALL | re.MULTILINE
    )
    if not section:
        return {"available": False, "ok": True, "missing": [], "indexed": []}

    indexed: set[str] = set()
    for line in section.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cell = line.split("|")[1].strip() if line.count("|") >= 2 else ""
        for path in re.findall(r"[`\[]([^`\]]+)[`\]]", cell):
            # removeprefix, not lstrip: lstrip("./") eats the leading dot of
            # `.claude/` and `.scratch/`, silently reporting both as missing.
            head = path.strip().removeprefix("./").split("/")[0]
            if head:
                indexed.add(head)

    try:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {"available": False, "ok": True, "missing": [], "indexed": []}

    if tracked.returncode != 0:
        return {"available": False, "ok": True, "missing": [], "indexed": []}

    dirs = sorted(
        {
            line.split("/")[0]
            for line in tracked.stdout.splitlines()
            if "/" in line
        }
    )
    missing = [d for d in dirs if d not in indexed]
    return {
        "available": True,
        "ok": not missing,
        "missing": missing,
        "indexed": sorted(indexed),
    }


def scan_git(root: Path, max_days: int = 45, min_days: int = 14) -> dict:
    def run(*args: str) -> str:
        try:
            return subprocess.run(
                ["git", *args],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""

    log = run("log", "--pretty=format:%ad\x1f%s\x1f%h", "--date=short")
    commits = []
    for line in log.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 3:
            commits.append({"date": parts[0], "subject": parts[1], "hash": parts[2]})

    counts = Counter(c["date"] for c in commits)
    today = date.today()

    # Window the chart to the repo's actual age. A fixed 45 days on a repo a few
    # days old spends most of its width on blank space and squashes the bars
    # that carry the signal.
    days = max_days
    if commits:
        first = date.fromisoformat(commits[-1]["date"])
        days = min(max_days, max(min_days, (today - first).days + 1))

    activity = [
        {
            "date": (day := (today - timedelta(days=offset)).isoformat()),
            "count": counts.get(day, 0),
        }
        for offset in range(days - 1, -1, -1)
    ]

    return {
        "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
        "dirty": bool(run("status", "--porcelain")),
        "total": len(commits),
        "recent": commits[:14],
        "activity": activity,
        "window_days": days,
        "last": commits[0]["date"] if commits else "",
    }


# --- attention --------------------------------------------------------------


def without_prefix(detail: str, headline: str) -> str:
    """Drop the headline off the front of the detail so a row doesn't say it twice."""
    stem = headline.rstrip("…").strip()
    if stem and detail.startswith(stem):
        return detail[len(stem) :].lstrip(" .,—-–") or detail
    return detail


def build_attention(data: dict) -> list[dict]:
    """What is actually asking for a decision, ranked by how loud it should be."""
    items: list[dict] = []

    inbox = next(
        (s["count"] for s in data["pkm"]["stages"] if s["key"] == "inbox"), 0
    )
    if inbox:
        items.append(
            {
                "severity": "warning",
                "title": f"{inbox} capture{'s' if inbox != 1 else ''} waiting in the PKM inbox",
                "detail": "Nothing clears the inbox on its own — /pkm-triage is user-invoked.",
                "action": "/pkm-triage",
            }
        )

    for entry in data["initiatives_backlog"]["entries"] + data["workspace_backlog"]["entries"]:
        if entry["section"].lower() != "open":
            continue
        # A closed entry stays in Open for its reasoning, but its work has
        # graduated, resolved or been decided. Ranking it here asks for a
        # decision that was already made.
        if "closed" in entry["flags"]:
            continue
        severity = (
            "critical" if "blocked" in entry["flags"]
            else "serious" if "risk" in entry["flags"]
            else None
        )
        if severity:
            items.append(
                {
                    "severity": severity,
                    "title": entry["headline"],
                    "detail": without_prefix(entry["detail"], entry["headline"]),
                    "action": "",
                }
            )

    publish = data.get("publish", {})
    if publish.get("available") and not publish.get("ok"):
        missing = publish["unclassified"]
        shown = ", ".join(missing[:3]) + ("…" if len(missing) > 3 else "")
        items.append(
            {
                "severity": "serious",
                "title": f"{len(missing)} file{'s' if len(missing) != 1 else ''} "
                f"in no publish rule — the export is aborting: {shown}",
                "detail": "Nothing has leaked; an unclassified file stops the export, which is "
                "the allowlist working. But the export only protects anything when someone runs "
                "it, and it cannot report that it is unused — so until these are classified in "
                "publish/manifest.md, the public repo is simply not being updated.",
                "action": "publish/export.sh --check",
            }
        )

    coverage = data.get("index_coverage", {})
    if coverage.get("available") and not coverage.get("ok"):
        missing = coverage["missing"]
        shown = ", ".join(f"{d}/" for d in missing[:4]) + ("…" if len(missing) > 4 else "")
        items.append(
            {
                "severity": "warning",
                "title": f"{len(missing)} tracked director{'ies are' if len(missing) != 1 else 'y is'} "
                f"missing from CLAUDE.md's index: {shown}",
                "detail": "A mention is not an index entry. An index naming most of the tree reads "
                "as exhaustive and gets trusted as a closed list, so what is missing is not merely "
                "unfound — it is denied by a document that is right about everything else. The "
                "symptom is not an error but a successful build of something redundant, which is "
                "why nothing else here can catch it.",
                "action": "",
            }
        )

    backup = data.get("backup") or {}
    state = backup.get("state")
    failed_recently = backup.get("last_result") == "failed"
    # A failure is reported even when the last success is still recent: one
    # failed run after a good one is not an emergency, but it is the first
    # sign of one, and staying silent for a day is how the last outage went
    # unnoticed.
    if state in {"critical", "stale", "never", "unreadable"} or (
        state == "fresh" and failed_recently
    ):
        if state == "fresh":
            title = "The most recent backup run failed"
            detail = (
                f"The last success was {describe_age(backup['age_hours'])}, so nothing is "
                "lost yet — but the run that should have replaced it did not finish."
            )
        elif state == "never":
            title = "No backup has ever succeeded"
            detail = "The status file records no successful run at all."
        elif state == "unreadable":
            title = "Backup status is configured but unreadable"
            detail = (
                f"Nothing could be read from {backup.get('path', 'the status file')} — "
                "the reporter may not have run yet, or the path is wrong."
            )
        else:
            age = describe_age(backup["age_hours"])
            title = f"Last successful backup was {age}"
            detail = (
                f"The most recent run {'failed' if failed_recently else 'has not succeeded'}. "
                "Offsite protection is only as current as this timestamp."
            )
        items.append(
            {
                "severity": "critical" if state in {"critical", "never"} else "warning",
                "title": title,
                "detail": detail,
                "action": "",
            }
        )

    embeds = data["graph"].get("broken_embeds", [])
    if embeds:
        missing = sorted({e["target"] for e in embeds})
        items.append(
            {
                "severity": "warning",
                "title": f"{len(embeds)} embeds point at files that do not exist: {', '.join(missing)}",
                "detail": "These render as broken blocks in Obsidian. A `.base` target is a Bases "
                "view — the notes it was meant to list are still there, but nothing surfaces them, "
                "which is why so much of the vault has no inbound link.",
                "action": "",
            }
        )

    for effort in data["efforts"]:
        if effort["state"] == "parked":
            items.append(
                {
                    "severity": "warning",
                    "title": f"{effort['title']} is parked at the map",
                    "detail": effort["status_note"]
                    or f"{effort['total'] - effort['resolved']} tickets keep; nothing is being lost.",
                    "action": "",
                }
            )
        elif effort["state"] == "complete" and effort["spec"]["state"] == "pending":
            items.append(
                {
                    "severity": "warning",
                    "title": f"{effort['title']}: every ticket resolved, no spec compiled",
                    "detail": "The effort has run to its answers but nothing has been written up.",
                    "action": "",
                }
            )

    rank = {"critical": 0, "serious": 1, "warning": 2, "good": 3}
    items.sort(key=lambda item: rank.get(item["severity"], 4))
    return items


# --- vault graph ------------------------------------------------------------

# Furniture files are structure, not content — a CONTEXT.md node in every domain
# would put ten identical hubs on the graph and say nothing.
GRAPH_FURNITURE = {"CONTEXT.md", "INDEX.md", "README.md", "backlog.md"}


def graph_group(parts: tuple[str, ...]) -> str:
    """Which color family a vault file belongs to.

    Five groups, matching the five categorical slots the graph legend uses:
    the three PKM stages, learning, and everything else ("life" — goals,
    health, initiatives, journaling, and the rest of the domains).
    """
    if parts[0] == "pkm":
        if len(parts) >= 4 and parts[1] == "notes" and parts[2] in ("source", "atomic", "synthesis"):
            return parts[2]
        return "life"
    if parts[0] == "learning":
        return "learning"
    return "life"


CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
CODE_SPAN = re.compile(r"`[^`\n]*`")
VAULT_LINK = re.compile(r"(!?)\[\[([^\]|#]+)")


def outbound_links(text: str) -> list[tuple[bool, str]]:
    """Wikilink targets in a note, as `(is_embed, target)`.

    Code is stripped first. This workspace's own docs write `[[wikilinks]]`
    inside backticks to *describe* the syntax, and Obsidian does not render
    those as links either — counting them invents a broken link out of prose.
    Anchors and aliases are dropped, but a path-qualified target keeps its
    path so the caller can try the whole thing before the bare name.
    """
    text = CODE_SPAN.sub(" ", CODE_FENCE.sub(" ", text))
    return [
        (bool(bang), target.strip().lower())
        for bang, target in VAULT_LINK.findall(text)
        if target.strip()
    ]


def scan_graph(root: Path) -> dict:
    """The whole vault as Obsidian sees it: every note a node, every wikilink
    an edge. Link targets that match no file become phantom nodes, the same
    unresolved-link ghosts Obsidian draws — they mark notes worth writing.

    Resolution has to match Obsidian's or the graph reports faults that aren't
    there: `[[business/CONTEXT]]` is a valid path-qualified link, `![[x.png]]`
    is an attachment rather than a missing note, and a link inside backticks is
    not a link at all. Only a target that resolves to nothing is a ghost.
    """
    vault = root / "projects"
    if not vault.is_dir():
        return {"nodes": [], "edges": [], "broken_embeds": []}

    every_file = [
        p for p in vault.rglob("*") if p.is_file() and ".obsidian" not in p.parts
    ]
    # Markdown first, so a name shared with an attachment resolves to the note.
    every_file.sort(key=lambda p: (p.suffix != ".md", p.as_posix()))

    # Every key a wikilink could legitimately use: bare name, name with
    # extension, and vault-relative path either way.
    resolvable: dict[str, Path] = {}
    for path in every_file:
        rel = path.relative_to(vault).as_posix().lower()
        for key in (path.stem.lower(), path.name.lower(), rel, rel.rsplit(".", 1)[0]):
            resolvable.setdefault(key, path)

    notes = [p for p in every_file if p.suffix == ".md" and p.name not in GRAPH_FURNITURE]

    nodes: list[dict] = []
    index_of: dict[str, int] = {}
    outbound: list[list[tuple[bool, str]]] = []
    for path in notes:
        text = read(path)
        rel = path.relative_to(vault)
        stem = path.stem.lower()
        if stem in index_of:  # vault filenames are unique by convention; be safe
            continue
        index_of[stem] = len(nodes)
        outbound.append(outbound_links(text))
        nodes.append(
            {
                "id": path.stem,
                "title": title(text, path.stem),
                "group": graph_group(rel.parts),
                "domain": rel.parts[0],
                "created": frontmatter(text).get("created", ""),
                "summary": truncate(strip_markdown(first_paragraph(text)), 240),
                "path": str(path.relative_to(root)),
            }
        )

    edges: set[tuple[int, int]] = set()
    broken_embeds: list[dict] = []
    for i, links in enumerate(outbound):
        for is_embed, target in links:
            if target == nodes[i]["id"].lower():
                continue
            hit = resolvable.get(target) or resolvable.get(target.rsplit("/", 1)[-1])
            if hit is not None:
                if hit.suffix != ".md":
                    continue  # an image or other attachment — not a graph edge
                key = hit.stem.lower()
                if key not in index_of:
                    continue  # resolves to furniture, which the graph omits
                j = index_of[key]
            elif is_embed:
                # An embed of something absent renders as a broken block in
                # Obsidian, which a phantom node would not convey.
                broken_embeds.append({"target": target, "note": nodes[i]["path"]})
                continue
            else:
                if target not in index_of:
                    index_of[target] = len(nodes)
                    nodes.append(
                        {
                            "id": target,
                            "title": target,
                            "group": "phantom",
                            "domain": "",
                            "created": "",
                            "summary": "Linked but not yet written — an unresolved wikilink.",
                            "path": "",
                        }
                    )
                j = index_of[target]
            edges.add((min(i, j), max(i, j)))

    degree = Counter()
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    for i, node in enumerate(nodes):
        node["degree"] = degree.get(i, 0)

    return {"nodes": nodes, "edges": sorted(edges), "broken_embeds": broken_embeds}


# --- media ------------------------------------------------------------------


def reading_lane(progress: str) -> str:
    """Which lane a source note sits in, derived from its `progress` position.

    The note stores a *position* ("chapter 12", "s4e12", "finished", "not
    started") and never a lane. The lane is computed here because a stored lane
    and a stored position are two records of one fact, and they drift — which is
    exactly what `readingStatus` did before this: it said `queued` on a note
    holding twelve chapters of reading.

    Emphasis and a trailing date are stripped before matching the two reserved
    values, because every other hand-written state in this workspace has
    eventually been annotated that way -- tickets grew `**resolved
    2026-08-14**`. No note words it like that today, and `finished` falling
    through to in-progress is a silent wrong answer rather than a visible one.

    Deliberately *not* prefix-matched: "finished chapter 3" is a position in a
    book someone is still reading, and treating a leading `finished` as the
    reserved value would file it as done.
    """
    value = re.sub(r"[*_`]", "", progress).strip().lower()
    value = re.sub(r"\s*\(?\d{4}-\d{2}-\d{2}\)?$", "", value).strip()
    if not value:
        return "unspecified"
    if value in {"not started", "unread", "queued"}:
        return "queued"
    if value in {"finished", "complete", "completed", "done"}:
        return "completed"
    return "in-progress"


# `in progress` is a position that names no position. Six notes carry it,
# inherited from the 2026-08-12 migration's `readingStatus: in-progress`, and
# pkm/CONTEXT.md calls it "a degraded value and not a target to write" that
# should be replaced the next time that book is picked up. Nothing surfaces
# that today, so the nudge never arrives.
DEGRADED_PROGRESS = {"in progress", "in-progress", "started", "reading"}


def progress_is_degraded(progress: str) -> bool:
    return re.sub(r"[*_`]", "", progress).strip().lower() in DEGRADED_PROGRESS


def scan_media(root: Path) -> dict:
    """The reading/watching room, derived from source notes' own frontmatter:
    sourceType says what kind of thing it is, `progress` how far in it Jonah is.

    The lane is derived from the position rather than stored beside it — see
    `reading_lane`."""
    directory = root / "projects" / "pkm" / "notes" / "source"
    items = []
    if directory.is_dir():
        for path in sorted(directory.glob("*.md")):
            if path.name in GRAPH_FURNITURE:
                continue
            text = read(path)
            fields = frontmatter(text)
            source = fields.get("source", "").strip().strip('"')
            work, _, author = source.partition("—")
            items.append(
                {
                    "slug": path.stem,
                    "title": title(text, path.stem),
                    "work": work.strip() or title(text, path.stem),
                    "author": author.strip(),
                    "kind": fields.get("sourceType", "unspecified").lower(),
                    "progress": fields.get("progress", "").strip(),
                    "status": reading_lane(fields.get("progress", "")),
                    "progress_degraded": progress_is_degraded(fields.get("progress", "")),
                    "created": fields.get("created", ""),
                    "provenance": fields.get("provenance", ""),
                    "sections": sum(
                        1 for line in body(text).splitlines() if line.startswith("## ")
                    ),
                    "words": len(body(text).split()),
                    "links": sorted(set(WIKILINK.findall(text)))[:10],
                    "path": str(path.relative_to(root)),
                }
            )

    attachments = 0
    attachment_dir = directory / "attachments"
    if attachment_dir.is_dir():
        attachments = sum(
            1 for p in attachment_dir.iterdir() if p.is_file() and not p.name.startswith(".")
        )

    return {"items": items, "attachments": attachments}


# --- goals ------------------------------------------------------------------


def section_bullets(text: str, heading: str, limit: int = 8) -> list[str]:
    """Top-level bullets under a given ## heading, flattened to plain text.

    Kept long (500 chars) because these bullets are also the open *questions*
    the console offers for answering — a question cut mid-premise can't be
    answered well.

    Two things are deliberately excluded, and both were putting settled matters
    in front of the user with an answer box attached:

    - **Bullets inside a deeper subsection.** Only `## ` used to close the
      section, so every bullet under every `###` beneath it was collected too.
      In one goal note that swept up seven bullets of analysis and standing
      decisions and offered them as open questions, where the real count was
      zero. A subsection's bullets argue that subsection's point; the
      section's own list is what stops at its first subheading.
    - **Struck bullets.** These notes close a question the way the rest of the
      workspace does: strike it and write the answer beside it. An answered
      question is the one thing an open-questions list must not contain.
    """
    lines = body(text).splitlines()
    bullets: list[str] = []
    in_section = False
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            # Any heading ends the section's own list: a sibling or shallower
            # one leaves it, a deeper one starts a subsection of its own.
            in_section = line.strip().lower() == heading.lower()
            continue
        if in_section and re.match(r"^-\s+", line):
            item = line.strip()[2:]
            if item.lstrip().startswith("~~"):
                continue
            bullets.append(truncate(strip_markdown(item), 500))
    return bullets[:limit]


def scan_goals(root: Path) -> list[dict]:
    """Goal notes: the goals domain, plus any vault note named `*-goal` —
    weight-goal lives in health/ because placement follows artifact class,
    but it is still a goal and the planning view should see it."""
    vault = root / "projects"
    paths: list[Path] = []
    goals_dir = vault / "goals"
    if goals_dir.is_dir():
        paths += [p for p in sorted(goals_dir.glob("*.md")) if p.stem != "CONTEXT"]
    for path in sorted(vault.rglob("*-goal.md")):
        if ".obsidian" not in path.parts and path not in paths:
            paths.append(path)

    goals = []
    for path in paths:
        text = read(path)
        goals.append(
            {
                "slug": path.stem,
                "title": title(text, path.stem),
                "domain": path.relative_to(vault).parts[0],
                "summary": truncate(strip_markdown(first_paragraph(text)), 320),
                "open": section_bullets(text, "## Open"),
                "links": sorted(set(WIKILINK.findall(text)))[:10],
                "updated": datetime.fromtimestamp(path.stat().st_mtime).date().isoformat(),
                "path": str(path.relative_to(root)),
            }
        )
    return goals


# --- backup freshness ---------------------------------------------------------

# Hours since the last successful backup before the console starts complaining.
# The warning threshold sits just past a day so a nightly job that slips an hour
# is not an alarm; the critical one at two days means a whole run was missed.
BACKUP_WARN_HOURS = 26
BACKUP_CRITICAL_HOURS = 48


def scan_backup() -> dict:
    """How long since a backup last *succeeded*, from a status file it writes.

    Off unless `WORKSPACE_BACKUP_STATUS` names a readable file of `key=value`
    lines including `last_success`. Deliberately generic: the job that writes it
    lives outside this repo, and the console's only question is how stale the
    last success is.

    Age-of-last-success is the right question rather than last-run-exit-code,
    because it is the only form that also catches a run which **never started**
    — a job that does not run cannot report that it did not run, so the reader
    has to judge freshness rather than the writer.
    """
    location = os.environ.get("WORKSPACE_BACKUP_STATUS", "").strip()
    if not location:
        return {}

    path = Path(location)
    if not path.is_file():
        return {"state": "unreadable", "path": location}

    fields: dict[str, str] = {}
    for line in read(path).splitlines():
        key, sep, value = line.partition("=")
        if sep and value.strip():
            fields[key.strip()] = value.strip()

    status: dict = {
        "path": location,
        "last_run": fields.get("last_run", ""),
        "last_result": fields.get("last_result", ""),
        "last_success": fields.get("last_success", ""),
    }

    if not status["last_success"]:
        status["state"] = "never"
        return status

    try:
        succeeded = datetime.fromisoformat(status["last_success"])
    except ValueError:
        status["state"] = "unreadable"
        return status
    if succeeded.tzinfo is None:
        succeeded = succeeded.astimezone()

    hours = (datetime.now(timezone.utc) - succeeded).total_seconds() / 3600
    status["age_hours"] = round(hours, 1)
    status["state"] = (
        "critical" if hours >= BACKUP_CRITICAL_HOURS
        else "stale" if hours >= BACKUP_WARN_HOURS
        else "fresh"
    )
    return status


def describe_age(hours: float) -> str:
    if hours < 48:
        return f"{round(hours)} hours ago"
    return f"{round(hours / 24)} days ago"


# --- inbox and open questions -------------------------------------------------


def scan_inbox(root: Path) -> list[dict]:
    """What is sitting in the capture inbox, waiting for /pkm-triage."""
    directory = root / "projects" / "pkm" / "inbox"
    if not directory.is_dir():
        return []
    items = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        text = read(path)
        fields = frontmatter(text)
        items.append(
            {
                "slug": path.stem,
                "title": title(text, path.stem),
                "captured": fields.get("captured", ""),
                "source": fields.get("source", ""),
                "why": fields.get("why", ""),
                "path": str(path.relative_to(root)),
            }
        )
    return items


def build_questions(data: dict) -> list[dict]:
    """Every open question the workspace is carrying, with enough provenance
    that an answer can be captured against it: goal notes' ## Open bullets and
    the ## Question of every unresolved ticket."""
    questions: list[dict] = []
    for goal in data["goals"]:
        for i, text in enumerate(goal["open"]):
            questions.append(
                {
                    "id": f"goal:{goal['slug']}:{i}",
                    "kind": "goal",
                    "origin": goal["title"],
                    "path": goal["path"],
                    "text": text,
                }
            )
    for ticket in data["tickets"]:
        if ticket["status"] == "resolved" or not ticket["question"]:
            continue
        questions.append(
            {
                "id": f"ticket:{ticket['id']}",
                "kind": "ticket",
                "origin": ticket["title"],
                "path": ticket["path"],
                "text": ticket["question"],
            }
        )
    return questions


# --- entry point ------------------------------------------------------------


def reconcile(data: dict) -> None:
    """Let an initiative's own status override its effort's inferred state.

    Ticket counts alone can't tell parked from stalled, or a closed effort from
    an abandoned one — the initiative note is where that decision is recorded.
    """
    by_slug = {i["slug"]: i for i in data["initiatives"]}
    for effort in data["efforts"]:
        initiative = by_slug.get(effort["slug"])
        effort["initiative"] = effort["slug"] if initiative else ""
        if not initiative:
            continue
        if initiative["status"] == "paused":
            effort["state"] = "parked"
        elif initiative["status"] == "done":
            effort["state"] = "closed"


def scan(root: Path) -> dict:
    data: dict = {
        "workspace": root.name,
        "root": str(root),
        "scanned_at": datetime.now().isoformat(timespec="seconds"),
        "efforts": scan_efforts(root),
        "initiatives": scan_initiatives(root),
        "workspace_backlog": scan_backlog(root, ".scratch/backlog.md", "Workspace"),
        "initiatives_backlog": scan_backlog(
            root, "projects/initiatives/backlog.md", "Initiatives"
        ),
        "skills": scan_skills(root),
        "agents": scan_agents(root),
        "guardrails": scan_guardrails(root),
        "domains": scan_domains(root),
        "pkm": scan_pkm(root),
        "graph": scan_graph(root),
        "media": scan_media(root),
        "goals": scan_goals(root),
        "learning": scan_learning(root),
        "registry": scan_registry(root),
        "publish": scan_publish(root),
        "index_coverage": scan_index_coverage(root),
        "adrs": scan_adrs(root),
        "git": scan_git(root),
        "backup": scan_backup(),
    }
    reconcile(data)
    data["attention"] = build_attention(data)
    data["tickets"] = [t for effort in data["efforts"] for t in effort["tickets"]]
    data["inbox_items"] = scan_inbox(root)
    data["questions"] = build_questions(data)
    return data
