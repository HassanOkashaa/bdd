# Gate 1 proposal — v1

Status: pending, not authorized for execution. Backend only; no user interface.

## Scope and contract

Propose `deduplicate_urls(urls: Iterable[str]) -> list[str]` in `url_helpers.py`.
Use exact string equality; retain the original spelling of each first occurrence.
Inputs are strings; URL validation, canonicalization, network requests, persistence,
and handling non-string values are outside this proposed contract.
Acceptance criteria are recorded in `features.json` as F01 and remain proposals
until explicit approval. No implementation or application tests have been written.

## Reuse assessment

The project README states there is no application implementation yet. No existing
project API or dependency configuration was found. Skill examples are not project
code. Python built-ins can provide ordered traversal and membership tracking;
standard-library unittest can verify behavior without third-party dependencies.
No external research or reads outside the project and skill files were performed.

## Ordered plan after approval

1. Write behavior tests in `test_url_helpers.py` for every F01 criterion, including
   interleaved duplicates, distinct string variants, generator input and unchanged
   input lists. Confirm failure due to the missing helper.
2. Implement the helper in `url_helpers.py` and run
   `python3 -m unittest discover -v` to verify all examples.
3. Prepare a review packet with the final diff, criteria and reproducible command
   for human or separate fresh-session review. Workers remain prohibited.
   Keep F01 unpassed until independent review and final checks are evidenced.
4. Update hive evidence and handoff. No commit, publication or release authorized.

## Budgets and decisions

One feature, at most one active feature, zero authorized workers, at most three
repair rounds after build approval. No new dependencies or spending. Token use
is not measured. The coordinator owns hive files; no builder is assigned yet.

Next user decision: approve or revise Gate 1 v1, especially exact-string matching
and the iterable-to-list contract, and explicitly authorize implementation when
ready. Optional bee names can be supplied separately; silence is not approval.
A later build approval alone does not lift the worker, commit or publishing bans.
