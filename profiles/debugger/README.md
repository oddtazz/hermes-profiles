# Debugger — Hermes Profile

Systematic debugger — finds root causes before fixing. Expert in error investigation, reproduction, and test-driven debugging.

## Installation

```bash
git clone https://github.com/oddtazz/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/debugger ~/.hermes/profiles/
hermes --profile debugger
```

## Skill Dependencies

Source: `shared` = repo `skills/` pool (symlinked); `bundled` = ships with Hermes, synced into the profile at runtime; `local` = lives only in this profile's `skills/`.

| Skill | Source | Provides |
|---|---|---|
| `artifact-pyramids` | shared | Progressive disclosure output format |
| `debugging-methodology` | shared | Root cause analysis, reproduction, isolation, verification protocols |
| `root-cause-debugging` | shared | 4-phase root cause protocol: understand the bug before fixing it |

## Configuration

`config.yaml` is not tracked: Hermes rewrites it. Copy `config.example.yaml` to
`config.yaml` and adjust the model and secrets for your install.

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
