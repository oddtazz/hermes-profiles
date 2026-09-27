---
name: twelve-factor-agents
description: "Use when building or reviewing LLM agents in code."
version: 1.0.0
author: Hermes Agent (distilled from humanlayer/12-factor-agents @ d20c728)
license: CC-BY-SA-4.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agents, llm, architecture, context-engineering, tool-calling, human-in-the-loop]
    related_skills: [twelve-factor, test-driven-development, human-approval-gates]
---

# Twelve-Factor Agents

Design and review checklist for LLM-powered software. Source: Dex Horthy /
HumanLayer, https://github.com/humanlayer/12-factor-agents (local clone
~/opt/12-factor-agents; content/ holds the factor essays). Not the same as
`twelve-factor` (12factor.net, service ops); use both for an agent service.

Core claim: good production agents are MOSTLY deterministic software with LLM
steps at the right points. "Prompt + bag of tools + loop until done" gets
70-80% quality; the last 20% needs you to own prompts, context, and control
flow. Prefer adding small agent concepts to an existing product over adopting a
framework wholesale.

## When to Use

- Designing, scaffolding, or refactoring an agent, tool-calling loop, or LLM feature
- Reviewing agent code (yours or a framework-based one) for reliability
- An agent spins on errors, loses focus, cannot pause for approval, or cannot resume
- Don't use for: one-shot prompt/completion calls with no tools or state; model
  training/fine-tuning; sampling-parameter tuning (the guide excludes these)

## The canonical loop

```
thread = Thread(events=[initial_event])          # user msg, cron, webhook...
while True:
    step = determine_next_step(render(thread))   # LLM -> ONE typed intent (JSON)
    thread.append(step)
    match step.intent:
        case sync tool  -> run it, append result, continue
        case async/risky/ask-human -> save(thread), notify, break (resume via webhook)
        case done_for_now -> return
```

Everything below refines this loop. Full TypeScript reference implementation:
`references/reference-implementation.md`.

## The factors (rule / litmus / violation)

1. **Natural language -> tool calls.** LLM's job is to turn text into a typed
   payload; deterministic code acts on it.
   Litmus: every LLM output is parsed into a known type before anything runs.
   Violation: acting on free text; no `else` branch for unknown intents.
2. **Own your prompts.** Prompts are versioned code in the repo, not hidden in a
   framework's `Agent(role=, goal=)`. Test them (unit tests + evals per prompt).
   Litmus: you can print the exact tokens sent to the model.
3. **Own your context window** (the most important factor; = context
   engineering). Input to the LLM is always "here's what happened, what next?".
   You choose the format: standard role/messages OR the whole history packed
   into one user message as `<event_type>yaml</event_type>` blocks. Optimize
   for token density and attention; filter secrets; drop resolved errors.
   Litmus: a `render(thread)` function you control builds every prompt.
4. **Tools are just structured outputs.** A tool = a typed class with an
   `intent` literal; the "call" is JSON + a switch. The model decides WHAT;
   your code decides HOW (it need not map 1:1 to a function).
5. **Unify execution state and business state.** Derive current step, waiting
   status, retries from the event thread. Keep out-of-band state (session ids,
   creds) minimal. Payoff: serializable, debuggable, resumable, forkable.
   Litmus: `awaiting_approval()` is computed from `thread.events[-1]`.
6. **Launch / pause / resume with simple APIs.** `POST /thread` to launch,
   `GET /thread/:id` to inspect, `POST /thread/:id/response` to resume.
   Must be able to pause BETWEEN tool selection and tool execution.
7. **Contact humans with tool calls.** `request_more_information`,
   `request_approval`, `done_for_now` are ordinary intents in the same union
   (the model always emits JSON; no high-stakes "text vs tool" first token).
   Give them structure: question, context, urgency, format (free_text|yes_no|
   multiple_choice). Enables outer-loop agents (cron/event -> agent -> human).
8. **Own your control flow.** Per-intent policy: sync (continue), async (save +
   break), high-stakes (save + request approval + break). The loop is also where
   you add: result summarization/caching, LLM-as-judge, context compaction,
   tracing/metrics, rate limits, durable sleep.
