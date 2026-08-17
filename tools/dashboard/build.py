#!/usr/bin/env python3
"""Build — or serve — the workspace dashboard.

    python3 tools/dashboard/build.py            # write dist/index.html
    python3 tools/dashboard/build.py --serve    # live at http://localhost:8787
    python3 tools/dashboard/build.py --open     # build, then open it

In `--serve` mode the workspace is re-scanned on every data request, so the page
tracks the files as they change. A plain build inlines a snapshot instead, which
is what makes the output a single portable file with no server behind it.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scan import scan  # noqa: E402

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
TEMPLATE = HERE / "template.html"
OUTPUT = HERE / "dist" / "index.html"

# Set by main() before the server starts. Read-only is for serving a synced
# copy of the workspace that must not be written — the homelab's Syncthing
# mirror is receive-only by design, and a capture written there would be
# fighting the sync topology instead of joining it.
READ_ONLY = False

# What the fingerprint watches — the same ground the scan reads. Walking mtimes
# is ~100× cheaper than a full scan, which is what lets the page ask "anything
# new?" every couple of seconds without the server re-reading the workspace.
WATCHED = (".scratch", "projects", ".claude", "docs", "registry", ".git")


def fingerprint() -> str:
    stamp = 0.0
    count = 0
    for name in WATCHED:
        base = ROOT / name
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if ".obsidian" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                if path.is_file():
                    stamp = max(stamp, path.stat().st_mtime)
                    count += 1
            except OSError:
                continue
    return f"{stamp:.0f}-{count}"


def render(live: bool) -> str:
    data = dict(scan(ROOT))
    if live:
        # Ship the fingerprint with the page so the first /api/version probe
        # compares against reality instead of always triggering a refetch.
        data["version"] = fingerprint()
        data["writable"] = not READ_ONLY
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> inside the data would close the tag early.
    payload = payload.replace("</", "<\\/")
    return (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("/*__DATA__*/null", payload)
        .replace("/*__LIVE__*/false", "true" if live else "false")
    )


def build(open_after: bool) -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(live=False), encoding="utf-8")
    size = OUTPUT.stat().st_size / 1024
    print(f"built {OUTPUT.relative_to(ROOT)} ({size:.0f} KB)")
    if open_after:
        subprocess.run(["open", str(OUTPUT)], check=False)
    return OUTPUT


INBOX = ROOT / "projects" / "pkm" / "inbox"


def slugify(text: str, fallback: str = "note") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60].rstrip("-") or fallback


def capture_file(payload: dict) -> Path:
    """Write one capture into the PKM inbox, in the documented format.

    This is the console's only write, and it lands in the one directory whose
    whole purpose is receiving raw material — promotion into notes/ still
    belongs to /pkm-triage. Answers name their question and its source file so
    triage can fold them back where they came from.
    """
    today = date.today().isoformat()
    answer = payload.get("answer", "").strip()
    if not answer:
        raise ValueError("empty answer")

    question = payload.get("question", "").strip()
    origin = payload.get("origin", "").strip()
    source_path = payload.get("path", "").strip()

    if question:
        slug = f"answer-{slugify(origin or question)}"
        why = (
            f"Jonah answered an open question from {origin or source_path} in the "
            "workspace console; the source file still carries it as open."
        )
        body_lines = [
            f"# Answer: {origin}" if origin else "# Answer",
            "",
            f"**The question** (from `{source_path}`): {question}" if source_path
            else f"**The question:** {question}",
            "",
            f"**Jonah's answer ({today}):**",
            "",
            answer,
            "",
            f"**Proposed routing:** fold into `{source_path}` at triage."
            if source_path else "",
        ]
    else:
        slug = slugify(answer.splitlines()[0])
        why = "Jonah captured this himself from the workspace console."
        body_lines = [answer]

    text = (
        "---\n"
        f"captured: {today}\n"
        "source: workspace console — submitted from the dashboard\n"
        f"why: {why}\n"
        "---\n\n"
        + "\n".join(body_lines).strip()
        + "\n"
    )

    INBOX.mkdir(parents=True, exist_ok=True)
    path = INBOX / f"{today}-{slug}.md"
    counter = 2
    while path.exists():
        path = INBOX / f"{today}-{slug}-{counter}.md"
        counter += 1
    path.write_text(text, encoding="utf-8")
    return path


# ─── the second write path ───────────────────────────────────────────────
#
# The console's first write was /api/capture, which only ever *adds* a file to
# the inbox. This one edits an existing note, so it is fenced considerably
# harder. Three rules, in order of how much damage skipping them would do:
#
#   1. Never write inside projects/pkm/notes/. That tree is human-gated —
#      a note being there means Jonah approved it — and a dashboard toggle is
#      not approval. /pkm-triage owns that boundary and keeps owning it.
#   2. Only a known key, only a known value. This endpoint exists to move a
#      status between states the domains already define; it is not a general
#      file editor reachable over HTTP.
#   3. Only inside the workspace, only markdown, and only where frontmatter
#      already exists. Writing frontmatter into a file that had none would be
#      inventing a schema for a domain that has deliberately not earned one.

WRITABLE_KEYS = {"status"}

# The union of what learning/ and initiatives/ actually use. `unknown` is in
# the corpus (imported assignments whose completion state was never recorded)
# so it has to be settable back to, not just away from.
WRITABLE_VALUES = {
    "status": {"active", "completed", "planned", "paused", "done", "not started", "unknown"},
}

GATED_TREE = "projects/pkm/notes"

FRONTMATTER_BLOCK = re.compile(r"\A---\n(.*?)\n---(\r?\n|\Z)", re.DOTALL)


def set_frontmatter(payload: dict) -> tuple[str, str, str]:
    """Set one frontmatter key on one note. Returns (path, key, value)."""
    raw_path = str(payload.get("path", "")).strip()
    key = str(payload.get("key", "")).strip()
    value = str(payload.get("value", "")).strip()

    if key not in WRITABLE_KEYS:
        raise ValueError(f"key not writable: {key!r}")
    if value not in WRITABLE_VALUES[key]:
        raise ValueError(f"value not allowed for {key}: {value!r}")
    if not raw_path.endswith(".md"):
        raise ValueError("only markdown notes can be edited")

    target = (ROOT / raw_path).resolve()
    try:
        relative = target.relative_to(ROOT.resolve())
    except ValueError:
        raise ValueError("path escapes the workspace") from None
    if not target.is_file():
        raise ValueError(f"no such note: {relative}")
    if relative.as_posix().startswith(GATED_TREE):
        raise ValueError(
            "projects/pkm/notes/ is human-gated — promotion belongs to /pkm-triage, "
            "not to a dashboard control"
        )

    text = target.read_text(encoding="utf-8")
    match = FRONTMATTER_BLOCK.match(text)
    if not match:
        raise ValueError(f"{relative} has no frontmatter to edit")

    block = match.group(1)
    line = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if line.search(block):
        updated = line.sub(f"{key}: {value}", block, count=1)
    else:
        updated = f"{block}\n{key}: {value}"

    # Rebuild rather than reformat: everything outside the one line, including
    # the body and every other field, is carried across untouched.
    target.write_text(text[: match.start(1)] + updated + text[match.end(1):], encoding="utf-8")
    return relative.as_posix(), key, value


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 — required by BaseHTTPRequestHandler
        if self.path.startswith("/api/version"):
            # Cheap change probe: the page polls this every couple of seconds
            # and only pulls a full re-scan when the fingerprint moves.
            self.send(200, "application/json", json.dumps({"v": fingerprint()}))
        elif self.path.startswith("/api/data"):
            payload = dict(scan(ROOT))
            payload["version"] = fingerprint()
            payload["writable"] = not READ_ONLY
            self.send(200, "application/json", json.dumps(payload, ensure_ascii=False))
        elif self.path in ("/", "/index.html"):
            self.send(200, "text/html; charset=utf-8", render(live=True))
        else:
            self.send(404, "text/plain", "not found")

    def do_POST(self) -> None:  # noqa: N802 — required by BaseHTTPRequestHandler
        is_capture = self.path.startswith("/api/capture")
        is_frontmatter = self.path.startswith("/api/frontmatter")
        if not (is_capture or is_frontmatter):
            self.send(404, "application/json", json.dumps({"error": "not found"}))
            return
        if READ_ONLY:
            self.send(403, "application/json", json.dumps({"error":
                "read-only console — this copy of the vault is a one-way mirror. "
                "Capture from Obsidian on the phone, or answer from the Mac console."}))
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if is_capture:
                path = capture_file(payload)
                result = {"ok": True, "path": str(path.relative_to(ROOT))}
            else:
                path_str, key, value = set_frontmatter(payload)
                result = {"ok": True, "path": path_str, "key": key, "value": value}
        except (ValueError, json.JSONDecodeError) as error:
            self.send(400, "application/json", json.dumps({"error": str(error)}))
            return
        self.send(200, "application/json", json.dumps(result))

    def send(self, code: int, content_type: str, payload: str) -> None:
        encoded = payload.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args) -> None:  # quiet: one line per scan is enough
        pass


def serve(port: int, host: str = "127.0.0.1", open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{'localhost' if host in ('127.0.0.1', '0.0.0.0') else host}:{port}"
    mode = "read-only" if READ_ONLY else "read/write"
    print(f"dashboard live at {url} ({mode}; re-scans on change; ctrl-c to stop)")
    if open_browser and sys.platform == "darwin":
        subprocess.run(["open", url], check=False)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
        server.server_close()


def main() -> None:
    global READ_ONLY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true", help="run the live server")
    parser.add_argument("--open", action="store_true", help="open the built file")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--host", default="127.0.0.1",
                        help="interface to bind (0.0.0.0 when a container maps the port)")
    parser.add_argument("--no-open", action="store_true", help="don't open a browser")
    parser.add_argument("--read-only", action="store_true",
                        help="serve without the capture endpoint — for a synced mirror "
                             "of the workspace that must not be written")
    parser.add_argument("--json", action="store_true", help="dump the scan and exit")
    args = parser.parse_args()
    READ_ONLY = args.read_only

    if args.json:
        print(json.dumps(scan(ROOT), indent=2, ensure_ascii=False))
    elif args.serve:
        serve(args.port, args.host, open_browser=not args.no_open)
    else:
        build(args.open)


if __name__ == "__main__":
    main()
