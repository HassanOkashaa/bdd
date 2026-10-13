# Independent validator review — 2026-10-14

Scope: uncommitted `scripts/validate_hive.py`, `tests/test_validate_hive.py`, `SKILL.md`, `references/state.md`, `references/portability.md` in `<bdd-directory>`. Read-only repository review; temporary fixtures only. No source edits, commits or publishing.

## Findings

1. **P2: malformed deep JSON crashes rather than returning the documented error result** — `scripts/validate_hive.py:23–24`. `json.loads` can raise `RecursionError`, which the handler does not catch. With `features.json` equal to `'[' * 10000 + '0' + ']' * 10000` (~20 KB), the CLI emits a traceback and exits 1 rather than giving a recovery diagnostic and exit 2. Reproduced on Python 3.12.2. Catch `RecursionError` alongside parse/read errors, and add a CLI regression ensuring no traceback and no mutation. A 1,200-deep fixture happened to remain below this parser's limit and returned normal validation errors; use sufficient depth for the regression.

2. **P2: duplicate JSON keys can silently discard state while validation reports success** — `scripts/validate_hive.py:23`. The default JSON loader keeps only the last occurrence. Starting from valid config, append a second `max_parallel_workers` field of 10 to an existing value of 1; the validator returns 0. The same mechanism applies to duplicated `bee_names`, `acceptance`, `permissions` or `evidence` fields. A later normal load/save can permanently drop the earlier value without the recovery process noticing, conflicting with the stated goal of preserving names, criteria, evidence and history. Reject duplicate keys using an `object_pairs_hook` that raises a clear error; do not choose either value automatically. Include nested duplicates in tests. The validator itself did not mutate files; the data-loss risk arises during subsequent ordinary load/save or normalization.

## Executed verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`: all 18 tests pass.
- 104 feature-field type probes across nulls, booleans, numbers, strings, arrays and objects: no unhandled exceptions.
- Malformed UTF-8 and truncated JSON: exit 2 with diagnostics.
- Deeply nested JSON: exit 1 with `RecursionError` as described above.
- Duplicate config field: exit 0 as described above.
- File SHA-256 snapshots before/after ordinary malformed-fixture CLI runs: no mutation.
- Local runtime: macOS, Python 3.12.2.

## Instructions assessment

Recovery instructions correctly require preserving originals, keeping custom names and extra history, avoiding reinitialization and separating structural validation from evidence truth. No unsafe deletion/reset instruction found. Clarification of narrowly observed command denial avoids claiming total shell loss and explicitly forbids bypassing denial. These are useful, restrained guarantees.

The validator checks JSON structures, dependency consistency and minimal evidence shape. It does not prove approvals/reviews, validate the complete existence/content of progress/approval/report artifacts, or establish acceptance coverage; its success message and state reference explicitly reserve evidence review. Do not market this as end-to-end state integrity.

Claude Code native-loading claims were inspected as documentation only, not independently rerun in this review. This review does not certify native activation or the claimed CLI version's behavior. Cross-platform tests and real recovery/resume through an assistant were also not run.
