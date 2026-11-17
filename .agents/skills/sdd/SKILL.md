---
name: sdd
description: Run Spec-Driven Development (SDD) for spec writing, feature planning, PRDs, bug-fix diagnosis, and structured task execution. Use when starting a new feature, drafting an EARS specification, breaking work into verifiable tasks, or fixing bugs with a state-tracked plan-execute-verify loop.
---

# Spec-Driven Development (SDD)

Execute software changes through a file-backed state machine using `.sdd/spec.md` as an executable contract, `.sdd/lessons.md` as repo memory, and `.sdd/state.json` as persistent state. See [references/AGENTS.md](references/AGENTS.md) for the full canonical rulebook.

## 1. Bootstrap & Hygiene

On first activation in a repository:
1. Ensure `.sdd/` exists and initialize `.sdd/lessons.md` from [references/lessons-template.md](references/lessons-template.md) (`<= 30` lines, git-tracked).
2. Read `.sdd/state.json` and `.sdd/spec.md` on every turn. If `.sdd/state.json` is missing, initialize it from [references/state-template.json](references/state-template.json).
3. Ensure `.gitignore` ignores `.sdd/state.json`, `.env*` (allowing `!.env.example`), `*.pem`, `*.key`, and `*credentials*.json` while keeping `.sdd/spec.md` and `.sdd/lessons.md` git-tracked.

## 2. Execution Modes & Tracks

Parse standalone commands (`mode: gated`, `mode: yolo`, `"yolo mode"`), inline flags (`--gated`, `--yolo`, `--fix`), or `sdd_mode: yolo` in project config/frontmatter on any turn and persist to `.sdd/state.json`:

| Mode / Flag | Behavior |
| :--- | :--- |
| `gated` (Default, `--gated`) | Pause after `SPECIFY` and `PLAN` for explicit user `approve` before writing code. |
| `yolo` (`--yolo`, `"yolo mode"`, `sdd_mode: yolo`) | Auto-generate `.sdd/spec.md`, `PLAN`, and `tasks[]` in `.sdd/state.json` on disk in one pass, immediately execute all tasks end-to-end, and run verification/tests. Skips human wait-gates, **never** skips writing Spec/Task artifacts. Only pause if a hard blocker or failing test cannot be auto-resolved after 2 attempts (`retry_count >= 2`). |
| `--fix` (`track: FIX`) | Skip `SPECIFY` and `PLAN`; run `DIAGNOSE -> EXECUTE -> VERIFY -> DONE`. |

## 3. State Machine & Personas

Enforce strict persona separation via `active_persona` in `.sdd/state.json`:

1. **`TRIAGE -> SPECIFY | DIAGNOSE`**
   - Evaluate scope, stack, and acceptance criteria. If critically ambiguous in `gated` mode, ask **max 3 single-line trade-off questions** and halt.
   - If clear (or `yolo` / user replies `skip`), advance to `DIAGNOSE` (`FIX` track) or `SPECIFY` (`FEATURE` track).
2. **`SPECIFY -> PLAN`** (`SPECIFIER`, `FEATURE` track)
   - Write `.sdd/spec.md` (`<= 150` lines) using [references/spec-template.md](references/spec-template.md): EARS requirements (`REQ-1: WHEN <trigger> THE SYSTEM SHALL <behavior>`), concrete interface/schema contracts, binary verification commands, and `## Out of Scope`.
   - Zero code or implementation guesses. Halt for `approve` if `sdd_mode == "gated"`.
3. **`PLAN -> EXECUTE`** (`ARCHITECT`, `FEATURE` track)
   - Decompose `.sdd/spec.md` into atomic, ordered `tasks[]` in `.sdd/state.json` (`id`, `desc`, `req_refs`, `status: "PENDING"`).
   - Zero code edits. Halt for `approve` if `sdd_mode == "gated"`.
4. **`DIAGNOSE -> EXECUTE`** (`BUILDER`, `FIX` track)
   - Reproduce the bug with a minimal failing test/check, record `T1` in `.sdd/state.json`, and advance to `EXECUTE`.
5. **`EXECUTE -> VERIFY`** (`BUILDER`)
   - Read `.sdd/lessons.md` first. Implement **only** the next `PENDING` task without touching unrelated files or altering `.sdd/spec.md`.
   - Run local test/lint commands to verify compilation and behavior, then advance to `VERIFY`.
6. **`VERIFY -> EXECUTE | DONE`** (`VERIFIER` — Isolated Context)
   - Spawn an isolated subagent / fresh verification context (loaded only with `.sdd/spec.md`, `.sdd/lessons.md`, `.sdd/state.json`, and `git diff`; strip `BUILDER` rationale). If subagents are unavailable in the host runtime (Claude Code, Cursor, Codex, Gemini, Antigravity), audit adversarially in-thread using quote-anchoring.
   - Audit `git diff` + test output against `.sdd/spec.md` and `## Out of Scope` (or the `DIAGNOSE` repro test on `FIX`). Immediately `FAIL` any diff containing hardcoded secrets, tokens, or credential files.
   - **On Fail:** Set task `status: "FAIL"`, append exact `REQ-ID`/test defect to `blockers[]`, increment `retry_count`, and route to `BUILDER`. Halt for human intervention if `retry_count >= 2`.
   - **On Pass:** Set task `status: "PASS"`, clear `blockers[]`, reset `retry_count: 0`. If a subtle repo quirk caused a failure or non-obvious fix, append 1 terse bullet to `.sdd/lessons.md` (keeping `<= 30` lines). Commit scoped task files locally (`feat(<feature_id>): <T_id> <short_desc>` or `fix(<feature_id>): <T_id> <short_desc>`, plus `.sdd/lessons.md` if updated); never `git push`. Loop to `EXECUTE` if `PENDING` tasks remain, else set `phase: "DONE"`.

## 4. Guardrails & Grounding

- **Secrets Shield:** Never read, print, or stage `.env*` (except `.env.example`), `*.pem`, `*.key`, or `*credentials*.json`.
- **Hard Halt:** Never run `git push`, `git reset --hard`, `rm -rf`, DB drops, `curl | sh`, or unapproved package installs (`npm install`, `pip install`, `cargo add`, `go get`) unless the exact package is approved in `.sdd/spec.md`.
- **Closed-World Grounding:** Never invent APIs, dependencies, or env vars not present in the repo or `.sdd/spec.md`; halt with `ERR_INSUFFICIENT_SPEC: [missing detail]`.

## 5. Output Contract

Persist `.sdd/state.json`, `.sdd/spec.md`, and `.sdd/lessons.md` before responding. Keep gate, status, and triage responses under 150 words:
- `🚦 State`: `<phase> | <active_persona> | <track> | <sdd_mode>`
- `📋 Delta`: Files changed, test results, or `REQ-ID` audit findings
- `⚠️ Blockers / Questions`: Active blockers, `retry_count`, or max 3 triage questions (`None` if clear)
- `👉 Next`: Exact next action (`Reply "approve"`, `Auto-advancing to T2`, or `DONE`)
