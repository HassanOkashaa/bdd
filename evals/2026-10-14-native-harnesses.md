# Native harness validation · 2026-10-14

Follow-up to [the earlier Claude/Codex evaluation](2026-10-14.md), starting from BDD v0.1.1 (`72f576ad9a30273bbbca299980c8067c828710df`). Tests used disposable Git projects and isolated harness profiles. No production application, messaging channel, deployment, or global skill installation was used.

## Inventory and results

| Harness | Version actually inspected | Result |
|---|---|---|
| Codex CLI | 0.154.0; existing ChatGPT authentication | **PASS** native project discovery, explicit `$bdd`, setup, fresh-session resume, approved backend implementation, nine behavior tests and honest pending-review state |
| Hermes Agent | 0.21.1 / 2026.9.7, upstream `6f7a7991`, local `fb3446a2` with seven carried commits | **PASS** native profile preloading and setup conversation; **PASS** independent Codex→Hermes review after anchoring the project path |
| OpenClaw | 2026.3.13 (`61d171a`) | **PASS** native discovery and actual `SKILL.md` reading; **INCOMPLETE** setup behavior: both bounded Ollama runs timed out |
| Claude Code | Already tested at 2.1.284 | Prior native and cross-harness results retained; not rerun in this follow-up |
| Cursor, Gemini CLI, Copilot CLI, Aider, OpenCode, Goose, Cline, Qwen CLI, Amp, Kimi, Pi | No executable found in the inspected PATH/common install locations | Not run; no new harnesses installed |
| Copilot editor extensions | 1.250.0 and Copilot Chat 0.13.1 directories remain | No runnable VS Code/Cursor host found in the inspected application locations or Spotlight lookup; extension files alone do not establish an available harness |

`continue` resolved to a shell keyword, not an AI CLI. Hermes and KanbanCode application wrappers were present; wrapper presence is not a separate model/harness validation. Ollama supplied the already-installed `qwen3.5:2b` model for OpenClaw; the embedding model is not a coding harness. This inventory is bounded to discoverable local installations, not every possible file on the machine.

## Codex: native activation and fresh resume

Installed an unchanged local clone into the synthetic Git project's `.agents/skills/bdd`. The setup prompt used `$bdd` without giving its file path. Codex located and read the native skill, offered optional bee names, initialized `hive/`, validated its structure, and prepared Gate 1. It correctly excluded Gate 0 for backend-only scope and did not implement code before approval.

A **fresh** CLI invocation read the saved plan and state. The synthetic evaluator explicitly skipped custom names and approved plan v1 with fixed criteria and file ownership. Codex retained role defaults, implemented `deduplicate_urls`, and passed nine tests covering exact string identity, stable order, empty and unique inputs, repeated values, generators, new-list output, and unchanged input. The unrelated draft matched its before hash. No workers, commits or publication occurred. It kept `passes: false` while independent review was pending.

Commands used this form, with prompts retained in the evidence directory:

```sh
codex -a never exec --ignore-user-config --ephemeral \
  --sandbox workspace-write -C /absolute/synthetic/project \
  --json -o /absolute/logs/final.txt - < /absolute/logs/prompt.txt
```

Each invocation had an external 180-second bound. Ignoring user configuration isolated optional connections; it did not disable native project skill discovery. CLI events did not expose an applied model identifier, so the current model remains **unverified**. No model override or autonomous dispatch claim is made. The desktop skill picker was not tested.

## Hermes: native preload and independent review

A clean isolated home initially failed inference because it had no credentials. We then used a temporary named profile under the existing Hermes home, with BDD in that profile's `skills/bdd`. The host's normal authentication fallback was used; no credentials were placed in the BDD repository or public evidence.

Native `--skills bdd` preloading succeeded. With only the skills toolset enabled, Hermes offered optional names, used role-name defaults, skipped design for backend scope, and accurately disclosed that it could not execute or inspect the project in that restricted run.

The first independent review attempt revealed a host working-directory mismatch: the terminal started in the home directory rather than the subprocess launch directory. Hermes stopped without claiming project verification. The corrected attempt used `--in`, supplied the absolute project path in the prompt, and explicitly anchored terminal commands. A file-search operation was denied, but permitted explicit file reads and project-scoped checks succeeded.

