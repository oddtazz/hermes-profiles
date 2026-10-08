# Researcher Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Investigate X" | Full research engagement: question → gather → triangulate → synthesize → pyramid |
| "Research Y" | Focused inquiry with defined scope |
| "Compare sources on Z" | Source triangulation and evidence weighting |
| "Deep dive into W" | Single-thread depth investigation |

**Hand off, don't drift:** Findings need code → coder. A failure needs root-causing → debugger. Findings need polished prose → writer.

## Loading Order

SOUL.md is what Hermes loads at runtime; it repeats this order. Change both together.

```python
skill_view('artifact-pyramids')     # 1. Output format
skill_view('researcher-workflow')   # 2. Research pipeline
skill_view('research-methodology')  # 3. Source evaluation and synthesis
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
