# Structured Implementation Prompt: Next.js DeepSeek-NVIDIA Chatbot

## Context

This prompt defines a build target for a Next.js chatbot application that wraps the `OpenAI` client SDK, configured with `base_url="https://integrate.api.nvidia.com/v1"`, to produce a futuristic minimalist conversational interface with tool- and skill-extensible architecture. The model runtime is `deepseek-ai/deepseek-v4-flash` via NVIDIA's integration endpoint.

All repositories in this workspace reside at `/Users/macbookpro/GitHub`. The target project name is **nvidia-deepseek-chatbot** and should be created as a new directory under the workspace root.

## Objective

Produce a production-ready Next.js chatbot application that:

1. Runs the exact model invocation semantics from the provided Python/OpenAI reference
2. Exposes a clean futuristic-minimalist chat UI at the root route
3. Maintains multi-turn conversation state via message history
4. Handles reasoning extraction as optional metadata
5. Manages all error states deterministically
6. Is structured for subsequent addition of tools, skills, and plugins

## Technical Invariants (Must Preserve)

Every model invocation MUST reproduce these exact values:

| Field         | Value                                                                      |
| ------------- | -------------------------------------------------------------------------- |
| `base_url`    | `https://integrate.api.nvidia.com/v1`                                      |
| `model`       | `deepseek-ai/deepseek-v4-flash`                                            |
| `temperature` | `1`                                                                        |
| `top_p`       | `0.95`                                                                     |
| `max_tokens`  | `16384`                                                                    |
| `extra_body`  | `{"chat_template_kwargs": {"thinking": true, "reasoning_effort": "high"}}` |
| `stream`      | `false` (unless intentionally extended)                                    |

### Response Extraction (Must Preserve)

```python
reasoning = getattr(completion.choices[0].message, "reasoning", None) or getattr(completion.choices[0].message, "reasoning_content", None)
if reasoning:
    print(reasoning)
print(completion.choices[0].message.content)
```

The equivalent TypeScript/Node.js logic MUST attempt both `reasoning` and `reasoning_content` property accesses on the response message object and handle both fields as potentially absent.

## Architecture

### Layers

```
[Browser UI]  <-->  Next.js API Route (app/api/chat/route.ts)  <-->  NVIDIA OpenAI-compatible endpoint
```

- **Frontend**: Next.js App Router page at `app/page.tsx`
- **Backend**: Next.js API route handler at `app/api/chat/route.ts`
- **No external database required** for Phase 1 — conversation state is ephemeral in the client

### Project Layout