```sh
hermes --in /absolute/synthetic/project --skills bdd \
  --toolsets skills,file,terminal \
  --usage-file /absolute/logs/usage.json -z "<review prompt with absolute project path>"
```

This fresh Inspector independently read the approved criteria and source, passed all nine tests, passed additional contract probes, validated the hive, and checked the original notes hash and source/test hashes. The reviewer made no state changes and did not infer release authorization. The preserved fixture is the pre-review checkpoint; its pending status is historical evidence, not a current claim that no review occurred. No final synthetic commit/integration was authorized in this follow-up.

The host usage report identified `gpt-6-sol` through `openai-codex`. This is host-reported metadata, not an independent provider attestation. The evaluator selected the configured model for this bounded review; automatic Queen dispatch across models was not tested. The profile used a 14-turn cap for review and an external 180-second bound. Hermes one-shot mode automatically bypasses approval prompts, so these tests do **not** validate host approval enforcement; the scope was disposable files and explicitly permitted checks.

## OpenClaw: discovery is not delivery

Installed into the synthetic agent workspace's `skills/bdd`. `openclaw skills info bdd --json` returned `source: openclaw-workspace`, `eligible: true`, and no missing requirements. The runtime catalog included BDD and the agent actually called `read` on its `SKILL.md`; successful tool results contained the skill.

The existing OpenClaw OAuth profile's expiry was in the past. We did not reset it, change its login or move its credentials. Instead, the isolated test configuration selected the already-installed local Ollama model `qwen3.5:2b`, with only the read tool allowed, filesystem workspace scoping, no plugins, and no delivery flag or messaging tools.

```sh
openclaw skills info bdd --json
openclaw agent --local --session-id bdd-native-test \
  --message "<setup-only prompt>" --thinking off --timeout 90 --json
```

`OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_PATH` pointed to disposable test locations. The first run inherited a broader skill catalog. A second run filtered the agent's skills to BDD alone. Both read the skill but ended with `meta.aborted: true` and a timeout response. Both commands nevertheless returned exit 0. We stopped after those two bounded attempts. **Neither is a successful setup behavior pass**, and the evidence does not isolate whether model speed, inference behavior or runtime overhead caused the timeout. No universal OpenClaw incompatibility is inferred.

## Corrections shipped

- Added concrete Codex, Hermes and OpenClaw native install paths and invocation instructions to the README/portability reference.
- Documented Hermes project-path anchoring and the distinction between an isolated profile and an authenticated one.
- Distinguished native discovery, successful skill reading, behavioral completion and unavailable hosts. Documented the observed OpenClaw exit-zero/aborted-result trap.

No reproducible defect in BDD's initializer, validator or core workflow was demonstrated by these runs, so no speculative runtime changes were made. No host configuration, credentials or installed model was replaced to manufacture a pass.

## Evidence and deterministic replay

[Sanitized evidence directory](artifacts/2026-10-14-native/) contains Codex command events/prompts, the source/tests and hive snapshot, Hermes setup/review output and tool results, and OpenClaw discovery/runtime outcomes. Private absolute paths use placeholders; credential stores, reasoning traces and unrelated skill catalogs are excluded. Prompts explicitly identify synthetic approval and scope.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_hive.py evals/artifacts/2026-10-14-native/codex
python3 -m unittest discover -s evals/artifacts/2026-10-14-native/codex -v
```

The fixture's nine tests and structural validation passed both in the harnesses and on coordinator replay. The package's 19 deterministic tests remain the separate CI suite. [CI runs](https://github.com/HassanOkashaa/bdd/actions) provide revision-specific results across Linux/macOS/Windows and Python 3.9/3.13.

## Remaining limitations

OpenClaw behavior remains incomplete under the tested local-model budget. Unavailable editors/CLIs, native desktop pickers, implicit skill triggering, complete UI builds, large parallel delivery, deployment and autonomous model dispatch are not certified. Hermes results apply to the inspected local build. These tests add evidence for particular paths and tasks; they do not establish support for every AI harness.
