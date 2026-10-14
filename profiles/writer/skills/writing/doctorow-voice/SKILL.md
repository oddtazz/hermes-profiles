---
name: doctorow-voice
description: "Use when writing in Cory Doctorow's voice or style."
version: 1.0.0
author: Tazz (oddtazz), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, voice, style, pastiche, essay, doctorow, pluralistic]
    related_skills: [de-ai-writing, corpus-style-analysis, editorial-methodology]
    editorial_name: "Cory Doctorow Voice Profile"
    editorial_description: "Write polemical tech-and-power essays in the style of Cory Doctorow's Pluralistic, derived from 2.6M words of his own prose."
---

# Cory Doctorow Voice Profile

Write prose in the style of Cory Doctorow: the Pluralistic essay register by default, with notes for his
reviews, personal pieces and fiction. Pair with `de-ai-writing` before delivering.

**Provenance.** Distilled from every Pluralistic issue (1,730 issues, 2020-02 to 2026-10, split into 2,874
essays, 2,635,282 words of his own prose), 13 CC-licensed books from Project Gutenberg (584,699 words of
fiction), and 445 craphound.com posts. Boing Boing (2001-2020) and Locus columns were firewalled and are
**not** in the corpus. Full evidence, verbatim exemplars and statistics:
`~/research/cory-doctorow-writing-style/00-index.md`

## When to Use

- "Write this like Cory Doctorow", "in the style of Pluralistic", "Doctorow-style essay/rant/review"
- Polemics about tech, monopoly, labour, copyright or finance where Tazz wants that register
- Critiquing a draft against his voice

Don't use for: passing text off as Doctorow's own work, inventing quotes or positions and attributing them
to him, or anything signed with his name. Style is fair game. Impersonation is not.

## The controlling principle

> **Explain how power works to a smart friend who is about to get screwed, with receipts, and be angry about it.**

Every rule below follows from this. He is a *systems explainer* who happens to be furious, not a ranter who
happens to explain. Each essay names a mechanism, shows it working in concrete cases, says who benefits,
and ends on what to do or a verdict on the culprit.

## The eight load-bearing traits

### 1. Open on the thesis, stated as a mechanism

No throat-clearing. The first paragraph (median 38 words) is the claim, often as a process or a law of
nature. Three openings he uses, by frequency:

- **Mechanism-thesis:** `Here is how platforms die: first, they are good to their users; then they abuse their users to make things better for their business customers; finally, they abuse those business customers to claw back all the value for themselves. Then, they die.`
- **News hook + colon + link (26% of essays):** `This is huge: yesterday, the FTC finalized a rule banning noncompete agreements for every American worker.`
- **First-person anecdote (9%):** `I have complex chronic pain, and I've seen a lot of specialists.`

Also: a paradox to resolve. `It may strike you as weird, but lenders love to lend money to poor people who will have trouble paying back their loans.`

### 2. Name the thing, define it, then use the name relentlessly

He coins a plain-English (often rude) term, defines it in one sentence, and repeats it as the essay's spine.
`I call this enshittification` is followed by `This is enshittification:` and then forms of the word 26 more times in the same essay.
Corpus counts: enshittification and its forms 1,284, "Big Tech" 1,001, bezzle(s) 181, the twiddling family
191, reverse centaur(s) 177, "felony contempt of business model" 59.

- The definition is a structure: `That's a worker who has to foot the bill to outfit a work environment where they nevertheless have no autonomy (chickenization) and whose body is conscripted to act as a peripheral for a digital system (reverse centaur)`
- New coinages are concrete and slightly absurd: "money-furnaces", "word-guessing programs", "Magic Underpants Gnomery".
- **Use his existing terms only for what they actually mean.** Enshittification is the specific three-stage platform-decay mechanism, not "anything getting worse". He polices this himself.

### 3. Receipts: colon, then the source

His most frequent structural habit (4.7 per 1,000 words; median 7 per essay): a sentence ends on a colon and
the next paragraph is a bare link. Claims are sourced, and named reporters get credit
(`Forbes's Emily Baker-White broke a fantastic story`).

- **Never invent a URL, a study, a statistic or a reporter.** If you don't have the real source, write
  `[source needed]` on its own line after the colon and tell Tazz. A fabricated receipt is worse than none.
- Without links (a short post, a piece for print), keep the habit as named attribution in the sentence.

### 4. Rhythm: medium sentences, wide swing, short paragraphs

- Sentence median **20 words**, mean 21, SD 13. 23% are 10 words or fewer and 25% are 30+. Both ends are needed.
- Paragraph median **39 words**, usually 1-2 sentences. 30-44% of paragraphs are a single sentence.
- The long sentence is a **catalogue**: piled clauses or a list of named victims (`It's what happened to nursing homes, Armark, private prisons, funeral homes, pet groomers...`).
- The short one is a **punch**, often its own paragraph, often a sarcastic gloss: `You know: "business."`
- Plain words: 1.63 syllables per word, FK grade 12. The ideas are complex. The vocabulary is not.

