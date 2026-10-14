# Source dossier: Julia Evans (jvns.ca)

Captured: 2026-10-14 via web_extract.

## S3. "Patterns in confusing explanations" (2021)
- URL: https://jvns.ca/blog/confusing-explanations/
- Author: Julia Evans. HN discussion: 566 points (news.ycombinator.com/item?id=28254630).

The 13 patterns, each with her stated fix:
1. Outdated assumptions about the audience's knowledge (Git book comparing branching to older VCSs). Fix: "test your explanations" on people who "don't already know the concept."
2. Inconsistent expectations of the reader's knowledge (explains a for loop, then assumes malloc). Fix: "pick 1 specific person and write for them!"
3. Strained analogies (parody: event system as the Mississippi River). Fix: "keep analogies to a single idea"; implicit metaphors ("flows") or one limited analogy (Jessica Kerr's laundry batching).
4. Fun illustrations on dry explanations. Fix: "make the design reflect the style of the explanation."
5. Unrealistic examples (`map(lambda x: x*x, ...)`, Oracle's `Bicycle` interface). Fix: realistic examples (`Comparable` from JDK source).
6. Jargon that doesn't mean anything ("Git is cryptographically secure, but it's not foolproof"). Fix: avoid jargon where not needed; show `git commit --author='Linus Torvalds'`.
7. Missing key information (content-addressable storage explained without saying the key is a hash of the content).
8. Too many concepts at a time (linker paragraph with five new concepts). Fix: "give each concept some space to breathe."
9. Starting out abstract (Wikipedia definition of Unix signals). Fix: "start out concrete" ("have you used `kill`? you've used signals!").
10. Unsupported statements ("header files are crucial tools"). Fix: "Prove that your statements are true!" with a program that fails to compile without `stdio.h`.
11. No examples.
12. Explaining the wrong way without saying it's wrong. Fix: "just say up front that the thing is a mistake!"
13. "What" without "why" (Kubernetes homepage feature list). "a weak 'why' is much better than no 'why'"; offer a personal reason.

## S4. "Write good examples by starting with real code" (2021)
- URL: https://jvns.ca/blog/2021/07/08/writing-great-examples/
- "start with real code that you wrote and then remove irrelevant details to make it into a self-contained example instead of coming up with examples out of thin air."
- Method: grep own code for `sort.+key`; finds most real uses sort by time; builds calendar-events example.
- "realistic examples help 'sell' the concept you're trying to explain."
- A CSS example took 2 hours to reduce from "hundreds of lines" to "5 lines of HTML and a tiny bit of CSS".
- Two further types named: surprising examples (change a mental model) and copy-paste starting points.

## S5. "Blog about what you've struggled with" (2021)
- URL: https://jvns.ca/blog/2021/05/24/blog-about-what-you-ve-struggled-with/
- Process: "1. Struggle with something 2. Eventually … figure out how to solve some of the problems I had 3. Write a blog post about what helped me"
- "it's not about the struggle, it's about what you learned"
- "write it down while you still remember what was hard"
- SQL example: talking to a newcomer revealed query execution order was the blocker; produced "SQL queries don't start with SELECT".

