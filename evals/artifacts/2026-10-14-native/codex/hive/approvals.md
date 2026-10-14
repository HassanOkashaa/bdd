# Approvals

## Gate 0 — excluded — 2026-10-14

Scope: Python backend URL deduplication helper, plan v1. No UI or design change.
Backend-only exclusion applies under both the supplied standing instructions and
BDD SKILL.md. This is an exclusion, not an inferred design approval.
Artifact: `hive/plan.md` v1.

## Gate 1 — pending — 2026-10-14

Scope: `hive/plan.md` v1, F01 criteria in `hive/features.json`, budgets and
permissions in `hive/config.json`.
User instruction: “Start setup only, offer optional bee naming and prepare the
applicable approval gate. Do not implement application code, commit, publish,
launch workers, or read outside this synthetic project and the skill files.”
No build approval received. Criteria are proposed, not frozen.
BDD requirement: “Do not infer it from silence.”
Next: user approves or revises the concrete plan and authorizes a build.

## Gate 2 — not reached

No implementation, verification, release or publishing approval exists.

## Gate 1 — approved — 2026-10-14

Artifact: `hive/plan.md` v1 (retained verbatim as the approved proposal).
Scope: F01 acceptance criteria in `hive/features.json`, now frozen unchanged.
Exact user decision: “I approve hive/plan.md v1 and its F01 criteria: exact-string deduplication preserving first-seen order, iterable inputs including a generator, new list output with input unchanged.”
User authorized implementation of only `url_helpers.py`, `test_url_helpers.py` plus hive evidence, tests and preparation for independent review. Role defaults confirmed. Workers, commits, publishing and reads outside the project and its skill remain prohibited. Preserve notes.txt exactly; no model identity inference. F01 must remain unpassed until independent review is complete. This supersedes the historical pending Gate 1 entry; Gate 2 remains unreached.
