# Coder — Hermes Profile

Implementation engineer — turns requirements and bug reports into tested, shippable code. TDD-first: test, then implement, then verify, then clean up.

## Installation

```bash
git clone https://github.com/oddtazz/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/coder ~/.hermes/profiles/
hermes --profile coder
```

## Skill Dependencies

Source: `shared` = repo `skills/` pool (symlinked); `bundled` = ships with Hermes, synced into the profile at runtime; `local` = lives only in this profile's `skills/`.

| Skill | Source | Provides |
|---|---|---|
| `artifact-pyramids` | shared | Progressive disclosure output format |
| `test-driven-development` | bundled | RED-GREEN-REFACTOR — tests before code |
| `requesting-code-review` | bundled | Pre-commit verification: security scan, quality gates, independent reviewer |
| `simplify-code` | bundled | Parallel 4-agent cleanup pass before presenting changes |
| `twelve-factor-agents` | local | Design rules for LLM agents and tool-calling loops |

## Configuration

`config.yaml` is not tracked: Hermes rewrites it. Copy `config.example.yaml` to
`config.yaml` and adjust the model and secrets for your install.

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
