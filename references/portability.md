# Harness portability

The portable contract is Markdown instructions plus project files. Native skill discovery, multi-agent execution, model routing and browser access vary by host. This package does not implement a scheduler, agent runtime, security sandbox, or enforced approval service.

| Available capability | Operating mode |
|---|---|
| Native Agent Skills loader | Install the whole skill directory using the host's documented mechanism. |
| File-reading coding assistant without a skill loader | Ask it to read `SKILL.md`; load linked references when needed. |
| Fresh-context workers | Delegate scoped builds and independent reviews if host policy allows. |
| One coding agent only | Build sequentially. Use a separate fresh session or human for independent review; keep that gate blocked until obtained. |
| No browser automation | Provide the running URL and acceptance steps for human verification; record actual feedback. |
| No shell or file access | Assist planning and review from supplied artifacts. The user must persist state and execute checks; do not claim autonomous delivery. |
| No Git or worktrees | Serialize file writes, retain user-managed snapshots, and identify the reviewed artifact version. |
| No configurable models | Use the current model; never pretend a routing preference was applied. |
| Session ends or usage limit reached | Save a checkpoint. Resume only when the user or a real configured host mechanism starts another session. |

## Universal invocation

Replace the path with your clone location:

> Read `/path/to/bdd/SKILL.md` and use it for this project. Start with my goal and the project's existing instructions. Discover your actual capabilities, initialize durable state without overwriting anything, and lead me through the applicable gates.

## Resume on another harness

> Read this project's instructions and `hive/progress.md`, `hive/features.json`, `hive/approvals.md`, and `hive/config.json`, then read `/path/to/bdd/SKILL.md`. Reconcile the working tree, active workers and reports. Resume the next authorized action without repeating approved work or inventing missing verification.

Copy or attach the linked references if the host cannot open relative files. Never overwrite global `AGENTS.md`, `CLAUDE.md`, or editor rules to install this package. A project may add a short pointer to the skill by explicit choice.

## Claude Code native loading (tested)

From your project directory, install into an unused directory:

```sh
git clone https://github.com/HassanOkashaa/bdd.git .claude/skills/bdd
```

Start a new normal Claude Code session and invoke `/bdd`. In the tested CLI 2.1.284, the normal loader discovered the project skill; the restricted test invocation did not. Safe mode also disables custom skills. If the host disables discovery, use the explicit-file prompt above and disclose that you are not using native activation. Do not overwrite an existing skill folder or weaken host permissions to enable discovery.

The project path and slash invocation follow the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills). Other harnesses may use different install paths; the explicit-file route remains portable.

## Codex native loading (tested)

From your Git project, clone into an unused skill directory:

```sh
git clone https://github.com/HassanOkashaa/bdd.git .agents/skills/bdd
```

Start Codex in that project and invoke `$bdd`. Codex CLI 0.154.0 discovered this directory, read the skill, initialized valid state, and resumed an approved backend build in a fresh session. If it does not appear, restart and check the host's skill settings. Do not substitute `.claude/skills` for Codex's project path.

The path and invocation follow [OpenAI's local skill documentation](https://learn.chatgpt.com/docs/build-skills). The desktop skill picker was not separately exercised. See [native-harness evidence](../evals/2026-10-14-native-harnesses.md).

## Hermes native preloading (tested)

Install into an unused directory under the active Hermes profile:

```sh
git clone https://github.com/HassanOkashaa/bdd.git "${HERMES_HOME:-$HOME/.hermes}/skills/bdd"
hermes --in /absolute/path/to/your-project --skills bdd
```

Tested with Hermes Agent 0.21.1 (a locally modified installation); results do not certify every upstream build. Tell the agent the absolute project path as well. In the noninteractive test, a terminal opened in the home directory despite the launch working directory. Check the actual tool working directory and anchor project commands explicitly; a missing relative file is not proof that project state was lost.

An isolated home without credentials could not run inference. A temporary named profile using the host's existing authentication fallback could preload BDD and complete the setup conversation. Keep authentication configuration separate from the skill. Do not copy credentials into BDD or your project's hive.

## OpenClaw native loading (discovery and reading tested)

Install into an unused directory inside the configured agent workspace:

```sh
git clone https://github.com/HassanOkashaa/bdd.git skills/bdd
openclaw skills info bdd --json
```

OpenClaw 2026.3.13 reported BDD eligible, and its agent read `SKILL.md` through the native catalog. The bounded local-model behavior tests did not establish a complete setup pass; consult the evaluation report. A loader result proves discovery, not successful delivery. Likewise, a CLI exit code of zero does not prove success when the result reports an aborted or timed-out agent turn.

The install location follows the shipped OpenClaw documentation ([online reference](https://docs.openclaw.ai/tools/skills)). No connected messaging channels or production workspace are needed to use BDD.
