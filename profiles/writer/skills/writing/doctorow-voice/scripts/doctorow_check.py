#!/usr/bin/env python3
"""Mechanical gate for drafts written in Cory Doctorow's Pluralistic essay register.

Targets come from 2,874 Pluralistic essays (2020-2026, ~2.6M words of his own prose).
Exit 0 = no FAILs, exit 1 = revise. WARNs are judgement calls, not failures.

Usage: doctorow_check.py draft.md [--quiet]
"""
import re
import statistics
import sys

WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
LINK = re.compile(r"<?https?://\S+>?|\[link\]|\[URL\]|\[source needed\]")

# Corpus rates per 1,000 words of his prose (see the research pyramid for sources).
BANNED = {  # all at or below 0.06/1k in the corpus: effectively never
    "however": 0.061, "moreover": 0.018, "furthermore": 0.001, "additionally": None,
    "although": 0.005, "delve": 0.004, "tapestry": 0.001, "testament": 0.006,
    "paradigm": 0.006, "seamless": 0.003, "stakeholder": 0.002, "landscape": 0.012,
    "notably": 0.035, "crucially": 0.011, "arguably": 0.011, "nuanced": None,
    "multifaceted": None, "realm": None, "navigate": None, "pivotal": None,
}
BANNED_PHRASES = [
    r"\bin conclusion\b", r"\bin today's\b", r"\bin an era\b", r"\bit's important to note\b",
    r"\bit is important to note\b", r"\blet's dive\b", r"\blet's explore\b", r"\bat its core\b",
    r"\bplays? a (vital|crucial|key|pivotal) role\b", r"\bstands as a\b", r"\bserves as a reminder\b",
    r"\bin the ever-\w+", r"\bgame-?changer\b", r"\bunlock(s|ing)? the\b", r"\bthe real question is\b",
    r"\bremains to be seen\b(?!\.)", r"\bmoving forward\b", r"\bat the end of the day\b",
]
PROFANITY = re.compile(r"\b(fuck\w*|shit\w*|bullshit|goddamn\w*|asshole\w*|crap\w*)\b", re.I)


def blocks(text):
    out = []
    for b in re.split(r"\n\s*\n", text):
        b = b.strip()
        if not b or b.startswith("#") or b.startswith(">") or LINK.fullmatch(b):
            continue
        if b.startswith("(Image"):
            continue
        out.append(b)
    return out


def sentences(block):
    block = LINK.sub("", block)
    block = re.sub(r"\b(e\.g|i\.e|etc|vs|Mr|Mrs|Dr|St|U\.S|Inc|Jr)\.", lambda m: m.group(0).replace(".", "∯"), block)
    return [s for s in re.split(r"(?<=[.!?])[\"”’)]*\s+(?=[\"“(A-Z0-9])", block) if WORD.search(s)]


