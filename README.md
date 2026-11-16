# ⚡ Spec-Driven Development (SDD) Harness

A lightweight, model-agnostic execution loop for **Google Antigravity** (CLI & Desktop IDE) and **OpenAI Codex** (CLI & Desktop App). Treats `.sdd/spec.md` as an executable contract, `.sdd/lessons.md` as repo memory, and `.sdd/state.json` as persistent disk state across sessions and tool switches.

## 🗂️ Repo Layout

* **`AGENTS.md`** — Master system rules (auto-loaded by OpenAI Codex).
* **`.gemini/GEMINI.md`** — Symlink to `AGENTS.md` (auto-loaded by Google Antigravity).
* **`.sdd/spec.md`** — Locked requirements & `Out of Scope` fence (git-tracked).
* **`.sdd/lessons.md`** — Verified repo-specific gotchas & test quirks, `<= 30` lines (git-tracked).
* **`.sdd/state.json`** — Live track, phase, persona, task queue, & retry ledger (git-ignored).

## ✅ Execution Checklists

### Feature Track (Default: `--spec-only`)
* [ ] **Launch** in repo root: `New feature: [describe feature]` (`--spec-only` is default).
* [ ] **Triage:** Answer up to 3 questions if asked, or reply `skip`.
* [ ] **Approve Spec:** Inspect `.sdd/spec.md`, then reply `approve` to unlock `PLAN -> EXECUTE -> VERIFY -> DONE`.
* [ ] *(Only with `--gate-all`)* Review `tasks[]` in `.sdd/state.json` and reply `approve` again.
* [ ] **Verify Commits:** Passing tasks auto-commit locally as `feat(<id>): <T_id> <desc>` (plus `.sdd/lessons.md` if updated). Never pushes remotely.

### Bug-Fix Fast Path (`--fix`)
* [ ] **Launch** with `--fix`: `Fix: [describe bug] --fix`
* [ ] **Diagnose:** `BUILDER` reproduces the bug with a failing test (`DIAGNOSE`), skipping `SPECIFY` and `PLAN`.
* [ ] **Fix & Verify:** `BUILDER` fixes it (`EXECUTE`), isolated `VERIFIER` audits the diff/test (`VERIFY`), and commits `fix(<id>): <T_id> <desc>`.

## 🎛️ Flags & Commands

| Flag / Command | Behavior | Best For |
| :--- | :--- | :--- |
| `--spec-only` / `mode: spec-only` | **(Default)** Pauses once after `SPECIFY`, then auto-runs `PLAN -> EXECUTE -> VERIFY` | Standard features |
| `--gate-all` / `mode: gate-all` | Pauses after **both** `SPECIFY` and `PLAN` | High-risk or unfamiliar repos |
| `--auto` / `mode: auto` | Runs `TRIAGE -> DONE` without pausing (unless `TRIAGE` hits ambiguity) | Well-defined tasks |
| `--fix` | Sets `track: "FIX"`; runs `DIAGNOSE -> EXECUTE -> VERIFY -> DONE` | Bug fixes with a repro test |
| `approve` | Advances past a `SPECIFY` or `PLAN` gate | Confirming specs/tasks |
| `skip` | Bypasses `TRIAGE` questions using defaults | Fast starts |

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

## 🛡️ Security Guardrails

* **Secrets Shield:** `.env*` (allowing `.env.example`), `*.pem`, `*.key`, and `*credentials*.json` are git-ignored and never read, printed, or staged.
* **Supply-Chain Gate:** Unapproved package installs (`npm install`, `pip install`, `cargo add`, `go get`) and `curl | sh` hard-halt unless the exact package is approved in `.sdd/spec.md`.
* **Diff Secret Check:** `VERIFIER` immediately `FAIL`s any `git diff` containing hardcoded secrets, tokens, or sensitive credential files before local commit.

## ♻️ Reusing in New Repositories

Copy `AGENTS.md` into any project root; the harness auto-creates `.gemini/GEMINI.md`, `.sdd/`, `.sdd/lessons.md`, and `.gitignore` rules on first turn:

```bash
cp path/to/AGENTS.md ./AGENTS.md && git init && git add AGENTS.md && git commit -m "chore: add SDD harness"
```
