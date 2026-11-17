# ⚡ `sdd-agent-template` — Spec-Driven Development Harness

Stop coding agents from drifting mid-feature with a file-backed Spec → Plan → Execute → Verify loop.
Keeps `.sdd/spec.md`, `.sdd/lessons.md`, and `.sdd/state.json` on disk so context stays lean and cross-agent handoffs stay deterministic.

---

## 🚀 Quick Start

### Option A: Brownfield (1-Line Skill Install)

Add the `sdd` skill to any existing repository (works with Claude Code, Cursor, Codex, Gemini, and Antigravity):

```bash
npx skills add fjantunen/sdd-agent-template
```

Invoke it directly in your agent chat:

```text
Use the sdd skill to add rate limiting to /api/login
```

### Option B: Greenfield (GitHub Template)

1. Click **`Use this template`** on GitHub to create a new repository with [AGENTS.md](AGENTS.md), [.gemini/GEMINI.md](.gemini/GEMINI.md), [.sdd/lessons.md](.sdd/lessons.md), and [.agents/skills/sdd/SKILL.md](.agents/skills/sdd/SKILL.md) pre-wired.
2. Clone your repo and start a feature or bug fix in your agent:
   - **Feature:** `New feature: [describe feature]`
   - **Bug Fix (`--fix`):** `Fix: [describe bug] --fix` *(skips Spec/Plan; runs `DIAGNOSE -> EXECUTE -> VERIFY -> DONE`)*

---

## 🎛️ Execution Modes: Gated vs. YOLO

Both modes write `.sdd/spec.md` and `.sdd/state.json` (`tasks[]`) to disk for auditability and lean context.

| Mode | Trigger | Behavior |
| :--- | :--- | :--- |
| **Gated Mode** *(Default)* | Default, `--gated`, `mode: gated` | Pauses after **Spec** (`SPECIFY`) and **Plan** (`PLAN`) for explicit `approve` before writing code. |
| **YOLO Mode** | `--yolo`, `"yolo mode"`, or `sdd_mode: yolo` in config/frontmatter | Auto-generates Spec, Plan, and Task breakdown in one pass, executes all tasks end-to-end, runs tests/verification, and only pauses on a hard blocker or failing test after 2 attempts. |

**Copy-paste prompt examples:**

```text
# Gated Mode (default) — review spec & plan before code is written
New feature: Add JWT refresh token rotation with tests
```

```text
# YOLO Mode — write spec & tasks to disk, then execute & verify end-to-end
New feature: Add JWT refresh token rotation with tests --yolo
```

---

## 🗂️ Repo Layout

* **[AGENTS.md](AGENTS.md)** — Master harness rules (auto-loaded by OpenAI Codex).
* **[.gemini/GEMINI.md](.gemini/GEMINI.md)** — Symlink to `AGENTS.md` (auto-loaded by Google Antigravity).
* **[.agents/skills/sdd/SKILL.md](.agents/skills/sdd/SKILL.md)** — Portable `agentskills.io` skill + [spec-template.md](.agents/skills/sdd/references/spec-template.md) and [state-template.json](.agents/skills/sdd/references/state-template.json).
* **[.sdd/lessons.md](.sdd/lessons.md)** — Verified repo-specific gotchas & test quirks, `<= 30` lines (git-tracked).
* **`.sdd/spec.md`** — Locked EARS requirements & `Out of Scope` fence (created per feature, git-tracked).
* **`.sdd/state.json`** — Live track, `sdd_mode`, phase, persona, task queue, & retry ledger (git-ignored).

## 🛡️ Security & Hygiene

* **Secrets Shield:** `.env*` (allowing `!.env.example`), `*.pem`, `*.key`, and `*credentials*.json` are git-ignored in [.gitignore](.gitignore) and never read, printed, or staged.
* **Supply-Chain Gate:** Unapproved package installs (`npm install`, `pip install`, `cargo add`, `go get`) and `curl | sh` hard-halt unless explicitly approved in `.sdd/spec.md`.
* **Diff Secret Check:** `VERIFIER` immediately `FAIL`s any `git diff` containing hardcoded secrets, tokens, or sensitive credential files before local commit (`git push` is never run automatically).
