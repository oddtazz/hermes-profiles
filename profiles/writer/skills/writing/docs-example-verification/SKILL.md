---
name: docs-example-verification
description: "Use when docs quote live API examples. Verify them."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [docs, verification, api, examples, kanban]
    related_skills: [de-ai-writing, artifact-pyramids]
---

# Verifying a doc's examples against the running thing

A guide that quotes a response body is a claim about a running program. Never paste a body from
memory, from the spec, or from an earlier run — capture it, then assert the pasted copy still equals
the capture. This is the procedure that worked for the article-evaluator user guide.

## Procedure

1. **Read the shipped code before the spec.** The contract describes intent; validation order, error
   `details` shapes and framework fallbacks are in the request handler and the schema. Document what
   the code does and flag the difference, in a dedicated "where this differs from the written
   contract" section, rather than choosing the nicer of the two.
2. **Write one harness that boots the service and drives it with real `curl`**, saving per-case
   `{status, headers, body}`. Record the literal command in the transcript alongside the output, so
   the doc's command line can be copied out of the log. Include: the happy paths, every documented
   error code, both flavours of any ambiguous code (two 502 causes, two 504 causes are typical), and
   the boundary values (limit−1, limit, limit+1).
3. **Boot it twice when a credential-free path exists.** A stub/fake engine proves the contract shape
   for readers without credentials; the real engine over a loopback provider proves the pipeline. If
   the fake provider is canned, say so in the doc and in the pyramid — its token counts are envelope
   values, not measurements.
4. **Write a checker, not a promise.** A small script that extracts every fenced JSON block from the
   finished doc and asserts (a) each one parses, (b) any captured body is byte-equal to its capture,
   (c) any quoted input (a heredoc request, a sample text) is identical to the real source file, and
   (d) totals stated in prose re-derive from the quoted numbers. Ship it with the doc and keep its
   PASS output as evidence.
5. **Verify the doc's own commands verbatim.** Copy the quickstart block into a shell script and run
   exactly that. Flags you added while testing (`--no-access-log`) must not appear in the doc unless
   you re-ran with them.
6. **Measure, do not estimate, the cost shape.** Import the prompt/request builder and count the
   characters or tokens the service actually sends, so "the rubric is a fixed per-call cost" is a
   number with a divisor rather than an adjective.
7. **Consolidate captures into one dossier JSON** (`case -> {status, headers, body}`) plus the raw
   transcripts. Per-case files explode into hundreds of items; the consolidated file is what a
   reviewer reads.
8. **Run the prose gates last:** `de-ai-writing`'s `banned_phrase_scan.py` and
   `structure_scan.py --genre docs` on the finished doc. A reference doc will trip the *silhouette*
   scan for having a table of contents and a closing navigation block — that is genre-valid; record
   it as a judgment call instead of deleting the TOC.

## Pitfalls

- **Mixed captures are the failure mode.** Pasting one run's `request_id` with another run's
  weaknesses produces a body that never existed. The checker in step 4 exists to catch exactly this;
  run it after every edit to the doc, not once at the end.
- **A fixture engine's scores are not an evaluation.** If the doc shows them, label them in the same
  breath, or a reader will quote them as a verdict on their article.
- **Timeouts with equal defaults race.** If the API wall-clock cap and the provider timeout share a
  default, say so and tell the reader which to raise.
- **Behaviour that no code path emits is "reserved", not documented.** Do not write a plausible
  example body for it; say it is unimplemented and name the code path that would emit it.
- **Write the doc where it ships.** Draft in scratch, but install into the durable repo before
  claiming done: scratch workspaces are cleaned up. Commit only your paths — a sibling task is
  usually editing the same repo, so `git add -A` will scoop their work into your commit.

## Done when

- The checker PASSes with its output retained.
- Every response body in the doc traces to a capture, and every capture that the doc relies on is in
  the dossier.
- The deltas list is complete and each item carries its raw evidence.
- The pyramid records what was *not* verified, in the same table as what was.
