# F01 independent review packet — pending

Reviewer: unassigned; no independent review has occurred. Workers are prohibited in this session.
Use a separate fresh session or human reviewer. Review read-only; report findings to the coordinator.

## Specification and inputs

- Approved spec: hive/plan.md v1; approval: latest Gate 1 entry in hive/approvals.md.
- Frozen criteria: F01 in hive/features.json.
- Scope and acceptance-to-check mapping: hive/briefs/F01.md.
- Code: url_helpers.py and test_url_helpers.py.
- Complete application diff against absent files: hive/reports/F01.diff.
- Exact target hashes: hive/reports/F01-artifacts.sha256. No HEAD exists on main.

## Review procedure

1. Verify `shasum -a 256 -c hive/reports/F01-artifacts.sha256` from project root.
2. Independently compare code and tests against each frozen criterion. Check exact equality, first-seen order, empty/unique/duplicate cases, a one-pass generator, fresh list output, and unchanged input list. Generator consumption is expected.
3. Run `python3 -B -m unittest discover -v`; inspect test adequacy and add independent checks as needed without modifying the delivered artifacts.
4. Run `python3 -B .agents/skills/bdd/scripts/validate_hive.py .` for state structure only.
5. Return reviewer identity/role, independence statement, timestamp, reviewed hashes, commands and exits, criterion-by-criterion verdicts, findings and overall verdict. Do not infer model identity.

This packet supplies the spec, brief, diff and reproducible checks, with no builder justification. Do not treat deterministic tests or schema validation as review approval. If artifacts change, revalidate affected checks and review the new hashes. The coordinator may mark F01 passed only after actual independent approval and final verification of the same artifacts. No commits or publishing are authorized.
