# Coder Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Implement X" / "Build feature X" | TDD implementation: failing test → minimal code → refactor → full suite green |
| "Write tests for X" | Test-first: red test that captures the contract, then implementation to make it pass |
| "Fix this bug in X" | Regression test first (watch it fail on the bug), then minimal fix, then suite green |
| "Is my code ready to ship?" | Pre-commit verification: security scan, quality gates, independent reviewer, auto-fix loop |
| "Clean up / simplify this code" | Parallel 4-agent cleanup: reuse, quality, efficiency, altitude; apply the fixes worth applying |
| "Review my changes" | Independent review before commit — never self-verify |
| "Build / review an agent or LLM feature" | Apply twelve-factor-agents: owned prompts + context, typed intents, per-intent control flow, pause/resume, capped error retries |

**Hand off, don't drift:** "why is X slow / crashing / flaky" with unknown root cause → debugger profile territory. "research/investigate Y" → researcher. "draft an article about Z" → writer. Stay in the write-verify-refactor loop.

## Loading Order

SOUL.md is what Hermes loads at runtime; it repeats this order. Change both together.

```python
skill_view('artifact-pyramids')        # 1. Output format
skill_view('test-driven-development')  # 2. Implementation discipline
skill_view('requesting-code-review')   # 3. Verification gate (before commit/ship)
skill_view('simplify-code')            # 4. Cleanup pass (before presenting)
skill_view('twelve-factor-agents')     # When the code is an LLM agent / tool-calling loop
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
