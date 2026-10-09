// Typed client for the FastAPI backend. Requests go to /api, which Vite proxies to the backend.

export interface BackendConfig {
  semantic_vis_url: string | null
  context_vis_url: string | null
  semantic_ready: boolean
}

const isUrlOrNull = (value: unknown): value is string | null => value === null || typeof value === 'string'

function isBackendConfig(value: unknown): value is BackendConfig {
  if (typeof value !== 'object' || value === null) return false
  const v = value as Record<string, unknown>
  return isUrlOrNull(v.semantic_vis_url) && isUrlOrNull(v.context_vis_url) && typeof v.semantic_ready === 'boolean'
}

export async function fetchConfig(signal?: AbortSignal): Promise<BackendConfig> {
  const response = await fetch('/api/config', { signal })
  if (!response.ok) throw new Error(`GET /api/config failed: HTTP ${response.status}`)
  const body: unknown = await response.json()
  if (!isBackendConfig(body)) throw new Error('GET /api/config returned an unexpected shape')
  return body
}

export interface SourceRef {
  ref: string
  why: string
}

export interface TraceStep {
  step: number
  tool: string
  input: string
  result: string
  ms: number
}

export interface RetrievalNode {
  id: string
  title: string
  type: string | null
  sections: string[]
  found_in_step: number | null
  best_rank: number | null
  opened: boolean
  cited: boolean
}

export interface RetrievalPath {
  graph_available: boolean
  steps: { step: number; tool: string; input: string; node_ids: string[] }[]
  nodes: RetrievalNode[]
  links: { source: string; target: string }[]
}

export interface ChatTurn {
  session_id: string
  turn: number
  answer: string
  sources: SourceRef[]
  confidence: 'high' | 'medium' | 'low'
  follow_up_questions: string[]
  reasoning_summary: string
  retrieval?: RetrievalPath
  trace: {
    steps: TraceStep[]
    latency_ms: number
    input_tokens: number
    output_tokens: number
    model: string
  }
}

const isObject = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null
const isStringArray = (v: unknown): v is string[] => Array.isArray(v) && v.every((x) => typeof x === 'string')

function isChatTurn(value: unknown): value is ChatTurn {
  if (!isObject(value) || !isObject(value.trace)) return false
  return (
    typeof value.session_id === 'string' &&
    typeof value.turn === 'number' &&
    typeof value.answer === 'string' &&
    Array.isArray(value.sources) &&
    value.sources.every((s) => isObject(s) && typeof s.ref === 'string' && typeof s.why === 'string') &&
    ['high', 'medium', 'low'].includes(value.confidence as string) &&
    isStringArray(value.follow_up_questions) &&
    typeof value.reasoning_summary === 'string' &&
    Array.isArray(value.trace.steps) &&
    typeof value.trace.latency_ms === 'number'
  )
}

async function errorDetail(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json()
    if (isObject(body) && typeof body.detail === 'string') return body.detail
  } catch {
    // fall through to the status text
  }
  return `HTTP ${response.status}`
}

async function postJson(url: string, body: unknown): Promise<unknown> {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) throw new Error(await errorDetail(response))
  return response.json()
}

export async function createSession(): Promise<string> {
  const body = await postJson('/api/sessions', {})
  if (!isObject(body) || typeof body.session_id !== 'string') {
    throw new Error('POST /api/sessions returned an unexpected shape')
  }
  return body.session_id
}

export async function sendChat(sessionId: string, message: string): Promise<ChatTurn> {
  const body = await postJson('/api/chat', { session_id: sessionId, message })
  if (!isChatTurn(body)) throw new Error('POST /api/chat returned an unexpected shape')
  return body
}

export interface MemoryStatus {
  state: 'idle' | 'queued' | 'syncing' | 'error'
  mode: 'per_turn' | 'manual'
  pending_turns: number
  last_success_at: string | null
  last_duration_s: number | null
  last_error: string | null
  initialized: boolean
}

function isMemoryStatus(value: unknown): value is MemoryStatus {
  if (!isObject(value)) return false
  return (
    ['idle', 'queued', 'syncing', 'error'].includes(value.state as string) &&
    ['per_turn', 'manual'].includes(value.mode as string) &&
    typeof value.pending_turns === 'number' &&
    typeof value.initialized === 'boolean'
  )
}

export async function fetchMemoryStatus(signal?: AbortSignal): Promise<MemoryStatus> {
  const response = await fetch('/api/memory/status', { signal })
  if (!response.ok) throw new Error(await errorDetail(response))
  const body: unknown = await response.json()
  if (!isMemoryStatus(body)) throw new Error('GET /api/memory/status returned an unexpected shape')
  return body
}

export async function requestMemorySync(): Promise<MemoryStatus> {
  const body = await postJson('/api/memory/sync', {})
  if (!isMemoryStatus(body)) throw new Error('POST /api/memory/sync returned an unexpected shape')
  return body
}

export interface DemoReset {
  session_id: string
  context_vis_url: string | null
  memory: MemoryStatus
}

export async function resetDemo(): Promise<DemoReset> {
  const body = await postJson('/api/demo/reset', {})
  if (!isObject(body) || typeof body.session_id !== 'string' || !isMemoryStatus(body.memory)) {
    throw new Error('POST /api/demo/reset returned an unexpected shape')
  }
  return body as unknown as DemoReset
}
