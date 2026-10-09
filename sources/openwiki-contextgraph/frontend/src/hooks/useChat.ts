import { useCallback, useEffect, useState } from 'react'
import { createSession, sendChat, type ChatTurn } from '../api'

export interface ChatEntry {
  question: string
  turn: ChatTurn
}

interface ChatState {
  sessionId: string | null
  entries: ChatEntry[]
  pendingQuestion: string | null
  error: string | null
}

const INITIAL: ChatState = { sessionId: null, entries: [], pendingQuestion: null, error: null }

const message = (err: unknown) => (err instanceof Error ? err.message : String(err))

/**
 * One chat session: created on mount and on newSession(); the session id lives only in memory.
 * `initialSessionId` adopts a session the backend already created (e.g. by a demo reset).
 */
export function useChat(initialSessionId?: string) {
  const [state, setState] = useState<ChatState>(INITIAL)

  const newSession = useCallback(async () => {
    setState(INITIAL)
    try {
      const sessionId = await createSession()
      setState((s) => ({ ...s, sessionId }))
    } catch (err) {
      setState((s) => ({ ...s, error: `Could not start a session: ${message(err)}` }))
    }
  }, [])

  useEffect(() => {
    if (initialSessionId) {
      setState({ ...INITIAL, sessionId: initialSessionId })
    } else {
      void newSession()
    }
  }, [newSession, initialSessionId])

  const ask = useCallback(
    async (question: string): Promise<boolean> => {
      const sessionId = state.sessionId
      if (!sessionId || state.pendingQuestion || !question.trim()) return false
      setState((s) => ({ ...s, pendingQuestion: question, error: null }))
      try {
        const turn = await sendChat(sessionId, question)
        setState((s) => ({ ...s, entries: [...s.entries, { question, turn }], pendingQuestion: null }))
        return true
      } catch (err) {
        setState((s) => ({ ...s, pendingQuestion: null, error: message(err) }))
        return false
      }
    },
    [state.sessionId, state.pendingQuestion],
  )

  return { ...state, ask, newSession }
}
