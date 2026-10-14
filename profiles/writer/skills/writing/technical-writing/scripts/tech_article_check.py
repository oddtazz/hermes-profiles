#!/usr/bin/env python3
"""Mechanical checks for a technical article written in Markdown.

Usage: python3 tech_article_check.py draft.md [--json]

Catches the rule breaks that can be detected from text alone. It cannot judge
payoff, reader fit, or correctness; it prints the opening and a skim view so
the agent judges those by hand.

Exit codes: 0 = no hard findings, 1 = hard findings, 2 = usage error.
Stdlib only.
"""
import json
import re
import sys

ASSUMPTION_HARD = ["simply", "obviously", "straightforward", "trivially",
                   "trivial", "easy", "easily", "of course", "clearly"]
ASSUMPTION_SOFT = ["just", "simple"]
MARKETING = ["powerful", "seamless", "seamlessly", "robust", "cutting-edge",
             "blazing", "blazingly", "revolutionary", "game-changer",
             "game-changing", "best-in-class", "world-class", "supercharge"]
SEQUEL = re.compile(r"\b(in (the )?(part (one|1|i)\b|previous (post|article))"
                    r"|last (post|article|time)|as (we|I) (saw|discussed) (earlier|before|last))",
                    re.I)
PREAMBLE = re.compile(r"^(since the dawn|back in (the )?\d|in today's (fast|world)"
                      r"|have you ever wondered|in this (article|post|blog post),? (we|I) will)",
                      re.I)
GENERIC_HEADINGS = {"introduction", "overview", "background", "details",
                    "conclusion", "summary", "misc", "more", "notes", "final thoughts"}
BAD_LINK_TEXT = {"here", "this", "click here", "this link", "link", "this post",
                 "this article", "read more"}
ACRONYM_OK = {"API", "APIs", "HTTP", "HTTPS", "URL", "URLs", "CSS", "HTML", "JSON",
              "CPU", "GPU", "RAM", "SQL", "OS", "UI", "CLI", "SSH", "DNS", "TCP",
              "IP", "UDP", "XML", "YAML", "PDF", "USB", "ID", "IDs", "I", "TODO",
              "AI", "OK", "US", "UK", "PR", "PRs", "CI", "CD", "VM", "VMs", "SDK",
              "IDE", "GB", "MB", "KB", "TB", "MIT", "FAQ", "README", "NOTE", "AWS"}

WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def strip_inline_code(s):
    return re.sub(r"`[^`]*`", "", s)


def strip_quoted(s):
    """Remove inline code and quoted mentions ("simply", 'easy', “just”)."""
    s = strip_inline_code(s)
    return re.sub(r"\"[^\"]*\"|“[^”]*”|‘[^’]*’|(?<![A-Za-z])'[^'\n]{1,40}'(?![A-Za-z])", "", s)


def parse(text):
    """Return list of (lineno, kind, content). kind: heading/code/blank/prose/image."""
    out, in_fence, fence_start = [], False, 0
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            if not in_fence:
                in_fence, fence_start = True, i
            else:
                in_fence = False
                out.append((fence_start, "code_end", i))
            continue
        if in_fence:
            continue
        if not line.strip():
            out.append((i, "blank", ""))
        elif re.match(r"^#{1,6}\s", line):
            out.append((i, "heading", line))
        elif re.match(r"^\s*!\[", line):
            out.append((i, "image", line))
        else:
            out.append((i, "prose", line))
    if in_fence:
        out.append((fence_start, "unclosed_fence", ""))
    return out


def paragraphs(items):
    paras, cur = [], []
    for ln, kind, content in items:
        if kind == "prose":
            cur.append((ln, content))
        else:
            if cur:
                paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    return paras


def sentences(s):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", s) if x.strip()]


