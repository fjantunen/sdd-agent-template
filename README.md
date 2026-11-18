# ⚡ Spec-Driven Development (SDD) Harness

Stop coding agents from drifting mid-feature with a lightweight, model-agnostic Spec → Plan → Execute → Verify loop.
Treats `.sdd/spec.md` as an executable contract, `.sdd/lessons.md` as repo memory, and `.sdd/state.json` as persistent disk state across sessions and tool switches.

## 🚀 Quick Start

### Option A: Brownfield (1-Line Skill Install)

Add the `sdd` skill to any existing repository (Claude Code, Cursor, Codex, Gemini, Antigravity):

```bash
npx skills add fjantunen/sdd-agent-template
```

Invoke it directly in your agent chat:

```text
Use the sdd skill to add rate limiting to /api/login
```

### Option B: Greenfield (GitHub Template)

1. Click **`Use this template`** on GitHub to create a new repository with [AGENTS.md](AGENTS.md), [.gemini/GEMINI.md](.gemini/GEMINI.md), [.sdd/lessons.md](.sdd/lessons.md), and [.agents/skills/sdd/SKILL.md](.agents/skills/sdd/SKILL.md) pre-wired.
2. Clone your repo and launch a feature or bug fix in your agent.

## 🗂️ Repo Layout

* **[AGENTS.md](AGENTS.md)** — Master system rules (auto-loaded by OpenAI Codex).
* **[.gemini/GEMINI.md](.gemini/GEMINI.md)** — Symlink to `AGENTS.md` (auto-loaded by Google Antigravity).
* **[.agents/skills/sdd/SKILL.md](.agents/skills/sdd/SKILL.md)** — Portable `agentskills.io` skill + [spec-template.md](.agents/skills/sdd/references/spec-template.md), [state-template.json](.agents/skills/sdd/references/state-template.json), and [skill-template.md](.agents/skills/sdd/references/skill-template.md).
* **[scripts/validate-skills.py](scripts/validate-skills.py)** — Validates skill frontmatter, line limits, JSON templates, symlinks, and relative links.
* **`.sdd/spec.md`** — Locked EARS requirements & `Out of Scope` fence (created per feature, git-tracked).
* **[.sdd/lessons.md](.sdd/lessons.md)** — Verified repo-specific gotchas & test quirks, `<= 30` lines (git-tracked).
* **`.sdd/state.json`** — Live track, `sdd_mode`, phase, persona, `acquired_skills[]`, task queue, & retry ledger (git-ignored).

## ✅ Execution Checklists

### Feature Track (Default: `gated`)
* [ ] **Launch** in repo root: `New feature: [describe feature]` (`gated` is default).
* [ ] **Triage:** Answer up to 3 questions if asked, or reply `skip`.
* [ ] **Approve Spec:** Inspect `.sdd/spec.md`, then reply `approve` to advance to `PLAN`.
* [ ] **Approve Plan:** Review `tasks[]` in `.sdd/state.json`, then reply `approve` to unlock `EXECUTE -> VERIFY -> DONE`. *(Skipped in `--yolo` mode.)*
* [ ] **Verify Commits:** Passing tasks auto-commit locally as `feat(<id>): <T_id> <desc>` (plus `.sdd/lessons.md` / `.agents/skills/` if updated). Never pushes remotely.

### Bug-Fix Fast Path (`--fix`)
* [ ] **Launch** with `--fix`: `Fix: [describe bug] --fix`
* [ ] **Diagnose:** `BUILDER` reproduces the bug with a failing test (`DIAGNOSE`), skipping `SPECIFY` and `PLAN`.
* [ ] **Fix & Verify:** `BUILDER` fixes it (`EXECUTE`), isolated `VERIFIER` audits the diff/test (`VERIFY`), and commits `fix(<id>): <T_id> <desc>`.

## 🎛️ Flags & Modes: Gated vs. YOLO

