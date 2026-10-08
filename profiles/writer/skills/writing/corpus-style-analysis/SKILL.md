---
name: corpus-style-analysis
description: "Use when analysing an author's style across a corpus."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [writing, style, stylometry, corpus, analysis, editorial]
    requires_tools: [terminal, execute_code, write_file, read_file, search_files]
    requires_toolsets: []
    requires_plugins: []
    editorial_name: "Corpus Style Analysis"
    editorial_description: "Analyse an author's voice across a whole body of work and deliver a traceable, quote-verified style pyramid."
---

# Corpus Style Analysis

Analyse how a specific author writes, across their whole published corpus, and deliver the result as
an artifact pyramid. Load `artifact-pyramids` first for the output format and
`editorial-methodology` for voice/revision discipline.

## When to use

- "Read all my blog posts and analyse my writing style"
- "What's my voice like across these N articles?"
- "Build me a style guide from this author's back catalogue"

Not for: editing a single draft (use editorial-methodology), or general summarisation.

## Pipeline

```
1. ENUMERATE   → find every item, prove the count is complete
2. EXTRACT     → fetch full text to L3 dossiers, flat files
3. STYLOMETRY  → compute stats programmatically (never estimate by eye)
4. READ        → read the whole corpus yourself before theorising
5. ANALYSE     → one L2 file per dimension
6. VERIFY      → check every quotation against the corpus
7. DELIVER     → L1 summary + 00-index; report the path
```

## Step 1 — Enumerate and prove completeness

Always establish the total from **at least two independent sources** and confirm they agree. Report
the agreement in the manifest; downstream readers must be able to trust coverage.

| Platform | Enumeration sources |
|----------|--------------------|
| Blogger | `sitemap.xml`, `/feeds/posts/default?alt=json&max-results=500` (`openSearch:totalResults`), per-page `?view=classic` |
| WordPress | `/wp-sitemap.xml`, `/wp-json/wp/v2/posts?per_page=100`, `/feed/` |
| Ghost | `/sitemap.xml`, `/ghost/api/content/posts/?key=…` |
| Substack | `/sitemap.xml`, `/archive?sort=old` |
| Generic | sitemap, RSS/Atom, on-site archive/index pagination |

**Blogger specifics:** the JSON feed returns full post HTML in one request — far better than
scraping 50 pages. Add `&max-results=500`. Each entry carries `title`, `published`, `updated`,
`link[rel=alternate]` and `content.$t`. Strip HTML with BeautifulSoup, converting `<br>` to
newlines and appending newlines to block elements, then `html.unescape`.

Pitfall: `web_extract` returns near-empty content for JS-rendered blog indexes. Try `curl` first to
inspect the raw HTML before reaching for the browser.

## Step 2 — Extract to flat dossier files

One file per item: `post-NN-YYYY-MM-DD-slug.md` under `03-dossiers/`. Include title, URL,
published, updated, word count and char count as a metadata block **before** the body.

**`03-dossiers/` must stay flat** — the artifact-pyramids spec forbids subdirectories there, because
nested paths break the SOURCES navigation contract. Prefix filenames with the index and date rather
than nesting by year.

Also emit a machine-readable `corpus-manifest.json` (title, date, year, url, words, chars,
paragraphs, dossier path) so later steps and downstream consumers don't re-parse markdown.

## Step 3 — Stylometry (the pitfalls that matter)

Compute, don't estimate. But three specific traps will silently corrupt your numbers:

### Trap 1 — Split sentences block-first, or your max sentence is garbage

Splitting on `(?<=[.!?])\s+` alone treats newlines as whitespace, so consecutive paragraphs glue
together into one "sentence". This inflated a real 56-word maximum to a bogus 74-word one.

```python
def sentences(text):
    out = []
    for block in re.split(r'\n+', text):        # paragraph first
        out += [s.strip() for s in re.split(r'(?<=[.!?])\s+', block) if s.strip()]
    return out
```

### Trap 2 — Homophone counts are not error counts

Counting raw occurrences of `there`/`its`/`then` massively overstates error rates — `there` appeared
41 times but only 9 were the `their` substitution. Hand-verify every homophone class and report
*verified misuse*, noting the raw total separately.

### Trap 3 — Apostrophe-dropping and case markers are usually partial, not absolute

Before writing "apostrophes are always dropped" or "the author always uses capital I", count both
directions. In one corpus the split was 37 dropped vs 11 kept, and 23 of 38 posts mixed `i` and `I`
*within the same post* — a far more interesting finding than either extreme.

### Metrics worth computing

- Sentence length: mean, **median**, std. deviation, % ≤5 / ≤10 / ≥30 words
- Blocks: count, mean, median (split on `\n+`, keep those >3 words)
- Punctuation per 1,000 words: `,` `;` `:` `"` `...` `-` `(` `!` `?`, list markers, P.S./EDIT
- Readability: Flesch + Flesch-Kincaid, plus **syllables per word** (1.37 = very plain, 1.55+
  formal, 1.8+ academic — often more diagnostic than the Flesch score itself)
