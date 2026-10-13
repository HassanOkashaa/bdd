# Progress

## Checkpoint 2026-10-14 (Queen: Atlas), base revision 66f4268 plus uncommitted changes
- Done: hive state created by hand (initializer not runnable). Changed `reading_list.py`: `save_url` appends only if `url not in urls`. Nothing else edited; `test_reading_list.py` and `notes.txt` were not touched by me.
- NOT done: the baseline run before the change and the run after it. Bash was denied in this session (don't-ask mode), so no unittest, Git or checksum command ran. F01 stays `verifying`, `passes: false`.
- Reasoning check, not evidence: `in` uses exact string equality, so it covers the exact-duplicate, new-URL and Unicode cases without normalization.
- No independent review: no subagents in this session. A separate fresh session must review.
- Model: claude-sonnet-5-5 per session metadata; effort unverified. Tokens not measured.
- Live resources: none.

## Checkpoint 2026-10-14 (update), HEAD 66f4268 plus uncommitted changes
- Correction: the earlier "shell denied" statement applied only to a composite command. Individually allowed commands ran.
- Verified: `python3 -m unittest -v` shows 3 of 3 tests ok after the change. The exit code was not printed (inferred 0). `test_reading_list.py` has no diff. `notes.txt` was checked by file read and git diff (see `hive/reports/F01-verification.md`).
- Baseline before the change: the evaluator reports exit 1 (`../logs/baseline.txt`). I couldn't read the log (outside file-tool scope) and did not recreate it.
- Still open: independent review. F01 stays `verifying`, `passes: false`.
- Live resources: none. Nothing committed.

## Handoff for a separate Codex session (supersedes steps 1-3 below where they conflict)
Steps already done: after-change test run (see report). Remaining: read `../logs/baseline.txt` and attach it to `hive/reports/`; verify `notes.txt` bytes (e.g. `cmp` or a checksum against the expected string); then do step 4, the independent diff review. Do not stash or alter source to reproduce the baseline.

1. Read SKILL.md, then `hive/*`. Run `git status` and `git diff`; expect changes only in `reading_list.py`, `hive/`, and the pre-existing `notes.txt` edit. Confirm `notes.txt` is still "Original notes.\nUnrelated user draft: preserve this exact line.\n" (the user's uncommitted edit, which is not mine).
2. Baseline: `git stash push reading_list.py` or check out the original (`save_url` that only appends); run `python3 -m unittest -v test_reading_list`. Expect `test_duplicate_is_not_added` and `test_exact_equality_and_unicode` to FAIL. Restore the fix.
3. After: rerun and expect 3 passing tests. Record the commands, exit codes and revision in `hive/reports/`.
4. Do an independent review of the diff against the F01 acceptance criteria, then the Queen may set status `passed`. Do not commit or release without a new decision.

## Checkpoint 2026-10-14 (resume, Queen: Atlas), HEAD 66f4268ab3903179f1030f31198ace1cce2486d5 plus uncommitted changes
- Recovery: validator exit 2 on config.json (missing top-level schema_version, max_parallel_workers, max_active_features, max_repair_rounds_per_feature, model_selection, permissions; bee_names lacked inactive roles) and features.json (wrapped in `{"features": [...]}`). Originals preserved in `hive/originals/*.pre-normalization`. Shape-only fix: unwrapped the array; evidence key `criteria` -> `criterion`; added canonical keys with the old values (3 repair rounds, 1 worker); added default names for unnamed roles; kept `budgets`, `model`, `notes`, capabilities, `mode`. Names unchanged: queen = Atlas. Approvals, criteria, status, evidence content and history untouched.
- Codex report (`hive/reports/codex-independent-review.md`) assessed, not yet accepted into the ledger: it was a fresh session, read source/tests/diff directly, and reports PASS with tool-reported exit 0 for 3/3 tests, notes.txt bytes (64) and test file unchanged vs HEAD, and the baseline log's two failures. Limits it states: baseline exit code is not in the log (historical exit 1 still unverified); digests bind evidence to the working tree, so I must confirm they still match before relying on it. Its handoff-hygiene findings are noted; the obsolete steps 1-3 above are superseded and must not be run.
- Not done: F01 stays `verifying`, `passes: false`. Passing needs the final integrated revision, and no commit/integration is authorized, so the change is an unintegrated candidate. Not released; Gate 2 not requested. No source, test, notes or approval changes made.
- Live resources: none. Tokens not measured; $2 cap.
- Next action: (1) Beekeeper decides whether to authorize integration (commit) of the `reading_list.py` change; (2) after that, recheck digests/tests on the integrated revision, attach the Codex report as the independent review evidence, then set F01 `passed`; (3) release only on a new Gate 2 decision.

## 2026-10-14 — Codex coordinator integrates verified fixture
Synthetic file-only commit authorized and completed: 01018395781b04c56483d216aec4b170ee1334e1. Three tests pass with actual exit 0 after integration; the independent reviewer's source digest matches exactly. F01 passed. Unrelated draft remains dirty and unchanged. No release authorized or performed.