Both modes write `.sdd/spec.md` and `.sdd/state.json` (`tasks[]`) to disk for auditability and lean context—`yolo` skips human wait-gates, not the specs themselves.

| Flag / Command | Behavior | Best For |
| :--- | :--- | :--- |
| `--gated` / `mode: gated` | **(Default)** Pauses after **both** `SPECIFY` and `PLAN` for explicit `approve` | High-control & unfamiliar repos |
| `--yolo` / `mode: yolo` / `"yolo mode"` | Auto-generates Spec, Plan, & Tasks in one pass, executes end-to-end, and only pauses on a hard blocker or failing test after 2 attempts | Well-defined features & fast iteration |
| `--fix` | Sets `track: "FIX"`; runs `DIAGNOSE -> EXECUTE -> VERIFY -> DONE` | Bug fixes with a repro test |
| `--allow-skills` | Allows pre-vetted `npx skills add` installs in `yolo` mode | Automated skill acquisition |
| `approve` | Advances past a `SPECIFY` or `PLAN` gate | Confirming specs/tasks |
| `skip` | Bypasses `TRIAGE` questions using defaults | Fast starts |

**Copy-paste prompt examples:**

```text
# Gated Mode (default) — review spec & plan before code is written
New feature: Add JWT refresh token rotation with tests
```

```text
# YOLO Mode — write spec & tasks to disk, then execute & verify end-to-end
New feature: Add JWT refresh token rotation with tests --yolo
```

## 🧠 Recommended Model Routing

* **Workhorse (`BUILDER` + `VERIFIER`):**
  * **Antigravity:** `Gemini 4 Hydrogen`
  * **Codex:** `GPT-6.1 Sol`
  * **Anthropic:** `Claude Sonnet 5.5`
* **Heavy Architecture (`SPECIFIER` + `ARCHITECT`):**
  * **Antigravity:** `Gemini 4 Carbon`
  * **Codex:** `GPT-6.1 Terra`
  * **Anthropic:** `Claude Opus 5.5`
* **Cross-Tool Handoffs:** Start a spec in Antigravity, close it, and type `approve` in Codex (or vice versa)—state persists on disk.

## 🔀 Parallel Features (Git Worktrees)

Keep **1 active feature per working directory**. Use a Git Worktree for concurrent work:

```bash
git worktree add ../repo-feat-b -b feat/second-feature
git worktree remove ../repo-feat-b
```

## 🛡️ Security & Skill Guardrails

* **Secrets Shield:** `.env*` (allowing `!.env.example`), `*.pem`, `*.key`, and `*credentials*.json` are git-ignored in [.gitignore](.gitignore) and never read, printed, or staged.
* **Supply-Chain Gate:** Unapproved package installs (`npm install`, `pip install`, `cargo add`, `go get`), `npx skills add`, and `curl | sh` hard-halt unless explicitly approved in `.sdd/spec.md` (or `sdd_skill_allowlist` / `--allow-skills` for skills).
* **Skill Acquisition & Crystallization:** `TRIAGE` scans only skill frontmatter (`name`, `description`) to keep context lean; reusable workflows (`retry_count >= 1` or `.sdd/lessons.md > 25` lines) auto-crystallize into `.agents/skills/<name>/SKILL.md` after `VERIFIER` audit.
* **Diff Secret Check:** `VERIFIER` immediately `FAIL`s any `git diff` containing hardcoded secrets, tokens, or sensitive credential files before local commit.

## ♻️ Reusing in New Repositories

Install as a skill (`npx skills add fjantunen/sdd-agent-template`), use the GitHub template, or copy `AGENTS.md` into any project root (the harness auto-creates `.gemini/GEMINI.md`, `.sdd/`, `.sdd/lessons.md`, and `.gitignore` rules on first turn):

```bash
cp path/to/AGENTS.md ./AGENTS.md && git init && git add AGENTS.md && git commit -m "chore: add SDD harness"
```