### 5. Punctuation fingerprint

Per 1,000 words: comma 57, straight double quote **20**, colon **9.7**, spaced en dash ` – ` **7.1**,
parenthesis **5.0**, question 1.6, exclamation 1.1, semicolon 1.0, **em dash 0.2**.

- **Spaced en dash ` – ` for asides and pivots, never the em dash.** `Pharma companies – led by Purdue Pharma, makers of Oxycontin, owned by the secretive billionaire Sackler family, who once threatened to sue me for criticizing them – deliberately created the epidemic`
- **Scare quotes on the enemy's euphemisms:** "monetize", "free", "AI", "efficiencies", "business".
- **Parentheses for the snide gloss:** `(comparatively honest)`, `(which you don't own!)`, `(and notorious tax-evader)`.
- **Colons do the setting up:** before a list, a link, a definition, a punchline.
- **Roman numerals** (I., II., III.) when he enumerates a scheme step by step (5% of essays).

### 6. Strip the jargon, then mock it

The core comic engine. Euphemisms get translated into crimes:
`Take "leveraged buyout," a polite name for stealing a whole goddamned company:` /
`"financial engineering" is really just a euphemism for "fraud"` /
`"work from home" is a thin euphemism for "live at work."`

Then he demolishes the defenders' analogy on its own terms:
`Private equity managers are like sea captains in exactly the same way that leveraged buyouts are like mortgages: not at all.`

### 7. One homely analogy, extended, then used as a refrain

He picks a carnival game, a schoolyard or a toddler, runs it for a paragraph or two, and comes back to it:

- `The peach-basket is a rigged game. The carny can use a hidden switch to force the balls to bounce out of the basket.` Later: `In other words, Tiktok is handing out giant teddy bears.`
- `giving a creator more copyright is like giving a bullied schoolkid extra lunch money`
- `Audible is like a toddler that won't let their broccoli touch their peas – only that toddler is also a rapacious monopolist that keeps 75% of every sale.`

For corporations he uses grotesque biology: `just another paperclip-maximizing artificial colony organism that treats human beings as inconvenient gut flora`.

### 8. Contempt aimed up, sympathy aimed down

Profanity appears in 40% of essays (0.8 per 1,000 words). It lands on billionaires, executives, monopolists
and their apologists, never on workers, users or the people being scammed. Readers are "you", the person
being ripped off (6.8 per 1,000 words). Mockery is specific and personal for the powerful:
`These guys – these terrible, mediocre, boring-ass losers – are bullshit factories` /
`A serial liar like Sam Altman will someday trip over his own dick`.

Underneath sits an optimist's politics: the problem is *policy choices*, so it can be fixed. Antitrust,
interoperability, right to repair, end-to-end and freedom of exit come up, along with democratically
accountable law in place of "corporate decree".

## Essay skeleton (Pluralistic register)

1. **Thesis or hook.** One paragraph, the claim, colon, link.
2. **Name the mechanism.** Coin or invoke the term and define it in one sentence.
3. **Walk the cases.** Two to five concrete examples (company, number, date, reporter), each a short paragraph with its receipt. `Think of Amazon:` / `Take X.`
4. **Translate and mock.** Strip the euphemism, scare-quote the jargon, hit the bad analogy.
5. **Extend the analogy.** One homely image, returned to later as a refrain.
6. **Concede, then turn.** `Now, it's possible to imagine that...` / `That doesn't make AI useless, it just makes it a normal technology` / `Sure:`
7. **Zoom out to policy.** What law or remedy fixes it, and why the current regime lets it happen. `That's why laws, not corporate decree, should determine...`
8. **Close on a kicker or verdict.** Last paragraph median 22 words. Never a summary. `Uber is a bezzle, and every bezzle ends.` / `Cool story, bro.` / `Enshittification truly is how platforms die. That's fine, actually.` About 15% of essays end on one last colon and link. 3% end on a question.

Pivot words between sections: `Which brings me to`, `In other words`, `That's why`, `That's how`,
`Now,`, `But`, `Remember`, `Think of`, `Take`. Sentence-initial "But" runs at 2.2 per 1,000 words.

## Register dial

| Register | Shape | Differences from the default |
|---|---|---|
| **Pluralistic essay** (default) | Skeleton above, 700-2,500 words | Baseline numbers |
| **Book review** | Opens on the author's reputation or the book's argument, summarises generously, closes with a recommendation | Superlatives allowed (`brilliant`, `gripping`), little profanity, no policy turn |
| **Personal / memoir** | First-person anecdote that becomes the argument | More "I" and specific places (Burbank, Toronto); still ends on the point |
| **Short post / link note** | 150-400 words: hook, the receipt, one gloss, a verdict | Mostly 1-sentence paragraphs |
| **Fiction (YA, Little Brother era)** | First-person teen narrator, scene-driven | Sentence median **9**, "I" 17/1k, questions 7/1k, `*italic*` emphasis, mid-scene lectures to "you" (`You've encountered this before.`). Plain diction (1.40 syllables per word, FK grade 6) |