def main(path, quiet=False):
    raw = open(path, encoding="utf-8").read()
    bl = blocks(raw)
    prose = "\n\n".join(bl)
    words = WORD.findall(prose)
    n = len(words)
    if n < 150:
        print(f"Only {n} words of prose: too short to judge. Check by ear.")
        return 0
    k = 1000 / n
    sl = [len(WORD.findall(s)) for b in bl for s in sentences(b)]
    pw = [len(WORD.findall(b)) for b in bl]
    low = prose.lower().replace("’", "'")
    results = []

    def r(level, name, msg):
        results.append((level, name, msg))

    med = statistics.median(sl)
    le10 = 100 * sum(x <= 10 for x in sl) / len(sl)
    ge30 = 100 * sum(x >= 30 for x in sl) / len(sl)
    lvl = "FAIL" if not 11 <= med <= 32 else ("WARN" if not 15 <= med <= 26 else "ok")
    r(lvl, "sentence median", f"{med} words (corpus 20; ok 15-26, fail outside 11-32)")
    r("WARN" if not 12 <= le10 <= 40 else "ok", "short sentences <=10w",
      f"{le10:.0f}% (corpus 23%)")
    r("WARN" if not 12 <= ge30 <= 40 else "ok", "long sentences >=30w",
      f"{ge30:.0f}% (corpus 25%); he needs both the short punch and the long stacked sentence")
    pmed = statistics.median(pw)
    r("FAIL" if pmed > 80 else ("WARN" if not 15 <= pmed <= 65 else "ok"), "paragraph median",
      f"{pmed} words (corpus 39; most paragraphs 1-3 sentences)")
    one = 100 * sum(len(sentences(b)) == 1 for b in bl) / len(bl)
    r("WARN" if one < 15 else "ok", "one-sentence paragraphs", f"{one:.0f}% (corpus 30-44%)")

    em = prose.count("—")
    r("FAIL" if em >= 3 or em * k > 1.5 else ("WARN" if em else "ok"), "em dashes",
      f"{em} found; he uses a spaced en dash ' – ' (7/1k), em dash 0.18/1k")
    en = prose.count(" – ")
    r("WARN" if n > 400 and en == 0 else "ok", "spaced en dash", f"{en * k:.1f}/1k (corpus 7.1/1k)")
    semi = prose.count(";") * k
    r("WARN" if semi > 3 else "ok", "semicolons", f"{semi:.1f}/1k (corpus 1.0/1k)")
    colon = prose.count(":") * k
    r("WARN" if n > 400 and colon < 3 else "ok", "colons", f"{colon:.1f}/1k (corpus 9.7/1k: set-ups, lists, link lead-ins)")
    paren = prose.count("(") * k
    r("WARN" if n > 400 and paren < 1 else "ok", "parenthetical asides", f"{paren:.1f}/1k (corpus 5.0/1k)")
    quotes = (prose.count('"') + prose.count("“")) * k
    r("WARN" if n > 400 and quotes < 4 else "ok", "quotation/scare marks", f"{quotes:.1f}/1k (corpus 20/1k)")
    excl = prose.count("!") * k
    r("WARN" if excl > 4 else "ok", "exclamation marks", f"{excl:.1f}/1k (corpus 1.1/1k)")

    hits = []
    for w in BANNED:
        c = len(re.findall(rf"\b{w}\b", low))
        if c:
            hits.append(f"{w}×{c}")
    # He uses each of these occasionally (often inside quoted material), so one hit is a WARN.
    # Several distinct ones together is the chatbot register, which he never writes in.
    r("FAIL" if len(hits) >= 3 else ("WARN" if hits else "ok"), "banned connectives/slop words",
      ", ".join(hits) or "none")
    ph = [p for p in BANNED_PHRASES if re.search(p, low)]
    r("FAIL" if len(ph) >= 2 else ("WARN" if ph else "ok"), "AI framing phrases", ", ".join(ph) or "none")
    nj = len(re.findall(r"\b(it's|it is|isn't|is) not (just|merely|only) .{0,60}?(it's|but)\b", low))
    r("WARN" if nj > 1 else "ok", "'not just X, but Y' frames", f"{nj} (he uses this rarely; once per piece at most)")

    you = len(re.findall(r"\byou\b", low)) * k
    i_ = len(re.findall(r"\bi\b", low)) * k
    r("WARN" if you < 2 else "ok", "second person 'you'", f"{you:.1f}/1k (corpus 6.8/1k: he talks to the reader)")
    r("ok", "first person 'I'", f"{i_:.1f}/1k (corpus 4.2/1k; 76% of essays use 'I')")
    but = len(re.findall(r"(^|[.!?]\s+)But\b", prose)) * k
    r("WARN" if n > 400 and but < 0.7 else "ok", "sentence-initial 'But'", f"{but:.1f}/1k (corpus 2.2/1k)")
    prof = len(PROFANITY.findall(prose)) * k
    r("WARN" if prof > 4 else "ok", "profanity", f"{prof:.1f}/1k (corpus 0.8/1k, in 40% of essays; aim it at the powerful)")

    last = bl[-1]
    lastw = len(WORD.findall(last))
    if re.search(r"\b(in (conclusion|summary|short)|to sum up|ultimately|all in all)\b", last.lower()):
        r("FAIL", "closing", "last paragraph summarises; end on a verdict, a kicker or a demand")
    elif last.rstrip().endswith("?"):
        r("WARN", "closing", "ends on a question (3% of his essays); prefer a verdict")
    else:
        r("ok", "closing", f"last paragraph {lastw} words (corpus median 22)")
    first = bl[0]
    if re.match(r"(In (today's|an era|recent years)|As we|Let's|Have you ever|Imagine a world)", first):
        r("FAIL", "opening", "generic frame; open on the thesis, the news hook or the anecdote")
    else:
        r("ok", "opening", first[:70] + ("…" if len(first) > 70 else ""))

    fails = sum(1 for x in results if x[0] == "FAIL")
    warns = sum(1 for x in results if x[0] == "WARN")
    for lvl, name, msg in results:
        if quiet and lvl == "ok":
            continue
        print(f"[{lvl:4}] {name}: {msg}")
    print(f"\n{n} words, {len(sl)} sentences, {len(bl)} paragraphs: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], "--quiet" in sys.argv))