```
nvidia-deepseek-chatbot/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts          # POST handler – sends messages, returns assistant response
│   ├── globals.css               # Futuristic minimalist design tokens
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Chat UI – message list, input bar, send button
├── lib/
│   ├── openai.ts                 # OpenAI client singleton initialisation
│   └── types.ts                  # Message, ChatRequest, ChatResponse types
├── components/
│   ├── MessageBubble.tsx         # Single chat message renderer
│   ├── ChatInput.tsx             # Text input + send button
│   ├── ReasoningPanel.tsx        # Optional expandable reasoning display
│   └── ErrorBanner.tsx           # Deterministic error display
├── .env.local                    # NVIDIA_API_KEY
├── next.config.ts
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

## API Route Specification (`app/api/chat/route.ts`)

### Method: `POST`

### Request Body

```typescript
interface ChatRequest {
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
}
```

### Implementation

```typescript
// STEP 1: Validate request body — reject empty or non-array messages
// STEP 2: Build payload (must preserve all technical invariants above)
// STEP 3: Call client.chat.completions.create(...)
// STEP 4: Extract content from choices[0].message.content
// STEP 5: Extract reasoning via getattr-style fallback:
//         response.choices[0].message.reasoning
//         response.choices[0].message.reasoning_content
// STEP 6: Return structured response payload (see below)
```

### Success Response (200)

```typescript
interface ChatResponse {
  reply: string; // completion.choices[0].message.content
  reasoning: string | null; // fallback chain: reasoning ?? reasoning_content ?? null
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
```

### Error Response (4xx/5xx/503)

```typescript
interface ErrorResponse {
  error: string; // Human-readable error description
  code:
    | 'INVALID_REQUEST'
    | 'UPSTREAM_ERROR'
    | 'AUTH_ERROR'
    | 'RATE_LIMITED'
    | 'TIMEOUT';
}
```

## OpenAI Client (`lib/openai.ts`)

```typescript
import OpenAI from 'openai';

export const client = new OpenAI({
  baseURL: 'https://integrate.api.nvidia.com/v1',
  apiKey: process.env.NVIDIA_API_KEY!, // MUST be set in .env.local
});
```

## UI Specification

### Visual Design

- **Colour palette**: Dark background (`#0a0a0f`), cyan/teal accent (`#00e5ff` / `#00b8d4`), white/light-grey text, subtle glass-morphism effects
- **Typography**: Monospace or tech-forward sans-serif for assistant responses (e.g. Inter, JetBrains Mono)
- **Message layout**: Left-aligned assistant (subtle glass card), right-aligned user (solid accent)
- **Reasoning display**: Collapsible panel below assistant messages when `reasoning` is available; labelled "Reasoning" with a subtle border and reduced opacity
- **Loading state**: Skeleton shimmer or animated ellipsis during API call
- **Empty state**: Centered welcome message with "Ask me anything" placeholder
- **Responsive**: Single-column mobile, max-width container (`max-w-3xl`) on desktop

### Interaction

- Send message via Enter key or click send button
- Auto-scroll to bottom on new message
- Disable input while request is in-flight
- Show error banner above input on failure (dismissable)
- "New Chat" button or command to reset conversation

## Conversation History Management

### Client-side State

```typescript
const [messages, setMessages] = useState<
  Array<{ role: 'user' | 'assistant'; content: string }>
>([]);
```

### Multi-turn Flow

1. User submits message `M_new`
2. Client constructs payload: `[messages[0..n], {role: "user", content: M_new}]`
3. Client sends full history to API route
4. API route appends assistant response to the response
5. Client appends assistant response to `messages` state

### Context Growth Warning

Message arrays grow unbounded. For this phase, accept the growth. Document in code that a future phase should implement sliding-window truncation or summarization.

## Reasoning Extraction Behavior

- Try `response.choices[0].message.reasoning` first
- Fall back to `response.choices[0].message.reasoning_content`
- If neither exists, set to `null`
- NEVER fail or return error when reasoning fields are absent
- Reasoning content is returned in the response payload but displayed ONLY as expandable UI — never prepended or mixed with reply text

## Edge Case Handling

| Edge Case                                     | Behaviour                                                                                           |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Empty input                                   | Client-side: prevent submission. Server-side: reject with 400 `INVALID_REQUEST`                     |
| API timeout (>30s)                            | Catch in route handler, return 503 `TIMEOUT`                                                        |
| Authentication failure (401)                  | Return 503 `AUTH_ERROR` — do NOT expose raw API key details in response                             |
| Rate limit (429)                              | Return 503 `RATE_LIMITED`                                                                           |
| Malformed upstream response (no `choices[0]`) | Return 503 `UPSTREAM_ERROR`                                                                         |
| Reasoning fields absent                       | `reasoning: null` in response, no interruption to reply flow                                        |
| Long response approaching 16384 tokens        | Stream partial if streaming is added; for non-streaming, truncate UI display with "Show all" expand |
| Network interruption client→route             | Error boundary in component, retry button shown                                                     |
| Multi-turn context bloat                      | Accept for Phase 1; add TODO comment for context window management                                  |

## Acceptance Criteria

1. **End-to-end flow**: User types message → API route calls NVIDIA endpoint → response renders in chat UI.
2. **Parameter fidelity**: Every model call uses the exact `model`, `temperature`, `top_p`, `max_tokens`, `extra_body`, and `base_url` values listed in Technical Invariants.
3. **Multi-turn**: Sending a follow-up message produces a contextually aware response that references prior exchange.
4. **Reasoning fallback**: Assistant response renders; if reasoning is present, an expandable panel shows it; if absent, no panel and no error.
5. **Error determinism**: Every error state produces the correct HTTP status code and structured error payload.
6. **Empty state**: Fresh page load shows a welcome/placeholder message.
7. **Loading state**: Input is disabled and visual feedback is shown while request is in-flight.
8. **No credentials leak**: API key is server-side only, never sent to client.

## Validation

### Static

- Confirm `route.ts` contains all required payload fields exactly matching Technical Invariants
- Confirm no `console.log` in production paths (use structured logging)
- Confirm `.env.local` is in `.gitignore`

### Runtime

```bash
# Start dev server
cd nvidia-deepseek-chatbot && npm run dev

# Test 1: Basic query
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}' \
  | jq '.reply | length'  # Expect >0

# Test 2: Reasoning presence
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Solve step by step: 23 * 17"}]}' \
  | jq '.reasoning'        # Expect non-null or null — both acceptable

# Test 3: Multi-turn
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"My name is Juan"},{"role":"assistant","content":"Hello Juan"},{"role":"user","content":"What is my name?"}]}' \
  | jq '.reply'            # Expect "Juan" or reference to prior turn

# Test 4: Empty input
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[]}' \
  | jq '.code'             # Expect "INVALID_REQUEST"

# Test 5: Bad auth (override key)
NVIDIA_API_KEY=bad curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"test"}]}' \
  | jq '.code'             # Expect "AUTH_ERROR"

# Test 6: UI loads
open http://localhost:3000   # Manual: page renders without console errors
```

## Dependency Installation

```bash
npx create-next-app@latest nvidia-deepseek-chatbot --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"

cd nvidia-deepseek-chatbot
npm install openai

# For future phases (not required for MVP):
# npm install @vercel/ai  # if streaming is added later
```

## Environment Configuration

File: `.env.local`

```
NVIDIA_API_KEY=<your-nvidia-api-key>
```

**IMPORTANT**: Never hardcode or commit real API keys. Obtain the key from your NVIDIA account and store it only in `.env.local` (which must be git-ignored). In production, use a secure runtime config (Vercel env vars, GCP Secret Manager, etc.). Never commit `.env.local`.

## Future Extension Points (Documented for Phase 2+)

- Tool/function calling: extend `extra_body` with tool definitions
- Streaming: swap to `stream: true` and use `ReadableStream` in the API route
- Session persistence: add database (SQLite/PostgreSQL) for persistent conversation history
- Context window management: sliding window or summarization for long conversations
- Skill system: register named "skills" that inject system prompts or tool definitions
- Markdown rendering: use `react-markdown` for rich assistant output

## Deliverables

1. A fully functional Next.js project at `/Users/macbookpro/GitHub/nvidia-deepseek-chatbot`
2. Running `npm run dev` exposes a chat UI at `localhost:3000` that accepts input and returns model responses
3. `curl` validation scripts above produce correct outputs
4. No credentials or secrets committed to version control
5. All acceptance criteria are demonstrably met
