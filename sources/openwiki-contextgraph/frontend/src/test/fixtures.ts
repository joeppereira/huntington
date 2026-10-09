import { vi } from 'vitest'
import type { BackendConfig } from '../api'

export const readyConfig: BackendConfig = {
  semantic_vis_url: 'http://127.0.0.1:4321',
  context_vis_url: 'http://127.0.0.1:4322',
  semantic_ready: true,
}

export function mockFetchJson(...bodies: Array<unknown | Error>) {
  const fn = vi.fn()
  for (const body of bodies) {
    if (body instanceof Error) {
      fn.mockRejectedValueOnce(body)
    } else {
      fn.mockResolvedValueOnce(new Response(JSON.stringify(body), { status: 200 }))
    }
  }
  vi.stubGlobal('fetch', fn)
  return fn
}

export const chatTurn = {
  session_id: '20261004-093012-a1b2',
  turn: 1,
  answer: 'The CET1 ratio was **15.1%** against a 10.2% requirement.',
  sources: [{ ref: 'openwiki/metrics/cet1-ratio.md#requirement-stack', why: 'lists the requirement stack' }],
  confidence: 'high',
  follow_up_questions: ['What drives the stress capital buffer?'],
  reasoning_summary: 'Searched for CET1 and read the metric page.',
  trace: {
    steps: [
      { step: 1, tool: 'semantic_search', input: '"CET1"', result: '8 hits: openwiki/metrics/cet1-ratio.md#x', ms: 41 },
      { step: 2, tool: 'semantic_read', input: 'openwiki/metrics/cet1-ratio.md [x]', result: '1 section, 1011 chars', ms: 22 },
    ],
    latency_ms: 6306,
    input_tokens: 6951,
    output_tokens: 779,
    model: 'claude-sonnet-5-5',
  },
}

export function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })
}

/** fetch stub that answers by URL; a route value of Error rejects (network failure). */
export function stubRoutes(routes: Record<string, unknown | Error>) {
  const fn = vi.fn((url: string) => {
    const body = routes[url]
    if (body === undefined) return Promise.resolve(jsonResponse({ detail: `no stub for ${url}` }, 404))
    if (body instanceof Error) return Promise.reject(body)
    return Promise.resolve(jsonResponse(body))
  })
  vi.stubGlobal('fetch', fn)
  return fn
}

export const idleMemory = {
  state: 'idle',
  mode: 'per_turn',
  pending_turns: 0,
  last_success_at: null,
  last_duration_s: null,
  last_error: null,
  initialized: false,
}
