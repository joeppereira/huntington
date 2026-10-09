import { useEffect, useRef, useState, type FormEvent } from 'react'
import { useChat } from '../hooks/useChat'
import { TurnCard } from './TurnCard'

interface ChatPanelProps {
  /** Called after each answered turn (the backend has just queued a memory sync). */
  onTurnCompleted?: () => void
  /** Adopt this backend session instead of creating one. */
  initialSessionId?: string
}

export function ChatPanel({ onTurnCompleted, initialSessionId }: ChatPanelProps = {}) {
  const { sessionId, entries, pendingQuestion, error, ask, newSession } = useChat(initialSessionId)
  const [draft, setDraft] = useState('')
  const endRef = useRef<HTMLDivElement>(null)
  const busy = pendingQuestion !== null
  const canSend = sessionId !== null && !busy && draft.trim().length > 0

  useEffect(() => {
    endRef.current?.scrollIntoView?.({ behavior: 'smooth', block: 'end' })
  }, [entries.length, pendingQuestion])

  const submit = async (question: string) => {
    if (await ask(question)) {
      setDraft('')
      onTurnCompleted?.()
    }
  }

  const onSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (canSend) void submit(draft.trim())
  }

  return (
    <div className="chat">
      <div className="chat__toolbar">
        <span className="chat__session">{sessionId ? `Session ${sessionId}` : 'Starting session…'}</span>
        <button type="button" className="button button--secondary" onClick={() => void newSession()} disabled={busy}>
          New session
        </button>
      </div>

      <div className="chat__log">
        {entries.length === 0 && !busy ? (
          <p className="chat__empty">Ask about Meridian Harbor's reports, models or APIs.</p>
        ) : null}
        {entries.map(({ question, turn }) => (
          <div key={turn.turn} className="chat__exchange">
            <p className="chat__question">{question}</p>
            <TurnCard turn={turn} onAsk={(q) => void submit(q)} disabled={busy} />
          </div>
        ))}
        {busy ? (
          <div className="chat__exchange">
            <p className="chat__question">{pendingQuestion}</p>
            <p className="chat__pending">Searching the wiki…</p>
          </div>
        ) : null}
        <div ref={endRef} />
      </div>

      {error ? (
        <p className="chat__error" role="alert">
          {error}
        </p>
      ) : null}

      <form className="chat__form" onSubmit={onSubmit}>
        <textarea
          aria-label="Ask a question"
          className="chat__input"
          value={draft}
          rows={2}
          disabled={sessionId === null}
          placeholder="e.g. Which APIs feed the CECL model?"
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) onSubmit(e)
          }}
        />
        <button type="submit" className="button" disabled={!canSend}>
          Send
        </button>
      </form>
    </div>
  )
}
