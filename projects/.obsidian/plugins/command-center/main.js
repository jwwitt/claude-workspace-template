"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  CommandCenterView: () => CommandCenterView,
  VIEW_TYPE: () => VIEW_TYPE,
  default: () => CommandCenterPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian = require("obsidian");
var import_node_child_process = require("node:child_process");
var import_node_fs = require("node:fs");
var import_node_path = require("node:path");
var VIEW_TYPE = "command-center-view";
var GATED = /* @__PURE__ */ new Set(["pkm-triage", "wiki-ingest"]);
var titleCase = (slug) => slug.replace(/-/g, " ").replace(/^./, (c) => c.toUpperCase());
function readSkills(root) {
  const dir = (0, import_node_path.join)(root, ".claude", "skills");
  let entries;
  try {
    entries = (0, import_node_fs.readdirSync)(dir);
  } catch {
    return [];
  }
  const skills = [];
  for (const slug of entries.sort()) {
    let text;
    try {
      text = (0, import_node_fs.readFileSync)((0, import_node_path.join)(dir, slug, "SKILL.md"), "utf8");
    } catch {
      continue;
    }
    const front = /^---\n([\s\S]*?)\n---/.exec(text);
    const field = (key) => new RegExp(`^${key}:\\s*(.+)$`, "m").exec(front?.[1] ?? "")?.[1]?.trim() ?? "";
    const name = field("name") || slug;
    const description = field("description");
    skills.push({
      invocation: `/${name}`,
      label: titleCase(name),
      // First sentence only — descriptions are written for skill matching and
      // run long, which a sidebar row cannot carry.
      blurb: description.split(/\.\s/)[0].replace(/\.$/, ""),
      gated: GATED.has(name)
    });
  }
  return skills;
}
var CONSOLE_CMD = "python3 tools/dashboard/build.py --serve";
function appleScriptString(value) {
  return '"' + value.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
}
function shellQuote(value) {
  return "'" + value.replace(/'/g, `'\\''`) + "'";
}
function workspaceRoot(app) {
  const adapter = app.vault.adapter;
  if (!(adapter instanceof import_obsidian.FileSystemAdapter)) return null;
  return (0, import_node_path.dirname)(adapter.getBasePath());
}
function runInTerminal(app, command, announce) {
  const root = workspaceRoot(app);
  if (!root) {
    new import_obsidian.Notice("Command Center: cannot resolve the vault path.");
    return;
  }
  const shellCmd = `cd ${shellQuote(root)} && ${command}`;
  const osa = [
    'tell application "Terminal"',
    "  activate",
    `  do script ${appleScriptString(shellCmd)}`,
    "end tell"
  ].join("\n");
  const child = (0, import_node_child_process.spawn)("osascript", ["-e", osa], { detached: true, stdio: "ignore" });
  child.on("error", (err) => new import_obsidian.Notice(`Command Center: launch failed \u2014 ${err.message}`));
  child.unref();
  new import_obsidian.Notice(announce);
}
var CommandCenterView = class extends import_obsidian.ItemView {
  constructor(leaf) {
    super(leaf);
  }
  getViewType() {
    return VIEW_TYPE;
  }
  getDisplayText() {
    return "Command Center";
  }
  getIcon() {
    return "terminal";
  }
  async onOpen() {
    const root = this.contentEl;
    root.empty();
    root.addClass("cc-root");
    const header = root.createDiv({ cls: "cc-header" });
    header.createEl("h2", { text: "Command Center", cls: "cc-title" });
    header.createEl("div", {
      text: "Each skill opens an interactive terminal \u2014 approval prompts stay yours to answer.",
      cls: "cc-subtitle"
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
          title: "Writes into the approval-gated notes tree"
        });
      }
      text.createDiv({ text: skill.blurb, cls: "cc-skill-blurb" });
      const btn = row.createEl("button", { text: "Run", cls: "cc-run" });
      btn.addEventListener(
        "click",
        () => runInTerminal(this.app, `claude ${shellQuote(skill.invocation)}`, `Opened a terminal for ${skill.invocation}`)
      );
    }
    const footer = root.createDiv({ cls: "cc-footer" });
    const consoleBtn = footer.createEl("button", { text: "Open Workspace Console", cls: "cc-secondary" });
    consoleBtn.addEventListener(
      "click",
      () => runInTerminal(this.app, CONSOLE_CMD, "Starting the Workspace Console\u2026")
    );
    const homeBtn = footer.createEl("button", { text: "Open Home.md", cls: "cc-secondary" });
    homeBtn.addEventListener("click", () => this.openHome());
  }
  async openHome() {
    const file = this.app.vault.getAbstractFileByPath("Home.md");
    if (file instanceof import_obsidian.TFile) {
      await this.app.workspace.getLeaf(true).openFile(file);
    } else {
      new import_obsidian.Notice("Command Center: Home.md not found at the vault root.");
    }
  }
};
var CommandCenterPlugin = class extends import_obsidian.Plugin {
  async onload() {
    this.registerView(VIEW_TYPE, (leaf) => new CommandCenterView(leaf));
    this.addRibbonIcon("terminal", "Command Center", () => this.activate());
    this.addCommand({
      id: "open-command-center",
      name: "Open Command Center",
      callback: () => this.activate()
    });
    const base = workspaceRoot(this.app);
    for (const skill of base ? readSkills(base) : []) {
      this.addCommand({
        id: `run${skill.invocation.replace(/\//g, "-")}`,
        name: `Run ${skill.invocation}`,
        callback: () => runInTerminal(this.app, `claude ${shellQuote(skill.invocation)}`, `Opened a terminal for ${skill.invocation}`)
      });
    }
  }
  async activate() {
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
};
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  CommandCenterView,
  VIEW_TYPE
});
