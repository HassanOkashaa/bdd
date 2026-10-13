# Durable state

The initializer creates `hive/` once and refuses to overwrite it. Templates are empty on purpose: the agent fills them from the user's project after intake. They are not an approved plan.

- `config.json`: budgets, actual host capabilities and operating mode. Three repair rounds per feature and one worker at a time are defaults; adjust to the project and host.
- `features.json`: ordered feature ledger. Coordinator-owned, not a substitute for approval.
- `approvals.md`: gate, status, scope/version, artifact reference, exact user decision and date. Record exclusions and explicit waivers here. Pending is never approval.
- `progress.md`: append checkpoints: completed work, current revision, verification, blockers, live resources, next action.
- `briefs/`: scoped assignments.
- `reports/`: test and review evidence, with reviewed revision and reproducible steps.
- `research/`: sourced findings relevant to actual decisions.

## Feature record

```json
{
  "id": "F01",
  "description": "A reader can save an article for later",
  "depends_on": [],
  "acceptance": [
    "Saving a valid article URL creates one entry",
    "The entry remains after restarting the app",
    "Saving the same URL twice does not create a duplicate"
  ],
  "status": "pending",
  "passes": false,
  "evidence": [],
  "blocked_reason": null
}
```

Valid statuses: `pending`, `building`, `verifying`, `blocked`, `passed`.
`passes` is true if and only if status is `passed`. Evidence entries should identify the acceptance criterion, command or human procedure, observed result, revision, and report location. A report from another revision needs an explicit relevance assessment or rerun; integration changes that affect it require fresh verification.

Dependencies must refer to existing IDs and be acyclic. Do not start a dependent feature until its prerequisites pass; partial implementation does not satisfy a dependency. Discovering a dependency requires a transparent ledger correction; changing approved scope or criteria needs a user decision. Keep prior approval and failure history.

## Stop and checkpoint

A checkpoint includes timestamp, last verified revision, feature state, failed commands, repair round, current branches/worktrees, worker identifiers, owned process IDs/ports/databases, remaining budget if available, and exactly what to do next. Never put credentials in state. On hosts without measurable token usage, bound work by rounds/features and disclose that tokens were not measured.

The ledger is evidence-based bookkeeping. These files cannot technically enforce permissions; enforcement belongs to the host and its tools.
