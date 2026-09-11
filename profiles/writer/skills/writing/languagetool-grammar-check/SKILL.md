---
name: languagetool-grammar-check
description: Use when checking grammar via the LanguageTool API.
---

# LanguageTool Grammar Check

Check text against a self-hosted LanguageTool server and return clean, cited corrections.

## Server

- Base URL: `http://10.100.10.252:9099/v2/`
- Version observed: 6.8 (community build, `premium: false` — free rules only)
- Swagger reference: https://languagetool.org/http-api/swagger-ui/#/default

## Endpoints

- `GET /v2/languages` — list supported languages (`name`, `code`, `longCode`)
- `POST /v2/check` — the grammar check (primary endpoint)

## Check request

Form-encoded (simplest, most reliable):

```bash
curl -s -m 30 -X POST "http://10.100.10.252:9099/v2/check" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "text=<TEXT>" \
  --data-urlencode "language=en-US"
```

JSON alternative (content-type `application/json`, body `{"text": "...", "language": "en-US"}`).

### Useful parameters

- `text` (required) — the text to check. Max ~20 KB by default.
- `language` (required) — e.g. `en-US`, `en-GB`, `de`, `fr`. Auto-detect with `auto`.
- `motherTongue` — e.g. `de` for false-friend checks (non-English native speakers).
- `enabledRules` / `disabledRules` — comma-separated rule IDs.
- `enabledCategories` / `disabledCategories` — e.g. `TYPOS`, `GRAMMAR`, `STYLE`.
- `enabledOnly` — `true` to use ONLY the enabled rules.
- `level` — `default` or `picky` (more aggressive, more false positives).

## Check response (JSON)

Top-level keys: `software`, `warnings`, `language`, `matches`, `sentenceRanges`.

Each `match` has:
- `message` — human explanation
- `shortMessage` — short label
- `replacements` — array of `{"value": "..."}` suggested fixes
- `offset` / `length` — character span in the input text
- `rule` — `{id, description, category:{id, name}, issueType}` (issueType ∈ `grammar`, `misspelling`, `style`, `typo`)
- `context` — `{text, offset, length}` and `sentence` — surrounding context

## Parsing workflow

1. POST the text and get JSON.
2. Collect `matches`. Ignore when `warnings.incompleteResults` is `true` (text too long) — split and re-check.
3. For each match, apply `replacements[0].value` by offset/length to reconstruct a corrected version, or just present `message` + `replacements` to the user.
4. Report per-match: the flagged phrase, the explanation, and the suggested fix.

## Response format for the user

Present corrections as a list, one bullet per match:

```
- `flagged phrase` → suggest "fix" (RULE_ID — issueType)
  explanation
```

Optionally append a fully corrected rewrite of the text.

## Pitfalls

- Offsets are in UTF-16 code units, not bytes — slice carefully with non-ASCII text.
- `picky` level returns many more matches; default to `default` unless the user asks for strict checking.
- Community build has no premium rules (e.g. some advanced style rules). Don't claim premium coverage.
- Always URL-encode the text with `--data-urlencode` so quotes, `&`, and newlines survive.
