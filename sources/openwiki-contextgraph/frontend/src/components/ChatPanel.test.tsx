import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { chatTurn, jsonResponse } from '../test/fixtures'
import { ChatPanel } from './ChatPanel'

type Handler = (url: string, init?: RequestInit) => Response | Promise<Response>

function stubApi(handler: Handler) {
  const fn = vi.fn((url: string, init?: RequestInit) => Promise.resolve(handler(url, init)))
  vi.stubGlobal('fetch', fn)
  return fn
}

const sessionThen = (chat: Handler): Handler => (url, init) =>
  url === '/api/sessions' ? jsonResponse({ session_id: chatTurn.session_id }) : chat(url, init)

describe('ChatPanel', () => {
  it('starts a session on mount and sends questions with it', async () => {
    const fetchMock = stubApi(sessionThen(() => jsonResponse(chatTurn)))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, 'What is CET1?')
    await userEvent.click(screen.getByRole('button', { name: /^send$/i }))

    expect(await screen.findByText('15.1%')).toBeInTheDocument()
    expect(screen.getByText('What is CET1?')).toBeInTheDocument()
    const chatCall = fetchMock.mock.calls.find(([url]) => url === '/api/chat')
    expect(JSON.parse(String(chatCall?.[1]?.body))).toEqual({ session_id: chatTurn.session_id, message: 'What is CET1?' })
    expect(input).toHaveValue('')
  })

  it('shows a pending state and blocks double sends', async () => {
    let release: (r: Response) => void = () => {}
    stubApi(sessionThen(() => new Promise<Response>((resolve) => (release = resolve))))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, 'q1{Enter}')
    expect(await screen.findByText(/searching the wiki/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^send$/i })).toBeDisabled()
    release(jsonResponse(chatTurn))
    expect(await screen.findByText('15.1%')).toBeInTheDocument()
  })

  it('shows the backend error and keeps the question for retry', async () => {
    stubApi(sessionThen(() => jsonResponse({ detail: 'The agent failed: overloaded' }, 502)))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, 'q1{Enter}')
    expect(await screen.findByRole('alert')).toHaveTextContent('The agent failed: overloaded')
    expect(input).toHaveValue('q1')
  })

  it('does not send blank messages', async () => {
    const fetchMock = stubApi(sessionThen(() => jsonResponse(chatTurn)))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, '   ')
    expect(screen.getByRole('button', { name: /^send$/i })).toBeDisabled()
    expect(fetchMock.mock.calls.filter(([url]) => url === '/api/chat')).toHaveLength(0)
  })

  it('starts a fresh session on "New session"', async () => {
    const fetchMock = stubApi(sessionThen(() => jsonResponse(chatTurn)))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, 'q1{Enter}')
    await screen.findByText('15.1%')
    await userEvent.click(screen.getByRole('button', { name: /new session/i }))
    await waitFor(() => expect(screen.queryByText('15.1%')).not.toBeInTheDocument())
    expect(fetchMock.mock.calls.filter(([url]) => url === '/api/sessions')).toHaveLength(2)
  })

  it('rejects a malformed chat response', async () => {
    stubApi(sessionThen(() => jsonResponse({ answer: 42 })))
    render(<ChatPanel />)
    const input = await screen.findByRole('textbox', { name: /ask a question/i })
    await waitFor(() => expect(input).toBeEnabled())
    await userEvent.type(input, 'q1{Enter}')
    expect(await screen.findByRole('alert')).toHaveTextContent(/unexpected shape/i)
  })
})
