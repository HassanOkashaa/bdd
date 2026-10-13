# Roles and delegation contracts

Use the fewest roles that provide distinct value. Names are optional and customizable.

| Role | Responsibility | Writes |
|---|---|---|
| Beekeeper | Product decisions and scoped approvals | Approval through user conversation |
| Queen / coordinator | Holds state, assigns ownership, verifies evidence, integrates | Shared `hive/` state and integration |
| Scout | Resolve a concrete uncertainty using primary sources | Assigned research report |
| Product lead | Scope, priorities and observable acceptance | Assigned specification |
| Architect | Dependency order, contracts and boundaries | Assigned contract documents |
| Designer | User journeys and rendered alternatives before build planning | External mockup location |
| Builder | Implement and test an assigned increment | Only assigned source and test files |
| Inspector | Fresh-context correctness and requirements review | Assigned report only; source read-only |
| Tester | Execute acceptance against the running result | Assigned report only; source read-only |
| Guard | Review changed trust boundaries | Assigned report only; source read-only |

The coordinator can perform several roles sequentially. A builder's own second pass is **self-review**, even if it adopts another name. Prefer a fresh session or human reviewer when independent verification is unavailable in the host. Do not mark a required independent check complete through roleplay.

The Queen owns model selection for every task. Follow [model routing](models.md), recording the available options, selected model/effort, reason and actual applied choice. Host restrictions and explicit user selections take precedence. No subscription or paid tool is required by the skill itself.

## Builder brief

- Feature ID and desired outcome.
- Frozen acceptance criteria and approved design reference (if applicable).
- Base revision, working directory, owned files, excluded files, shared-file owner.
- Dependencies and exact agreed API/data contract.
- Check commands and isolated database/ports/process ownership.
- Available tools, applicable permissions, maximum repair rounds and budget.
- Report path and required contents: changed files/revision, commands/results, evidence, limitations, blockers.
- You are not alone in the codebase. Preserve other contributors' changes; report ownership conflicts rather than overwriting them.

## Review brief

Supply the acceptance criteria, design artifact if relevant, candidate revision/diff, environment instructions and check commands. Withhold the builder's reasoning and self-assessment; factual commands/logs are allowed as reproducibility inputs. Ask the reviewer to verify, not trust, reported outcomes.

Report `PASS`, `FAIL`, or `BLOCKED`, the reviewed revision, criteria checked, reproducible findings, severity, and missing evidence. Source code is read-only; report writes are allowed only at the assigned path. A screenshot proves appearance at one moment, not working persistence or authorization.
