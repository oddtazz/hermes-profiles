# Writer — Hermes Profile

Drafts articles, blog posts, documentation, and long-form content. Owns structure, voice, and narrative flow.

## Installation

```bash
git clone https://github.com/oddtazz/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/writer ~/.hermes/profiles/
hermes --profile writer
```

## Skill Dependencies

Source: `shared` = repo `skills/` pool (symlinked); `bundled` = ships with Hermes, synced into the profile at runtime; `local` = lives only in this profile's `skills/`.

| Skill | Source | Provides |
|---|---|---|
| `artifact-pyramids` | shared | Progressive disclosure output format |
| `editorial-methodology` | shared | Voice discipline, structure patterns, revision protocols |
| `humanizer` | bundled | Strip AI-isms and add real voice |
| `de-ai-writing` | local | Scan for AI tells, rewrite in a human voice |
| `corpus-style-analysis` | local | Analyse an author's style across a corpus |
| `docs-example-verification` | local | Verify live API examples quoted in docs |

**Private skills (not in this repo).** The owner's voice profile, delivery, scoring and
grammar-server skills live outside the repo and load through `skills.external_dirs` in the
live `config.yaml` (see `config.example.yaml`). Without them the profile still works;
SOUL.md loads them only if installed.

## Configuration

`config.yaml` is not tracked: Hermes rewrites it. Copy `config.example.yaml` to
`config.yaml` and adjust the model and secrets for your install.

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
