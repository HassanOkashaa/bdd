# Bee Driven Development (BDD) 🐝

**Give your AI coding project a team, a memory, and a definition of done.**

A portable skill for turning a product idea into small, verified increments. You describe the outcome and approve key decisions. A coordinator organizes the work, builders implement it, and reviewers check it against your requirements.

Use it with one coding agent or a multi-agent harness. No framework, API key, paid service, or runtime dependency is required to read the skill. The optional setup command uses Python 3.9+.

> Early release. Tested with Claude Code 2.1.284 and Codex desktop on synthetic setup, regression, handoff and resume scenarios. Native Claude `/bdd` activation and live Sonnet/Opus selection were verified. See [results, fixes and remaining limits](evals/2026-10-14.md). Portability does not mean identical capabilities in every harness.

## Start in three steps

**1. Clone the skill.**

```sh
git clone https://github.com/HassanOkashaa/bdd.git
```

**2. Open your project in your AI coding assistant and paste this.** Replace the path and describe your idea:

```text
Read /absolute/path/to/bdd/SKILL.md and use
Bee Driven Development (BDD) for this project.

My goal: [what I want people to be able to do].
Start by inspecting the project and your available capabilities.
Guide me through the applicable gates, then build within the approved scope.
```

**3. Name your bees, or skip and use role names.** The assistant offers this once at setup. Name any roles you like; unnamed roles stay Queen, Builder, Inspector, Tester, and so on. Your choices are saved for the next session. Then review the proposed direction and plan. After approval, the agent works through verified features and keeps a handoff in your project. It pauses for decisions or missing capabilities that actually block delivery.

The agent can initialize state for you. To do it yourself:

```sh
python3 /absolute/path/to/bdd/scripts/init_hive.py /absolute/path/to/your-project
```

Your project directory must already exist. Setup creates only `hive/`, refuses existing state, and does not install packages, change source files, commit, or contact a service.

Optional names can also be supplied directly during setup:

```sh
python3 /absolute/path/to/bdd/scripts/init_hive.py /absolute/path/to/your-project --bee-name 'queen=Atlas' --bee-name 'builder=Patch'
```

These are examples, not defaults. Custom names appear alongside roles, such as `Atlas (Queen)`. Names never change permissions or the Queen's model-selection responsibility. You can rename bees later through the assistant without resetting state.

## What you get

- **A coordinator:** one place for decisions, status and integration.
- **Clear ownership:** each builder knows which files it may change.
- **Verification before completion:** automated checks, independent review, and real acceptance evidence.
- **A durable memory:** progress, approvals, briefs and reports survive a new chat or a different harness.
- **Bounded autonomy:** work proceeds inside approved scope with limited repair rounds and explicit release authority.

```text
Your goal → design approval when needed → plan approval
                                         ↓
                           brief → build → check → review
                                     ↑               ↓
                                  repair       integrate + verify
                                                     ↓
                                               next feature
                                                     ↓
                                              release approval
```

## The hive

| Role | What it does |
|---|---|
| You, the Beekeeper | Choose the outcome and approve key decisions |
| Queen | Coordinate, preserve state and integrate verified work |
| Builder | Implement a clearly owned increment |
| Inspector | Independently check correctness and requirements |
| Tester | Exercise the actual user journey |
| Scout / Designer / Architect / Guard | Join when research, design, contracts or security need attention |

You do not need nine agents. A small task may need one builder and a fresh reviewer. One agent can perform planning and building sequentially; its self-review is not mislabeled as independent review.

## Three gates, one clear flow

| Gate | When it applies | What you approve |
|---|---|---|
| 0 · Design | New or materially changed user interfaces | A rendered direction you have actually viewed |
| 1 · Build | Before implementing the scoped work | Plan, feature acceptance and boundaries |
| 2 · Release | Before production changes | Verified release and rollout/rollback approach |

Backend work and behavior-restoring fixes skip the design gate. Your existing project policies and scoped authorizations still apply. The agent records explicit waivers; silence never counts as approval.

## Use with your harness