- Pronoun density: first/second person, singular vs plural
- Sentence openers (first token) — reveals the dominant launch pattern
- ALL-CAPS tokens, emoticon counts, profanity with token breakdown
- Content words with stopwords removed
- **Per-year drift** for every one of the above (the trend is usually the story)
- Cadence: posts/year, median gap, longest gaps
- Title conventions: length, terminal punctuation, case pattern

### Vocabulary-absence testing

Grepping for the *absent* register is unusually revealing. Test the whole set:
`however, nevertheless, furthermore, consequently, arguably, therefore, moreover, thus, hence,
whereas, regarding, subsequently, utilise, methodology, perspective, paradigm, framework, leverage,
stakeholder, aspect, factor`. Zero hits for most of these, next to 96 hits for `and`, tells you more
than any positive finding. Count both coordinators and subordinators.

## Step 4 — Read the corpus yourself

Statistics describe; only reading explains. For a corpus under ~30k words, read it all before
forming a thesis. The best findings are structural and invisible to metrics — in one archive, that
posts *stop* rather than conclude, and the most affecting line was a bereavement dropped mid-list
between two conference reports.

## Step 5 — Analysis layer: one file per dimension

Standard dimension set (adapt to the corpus):

1. `voice-and-persona.md` — who speaks, to whom, what authority is claimed or refused
2. `syntax-and-rhythm.md` — sentence construction, parataxis vs subordination, fragments
3. `diction-and-orthography.md` — vocabulary layers, spelling, punctuation habits, error density
4. `structure-and-argument.md` — post shapes, how claims get defended, openings, closings
5. `genre-and-topic-map.md` — full item-by-category table totalling to the corpus count
6. `emotion-humour-and-register.md` — emotional range, humour mechanisms, surface markers
7. `evolution-<start>-<end>.md` — per-year drift and cadence
8. `influences-and-intertext.md` — every attributed source, what the prose was learned from
9. `style-playbook.md` — the findings converted to rules + a calibration checklist

Write the playbook as the practitioner deliverable: numbered imperative rules, a do/don't table, and
a short self-check. Separate what is **load-bearing for the voice** (preserve) from what is **plainly
error** (safe to fix) — that distinction is the most actionable thing you can give an author.

## Step 6 — Verify every quotation (do not skip)

**Fabrication is the dominant failure mode of this task.** Writing confidently *about* prose invites
inventing plausible-sounding quotes for it. After drafting, mechanically check every quoted span
against the corpus:

```python
norm = lambda s: re.sub(r'\s+', ' ', s.replace('\u2019', "'")).strip().lower()
CORPUS = norm("\n".join(bodies.values()))
CORPUS_NOWS = CORPUS.replace(' ', '')
# for each span: `s in CORPUS` or `s.replace(' ','') in CORPUS_NOWS`
```

Expected false positives, so filter before chasing: post titles, table cells, elision notation
(`1st of all ... 3rdly`), and words cited *because they are absent*. Everything else that fails is
a real problem — rewrite the sentence around a genuine quote.

Hyperlinks removed during HTML stripping leave an orphaned space (`from here .`), which breaks exact
matching. Either normalise around it or document the exception explicitly in the dossier header.

Also verify any **counted** claim you assert in prose ("44 distinct errors" → recount; it was 48).

## Step 7 — Assemble the pyramid

Build bottom-up, then audit:

1. L3 dossiers: per-item posts + `corpus-manifest.md`, `quantitative-stats.md`,
   `typo-inventory.md`, `exemplar-passages.md` (verbatim excerpts grouped by rhetorical move, each
   attributed)
2. L2 analysis: the dimension files, each with its own SOURCES section
3. L1 `01-summary/findings.md`: verdict, key findings, **prioritised implications**, limits
4. `00-index.md`: navigation and provenance ONLY — no findings
5. `artifact-inventory.md` at the root, with the quality-gate log

### Auditing

Run independently of the skill's helper script:

```bash
# required SOURCES only on 00-index, L1, L2 — L3 is the bottom layer
# every /home/... path in a SOURCES block must exist
# 03-dossiers must contain no subdirectories
```

**Pitfall:** `artifact-pyramids`' own `scripts/pyramid-status.sh` reports all three layers as
"Missing" for a spec-compliant project. Its `count_layer` matches *files* named `01-*`, `*summary*`,
`02-*`, `*analysis*`, `03-*`, `*dossier*`, which only works for a flat root-level layout — while the
skill's documented Project Structure uses `01-summary/`, `02-analysis/`, `03-dossiers/` as
**directories** containing kebab-case files. Do not restructure a correct pyramid to satisfy the
script; audit with your own checker and note the discrepancy in `artifact-inventory.md`.

## Reporting

Return the absolute path to `00-index.md`. Do not paste the analysis into chat — the pyramid is the
deliverable. One short paragraph may point at the headline finding and flag any caveats (small
corpus, single-post years, tool gaps).

## Corpus-size honesty

State the limitation in the L1 file and again in `00-index.md`. A 5,000-word corpus across nine
years supports *descriptive* claims about that archive, not a general profile of the author.
Percentages from a few hundred sentences are indicative. Say so before someone over-reads them.
