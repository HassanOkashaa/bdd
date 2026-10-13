# Contributing

Small, evidence-backed improvements are welcome. Open an issue with the user problem, host/version, operating mode, expected outcome, and observed outcome. Use synthetic or redacted artifacts; never upload credentials or private project state.

For a change:

1. Keep `SKILL.md` focused on decisions that improve delivery. Put conditional details in references.
2. Preserve the generic Markdown/file contract. Host adapters may document additional capabilities but must not become core dependencies.
3. Run `python3 -m unittest discover -s tests -v` when setup tooling changes.
4. Run relevant scenarios in `evals/scenarios.md` for behavior changes and record actual results, host/model, limitations and artifact references. Clearly distinguish a paper review from an executed evaluation.
5. Submit a pull request explaining the problem, change and evidence. Do not add compatibility badges or production-readiness claims without testing.

By contributing, you agree that your contribution is provided under this repository's MIT license.
