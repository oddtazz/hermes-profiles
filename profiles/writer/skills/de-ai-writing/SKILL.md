---
name: de-ai-writing
description: "De-slop prose: scan for AI tells, rewrite in a human voice."
version: 1.0.0
author: Gaurav Chaturvedi (oddtazz), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, humanize, anti-ai-slop, voice, prose]
    related_skills: [humanizer]
---

# De-AI Writing (unslop methodology)

Detect and remove AI writing patterns using the deterministic scanner pipeline from [theclaymethod/unslop](https://github.com/theclaymethod/unslop) (MIT). Detection carries the weight: three stdlib-only scanners run cheaply and return JSON, then a rewrite pass rebuilds the prose under hard guards (facts, register, meaning). Voice work runs under detection's constitution — any rewrite that reintroduces a tell fails.

Two related skills exist; use all three as a toolkit:
- `humanizer` — the catalog of 34 AI patterns with before/after examples (the *what*)
- `de-ai-writing` (this) — the deterministic scanner pipeline + two-pass rewrite contract (the *how*)
- `twelve-factor` — service architecture, not writing; ignore unless you need it

## When to Use

- "Humanize / de-slop / de-AI / clean up" a piece of writing (blog post, essay, PR description, docs, memo, email, LinkedIn post, resume bullet)
- "Make this sound human / not like ChatGPT / less robotic"
- "Audit / flag the AI tells, don't change anything" before publishing
- Reviewing your own draft output before delivery (Hermes's own prose included)
- Don't use for: code review, math, or anything non-prose; writing in a non-English language (scanners decline non-English input)

## Prerequisites

- Python 3.8+ with stdlib only — no pip installs.
- Scanner scripts are vendored under `scripts/` in this skill directory. They run standalone: `python3 scripts/<scanner>.py < input.txt`.
- If you're in a repo and the `scripts/` dir is missing, `git clone --depth 1 https://github.com/theclaymethod/unslop.git` and point at `unslop/scripts/`.

## Quick Reference

```bash
# Detection (JSON to stdout; exit 1 if flagged)
python3 scripts/banned_phrase_scan.py < in.txt            # phrase layer: 16 literal triggers, quoted spans masked
python3 scripts/banned_phrase_scan.py --include-quoted < in.txt
python3 scripts/structure_scan.py < in.txt                # structure layer: 36 patterns + rhythm/coda metrics
python3 scripts/structure_scan.py --genre docs < in.txt   # reference-doc carve-outs (bold-label lists OK)
python3 scripts/silhouette_scan.py < in.txt               # silhouette layer: idea-arrangement tells (needs 3+ paragraphs)

# Preservation and diff checks
python3 scripts/extract_constraints.py < in.txt
python3 scripts/validate_preservation.py original.txt transformed.txt
python3 scripts/validate_preservation.py --strict original.txt transformed.txt   # legal/medical/security/scientific
python3 scripts/diff_check.py original.txt transformed.txt                        # over-edit guard (40% max change)
python3 scripts/readability_metrics.py < in.txt

# Co-writer suggestions
python3 scripts/suggest.py document.md
python3 scripts/check_suggestions.py suggestions.json     # 4 contract gates: span-minimality, replacement-scanner, accept-all, span-overlap
```

## Procedure

### A. Audit-only ("just flag it" / "review before I publish")

1. Run all three scanners on the text (or a file). Note: quoted spans and code fences are exempt by default; use `--include-quoted` only to audit examples inside docs.
2. For each flag, judge context: is it a genuine AI tell, or a literal/domain/quoted use (protected)? A scanner match alone never authorizes an edit.
3. Report as a list: quoted span, category, severity (hard = always a tell, soft = register guard your real voice can override), and why it reads as AI.
4. Separate clear problems from judgment calls (soft cadence, document-shape metrics) in the report.

→ Done when: every flag is either confirmed-as-tell or explained as protected (literal, quoted, domain-valid, genre-natural, attributed, caveated).

### B. Rewrite (default; the two-pass contract)

**Pass 1 — Diagnose:**
1. Run the three scanners; record violations.
2. Extract must-preserve constraints: `python3 scripts/extract_constraints.py < original.txt` — numbers, names, dates, quotes, units, citations, `and/or`, negations, scope words, register hedges ("never store secrets", "may cause drowsiness", "does not establish causation").
3. Identify the *smallest defective span* for each confirmed tell. Do NOT fact-check or infer truth from outside knowledge; missing proof alone isn't a defect.

**Pass 2 — Reconstruct:**
4. Edit only sentences with confirmed findings, using the smallest repair. Copy every other sentence byte-for-byte, in order.
5. Preserve facts, quantities, dates, names, quotes, citations, code, units, scope, uncertainty, attribution, register, and meaning. Add nothing: no claims, advice, personality, anecdote, certainty, or conclusion.
6. Preserve force-bearing "never", "must", "all" exactly in safety/security/legal/technical rules. Magnitude matters: `$47.3M` must not become `$47.3 billion`; `150 km` must not become `150 miles`.
7. No staccato anti-slop prose, no stock-phrase substitution, no mic-drop closers. Trust the reader; cut what carries no meaning.
8. Voice presets (optional): read one of `references/presets/*.md` before writing — `crisp` (technical/docs), `warm` (emails/blog), `expert` (thought leadership), `story` (case studies). Presets change delivery, not facts.
9. With no findings: return the source exactly. Byte-exact no-op on clean prose is the required behavior.

**Pass 3 — Validate:**
10. Run the full battery; block on any failure:
```bash
python3 scripts/validate_preservation.py original.txt transformed.txt     # (--strict for regulated text)
python3 scripts/banned_phrase_scan.py < transformed.txt
python3 scripts/structure_scan.py < transformed.txt
python3 scripts/silhouette_scan.py < transformed.txt
python3 scripts/readability_metrics.py < transformed.txt
python3 scripts/diff_check.py original.txt transformed.txt                # excessive_change flag = over-editing
```
11. Strict mode (user asks, or legal/medical/security/scientific text): score the rewrite on the 8-criterion rubric (directness, natural rhythm, concrete verbs, reader trust, human authenticity, content density, fact preservation, template avoidance) — fail below 32/40. Rubric: `references/rubric.md`.

→ Done when: all hard scanner flags cleared, preservation passes (or `--strict` fails on nothing), no introduced anti-slop register, diff under the over-edit threshold, and every sentence that wasn't defective is byte-identical.

### C. Co-writer ("suggest edits, don't rewrite")

1. Run `scripts/suggest.py document.md` for structured suggestions (span, severity, category, rationale, proposed replacement). Hard findings become direct replacements; soft findings are phrased as questions.
2. If you accept suggestions wholesale, run `scripts/check_suggestions.py suggestions.json` — the four contract gates make "accept all" safe: span-minimality, replacement-scanner, accept-all, span-overlap.

→ Done when: every suggestion passes the four gates, or unaccepted suggestions are listed as judgment calls.

## The Tell Catalog (What to Catch)

Full catalog: `references/taboo-phrases.md` (36 categories, 1,183 lines). The scanner packs ship in `references/packs/`. Headline families:

- **Openers/emphasis/inflation:** "Here's the thing:", "Let me be clear", "It turns out", "Full stop.", "Let that sink in.", "The struggle is real.", "stands as a testament to", "pivotal moment", "rich tapestry", "the numbers speak for themselves"
- **Contrast/questions/drama:** "It's not X, it's Y", "Not only... but also", "Why does this matter? Because...", "[Noun]. That's it. That's the [thing].", "(arguably ...)"
- **Attribution/flattery/jargon:** "Experts argue", "Studies show", "worth reading", "Whether you're a seasoned developer or just starting out", "navigate challenges", "leverage synergies", "circle back", "world-class", "state-of-the-art"
- **Chatbot residue/punctuation:** "I hope this helps", "Certainly!", "Great question!", "as an AI language model", "as of my knowledge cutoff", emoji headers, em-dash overuse (2+ per paragraph is a hard flag), "Let me think step by step"
- **Structural/silhouette:** uniform sentence rhythm, staccato one-line paragraphs, connective scaffolds ("However," / "Moreover," openers), moralizing codas ("Ultimately, this reminds us that..."), outline-following arrangement, recap loops, callback vocabulary
- **Macro tells left to agent judgment** (no scanner): both-sidesism, templated redemption arcs, over-determination, uniform emotional register

## What Gets Protected (Do-No-Harm)

- **Register guards** — legal/medical/security/scientific hedges, negations, absolutes, scope words carry meaning: "never store secrets", "may cause drowsiness", "does not establish causation", "notwithstanding anything to the contrary"
- **Literal domain usage** — construction, mechanics, law, medicine, finance, sailing, code use gated words literally; contextual gating, not word bans
- **Quoted examples** — quoted spans, blockquotes, code fences exempt by default
- **Facts with magnitude awareness** — numbers, names, dates, quotes, units, references like `Section 12(b)`, `and/or` scope
- **Genre carve-outs** — bold-label lists OK in reference docs (`--genre docs`), staccato OK in social copy (`--genre social`), section-roadmap abstracts are academic convention
- **English only** — non-English input gets cheap detection and a clear decline

## Pitfalls

- A scanner match is not an edit warrant. Literal, domain-valid, quoted, attributed, and genre-natural uses stay. The decision rule: return a finding only when the contextual defect is clearer than preservation.
- Detection is not the whole product. The unslop maintainers' own public benchmark is a **no-ship** on the core bar (recall/repair improved over plain model, precision/damage bar not yet met). The scanners are a trust asset and a guardrail, not a proof that a rewrite improved writing.
- Quoted examples are exempt by default so a tutorial documenting bad writing doesn't flag its own examples.
- Em-dash overuse is the single most reliable punctuation tell; the default is zero per paragraph.
- Silhouette scanning needs 3+ prose paragraphs; below that it returns "not scored".
- Don't over-edit: `diff_check.py` flags >40% change. Byte-exact no-op on already-clean prose is a feature.
- The scanners decline non-English input (cheap detection + clear refusal) rather than guessing.
- Rewriting only (no detection first) is how slop survives: an LLM rewriting an LLM draft without gates reproduces the same tells. Always diagnose before reconstruct.

## Verification

- Audit: every flag confirmed-as-tell or explained as protected; report separates clear problems from judgment calls.
- Rewrite: preservation passes, zero hard flags remain, no new anti-slop register, diff under threshold, clean prose returns byte-identical.
- Co-writer: all suggestions pass the four gates.

## References

- Source repo: https://github.com/theclaymethod/unslop (MIT) — README documents the full methodology, the three detection layers, and the eval suite.
- `references/taboo-phrases.md` — authoritative tell catalog (vendored from unslop).
- `references/packs/` — scanner rule-packs + manifest (vendored).
- `references/presets/` — crisp/warm/expert/story voice deltas (vendored).
- `references/rubric.md` — strict scoring criteria (vendored).
- `scripts/` — scanner and validation scripts (vendored from unslop, stdlib-only, run standalone).
- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — source of part of the catalog; `scripts/wiki_sync.py` can sync new patterns eval-first.