9. **Compact errors into the context window.** On tool failure append a
   FORMATTED error event and retry; cap consecutive errors (~3) then escalate to
   a human or reset context. Don't dump raw stack traces; remove errors once
   resolved to stop spin-outs.
10. **Small, focused agents.** 3-10 steps, 20 max, one domain each, embedded in
    a mostly deterministic pipeline. Grow scope only while quality holds.
11. **Trigger from anywhere, meet users where they are.** Same agent reachable
    from Slack/email/SMS/cron/webhook; replies on the originating channel. Needs
    6 + 7 first.
12. **Stateless reducer.** `agent(thread, event) -> thread'` (a foldl over
    events). No hidden in-process state.
13. **(Appendix) Pre-fetch likely context.** If the model will almost surely call
    tool X (e.g. list_git_tags), call it deterministically first, append
    `list_git_tags` + `list_git_tags_result` events, and remove X from the tool
    union. Saves a round trip and a failure mode.

## Procedure

### A. Build a new agent

1. Scope: one domain, <= ~10 steps. Draw the surrounding deterministic pipeline;
   the agent is one node (F10).
2. Define the intent union as typed classes: domain tools + human tools
   (`request_more_information`, `done_for_now`, `request_approval` when needed)
   (F1, F4, F7).
3. Write `determine_next_step(thread_str) -> Union` as a repo-owned prompt;
   use structured-output parsing (BAML, Pydantic/Instructor, Zod, JSON schema
   mode) (F2).
4. Implement `Thread{events[]}` + `render()` (serializer) + JSON persistence
   store (file/sqlite/postgres) (F3, F5).
5. Write the loop with an explicit per-intent policy table: sync / async / needs
   approval / terminal (F8). Default unknown intent -> error event.
6. Add the error path: formatted error event, consecutive-error counter, escalate
   at the cap (F9).
7. Expose launch / get / respond endpoints; the respond handler appends the
   human event (approval = run the pending tool; rejection = append the reason
   as feedback) and re-enters the loop (F6, F7).
8. Pre-fetch any context the model always needs (F13).
9. Write prompt tests: fixed thread string in -> assert intent/fields out.
   Cover: greeting -> clarification, happy path, multi-step thread -> done,
   garbage input -> clarification, post-clarification -> tool.

-> Done when: the agent runs end-to-end on a real model; a risky intent pauses,
   persists, and resumes from a separate process via the respond API; prompt
   tests pass.

### B. Review an existing agent

For each factor 1-13: pass / fail / N/A with a code citation (file:line), then
the single highest-impact fix per failure. Prioritize 3, 8, 7, 9 (largest
reliability gains), then 5/6 (operability). Deliver a table + ranked fix list.

## Pitfalls

- Frameworks that pause only in-memory (`while ... sleep`) or not between
  selection and execution force a bad choice: restrict to low-stakes tools, or
  yolo. Check this first when reviewing.
- Error retry without a cap and without context cleanup -> the agent repeats
  the same failing call. Cap + compact + escalate.
- Growing one agent until it handles everything -> long context -> lost focus.
  Split into focused agents before adding step 20.
- A custom context format is an experiment, not a law: measure it against the
  standard messages format with evals before committing.
- Resolved errors and verbose tool results left in context waste tokens and
  steer the model. Summarize or drop them in `render()`.
- Out-of-band execution state (step counters, flags in a separate table) drifts
  from the thread. Derive it from events.
- The repo's code (calculator agent, workshops) is teaching material, not a
  production base. Mid-2025 view: step limits in F10 are looser for current
  frontier models, but the scoping principle still holds.

## Verification

- Build: kill the process while an approval is pending; restart; approve via the
  API; the agent continues from the persisted thread.
- Build: force a tool to throw 3x; the thread shows compact error events, then
  escalation, not an infinite loop.
- Review: 13-row table with evidence for each row.

## References

- `references/reference-implementation.md` - TS/BAML loop, Thread serializer,
  state store, approval-resume server, prompt tests (from the repo template).
- Source essays: ~/opt/12-factor-agents/content/factor-NN-*.md; workshop that
  builds it step by step: ~/opt/12-factor-agents/workshops/2025-05-17/walkthrough.md