The package follows the [Agent Skills format](https://agentskills.io/specification): a `SKILL.md` entrypoint with linked references and optional scripts.

| Your environment | How to use it |
|---|---|
| A harness with native Agent Skills support | Install this entire directory through its documented skill installer |
| Codex, Claude Code, Cursor, Copilot, Gemini CLI, or another assistant with file access | Use the explicit “read this SKILL.md” prompt above; native installation varies by product/version |
| A single-agent setup | Build sequentially, then use a fresh session or a human for independent review |
| Chat-only assistant | Supply the skill and relevant files; run checks and persist state yourself |

Claude Code and Codex desktop have been exercised in bounded cross-harness tests; the other named products remain untested. See [the validation report](evals/2026-10-14.md) and [native Claude setup / portability](references/portability.md).

For native Claude Code use, clone into an unused `.claude/skills/bdd` directory inside your project, start a new normal session, and invoke `/bdd`. Restricted or safe modes can omit custom skills; use the explicit-file prompt when discovery is unavailable.

## Continue tomorrow, or switch assistants

Open the same project in the next assistant and paste:

```text
Read /absolute/path/to/bdd/SKILL.md and this project's
hive/progress.md, hive/features.json, hive/approvals.md and hive/config.json.
Reconcile them with the actual repository and active work, then resume
the next authorized action. Preserve existing changes and approvals.
```

A skill does not keep running after its host stops. The checkpoint makes resuming explicit and reliable.

## Project files

```text
your-project/
└── hive/
    ├── config.json       Operating mode, capabilities and limits
    ├── features.json     Acceptance criteria and verified status
    ├── approvals.md      Decisions with scope and artifact references
    ├── progress.md       Checkpoints and the next action
    ├── briefs/           Builder and reviewer assignments
    ├── reports/          Verification evidence
    └── research/         Relevant sourced findings
```

See the [state contract](references/state.md) and [worked example](examples/reading-list.md). Commit non-sensitive state with the project when appropriate; keep credentials, personal information, and private logs out of it.

## Tune it to your project

Start with the generated config. Default to one active feature and one worker; increase concurrency only with non-overlapping ownership and isolated resources. Default to three repair rounds per feature. The Queen chooses the model and reasoning effort for each task, balancing difficulty, risk, latency and cost against the models actually available. Explicit user choices take precedence. Every brief records the choice and reason; unavailable routing is disclosed. There are no vendor/model locks. See [model routing](references/models.md).

The skill works with an existing codebase. It does not replace project rules, reset files, require a new tech stack, or grant deployment permissions.

Before resuming an existing hive, check its portable state:

```sh
python3 /absolute/path/to/bdd/scripts/validate_hive.py /absolute/path/to/your-project
```

Validation reports structural issues without changing files. Preserve originals when correcting state; a valid file is not proof that its approval or verification claims are true.

## When something blocks

| Situation | Expected behavior |
|---|---|
| `hive/` already exists | Read and resume it; the initializer refuses to overwrite |
| No browser available | Request human acceptance with concrete steps; do not claim a browser pass |
| No subagents available | Build sequentially and obtain a fresh-session or human review |
| Checks keep failing | Stop the affected feature at the repair limit with findings and next options |
| Unrelated work is in the checkout | Preserve it and isolate or serialize the hive's changes |
| Session or usage ends | Checkpoint and resume later; no claim of invisible background work |

## Quality and contribution

Run the dependency-free setup tests:

```sh
python3 -m unittest discover -s tests -v
```

The 19 tests cover safe initialization, optional bee naming, portable state shape, dependency consistency, evidence requirements, malformed JSON and mutation-free validation. They do not establish the quality of an LLM's decisions. [Behavioral evaluation scenarios](evals/scenarios.md) define the separate checks needed for a harness compatibility claim.

See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and reporting. Keep the core portable, use synthetic examples, and include observed evidence for any compatibility claim.

## Foundations

The workflow draws on feature-by-feature delivery and durable progress from Anthropic's [long-running agent harness work](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), and separation of planning, building and evaluation from its [application harness design research](https://www.anthropic.com/engineering/harness-design-long-running-apps). This repository's workflow and templates are an independent implementation, not an official integration or endorsement.

## License

[MIT](LICENSE). Use, adapt and redistribute it in personal or commercial projects.
