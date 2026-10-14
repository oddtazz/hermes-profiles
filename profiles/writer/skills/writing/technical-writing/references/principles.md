# Technical writing principles (with sources)

Distilled from 13 sources read on 2026-10-14. Verbatim excerpts with URLs are in
`references/sources-*.md`.
Source tags: S1-S2 Michael Lynch (Refactoring English), S3-S5 Julia Evans (jvns.ca),
S6 DigitalOcean guidelines, S7 Google Technical Writing One, S8 Diátaxis,
S9 Smashing Magazine, S10-S11 Paul Graham, S12-S13 Nielsen Norman Group.

## 1. Substance comes first
- Useful = true × important × new to most readers × stated as strongly as the evidence allows. Any factor at zero zeroes the piece (S10).
- Best topic source: something the writer struggled with and then solved. The post is about the lesson, not the struggle (S5).
- If the writer learned nothing while writing, cut it or rethink it (S10).
- Vague-but-safe ("it's complex, many factors") and unsupported assertion ("X is crucial") both fail. Prove claims with something the reader can run or see (S3 p10, S10).
- A weak, honest "why" beats a feature list with no "why" (S3 p13).

## 2. One named reader
- Good doc = what the reader needs − what they already know (S7).
- Pick one real person. List terms they know and terms they don't, then check every term in the draft against the list (S2, S3 p2).
- Keep assumptions consistent: never explain a for loop and then assume malloc (S3 p2).
- Never "simply", "easy", "just", "obviously" (S6).
- Explain on the page. A link is a bonus, not a prerequisite. Gloss the term in one sentence before linking (S2).
- No "in part one…" openers. Summarise what's needed (S2).
- Widen by one ring if it costs a sentence or two (S1).
- Test on someone who doesn't know the topic; experts share your blind spots (S3 p1).

## 3. Concrete before abstract
- Open on something the reader has done ("have you used `kill`? you've used signals"), then name the concept (S3 p9).
- Compare with something familiar (S7).
- Examples come from real code with irrelevant details removed. No Bicycle interfaces, no squaring lists (S4, S3 p5).
- One new concept at a time (S3 p8). One-idea analogies only (S3 p3).
- Don't leave out the key idea (content-addressable → key is a hash of the content) (S3 p7).
- Say a mistake is a mistake before showing it (S3 p12).
- Every code block is followed by prose: what it does and why. Explain flags (S6).
- Real screenshots, graphs or diagrams beat decoration. Visual tone matches the prose (S1, S3 p4).

## 4. Built for the skimmer
- Title + first three sentences answer "is this for me?" and "what do I get?" Preamble (bios, epigraphs, history) spends that budget (S1, S2).
- Key point first, inverted pyramid (S7, S12).
- 79% of web readers scan; meaningful (not clever) headings, one idea per paragraph, lists where items are parallel (S12, S13).
- Headings alone should tell the story (S1 skim test).
- One article type: tutorial, how-to, reference, explanation (S8), or case study / opinion (S9). The common blur is a tutorial stuffed with explanation; give one line and link out (S8).
- Know the route to readers before writing: search, HN, Lobsters, subreddit, forum (S1).
- Check mobile: no horizontal overflow, readable contrast (S2).

## 5. Plain, calibrated, edited
- Ordinary words, short sentences, no idioms that won't translate (S7, S11).
- No marketese; objective wording alone measured +27% usability (S12).
- Confidence matches evidence. "I think" is information when it marks a guess (S10).
- Genre decides tone: docs-style tutorials are second person, neutral, no jokes (S6). Blog posts and essays sound like a person: first person, the way you'd say it (S2).
- Draft loose, edit tight. Keep rereading until no sentence catches (S10, S11).
