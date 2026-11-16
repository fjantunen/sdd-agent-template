# ⚡ Spec-Driven Development (SDD) Harness

A lightweight, model-agnostic execution loop for **Google Antigravity** (CLI & Desktop IDE) and **OpenAI Codex** (CLI & Desktop App). Treats `.sdd/spec.md` as an executable contract and `.sdd/state.json` as persistent disk state across sessions, restarts, and tool switches.

## 🗂️ Repo Layout (Already Bootstrapped)

* **`AGENTS.md`** — Master system rules (auto-loaded by OpenAI Codex).
* **`.gemini/GEMINI.md`** — Symlink to `AGENTS.md` (auto-loaded by Google Antigravity).
* **`.sdd/spec.md`** — Locked requirements & `Out of Scope` fence (git-tracked).
* **`.sdd/state.json`** — Live phase, persona, task queue, & retry ledger (git-ignored).

## ✅ Execution Checklist (1 Feature at a Time)

### Phase 1: Launch & Triage

* [ ] **Open Antigravity or Codex** in your repo root (recommended workhorse: `Gemini 4 Hydrogen`, `GPT-6.1 Sol`, or `Claude Sonnet 5.5`).
* [ ] **Start a feature** using an inline HITL flag:
  ```text
  New feature: [DESCRIBE FEATURE OR BUG FIX] --spec-only
  ```
* [ ] **Answer up to 3 triage questions** if scope is vague (or reply `skip` to proceed immediately).

### Phase 2: Spec & Plan Approval

* [ ] **Inspect `.sdd/spec.md`** once `SPECIFIER` finishes generating requirements and the `## Out of Scope` fence.
* [ ] **Approve the spec** to unlock execution:
  ```text
  approve
  ```
* [ ] *(Only in `--gate-all` mode)* Review `.sdd/state.json` task breakdown and reply `approve` again.

### Phase 3: Autonomous Build & Isolated Verification

* [ ] **Let `BUILDER` execute** each `PENDING` task (`T1..Tn`) one at a time with local tests/linters.
* [ ] **Let `VERIFIER` audit** each task in an isolated context against `.sdd/spec.md` and `git diff`.
* [ ] **Verify local auto-commits:** Every passing task automatically commits locally as `feat(<feature_id>): <T_id> <short_desc>` (never pushes remotely).
* [ ] **Confirm `phase: "DONE"`** in the final status block (or resolve blockers manually if `retry_count` hits `3`).

## 🎛️ Control Commands & HITL Modes

Pass flags inline on launch or switch modes mid-run:

| Command / Flag | Behavior | Best For |
| :--- | :--- | :--- |
| `--spec-only` / `mode: spec-only` | Pauses once after `SPECIFY`, then auto-runs `PLAN -> EXECUTE -> VERIFY` | **Default 80/20 workflow** |
| `--gate-all` / `mode: gate-all` | Pauses after **both** `SPECIFY` and `PLAN` | High-risk or unfamiliar repos |
| `--auto` / `mode: auto` | Runs end-to-end without pausing (unless `TRIAGE` hits ambiguity) | Small, well-defined bug fixes |
| `approve` | Advances past a `SPECIFY` or `PLAN` gate | Confirming specs/tasks |
| `skip` | Bypasses `TRIAGE` questions using best-practice defaults | Fast starts |
| `New feature: [desc]` | Resets a `DONE` `.sdd/state.json` for your next feature | Sequential features |

## 🧠 Recommended Model Routing

* **Daily Workhorse (`BUILDER` + `VERIFIER`):**
  * **Google Antigravity:** `Gemini 4 Hydrogen` — fast, low-cost, strict diff adherence, and high prompt-injection resilience.
  * **OpenAI Codex:** `GPT-6.1 Sol` (default 500k context, `medium`/`high` reasoning effort) — fast multi-file edits and long-horizon diff adherence without burning quota.
  * **Anthropic:** `Claude Sonnet 5.5` — top single-model terminal benchmark reliability.
* **Heavy Architecture (`SPECIFIER` + `ARCHITECT`):**
  * **Google Antigravity:** `Gemini 4 Carbon` or `Gemini 4 Argon`
  * **OpenAI Codex:** `GPT-6.1 Terra` or `GPT-6 Astra` (`high` reasoning effort) — best for complex greenfield specs, multi-service contracts, and attached thread-fork verification before handing off to `Sol`.
  * **Anthropic:** `Claude Opus 5.5`
* **Cross-Tool Handoffs:** Start a spec in **Antigravity IDE**, close it, and type `approve` in **Codex CLI** (or vice versa)—state persists automatically on disk.

## 🔀 Running Multiple Features in Parallel

Keep **1 active feature per working directory** so `.sdd/state.json` and git diffs never collide. To run parallel agents in Antigravity Agent Manager or Codex threads, spin up a Git Worktree per feature:

```bash
# Create an isolated workspace + branch for a second concurrent feature
git worktree add ../repo-feat-b -b feat/second-feature

# Remove worktree after merging
git worktree remove ../repo-feat-b
```

## ♻️ Reusing in New Repositories

Copy `AGENTS.md` into any new project root and run one starter prompt—the harness auto-creates `.gemini/GEMINI.md`, `.sdd/`, and `.gitignore` rules on first turn:

```bash
cp path/to/AGENTS.md ./AGENTS.md && git init && git add AGENTS.md && git commit -m "chore: add SDD harness"
```