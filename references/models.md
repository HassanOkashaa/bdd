# Model routing: the Queen decides

For every task, the Queen chooses a model and reasoning effort from the host's actual available options. Do not ask the user to pick routine assignments. User-specified choices, budget constraints, and host restrictions override the default routing policy.

## Before assigning work

1. Inspect the host's exposed model catalog and supported reasoning settings when available. Prefer current host metadata over remembered model names or marketing claims. If no catalog exists, use the documented available choices or current model, and disclose the limitation.
2. Assess ambiguity, blast radius, context size, necessary tools, verification strength, and remaining budget. Select the least costly available model likely to meet the quality bar, not simply the cheapest or largest one.
3. Put `requested_model`, `requested_effort`, `routing_reason`, and `actual_model` in the brief/report. Verify applied settings from the dispatch result or host metadata. If not exposed, write `actual_model: unverified`; do not claim enforcement.
4. If model overrides are unavailable, continue on the current model where capable, record the limitation, and seek a stronger external/human review only when required. Do not invent an API or buy capacity.

## Starting policy

| Task characteristics | Selection preference |
|---|---|
| Ambiguous architecture, cross-cutting planning, subtle correctness review | Strongest suitable reasoning model within budget |
| Bounded implementation with a fixed contract and good tests | Capable coding model with enough reasoning for the feature |
| Browser acceptance and research | Model with the required tools and reliable evidence handling |
| Mechanical, read-only inventory or format checks | Lower-cost model, or deterministic tooling without a model |
| Authentication, authorization, payments or sensitive data changes | Capable builder plus an independent strong reviewer; never substitute cheap review merely to save tokens |

These are starting preferences, not permanent role-to-model locks. A difficult builder task may need the strongest model; a tiny planning task may not. The Queen can revise routing as new evidence arrives.

## Escalation and cost control

When failure suggests reasoning or context limits, escalate capability if available and within authorization/budget. First distinguish model limitations from a broken environment, ambiguous requirements, or missing credentials. More expensive retries do not repair missing evidence. Preserve the original repair-round count across model switches. If the limit is exhausted, stop the feature and report the blocker.

Record routing decisions in brief headers and checkpoints so a resumed Queen can understand them. Do not make cross-vendor quality claims without current evidence. Keep models configurable; no named vendor is required.
