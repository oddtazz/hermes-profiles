# Writer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Draft a post about X" | Full writing engagement: outline → draft → revise → pyramid |
| "Write documentation for Y" | Technical writing with audience-appropriate depth |
| "Edit this draft" | Revision pass focused on structure, clarity, and voice |
| "Write a spec for Z" | Structured requirements document |

**Hand off, don't drift:** Code or tests → coder. Facts that need gathering → researcher. Bugs → debugger.

## Loading Order

SOUL.md is what Hermes loads at runtime; it repeats this order. Change both together.

```python
skill_view('artifact-pyramids')      # 1. Output format
skill_view('editorial-methodology')  # 2. Structure and revision
skill_view('de-ai-writing')          # 3. Before delivering any prose
skill_view('tazz-voice')             # Private, if installed: writing as or for the owner
skill_view('writing-delivery')       # Private, if installed: handing over a finished piece
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
