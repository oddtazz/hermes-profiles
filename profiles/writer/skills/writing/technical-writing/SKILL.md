---
name: technical-writing
description: "Use when writing or reviewing a tech article or tutorial."
version: 0.1.0
author: Gaurav Chaturvedi (oddtazz), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, technical-writing, blog, tutorial, editing, explanation]
    related_skills: [editorial-methodology, de-ai-writing]
---

# Technical Writing Skill

How to write technical articles people finish: blog posts, tutorials, how-tos,
explainers, case studies, postmortems, READMEs with prose. Built from 13 sources
(Lynch, Evans, DigitalOcean, Google, Diátaxis, Smashing, Graham, NN/g). The full
rules with source tags are in `references/principles.md`; verbatim excerpts with URLs
are in `references/sources-*.md`.

This skill covers **what goes on the page and in what order**. `de-ai-writing`
still owns AI tells. If installed, `tazz-voice` owns Tazz's register and
`article-evaluator` gives an optional second-opinion score.

API references, READMEs and CLI help belong to `technical-documentation`
(exhaustive reference docs). This skill is for articles people read start to finish.

## When to Use

- Drafting any technical article, tutorial, how-to, explainer, or dev blog post
- Reviewing or editing someone's technical draft ("is this good?", "tighten this")
- Turning notes, a debugging session, or code into a write-up
- Don't use for: API reference tables, commit messages, or fiction

## Quick Reference

```bash
python3 scripts/tech_article_check.py draft.md          # findings + opening + skim view
python3 scripts/tech_article_check.py draft.md --json   # machine-readable
```

Exit **0** = no hard findings, **1** = hard findings, **2** = usage error (missing or empty file).
Run it through `terminal` from this skill's directory. Stdlib Python only.

## Procedure

### 1. Reader card (before any prose)

Write these five lines into the working notes. If any line is blank, don't draft yet.

1. **Reader:** one real or concrete person, their role, and what they already know.
2. **Terms:** words they know vs. words that must be explained on the page.
3. **Payoff:** what the reader can do, understand, or believe afterwards, in one sentence.
4. **Type:** exactly one of tutorial / how-to / reference / explanation / case study / opinion.
5. **Route:** where this reader will find it (search query, HN, Lobsters, a subreddit, a team wiki).

→ *Done when:* all five lines are filled, and the payoff passes Graham's test: true, matters, new to most readers.

### 2. Outline as a skim view

Write the title, the first three sentences, and the H2 headings, and nothing else.
The title plus three sentences must answer "is this for me?" and "what do I get?"
Each heading states a claim or a result ("Nothing you install survives the exit"),
not a topic ("Overview").

→ *Done when:* someone reading only the outline could retell the article.

### 3. Draft (creative mode, don't edit)

- Put something concrete before every abstraction: a command, real output, a real bug.
- Build examples from real code. Strip irrelevant details, don't invent toy domains.
- Introduce one new concept per paragraph. Analogies make one point and stop.
- After every code block, write what it does and why. Explain the flags.
- Prove claims: show output, a failing case, or a number with its source.
- Follow the genre rule for tone (see `references/principles.md` §5). Blog posts written as Tazz also go through `tazz-voice`.

### 4. Review (critical mode)

1. Run `tech_article_check.py`. Fix every **hard** finding. For each **soft** finding, fix it or note why it stays.
2. Answer the four "JUDGE BY HAND" questions it prints, in writing, against the reader card.
3. Term audit: every technical term not on the reader's "knows" list gets a one-sentence gloss where it first appears.
4. Run the `de-ai-writing` scanners. For Tazz pieces, also run the `tazz-voice` gate.
5. Optional: run `article-evaluator` for a score, following its noise rules.

→ *Done when:* the checker exits 0, all four manual answers are "yes", the term audit is clean, and the voice and AI-tell gates pass.

### 5. Report

When handing over, state the reader, type and payoff in one line each, and list anything
left open (an untested command, an unverified number). Never claim a command works
unless it was actually run.

## Pitfalls

- **The checker is mechanical.** It can't judge payoff, correctness, or reader fit. A
  clean exit only means none of the detectable rules were broken. The manual questions
  are the real gate.
- **"just" and "simple" are soft on purpose.** "just one file" (meaning *only*) is fine.
  "just configure nginx" is not.
- **The acronym check over-fires** on names the reader certainly knows. Judge each one against the reader card.
- **Quoted lines (`>`) are exempt** from word checks, so an article *about* bad
  phrasing doesn't flag its own examples.
- **Generic headings are fine in reference docs and DigitalOcean-style tutorials**
  ("Prerequisites", "Step 1 — …"). The rule targets blog and explainer articles.
- **Don't fix length by cutting reasoning.** Cut preamble and repetition, keep the "why".
- **Tutorials creep into explanation.** Give one line ("we use HTTPS because it's safer")
  and link out (Diátaxis).

## Verification

- `tests/fixtures/bad.md` exits 1 with 8 hard findings (preamble, sequel, simply,
  obviously, powerful, link text "here", unexplained code block, easy).
  `tests/fixtures/good.md` exits 0 with zero findings. A missing file exits 2.
  `tests/fixtures/mentions.md` checks that quoted mentions are exempt.
  Run `python3 -I tests/test_checker.py` after any edit to the script.
- A delivered article has a reader card, a clean checker run on the exact delivered
  text, and written answers to the four manual questions.
