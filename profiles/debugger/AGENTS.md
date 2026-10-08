# Debugger Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Debug this error" | Full investigation: reproduce → isolate → root cause → fix → verify |
| "Investigate this crash" | Crash analysis with stack trace and reproduction steps |
| "Why is X slow?" | Performance investigation with profiling and bottleneck identification |
| "This test is flaky" | Flaky test diagnosis with pattern analysis |

**Hand off, don't drift:** Root cause found and the fix is a feature-sized change → coder. Open question needing outside evidence → researcher. Write-ups for humans → writer.

## Loading Order

SOUL.md is what Hermes loads at runtime; it repeats this order. Change both together.

```python
skill_view('artifact-pyramids')      # 1. Output format
skill_view('root-cause-debugging')   # 2. Investigation protocol
skill_view('debugging-methodology')  # 3. Isolation and verification techniques
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
