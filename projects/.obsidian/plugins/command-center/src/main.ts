import {
  App,
  FileSystemAdapter,
  ItemView,
  Notice,
  Plugin,
  TFile,
  WorkspaceLeaf,
} from "obsidian";
import { spawn } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";

export const VIEW_TYPE = "command-center-view";

/* ------------------------------------------------------------------ *
 * Scope
 *
 * A launcher, and deliberately nothing more. Metrics over this workspace
 * already belong to the Workspace Console (tools/dashboard/), which reads the
 * same files and does it better; duplicating its counts here would create a
 * second renderer of one truth for no gain. What nothing else offers is
 * starting a skill without leaving Obsidian, so that is all this does.
 *
 * `gated` marks a skill that must not run headlessly. This workspace's trust
 * boundary is that nothing enters projects/pkm/notes/ without Jonah's
 * approval, and a headless run would answer its own approval prompt. Every
 * launch therefore opens an interactive terminal rather than capturing output
 * — the button saves the typing, never the judgement.
 * ------------------------------------------------------------------ */

interface Skill {
  invocation: string;
  label: string;
  blurb: string;
  gated: boolean;
}

/**
 * Skills that write into the approval-gated notes tree.
 *
 * This one stays hand-written, and the distinction matters: the *list* of
 * skills is an enumeration a directory read can produce, but which of them
 * cross a trust boundary is a judgement no frontmatter records. Hard-coding
 * the first would drift; hard-coding the second is just where the judgement
 * lives.
 */
const GATED = new Set(["pkm-triage", "wiki-ingest"]);

const titleCase = (slug: string): string =>
  slug.replace(/-/g, " ").replace(/^./, (c) => c.toUpperCase());

/**
 * Read the skills off disk rather than listing them here.
 *
 * `systems/CONTEXT.md` states the rule this follows: "enumerations that a
 * command can produce are never hand-maintained." A hard-coded array goes
 * stale the first time a skill is added or removed, and it goes stale
 * silently — the button simply describes something that no longer exists.
 */
function readSkills(root: string): Skill[] {
  const dir = join(root, ".claude", "skills");
  let entries: string[];
  try {
    entries = readdirSync(dir);
  } catch {
    return [];
  }

  const skills: Skill[] = [];
  for (const slug of entries.sort()) {
    let text: string;
    try {
      text = readFileSync(join(dir, slug, "SKILL.md"), "utf8");
    } catch {
      continue; // not a skill directory
    }
    const front = /^---\n([\s\S]*?)\n---/.exec(text);
    const field = (key: string): string =>
      new RegExp(`^${key}:\\s*(.+)$`, "m").exec(front?.[1] ?? "")?.[1]?.trim() ?? "";

    const name = field("name") || slug;
    const description = field("description");
    skills.push({
      invocation: `/${name}`,
      label: titleCase(name),
      // First sentence only — descriptions are written for skill matching and
      // run long, which a sidebar row cannot carry.
      blurb: description.split(/\.\s/)[0].replace(/\.$/, ""),
      gated: GATED.has(name),
    });
  }
  return skills;
}

/** The console's serve mode; it opens a browser itself. */
const CONSOLE_CMD = "python3 tools/dashboard/build.py --serve";

/* ------------------------------------------------------------------ *
 * Launching
 * ------------------------------------------------------------------ */

/** Escape for embedding inside an AppleScript double-quoted string literal. */
function appleScriptString(value: string): string {
  return '"' + value.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
}

