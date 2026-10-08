# Researcher — Hermes Profile

Deep-dive research specialist — scans sources, gathers evidence, triangulates findings, and produces structured briefs and synthesis reports.

## Installation

```bash
git clone https://github.com/oddtazz/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/researcher ~/.hermes/profiles/
hermes --profile researcher
```

## Skill Dependencies

Source: `shared` = repo `skills/` pool (symlinked); `bundled` = ships with Hermes, synced into the profile at runtime; `local` = lives only in this profile's `skills/`.

| Skill | Source | Provides |
|---|---|---|
| `artifact-pyramids` | shared | Progressive disclosure output format |
| `research-methodology` | shared | Source evaluation, triangulation, synthesis |
| `researcher-workflow` | shared | Non-interactive deep research pipeline for assigned tasks |

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
