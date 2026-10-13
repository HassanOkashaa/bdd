# Worked example: a reading-list app

This is a synthetic walkthrough, not evidence of a completed build.

**User request:** “Build a small app where I save articles to read later.”

1. The coordinator inspects the existing project and asks about only consequential unknowns, such as whether data must sync between devices.
2. For the new UI, the designer presents rendered alternatives with realistic sample articles. The user views and selects one. The coordinator records the exact artifact and approval in `hive/approvals.md`.
3. The plan proposes F01 save/list/persist, F02 prevent duplicates and validate URLs, F03 mark as read. Dependencies and observable acceptance are explicit. The user approves.
4. F01's builder receives ownership of the relevant persistence and list files, plus the agreed contract. It demonstrates persistence after restart with an integration test.
5. Automated checks run. A fresh reviewer reads the diff and acceptance criteria; a tester saves an article in the running app and restarts it. If storage is only in memory, the feature fails regardless of how good the screenshot looks.
6. The coordinator integrates, reruns relevant checks, and records evidence for the integrated revision before marking F01 passed.
7. The next session reads progress and continues F02. No approved direction needs to be reinvented.
8. The completed app is described as verified locally. Hosting credentials and production release remain separate decisions.

**Single-agent variant:** the builder leaves a review packet for a fresh assistant session or a human. F01 remains `verifying` or `blocked` until required independent evidence arrives. Renaming the same agent “Inspector” does not make the review independent.
