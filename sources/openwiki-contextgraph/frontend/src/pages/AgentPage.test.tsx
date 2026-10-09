import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { idleMemory, jsonResponse, readyConfig } from '../test/fixtures'
import { AgentPage } from './AgentPage'

function stubMemory(statuses: object[]) {
  const queue = [...statuses]
  const fn = vi.fn((url: string, init?: RequestInit) => {
    if (url === '/api/sessions') return Promise.resolve(jsonResponse({ session_id: 's1' }))
    if (url === '/api/memory/sync' && init?.method === 'POST') {
      return Promise.resolve(jsonResponse({ ...idleMemory, state: 'queued' }, 202))
    }
    if (url === '/api/memory/status') {
      const next = queue.length > 1 ? queue.shift() : queue[0]
      return Promise.resolve(jsonResponse(next))
    }
    return Promise.resolve(jsonResponse({ detail: 'unexpected' }, 404))
  })
  vi.stubGlobal('fetch', fn)
  return fn
}

describe('AgentPage memory pane', () => {
  it('overlays the empty memory graph until the first sync', async () => {
    stubMemory([idleMemory])
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    expect(await screen.findByText(/memory graph appears after the first synced turn/i)).toBeInTheDocument()
  })

  it('removes the overlay once memory is initialized', async () => {
    stubMemory([{ ...idleMemory, state: 'syncing', pending_turns: 1 }, { ...idleMemory, initialized: true }])
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    expect(await screen.findByText(/syncing \(1 turn pending\)/i)).toBeInTheDocument()
    await waitFor(() => expect(screen.queryByText(/appears after the first synced turn/i)).not.toBeInTheDocument())
    expect(screen.getByRole('status')).toHaveTextContent('up to date')
  })

  it('"Sync memory now" posts to /api/memory/sync', async () => {
    const fetchMock = stubMemory([{ ...idleMemory, mode: 'manual', pending_turns: 2, initialized: true }])
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    const button = await screen.findByRole('button', { name: /sync memory now/i })
    await userEvent.click(button)
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url, init]) => url === '/api/memory/sync' && init?.method === 'POST')).toBe(true),
    )
  })
})

describe('AgentPage reset demo', () => {
  function stubReset(resetResponse: Response | Error) {
    const calls: string[] = []
    let session = 0
    const fn = vi.fn((url: string, init?: RequestInit) => {
      calls.push(`${init?.method ?? 'GET'} ${url}`)
      if (url === '/api/sessions') return Promise.resolve(jsonResponse({ session_id: `s${++session}` }))
      if (url === '/api/memory/status') return Promise.resolve(jsonResponse({ ...idleMemory, initialized: true }))
      if (url === '/api/demo/reset') {
        return resetResponse instanceof Error ? Promise.reject(resetResponse) : Promise.resolve(resetResponse)
      }
      return Promise.resolve(jsonResponse({ detail: 'unexpected' }, 404))
    })
    vi.stubGlobal('fetch', fn)
    return calls
  }

  it('asks for confirmation and does nothing on cancel', async () => {
    const calls = stubReset(jsonResponse({}))
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    await userEvent.click(await screen.findByRole('button', { name: 'Reset demo' }))
    expect(screen.getByText(/wipe the agent's memory/i)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Cancel' }))
    expect(screen.queryByText(/wipe the agent's memory/i)).not.toBeInTheDocument()
    expect(calls).not.toContain('POST /api/demo/reset')
  })

  it('wipes memory and switches the chat to the new session', async () => {
    stubReset(jsonResponse({ session_id: 'fresh-1', context_vis_url: 'http://127.0.0.1:4322', memory: idleMemory }))
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    expect(await screen.findByText('Session s1')).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Reset demo' }))
    await userEvent.click(screen.getByRole('button', { name: 'Wipe memory' }))
    expect(await screen.findByText('Session fresh-1')).toBeInTheDocument()
  })

  it('explains a failed reset', async () => {
    stubReset(jsonResponse({ detail: 'Could not wipe the memory folder: access denied' }, 500))
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    await userEvent.click(await screen.findByRole('button', { name: 'Reset demo' }))
    await userEvent.click(screen.getByRole('button', { name: 'Wipe memory' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Reset failed: Could not wipe the memory folder: access denied')
  })
})

describe('AgentPage memory status unavailable', () => {
  it('says so when the status cannot be read', async () => {
    vi.stubGlobal('fetch', vi.fn((url: string) =>
      url === '/api/sessions' ? Promise.resolve(jsonResponse({ session_id: 's1' })) : Promise.reject(new Error('down')),
    ))
    render(<AgentPage config={readyConfig} hidden={false} memoryPollMs={20} />)
    expect(await screen.findByRole('status')).toHaveTextContent('Memory: status unavailable')
  })
})