def check(text):
    items = parse(text)
    findings = []

    def add(line, check_id, severity, msg):
        findings.append({"line": line, "check": check_id, "severity": severity, "message": msg})

    prose_lines = [(ln, c) for ln, k, c in items if k == "prose"]
    all_prose = " ".join(strip_inline_code(c) for _, c in prose_lines)
    total_words = len(WORD.findall(all_prose))

    # 1. Assumption and marketing words (prose only, inline code removed)
    for ln, c in prose_lines + [(ln, c) for ln, k, c in items if k == "heading"]:
        low = strip_quoted(c).lower()
        if low.lstrip().startswith(">"):
            continue  # quoted material is exempt
        for w in ASSUMPTION_HARD:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                add(ln, "assumption-word", "hard", f"'{w}' assumes the reader's knowledge; show the step instead")
        for w in ASSUMPTION_SOFT:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                add(ln, "assumption-word", "soft", f"'{w}': keep only if it means 'only'/'exactly', not 'easy'")
        for w in MARKETING:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                add(ln, "marketing", "hard", f"'{w}' is marketese; replace with a measured claim")
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", c):
            if m.group(1).strip().lower() in BAD_LINK_TEXT:
                add(ln, "link-text", "hard", f"link text '{m.group(1)}' says nothing; name the destination and gloss it")

    # 2. Opening: first body paragraph after the H1
    paras = paragraphs(items)
    opening = ""
    if paras:
        first = paras[0]
        opening = " ".join(c for _, c in first)
        first_ln = first[0][0]
        open_sents = sentences(opening)[:3]
        opening = " ".join(open_sents)
        if PREAMBLE.search(opening.strip()):
            add(first_ln, "preamble-opener", "hard", "opening starts with preamble, not the reader's payoff")
        if len(WORD.findall(" ".join(c for _, c in first))) > 90:
            add(first_ln, "long-opening", "soft", "first paragraph over 90 words; the payoff may be buried")
    head300 = " ".join(all_prose.split()[:300])
    m = SEQUEL.search(head300)
    if m:
        ln = next((l for l, c in prose_lines if m.group(0).lower() in c.lower()), 0)
        add(ln, "sequel-opener", "hard", f"'{m.group(0)}' near the top assumes a previous post; summarise what's needed instead")

    # 3. Code blocks must be followed by explanatory prose
    for idx, (ln, kind, content) in enumerate(items):
        if kind == "unclosed_fence":
            add(ln, "code-fence", "hard", "code fence never closed")
        if kind != "code_end":
            continue
        nxt = next(((k, c) for _, k, c in items[idx + 1:] if k != "blank"), None)
        if nxt is None or nxt[0] in ("heading", "code_end", "unclosed_fence"):
            add(ln, "code-unexplained", "hard", "code block not followed by prose saying what it does and why")

    # 4. Paragraph size
    for p in paras:
        words = len(WORD.findall(" ".join(strip_inline_code(c) for _, c in p)))
        if words > 120 and not p[0][1].lstrip().startswith(("-", "*", "|", ">")):
            add(p[0][0], "wall-of-text", "soft", f"paragraph of {words} words; split to one idea per paragraph")

    # 5. Headings
    heads = [(ln, c) for ln, k, c in items if k == "heading"]
    h2 = [h for h in heads if re.match(r"^##\s", h[1])]
    if total_words > 600 and len(h2) < 2:
        add(0, "few-headings", "soft", f"{total_words} words with {len(h2)} H2 headings; skimmers need signposts")
    for ln, c in heads:
        t = re.sub(r"^#+\s*", "", c).strip().lower().rstrip(":")
        if t in GENERIC_HEADINGS:
            add(ln, "generic-heading", "soft", f"heading '{t}' tells a skimmer nothing; say what the section claims")

    # 6. Acronyms used without expansion on first use
    seen = set()
    for ln, c in prose_lines:
        s = strip_inline_code(c)
        s = re.sub(r"\]\([^)]*\)", "]", s)  # drop URLs
        for m in re.finditer(r"\b[A-Z][A-Z0-9]{1,5}s?\b", s):
            tok = m.group(0)
            if tok in ACRONYM_OK or tok in seen:
                continue
            seen.add(tok)
            window = s[max(0, m.start() - 60): m.end() + 60]
            if "(" + tok not in window and tok + " (" not in window and "(" not in window:
                add(ln, "acronym", "soft", f"'{tok}' first used without expansion; spell it out unless the reader certainly knows it")

    # 7. Skim view: headings + images + first sentence of each section
    skim, want_first = [], True
    for ln, kind, c in items:
        if kind == "heading":
            skim.append(c)
            want_first = True
        elif kind == "image":
            skim.append("  " + c)
        elif kind == "prose" and want_first:
            sent = sentences(c)
            skim.append("    > " + (sent[0] if sent else c)[:140])
            want_first = False

    findings.sort(key=lambda f: (f["severity"] != "hard", f["line"]))
    return {
        "words": total_words,
        "hard": sum(f["severity"] == "hard" for f in findings),
        "soft": sum(f["severity"] == "soft" for f in findings),
        "findings": findings,
        "opening_first_three_sentences": opening,
        "skim_view": skim,
        "manual_questions": [
            "Opening: does it answer 'is this for me?' and 'what do I get?'",
            "Skim view: do headings alone tell the story?",
            "Every claim: is there an example, output, or check the reader can run?",
            "Article type: tutorial, how-to, reference, explanation, case study, or opinion - only one?",
        ],
    }


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print((__doc__ or "").strip(), file=sys.stderr)
        return 2
    try:
        text = open(args[0], encoding="utf-8").read()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not text.strip():
        print("error: empty draft", file=sys.stderr)
        return 2
    r = check(text)
    if "--json" in argv:
        print(json.dumps(r, indent=2))
    else:
        print(f"words={r['words']} hard={r['hard']} soft={r['soft']}")
        for f in r["findings"]:
            print(f"  L{f['line']:<4} {f['severity']:<4} {f['check']:<18} {f['message']}")
        print("\nOPENING (first three sentences):\n  " + (r["opening_first_three_sentences"] or "(none)"))
        print("\nSKIM VIEW:")
        for s in r["skim_view"]:
            print("  " + s)
        print("\nJUDGE BY HAND:")
        for q in r["manual_questions"]:
            print("  - " + q)
    return 1 if r["hard"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
