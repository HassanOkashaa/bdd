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

> Read `/path/to/hive-driven-development/SKILL.md` and use it for this project. Start with my goal and the project's existing instructions. Discover your actual capabilities, initialize durable state without overwriting anything, and lead me through the applicable gates.

## Resume on another harness

> Read this project's instructions and `hive/progress.md`, `hive/features.json`, `hive/approvals.md`, and `hive/config.json`, then read `/path/to/hive-driven-development/SKILL.md`. Reconcile the working tree, active workers and reports. Resume the next authorized action without repeating approved work or inventing missing verification.

Copy or attach the linked references if the host cannot open relative files. Never overwrite global `AGENTS.md`, `CLAUDE.md`, or editor rules to install this package. A project may add a short pointer to the skill by explicit choice.
