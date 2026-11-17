# Feature Spec: <feature_id>

> Max 150 lines. Treat as an executable contract.

## Overview
<1-3 sentences describing what is being built and why.>

## Requirements (EARS)
- **REQ-1:** WHEN <trigger/precondition> THE SYSTEM SHALL <observable behavior>.
- **REQ-2:** IF <error/edge condition> THEN THE SYSTEM SHALL <fallback/error behavior>.

## Interface & Schema Contracts
- **Inputs / CLI / API:** `<exact signature, endpoint, or flag>`
- **Outputs / State / Files:** `<exact schema, return value, or file path>`
- **Approved Dependencies (if any):** `None` *(list exact package names if new installs are required)*

## Verification Commands
```bash
# Binary pass/fail checks run during EXECUTE and VERIFY
<test-or-lint-command>
```

## Out of Scope
- <Explicitly excluded feature, refactor, or behavior>
- <Do not modify unrelated files or public APIs not listed above>
