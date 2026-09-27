# Reference implementation (TypeScript + BAML)

Condensed from humanlayer/12-factor-agents
`packages/create-12-factor-agent/template/` and `workshops/2025-05-17/`.
The same shape works in Python (Pydantic/Instructor) or any typed language.

## 1. Intent union + owned prompt (baml_src/agent.baml) - F1, F2, F4, F7

```baml
class ClarificationRequest {
  intent "request_more_information" @description("you can request more information from me")
  message string
}
class DoneForNow {
  intent "done_for_now"
  message string @description("message to send to the user about the work that was done")
}
class DivideTool { intent "divide"  a int | float  b int | float }
// ... AddTool, SubtractTool, MultiplyTool

type HumanTools = ClarificationRequest | DoneForNow
type CalculatorTools = AddTool | SubtractTool | MultiplyTool | DivideTool

function DetermineNextStep(thread: string) -> HumanTools | CalculatorTools {
  client "openai/gpt-4o"
  prompt #"
    {{ _.role("system") }}
    You are a helpful assistant that can help with tasks.
    {{ _.role("user") }}
    You are working on the following thread:
    {{ thread }}
    What should the next step be?
    {{ ctx.output_format }}
    Always think about what to do next first, like:
    - ...
    {...} // schema
  "#
}
```

The "think first" block lets the model reason before emitting JSON; BAML's
schema-aligned parser strips the reasoning.

## 2. Prompt tests (same file) - F2

```baml
test MathOperationPostClarification {
  functions [DetermineNextStep]
  args { thread #"
    <user_input>can you multiply 3 and FD*(#F&& ?</user_input>
    <request_more_information>message: Could you clarify the numbers?</request_more_information>
    <human_response>lets try 12 instead</human_response>
  "# }
  @@assert(intent, {{this.intent == "multiply"}})
  @@assert(b, {{this.b == 12}})
}
```

Minimum set: hello -> request_more_information; simple op -> tool; full
multi-step thread -> done_for_now with answer in message; garbage ->
clarification; post-clarification -> correct tool.

## 3. Thread + serializer (src/agent.ts) - F3, F5, F12

```ts
export interface Event { type: string; data: any }

export class Thread {
  constructor(public events: Event[]) {}

  serializeForLLM() { return this.events.map(e => this.serializeOneEvent(e)).join("\n"); }

  serializeOneEvent(e: Event) {
    const tag = e.data?.intent || e.type;
    const body = typeof e.data !== "object" ? e.data
      : Object.keys(e.data).filter(k => k !== "intent").map(k => `${k}: ${e.data[k]}`).join("\n");
    return `<${tag}>\n${body}\n</${tag}>`;
  }

  // execution state DERIVED from business state (F5)
  awaitingHumanResponse() { return ["request_more_information", "done_for_now"].includes(this.lastEvent().data.intent); }
  awaitingHumanApproval() { return this.lastEvent().data.intent === "divide"; }
  lastEvent() { return this.events[this.events.length - 1]; }
}
```

Rendered context looks like:

```xml
<user_input>can you multiply 3 and 4, then divide by 2</user_input>
<multiply>a: 3
b: 4</multiply>
<tool_response>12</tool_response>
<divide>a: 12
b: 2</divide>
```

## 4. Loop with per-intent control flow - F8, F9

The error counter is from the factor-9 essay; the repo template loop has no
try/catch. Add it.

```ts
export async function agentLoop(thread: Thread): Promise<Thread> {
  let consecutiveErrors = 0;
  while (true) {
    const nextStep = await b.DetermineNextStep(thread.serializeForLLM());
    thread.events.push({ type: "tool_call", data: nextStep });

    switch (nextStep.intent) {
      case "done_for_now":
      case "request_more_information":
        return thread;                       // terminal / async human: break
      case "divide":
        return thread;                       // high-stakes: break for approval
      default:
        try {
          thread = await handleNextStep(nextStep, thread);   // sync: continue
          consecutiveErrors = 0;
        } catch (e) {
          if (++consecutiveErrors >= 3) {
            thread.events.push({ type: "error", data: "3 consecutive failures, escalating" });
            return thread;                   // escalate to human
          }
          thread.events.push({ type: "error", data: formatError(e) }); // compact, not raw trace
        }
    }
  }
}
```

## 5. State store - F5, F6

```ts
export interface ThreadStore {
  create(thread: Thread): Promise<string>;
  get(id: string): Promise<Thread | undefined>;
  update(id: string, thread: Thread): Promise<void>;
}
// Template: FileSystemThreadStore writes .threads/<uuid>.json plus <uuid>.txt
// (the rendered prompt, handy for debugging). Swap for redis/sqlite/postgres.
```

## 6. Launch / resume API - F6, F7, F11

```ts
app.post("/thread", async (req, res) => {           // launch
  const thread = new Thread([{ type: "user_input", data: req.body.message }]);
  const result = await agentLoop(thread);
  const id = await store.create(result);
  res.json({ thread_id: id, ...result });
});

app.get("/thread/:id", async (req, res) => res.json(await store.get(req.params.id)));

app.post("/thread/:id/response", async (req, res) => {   // resume (webhook target)
  let thread = await store.get(req.params.id);
  if (req.body.type === "approval" && thread.awaitingHumanApproval()) {
    if (req.body.approved) {
      thread = await handleNextStep(thread.lastEvent().data, thread);   // run the paused tool
    } else {
      thread.events.push({ type: "tool_response",
        data: `user denied the operation with feedback: "${req.body.comment}"` });
    }
  } else if (req.body.type === "response" && thread.awaitingHumanResponse()) {
    thread.events.push({ type: "human_response", data: req.body.message });
  } else {
    return res.status(400).json({ error: "thread not waiting for this response type" });
  }
  thread = await agentLoop(thread);
  await store.update(req.params.id, thread);
  res.json(thread);
});
```

In production do not block the web worker on `agentLoop`; enqueue and return.
The workshop's later chapters wire the respond endpoint to a HumanLayer webhook
so approvals arrive by email/Slack (F11).