Say which register you picked when you deliver.

## Overrides of generic anti-slop rules

These are soft tells in the `de-ai-writing` catalogue but they are **authentic here**. Don't strip them:

| Generic rule | Why it doesn't apply |
|---|---|
| "Cut 'In other words' / 'Here's how' signposts" | He uses them (0.14 and 0.10 per 1k) to return to the analogy or open a mechanism walk. Keep them sparing. |
| "Avoid scare quotes" | 20 per 1k. Quoting the enemy's euphemism is the joke. |
| "Cut sentence-initial But/And" | "But" opens 5,941 sentences in the corpus. |
| "Avoid profanity / invective" | 40% of essays. Aim it upward. |
| "Avoid lists" | Catalogues of victims and Roman-numeral schemes are his. |
| "Avoid coinages" | Naming is the method. |

Still forbidden (all at or below 0.06 per 1k in 2.6M words): `however`, `moreover`, `furthermore`,
`although`, `delve`, `tapestry`, `testament`, `paradigm`, `seamless`, `stakeholder`, `landscape`,
`notably`, `crucially`, `arguably`, plus "in today's", "it's important to note", "plays a vital role",
"at its core", "in conclusion". No em dashes. No balanced both-sides paragraph. He concedes a point in
order to demolish it.

## Pitfalls

- **Pastiche by catchphrase.** Dropping "enshittification", "eminently guillotineable" and "cool story, bro"
  into a piece is cosplay. Reuse the *moves* with new words. Only use his terms when the piece is actually
  about those mechanisms.
- **Rant without mechanism.** Anger alone is not his voice. If a paragraph is angry but explains nothing
  (who profits, how, by what rule), it's wrong.
- **Fake receipts.** The colon-link habit pulls hard toward inventing citations. Never do it. Use real
  sources or `[source needed]`.
- **Attributing positions.** Don't write "as Doctorow argues..." for claims you haven't verified in the corpus.
- **Over-shortening.** His median sentence is 20 words, not 10. Punchy one-liners only work beside long,
  stacked sentences.
- **Era drift.** 2020 is choppier (64% one-sentence paragraphs, many linkdump items). 2023-26 is denser
  (paragraph median 48-54 words, sentence median 20-22). Default to the 2023-26 register.
- **Corpus gap.** The Boing Boing years (2001-2020) aren't here, so the blog voice of that era is unmeasured.

## Verification

1. **First paragraph states the claim?** If you could cut it and lose nothing, it was a frame.
2. **Is there a named mechanism with a one-sentence definition?**
3. **Every factual claim has a real source or `[source needed]`?** No invented URLs, numbers or reporters.
4. **At least one euphemism stripped and one homely analogy extended?**
5. **Spaced en dashes, no em dashes? Scare quotes on the enemy's words? Parenthetical snark?**
6. **Is the contempt aimed at the powerful, and is the reader addressed as the one being ripped off?**
7. **Policy turn present (for essays)? Ending a kicker or verdict, not a summary?**
8. **No catchphrase cosplay, and nothing attributed to Doctorow himself?**

Then run the mechanical gate:

```bash
python3 scripts/doctorow_check.py draft.md          # exit 1 = revise; add --quiet to show only problems
```

It checks sentence and paragraph distributions, dash, colon, parenthesis and quote rates, banned
connectives, AI framing phrases, second-person density, and the opening and closing moves. Calibration:
**about 91% of real Pluralistic essays pass with zero FAILs** (180/200 and 184/200 on two random
samples). A generic chatbot-register essay on the same subject fails with 5 FAILs. WARNs are judgement
calls. FAILs mean revise.

Then run the `de-ai-writing` phrase and structure scanners, honouring the overrides above.
**Ignore `silhouette_scan.py` for this voice.** It flags 58 of 60 random real Pluralistic essays,
mostly through `callback_content` and `preview_fulfillment`. Thesis-first openings and closing on the
coined term are how he builds an essay, not a tell.

A semicolon WARN on a policy paragraph is acceptable. He does write "do X; do Y; and do Z" remedy lists,
just rarely (1.0 per 1k).

## Reference

`~/research/cory-doctorow-writing-style/00-index.md`

- `01-summary/findings.md`: the verdict and key findings
- `02-analysis/*.md`: voice, syntax and punctuation, structure, lexicon, registers and drift
- `03-dossiers/exemplar-passages.md`: 59 verbatim passages grouped by move (build fails if any is not verbatim)
- `03-dossiers/quantitative-stats.md`: every number in this skill
- `03-dossiers/calibration-draft.md`: a test essay written with this skill, with its gate output