/** Escape for embedding inside a POSIX single-quoted shell word. */
function shellQuote(value: string): string {
  return "'" + value.replace(/'/g, `'\\''`) + "'";
}

/**
 * Resolve the workspace root — the vault root is `projects/`, but `.claude/`
 * and `tools/` live one level above it, so anything invoked here has to start
 * from the parent rather than from the vault.
 */
function workspaceRoot(app: App): string | null {
  const adapter = app.vault.adapter;
  if (!(adapter instanceof FileSystemAdapter)) return null;
  return dirname(adapter.getBasePath());
}

function runInTerminal(app: App, command: string, announce: string): void {
  const root = workspaceRoot(app);
  if (!root) {
    new Notice("Command Center: cannot resolve the vault path.");
    return;
  }

  const shellCmd = `cd ${shellQuote(root)} && ${command}`;
  const osa = [
    'tell application "Terminal"',
    "  activate",
    `  do script ${appleScriptString(shellCmd)}`,
    "end tell",
  ].join("\n");

  const child = spawn("osascript", ["-e", osa], { detached: true, stdio: "ignore" });
  child.on("error", (err) => new Notice(`Command Center: launch failed — ${err.message}`));
  child.unref();

  new Notice(announce);
}

/* ------------------------------------------------------------------ *
 * View
 * ------------------------------------------------------------------ */

export class CommandCenterView extends ItemView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE;
  }

  getDisplayText(): string {
    return "Command Center";
  }

  getIcon(): string {
    return "terminal";
  }

  async onOpen(): Promise<void> {
    const root = this.contentEl;
    root.empty();
    root.addClass("cc-root");

    const header = root.createDiv({ cls: "cc-header" });
    header.createEl("h2", { text: "Command Center", cls: "cc-title" });
    header.createEl("div", {
      text: "Each skill opens an interactive terminal — approval prompts stay yours to answer.",
      cls: "cc-subtitle",
    });

    const base = workspaceRoot(this.app);
    const skills = base ? readSkills(base) : [];

    if (!skills.length) {
      root.createDiv({ cls: "cc-empty", text: "No skills found in .claude/skills/." });
    }

    const list = root.createDiv({ cls: "cc-skills" });
    for (const skill of skills) {
      const row = list.createDiv({ cls: "cc-skill" });

      const text = row.createDiv({ cls: "cc-skill-text" });
      const name = text.createDiv({ cls: "cc-skill-name" });
      name.createSpan({ text: skill.label });
      if (skill.gated) {
        name.createSpan({
          text: "gated",
          cls: "cc-badge",
          title: "Writes into the approval-gated notes tree",
        });
      }
      text.createDiv({ text: skill.blurb, cls: "cc-skill-blurb" });

      const btn = row.createEl("button", { text: "Run", cls: "cc-run" });
      btn.addEventListener("click", () =>
        runInTerminal(this.app, `claude ${shellQuote(skill.invocation)}`, `Opened a terminal for ${skill.invocation}`),
      );
    }

    const footer = root.createDiv({ cls: "cc-footer" });

    const consoleBtn = footer.createEl("button", { text: "Open Workspace Console", cls: "cc-secondary" });
    consoleBtn.addEventListener("click", () =>
      runInTerminal(this.app, CONSOLE_CMD, "Starting the Workspace Console…"),
    );

    const homeBtn = footer.createEl("button", { text: "Open Home.md", cls: "cc-secondary" });
    homeBtn.addEventListener("click", () => this.openHome());
  }

  private async openHome(): Promise<void> {
    const file = this.app.vault.getAbstractFileByPath("Home.md");
    if (file instanceof TFile) {
      await this.app.workspace.getLeaf(true).openFile(file);
    } else {
      new Notice("Command Center: Home.md not found at the vault root.");
    }
  }
}

/* ------------------------------------------------------------------ *
 * Plugin
 * ------------------------------------------------------------------ */

export default class CommandCenterPlugin extends Plugin {
  async onload(): Promise<void> {
    this.registerView(VIEW_TYPE, (leaf) => new CommandCenterView(leaf));

    this.addRibbonIcon("terminal", "Command Center", () => this.activate());

    this.addCommand({
      id: "open-command-center",
      name: "Open Command Center",
      callback: () => this.activate(),
    });

    // Each skill also gets a palette entry, which is faster than the sidebar
    // once you know the name. Read once at load: Obsidian fixes the command
    // list at registration, so a skill added later appears on next reload.
    const base = workspaceRoot(this.app);
    for (const skill of base ? readSkills(base) : []) {
      this.addCommand({
        id: `run${skill.invocation.replace(/\//g, "-")}`,
        name: `Run ${skill.invocation}`,
        callback: () =>
          runInTerminal(this.app, `claude ${shellQuote(skill.invocation)}`, `Opened a terminal for ${skill.invocation}`),
      });
    }
  }

  async activate(): Promise<void> {
    const { workspace } = this.app;

    const existing = workspace.getLeavesOfType(VIEW_TYPE);
    if (existing.length > 0) {
      workspace.revealLeaf(existing[0]);
      return;
    }

    const leaf = workspace.getRightLeaf(false);
    if (!leaf) return;
    await leaf.setViewState({ type: VIEW_TYPE, active: true });
    workspace.revealLeaf(leaf);
  }
}
